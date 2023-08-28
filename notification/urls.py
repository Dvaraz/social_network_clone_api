from django.urls import path

from notification.views import NotificationsView


urlpatterns = [
    path('', NotificationsView.as_view({"get": "list"}), name='notifications'),
    path('read/<uuid:pk>/', NotificationsView.as_view({"post": "update"}), name='notifications_read'),
]
