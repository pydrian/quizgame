# Generated by Django 4.0 on 2021-12-24 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapp', '0003_rename_qid_choices_quest'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='points',
            field=models.IntegerField(default=5),
        ),
    ]
