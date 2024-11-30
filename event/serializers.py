from rest_framework import serializers
from .models import Event,Location,Event_Skill,Skill,Event_Organizer,Invitation,Interest,Message,Event_Category, Event_Type
from account.models import User,Troupe,Gurukulam,Location




class Event_Type_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Event_Type
        fields = ['id',"name"]

class EventSerializer(serializers.ModelSerializer):
    event_type = serializers.StringRelatedField()
    event_category = serializers.StringRelatedField()
    location = serializers.StringRelatedField()
    gurukulam = serializers.StringRelatedField()
    event_organizer = serializers.StringRelatedField()
    poster_image = serializers.SerializerMethodField()
    class Meta:
        model = Event
        exclude = ['created_on','self_reference','auto_accept']

    def get_poster_image(self, obj):
        if obj.poster_image:
            return self.context['request'].build_absolute_uri(obj.poster_image.url)
        return None

class EventSkill_Serializer(serializers.ModelSerializer):
    skill = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(),many=True)
    class Meta:
        model = Event_Skill
        fields = ['skill']

class Create_Event_Serializer(serializers.ModelSerializer):
    skill = EventSkill_Serializer(many=True, required=False)
    class Meta:
        model = Event
        exclude = ['created_on','event_organizer','gurukulam',"auto_accept"]

    '''    

    def create(self, validated_data):
        skill_data = validated_data.pop('skill',[])
        event = Event.objects.create(**validated_data)

        for skill_data in skills_data:
            skill = Event_Skill.objects.create(**skill_data)
            event.skills.add(skill)
        return event

    '''

class Location_Serializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField()

    class Meta:
        model = Location
        fields = '__all__'

class Event_Category_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Event_Category
        fields = ['id', 'name']

class Edit_Event_Serializer(serializers.ModelSerializer):
    event_type = serializers.StringRelatedField()
    event_category = Event_Category_Serializer()
    location = Location_Serializer()
    poster_image = serializers.SerializerMethodField()

    class Meta:
        model = Event
        exclude = ['created_on','auto_accept']

    def get_poster_image(self, obj):
        if obj.poster_image:
            return self.context['request'].build_absolute_uri(obj.poster_image.url)
        return None

class Edit_Event_Serializer1(serializers.ModelSerializer):
    #poster_image = serializers.SerializerMethodField()
    class Meta:
        model = Event
        exclude = ['created_on','auto_accept']

    def get_poster_image(self, obj):
        if obj.poster_image:
            return self.context['request'].build_absolute_uri(obj.poster_image.url)
        return None

class Event_Details_Serializer(serializers.ModelSerializer):
    event_type = serializers.StringRelatedField()
    event_category = serializers.StringRelatedField()
    location = serializers.StringRelatedField()
    gurukulam = serializers.StringRelatedField()
    event_organizer = serializers.StringRelatedField()
    poster_image = serializers.SerializerMethodField()
    created_by_current_user = serializers.SerializerMethodField()
    share_link = serializers.SerializerMethodField()
    share_text = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id','name','event_type','event_category','event_details','from_date','to_date','location','share_link','share_text','ticket_booking_link_1','poster_image','registration_close_date','venue','self_reference','gurukulam','event_organizer','highlight','registration_close_date_status','created_by_current_user']
    
    def get_share_link(self, obj):

        return str('http://padane.in/event_details/')+ str(obj.id)+ str('/')

    def get_share_text(self, obj):

        return str('Join This Event,')+ str(obj.name)

    def get_created_by_current_user(self, obj):
        current_user = self.context['request'].user
        if obj.event_organizer and obj.event_organizer.user:
            return current_user == obj.event_organizer.user
        elif obj.gurukulam and obj.gurukulam.user:
            return current_user == obj.gurukulam.user
        return False

    def get_poster_image(self, obj):
        if obj.poster_image:
            return self.context['request'].build_absolute_uri(obj.poster_image.url)
        return None

class Event_Skill_Serializer(serializers.ModelSerializer):
    event = serializers.StringRelatedField()
    skill = serializers.StringRelatedField()
    
    class Meta:
        model = Event_Skill
        fields = '__all__'

class Event_Skill_Serializer1(serializers.ModelSerializer):
    event = serializers.StringRelatedField()
    skill_name = serializers.SerializerMethodField()
    skill_category = serializers.SerializerMethodField()
    skill_category_id = serializers.SerializerMethodField()

    class Meta:
        model = Event_Skill
        fields = ['event','skill','skill_name','skill_category_id','skill_category']


    def get_skill_name(self, obj):
        return str(obj.skill)


    def get_skill_category(self, obj):
        return str(obj.skill.skill_category)


    def get_skill_category_id(self, obj):
        return obj.skill.skill_category.id

class Event_Organizer_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mobile_no','email']

class Related_Event_Serializer(serializers.ModelSerializer):
    event_type = serializers.StringRelatedField()
    event_category = serializers.StringRelatedField()
    poster_image = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = ['id','name','poster_image','event_type','event_category','from_date','to_date']

    def get_poster_image(self, obj):
        if obj.poster_image:
            return self.context['request'].build_absolute_uri(obj.poster_image.url)
        return None

class Message_Serializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    messaged_by_me  = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Message
        fields = ['invitation','interest','id','user','text','sent_on','unread','messaged_by_me']

    def get_messaged_by_me(self,obj):
        if self.context['request'].user.id == obj.user.id:
            return True
        return False


class Invitation_Serializer(serializers.ModelSerializer):
    event = serializers.StringRelatedField()
    musician = serializers.StringRelatedField()
    gurukulam = serializers.StringRelatedField()
    troupe = serializers.StringRelatedField()
    messages = Message_Serializer(many=True,read_only=True)
    invitation_from = serializers.SerializerMethodField()
    invitation_from_profile_picture = serializers.SerializerMethodField()
    
    class Meta:
        model = Invitation
        fields = ['id','invitation_from','invitation_from_profile_picture','event','event_id','status','musician','gurukulam','troupe','timestamp','get_last_message','messages']
    
    def get_invitation_from(self, obj):
        event = obj.event
        if event.event_organizer:
            return str(event.event_organizer)
        else:
            return str(event.gurukulam)

    def get_invitation_from_profile_picture(self, obj):
        event = obj.event
        default_profile_picture_url = "http://padane.in/static/blank-profile-picture.webp"

        if event.event_organizer and event.event_organizer.user.profile_picture:
            return self.context['request'].build_absolute_uri(event.event_organizer.user.profile_picture.url)
        elif event.gurukulam and event.gurukulam.user.profile_picture:
            return self.context['request'].build_absolute_uri(event.gurukulam.user.profile_picture.url)
        else:
            return default_profile_picture_url
    
    '''def get_invitation_from_profile_picture(self, obj):
        event = obj.event
        default_profile_picture_url ="http://padane.in/static/blank-profile-picture.webp"
        if event.event_organizer:
            return self.context['request'].build_absolute_uri(event.event_organizer.user.profile_picture.url)
        elif event.gurukulam:
            return self.context['request'].build_absolute_uri(event.gurukulam.user.profile_picture.url)
        else:
            return default_profile_picture_url'''


class Interest_Serializer(serializers.ModelSerializer):
    event = serializers.StringRelatedField()
    musician = serializers.StringRelatedField()
    troupe = serializers.StringRelatedField()
    messages = Message_Serializer(many=True,read_only=True)
    interest_to = serializers.SerializerMethodField()
    interest_to_profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = Interest
        fields = ['id','interest_to','interest_to_profile_picture','event','event_id','status','musician','troupe','timestamp','get_last_message','messages']
    
    def get_interest_to(self, obj):
        event = obj.event
        if event.event_organizer:
            return str(event.event_organizer)
        else:
            return str(event.gurukulam)

    def get_interest_to_profile_picture(self, obj):
        event = obj.event
        default_profile_picture_url = "http://padane.in/static/blank-profile-picture.webp"

        if event.event_organizer and event.event_organizer.user.profile_picture:
            return self.context['request'].build_absolute_uri(event.event_organizer.user.profile_picture.url)
        elif event.gurukulam and event.gurukulam.user.profile_picture:
            return self.context['request'].build_absolute_uri(event.gurukulam.user.profile_picture.url)
        else:
            return default_profile_picture_url

class Event_Serializer(serializers.ModelSerializer):
    event = serializers.StringRelatedField()
    musician = serializers.StringRelatedField()
    troupe = serializers.StringRelatedField()
    messages = Message_Serializer(many=True,read_only=True)
    poster_image = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = "__all__"
    
    def get_poster_image(self, obj):
        if obj.poster_image:
            return self.context['request'].build_absolute_uri(obj.poster_image.url)
        return None
    

class My_Event_Serializer(serializers.ModelSerializer):
    poster_image = serializers.SerializerMethodField()
    location = serializers.StringRelatedField()
    event_creator_name = serializers.SerializerMethodField()
    event_creator_id = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id','name','event_creator_name','event_creator_id','location','venue','poster_image','event_details','from_date','to_date','registration_close_date','highlight','invitation_count','interest_count']
    
    def get_poster_image(self, obj):
        if obj.poster_image:
            return self.context['request'].build_absolute_uri(obj.poster_image.url)
        return None

    def get_event_creator_name(self, obj):
        creator = obj.creator()
        if creator:
            return str(creator)
        return None

    def get_event_creator_id(self, obj):
        creator = obj.creator()
        if creator:
            return creator.id
        return None


class Organizer_Invitation_Serializer(serializers.ModelSerializer):
    event = serializers.StringRelatedField()
    musician = serializers.StringRelatedField()
    gurukulam = serializers.StringRelatedField()
    troupe = serializers.StringRelatedField()
    messages = Message_Serializer(many=True,read_only=True)      
    invitation_to = serializers.StringRelatedField()
    invitation_to_id = serializers.StringRelatedField()

    class Meta:
        model = Invitation
        fields = ['id','invitation_to','invitation_to_id','event','status','musician','gurukulam','troupe','timestamp','get_last_message','messages']


class Organizer_Interest_Serializer(serializers.ModelSerializer):
    event = serializers.StringRelatedField()
    musician = serializers.StringRelatedField()
    troupe = serializers.StringRelatedField()
    messages = Message_Serializer(many=True,read_only=True)
    intrested_by= serializers.StringRelatedField()
    intrested_by_id = serializers.StringRelatedField()

    class Meta:
        model = Interest
        fields = ['id','intrested_by','intrested_by_id','event','status','musician','troupe','timestamp','get_last_message','messages']

    

class Troupe_Search_Serializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Troupe
        fields = ['id','user','full_name','profile_picture']
    
    def get_profile_picture(self, obj):
        profile_picture = getattr(obj.user, 'profile_picture', None)
        if profile_picture:
            return self.context['request'].build_absolute_uri(profile_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url

class Gurukulam_Search_Serializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Gurukulam
        fields = ['id','user','full_name','profile_picture']

    def get_profile_picture(self, obj):
        profile_picture = getattr(obj.user, 'profile_picture', None)
        if profile_picture:
            return self.context['request'].build_absolute_uri(profile_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url

class Event_Serializer1(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['name','invitation_count','accepted_invitation_count','reject_invitation_count','pending_request_count','interest_count','accepted_interest_count','reject_interest_count','pending_interest_count']