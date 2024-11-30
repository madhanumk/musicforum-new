from django import forms
from .models import Event
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
        fields = ['name','event_type','event_category','event_details','highlight','location','from_date','to_date','venue','poster_image','registration_close_date','self_reference','x','y','width', 'height','auto_accept']
    
    def __init__(self, *args, **kwargs):
        super(Event_Form, self).__init__(*args, **kwargs)
        self.fields['self_reference'].label = "Limited to personal invitation, No other registration allowed."
        self.fields['event_details'].widget.attrs['rows'] = 3
        self.fields['highlight'].widget.attrs['rows'] = 3
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Event Name'
        self.fields['x'].required = False
        self.fields['y'].required = False       
        self.fields['width'].required = False
        self.fields['height'].required = False
        self.fields["event_type"].choices = [("", "Choose Event Type"),] + \
            list(self.fields["event_type"].choices)[1:]
        self.fields["event_category"].choices = [("", "Choose Event Category"),] + \
            list(self.fields["event_category"].choices)[1:]
        self.fields["location"].choices = [("", "Choose Location"),] + \
            list(self.fields["location"].choices)[1:]
        




    def save(self, **kwargs):
        event = super(Event_Form, self).save()

        if 'poster_image' in self.changed_data:
            x = self.cleaned_data.get('x')
            y = self.cleaned_data.get('y')
            w = self.cleaned_data.get('width')
            h = self.cleaned_data.get('height')
            image = Image.open(event.poster_image)
            cropped_image = image.crop((x, y, w+x, h+y))
            resized_image = cropped_image.resize((1803, 769), Image.ANTIALIAS)
            resized_image.save(event.poster_image.path)
        return event