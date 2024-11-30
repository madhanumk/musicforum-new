from django.db import models
from datetime import  date
from account.models import Gurukulam, Event_Organizer, Musician, Troupe, Location, Skill, User
from django.db.models import Q 
from django.urls import reverse
# Create your models here.
event_type_options = (('','Choose Event Type'),('C','Contest'),('N','Normal'))
request_status_options = (('','Choose Status'),('A','Accept'),('R','Reject'),('S','Sent'))


class Subscription_Type(models.Model):
    name = models.CharField(max_length=60)
    price = models.FloatField()
    days = models.PositiveIntegerField(null=True)


    def __str__(self):
        return self.name

class Subscription(models.Model):
    subscription_type =  models.ForeignKey(Subscription_Type,on_delete=models.CASCADE)
    gurukulam = models.ForeignKey(Gurukulam,on_delete=models.CASCADE,blank=True,null=True)
    event_organizer = models.ForeignKey(Event_Organizer,on_delete=models.CASCADE,blank=True,null=True)
    musician = models.ForeignKey(Musician,on_delete=models.CASCADE,blank=True,null=True)
    troupe = models.ForeignKey(Troupe,on_delete=models.CASCADE,blank=True,null=True)
    subscription_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=False)



class Event_Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Event_Type(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=300)
    event_type =  models.ForeignKey(Event_Type,on_delete=models.CASCADE)
    event_category = models.ForeignKey(Event_Category,on_delete=models.CASCADE)
    event_details = models.TextField()
    from_date = models.DateTimeField(null=True)
    to_date = models.DateTimeField(null=True)
    location = models.ForeignKey(Location,on_delete=models.CASCADE,null=True)
    created_on = models.DateTimeField(auto_now=True)    
    poster_image= models.ImageField(upload_to="event_poster",null=True,blank=True)
    registration_close_date = models.DateField(null=True)
    venue = models.CharField(max_length=255,null=True,blank=True)
    self_reference = models.BooleanField(default=False)
    gurukulam = models.ForeignKey(Gurukulam,on_delete=models.CASCADE,null=True,blank=True)
    event_organizer = models.ForeignKey(Event_Organizer,on_delete=models.CASCADE,null=True,blank=True)
    highlight = models.TextField(null=True)
    auto_accept = models.BooleanField(default=False)
    #event_video = models.URLField(max_length=200,null=True,blank=True)
    ticket_booking_link_1 = models.URLField(max_length=200, null=True,blank=True)
    ticket_booking_link_2 = models.URLField(max_length=200, null=True,blank=True)
    ticket_booking_place = models.CharField(max_length=255,null=True,blank=True)
    likes = models.PositiveIntegerField(default=0)
    user_likes = models.ManyToManyField(User,blank=True, related_name='liked_events')
    
   
                                                                                            

    def __str__(self):
        return self.name

    @property
    def like_count_property(self):
        return self.user_likes.count()
        
    def creator(self):
        if self.gurukulam:
            return self.gurukulam.user
        elif self.event_organizer:
            return self.event_organizer.user

    def participants(self):
        accepted_musician_list = list(Interest.objects.filter(event=self, status="A").values_list('musician__user__id', flat=True))
        accepted_troupe_list = list(Interest.objects.filter(event=self, status="A").values_list('troupe__user__id', flat=True))
        accepted_musician_list_1 = list(Invitation.objects.filter(event=self, status="A").values_list('musician__user__id', flat=True))
        accepted_troupe_list_1 = list(Invitation.objects.filter(event=self, status="A").values_list('troupe__user__id', flat=True))
        
        final_list = accepted_musician_list + accepted_troupe_list + accepted_musician_list_1 + accepted_troupe_list_1
        final_list = [i for i in final_list if i is not None]
        
        users = User.objects.filter(id__in=final_list)
      
        return users


    class Meta:
        ordering = ('-id', )

    def invitation_count(self):
        data = Event.objects.filter(id=self.id).annotate(count= models.Count('invitation__id')) 
        return data[0].count 

    def interest_count(self):
        data = Event.objects.filter(id=self.id).annotate(count= models.Count('interest__id')) 
        return data[0].count 

    def accepted_count(self):
        try:
            data = Event.objects.filter(Q(invitation__status="A") | Q(interest__status="A"),id=self.id).annotate(count= models.Count('invitation__id') + models.Count('interest__id') ) 
            return data[0].count
        except:
            return 0 
        
    def accepted_persons(self):
        accepted_musician_list = list(Interest.objects.filter(event=self,status="A").values_list('musician__user__id',flat=True)) 
        accepted_troupe_list = list(Interest.objects.filter(event=self,status="A").values_list('troupe__user__id',flat=True)) 
        accepted_musician_list_1 = list(Invitation.objects.filter(event=self,status="A").values_list('musician__user__id',flat=True)) 
        accepted_troupe_list_1 = list(Invitation.objects.filter(event=self,status="A").values_list('troupe__user__id',flat=True))
        final_list = accepted_musician_list + accepted_troupe_list + accepted_musician_list_1 + accepted_troupe_list_1
        final_list = [i for i in final_list if i is not None]
        users = User.objects.filter(id__in=final_list)
      
        return users



    def rejected_count(self):
        try:
            data = Event.objects.filter(Q(invitation__status="R") | Q(interest__status="R"),id=self.id).annotate(count= models.Count('invitation__id') + models.Count('interest__id') ) 
            return data[0].count 
        except:
            return 0


    def accepted_invitation_count(self):
        try:
            data = Event.objects.filter(id=self.id, invitation__status='A').annotate(count= models.Count('invitation__id')) 
            return data[0].count
        except:
            return 0

    def accepted_interest_count(self):
        try:
            data = Event.objects.filter(id=self.id, interest__status='A').annotate(count= models.Count('interest__id')) 
            return data[0].count
        except:
            return 0


    def reject_invitation_count(self):
        try:
            data = Event.objects.filter(id=self.id, invitation__status='R').annotate(count= models.Count('invitation__id')) 
            return data[0].count
        except:
            return 0

    def reject_interest_count(self):
        try:
            data = Event.objects.filter(id=self.id, interest__status='R').annotate(count= models.Count('interest__id')) 
            return data[0].count
        except:
            return 0
    
    def pending_request_count(self):
        try:
            data = Event.objects.filter(id=self.id, invitation__status='S').annotate(count= models.Count('invitation__id')) 
            return data[0].count
        except:
            return 0

    def pending_interest_count(self):
        try:
            data = Event.objects.filter(id=self.id, interest__status='S').annotate(count= models.Count('interest__id')) 
            return data[0].count
        except:
            return 0

    def registration_close_date_status(self):
        if self.registration_close_date < date.today():
            return True
        else:
            return False
            
    def unread_message_count(self):
        if self.event_organizer:           
            interest_count = Message.objects.filter(interest__event__id=self.id,interest__event__event_organizer=self.event_organizer,unread=True).exclude(user=self.event_organizer.user).count()
            invitation_count = Message.objects.filter(invitation__event__id=self.id,invitation__event__event_organizer=self.event_organizer,unread=True).exclude(user=self.event_organizer.user).count()
            total  = interest_count + invitation_count
            return total
        elif self.gurukulam:
            interest_count = Message.objects.filter(interest__event__id=self.id,interest__event__gurukulam=self.gurukulam,unread=True).exclude(user=self.gurukulam.user).count()
            invitation_count = Message.objects.filter(invitation__event__id=self.id,invitation__event__gurukulam=self.gurukulam,unread=True).exclude(user=self.gurukulam.user).count()
            total  = interest_count + invitation_count
            return total


            
    def unread_invitation_message_count(self):
        if self.event_organizer:           
            #interest_count = Message.objects.filter(interest__event__id=self.id,interest__event__event_organizer=self.event_organizer,unread=True).exclude(user=self.event_organizer.user).count()
            invitation_count = Message.objects.filter(invitation__event__id=self.id,invitation__event__event_organizer=self.event_organizer,unread=True).exclude(user=self.event_organizer.user).count()
            #total  = interest_count + invitation_count
            return invitation_count
        elif self.gurukulam:
            #interest_count = Message.objects.filter(interest__event__id=self.id,interest__event__gurukulam=self.gurukulam,unread=True).exclude(user=self.gurukulam.user).count()
            invitation_count = Message.objects.filter(invitation__event__id=self.id,invitation__event__gurukulam=self.gurukulam,unread=True).exclude(user=self.gurukulam.user).count()
            #total  = interest_count + invitation_count
            return invitation_count

    def unread_interest_message_count(self):
        if self.event_organizer:           
            interest_count = Message.objects.filter(interest__event__id=self.id,interest__event__event_organizer=self.event_organizer,unread=True).exclude(user=self.event_organizer.user).count()
            #invitation_count = Message.objects.filter(invitation__event__id=self.id,invitation__event__event_organizer=self.event_organizer,unread=True).exclude(user=self.event_organizer.user).count()
            #total  = interest_count + invitation_count
            return interest_count
        elif self.gurukulam:
            interest_count = Message.objects.filter(interest__event__id=self.id,interest__event__gurukulam=self.gurukulam,unread=True).exclude(user=self.gurukulam.user).count()
            #invitation_count = Message.objects.filter(invitation__event__id=self.id,invitation__event__gurukulam=self.gurukulam,unread=True).exclude(user=self.gurukulam.user).count()
            #total  = interest_count + invitation_count
            return interest_count

    def get_absolute_url(self):
        return reverse('event_details', kwargs={'pk': self.pk, })
    



class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bookmarked {self.event.name}"
    
class Pin_Event(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return event.name + "-" + user.first_name

class Event_Skill(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)  
    skill = models.ForeignKey(Skill,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.skill.skill_name


#event creator send request to musician,Gurukulam, Troupe
class Invitation(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE,null=True)
    status = models.CharField(choices=request_status_options,max_length=1,null=True)
    musician = models.ForeignKey(Musician,on_delete=models.CASCADE,blank=True,null=True,related_name="minvitation")
    gurukulam = models.ForeignKey(Gurukulam,on_delete=models.CASCADE,blank=True,null=True)
    troupe = models.ForeignKey(Troupe,on_delete=models.CASCADE,blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    accepted_time = models.DateTimeField(auto_now=True,null=True)
    

    def __str__(self):
        if self.musician != None:
            return self.musician.user.first_name
        elif self.troupe != None:
            return self.troupe.user.name
        elif self.gurukulam != None:
            return self.gurukulam.user.name

    def get_last_message(self):
        try:
            message = Message.objects.filter(invitation=self.id).values_list('text').last()  
            return message[0]
        except:
            message = "Ping"
            return message
        

    def get_last_message_time(self):
        try:
            sent_on = Message.objects.filter(invitation=self.id).values_list('sent_on').last()  
            return sent_on[0]
        except:
            return None


    def unread_message_count(self):
        if self.musician:
            invitation_count = Message.objects.filter(invitation=self,invitation__musician=self.musician,unread=True).exclude(user=self.musician.user).count()
        elif self.troupe:
            invitation_count = Message.objects.filter(invitation=self,invitation__troupe=self.troupe,unread=True).exclude(user=self.troupe.user).count()
        return invitation_count 

    def eo_unread_message_count(self):
        if self.event.event_organizer:
            if self.musician:
                invitation_count = Message.objects.filter(invitation=self,invitation__musician=self.musician,unread=True).exclude(user=self.event.event_organizer.user).count()
            elif self.troupe:
                invitation_count = Message.objects.filter(invitation=self,invitation__troupe=self.troupe,unread=True).exclude(user=self.event.event_organizer.user).count()
            elif self.gurukulam:
                invitation_count = Message.objects.filter(invitation=self,invitation__gurukulam=self.gurukulam,unread=True).exclude(user=self.event.event_organizer.user).count()
        elif self.event.gurukulam:
            if self.musician:
                invitation_count = Message.objects.filter(invitation=self,invitation__musician=self.musician,unread=True).exclude(user=self.event.gurukulam.user).count()
            elif self.troupe:
                invitation_count = Message.objects.filter(invitation=self,invitation__troupe=self.troupe,unread=True).exclude(user=self.event.gurukulam.user).count()
            elif self.gurukulam:
                invitation_count = Message.objects.filter(invitation=self,invitation__gurukulam=self.gurukulam,unread=True).exclude(user=self.event.gurukulam.user).count()
    
        return invitation_count


    def invitation_to(self):
        if self.musician:
            return self.musician
        elif self.gurukulam:
            return self.gurukulam
        elif self.troupe:
            return self.troupe
    
    def invitation_to_id(self):
        if self.musician:
            return self.musician.user.id
        elif self.gurukulam:
            return self.gurukulam.user.id
        elif self.troupe:
            return self.troupe.user.id

    def event_posted_by(self):
        if self.event.event_organizer:
            return self.event.event_organizer
        elif self.event.gurukulam:
            return self.event.gurukulam
    class Meta:
        ordering = ['-id']

class Interest(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE,null=True)
    musician = models.ForeignKey(Musician,on_delete=models.CASCADE,blank=True,null=True,related_name="minterest")
    status = models.CharField(choices=request_status_options,max_length=1,null=True)
    troupe = models.ForeignKey(Troupe,on_delete=models.CASCADE,blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True,null=True)
    accepted_time = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        if self.musician != None:
            return self.musician.user.first_name
        elif self.troupe != None:
            return self.troupe.user.name

    def get_last_message(self):
        try:
            message = Message.objects.filter(interest=self.id).values_list('text').last() 
            return message[0]
        except:
            message = "Ping" 
            return message

    def unread_message_count(self):
        if self.musician:
            interest_count = Message.objects.filter(interest=self,interest__musician=self.musician,unread=True).exclude(user=self.musician.user).count()
        elif self.troupe:
            interest_count = Message.objects.filter(interest=self,interest__troupe=self.troupe,unread=True).exclude(user=self.troupe.user).count()
    
        return interest_count 

    def eo_unread_message_count(self):
        if self.event.event_organizer:
            if self.musician:
                interest_count = Message.objects.filter(interest=self,interest__musician=self.musician,unread=True).exclude(user=self.event.event_organizer.user).count()
            elif self.troupe:
                interest_count = Message.objects.filter(interest=self,interest__troupe=self.troupe,unread=True).exclude(user=self.event.event_organizer.user).count()
            
        elif self.event.gurukulam:
            if self.musician:
                interest_count = Message.objects.filter(interest=self,interest__musician=self.musician,unread=True).exclude(user=self.event.gurukulam.user).count()
            elif self.troupe:
                interest_count = Message.objects.filter(interest=self,interest__troupe=self.troupe,unread=True).exclude(user=self.event.gurukulam.user).count()
            


        return interest_count 

    def intrested_by(self):
        if self.musician:
            return self.musician
        elif self.troupe:
            return self.troupe
    
    def intrested_by_id(self):
        if self.musician:
            return self.musician.user.id
        elif self.troupe:
            return self.troupe.user.id

    def event_posted_by(self):
        if self.event.event_organizer:
            return self.event.event_organizer
        elif self.event.gurukulam:
            return self.event.gurukulam

    class Meta:
        ordering = ['-id']
        
  


class Message(models.Model):
    invitation = models.ForeignKey(Invitation,on_delete=models.CASCADE,blank=True,null=True)
    interest = models.ForeignKey(Interest,on_delete=models.CASCADE,blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    text = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)
    unread = models.BooleanField(default=True)

    def __str__(self):
        return self.user.first_name + self.user.name

   
    @staticmethod
    def unread_count(user):
        invitation_count = Message.objects.filter((Q(invitation__event__gurukulam__user=user) | Q(invitation__event__event_organizer__user=user) | Q(invitation__musician__user=user) | Q(invitation__gurukulam__user=user)| Q(invitation__troupe__user=user)   ),~Q(user=user),unread=True).count()
        interest_count = Message.objects.filter((Q(interest__event__gurukulam__user=user) | Q(interest__event__event_organizer__user=user) | Q(interest__musician__user=user)  | Q(interest__troupe__user=user)),~Q(user=user),unread=True).count()
        return invitation_count + interest_count