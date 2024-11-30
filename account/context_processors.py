from event.models import Message
from account.models import Location
from account.models import Chat

#unread Message Count
def unread_message_count(request):

    try:
        return {'unread_message_count': Message.unread_count(request.user),'cities':Location.objects.all(),}
    except:
        return {'unread_message_count': 0,'cities':Location.objects.all(), }


#unread Chat Count
def unread_chat_count(request):

    try:
        return {'unread_chat_count': Chat.unread_count(request.user)}
    except:
        return {'unread_chat_count': 0 }