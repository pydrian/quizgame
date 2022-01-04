from rest_framework import serializers
from .models import Game, Question, Answer, User


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields ='__all__'


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['choiceid', 'quest', 'variant']
