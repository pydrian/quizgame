import re
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

EMAIL_ALG = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


class Validator:
    def __init__(self):
        self.mapping = {}

    def map_field(self, fieldname, fieldtype, 
        required: bool = False, min_len=None, max_len=None, allowed: list = []):

        self.mapping[fieldname] = {
            'fieldtype': fieldtype,
            'required': required,
            'max_len': max_len,
            'min_len': min_len,
            'allowed': allowed
        }
    
    def validate(self, payload):
        validated = {}
        for field in self.mapping:
            if field not in payload:
                if self.mapping[field]['required']:
                    raise serializers.ValidationError(f"{field} is required")
                continue

            if self.mapping[field]['fieldtype'] == 'email':
                if not re.fullmatch(EMAIL_ALG, str(payload[field])):
                    raise serializers.ValidationError("Email is not valid")
                validated[field] = payload[field]
                continue
            
            if not isinstance(payload[field], self.mapping[field]['fieldtype']):
                raise serializers.ValidationError(f"{field} must be of type {self.mapping[field]['fieldtype']}")
            
            if self.mapping[field]['max_len']:
                if len(payload[field]) < self.mapping[field]['min_len']\
                    or len(payload[field]) > self.mapping[field]['max_len']:
                    raise serializers.ValidationError(
                        f"{field} has constraint length greater than {self.mapping[field]['min_len']}, less than {self.mapping[field]['max_len']}"
                    )

            if field == 'password':
                validated[field] = make_password(payload[field])
                continue
            
            if not self.mapping[field]['allowed']:
                validated[field] = payload[field]
                continue
            
            if not payload[field] in self.mapping[field]['allowed']:
                raise serializers.ValidationError(f"{field} has allowed values constraint: {self.mapping[field]['allowed']}")

            validated[field] = payload[field]

        return validated
