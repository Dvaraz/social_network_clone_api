from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.models import Conversation, ConversationMessage
from chat.serializers import ConversationSerializer, ConversationMessageSerializer, ConversationDetailSerializer
from account.models import User


class ConversationListView(ListAPIView):

    def get_queryset(self):
        conversations = Conversation.objects.filter(users__in=list([self.request.user]))
        return conversations

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ConversationSerializer(queryset, many=True)
        return Response(serializer.data)


class ConversationDetail(APIView):
    def get(self, request, id):
        conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=id)
        serializer = ConversationDetailSerializer(conversation)

        return Response(serializer.data)


class ConversationGetCreate(APIView):
    def get(self, request, user_pk):
        user = User.objects.get(pk=user_pk)

        conversations = Conversation.objects.filter(users__in=list([request.user])).filter(users__in=list([user]))

        if conversations.exists():
            conversation = conversations.first()
        else:
            conversation = Conversation.objects.create()
            conversation.users.add(user, request.user)
            conversation.save()

        serializer = ConversationDetailSerializer(conversation)

        return Response(serializer.data)


class ConversationSendMessage(APIView):
    def post(self, request, id):
        conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=id)

        for user in conversation.users.all():
            if user != request.user:
                sent_to = user

        conversation_message = ConversationMessage.objects.create(
            conversation=conversation,
            body=request.data.get('body'),
            created_by=request.user,
            sent_to=sent_to
        )
        serializer = ConversationMessageSerializer(conversation_message)

        return Response(serializer.data)
