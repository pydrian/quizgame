from django.contrib import admin
from .models import Question, Answer, Game, User, Rank

admin.site.register(Question)
admin.site.register(Game)
admin.site.register(Answer)
admin.site.register(Rank)
