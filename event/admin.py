from django.contrib import admin
from .models import Event, Invitation, Interest, Event_Skill, Pin_Event
from import_export.admin import ImportExportModelAdmin

admin.site.register(Event)

@admin.register(Invitation)
class InvitationModelAdmin(ImportExportModelAdmin):    
    list_display = ['event','invitation_to']


admin.site.register(Interest)
admin.site.register(Event_Skill)
admin.site.register(Pin_Event)
