from rest_framework import serializers
from account.models import User,Key_Performer,Event_Performer,Gurukulam_Teacher,Troupe,Lecture_Video,Course,Gurukulam_Testimonial,Musician,Musician_Skill,Highlight,Musician_Award,Gurukulam,Gurukulam_Skill,Gurukulam_Award,Troupe,Troupe_Skill,Post,Event_Organizer,Event_Performer,Musician_Gurukulam,Post_Comment,Skill,Skill_Level,UserFollowing,Conversation,Chat,Location, Skill_Category
from django.contrib.auth.models import Group
from event.models import Event
from bs4 import BeautifulSoup
import json

from account.models import Report_People,Music_Lover

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class Group_Serializer(serializers.ModelSerializer):
    class Meta:
        model =  Group
        fields = '__all__'


class Skill_Category_Serializer(serializers.ModelSerializer):
    class Meta:
        model =  Skill_Category
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField('get_role')
    profile_picture = serializers.SerializerMethodField()
    #profile_picture = serializers.URLField(read_only=True, source='profile_picture.url')

    def get_role(self,obj):
        return [group.name for group in obj.groups.all()][0]

    class Meta:
        model = User
        fields = ['first_name','last_name','role','location','profile_picture']
    
    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return self.context['request'].build_absolute_uri(obj.profile_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    first_name = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password','groups','location']



class Location_Serializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField()

    class Meta:
        model = Location
        fields = '__all__'

class My_profileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    cover_picture = serializers.SerializerMethodField()

    class Meta:
        model =  User
        fields = ['id','first_name','last_name','profile_picture','cover_picture','instagram','twitter','following_count','followers_count']


    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return self.context['request'].build_absolute_uri(obj.profile_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url

    def get_cover_picture(self, obj):
        if obj.cover_picture:
            return self.context['request'].build_absolute_uri(obj.cover_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url

class Aboutme_Serializer(serializers.ModelSerializer):
    class Meta:
        model =  Musician
        fields = ['about_me']


class Musician_Skill_Serializer(serializers.ModelSerializer):
    skill = serializers.StringRelatedField()
    skill_level = serializers.StringRelatedField()
    musician = serializers.StringRelatedField()

    class Meta:
        model =  Musician_Skill
        fields = '__all__'

class Musician_Highlight_Serializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model =  Highlight
        fields = '__all__'

class Musician_School_Serializer(serializers.ModelSerializer):
    musician = serializers.StringRelatedField()
    gurukulam = serializers.StringRelatedField()

    class Meta:
        model =  Musician_Gurukulam
        fields = '__all__'


class Musician_Award_Serializer(serializers.ModelSerializer):
    musician = serializers.StringRelatedField()
    image = serializers.SerializerMethodField()
    class Meta:
        model =  Musician_Award
        fields = ['id','musician','title','image']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None
    


class KeyPerformerSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()
    profile_photo = serializers.StringRelatedField()
    musician = serializers.StringRelatedField()
    troupe = serializers.StringRelatedField()
    class Meta:
        model = Key_Performer
        fields = '__all__'

class EventPerformerSerializer(serializers.ModelSerializer):
    event_organizer = serializers.StringRelatedField()
    troupe = serializers.StringRelatedField()
    musician = serializers.StringRelatedField()
    class Meta:
        model = Event_Performer
        fields = '__all__'

class GurukulamTeacherSerializer(serializers.ModelSerializer):
    musician = serializers.StringRelatedField()
    gurukulam = serializers.StringRelatedField()
    sender = serializers.StringRelatedField()

    class Meta:
        model = Gurukulam_Teacher
        fields = '__all__'


class TroupeSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()
    profile_photo = serializers.StringRelatedField()
    musician = serializers.StringRelatedField()
    troupe = serializers.StringRelatedField()

    class Meta:
        model = Troupe
        fields = '__all__'

class Musicschool_profileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    cover_picture = serializers.SerializerMethodField()
    class Meta:
        model =  User
        fields = ['id','first_name','last_name','profile_picture','cover_picture','following_count','followers_count']

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return self.context['request'].build_absolute_uri(obj.profile_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url

    def get_cover_picture(self, obj):
        if obj.cover_picture:
            return self.context['request'].build_absolute_uri(obj.cover_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url

class Musicschool_aboutmeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gurukulam
        fields = ['about_us']

class Musicschool_Skill_Serializer1(serializers.ModelSerializer):
    gurukulam = serializers.StringRelatedField()
    skill = serializers.StringRelatedField()

    class Meta:
        model =  Gurukulam_Skill
        fields = '__all__'

class Musicschool_Award_Serializer(serializers.ModelSerializer):
    gurukulam = serializers.StringRelatedField()
    photo = serializers.SerializerMethodField()
    class Meta:
        model =  Gurukulam_Award
        fields = '__all__'

    def get_photo(self, obj):
        if obj.photo:
            return self.context['request'].build_absolute_uri(obj.photo.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url

class Musicschool_Highlight_Serializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model =  Highlight
        fields = '__all__'

class LectureVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture_Video
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class GurukulamTestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gurukulam_Testimonial
        fields = '__all__'

class Troupe_profileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    cover_picture = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','first_name','last_name','profile_picture','cover_picture','following_count','followers_count']

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return self.context['request'].build_absolute_uri(obj.profile_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url

    def get_cover_picture(self, obj):
        if obj.cover_picture:
            return self.context['request'].build_absolute_uri(obj.cover_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url

class Troupe_aboutmeSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Troupe
        fields = ['about_us']

class Troupe_Skill_Serializer(serializers.ModelSerializer):
    troupe = serializers.StringRelatedField()
    skill = serializers.StringRelatedField()

    class Meta:
        model =  Troupe_Skill
        fields = '__all__'

class Troupe_Key_Performer_Serializer(serializers.ModelSerializer):
    musician = serializers.StringRelatedField()
    troupe = serializers.StringRelatedField()

    class Meta:
        model = Key_Performer
        fields = '__all__'

class Troupe_Highlight_Serializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model =  Highlight
        fields = '__all__'

class Musician_edit_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Musician
        fields = ['dob','gender','profession','about_me']


class Musicschool_edit_Serializer(serializers.ModelSerializer):
    class Meta:
        model =  Gurukulam
        fields = ['phone_no','about_us']

class Troupe_edit_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Troupe
        fields = ['president','about_us']

class Event_edit_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Event_Organizer
        fields = ['about_us']

class Musiclover_edit_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Music_Lover
        fields = ['dob']

class Location_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name']

class User_edit_Serializer(serializers.ModelSerializer):
    location = Location_Serializer()
    profile_picture = serializers.SerializerMethodField()
    cover_picture = serializers.SerializerMethodField()
    
    class Meta:
        model =  User
        fields = ['first_name','last_name','address','mobile_no','location','profile_picture','cover_picture','instagram','twitter']

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return self.context['request'].build_absolute_uri(obj.profile_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url

    def get_cover_picture(self, obj):
        if obj.cover_picture:
            return self.context['request'].build_absolute_uri(obj.cover_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url

class User_edit_Serializer1(serializers.ModelSerializer):
    #profile_picture = serializers.SerializerMethodField()
    #cover_picture = serializers.SerializerMethodField()
 
    class Meta:
        model =  User
        fields = ['first_name','last_name','address','mobile_no','location','profile_picture','cover_picture','instagram','twitter']

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return self.context['request'].build_absolute_uri(obj.profile_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url

    def get_cover_picture(self, obj):
        if obj.cover_picture:
            return self.context['request'].build_absolute_uri(obj.cover_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url

class Musician_Post_Serializer(serializers.ModelSerializer):
    content_data = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['user', 'content', 'posted_on', 'location', 'invitation', 'interest', 'highlight', 'likes', 'user_likes', 'content_data']

    def get_content_data(self, obj):
        # Use BeautifulSoup to extract data
        soup = BeautifulSoup(obj.content, 'html.parser')
        
        # Extract text content
        text_content = soup.get_text(separator=' ').strip()
        
        # Extract video URL
        video_tag = soup.find('a', href=True, text='Watch Video')
        video_url = video_tag['href'] if video_tag else None
        
        # Extract image URL
        img_tag = soup.find('img', src=True)
        image_url = img_tag['src'] if img_tag else None
        
        return {
            'text_content': text_content,
            'video_url': video_url,
            'image_url': image_url
        }

class Troupe_Post_Serializer(serializers.ModelSerializer):

    content_data = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['user', 'content', 'posted_on', 'location', 'invitation', 'interest', 'highlight', 'likes', 'user_likes', 'content_data']

    def get_content_data(self, obj):
        # Use BeautifulSoup to extract data
        soup = BeautifulSoup(obj.content, 'html.parser')
        
        # Extract text content
        text_content = soup.get_text(separator=' ').strip()
        
        # Extract video URL
        video_tag = soup.find('a', href=True, text='Watch Video')
        video_url = video_tag['href'] if video_tag else None
        
        # Extract image URL
        img_tag = soup.find('img', src=True)
        image_url = img_tag['src'] if img_tag else None
        
        return {
            'text_content': text_content,
            'video_url': video_url,
            'image_url': image_url
        }



class Musicschool_Post_Serializer(serializers.ModelSerializer):

    content_data = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['user', 'content', 'posted_on', 'location', 'invitation', 'interest', 'highlight', 'likes', 'user_likes', 'content_data']

    def get_content_data(self, obj):
        # Use BeautifulSoup to extract data
        soup = BeautifulSoup(obj.content, 'html.parser')
        
        # Extract text content
        text_content = soup.get_text(separator=' ').strip()
        
        # Extract video URL
        video_tag = soup.find('a', href=True, text='Watch Video')
        video_url = video_tag['href'] if video_tag else None
        
        # Extract image URL
        img_tag = soup.find('img', src=True)
        image_url = img_tag['src'] if img_tag else None
        
        return {
            'text_content': text_content,
            'video_url': video_url,
            'image_url': image_url
        }





class Event_Post_Serializer(serializers.ModelSerializer):

    content_data = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['user', 'content', 'posted_on', 'location', 'invitation', 'interest', 'highlight', 'likes', 'user_likes', 'content_data']

    def get_content_data(self, obj):
        # Use BeautifulSoup to extract data
        soup = BeautifulSoup(obj.content, 'html.parser')
        
        # Extract text content
        text_content = soup.get_text(separator=' ').strip()
        
        # Extract video URL
        video_tag = soup.find('a', href=True, text='Watch Video')
        video_url = video_tag['href'] if video_tag else None
        
        # Extract image URL
        img_tag = soup.find('img', src=True)
        image_url = img_tag['src'] if img_tag else None
        
        return {
            'text_content': text_content,
            'video_url': video_url,
            'image_url': image_url
        }

class Event_profileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    cover_picture = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id','first_name','last_name','profile_picture','cover_picture','following_count','followers_count']

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return self.context['request'].build_absolute_uri(obj.profile_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url

    def get_cover_picture(self, obj):
        if obj.cover_picture:
            return self.context['request'].build_absolute_uri(obj.cover_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url

class Event_aboutmeSerializer(serializers.ModelSerializer):
    class Meta:

        model = Event_Organizer
        fields = ['about_us']

class Event_Performer_Serializer1(serializers.ModelSerializer):
    musician_followers_count = serializers.SerializerMethodField()
    musician = serializers.StringRelatedField()
    troupe = serializers.StringRelatedField()
    musician_profile_picture = serializers.SerializerMethodField()
    musician_user_id = serializers.SerializerMethodField()
    class Meta:
        model = Event_Performer
        fields = ['id','musician_id','musician','musician_profile_picture','musician_user_id','musician_followers_count','troupe_id','troupe']
        
    def get_musician_followers_count(self, obj):
        try:
            return obj.musician.user.followers_count()
        except:
            return None

    def get_musician_user_id(self, obj):
        try:
            return obj.musician.user.id
        except:
            return None

    def get_musician_profile_picture(self, obj):
        request = self.context.get('request')
        try:
            if request and obj.musician.user.profile_picture:
                return request.build_absolute_uri(obj.musician.user.profile_picture.url)
        except:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url

class Event_Highlight_Serializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model =  Highlight
        fields = '__all__'

class Comment_Serializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    user_id = serializers.IntegerField()
    user_profile_picture = serializers.SerializerMethodField()

    class Meta:
        model =  Post_Comment
        fields = ['id','comment','user','user_id','post','commented_on','user_profile_picture']

    def get_user_id(self, obj):
        return obj.user.id

    def get_user_profile_picture(self, obj):
        user = obj.user
        if user.profile_picture:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(user.profile_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url
    
class Post_Serializer(serializers.ModelSerializer):
    comments = Comment_Serializer(many=True)
    liked_by_user = serializers.SerializerMethodField()
    user_profile_picture = serializers.SerializerMethodField()
    current_user_profile_picture = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    content_data = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Post
        fields = ['id','user','name','user_profile_picture','content','posted_on','comment_count','like_count','liked_by_user','comments','current_user_profile_picture','content_data']

    def get_name(self, post):
        return str(post.user)

    def get_liked_by_user(self, post):
        user = self.context['request'].user
        return post.user_likes.filter(id=user.id).exists()

    def get_user_profile_picture(self, post):
        user = post.user
        if user.profile_picture:
            return self.context['request'].build_absolute_uri(user.profile_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url

    def get_current_user_profile_picture(self, post):
        user = self.context['request'].user
        if user.profile_picture:
            return self.context['request'].build_absolute_uri(user.profile_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url
        
    def get_content_data(self, obj):
        # Use BeautifulSoup to extract data
        soup = BeautifulSoup(obj.content, 'html.parser')

        BASE_URL = 'http://padane.in'
        
        # Extract text content
        text_content = soup.get_text(separator=' ').strip()
        
        # Extract video URL
        video_tag = soup.find('a', href=True, text='Watch Video')
        video_url = video_tag['href'] if video_tag else None
        
        # Extract image URL
        img_tag = soup.find('img', src=True)
        image_url = BASE_URL+img_tag['src'] if img_tag else None

        event_details_id = None
        if obj.content.startswith("I am going to participate"):
            event_tag = soup.find('a', href=True)
            if event_tag and '/event_details/' in event_tag['href']:
                try:
                    # Extract the ID from the URL
                    event_details_id = int(event_tag['href'].split('/event_details/')[1].split('/')[0])
                except (IndexError, ValueError):
                    event_details_id = None
        
        return {
            'text_content': text_content,
            'video_url': video_url,
            'image_url': image_url,
            'event_details_id':event_details_id
        }



class Post_Comment_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Post_Comment
        fields = ['id','comment']

class Following_Serializer(serializers.ModelSerializer):
    
    group = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()


    
    profile_picture = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    class Meta:
        model = UserFollowing
        fields = ['first_name','last_name','group','following_count', 'followers_count','following','profile_picture','user_id']

    def get_group(self, obj):
        return str(obj.following_user_id.groups.all()[0])
    
    def get_following_count(self, obj):
        return UserFollowing.objects.filter(user=obj.following_user_id).count()

    def get_followers_count(self, obj):
        return UserFollowing.objects.filter(following_user_id=obj.following_user_id).count()

    def get_following(self, obj):
        if UserFollowing.objects.filter(following_user_id=obj.following_user_id,user=self.context.get("request").user ).exists():
            return True
        else:
            return False
        
    def get_profile_picture(self, obj):
        if obj.following_user_id.profile_picture:
            return self.context['request'].build_absolute_uri(obj.following_user_id.profile_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url

    def get_user_id(self, obj):
        return obj.following_user_id.id
    

    def get_first_name(self, obj):
        return obj.following_user_id.first_name
    
    def get_last_name(self, obj):
        return obj.following_user_id.last_name

class Followers_Serializer(serializers.ModelSerializer):
    
    group = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()


    profile_picture = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    class Meta:
        model = UserFollowing
        fields = ['first_name','last_name','group','following_count', 'followers_count','following','profile_picture','user_id']

    def get_group(self, user):
        return str(user.user.groups.all()[0])

    def get_following_count(self, obj):
        return UserFollowing.objects.filter(user=obj.user).count()

    def get_followers_count(self, obj):
        return UserFollowing.objects.filter(following_user_id=obj.user).count()

    def get_following(self, obj):
        if UserFollowing.objects.filter(following_user_id=obj.user.id,user=self.context.get("request").user.id).exists():
            return True
        else:
            return False
        


    def get_profile_picture(self, obj):
        if obj.user.profile_picture:
            return self.context['request'].build_absolute_uri(obj.user.profile_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url

    def get_user_id(self, obj):
        return obj.user.id
    

    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name

class All_People_Serializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id','first_name','last_name','group','following_count', 'followers_count','following','profile_picture','user_id']

    def get_following(self, obj):
        request_user = self.context.get("request").user
        return UserFollowing.objects.filter(following_user_id=obj.id, user=request_user.id).exists()
    

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return self.context['request'].build_absolute_uri(obj.profile_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url

    def get_user_id(self, obj):
        return obj.id
    
    def get_following_count(self, obj):
        return UserFollowing.objects.filter(user=obj.id).count()

    def get_followers_count(self, obj):
        return UserFollowing.objects.filter(following_user_id=obj.id).count()
    

class Conversation_Serializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField(read_only=True)
    sender_id = serializers.SerializerMethodField(read_only=True)
    sender_profile_picture = serializers.SerializerMethodField(read_only=True)
    receiver_name = serializers.SerializerMethodField(read_only=True)
    receiver_id = serializers.SerializerMethodField(read_only=True)
    receiver_profile_picture = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Conversation
        fields = ['id','get_last_message','sender_id','sender_name','sender_profile_picture','receiver_name','receiver_profile_picture','receiver_id','date']

    def get_sender_name(self,obj):
        if self.context['request'].user.id == obj.sender.id:
            return str(obj.sender)
        else:
            return str(obj.receiver)
    

    def get_sender_id(self,obj):

        if self.context['request'].user.id == obj.sender.id:
            return str(obj.sender.id)
        else:
            return str(obj.receiver.id)
        
    
    def get_sender_profile_picture(self, obj):

        if self.context['request'].user.id == obj.sender.id:
            if obj.sender.profile_picture:
                return self.context['request'].build_absolute_uri(obj.sender.profile_picture.url)
            else:
                default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
                return default_image_url
        else:
            if obj.receiver.profile_picture:
                return self.context['request'].build_absolute_uri(obj.receiver.profile_picture.url)
            else:
                default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
                return default_image_url
        
    
    def get_receiver_name(self, obj):
        if self.context['request'].user.id == obj.sender.id:
            return str(obj.receiver)
        else:
            return str(obj.sender)

    def get_receiver_id(self, obj):
        if self.context['request'].user.id == obj.sender.id:
            return str(obj.receiver.id)
        else:
            return str(obj.sender.id)

    def get_receiver_profile_picture(self, obj):

        if self.context['request'].user.id == obj.sender.id:
            if obj.receiver.profile_picture:
                return self.context['request'].build_absolute_uri(obj.receiver.profile_picture.url)
            else:
                default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
                return default_image_url
        else:
            if obj.sender.profile_picture:
                return self.context['request'].build_absolute_uri(obj.sender.profile_picture.url)
            else:
                default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
                return default_image_url
    
    

class Chat_Serializer(serializers.ModelSerializer):
    receiver_name = serializers.SerializerMethodField(read_only=True)
    messaged_by_me  = serializers.SerializerMethodField(read_only=True)
    receiver_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Chat
        fields = ['conversation','receiver_name','receiver_id','message','date','unread','messaged_by_me']

    def get_receiver_name(self,obj):
        if self.context['request'].user.id == obj.sender.id:
            return str(obj.conversation.receiver)
        return str(self.context['request'].user)
    
    def get_receiver_id(self,obj):
        if self.context['request'].user.id == obj.sender.id:
            return str(obj.conversation.receiver.id)
        return str(self.context['request'].user)

    
    def get_messaged_by_me(self,obj):
        if self.context['request'].user.id == obj.sender.id:
            return True
        return False

class Add_Musician_Skill_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Musician_Skill
        fields = ['skill','skill_level','teach','perform']

class Skill_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id','skill_name']


class Skill_Serializer_Filter(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id','skill_name','skill_category']


class Skill_Level_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Skill_Level
        fields = ['id','level']

class Musician_Myschool_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Musician_Gurukulam
        fields = ['gurukulam']

class Gurukulam_Serializer(serializers.ModelSerializer):
    gurukulam_name = serializers.CharField(source='user.get_full_name', read_only=True)
    class Meta:
        model = Gurukulam
        fields = ['id','gurukulam_name']

class Musician_Myaward_Serializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    image = serializers.ImageField(required=True)
    class Meta:
        model = Musician_Award
        fields = ['title','image']

class Myhighlight_Serializer(serializers.ModelSerializer):
     class Meta:
        model = Highlight
        fields = ['title','video_link','description']

class Musicschool_Skill_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Gurukulam_Skill
        fields = ['skill','skill_name']

class Musicschool_Myaward_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Gurukulam_Award
        fields = ['title','photo']

class Musicschool_Lecture_Videos_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture_Video
        fields = ['title','video']

class Event_Performer_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Event_Performer
        fields = ['musician','troupe']

class Musician_Serializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.first_name', read_only=True)
    class Meta:
        model = Musician
        fields = ['id','user_name']

class Troupe_Serializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.first_name', read_only=True)
    class Meta:
        model = Troupe
        fields = ['id','user_name']

class Band_Skill_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Troupe_Skill
        fields = ['skill']

class Band_Performer_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Key_Performer
        fields = ['musician']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class SkillLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill_Level
        fields = '__all__'


class Musician_Skill_Serializer1(serializers.ModelSerializer):
    skill= serializers.ReadOnlyField(source='skill.skill_name')
    class Meta:
        model = Musician_Skill
        fields = ['skill']

class MusicianSerializer(serializers.ModelSerializer):
    musician_skill = Musician_Skill_Serializer1(many=True, read_only=True)
    profile_picture = serializers.SerializerMethodField(read_only=True)
    
    #full_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Musician
        fields = ['id','user','full_name','profile_picture','profession','musician_skill']

    def get_profile_picture(self, obj):
        profile_picture = getattr(obj.user, 'profile_picture', None)
        if profile_picture:
            return self.context['request'].build_absolute_uri(profile_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url
        
class Musician_Association_Myschool_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Gurukulam_Teacher
        fields = ['gurukulam']


class Report_People_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Report_People 
        fields = ['id','complaint','report_file']

    def validate(self, data):
        complaint = data.get('complaint')
        report_file = data.get('report_file')

        if complaint is None and report_file is None:
            raise serializers.ValidationError("Provide either 'complaint' or 'report_file'.")

        return data

#Serializer for Reset the user's password.
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class UserSerializer1(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'name','group')

class EventSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name','group')

class Group_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id','name']

class Musiclover_profileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    cover_picture = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id','first_name','last_name','address','location','profile_picture','cover_picture','following_count','followers_count']

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return self.context['request'].build_absolute_uri(obj.profile_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url

    def get_cover_picture(self, obj):
        if obj.cover_picture:
            return self.context['request'].build_absolute_uri(obj.cover_picture.url)
        else:
            default_image_url = self.context['request'].build_absolute_uri('http://padane.in/static/blank-profile-picture.webp')
            return default_image_url


class Musiclover_aboutmeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music_Lover
        fields = ['dob']


class EventSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
       

class UserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = '__all__'