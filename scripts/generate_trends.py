# -*- coding: utf-8 -*-

import django
import os
import sys

from datetime import timedelta, datetime
from collections import Counter
from django.utils import timezone


sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
django.setup()


from post.models import Post, Trend


def extract_hashtags(text):
    hashtag_list = []

    for word in text.split():
        if word[0] == '#':
            hashtag_list.append(word[1:])

    return hashtag_list


Trend.objects.all().delete()

trends = []
this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
twenty_four_hours = this_hour - timedelta(hours=24)


for post in Post.objects.filter(created_at__gte=twenty_four_hours):
    trends.extend(extract_hashtags(post.body))


for trend in Counter(trends).most_common(10):
    Trend.objects.create(hashtag=trend[0], occurrences=trend[1])



