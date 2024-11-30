from django import forms
from .models import Event, Event_Type
from django.contrib.admin import widgets 
from PIL import Image


class Event_Form(forms.ModelForm):    
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    from_date = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime())  
    to_date = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime())
    registration_close_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'} ))
    

    
    class Meta:
        model = Event    
        fields = ['name','event_type','event_category','event_details','highlight','location','from_date','to_date','venue','poster_image','registration_close_date','self_reference','x','y','width', 'height','auto_accept','ticket_booking_link_1','ticket_booking_place']

        widgets = {
            'event_type': forms.RadioSelect,
            
        }
    
    def __init__(self, *args, **kwargs):
        super(Event_Form, self).__init__(*args, **kwargs)
        self.fields['self_reference'].label = "Limited to personal invitation, No other registration allowed."
        self.fields['ticket_booking_link_1'].label = "ticket booking link"
        self.fields['event_details'].widget.attrs['rows'] = 2
        self.fields['highlight'].widget.attrs['rows'] = 2
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Event Name'
        self.fields['x'].required = False
        self.fields['y'].required = False       
        self.fields['width'].required = False
        self.fields['height'].required = False
        self.fields["event_category"].choices = [("", "Choose Event Category"),] + \
            list(self.fields["event_category"].choices)[1:]
        self.fields["location"].choices = [("", "Choose Location"),] + \
            list(self.fields["location"].choices)[1:]    
        self.fields['event_category'].widget.attrs['class'] = "dropdown-item"
        self.fields['event_details'].widget.attrs['class'] = "textarea is-fade"
        self.fields['highlight'].widget.attrs['class'] = "textarea is-fade"
        self.fields['location'].widget.attrs['class'] = "dropdown-item"
        self.fields['name'].widget.attrs['class'] = "input"
        self.fields['registration_close_date'].widget.attrs['class'] = "input"
        self.fields['from_date'].widget.attrs['class'] = "input"
        self.fields['to_date'].widget.attrs['class'] = "input"
        self.fields['venue'].widget.attrs['class'] = "input"
        self.fields['ticket_booking_link_1'].widget.attrs['class'] = "input"
        self.fields['ticket_booking_place'].widget.attrs['class'] = "input"
        self.fields['event_type'].empty_label = None