from account.models import Musician, User
from django import template
from event.models import Interest, Invitation
from account.models import Musician, Troupe

register = template.Library()


@register.simple_tag
def get_request_status(event_id, user):
    user = User.objects.get(id=user.id)
    if user.groups.filter(name='Musician').exists():
        musician = Musician.objects.get(user__id=user.id)
        if Invitation.objects.filter(event=event_id,musician=musician).exists() or Interest.objects.filter(event=event_id,musician=musician).exists():
            try:
                invitation = Invitation.objects.get(event=event_id,musician=musician)            
                context = {
                    'invitation' : True,
                    'invitation_sent_id' : invitation.id,
                    'last_message' :invitation.get_last_message()
                }
            except:
                interest = Interest.objects.get(event=event_id,musician=musician)            
                context = {
                    'interest' : True,
                    'interest_sent_id' : interest.id,
                    'last_message' :interest.get_last_message()
                }
        else:
              context = {
                'invitation' : False,
                'interest' : False,
            }        
        return context
    elif user.groups.filter(name='Troupe').exists():
        troupe = Troupe.objects.get(user__id=user.id)
        if Invitation.objects.filter(event=event_id,troupe=troupe).exists() or Interest.objects.filter(event=event_id,troupe=troupe).exists():
            try:
                invitation = Invitation.objects.get(event=event_id,troupe=troupe)            
                context = {
                    'invitation' : True,
                    'invitation_sent_id' : invitation.id,
                    'last_message' :invitation.get_last_message()
                }
            except:
                interest = Interest.objects.get(event=event_id,troupe=troupe)            
                context = {
                    'interest' : True,
                    'interest_sent_id' : interest.id,
                    'last_message' :interest.get_last_message()
                }
        else:
              context = {
                'invitation' : False,
                'interest' : False,
            }        
        return context