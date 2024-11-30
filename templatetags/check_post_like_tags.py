from django import template
from account.models import Post, Chat

register = template.Library()

@register.simple_tag
def get_rate(crit, rates):
    return rates.get(crit=crit).rate

  

@register.simple_tag
def get_post_like_status(post_id, user):

    if Post.objects.filter(id=post_id,user_likes=user).exists():
        return True
    else:
        return False


@register.simple_tag
def count_unread_chat(conversation_id,user):
    count = Chat.objects.filter(conversation__id=conversation_id,unread=True).exclude(sender=user).count()
    return count




@register.simple_tag
def count_read_chat(conversation_id,user):
    count = Chat.objects.filter(conversation__id=conversation_id,unread=False).exclude(sender=user).count()
    return count

@register.simple_tag
def count_my_unread(post_id,user):
    count = Message.objects.filter(interest__post__id=post_id,unread=True).exclude(message_by=user).count()
    return count

@register.simple_tag
def count_int_unread(post_id,user):
    interest = Interest.objects.get(post__id=post_id,shown_by=user)
    count = Message.objects.filter(interest=interest,unread=True).exclude(message_by=user).count()
    return count


@register.simple_tag
def check_interest(post_id,user):
    if Interest.objects.filter(post__id=post_id,shown_by=user).exists():
        return True
    else:
        return False


