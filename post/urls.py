from django.urls import path

from post.views import PostListView, PostCreate, PostListProfile, PostLike, PostDetail, PostCreateComment, Trends


urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<uuid:id>/', PostDetail.as_view(), name='post_detail'),
    path('<uuid:id>/like/', PostLike.as_view(), name='post_like'),
    path('<uuid:id>/comment/', PostCreateComment.as_view(), name='post_create_comment'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('profile/<uuid:id>/', PostListProfile.as_view(), name='post_list_profile'),
    path('trends/', Trends.as_view(), name='get_trends'),
]


