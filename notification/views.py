from rest_framework.response import Response
from rest_framework.generics import mixins
from rest_framework.viewsets import GenericViewSet

from notification.serializers import NotificationSerializer
from notification.models import Notification


class NotificationsView(mixins.ListModelMixin, mixins.UpdateModelMixin, GenericViewSet):

    def list(self, request, *args, **kwargs):
        received_notifications = request.user.received_notifications.filter(is_read=False)
        serializer = NotificationSerializer(received_notifications, many=True)
        return Response(serializer.data)

    def update(self, request, pk):
        notification = Notification.objects.filter(created_for=request.user).get(pk=pk)
        notification.is_read = True
        notification.save()

        return Response({'message': 'notification read'})

