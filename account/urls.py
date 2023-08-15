from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from account.views import SingUp
from account.views import UserMe


urlpatterns = [
    path('me/', UserMe.as_view(), name='me'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SingUp.as_view(), name='signup'),
]
