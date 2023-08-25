from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from account.views import SingUp, UserMe, SendFriendshipRequest, Friends, HandleRequest, EditProfile, EditPassword, ActivateEmail


urlpatterns = [
    path('me/', UserMe.as_view(), name='me'),
    path('signup/', SingUp.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('editprofile/', EditProfile.as_view(), name='editprofile'),
    path('editpassword/', EditPassword.as_view(), name='editpassword'),
    path('friends/<uuid:pk>/', Friends.as_view(), name='friends'),
    path('friends/<uuid:pk>/request/', SendFriendshipRequest.as_view(), name='send_friendship_request'),
    path('friends/<uuid:pk>/<str:status>/', HandleRequest.as_view(), name='handle_request'),
    path('activateemail/', ActivateEmail.as_view(), name='activateemail'),
]
