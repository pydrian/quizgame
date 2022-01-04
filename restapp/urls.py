from django.urls import path
from . import views

urlpatterns = [
    path('games/', views.GameCRUD.as_view()),
    path('users/', views.ManageUsers.as_view()),
    path('quests/', views.QuestionCRUD.as_view()),
    path('answers/', views.AnswerCRUD.as_view()),
    path('play/', views.Play.as_view()),
    path('points/', views.Points.as_view()),
    path('rank/', views.RankView.as_view())
]
