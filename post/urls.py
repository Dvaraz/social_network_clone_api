from django.urls import path

from post.views import PostListView, PostCreate, PostListProfile, PostLike


urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<uuid:id>/like/', PostLike.as_view(), name='post_like'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('profile/<uuid:id>/', PostListProfile.as_view(), name='post_list_profile'),
]
