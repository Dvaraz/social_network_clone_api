# Generated by Django 4.2.4 on 2023-08-24 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_alter_comment_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashtag', models.CharField(max_length=255)),
                ('occurrences', models.IntegerField()),
            ],
        ),
    ]
