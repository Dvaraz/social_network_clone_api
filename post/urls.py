from django.urls import path

from post.views import PostListView, PostCreate


urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('create/', PostCreate.as_view(), name='post_create'),
]
