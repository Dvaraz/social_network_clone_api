# Generated by Django 4.2.4 on 2023-08-22 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_user_friends_friendshiprequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friends_count',
            field=models.IntegerField(default=0),
        ),
    ]
