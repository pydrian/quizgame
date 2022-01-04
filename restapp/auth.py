from rest_framework_simplejwt.tokens import AccessToken
from .models import User


def get_current_user(request):
    access_token = AccessToken(request.headers['Authorization'].split(' ')[1])
    user = User.objects.get(id=access_token['user_id'])
    return user
