from django.urls import path

from post.views import PostListView, PostCreate, PostListProfile


urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('profile/<uuid:id>/', PostListProfile.as_view(), name='post_list_profile'),
]
