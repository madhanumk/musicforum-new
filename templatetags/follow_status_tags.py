from django import template
from account.models import UserFollowing

register = template.Library()


@register.simple_tag
def get_follow_status(user_id, user):

    if UserFollowing.objects.filter(following_user_id=user_id,user=user).exists():
        return True
    else:
        return False
