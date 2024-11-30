from __future__ import unicode_literals
from django.db import models

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from .managers import UserManager
import urllib.parse as urlparse
from django.db.models import Q
from django.core.exceptions import ValidationError
import datetime



# Create your models here.
gender_options = (('','Choose Gender'),('M','Male'),('F','Female'),('T','Transgender'),('N','None'))
key_performer_options = (('','Choose '),('A','Accept'),('R','Reject'),('S','Sent'))
musician_gurukulam_options = (('','Choose '),('A','Accept'),('R','Reject'),('S','Sent'))
request_status_options = (('','Choose Status'),('A','Accept'),('R','Reject'),('S','Sent'))


class Location(models.Model):
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name


class Skill_Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name
    


class Skill(models.Model):
    skill_name = models.CharField(max_length=50)
    skill_category = models.ForeignKey(Skill_Category,on_delete=models.CASCADE)


    def __str__(self):
        return str(self.skill_name)

class Skill_Level(models.Model):
    level = models.CharField(max_length=50)

    def __str__(self):
        return self.level


class Highlight_Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=60, unique=True)    
    first_name = models.CharField(_('first name'), max_length=250, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    name =  models.CharField(_('name'), max_length=400, blank=True)
    email = models.EmailField(_('email address'),unique=True,null=True )
    verified_email=models.BooleanField(default=False)    
    registered_on = models.DateTimeField(_('date joined'), auto_now_add=True)       
    address = models.TextField(blank=True,null=True)
    mobile_no = models.CharField(max_length=10,blank=True,null=True)    
    location = models.ForeignKey(Location, on_delete=models.CASCADE,blank=True,null=True)
    profile_picture = models.ImageField(blank=True,null=True)
    cover_picture = models.ImageField(blank=True,null=True)
    registered_on = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True) 
    is_staff=models.BooleanField(default=False)
    groups = models.ManyToManyField(Group)
    instagram = models.URLField(max_length=200,null=True,blank=True)
    twitter = models.URLField(max_length=200,null=True,blank=True)
    webtour = models.BooleanField(default=False)
    email_subscription = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        if self.first_name:
            return self.first_name        
        elif self.name:
            return self.name
        else:
            return self.username
        
    @property
    def group(self):
        group = self.groups.all()[0]
        return str(group)

    def picture(self):
        if self.profile_picture:
            picture = self.profile_picture
        elif self.cover_picture:
            picture = self.cover_picture
        else:
            picture = None
        return picture

    def get_full_name(self):
        if self.first_name:
            full_name = '%s %s' % (self.first_name, self.last_name)
        else:
            full_name = self.name
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def following_count(self):
        count= UserFollowing.objects.filter(user=self.id).count()
        return str(count)

    def followers_count(self):
        count= UserFollowing.objects.filter(following_user_id=self.id).count()
        return str(count)

    def events_count(self):
        group = self.groups.all()[0]
        if str(group) == "Musician":
            invitation = Invitation.objects.filter(status="A",musician__user__id=self.id).count()
            interest = Interest.objects.filter(status="A",musician__user__id=self.id).count()
            return invitation+interest
        elif str(group) == "Event Organizer":
            event = Event.objects.filter(event_organizer__user__id=self.id).count()
            return event
        
    def update_location(user,location_id):
        data  = dict()

        try:
            location  = Location.objects.get(id=location_id)
        except:
            location = None

        if location:
            user  = user
            user.location= location
            user.save()
            data['updated'] = True
        else:
            data['updated'] = False
            data['error_message'] = "Location is not available"
            
        return data

'''class Instrument(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name'''

class Music_Lover(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="music_lover")
    dob = models.DateField(help_text="Date of Birth",null=True,blank=True)
    gender = models.CharField(choices=gender_options,max_length=1,null=True)
    def __str__(self):
        return str(self.user)

    def full_name(self):
        return str(self.user)

class Musician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="musician")
    dob = models.DateField(help_text="Date of Birth",null=True,blank=True)
    gender = models.CharField(choices=gender_options,max_length=1,null=True)
    profession  = models.CharField(max_length=50)
    about_me = models.TextField()

    def __str__(self):
        return str(self.user)

    def full_name(self):
        return str(self.user)


    def interest_count(self):
        count = Interest.objects.filter(musician=self.user.musician).count() 
        return count 

    def interest_accepted_count(self):
        count = Interest.objects.filter(status="A",musician=self.user.musician).count()
        return count


    def interest_rejected_count(self):
        count = Interest.objects.filter(status="R",musician=self.user.musician).count()
        return count

    def pending_interest_count(self):
        count = Interest.objects.filter(status="S",musician=self.user.musician).count()
        return count


    def invitation_count(self):
        count = Invitation.objects.filter(musician=self.user.musician).count()
        return count


    def accepted_invitation_count(self):
        count = Invitation.objects.filter(musician=self.user.musician,status="A").count()
        return count



    def rejected_invitation_count(self):
        count = Invitation.objects.filter(musician=self.user.musician,status="R").count()
        return count


    
    def pending_invitation_count(self):
        count = Invitation.objects.filter(musician=self.user.musician,status="S").count()
        return count



class Musician_Skill(models.Model):
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE,related_name='musician_skill')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    skill_level = models.ForeignKey(Skill_Level, on_delete=models.CASCADE)
    teach = models.BooleanField(default=False)
    perform = models.BooleanField(default=False)


    def __str__(self):
        return str(self.skill)


class Highlight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="highlight")
    title = models.CharField(max_length=100)
    video_link = models.URLField(max_length=200)
    description = models.TextField(null=True)

    def __str__(self):
        return self.title

    def video_id(self):
        url_data = urlparse.urlparse(self.video_link)
        query = urlparse.parse_qs(url_data.query)
        try:
            video = query["v"][0]
        except:
            video = self.video_link
        return str(video)


class Musician_Highlight(models.Model):
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    video_link = models.URLField(max_length=200)
    highlight_category = models.ManyToManyField(Highlight_Category)

    def __str__(self):
        return self.title

    def video_id(self):
        url_data = urlparse.urlparse(self.video_link)
        query = urlparse.parse_qs(url_data.query)
        try:
            video = query["v"][0]
        except:
            video = self.video_link
        return str(video)


class Gurukulam(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=10, null=True, blank= True)
    about_us= models.TextField(blank=True)
    website = models.URLField(max_length=200,null=True,blank=True)

    def __str__(self):
        return str(self.user)
    
    def full_name(self):
        return str(self.user)


class Gurukulam_Teacher(models.Model):
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE)
    gurukulam = models.ForeignKey(Gurukulam,on_delete=models.CASCADE)    
    status = models.CharField(choices=musician_gurukulam_options,max_length=1,null=True) 
    sender = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.musician) + ' - ' + str(self.gurukulam)


class Musician_Gurukulam(models.Model):
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE,related_name="gurukulas")
    gurukulam = models.ForeignKey(Gurukulam,on_delete=models.CASCADE)    
    status = models.CharField(choices=musician_gurukulam_options,max_length=1,null=True) 
    sender = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.gurukulam)


class Musician_Award(models.Model):
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE,related_name='musician_award')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='musician_award',null=True)

    def __str__(self):
        return self.title


class Troupe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="troupe")
    president =  models.CharField(max_length=100,blank=True)
    about_us = models.TextField(blank=True)

    def __str__(self):
        return str(self.user)
    
    def full_name(self):
        return str(self.user)


    def interest_count(self):
        count = Interest.objects.filter(troupe=self.user.troupe).count() 
        return count 

    def interest_accepted_count(self):
        count = Interest.objects.filter(status="A",troupe=self.user.troupe).count()
        return count


    def interest_rejected_count(self):
        count = Interest.objects.filter(status="R",troupe=self.user.troupe).count()
        return count

    def pending_interest_count(self):
        count = Interest.objects.filter(status="S",troupe=self.user.troupe).count()
        return count


    def invitation_count(self):
        count = Invitation.objects.filter(troupe=self.user.troupe).count()
        return count


    def accepted_invitation_count(self):
        count = Invitation.objects.filter(troupe=self.user.troupe,status="A").count()
        return count


    def rejected_invitation_count(self):
        count = Invitation.objects.filter(troupe=self.user.troupe,status="R").count()
        return count


    
    def pending_invitation_count(self):
        count = Invitation.objects.filter(troupe=self.user.troupe,status="S").count()
        return count



class Troupe_Skill(models.Model):
    troupe = models.ForeignKey(Troupe, on_delete=models.CASCADE,related_name="troupe_skill")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.skill)


class Troupe_Highlight(models.Model):
    troupe = models.ForeignKey(Troupe,on_delete=models.CASCADE)
    title = models.CharField(max_length=400)
    video_link = models.URLField(max_length=200)
    highlight_category = models.ManyToManyField(Highlight_Category)

    def __str__(self):
        return self.title 

    def video_id(self):
        url_data = urlparse.urlparse(self.video_link)
        query = urlparse.parse_qs(url_data.query)
        try:
            video = query["v"][0]
        except:
            video = self.video_link
        return str(video)

class Key_Performer(models.Model):
    troupe = models.ForeignKey(Troupe, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True,blank=True)
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE,blank=True,null=True)
    profile_photo = models.ImageField(blank=True)
    status = models.CharField(choices=key_performer_options,max_length=1,null=True) 

    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.musician.user)

    class Meta:
        ordering = ('-id',)


class Gurukulam_Skill(models.Model):
    gurukulam = models.ForeignKey(Gurukulam, on_delete=models.CASCADE,related_name="gurukulam_skill")
    skill = models.ForeignKey(Skill,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.skill)
        
    @property
    def skill_name(self):
        return str(self.skill.skill_name)


    class Meta:
        ordering = ('-id',)


class Course(models.Model):
    gurukulam =  models.ForeignKey(Gurukulam, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100)
    age_limit = models.PositiveIntegerField()
    overview = models.TextField()
    prerequisite = models.TextField()
    learning_outcome =  models.TextField()
    others = models.TextField()


    def __str__(self):
        return self.topic


    class Meta:
        ordering = ('-id',)


class Lecture_Video(models.Model):
    gurukulam = models.ForeignKey(Gurukulam, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video = models.URLField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-id',)

    def video_id(self):
        url_data = urlparse.urlparse(self.video)
        query = urlparse.parse_qs(url_data.query)
        try:
            video = query["v"][0]
        except:
            video = self.video
        return str(video)
    

class Gurukulam_Award(models.Model):
    gurukulam = models.ForeignKey(Gurukulam, on_delete=models.CASCADE,related_name="gurukulam_award")
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="gurukulam/award")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-id',)


class Gurukulam_Testimonial(models.Model):
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE)
    gurukulam = models.ForeignKey(Gurukulam, on_delete=models.CASCADE)
    testimonial = models.TextField()

    class Meta:
        ordering = ('-id',)


class Event_Organizer(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    about_us = models.TextField(blank=True)
    website = models.URLField(max_length=200,null=True,blank=True)


    def __str__(self):
        return str(self.user)


class Event_Performer(models.Model):
    event_organizer =  models.ForeignKey(Event_Organizer,on_delete=models.CASCADE)
    musician =  models.ForeignKey(Musician,on_delete=models.CASCADE,blank=True,null=True)
    troupe =  models.ForeignKey(Troupe,on_delete=models.CASCADE,blank=True,null=True)
    status = models.CharField(choices=request_status_options,max_length=1,default="A")

     

class Event_Organizer_Highlight(models.Model):
    event_organizer = models.ForeignKey(Event_Organizer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    video_link = models.URLField(max_length=200)
    highlight_category = models.ManyToManyField(Highlight_Category)

    def __str__(self):
        return self.title

    def video_id(self):
        url_data = urlparse.urlparse(self.video_link)
        query = urlparse.parse_qs(url_data.query)
        try:
            video = query["v"][0]
        except:
            video = self.video_link
        return str(video)

    class Meta:
        ordering = ['-id']




class UserFollowing(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User,on_delete=models.CASCADE, related_name="following")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    def follow_or_unfollow(user,following_user_id):
        if UserFollowing.objects.filter(user=user,following_user_id=following_user_id).exists():
            UserFollowing.objects.get(user=user,following_user_id=following_user_id).delete()
            return False
        else:
            UserFollowing.objects.create(user=user,following_user_id=following_user_id)
            return True
            
class Report_People(models.Model):
    reported_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="reported_by")
    reported_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="reports")
    reported_on = models.DateField(auto_now=True)
    complaint = models.TextField(blank=True)
    report_file = models.FileField(upload_to="report file",blank=True)
    is_active = models.BooleanField(default=True)

    def delete(id):
        Report_People.objects.filter(id=id).delete()    
        return True

    def skip_all_reports(user):
        Report_People.objects.filter(reported_user__id=user).update(is_active=False)
        return True

    class Meta:
        ordering = ['-id']


from event.models import Invitation, Interest, Event

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="posted_by")
    content = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Location,on_delete=models.CASCADE,null=True,)
    invitation = models.ForeignKey(Invitation,on_delete=models.CASCADE,null=True,blank=True)
    interest = models.ForeignKey(Interest,on_delete=models.CASCADE,null=True,blank=True)
    highlight = models.ForeignKey(Highlight,on_delete=models.CASCADE,null=True,blank=True)
    likes = models.PositiveIntegerField(default=0)
    user_likes = models.ManyToManyField(User,blank=True)

    @property
    def comment_count(self):
        count = Post_Comment.objects.filter(post=self.id).count()
        return count
    
    @property
    def like_count(self):
        return self.user_likes.count()


    def like_or_unlike(id,user):
        if Post.objects.filter(id=id,user_likes=user).exists():
            post = Post.objects.get(id=id)
            post.user_likes.remove(user)
            return False
        else:
            post = Post.objects.get(id=id)
            post.user_likes.add(user)
            return True
        
    def people_liked(self):
        accepted_musician_list = list(Interest.objects.filter(event=self,status="A").values_list('musician__user__id',flat=True)) 
        accepted_troupe_list = list(Interest.objects.filter(event=self,status="A").values_list('troupe__user__id',flat=True)) 
        accepted_musician_list_1 = list(Invitation.objects.filter(event=self,status="A").values_list('musician__user__id',flat=True)) 
        accepted_troupe_list_1 = list(Invitation.objects.filter(event=self,status="A").values_list('troupe__user__id',flat=True))
        final_list = accepted_musician_list + accepted_troupe_list + accepted_musician_list_1 + accepted_troupe_list_1
        final_list = [i for i in final_list if i is not None]
        users = User.objects.filter(id__in=final_list)
      
        return users
    


    class Meta:
        ordering = ['-id']
    


class Post_Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    comment = models.TextField()
    commented_on = models.DateTimeField(auto_now_add=True)


class Reply(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    created = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(Post_Comment,on_delete=models.CASCADE)
    reply = models.TextField(max_length=1000)


class Conversation(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,related_name="receiver")
    date = models.DateTimeField(auto_now=True)


    @property
    def get_last_message(self):
        chat  = Chat.objects.filter(conversation=self).last()
        return chat.message


class Chat(models.Model):
    conversation =  models.ForeignKey(Conversation, on_delete=models.CASCADE,null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    message = models.TextField()
    unread = models.BooleanField(default=True)
    m_file = models.FileField(upload_to="message_file",null=True,blank=True)

    def save(self, receiver, force_insert=False, force_update=False):
        try:
            conversation =  Conversation.objects.get(Q(sender=self.sender,receiver=receiver) | Q(sender=receiver,receiver=self.sender))
        except:
            conversation,created= Conversation.objects.get_or_create(sender=self.sender,receiver=receiver)

  

        self.conversation = conversation
        conversation.date=datetime.datetime.now()
        conversation.save()

        super(Chat, self).save(force_insert, force_update)
        
    @staticmethod    
    def unread_count(user):
        count = Chat.objects.filter(Q(conversation__sender=user,unread=True)|Q(conversation__receiver=user,unread=True)).exclude(sender=user).count()
        return count

    @staticmethod    
    def readed_count(user):
        count = Chat.objects.filter(Q(conversation__sender=user,unread=False)|Q(conversation__receiver=user,unread=False)).exclude(sender=user).count()
        return count


class Blocked_User(models.Model):
    blocked_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="blocked_by")
    blocked_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='blocked_user')


    def block_unblock(user,blocked_user):
        if Blocked_User.objects.filter(blocked_by=user,blocked_user=blocked_user).exists():
            Blocked_User.objects.get(blocked_by=user,blocked_user=blocked_user).delete()
            return False
        else:
            Blocked_User.objects.create(blocked_by=user,blocked_user=blocked_user)
            return True