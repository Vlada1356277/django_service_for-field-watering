# Generated by Django 5.0.4 on 2024-05-13 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bonds', '0003_user_auth_token_alter_user_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.AddField(
            model_name='user',
            name='esiaId',
            field=models.CharField(default='', max_length=40),
        ),
    ]
