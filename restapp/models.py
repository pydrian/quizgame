from django.db import models
from jsonfield import JSONField
from django.contrib.auth import get_user_model


User = get_user_model()


class Game(models.Model):
    gameid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.name}"


class Question(models.Model):
    questid = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    question = models.CharField(max_length=300)
    points = models.IntegerField(default=5)

    def __str__(self):
        return f"{self.question}"


class Answer(models.Model):
    choiceid = models.AutoField(primary_key=True)
    quest = models.ForeignKey(Question, on_delete=models.CASCADE)
    variant = models.CharField(max_length=80)
    status = models.BooleanField()

    def __str__(self):
        return f"{self.variant}"


class Rank(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING)
    quest = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    points = models.IntegerField(default=0)
