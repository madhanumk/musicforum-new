from django import forms
from django.forms import fields
from .models import User, Musician, Music_Lover, Gurukulam, Troupe, Event_Organizer, Musician_Award, Musician_Highlight, Musician_Skill, Musician_Gurukulam, Gurukulam_Skill, Gurukulam_Award, Gurukulam_Testimonial, Lecture_Video, Course, Troupe_Highlight,Key_Performer, Event_Organizer_Highlight, Event_Performer, Highlight, Troupe_Skill, Report_People, Gurukulam_Teacher
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.widgets import PasswordInput, TextInput
from django.utils.safestring import mark_safe
from string import Template
from django.contrib.auth.models import Group
from PIL import Image
from django.db.models import Q
from django.core.exceptions import ValidationError




class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Mail Id','class' : 'reg_form_input_1 input email-input'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password','class' : 'reg_form_input_1 input password-input'}))
    

    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = 'Custom error, if you not verified kindly verify it'
        super(CustomAuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Email Address"


class Signup_Form(UserCreationForm): 

    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.exclude(name='Portal Admin'),widget=forms.CheckboxSelectMultiple(attrs={'class': "group"}))
    
    class Meta:
        model = User
        fields = ('first_name','last_name','email','password1', 'password2','groups','email_subscription')

    def __init__(self, *args, **kwargs):
        super(Signup_Form, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None
        self.fields['groups'].label = "Role"
        self.fields['email_subscription'].label = "Send me upcoming events"


class Gurukulam_Signup_Form(UserCreationForm):    
    class Meta:
        model = User
        fields = ('email','password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(Gurukulam_Signup_Form, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None




class Event_Organizer_Form(UserCreationForm):    
    class Meta:
        model = User
        fields = ('email','password1', 'password2',)


    def __init__(self, *args, **kwargs):
        super(Event_Organizer_Form, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None



class Troupe_Signup_Form(UserCreationForm):    
    class Meta:
        model = User
        fields = ('email','password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(Troupe_Signup_Form, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

class EditMusicianUserForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name','address', 'mobile_no','location','profile_picture','cover_picture','x','y','width','height','instagram','twitter' ]


    def __init__(self, *args, **kwargs):
        super(EditMusicianUserForm, self).__init__(*args, **kwargs)
        self.fields['x'].required = False
        self.fields['y'].required = False       
        self.fields['width'].required = False
        self.fields['height'].required = False

        self.fields["location"].choices = [("", "Choose Location"),] + \
            list(self.fields["location"].choices)[1:]


        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input is-fade'

class MusicianForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'} ))
   
    class Meta:
        model = Musician
        fields = ['dob','gender','profession', 'about_me']


    def __init__(self, *args, **kwargs):
        super(MusicianForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input is-fade'



class EditMusicLoverUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','address','location', 'mobile_no', 'profile_picture','cover_picture' ]
        labels = {
            'first_name' : "Name",
        }
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['address'].required = True
        self.fields['location'].required = True
        self.fields['mobile_no'].required = True
        self.fields['profile_picture'].required = True
        self.fields["location"].choices = [("", "Choose Location"),] + \
            list(self.fields["location"].choices)[1:]

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input is-fade'
        
class MusicLoverForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'} ))
   
    class Meta:
        model = Music_Lover
        fields = ['dob','gender']

    def __init__(self, *args, **kwargs):
        super(MusicLoverForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input is-fade'
   

class EditGurukulamUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','address','location', 'profile_picture','cover_picture' ]
        labels = {
            'first_name' : "Name",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['address'].required = True
        self.fields['location'].required = True
        self.fields['profile_picture'].required = True

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input is-fade'


class GurukulamForm(forms.ModelForm):
    class Meta:
        model = Gurukulam
        fields = ['phone_no','about_us']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_no'].required = True
        self.fields['about_us'].required = True

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input is-fade'



class Edit_Troupe_UserForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ['first_name','address','location','mobile_no', 'profile_picture','cover_picture' ]
        labels = {
            'first_name' : 'Name',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['address'].required = True
        self.fields['location'].required = True
        self.fields['profile_picture'].required = True
        self.fields['mobile_no'].required = True

        self.fields['x'].required = False
        self.fields['y'].required = False       
        self.fields['width'].required = False
        self.fields['height'].required = False

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input is-fade'




class Troup_Profile_Form(forms.ModelForm):
    class Meta:
        model = Troupe
        fields = ['president','about_us']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['president'].required = True
        self.fields['about_us'].required = True

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input is-fade'


class Edit_Event_Org_UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name','address','location','mobile_no', 'cover_picture','profile_picture' ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['address'].required = True
        self.fields['location'].required = True
        self.fields['cover_picture'].required = True
        self.fields['mobile_no'].required = True

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input is-fade'


class Event_Org_Profile_Form(forms.ModelForm):
    class Meta:
        model = Event_Organizer
        fields = ['about_us']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['about_us'].required = True

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input is-fade'


#Musician

class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        html =  Template("""<img src="$link"/>""")
        return mark_safe(html.substitute(link=value.url))



class Musician_Award_Form(forms.ModelForm):
    class Meta:
        model = Musician_Award
        fields = ['title', 'image']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(Musician_Award_Form, self).__init__(*args, **kwargs)


class Highlight_Form(forms.ModelForm):
    class Meta:
        model = Highlight
        fields = ['title', 'video_link','description']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(Highlight_Form, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input'



class Musician_Highlight_Form(forms.ModelForm):
    class Meta:
        model = Musician_Highlight
        fields = ['title', 'highlight_category','video_link']




class Musician_Skill_Form(forms.ModelForm):

    class Meta:
        model = Musician_Skill
        fields = ['skill','skill_level','teach','perform']
        labels = {
            "teach": "to teach",
            "perform":"to perform",
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(Musician_Skill_Form, self).__init__(*args, **kwargs)

class Musician_Gurukulam_Form(forms.ModelForm):
    class Meta:
        model = Musician_Gurukulam
        fields = ['gurukulam']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(Musician_Gurukulam_Form, self).__init__(*args, **kwargs)


class Gurukulam_Skill_Form(forms.ModelForm):
    class Meta:
        model = Gurukulam_Skill
        fields = ['skill',]




class Gurukulam_Award_Form(forms.ModelForm):
    class Meta:
        model = Gurukulam_Award
        fields = ['title','photo']


class Gurukulam_Testimonial_Form(forms.ModelForm):

    class Meta:
        model= Gurukulam_Testimonial
        fields =['musician','testimonial']

class Lecture_Video_Form(forms.ModelForm):

    class Meta:
        model = Lecture_Video
        fields = ['title','video']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(Lecture_Video_Form, self).__init__(*args, **kwargs)


class Course_Form(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['topic','age_limit','overview','prerequisite','learning_outcome','others']


class Troupe_Highlight_Form(forms.ModelForm):
    class Meta:
        model = Troupe_Highlight
        fields = ['title','video_link','highlight_category']


class Key_Performer_Form(forms.ModelForm):

    class Meta:
        model = Key_Performer
        fields = ['name','musician','profile_photo']


class Event_Organizer_Highlight_Form(forms.ModelForm):

    class Meta:
        model = Event_Organizer_Highlight
        fields = ['title','video_link','highlight_category']


class Event_Performer_Form(forms.ModelForm):
    class Meta:
        model = Event_Performer
        fields = ['musician', 'troupe']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(Event_Performer_Form, self).__init__(*args, **kwargs)
        self.fields["musician"].choices = [("", "Choose Musician"),] + \
             list(self.fields["musician"].choices)[1:]
        self.fields["troupe"].choices = [("", "Choose Troupe"),] + \
             list(self.fields["troupe"].choices)[1:]

    # this function will be used for the validation
    def clean(self):
 
        # data from the form is fetched using super function
        super(Event_Performer_Form, self).clean()
         
        # extract the musician and troupe field from the data
        musician = self.cleaned_data.get('musician')
        troupe = self.cleaned_data.get('troupe')

        if not musician and not troupe:            
                raise forms.ValidationError('Choose atleast one musician or troupe.')

        elif musician and not troupe:
            if Event_Performer.objects.filter(musician=musician,event_organizer=self.request.user.event_organizer).exists():
                raise forms.ValidationError('Already Added.')
        elif not musician and troupe:
            if Event_Performer.objects.filter(troupe=troupe,event_organizer=self.request.user.event_organizer).exists():
                raise forms.ValidationError('Already Added.')

        elif musician and troupe:
            if Event_Performer.objects.filter(Q(musician=musician,event_organizer=self.request.user.event_organizer) | Q(troupe=troupe,event_organizer=self.request.user.event_organizer)).exists():
                raise forms.ValidationError('Already Added.')

            return self.cleaned_data


class Troupe_Skill_Form(forms.ModelForm):
    class Meta:
        model = Troupe_Skill
        fields = ['skill']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(Troupe_Skill_Form, self).__init__(*args, **kwargs)
        self.fields["skill"].choices = [("", "Choose Skill"),] + \
             list(self.fields["skill"].choices)[1:]
             
             
class Report_People_Form(forms.ModelForm):
    class Meta:
        model = Report_People
        fields = ['complaint','report_file']

    def __init__(self,*args,post_data=None, **kwargs):
        self.request = kwargs.pop("request")              
        super(Report_People_Form, self).__init__(*args, **kwargs)


class Add_Musician_Form(forms.ModelForm):
    class Meta:
        model = Musician_Gurukulam
        fields = ['musician']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(Add_Musician_Form, self).__init__(*args, **kwargs)


class Add_Gurukulam_Teacher_Form(forms.ModelForm):
    class Meta:
        model = Gurukulam_Teacher
        fields = ['musician']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(Add_Gurukulam_Teacher_Form, self).__init__(*args, **kwargs)


class Add_Teacher_Gurukulam_Form(forms.ModelForm):
    class Meta:
        model = Gurukulam_Teacher
        fields = ['gurukulam']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(Add_Teacher_Gurukulam_Form, self).__init__(*args, **kwargs)