from django.urls import path

from chat.views import ConversationListView, ConversationDetail, ConversationSendMessage, ConversationGetCreate


urlpatterns = [
    path('', ConversationListView.as_view(), name='conversation_list'),
    path('<uuid:id>/', ConversationDetail.as_view(), name='conversation_detail'),
    path('<uuid:id>/send/', ConversationSendMessage.as_view(), name='conversation_send_message'),
    path('<uuid:user_pk>/getOrCreate/', ConversationGetCreate.as_view(), name='conversation_get_or_create'),
]
