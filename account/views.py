from cmath import e
from django.shortcuts import render
from .forms import Signup_Form, CustomAuthForm, MusicLoverForm, EditMusicLoverUserForm, EditMusicianUserForm, MusicianForm,EditGurukulamUserForm,GurukulamForm, Edit_Troupe_UserForm, Troup_Profile_Form, Event_Org_Profile_Form,Edit_Event_Org_UserForm, Musician_Award_Form, Musician_Highlight_Form, Musician_Skill_Form, Musician_Gurukulam_Form, Gurukulam_Skill_Form, Gurukulam_Award_Form, Gurukulam_Testimonial_Form, Lecture_Video_Form, Course_Form, Troupe_Highlight_Form, Key_Performer_Form, Event_Organizer_Highlight_Form, Event_Performer_Form, Highlight_Form,Troupe_Skill_Form, Report_People_Form, Add_Musician_Form, Add_Gurukulam_Teacher_Form, Add_Teacher_Gurukulam_Form
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse, request
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, message
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import login, authenticate, logout
from .models import  Music_Lover, Event_Organizer_Highlight, Event_Performer, Reply, Skill_Category, User, Troupe, Event_Organizer, Gurukulam, Musician, Musician_Award, Musician_Highlight, Musician_Skill, Musician_Gurukulam, Gurukulam_Skill, Gurukulam_Award, Gurukulam_Testimonial, Lecture_Video, Course, Troupe_Highlight, Key_Performer, Location, Troupe_Skill, Post, UserFollowing, Post_Comment, Highlight, Blocked_User, Chat, Conversation, Skill_Level, Gurukulam_Teacher
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout as user_logout
from functools import wraps
from itertools import chain
import ast
from event.models import Event, Bookmark,Event_Skill, Invitation, Interest, Message, Skill, Event_Category, Event_Type
from event.forms import Event_Form
from datetime import datetime
import urllib.parse as urlparse
from event.views import send_email
from django.db.models import Q ,Max, Count, F
from event.forms import Event_Form
from PIL import Image
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
#authentication start
from django.conf import settings
from django.urls import reverse
import requests 
from django.contrib.auth import login
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from .serializers import LoginSerializer,SignupSerializer,My_profileSerializer,KeyPerformerSerializer, EventPerformerSerializer,GurukulamTeacherSerializer,TroupeSerializer, LectureVideoSerializer,CourseSerializer, GurukulamTestimonialSerializer,Aboutme_Serializer,Musician_Skill_Serializer,Musician_Highlight_Serializer,Musician_Award_Serializer,User_edit_Serializer,Musician_edit_Serializer,Musicschool_profileSerializer,Musicschool_aboutmeSerializer,Musicschool_Skill_Serializer,Musicschool_Award_Serializer,Musicschool_Highlight_Serializer,Troupe_profileSerializer,Troupe_aboutmeSerializer,Troupe_Skill_Serializer, Troupe_Highlight_Serializer,Troupe_Key_Performer_Serializer,Musician_Post_Serializer,Troupe_Post_Serializer,Musicschool_Post_Serializer,Event_Post_Serializer,Event_profileSerializer,Event_aboutmeSerializer,Event_Performer_Serializer,Event_Highlight_Serializer,Musicschool_edit_Serializer,Troupe_edit_Serializer,Event_edit_Serializer,Musician_School_Serializer,Post_Serializer,Post_Comment_Serializer,Comment_Serializer,Musician_Myschool_Serializer,Following_Serializer, Followers_Serializer, All_People_Serializer, Conversation_Serializer, Chat_Serializer,Musician_Myaward_Serializer,Myhighlight_Serializer,Musicschool_Myaward_Serializer,Musicschool_Lecture_Videos_Serializer,Event_Performer_Serializer,Band_Skill_Serializer,Band_Performer_Serializer,Skill_Serializer,Skill_Level_Serializer,Gurukulam_Serializer,Musician_Serializer,Troupe_Serializer,Add_Musician_Skill_Serializer, Group_Serializer, Location_Serializer, UserSerializer, Musician_Association_Myschool_Serializer,Location_Serializer,User_edit_Serializer1,UserSerializer1,EventSerializer1,Event_Performer_Serializer1,Musicschool_Skill_Serializer1, Skill_Category_Serializer, Skill_Serializer_Filter, Group_Serializer, Musiclover_aboutmeSerializer,Musiclover_profileSerializer,Musiclover_edit_Serializer
from .serializers import Report_People_Serializer , UserFollowingSerializer
from .models import Report_People


from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .serializers import PasswordResetSerializer ,EventSerializer2
from django.core.paginator import Paginator
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from event.serializers import Event_Type_Serializer, Event_Category_Serializer
 

# Create your views here.
def complete_profile(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.user.username)
        except:
            return function(request, *args, **kwargs)

        if user.groups.filter(name='Artist').exists():
            if user.address == "" or user.mobile_no is None or user.location is None or user.profile_picture == "":
                return redirect('musician_edit_profile')
            else:
                return function(request, *args, **kwargs)

        elif user.groups.filter(name='Music School').exists():
            if user.address == "" or user.gurukulam.phone_no is None or user.location is None or user.profile_picture == "" or  user.gurukulam.about_us == "":
                return redirect('/gurukulam_edit_profile')
            else:
                return function(request, *args, **kwargs)

        elif user.groups.filter(name='Band').exists():
            if user.address == "" or user.mobile_no is None or user.location is None or user.profile_picture == "" or  user.troupe.about_us == "":
                return redirect('troupe_edit_profile')
            else:
                return function(request, *args, **kwargs)

        elif user.groups.filter(name='Event Organizer').exists():
            if user.address == "" or user.mobile_no is None or user.location is None or user.profile_picture == "" or  user.event_organizer.about_us == "":
                return redirect('event_organizer_edit_profile')
            else:
                return function(request, *args, **kwargs)
        
        elif user.groups.filter(name='Music Lover').exists():
            if user.address == "" or user.mobile_no is None or user.location is None or user.profile_picture == "":
                return redirect('music_lover_edit_profile')
            else:
                return function(request, *args, **kwargs)

        try:
            profile = User.objects.get(username=request.user,first_name__isnull=False,last_name__isnull=False,father_name__isnull=False,address__isnull=False,mobile_no__isnull=False,highest_qualification__isnull=False,age__isnull=False,parents_mobile_no__isnull=False,college_work__isnull=False)
            if profile.profile_picture:
                return function(request, *args, **kwargs)   
            else:
                return redirect('/admin')

        except:
            
            return redirect('/admin')

  return wrap

def update_name(request):
    users  = User.objects.all()

    for user in users:
        if user.name:
            user.first_name = user.name
            user.save()

    return JsonResponse({'status':'done'})

def signup(request):
    if request.method == "POST":
        data = dict()
        form = Signup_Form (request.POST)
        if form.is_valid():
            group = Group.objects.get(id=request.POST['groups'])
            if group.name == "Artist":                  
                user = form.save(commit=False)
                user.username=form.cleaned_data['email']
            else:
                user = form.save(commit=False)
                user.username=form.cleaned_data['email']
                user.first_name = form.cleaned_data['first_name'] + ' ' + form.cleaned_data['last_name']
                user.last_name = ''
                user.name  = ''
                

            user.is_active = False
            user.save()    
            groups = form.cleaned_data['groups']
            for group in groups:
                user.groups.add(group) 
                
                if group.name == "Artist":
                    musician = Musician.objects.create(user=user)
                elif group.name == "Music School":
                    ms = Gurukulam.objects.create(user=user)
                elif group.name == "Event Organizer":
                    organizer = Event_Organizer.objects.create(user=user)
                elif group.name == "Band":
                    troupe = Troupe.objects.create(user=user)
                elif group.name == "Music Lover":
                    music_lover = Music_Lover.objects.create(user=user)


            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('registration/account_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': force_str(urlsafe_base64_encode(force_bytes(user.pk))),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            data['valid'] = True
            return redirect('/registered-successfully/')

        else:         
            return render(request,'registration/signup.html',{'form':form,})
    else:       
        form = Signup_Form()
    context = {
            'form':form,
           }
    return render(request,'registration/signup.html',context)

def registered(request):
    return HttpResponse("Registered")

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.verified_email = True
        user.save()
        return render(request,'account/email_verified.html')        
    else:
        return HttpResponse('Activation link is invalid!')

class CustomLoginView(LoginView):
    authentication_form = CustomAuthForm
    redirect_authenticated_user = True

def logout(request):
    request.session['is_logout'] = True
    user_logout(request)
    return render(request,'account/logout.html', {})

def profile(request,pk):
    user_object = User.objects.get(id=pk)
    posts = Post.objects.filter(user=user_object)
    for group in user_object.groups.all():
        if group.name == "Artist":
            is_musician = True
            troupes = Key_Performer.objects.filter(musician=user_object.musician)
            event_performer_requests = Event_Performer.objects.filter(musician=user_object.musician)
            highlights = Highlight.objects.filter(user=user_object)
            testimonials = Gurukulam_Testimonial.objects.filter(musician=user_object.musician)
            gurukulas = Musician_Gurukulam.objects.filter(status="A",musician=user_object.musician)    
            context  = {
                'is_musician' : is_musician,
                'troupes':troupes,
                'event_performer_requests':event_performer_requests,
                'highlights':highlights,
                'testimonials':testimonials,
                'gurukulas':gurukulas,
                'posts':posts,
                'user_object' :user_object,
            }

        elif group.name == "Event Organizer":
            is_event_organizer = True
            highlights = Highlight.objects.filter(user=user_object)
            events = Event.objects.filter(event_organizer=user_object.event_organizer,to_date__lt=datetime.now())
            performers = Event_Performer.objects.filter(event_organizer=user_object.event_organizer,status="A")

            context = { 
                'posts':posts,
                'highlights':highlights,
                'events'  : events,  
                'key_performers': performers ,  
                'user_object' :user_object,
                'is_event_organizer':is_event_organizer,    
            }        
        elif group.name == "Music School":
            gurukulam_skills = Gurukulam_Skill.objects.filter(gurukulam=user_object.gurukulam)
            courses = Course.objects.filter(gurukulam=user_object.gurukulam)
            lecture_videos = Lecture_Video.objects.filter(gurukulam=user_object.gurukulam)
            gurukulam_awards = Gurukulam_Award.objects.filter(gurukulam=user_object.gurukulam)
            testimonials = Gurukulam_Testimonial.objects.filter(gurukulam=user_object.gurukulam)
            teachers = Gurukulam_Teacher.objects.filter(gurukulam=user_object.gurukulam,status="A")
            context = {
                'posts':posts,
                'is_gurukulam'    : True,
                'gurukulam_skills'  :gurukulam_skills,
                'gurukulam_awards'  : gurukulam_awards,
                'gurukulam_testimonials':testimonials,
                'lecture_videos'    :lecture_videos,
                'courses'            :courses,
                'teachers'          : teachers,
                'user_object' :user_object,
            }
        elif group.name == "Band":
            troupe_highlights = Highlight.objects.filter(user=user_object)
            key_performers = Key_Performer.objects.filter(troupe=user_object.troupe)
            troupe_skills = Troupe_Skill.objects.filter(troupe=user_object.troupe)
            context = {  
                'posts':posts,
                'troupe_highlights':troupe_highlights,   
                'key_performers'   :key_performers, 
                'troupe_skills'   : troupe_skills, 
                'is_troupe' : True,
                'user_object' :user_object,
            }    
        context['user_object']  = user_object
        return render(request,'account/profile.html', context)

# Bookmark an event
@complete_profile
@login_required(login_url='signin')
def home(request):
    recent_followers = UserFollowing.objects.filter(following_user_id=request.user.id )[:5]
    user_groups = request.user.groups.all()
    user = request.user
    followers = UserFollowing.objects.filter(following_user_id=request.user).order_by('-id')[:8]    
    skill_categories = Skill_Category.objects.all()
    event_categories = Event_Category.objects.all()
    skills = Skill.objects.all()
    locations = Location.objects.all()
    event_types = Event_Type.objects.all()
    unread_message_count = Message.unread_count(user)
    musicians = Musician.objects.filter().exclude(user=request.user)[:5]
    troupes = Troupe.objects.filter().exclude(user=request.user)[:5]
    gurukulas = Gurukulam.objects.filter().exclude(user=request.user)[:5]
    skill_levels = Skill_Level.objects.all()
    latest_events = Event.objects.filter(registration_close_date__gte=datetime.now())[:5]
    top_events = Event.objects.annotate(like_count=Count('user_likes')).order_by('-like_count')[:5]
    events_at_location = Event.objects.filter(location=user.location)[:5]
    following = UserFollowing.objects.filter(user=request.user).order_by('-id')[:8]

    following_user_ids = UserFollowing.objects.filter(user=request.user).values_list('following_user_id', flat=True)
    
    organizer_events = Event.objects.filter(
        Q(event_organizer__user__in=following_user_ids) | Q(gurukulam__user__in=following_user_ids)
    )

    participant_events = Event.objects.filter(
        Q(interest__musician__user__in=following_user_ids, interest__status="A") | 
        Q(interest__troupe__user__in=following_user_ids, interest__status="A") |
        Q(invitation__musician__user__in=following_user_ids, invitation__status="A") |
        Q(invitation__troupe__user__in=following_user_ids, invitation__status="A")
    ).distinct()
   
    organizer_events_list = list(organizer_events)
    participant_events_list = list(participant_events)
    
    recommended_events = list(set(organizer_events_list + participant_events_list))
    
    total_count = Post.objects.all().order_by('-id').count()
    if total_count > 10:
        load_more_post = True
    else:
        load_more_post = False

    popular_events = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False).annotate(like_count=Count('user_likes')).order_by('-like_count')

    if user.location:
        for group in user_groups:
            if group.name == "Artist":
                sent_requests = Interest.objects.filter(musician=request.user.musician).values_list('event__id', flat=True)
                received_requests = Invitation.objects.filter(musician=request.user.musician).values_list('event__id', flat=True)
                musician_skills = Musician_Skill.objects.filter(musician=request.user.musician).values_list('skill__id', flat=True)
            
                if not sent_requests and  not received_requests:                
                    events = Event.objects.filter(location=user.location,registration_close_date__gte=datetime.now(),self_reference=False).distinct()[:50]
                elif  sent_requests and  not received_requests:
                    events = Event.objects.filter(location=user.location,registration_close_date__gte=datetime.now(),self_reference=False).distinct().exclude(id__in=sent_requests)[:50]
                elif not sent_requests and  received_requests:
                    events = Event.objects.filter(location=user.location,registration_close_date__gte=datetime.now(),self_reference=False).distinct().exclude(id__in=received_requests)[:50]    
                else:
                    event_exclude_ids_list = chain(sent_requests, received_requests)
                    events = Event.objects.filter(location=user.location,registration_close_date__gte=datetime.now(),self_reference=False).distinct().exclude(id__in=event_exclude_ids_list)[:50]
                
                posts = Post.objects.all().order_by('-id')[:10]
                followers_friends = list(UserFollowing.objects.filter(following_user_id=request.user.id).values_list('user__id',flat=True).order_by('?')[:3])

                eventer  = Event_Skill.objects.filter(skill__id__in=musician_skills,event__event_organizer__isnull=False).values_list('event__event_organizer__user__id', flat=True).order_by('?')[:2]
                
                recommended_people = list(followers_friends) + list(eventer)
                recommended_people = [*set(recommended_people)]
                

                top_peoples = User.objects.filter(id__in=recommended_people).exclude(id=request.user.id,groups__name="Music Lover")[:5]
                musician_skills = Musician_Skill.objects.filter(musician=request.user.musician).values_list('skill__id', flat=True)
                #events = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False).exclude(Q(invitation__musician=request.user.musician) | Q(interest__musician=request.user.musician))
                watch_lists = Event.objects.filter(user_likes=user).distinct()
                top_artists = Musician.objects.annotate(followers_count=Count('user__following__user')).order_by('-followers_count')[:20] 

                context = {
                    'event_categories':event_categories,
                    'followers' : followers,
                    'posts' : posts,
                    'top_peoples' : top_peoples,
                    'events' : events,
                    'skills':skills,
                    'locations':locations,
                    'event_types':event_types,
                    'event_categories':event_categories,
                    'skill_categories':skill_categories,
                    'unread_message_count' : unread_message_count,
                    'load_more_post':load_more_post,
                    'locations':locations,
                    'place':'home',
                    'musicians':musicians,
                    'troupes':troupes,
                    'gurukulas':gurukulas,
                    'skill_levels':skill_levels,
                    'latest_events':latest_events,
                    'musician_skills':musician_skills,
                    'recommended_events':recommended_events,
                    'watch_lists':watch_lists,
                    'top_artists':top_artists,
                    'recent_followers':recent_followers,
                    'popular_events':popular_events
                }
                return render(request,'musician/home.html', context)
            
            elif group.name == "Event Organizer":
                form = Event_Form()
                top_peoples = User.objects.filter(location=user.location,groups__name__in=('Musician','Event Organizer','Gurukulam','Troupe')).exclude(id=request.user.id).order_by('-id')[:5]            
                events = Event.objects.filter(location=user.location,registration_close_date__gte=datetime.now())[:20]
                posts = Post.objects.all().order_by('-id')[:10]
                #invitation_msg =  list(Message.objects.filter(invitation__event__event_organizer=request.user.event_organizer).annotate(last=Max('invitation__message__sent_on')).filter(sent_on=F('last')).order_by('-sent_on').values_list('id',flat=True)[:3])
                #interest_msg =  list(Message.objects.filter(interest__event__event_organizer=request.user.event_organizer).annotate(last=Max('interest__message__sent_on')).filter(sent_on=F('last')).order_by('-sent_on').values_list('id',flat=True)[:3])
                #msg_ids = invitation_msg + interest_msg
                #chats = Message.objects.filter(id__in=msg_ids).order_by('sent_on')[:5]
                watch_lists = Event.objects.filter(user_likes=user).distinct()
                top_artists = Musician.objects.annotate(followers_count=Count('user__following__user')).order_by('-followers_count')[:20] 
                context = {
                    'followers' : followers,
                    'top_peoples' : top_peoples,
                    'events':events,
                    'posts' : posts,
                    'locations':locations,
                    'skill_levels':skill_levels,
                    'form':form,
                    'skills':skills,
                    'locations':locations,
                    'event_types':event_types,
                    'skill_categories':skill_categories,
                    'event_categories':event_categories,
                    'load_more_post':load_more_post,
                    'place':'home',   
                    'musicians':musicians,
                    'troupes':troupes,
                    'gurukulas':gurukulas,   
                    'latest_events':latest_events, 
                    'watch_lists':watch_lists,  
                    'top_artists':top_artists,    
                    'recent_followers':recent_followers,  
                    'popular_events':popular_events, 

                }

                return render(request,'musician/home.html', context)

            elif group.name == "Music School":
                events = Event.objects.filter(location=user.location,registration_close_date__gte=datetime.now()).order_by('-id')[:30]
                form = Event_Form()
                top_peoples = User.objects.filter(location=user.location,groups__name__in=('Musician','Event Organizer','Gurukulam','Troupe')).exclude(id=request.user.id)[:5]
                invitation_msg =  list(Message.objects.filter(invitation__event__gurukulam=request.user.gurukulam).annotate(last=Max('invitation__message__sent_on')).filter(sent_on=F('last')).order_by('-sent_on').values_list('id',flat=True)[:3])
                interest_msg =  list(Message.objects.filter(interest__event__gurukulam=request.user.gurukulam).annotate(last=Max('interest__message__sent_on')).filter(sent_on=F('last')).order_by('-sent_on').values_list('id',flat=True)[:3])
                msg_ids = invitation_msg + interest_msg
                chats = Message.objects.filter(id__in=msg_ids).order_by('sent_on')[:5]
                skill_categories = Skill_Category.objects.all()
                posts = Post.objects.all().order_by('-id')[:10]
                watch_lists = Event.objects.filter(user_likes=user).distinct()
                top_artists = Musician.objects.annotate(followers_count=Count('user__following__user')).order_by('-followers_count')[:20] 
                context = { 
                    'posts':posts,               
                    'form':form,
                    'place':'home',
                    'chats':chats,
                    'events':events,
                    'followers' : followers,
                    'top_peoples':top_peoples,
                    'skill_categories':skill_categories,
                    'load_more_post':load_more_post,
                    'skills':skills,
                    'locations':locations,
                    'event_types':event_types,
                    'event_categories':event_categories,
                    'skill_levels':skill_levels,
                    'musicians':musicians,
                    'troupes':troupes,
                    'gurukulas':gurukulas,
                    'latest_events':latest_events,
                    'watch_lists':watch_lists,
                    'top_artists':top_artists,
                    'recent_followers':recent_followers,
                    'popular_events':popular_events,
                
                }

                return render(request,'musician/home.html', context)

            elif group.name == "Music Lover":               

               # events = Event.objects.filter(location=user.location,registration_close_date__gte=datetime.now())[:20]
                top_peoples = User.objects.filter(location=user.location,groups__name__in=('Musician','Event Organizer','Gurukulam','Troupe')).exclude(id=request.user.id)[:5] 
                top_events = Event.objects.annotate(like_count=Count('user_likes')).order_by('-like_count')[:5]
                events_at_location = Event.objects.filter(location=user.location)[:5]
                following = UserFollowing.objects.filter(user=request.user).order_by('-id')[:8]
                liked_events = Event.objects.filter(user_likes=user)

                #bookmarked_events = Bookmark.objects.filter(user=request.user).values_list('event', flat=True)
                #bookmarked_events_list = Event.objects.filter(id__in=bookmarked_events)    
                watch_lists = Event.objects.filter(user_likes=user).distinct()
                top_artists = Musician.objects.annotate(followers_count=Count('user__following__user')).order_by('-followers_count')[:20] 

                context = { 
                    #'events':events,
                    'top_events':top_events, 
                    'locations':locations,
                    'musicians':musicians,
                    'following':following,
                    'top_peoples' : top_peoples,
                    'followers' : followers,
                    'troupes':troupes,
                    'gurukulas':gurukulas,
                    'latest_events':latest_events,
                    'events_at_location':events_at_location,
                    'recommended_events':recommended_events,
                    #'bookmarked_events': bookmarked_events_list,
                     'liked_events': liked_events,  
                     'watch_lists':watch_lists,
                     'top_artists':top_artists,
                     'recent_followers':recent_followers,    
                     'popular_events':popular_events,       

                }

                return render(request,'musician/home.html', context)


            elif group.name == "Band":
                top_peoples = User.objects.filter(location=user.location,groups__name__in=('Musician','Event Organizer','Gurukulam','Troupe')).exclude(id=request.user.id)[:5]
                posts = Post.objects.all().order_by('-id')[:10]
                events = Event.objects.filter(location=request.user.location,registration_close_date__gte=datetime.now(),self_reference=False).exclude(Q(invitation__troupe=request.user.troupe) | Q(interest__troupe=request.user.troupe))
            
                context = {
                    'followers' : followers,              
                    'posts' : posts,
                    'top_peoples' : top_peoples,
                    'events' : events,
                    'skills':skills,
                    'skill_levels':skill_levels,
                    'place':'home',
                    'locations':locations,
                    'event_types':event_types,
                    'event_categories':event_categories,
                    'skill_categories':skill_categories,
                    'load_more_post':load_more_post,
                    'musicians':musicians,
                    'troupes':troupes,
                    'gurukulas':gurukulas,
                    'latest_events':latest_events,
                    'recent_followers':recent_followers,
                    'popular_events':popular_events,
                    
                }
                return render(request ,'musician/home.html',context)
        context = {}
        return render(request,'musician/home.html', context)
    else:
        for group in user_groups:
            if group.name == "Artist":
                sent_requests = Interest.objects.filter(musician=request.user.musician).values_list('event__id', flat=True)
                received_requests = Invitation.objects.filter(musician=request.user.musician).values_list('event__id', flat=True)
                musician_skills = Musician_Skill.objects.filter(musician=request.user.musician).values_list('skill__id', flat=True)
            
                if not sent_requests and  not received_requests:
                    events = Event.objects.filter(registration_close_date__gte=datetime.now(),event_skill__skill__id__in=musician_skills,self_reference=False).distinct()[:50]
                elif  sent_requests and  not received_requests:
                    events = Event.objects.filter(registration_close_date__gte=datetime.now(),event_skill__skill__id__in=musician_skills,self_reference=False).distinct().exclude(id__in=sent_requests)[:50]
                elif not sent_requests and  received_requests:
                    events = Event.objects.filter(registration_close_date__gte=datetime.now(),event_skill__skill__id__in=musician_skills,self_reference=False).distinct().exclude(id__in=received_requests)[:50]    
                else:
                    event_exclude_ids_list = chain(sent_requests, received_requests)
                    events = Event.objects.filter(registration_close_date__gte=datetime.now(),event_skill__skill__id__in=musician_skills,self_reference=False).distinct().exclude(id__in=event_exclude_ids_list)[:50]
                
                posts = Post.objects.all().order_by('-id')[:10]
                top_peoples = User.objects.filter(groups__name__in=('Musician','Event Organizer','Gurukulam','Troupe'))[:5]


                musician_skills = Musician_Skill.objects.filter(musician=request.user.musician).values_list('skill__id', flat=True)
                events = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False).exclude(Q(invitation__musician=request.user.musician) | Q(interest__musician=request.user.musician))
                
                context = {
                    'event_categories':event_categories,
                    'followers' : followers,
                    'posts' : posts,
                    'top_peoples' : top_peoples,
                    'events' : events,
                    'skills':skills,
                    'locations':locations,
                    'event_types':event_types,
                    'event_categories':event_categories,
                    'skill_categories':skill_categories,
                    'unread_message_count' : unread_message_count,
                    'load_more_post':load_more_post,
                    'place':'home',
                    'skill_levels':skill_levels,
                    'musicians':musicians,
                    'troupes':troupes,
                    'gurukulas':gurukulas,
                    'latest_events':latest_events,
                    'recent_followers':recent_followers,
                    'popular_events':popular_events,
                }
                return render(request,'musician/home.html', context)

            
            elif group.name == "Music Lover":

               # events = Event.objects.filter(location=user.location,registration_close_date__gte=datetime.now())[:20]
                top_peoples = User.objects.filter(location=user.location,groups__name__in=('Musician','Event Organizer','Gurukulam','Troupe')).exclude(id=request.user.id)[:5] 
                top_events = Event.objects.annotate(like_count=Count('user_likes')).order_by('-like_count')[:5]
                events_at_location = Event.objects.filter(location=user.location)[:15]
                    
                context = { 
                    #'events':events,
                    'top_events':top_events, 
                    'locations':locations,
                    'musicians':musicians,
                    'top_peoples' : top_peoples,
                    'followers' : followers,
                    'troupes':troupes,
                    'gurukulas':gurukulas,
                    'latest_events':latest_events,
                    'bookmarked_events': bookmarked_events,
                    'events_at_location':events_at_location,
                    'recommended_events':recommended_events,
                    'recent_followers':recent_followers,
                    'popular_events':popular_events,
                }

                return render(request,'musician/home.html', context)
            
            elif group.name == "Event Organizer":
                form = Event_Form()
                top_peoples = User.objects.all().order_by('-id')[:7]            
                events = Event.objects.filter(registration_close_date__gte=datetime.now())[:20]
                posts = Post.objects.all().order_by('-id')[:10]
       
                context = {
                    'followers' : followers,
                    'top_peoples' : top_peoples,
                    'events':events,
                    'posts' : posts,
                    'cities':cities,
                    'skill_levels':skill_levels,
                    'form':form,
                    'skills':skills,
                    'locations':locations,
                    'event_types':event_types,
                    'skill_categories':skill_categories,
                    'event_categories':event_categories,
                    'load_more_post':load_more_post,
                    'place':'home',
                    'musicians':musicians,
                    'troupes':troupes,
                    'gurukulas':gurukulas,
                    'latest_events':latest_events,  
                    'recent_followers':recent_followers,  
                    'popular_events':popular_events,            

                }

                return render(request,'musician/home.html', context)

            elif group.name == "Gurukulam":
                events = Event.objects.all().order_by('-id')[:30]
                form = Event_Form()
                top_peoples = User.objects.filter(groups__name__in=('Musician','Event Organizer','Gurukulam','Troupe'))[:5]
                invitation_msg =  list(Message.objects.filter(invitation__event__gurukulam=request.user.gurukulam).annotate(last=Max('invitation__message__sent_on')).filter(sent_on=F('last')).order_by('-sent_on').values_list('id',flat=True)[:3])
                interest_msg =  list(Message.objects.filter(interest__event__gurukulam=request.user.gurukulam).annotate(last=Max('interest__message__sent_on')).filter(sent_on=F('last')).order_by('-sent_on').values_list('id',flat=True)[:3])
                msg_ids = invitation_msg + interest_msg
                chats = Message.objects.filter(id__in=msg_ids).order_by('sent_on')[:5]
                skill_categories = Skill_Category.objects.all()
                posts = Post.objects.all().order_by('-id')[:10]
                context = { 
                    'posts':posts,               
                    'form':form,
                    'cities':cities,
                    'chats':chats,
                    'skill_levels':skill_levels,
                    'events':events,
                    'followers' : followers,
                    'top_peoples':top_peoples,
                    'skill_categories':skill_categories,
                    'load_more_post':load_more_post,
                    'skills':skills,
                    'locations':locations,
                    'event_types':event_types,
                    'event_categories':event_categories,
                    'place':'home',
                    'musicians':musicians,
                    'troupes':troupes,
                    'gurukulas':gurukulas,  
                    'latest_events':latest_events,    
                    'recent_followers':recent_followers,    
                    'popular_events':popular_events,      
                }
                return render(request,'musician/home.html', context)

            elif group.name == "Band":
                top_peoples = User.objects.filter(groups__name__in=('Musician','Event Organizer','Gurukulam','Troupe'))[:5]
                posts = Post.objects.all().order_by('-id')[:10]
                events = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False).exclude(Q(invitation__troupe=request.user.troupe) | Q(interest__troupe=request.user.troupe))
                context = {
                    'followers' : followers,              
                    'posts' : posts,
                    'cities':cities,
                    'top_peoples' : top_peoples,
                    'events' : events,
                    'skills':skills,
                    'skill_levels':skill_levels,
                    'locations':locations,
                    'event_types':event_types,
                    'event_categories':event_categories,
                    'skill_categories':skill_categories,
                    'load_more_post':load_more_post,
                    'place':'home',
                    'latest_events':latest_events,
                    'recent_followers':recent_followers,
                    'popular_events':popular_events,
                    
                }
                return render(request ,'musician/home.html',context)
        context = {}
        return render(request,'musician/home.html', context)

@login_required(login_url='signin')
def my_opportunities(request,type):
    user = request.user
    if type == "invitation":
        status = request.GET.get('status')
        if not status:
            status_filter = ('R','A','S')
        else:
            status_filter = status
        if user.groups.filter(name='Artist').exists():
            invitations = Invitation.objects.filter(musician=user.musician,status__in=status_filter)
        elif user.groups.filter(name='Band').exists():
            invitations = Invitation.objects.filter(troupe=user.troupe,status__in=status_filter)
        page = request.GET.get('page', 1)    
        paginator = Paginator(invitations, 20)
        try:
            invitations = paginator.page(page)
        except PageNotAnInteger:
            invitations = paginator.page(1)
        except EmptyPage:
            invitations = paginator.page(paginator.num_pages)    
        
        context = {
            'invitations' : invitations,
            'page' : page,
            'status': status,
            'type'   : type,
         }
    elif type == "interest":
        status = request.GET.get('status')
        if not status:
            status_filter = ('R','A','S')
        else:
            status_filter = status
        if user.groups.filter(name='Artist').exists():
            interests = Interest.objects.filter(musician=user.musician,status__in=status_filter)
        elif user.groups.filter(name='Band').exists():
            interests = Interest.objects.filter(troupe=user.troupe,status__in=status_filter)
        page = request.GET.get('page', 1)             
        paginator = Paginator(interests, 20)
        try:
            interests = paginator.page(page)
        except PageNotAnInteger:
            interests = paginator.page(1)
        except EmptyPage:
            interests = paginator.page(paginator.num_pages)    
        context = {
            'interests' : interests,
            'page' : page,
            'status': status,
            'interest_tab_active': True,
            'type'  : type,
         }
    return render(request, 'my_opportunities.html', context)

@login_required(login_url='signin')
def edit_profile(request):
    musician = Musician.objects.get(user=request.user)
    if request.method == 'POST':
        form = EditMusicianUserForm(request.POST,request.FILES, instance=request.user)
        musician_form = MusicianForm(request.POST,instance=musician)      
        if form.is_valid() and musician_form.is_valid():           
            form.save()   
            musician_form.save()   
            return redirect('my_profile')
        else:
            return render(request,'musician/edit_profile.html', {'form': form,'musician_form':musician_form,})      
    else:        
        form = EditMusicianUserForm(instance=request.user)
        musician_form = MusicianForm(instance=musician)              
        return render(request,'musician/edit_profile.html', {'form': form,'musician_form':musician_form,})

@login_required(login_url='signin')
def edit_profile_music_lover(request):
    music_lover = Music_Lover.objects.get(user=request.user)
    if request.method == 'POST':
        form = EditMusicLoverUserForm(request.POST,request.FILES, instance=request.user)
        music_lover_form = MusicLoverForm(request.POST,instance=music_lover)      
        if form.is_valid() and music_lover_form.is_valid():           
            form.save()   
            music_lover_form.save()   
            return redirect('my_profile')
        else:
            return render(request,'music_lover/edit_profile.html', {'form': form,'music_lover_form':music_lover_form,})      
    else:        
        form = EditMusicLoverUserForm(instance=request.user)
        music_lover_form = MusicLoverForm(instance=music_lover)              
        return render(request,'music_lover/edit_profile.html', {'form': form,'music_lover_form':music_lover_form,})

#gurukulam
@login_required(login_url='signin')
def view_student(request):
    if request.method == "POST":
        status = request.POST.get('status')
        student_id = request.POST.get('student_id')
        if status == "A":
            status = Musician_Gurukulam.objects.filter(id=student_id).update(status=status)
        elif status == "R":            
            status = Musician_Gurukulam.objects.filter(id=student_id).update(status=status)
        students = Musician_Gurukulam.objects.filter(gurukulam=request.user.gurukulam)       
    else:
        students = Musician_Gurukulam.objects.filter(~Q(sender=request.user),gurukulam=request.user.gurukulam,)
    context = {
        'students' : students,
    }
    return render(request, 'gurukulam/view_students.html', context)

@login_required(login_url='signin')
def view_teacher(request):
    if request.method == "POST":
        status = request.POST.get('status')
        student_id = request.POST.get('student_id')
        if status == "A":
            status = Gurukulam_Teacher.objects.filter(id=student_id).update(status=status)
        elif status == "R":            
            status = Gurukulam_Teacher.objects.filter(id=student_id).update(status=status)
        students = Gurukulam_Teacher.objects.filter(gurukulam=request.user.gurukulam)       
    else:
        students = Gurukulam_Teacher.objects.filter(~Q(sender=request.user),gurukulam=request.user.gurukulam,)
    context = {
        'students' : students,
    }

    return render(request, 'gurukulam/view_teachers.html', context)

@login_required(login_url='signin')
def view_sent_request(request):
    pendind_requests =  Musician_Gurukulam.objects.filter(sender=request.user,gurukulam=request.user.gurukulam,status="S")
    accepted_requests = Musician_Gurukulam.objects.filter(sender=request.user,gurukulam=request.user.gurukulam,status="A")
    rejected_requests = Musician_Gurukulam.objects.filter(sender=request.user,gurukulam=request.user.gurukulam,status="R")
    context = {
        'pendind_requests':pendind_requests,
        'accepted_requests':accepted_requests,
        'rejected_requests' : rejected_requests,
    }
    return render(request, 'gurukulam/view_sent_request.html', context)

def gurukulam_edit_profile(request):
    gurukulam = Gurukulam.objects.get(user=request.user)
    if request.method == 'POST':
        form = EditGurukulamUserForm(request.POST,request.FILES, instance=request.user)
        gurukulam_form = GurukulamForm(request.POST,instance=gurukulam)       

        if form.is_valid() and gurukulam_form.is_valid():           
            form.save()   
            gurukulam_form.save()   
            return redirect('my_profile')
        else:
            return render(request,'gurukualm/gurukulam_edit_profile.html', {'form': form,'gurukulam_form':gurukulam_form,})

    else:        
        form = EditGurukulamUserForm(instance=request.user)
        gurukulam_form = GurukulamForm(instance=gurukulam)              
        return render(request,'gurukulam/gurukulam_edit_profile.html', {'form': form,'gurukulam_form':gurukulam_form,})

def troupe_invitation(request,pk):
    troupe_invitation = Key_Performer.objects.get(id=pk,musician=request.user.musician) 
    top_peoples = User.objects.all()[:7]
       
    if request.method == 'POST':
        status = request.POST.get('status')
        status = Key_Performer.objects.filter(id=pk).update(status=status)
        return redirect('troupe_invitation',pk=pk)       
        
    else:
        pass
        
    context ={
        'troupe_invitation' : troupe_invitation, 
        'top_peoples' : top_peoples,      

      }   

    return render(request,'musician/view_troupe_invitation.html', context)

def troupe_edit_profile(request):
    troupe = Troupe.objects.get(user=request.user)
    if request.method == 'POST':
        form = Edit_Troupe_UserForm(request.POST,request.FILES, instance=request.user)
        troupe_form = Troup_Profile_Form(request.POST,instance=troupe)       

        if form.is_valid() and troupe_form.is_valid():           
            form.save()   
            troupe_form.save()   
            return redirect('my_profile')
        else:
            return render(request,'troupe/troupe_edit_profile.html', {'form': form,'troupe_form':troupe_form,})

    else:        
        form = Edit_Troupe_UserForm(instance=request.user)
        troupe_form = Troup_Profile_Form(instance=troupe)              
        return render(request,'troupe/troupe_edit_profile.html', {'form': form,'troupe_form':troupe_form,})

def event_organizer_edit_profile(request):
    event_organizer = Event_Organizer.objects.get(user=request.user)
    if request.method == 'POST':
        form = Edit_Troupe_UserForm(request.POST,request.FILES, instance=request.user)
        event_org_form = Event_Org_Profile_Form(request.POST,instance=event_organizer)       

        if form.is_valid() and event_org_form.is_valid():           
            form.save()   
            event_org_form.save()   
            return redirect('my_profile')
        else:
            return render(request,'event_organizer/edit_profile.html', {'form': form,'event_org_form':event_org_form,})

    else:        
        form = Edit_Troupe_UserForm(instance=request.user)
        event_org_form = Event_Org_Profile_Form(instance=event_organizer)              
        return render(request,'event_organizer/edit_profile.html', {'form': form,'event_org_form':event_org_form,})

def ajax_event_edit(request,model_name,pk):
    
    user = request.user
    if user.groups.filter(name='Event Organizer').exists():
        event = Event.objects.get(id=pk,event_organizer=user.event_organizer)
    if user.groups.filter(name='Music School').exists():
        event = Event.objects.get(id=pk,gurukulam=user.gurukulam)

    page=request.GET.get('page', None)
    
    data = dict()
    event_skills = Event_Skill.objects.filter(event=event)
    skill_id = request.POST.getlist("skill")
        
    if request.method == 'POST':      
        form = Event_Form(request.POST,request.FILES, instance=event)
        if form.is_valid():          
            event = form.save(commit=False)      
            event.save()

            for skill in skill_id:
                skill = Skill.objects.get(id=skill)
                event_skill = Event_Skill.objects.create(event=event,skill=skill)
           
            if user.groups.filter(name='Event Organizer').exists():
                if page == "recent_event":
                    events = Event.objects.filter(event_organizer=request.user.event_organizer,to_date__gte=datetime.now()).order_by('-from_date')
                elif page == "all_event":
                    events = Event.objects.filter(event_organizer=request.user.event_organizer).order_by('-from_date')                  
                else:
                    events = Event.objects.filter(event_organizer=request.user.event_organizer).order_by('-from_date')

            elif user.groups.filter(name='Music School').exists():
                if page == "home":
                    events = Event.objects.filter(gurukulam=request.user.gurukulam,to_date__gte=datetime.now()).order_by('-from_date')
                else:
                    events = Event.objects.filter(gurukulam=request.user.gurukulam).order_by('-from_date')

            data['valid'] = True
            if page == "event_details":
                data['event_details_top_div'] = render_to_string('event/event-details-top-div.html',{'event':event},request)
                data['title'] = event.name
                data['detailshtml'] = render_to_string('event/event-details-details-div.html',{'event':event},request)
            else:
                data['html'] = render_to_string('event_organizer/events.html',{'events':events,'page':page,},request)

        else:          
            data['valid'] = False
            data['form'] = render_to_string('event/create_event_form.html',{'form':form,'operation':'Update','model_name':"event",'event_id':pk,'page':page,},request)
        
    else:
        
        form = Event_Form(instance=event)
        data['form'] = render_to_string('event/create_event_form.html',{'form':form,'operation':'Update','model_name':"event",'event_id':pk,'page':page,'event_skills':event_skills,},request)

    return JsonResponse(data)

def ajax_add_event_performer(request):
    user = request.user
    data = dict()
    if request.method == 'POST':
        
        form = Event_Performer_Form(request.POST)
        if form.is_valid():            
            performer = form.save(commit=False)            
            performer.event_organizer = user.event_organizer   
            performer.status = "S"   
            performer.save()  

            link= str(request.META['HTTP_HOST'])+'/event_performer_invitation/'+str(performer.id)
            if  performer.musician:
                mail_to = performer.musician.user.email
            elif performer.troupe:
                mail_to = performer.troupe.user.email       

            subject = 'Event Performer - Reg'
            message = str(request.user) +' has added you as a their Event Performer, please accept or reject his offer by clicking here. Link: {}'.format(link)     
            send_email(subject,mail_to,message)
             
            performers = Event_Performer.objects.filter(event_organizer = user.event_organizer)
            data['valid'] = True
            data['html'] = render_to_string('event_organizer/performers.html',{'performers':performers,},request)

        else:
            data['valid'] = False
            data['form'] = render_to_string('event_organizer/performer_form.html',{'form':form,'operation':'Add',},request)
        
    else:
        form = Event_Performer_Form()
        data['form'] = render_to_string('event_organizer/performer_form.html',{'form':form,'operation':'Add',},request)

    return JsonResponse(data)

def ajax_delete_event_performer(request,pk):
    data = dict()
    performer = Event_Performer.objects.get(id=pk)
    user = request.user
    if performer.event_organizer == user.event_organizer:
        performer.delete()
        performers = Event_Performer.objects.filter(event_organizer = user.event_organizer)
        data['valid'] = True
        data['html'] = render_to_string('event_organizer/performers.html',{'performers':performers,},request)

    else:
        data['valid'] = False
    return JsonResponse(data) 

def ajax_event_delete(request,model_name,pk):
    user = request.user
    data = dict()
    event = Event.objects.get(id=pk)
    page=request.GET.get('page', None)

    if request.user.groups.filter(name='Event Organizer').exists():
        if event.event_organizer == request.user.event_organizer:
            event.delete()

            if page == "home":
                events = Event.objects.filter(event_organizer=request.user.event_organizer,to_date__gte=datetime.now())
            else:
                events = Event.objects.filter(event_organizer=request.user.event_organizer)
            data['valid'] = True
            data['html'] = render_to_string('event_organizer/events.html',{'events':events},request)
    elif request.user.groups.filter(name='Gurukulam').exists():

        if event.gurukulam== request.user.gurukulam:
            event.delete()
            events = Event.objects.filter(gurukulam=request.user.gurukulam)
            data['valid'] = True
            data['html'] = render_to_string('event_organizer/events.html',{'events':events},request)
                
    else:
        data['valid'] = False

    return JsonResponse(data)

def ajax_create_event_organizer_highlight(request):
    user = request.user
    data = dict()
    if request.method == 'POST':
        form = Event_Organizer_Highlight_Form(request.POST)
        if form.is_valid():            
            highlight = form.save(commit=False)            
            highlight.event_organizer = user.event_organizer      
            highlight.save()  
            form.save_m2m() 
            highlights = Event_Organizer_Highlight.objects.filter(event_organizer=request.user.event_organizer)
            data['valid'] = True
            data['html'] = render_to_string('event_organizer/highlights.html',{'highlights':highlights},request)            
        else:
            data['valid'] = False
            data['form'] = render_to_string('event_organizer/highlight_form.html',{'form':form,'operation':'Add',},request)
        
    else:
        form = Event_Organizer_Highlight_Form()
        data['form'] = render_to_string('event_organizer/highlight_form.html',{'form':form,'operation':'Add',},request)

    return JsonResponse(data)

def ajax_edit_event_organizer_highlight(request,pk):
    user = request.user
    data = dict()
    highlight =  Event_Organizer_Highlight.objects.get(id=pk,event_organizer=user.event_organizer)
    if request.method == 'POST':
        form = Event_Organizer_Highlight_Form(request.POST,instance=highlight)
        if form.is_valid():            
            highlight = form.save(commit=False)            
            highlight.event_organizer = user.event_organizer      
            highlight.save()  
            form.save_m2m() 
            highlights = Event_Organizer_Highlight.objects.filter(event_organizer=request.user.event_organizer)
            
            data['valid'] = True
            data['html'] = render_to_string('event_organizer/highlights.html',{'highlights':highlights},request)
            
        else:
            data['valid'] = False
            data['form'] = render_to_string('event_organizer/highlight_form.html',{'form':form,'operation':'Update','highlight_id':pk},request)
        
    else:
        form = Event_Organizer_Highlight_Form(instance=highlight)
        data['form'] = render_to_string('event_organizer/highlight_form.html',{'form':form,'operation':'Update','highlight_id':pk,},request)

    return JsonResponse(data)

def ajax_delete_eventer_highlight(request,pk):
    user = request.user
    data = dict()
    highlight =  Event_Organizer_Highlight.objects.get(id=pk)

    if highlight.event_organizer == user.event_organizer:
        highlight.delete()
        highlights = Event_Organizer_Highlight.objects.filter(event_organizer=request.user.event_organizer)  
        data['valid'] = True
        data['html'] = render_to_string('event_organizer/highlights.html',{'highlights':highlights},request)
           
    else:
        data['valid'] = False

    return JsonResponse(data)

def event_performer_invitation(request,pk):
    top_peoples = User.objects.all()[:7]
    user = request.user
    if user.groups.filter(name='Musician').exists():
        performer_invitation = Event_Performer.objects.get(id=pk,musician=user.musician)  
    elif user.groups.filter(name='Troupe').exists():  
        performer_invitation = Event_Performer.objects.get(id=pk) 
    else:
        return HttpResponse("Error")

    if request.method == 'POST':
        status = request.POST.get('status')
        status = Event_Performer.objects.filter(id=pk).update(status=status)
        return redirect('event_performer_invitation',pk=pk)       
        
    else:
        pass        
    context ={
        'performer_invitation' : performer_invitation,   
        'top_peoples' : top_peoples,     

      }   

    return render(request,'musician/view_event_performer_invitation.html', context)

def search(request):
    name = request.GET.get('name')

    if name:
        musicians = Musician.objects.filter( Q(user__first_name__icontains = name) | Q(user__last_name__icontains = name)).exclude(user=request.user)   
        gurukulas = Gurukulam.objects.filter( Q(user__name__icontains = name) | Q(user__name__icontains = name)).exclude(user=request.user)
        event_organizers = Event_Organizer.objects.filter( Q(user__name__icontains = name) | Q(user__name__icontains = name)).exclude(user=request.user)
        troupes = Troupe.objects.filter( Q(user__name__icontains = name) | Q(user__name__icontains = name)).exclude(user=request.user)
    else:
        musicians = None
        gurukulas = None
        troupes = None
        event_organizers = None
        name = None

    context ={

        'musicians': musicians,
        'event_organizers' : event_organizers,
        'gurukulas'  : gurukulas,
        'troupes':   troupes,
        'name'   : name,
 
    }

    return render(request,'search.html', context)

def ajax_follow(request,pk):
    data = dict()    
    if not  UserFollowing.objects.filter(user=request.user,following_user_id=pk).exists():
        user_object = User.objects.get(id=pk)
        follow = UserFollowing.objects.create(user=request.user,following_user_id=user_object)
        data['valid'] = True
    else:
        data['valid'] = False

    return JsonResponse(data)

def ajax_unfollow(request,pk):
    data = dict()

    try:
        follow = UserFollowing.objects.get(following_user_id=pk,user=request.user) 
        follow.delete()
        data['valid'] = True  
        
    except:
        data['valid'] = False

    return JsonResponse(data)

def ajax_like(request,pk):
    data = dict()
    user = User.objects.get(username=request.user.username)  
    
    if not  Post.objects.filter(id=pk,user_likes__id=user.id).exists():        
        post = Post.objects.get(id=pk)
        post.likes +=1
        post.user_likes.add(user)
        post.save()
        data['valid'] = True
    else:
        data['valid'] = False

    return JsonResponse(data)

def ajax_unlike(request,pk):
    data = dict()
    user = User.objects.get(username=request.user.username)

    try:        
        post = Post.objects.get(id=pk,user_likes__id=user.id)
        post.likes -=1    
        post.user_likes.remove(user)
        post.save()
        data['valid'] = True
     
    except:
        data['valid'] = False       

    return JsonResponse(data)

def ajax_comment(request,pk):
    data= dict()
    if request.method == "POST":
        comment = request.POST.get('comment')
        post = Post.objects.get(id=pk)
        post_comment = Post_Comment.objects.create(user=request.user,post=post,comment=comment)
        data['valid'] =  True
        data['html'] = render_to_string('post/comments.html',{'post':post},request)
        data['comment_count'] = str(post.comment_count)

    else:
        data['valid'] =  False 

    return JsonResponse(data)

def ajax_reply(request,pk):
    data= dict()
    if request.method == "POST":
        reply = request.POST.get('reply')
        comment = Post_Comment.objects.get(id=pk)
        reply = Reply.objects.create(user=request.user,comment=comment,reply=reply)
        data['valid'] =  True
        data['html'] = data['html'] = render_to_string('post/reply.html',{'comment':comment},request)

    else:
        data['valid'] =  False 

    return JsonResponse(data)

def ajax_delete_comment(request,pk):
    data= dict()
    comment= Post_Comment.objects.get(id=pk)    

    if comment.user == request.user:
        post= comment.post.id
        comment.delete()
        post = Post.objects.get(id=post)
        data['valid'] =  True
        data['html']  = render_to_string('post/comments.html',{'post':post},request)
        data['comment_count'] = str(post.comment_count)
        data['post_id'] = post.id

    else:
        data['valid'] =  False 

    return JsonResponse(data)

def ajax_delete_reply(request,pk):
    data= dict()
    reply_object= Reply.objects.get(id=pk)    

    if reply_object.user == request.user:
        comment_id= reply_object.comment.id
        reply_object.delete()   
        comment = Post_Comment.objects.get(id=comment_id)
        data['valid'] =  True
        data['html'] = data['html'] = render_to_string('post/reply.html',{'comment':comment},request)
        data['comment_id'] = comment.id
    else:
        data['valid'] =  False 

    return JsonResponse(data)

def following(request):
    try:
        followings = UserFollowing.objects.filter(user=request.user)
        print("Followings Count:", followings.count())
        locations = Location.objects.all()
        skills = Skill.objects.all()
        skill_categories = Skill_Category.objects.all()
        followers=  request.user.followers_count
        context = {
            'followings' : followings,
            'followers':followers,
        }    
        return render(request,'account/following.html', context)
    except Exception as e:
        # Log the error or handle it
        return HttpResponse("An error occurred: " + str(e))

def followers(request):
    user_object = User.objects.get(id=request.user.id)
    followers = UserFollowing.objects.filter(following_user_id =user_object )
    following =  request.user.following_count
    locations = Location.objects.all()
    skills = Skill.objects.all()
    skill_categories = Skill_Category.objects.all()

    context = {
        'followers' : followers,
        'user_object' : user_object,
        'following':following,
        'skills':skills,      
        'locations':locations,
        'skill_categories':skill_categories,
    }    
    return render(request,'account/followers.html', context)

def user_following(request,pk):
    users= UserFollowing.objects.filter(user=pk)
    user_object = User.objects.get(id=pk)
    context = {
        'users' : users,
        'user_object' : user_object,
    }    
    return render(request,'account/view_user_following.html', context)

def user_followers(request,pk):
    user_object = User.objects.get(id=pk)
    users= UserFollowing.objects.filter(following_user_id =user_object )

    context = {
        'users' : users,
        'user_object' : user_object,
    }    
    return render(request,'account/view_user_followers.html', context)

def search_musician(request):
    if request.method == "POST":
        data = dict()
        name = request.GET.get('name')
        skill =   [ast.literal_eval(i) for i in request.POST.getlist('skill')]
        gender =  request.POST.getlist('gender')
        location = [ast.literal_eval(i) for i in request.POST.getlist('location')]
        if name:
            if skill:
                if gender:
                    if location:
                        musician_filter = Musician.objects.filter(Q(user__last_name__icontains=name) | Q(user__first_name__icontains=name),musician_skill__skill__id__in=skill,gender__in=gender,user__location__id__in=location).exclude(id=request.user.musician.id).distinct()
                    else:
                        musician_filter = Musician.objects.filter(Q(user__last_name__icontains=name) | Q(user__first_name__icontains=name),musician_skill__skill__id__in=skill,gender__in=gender).exclude(id=request.user.musician.id).distinct()
                elif location:
                    musician_filter = Musician.objects.filter(Q(user__last_name__icontains=name) | Q(user__first_name__icontains=name),musician_skill__skill__id__in=skill,user__location__id__in=location).exclude(id=request.user.musician.id).distinct()

                else:
                    musician_filter = Musician.objects.filter(Q(user__last_name__icontains=name) | Q(user__first_name__icontains=name),musician_skill__skill__id__in=skill).exclude(id=request.user.musician.id).distinct()
            elif gender:
                if location:
                    musician_filter = Musician.objects.filter(Q(user__last_name__icontains=name) | Q(user__first_name__icontains=name),gender__in=gender,user__location__id__in=location).exclude(user__id=request.user.id)
                else:
                    musician_filter = Musician.objects.filter(Q(user__last_name__icontains=name) | Q(user__first_name__icontains=name),gender__in=gender).exclude(user__id=request.user.id)

            elif location:
                musician_filter = Musician.objects.filter(Q(user__last_name__icontains=name) | Q(user__first_name__icontains=name),user__location__id__in=location).exclude(user__id=request.user.id)

            else:
                musician_filter = Musician.objects.filter(Q(user__last_name__icontains=name) | Q(user__first_name__icontains=name)).exclude(user__id=request.user.id)
                
        data['valid'] = True
        data['html'] = render_to_string('account/musician_list.html',{'musicians':musician_filter},request)
        
        return JsonResponse(data)

    else:
        name = request.GET.get('name')
        
        if name:
            musicians = Musician.objects.filter( Q(user__first_name__icontains = name) | Q(user__last_name__icontains = name)).exclude(user=request.user)   
        else:
            musicians = None

        locations = Location.objects.all()
        skills = Skill.objects.all()
        context ={
            'musicians': musicians, 
            'name'     : name,
            'locations':locations,
            'skills'  : skills,
        }
        return render(request,'account/search_musician.html', context)

def search_eventer(request):
    if request.method == "POST":
        data = dict()
        name = request.GET.get('name')
        location = [ast.literal_eval(i) for i in request.POST.getlist('location')]
        if name:       
            if location:
                event_organizers = Event_Organizer.objects.filter(user__name__icontains=name,user__location__id__in=location).exclude(user=request.user)
            else:
                event_organizers = Event_Organizer.objects.filter(user__name__icontains=name).exclude(user=request.user)
        
        data['valid'] = True
        data['html'] = render_to_string('account/event_organizer_list.html',{'event_organizers':event_organizers},request)
        
        return JsonResponse(data)

    else:
        name = request.GET.get('name')        
        if name:
            event_organizers = Event_Organizer.objects.filter(user__name__icontains=name).exclude(user=request.user)   
        else:
            event_organizers = None

        locations = Location.objects.all()
        context ={
            'event_organizers': event_organizers, 
            'name'     : name,
            'locations':locations,

        }
        return render(request,'account/search_event_organizer.html', context)

def search_gurukulam(request):
    if request.method == "POST":
        data = dict()
        name = request.GET.get('name')
        location = [ast.literal_eval(i) for i in request.POST.getlist('location')]
        skill = [ast.literal_eval(i) for i in request.POST.getlist('skill')]
        if name:       
            if location:
                if skill:
                    gurukulas = Gurukulam.objects.filter(user__name__icontains=name,user__location__id__in=location,gurukulam_skill__id__in=skill).exclude(user=request.user).distinct()
                else:
                    gurukulas = Gurukulam.objects.filter(user__name__icontains=name,user__location__id__in=location).exclude(user=request.user)
            elif skill:
                gurukulas = Gurukulam.objects.filter(user__name__icontains=name,gurukulam_skill__id__in=skill).exclude(user=request.user).distinct()
            else:
                gurukulas = Gurukulam.objects.filter(user__name__icontains=name).exclude(user=request.user)
        else:
            gurukulas = None
        data['valid'] = True
        data['html'] = render_to_string('account/gurukulam_list.html',{'gurukulas':gurukulas},request)
        
        return JsonResponse(data)

    else:
        name = request.GET.get('name')        
        if name:
            event_organizers = Event_Organizer.objects.filter(user__name__icontains=name).exclude(user=request.user)   
        else:
            event_organizers = None

        locations = Location.objects.all()
        skills = Skill.objects.all()
        context ={
            'event_organizers': event_organizers, 
            'name'     : name,
            'locations':locations,
            'skills' : skills ,
        }
        return render(request,'account/search_gurukulam.html', context)

def search_troupe(request):
    if request.method == "POST":
        data = dict()
        name = request.GET.get('name')
        location = [ast.literal_eval(i) for i in request.POST.getlist('location')]
        skill = [ast.literal_eval(i) for i in request.POST.getlist('skill')]
      
        if name:       
            if location:
                if skill:
                    troupes = Troupe.objects.filter(user__name__icontains=name,user__location__id__in=location,troupe_skill__id__in=skill).exclude(user=request.user).distinct()
                else:
                    troupes = Troupe.objects.filter(user__name__icontains=name,user__location__id__in=location).exclude(user=request.user)
            elif skill:
                troupes =Troupe.objects.filter(user__name__icontains=name,troupe_skill__id__in=skill).exclude(user=request.user).distinct()
            else:
                troupes =Troupe.objects.filter(user__name__icontains=name).exclude(user=request.user)
        else:
            troupes = None

        data['valid'] = True
        data['html'] = render_to_string('account/troupe_list.html',{'troupes':troupes},request)
        
        return JsonResponse(data)

    else:
        name = request.GET.get('name')        
        if name:
            troupes = Troupe.objects.filter(user__name__icontains=name).exclude(user=request.user)   
        else:
            troupes = None

        locations = Location.objects.all()
        skills = Skill.objects.all()
        context ={
            'troupes': troupes, 
            'name'     : name,
            'locations':locations,
            'skills': skills,

        }
        return render(request,'account/search_troupe.html', context)

def event_finder(request,pk):

    if request.method == "POST":

        data=dict()

        skill =[ast.literal_eval(i) for i in request.POST.getlist('skill')] 
        locations =[ast.literal_eval(i) for i in request.POST.getlist('location')] 
        event_types =[ast.literal_eval(i) for i in request.POST.getlist('event_type')]  
        event_categories =[ast.literal_eval(i) for i in request.POST.getlist('event_category')]
        name =  request.POST.get('name')
        from_date =  request.POST.get('after_date')
        to_date =  request.POST.get('to_date')
    
        event_filter = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False)
             
        if skill:
            event_filter = event_filter.filter(event_skill__skill__id__in=skill).distinct()

        if locations:
            event_filter = event_filter.filter(location__id__in=locations)
        if event_types:
            event_filter = event_filter.filter(event_type__id__in=event_types)

        if event_categories:
            event_filter = event_filter.filter(event_category__id__in=event_categories)

        if name:
            event_filter = event_filter.filter(name__icontains=name)

        if from_date:
            event_filter = event_filter.filter(event_date__gte=from_date)
        if to_date:
            event_filter = event_filter.filter(event_date__lte=to_date)

        data['valid'] = True
        data['html'] = render_to_string('event/event_list.html',{'events':event_filter},request)
        return JsonResponse(data)
    else:
        events = Event.objects.filter(location_id=pk,to_date__gte=datetime.now(),self_reference=False)
        event_types = Event_Type.objects.all()
        event_categories = Event_Category.objects.all()
        skill_categories = Skill_Category.objects.all()
        skills = Skill.objects.all()

        context ={
            'events': events, 
            'event_types':event_types, 
            'event_categories':event_categories,   
            'skill_categories':skill_categories,
            'skills':skills, 
            'pk'  :pk, 
        }
        return render(request,'event_finder.html', context)

#Default location Set
def set_location(request):
    data = dict()
    location = request.GET.get('location', None)
    place = request.GET.get('place', None)
    data['place'] = place

    try:
        location_instance = Location.objects.get(name=location.lstrip())
        user = User.objects.filter(id=request.user.id).update(location=location_instance)
        data['valid'] = True

        if place:       
            if request.user.groups.filter(name='Musician').exists():
                user_type ="'Musician"
                sent_requests = Interest.objects.filter(musician=request.user.musician).values_list('event__id', flat=True)
                received_requests = Invitation.objects.filter(musician=request.user.musician).values_list('event__id', flat=True)
                musician_skills = Musician_Skill.objects.filter(musician=request.user.musician).values_list('skill__id', flat=True)
                
                if not sent_requests and  not received_requests:                
                    events = Event.objects.filter(location=location_instance,registration_close_date__gte=datetime.now(),event_skill__skill__id__in=musician_skills,self_reference=False).distinct()[:50]
                elif  sent_requests and  not received_requests:                    
                    events = Event.objects.filter(location=location_instance,registration_close_date__gte=datetime.now(),event_skill__skill__id__in=musician_skills,self_reference=False).distinct().exclude(id__in=sent_requests)[:50]
                elif not sent_requests and  received_requests:                    
                    events = Event.objects.filter(location=location_instance,registration_close_date__gte=datetime.now(),event_skill__skill__id__in=musician_skills,self_reference=False).distinct().exclude(id__in=received_requests)[:50]
                else:                    
                    event_exclude_ids_list = chain(sent_requests, received_requests)                    
                    events = Event.objects.filter(location=location_instance,registration_close_date__gte=datetime.now(),event_skill__skill__id__in=musician_skills,self_reference=False).distinct().exclude(id__in=event_exclude_ids_list)[:50]
            elif request.user.groups.filter(name='Event Organizer').exists():
                user_type ="event_organizer"            
                events = Event.objects.filter(location=location_instance,registration_close_date__gte=datetime.now())
            elif request.user.groups.filter(name='Band').exists():
                sent_requests = Interest.objects.filter(troupe=request.user.troupe).values_list('event__id', flat=True)
                received_requests = Invitation.objects.filter(troupe=request.user.troupe).values_list('event__id', flat=True)
                troupe_skills = Troupe_Skill.objects.filter(troupe=request.user.troupe).values_list('skill__id', flat=True)
                
                if not sent_requests and  not received_requests:                
                    events = Event.objects.filter(location__location_name=location_instance,registration_close_date__gte=datetime.now(),event_skill__skill__id__in=troupe_skills,self_reference=False).distinct()[:50]
                elif  sent_requests and  not received_requests:                    
                    events = Event.objects.filter(location=location_instance,registration_close_date__gte=datetime.now(),event_skill__skill__id__in=troupe_skills,self_reference=False).distinct().exclude(id__in=sent_requests)[:50]
                elif not sent_requests and  received_requests:                    
                    events = Event.objects.filter(location=location_instance,registration_close_date__gte=datetime.now(),event_skill__skill__id__in=troupe_skills,self_reference=False).distinct().exclude(id__in=received_requests)[:50]
                else:                    
                    event_exclude_ids_list = chain(sent_requests, received_requests)                    
                    events = Event.objects.filter(location=location_instance,registration_close_date__gte=datetime.now(),event_skill__skill__id__in=troupe_skills,self_reference=False).distinct().exclude(id__in=event_exclude_ids_list)[:50]
                user_type ="troupe"
            elif request.user.groups.filter(name='Music School').exists():
                events = Event.objects.filter(location=location_instance,registration_close_date__gte=datetime.now())
                user_type ="gurukulam"
            
            gurukulas = Gurukulam.objects.filter(user__location=location_instance).order_by('?')[:5]
            
            event_organizers =  Event_Organizer.objects.filter(user__location=location_instance).annotate(num_events=Count('event')).order_by('-num_events').exclude(user=request.user)[:5]
            instrumentalists = Musician.objects.filter(Q(invitation__status="A") | Q(interest__status="A"),user__location=location_instance,user__location__isnull=False,musician_skill__skill__skill_category__category_name="Instrument").distinct().exclude(user=request.user)[:5]
            users = User.objects.filter(groups__name__in=('Musician','Event Organizer','Music School','Band'),location=location_instance).exclude(id=request.user.id).distinct()[:5]
            data['top_features'] = render_to_string('account/top_features.html',{'users':users,'user':request.user},request)
            data['events'] = render_to_string('event/event_list.html',{'events':events,'user_type':user_type,'user':request.user,})
    except:
        data['valid'] = False
        data['response'] = "Kindly contact Adminstrator.."

    return JsonResponse(data)

def search_top_peoples(request):
    data = dict()
    user=request.user
    name = request.GET.get('name', None)

    type=request.GET.get('type', None)
    if type == "reset":
        gurukulas = Gurukulam.objects.filter(user__location=user.location).exclude(user=user).order_by('?')[:5]
        event_organizers = Event_Organizer.objects.filter(user__location=user.location).annotate(num_events=Count('event')).order_by('-num_events').exclude(user=user)[:5]
        instrumentalists = Musician.objects.filter(Q(invitation__status="A") | Q(interest__status="A"),user__location=user.location,user__city__isnull=False,musician_skill__skill__skill_category__category_name="Instrument").distinct().exclude(user=user).annotate(total_counts=Count('invitation')+Count('interest')).order_by('-total_counts')[:5]
        vocalists = Musician.objects.filter(Q(invitation__status="A") | Q(interest__status="A"),user__location=user.location,user__city__isnull=False,musician_skill__skill__skill_category__category_name="Vocal").distinct().exclude(user=user).annotate(total_counts=Count('invitation')+Count('interest')).order_by('-total_counts')[:5] 
        data['top_features'] = render_to_string('account/top_features-1.html',{'event_organizers':event_organizers,'gurukulas':gurukulas,'instrumentalists':instrumentalists,'vocalists':vocalists,},request)
    else:        
        gurukulas = Gurukulam.objects.filter(user__name__icontains=name,user__location=user.location,user__city__isnull=False).order_by('?').exclude(user=request.user)[:5]      
        event_organizers =  Event_Organizer.objects.filter(user__name__icontains=name,user__location=user.location,user__city__isnull=False).exclude(user=request.user).annotate(num_events=Count('event')).order_by('-num_events')[:5]
        instrumentalists = Musician.objects.filter(Q(user__last_name__icontains=name) | Q(user__first_name__icontains=name),user__location=user.location,user__city__isnull=False,musician_skill__skill__skill_category__category_name="Instrument").distinct().exclude(user=request.user)[:5]
        vocalists = Musician.objects.filter(Q(user__last_name__icontains=name) | Q(user__first_name__icontains=name),user__location=user.location,user__city__isnull=False,musician_skill__skill__skill_category__category_name="Vocal").distinct().exclude(user=request.user)[:5]
        data['top_features'] = render_to_string('account/top_features.html',{'event_organizers':event_organizers,'gurukulas':gurukulas,'instrumentalists':instrumentalists,'vocalists':vocalists,},request)
    
    data['valid'] = True
    return JsonResponse(data)

def post_likes(request,pk):
    data = dict()
    try:
        users= Post.objects.filter(id=pk).values_list('user_likes', flat=True)
        users = User.objects.filter(id__in=users)
        data['post_likes']  = render_to_string('account/post-liked-list.html',{'users':users},request)
        data['valid'] = True
    except:
        data['valid'] = False

    return JsonResponse(data)

#Load more post
def load_more_post(request):
    data= dict()
    if request.method == "POST":
        count = int(request.POST['count'])
        limit = 10
        following_users =UserFollowing.objects.filter(user=request.user).values_list('following_user_id', flat=True)
        posts = Post.objects.all()[count:limit+count]
        total_count = Post.objects.all().count()
        data['posts']  = render_to_string('account/load-more-post.html',{'posts':posts},request)        
        data['total_count'] = total_count
        data['valid'] = True

    else:
        data['valid'] = False
    return JsonResponse(data)

#post filter
def post_filter(request):
    data = dict()
    user= request.user
    if request.method == "POST":
        post_filter_type =request.POST.get('post_filter_type')         
        if post_filter_type == "is_i_follow":            
            followings = list(UserFollowing.objects.filter(user=user).values_list('following_user_id__id', flat=True))
            posts =  Post.objects.filter(user__id__in=followings).distinct()   
        elif post_filter_type == "is_recent_all":
            posts =  Post.objects.all().order_by('-id')[:5]
    
        data['html'] = render_to_string('posts.html',{'posts':posts},request)
        data['valid'] = True
    
    return JsonResponse(data)

def ajax_follow_unfollow(request,pk):
    data =  dict()    
    following_user_id = User.objects.get(id=pk)
    status = UserFollowing.follow_or_unfollow(user=request.user,following_user_id=following_user_id)
    data['followed'] = status
    return JsonResponse(data)

def search_people(request):
    data = dict()
    user=request.user
    skill_category = request.POST.getlist('skill_category')
    page = request.GET.get('page', None)
    people_type = request.GET.get('people_type', None)

    if page == "people":
        if people_type == "eventer":
            users = User.objects.filter(Q(last_name__icontains=name) | Q(first_name__icontains=name) | Q(name__icontains=name),groups__name="Event Organizer").exclude(id=request.user.id).distinct()[:50]
        elif people_type == "musician":
            users = User.objects.filter(Q(last_name__icontains=name) | Q(first_name__icontains=name),groups__name="Artist").exclude(id=request.user.id).distinct()[:50]
        elif people_type == "troupe":
            users = User.objects.filter(Q(last_name__icontains=name) | Q(first_name__icontains=name) | Q(name__icontains=name),groups__name="Troupe").exclude(id=request.user.id).distinct()[:50]
        elif people_type == "gurukulam":
            users = User.objects.filter(Q(last_name__icontains=name) | Q(first_name__icontains=name) | Q(name__icontains=name),groups__name="Gurukulam").exclude(id=request.user.id).distinct()[:50]
        elif people_type == "teacher":
            users = User.objects.filter(Q(last_name__icontains=name) | Q(first_name__icontains=name) | Q(name__icontains=name),musician__musician_skill__teach=True).exclude(id=request.user.id).distinct()[:50]
        else:
            users = User.objects.filter(Q(last_name__icontains=name) | Q(first_name__icontains=name) | Q(name__icontains=name)).exclude(id=request.user.id).distinct()[:55]
    else:      
        if people_type == "eventer":
            users = User.objects.filter(Q(last_name__icontains=name) | Q(first_name__icontains=name) | Q(name__icontains=name),groups__name="Event Organizer").exclude(id=request.user.id).distinct()[:10]
        elif people_type == "musician":
            users = User.objects.filter(Q(last_name__icontains=name) | Q(first_name__icontains=name),groups__name="Artist").exclude(id=request.user.id).distinct()[:10]
        elif people_type == "troupe":
            users = User.objects.filter(Q(last_name__icontains=name) | Q(first_name__icontains=name) | Q(name__icontains=name),groups__name="Troupe").exclude(id=request.user.id).distinct()[:10]
        elif people_type == "gurukulam":
            users = User.objects.filter(Q(last_name__icontains=name) | Q(first_name__icontains=name) | Q(name__icontains=name),groups__name="Gurukulam").exclude(id=request.user.id).distinct()[:10]
        elif people_type == "teacher":
            users = User.objects.filter(Q(last_name__icontains=name) | Q(first_name__icontains=name) | Q(name__icontains=name),musician__musician_skill__teach=True).exclude(id=request.user.id).distinct()[:50]              
        else:
            users = User.objects.filter(Q(last_name__icontains=name) | Q(first_name__icontains=name) | Q(name__icontains=name)).exclude(id=request.user.id).distinct()[:5]
                
    data['users'] = render_to_string('account/search_people.html',{'users':users,'page':page,'people_type':people_type},request)    
    data['valid'] = True
    return JsonResponse(data)


def ajax_like_unlike(request,pk):
    data =  dict()    
    liked = Post.like_or_unlike(id=pk,user=request.user)
    post = Post.objects.get(id=pk)
    likes_count = post.user_likes.count()
    if post:
        data['liked'] = liked
        data['like_count'] = likes_count
    else:
        data['like_count'] = likes_count
        data['liked'] = liked

    return JsonResponse(data)


def home_event_filter(request):
    data = dict()
    user=request.user
    event_filter = request.GET.get('event_filter', None)

    for group in user.groups.all():
        if group.name  == "Artist":
            sent_requests = Interest.objects.filter(musician=request.user.musician).values_list('event__id', flat=True)
            received_requests = Invitation.objects.filter(musician=request.user.musician).values_list('event__id', flat=True)
            user_type = "musician"
            musician_skills = Musician_Skill.objects.filter(musician=request.user.musician).values_list('skill__id', flat=True)
            
        elif group.name  == "Troupe":
            sent_requests = Interest.objects.filter(troupe=request.user.troupe).values_list('event__id', flat=True)
            received_requests = Invitation.objects.filter(troupe=request.user.troupe).values_list('event__id', flat=True)
            user_type = "troupe"

        elif group.name  == "Event Organizer":
            sent_requests = None
            received_requests = None
            user_type = "event_organizer"

        elif group.name  == "Gurukulam":
            sent_requests = None
            received_requests = None
            user_type = "gurukulam"
            
        elif group.name == "Admin":
            is_admin = True

    if event_filter == "recent":
        if not sent_requests and  not received_requests:
            events = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False)[:30]
        elif  sent_requests and  not received_requests:
            events = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False).exclude(id__in=sent_requests)[:30]
        elif not sent_requests and  received_requests:
            events = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False).exclude(id__in=received_requests)[:30]
        else:
            event_exclude_ids_list = chain(sent_requests, received_requests)
            events = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False).exclude(id__in=event_exclude_ids_list)[:30]
    elif event_filter == "interest":

        if user_type == "musician":
            interests = list(Musician_Skill.objects.filter(musician=request.user.musician).values_list('skill',flat=True))

        if not sent_requests and  not received_requests:
            event_filter= Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False,event_skill__skill__in=interests)[:30]
        elif  sent_requests and  not received_requests:
            event_filter = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False,event_skill__skill__in=interests).exclude(id__in=sent_requests)[:30]
        elif not sent_requests and  received_requests:
            event_filter = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False,event_skill__skill__in=interests).exclude(id__in=received_requests)[:30]
    
        else:
            event_exclude_ids_list = chain(sent_requests, received_requests)
            events = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False,event_skill__skill__in=interests).exclude(id__in=event_exclude_ids_list)[:30]
     
    elif event_filter == "i_follow":
        following = UserFollowing.objects.filter(user=request.user,following_user_id__groups__name__in=('Event Organizer','Gurukulam')).values_list('following_user_id__id',flat=True)
        if not sent_requests and  not received_requests:
            events = Event.objects.filter(Q(gurukulam__user__id__in=following) | Q(event_organizer__user__id__in=following),registration_close_date__gte=datetime.now(),self_reference=False)[:30]
        elif  sent_requests and  not received_requests:
            events = Event.objects.filter(Q(gurukulam__user__id__in=following) | Q(event_organizer__user__id__in=following),registration_close_date__gte=datetime.now(),self_reference=False).exclude(id__in=sent_requests)[:30]
        elif not sent_requests and  received_requests:
            events = Event.objects.filter(Q(gurukulam__user__id__in=following) | Q(event_organizer__user__id__in=following),registration_close_date__gte=datetime.now(),self_reference=False).exclude(id__in=received_requests)[:30]
        else:
            event_exclude_ids_list = chain(sent_requests, received_requests)
            events = Event.objects.filter(Q(gurukulam__user__id__in=following) | Q(event_organizer__user__id__in=following),registration_close_date__gte=datetime.now(),self_reference=False).exclude(id__in=event_exclude_ids_list)[:30]
    elif event_filter == "clear":
        events = None
    data['events'] = render_to_string('event/events.html',{'events':events,},request)    
    data['valid'] = True
    return JsonResponse(data)


@login_required(login_url='signin')
def all_peoples(request):
    locations = Location.objects.all()
    skills = Skill.objects.all()
    skill_categories = Skill_Category.objects.all()
    users= User.objects.filter(is_active=True).exclude(Q(id=request.user.id) | Q(is_superuser=True))

    name = request.GET.get('name', None)
    people_type = request.GET.get('people_type', None)

    if name:
        users = User.objects.filter(Q(last_name__icontains=name) | Q(first_name__icontains=name) | Q(name__icontains=name), groups__name__in=('Musician','Band','Music School','Event Organizer')).exclude(id=request.user.id).distinct()
    else:
        users = User.objects.filter(groups__name__in=('Musician','Band','Music School','Event Organizer')).exclude(id=request.user.id).distinct()
    

    followers = request.user.followers_count
    following =  request.user.following_count

    user_groups = Group.objects.all()

    context = {
        'users' : users,
        'name' : name,
        'skills':skills,
        'people_type' : people_type,
        'locations':locations,
        'skill_categories':skill_categories,
        'followers': followers,
        'following' : following,
        'user_groups':user_groups,

    }    
    return render(request,'account/all_peoples.html', context)

@login_required(login_url='signin')
def my_profile(request):
    user_groups = request.user.groups.all()  
    followers = UserFollowing.objects.filter(following_user_id=request.user).order_by('-id')[:8]
    user = request.user
    for group in user_groups:
        if group.name == "Artist":
            troupes = Key_Performer.objects.filter(musician=request.user.musician)
            event_performer_requests = Event_Performer.objects.filter(musician=request.user.musician)    
            gurukulam_teachers = Gurukulam_Teacher.objects.filter(sender=request.user)  
            musician_skills = Musician_Skill.objects.filter(musician=request.user.musician).values_list('skill__id', flat=True)  
            followers_friends = list(UserFollowing.objects.filter(following_user_id=request.user.id).values_list('user__id',flat=True).order_by('?')[:3])

            eventer  = Event_Skill.objects.filter(skill__id__in=musician_skills,event__event_organizer__isnull=False).values_list('event__event_organizer__user__id', flat=True).order_by('?')[:2]
            
            recommended_people = list(followers_friends) + list(eventer)
            recommended_people = [*set(recommended_people)]
            

            top_peoples = User.objects.filter(id__in=recommended_people).exclude(id=request.user.id)[:5]    
            context = {
                'followers' : followers,
                'top_peoples' : top_peoples,
                'troupes' : troupes,
                'event_performer_requests':event_performer_requests,
                'gurukulam_teachers':gurukulam_teachers,
            }
            return render(request,'account/my_profile.html', context)
        
        elif group.name == "Music Lover":

            top_peoples = User.objects.filter(location=user.location,groups__name__in=('Musician','Event Organizer','Gurukulam','Troupe')).exclude(id=request.user.id).order_by('-id')[:5]

            context = { 
                'followers' : followers,
                'top_peoples' : top_peoples,
        
            }
            return render(request,'account/my_profile.html', context)


        elif group.name == "Event Organizer":
            performers = Event_Performer.objects.filter(event_organizer=request.user.event_organizer)
            top_peoples = User.objects.filter(location=user.location,groups__name__in=('Musician','Event Organizer','Gurukulam','Troupe')).exclude(id=request.user.id).order_by('-id')[:5]
            context = { 
                'followers' : followers,
                'top_peoples' : top_peoples,
                'performers': performers,        
            }
            return render(request,'account/my_profile.html', context)

        elif group.name == "Band":
            key_performers = Key_Performer.objects.filter(troupe=request.user.troupe) 
            troupe_skills = Troupe_Skill.objects.filter(troupe=request.user.troupe)  
            top_peoples = User.objects.filter(location=user.location,groups__name__in=('Musician','Event Organizer','Gurukulam','Troupe')).exclude(id=request.user.id)[:5]         
            context = { 
                'followers' : followers,
                'top_peoples' : top_peoples,
                'key_performers': key_performers,  
                'troupe_skills' : troupe_skills,                      
            }
            return render(request,'account/my_profile.html', context)


        elif group.name == "Music School":
            lecture_videos = Lecture_Video.objects.filter(gurukulam=request.user.gurukulam)    
            courses = Course.objects.filter(gurukulam=request.user.gurukulam)  
            testimonials = Gurukulam_Testimonial.objects.filter(gurukulam=request.user.gurukulam)
            top_peoples = User.objects.filter(location=user.location,groups__name__in=('Musician','Event Organizer','Gurukulam','Troupe')).exclude(id=request.user.id)[:5]
            
            context = { 
                'followers' : followers,
                'top_peoples' : top_peoples,
                'lecture_videos':lecture_videos,
                'courses':courses,
                'testimonials':testimonials,                                        
            }
            return render(request,'account/my_profile.html', context)





from  .decode_base64_file import decode_base64_file

def ajax_add(request,model_name):
    data =  dict()
    if model_name == 'musician_gurukulam':
        if request.method == "POST":
            form = Musician_Gurukulam_Form(request.POST,request=request,)

            if form.is_valid():
                form = form.save(commit=False)
                form.musician = request.user.musician
                form.sender = request.user
                form.status = 'S'
                form.save()
                data['valid'] = True
                data['model_name'] = model_name
                data['html'] = render_to_string('account/musician_gurukulam.html',{},request)
            else:
                data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Gurukulam'},request)
                data['valid'] = False

        else:
            form = Musician_Gurukulam_Form(request=request)

            data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Gurukulam'},request)
            data['valid'] = True
    
    elif model_name == "musician_skill":

        if request.method == "POST":
            form = Musician_Skill_Form(request.POST,request=request,)

            if form.is_valid():
                form = form.save(commit=False)
                form.musician = request.user.musician
                form.save()
                data['valid'] = True
                data['model_name'] = model_name
                data['html'] = render_to_string('musician/musician_skill.html',{},request)
            else:
                data['form'] = render_to_string('account/musician_skill_form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Musician Skill'},request)
                data['valid'] = False

        else:
            form = Musician_Skill_Form(request=request)

            data['form'] = render_to_string('account/musician_skill_form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Musician Skill'},request)
            data['valid'] = True

    elif model_name == 'musician_award':
        if request.method == "POST":
            form = Musician_Award_Form(request.POST,request.FILES,request=request,)

            if form.is_valid():
                form = form.save(commit=False)
                form.musician = request.user.musician
                form.save()
                data['valid'] = True
                data['model_name'] = model_name
                data['html'] = render_to_string('musician/musician_award.html',{},request)
            else:
                data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Musician Award'},request)
                data['valid'] = False

        else:
            form = Musician_Award_Form(request=request)

            data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Musician Award'},request)
            data['valid'] = True


    elif model_name == 'highlight':
        if request.method == "POST":
            form = Highlight_Form(request.POST,request=request,)

            if form.is_valid():
                highlight = form.save(commit=False)
                highlight.user = request.user
                highlight.save()
                form.save_m2m()
                #create post 
                post =Post.objects.create(highlight=highlight,user=request.user,content= highlight.description + '<br>Video Link: <a href='+str(highlight.video_link)+'">Watch Video </a>')  

                data['valid'] = True
                data['model_name'] = model_name
                data['html'] = render_to_string('account/highlight.html',{},request)
            else:
                data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Highlight'},request)
                data['valid'] = False

        else:
            form = Highlight_Form(request=request)

            data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Highligh'},request)
            data['valid'] = True

    elif model_name == 'event_performer':
        if request.method == "POST":
            form = Event_Performer_Form(request.POST,request=request,)

            if form.is_valid():
                performer = form.save(commit=False)
                performer.event_organizer = request.user.event_organizer
                performer.status = "A"
                performer.save()                
                data['valid'] = True
                data['model_name'] = model_name
                performers = Event_Performer.objects.filter(event_organizer=request.user.event_organizer)
                data['html'] = render_to_string('account/event_performer.html',{'performers':performers,},request)
            else:
                data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Highlight'},request)
                data['valid'] = False

        else:
            form = Event_Performer_Form(request=request)
            data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Performer'},request)
            data['valid'] = True


    elif model_name == 'event_home':
        if request.method == "POST":
            cropped_image = request.POST.get('cropped_image')
            form = Event_Form(request.POST,request.FILES)

            musicians = ast.literal_eval(request.POST.get('musicians[]'))
            troupes = ast.literal_eval(request.POST.get('troupes[]'))
            gurukulas = ast.literal_eval(request.POST.get('gurukulas[]'))
            message = request.POST.get('message')
           
            auto_accept = request.POST.get('auto_accept')
       
            if auto_accept is None:
                status = "S"
            else:
                status = "A"

            skill_id = request.POST.getlist("skill") 


            if form.is_valid():
                event = form.save(commit=False)
                if request.user.groups.filter(name='Event Organizer').exists():
                    event.event_organizer = request.user.event_organizer
                else:
                    event.gurukulam = request.user.gurukulam
                #event.save() 
                auto_accept = request.POST.get('auto_accept')

                
                '''
               
                
                x = float(request.POST.get('x'))
                y = float(request.POST.get('y'))
                w = float(request.POST.get('width'))
                h = float(request.POST.get('height'))
                files = request.FILES
                image_file = files.get('poster_image', None)
                image = Image.open(image_file)              
                cropped_image = image.crop((x, y, w+x, h+y))
                resized_image = cropped_image.resize((1024, 576), Image.ANTIALIAS)                         
                resized_image.save(event.poster_image.path)

                '''
                if cropped_image:
                    event.poster_image = decode_base64_file(cropped_image)                
                    event.save()
                else:
                    event.save()
              

                skill_id = request.POST.getlist("skill") 
                for skill in skill_id:
                    skill = Skill.objects.get(id=skill)
                    event_skill = Event_Skill.objects.create(event=event,skill=skill)


                for musician in  musicians:
                    invitation = Invitation.objects.create(event=event,status=status,musician=Musician.objects.get(id=musician))
                    message_obj = Message(user=request.user, invitation=invitation, text=message)
                    message_obj.save()
                    

                for gurukulam in  gurukulas:
                    invitation = Invitation.objects.create(event=event,status=status,gurukulam=Gurukulam.objects.get(id=gurukulam))
                    message_obj = Message(user=request.user, invitation=invitation, text=message)
                    message_obj.save()

                for troupe in  troupes:
                    invitation = Invitation.objects.create(event=event,status=status,troupe=Troupe.objects.get(id=troupe))
                    message_obj = Message(user=request.user, invitation=invitation, text=message)
                    message_obj.save()

                             
                data['valid'] = True
            else:
                print(form.errors)
                data['valid'] = False
    elif model_name == "key_performer":
        if request.method == 'POST':
            form = Key_Performer_Form(request.POST,request.FILES)
            if form.is_valid():
                performer = form.save(commit=False)
                performer.troupe = request.user.troupe  
                performer.save()   

                #email                
                link= str(request.META['HTTP_HOST'])+'/troupe_invitation/'+str(performer.id)    
                mail_to = performer.musician.user.email      
                subject = 'Troupe Invitation - Reg'
                message ='You have been invited to troupe'+str(request.user)+'; please accept or decline by clicking here. Link: {}'.format(link)     
                #send_email(subject,mail_to,message)                

                key_performers = Key_Performer.objects.filter(troupe=request.user.troupe)
                data['valid'] = True
                data['model_name'] = model_name
                data['html'] = render_to_string('troupe/key_performers.html',{'key_performers':key_performers},request)
                
            else:
                data['valid'] = False
                data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Performer'},request)
            
        else:
            form = Key_Performer_Form()
            data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Key Performer'},request)
    
    elif model_name == "gurukulam_skill":
        if request.method == 'POST':
            form = Gurukulam_Skill_Form(request.POST)
            if form.is_valid():
                skill = form.save(commit=False)
                skill.gurukulam = request.user.gurukulam        
                skill.save()   
                gurukulam_skills = Gurukulam_Skill.objects.filter(gurukulam=request.user.gurukulam)
                data['valid'] = True
                data['html'] = render_to_string('gurukulam/skill.html',{},request)
                data['model_name'] = model_name
            
            else:
                data['valid'] = False
                data['form'] = render_to_string('account/form.html',{'form':form,'operation':'Add','model':'Skill','model_name':model_name,},request)
            
        else:
            form = Gurukulam_Skill_Form()
            data['form'] = render_to_string('account/form.html',{'form':form,'operation':'Add','model':'Skill','model_name':model_name,},request)

    elif model_name == "gurukulam_award":
        if request.method == 'POST':
            form = Gurukulam_Award_Form(request.POST,request.FILES)
            if form.is_valid():
                award = form.save(commit=False)
                award.gurukulam = request.user.gurukulam        
                award.save()   
               
                data['valid'] = True
                data['html'] = render_to_string('gurukulam/award.html',{},request)
                data['model_name'] = model_name
            
            else:
                data['valid'] = False
                data['form'] = render_to_string('account/form.html',{'form':form,'operation':'Add','model':'Skill','model_name':model_name,},request)
            
        else:
            form = Gurukulam_Award_Form()
            data['form'] = render_to_string('account/form.html',{'form':form,'operation':'Add','model':'Award','model_name':model_name,},request)

    elif model_name == "troupe_skill":

        if request.method == "POST":
            form = Troupe_Skill_Form(request.POST,request=request,)

            if form.is_valid():
                form = form.save(commit=False)
                form.troupe = request.user.troupe
                form.save()
                data['valid'] = True
                data['model_name'] = model_name
                troupe_skills = Troupe_Skill.objects.filter(troupe=request.user.troupe)
                data['html'] = render_to_string('troupe/troupe_skill.html',{'troupe_skills':troupe_skills,},request)
            else:
                data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Troupe Skill'},request)
                data['valid'] = False

        else:
            form = Troupe_Skill_Form(request=request)
            data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Troupe Skill'},request)
            data['valid'] = True
    elif model_name == "lecture_video":
        if request.method == 'POST':
            form = Lecture_Video_Form(request.POST,request=request)
            if form.is_valid():
                lecture_video = form.save(commit=False)
                lecture_video.gurukulam = request.user.gurukulam     
                lecture_video.save()   

                lecture_videos = Lecture_Video.objects.filter(gurukulam=request.user.gurukulam)
                data['valid'] = True
                data['model_name'] = model_name
                data['html'] = render_to_string('gurukulam/lecture_videos.html',{'lecture_videos':lecture_videos},request)
                
            else:
                
                data['valid'] = False
                data['form'] = render_to_string('gurukulam/lecture_video_form.html',{'form':form,'operation':'Add',},request)
            
        else:
            form = Lecture_Video_Form(request=request)
            data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Lecture Video'},request)

    elif model_name == "course":
       
        if request.method == 'POST':
            form = Course_Form(request.POST)
            if form.is_valid():
                course = form.save(commit=False)
                course.gurukulam = request.user.gurukulam     
                course.save() 
                data['model_name'] = model_name   

                courses = Course.objects.filter(gurukulam=request.user.gurukulam)
                data['valid'] = True
                data['html'] = render_to_string('gurukulam/courses.html',{'courses':courses},request)
                
            else:
                data['valid'] = False
                data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Course',},request)
                
        else:
            form = Course_Form()
            data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Course',},request)

    elif model_name == "testimonial":
        if request.method == 'POST':
            form = Gurukulam_Testimonial_Form(request.POST)
            if form.is_valid():
                testimonial = form.save(commit=False)
                testimonial.gurukulam = request.user.gurukulam
                data['model_name'] = model_name 
                testimonial.save()   
                gurukulam_testimonials = Gurukulam_Testimonial.objects.filter(gurukulam=request.user.gurukulam)
                data['valid'] = True
                data['html'] = render_to_string('gurukulam/testimonials.html',{'testimonials':gurukulam_testimonials},request)
                
            else:
                data['valid'] = False
                data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Testimonial',},request)
            
        else:
            form = Gurukulam_Testimonial_Form()
            data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Testimonial',},request)

    elif model_name == 'add_musician':
        if request.method == "POST":
            form = Add_Musician_Form(request.POST,request=request,)

            if form.is_valid():
                form = form.save(commit=False)
                form.gurukulam = request.user.gurukulam
                form.sender = request.user
                form.status = 'S'
                form.save()
                data['valid'] = True
                data['model_name'] = model_name
                data['html'] = render_to_string('account/musician_gurukulam.html',{},request)
            else:
                data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Musician'},request)
                data['valid'] = False

        else:
            form = Add_Musician_Form(request=request)

            data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Musician'},request)
            data['valid'] = True
    
    elif model_name == 'add_teacher':
        if request.method == "POST":
            form = Add_Gurukulam_Teacher_Form(request.POST,request=request,)

            if form.is_valid():
                form = form.save(commit=False)
                form.gurukulam = request.user.gurukulam
                form.sender = request.user
                form.status = 'S'
                form.save()
                data['valid'] = True
               
            else:
                data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Gurukulam Teacher'},request)
                data['valid'] = False

        else:
            form = Add_Gurukulam_Teacher_Form(request=request)

            data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Gurukulam Teacher'},request)
            data['valid'] = True

    elif model_name == 'teacher_send_request_to_gurukulam':
        if request.method == "POST":
            form = Add_Teacher_Gurukulam_Form(request.POST,request=request)

            if form.is_valid():
                form = form.save(commit=False)
                form.musician = request.user.musician
                form.sender = request.user
                form.status = 'S'
                form.save()
                data['valid'] = True
                data['model_name'] = model_name
                gurukulam_teachers = Gurukulam_Teacher.objects.filter(sender=request.user)
                data['html'] = render_to_string('account/musician_teacher_gurukulam.html',{'gurukulam_teachers':gurukulam_teachers,},request)
               
            else:
                data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Gurukulam Teacher'},request)
                data['valid'] = False

        else:
            form = Add_Teacher_Gurukulam_Form(request=request)

            data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Add",'model_name':model_name,'model':'Gurukulam Teacher'},request)
            data['valid'] = True

    return JsonResponse(data)


def ajax_edit(request,model_name,pk):
    data =  dict()
    if model_name == 'musician_gurukulam':
        musician_gurukulam = Musician_Gurukulam.objects.get(id=pk,musician=request.user.musician)
        if request.method == "POST":
            form = Musician_Gurukulam_Form(request.POST,request=request,instance=musician_gurukulam)

            if form.is_valid():
                form.save()
                data['valid'] = True
                data['model_name'] = model_name
                data['html'] = render_to_string('account/musician_gurukulam.html',{},request)
            else:
                data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Update",'model_name':model_name,'model':'Gurukulam','pk':pk},request)
                data['valid'] = False

        else:
            form = Musician_Gurukulam_Form(request=request,instance=musician_gurukulam)

            data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Update",'model_name':model_name,'model':'Gurukulam','pk':pk},request)
            data['valid'] = True
    
    elif model_name == "musician_skill":
        musician_skill = Musician_Skill.objects.get(id=pk,musician=request.user.musician)

        if request.method == "POST":
            form = Musician_Skill_Form(request.POST,request=request,instance=musician_skill)

            if form.is_valid():
                form = form.save(commit=False)
                form.musician = request.user.musician
                form.save()
                data['valid'] = True
                data['model_name'] = model_name
                data['html'] = render_to_string('musician/musician_skill.html',{},request)
            else:
                data['form'] = render_to_string('account/musician_skill_form.html',{'form':form,'operation':"Update",'model_name':model_name,'model':'Musician Skill','pk':pk},request)
                data['valid'] = False

        else:
            form = Musician_Skill_Form(request=request,instance=musician_skill)

            data['form'] = render_to_string('account/musician_skill_form.html',{'form':form,'operation':"Update",'model_name':model_name,'model':'Musician Skill','pk':pk},request)
            data['valid'] = True

    elif model_name == 'musician_award':
        musician_award =  Musician_Award.objects.get(id=pk,musician=request.user.musician)
        if request.method == "POST":
            form = Musician_Award_Form(request.POST,request.FILES,request=request,instance=musician_award)

            if form.is_valid():
                form = form.save(commit=False)
                form.musician = request.user.musician
                form.save()
                data['valid'] = True
                data['model_name'] = model_name
                data['html'] = render_to_string('musician/musician_award.html',{},request)
            else:
                data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Update",'model_name':model_name,'model':'Musician Award','pk':pk},request)
                data['valid'] = False

        else:
            form = Musician_Award_Form(request=request,instance=musician_award)
            data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Update",'model_name':model_name,'model':'Musician Award','pk':pk},request)
            data['valid'] = True


    elif model_name == 'highlight':
        highlight = Highlight.objects.get(id=pk,user=request.user)
        if request.method == "POST":
            form = Highlight_Form(request.POST,request=request,instance=highlight)

            if form.is_valid():
                highlight = form.save(commit=False)
                highlight.user = request.user
                highlight.save()
                post =Post.objects.get(user=request.user.id,highlight=highlight.id)
                post.content = highlight.description + '<br>Video Link: <a href='+str(highlight.video_link)+'">Watch Video </a>'
                post.save()
                form.save_m2m()
                data['valid'] = True
                data['model_name'] = model_name
                data['html'] = render_to_string('account/highlight.html',{},request)
            else:
                data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Update",'model_name':model_name,'model':'Highlight','pk':pk},request)
                data['valid'] = False

        else:
            form = Highlight_Form(request=request,instance=highlight)

            data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Update",'model_name':model_name,'model':'Highlight','pk':pk},request)
            data['valid'] = True


    elif model_name == 'event_performer':
        event_performer = Event_Performer.objects.get(id=pk,event_organizer=request.user.event_organizer)
        if request.method == "POST":
            form = Event_Performer_Form(request.POST,request=request,instance=event_performer)

            if form.is_valid():
                performer = form.save(commit=False)
                performer.event_organizer = request.user.event_organizer
                performer.status = "S"
                performer.save()
                
                data['valid'] = True
                data['model_name'] = model_name
                performers = Event_Performer.objects.filter(event_organizer=request.user.event_organizer)
                data['html'] = render_to_string('account/event_performer.html',{'performers':performers,},request)
            else:
                data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Update",'model_name':model_name,'model':'Highlight','pk':pk},request)
                data['valid'] = False

        else:
            form = Event_Performer_Form(request=request,instance=event_performer)
            data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Update",'model_name':model_name,'model':'Performer','pk':pk},request)
            data['valid'] = True


    elif model_name == "gurukulam_skill":
        skill = Gurukulam_Skill.objects.get(id=pk,gurukulam=request.user.gurukulam)
        if request.method == 'POST':
            form = Gurukulam_Skill_Form(request.POST,instance=skill)
            if form.is_valid():                     
                form.save()   
                data['valid'] = True
                data['html'] = render_to_string('gurukulam/skill.html',{},request)
                data['model_name'] = model_name            
            else:
                data['valid'] = False
                data['form'] = render_to_string('account/form.html',{'form':form,'operation':'Update','model':'Skill','model_name':model_name,'pk':pk},request)
        else:
            form = Gurukulam_Skill_Form(instance=skill)
            data['form'] = render_to_string('account/form.html',{'form':form,'operation':'Update','model':'Skill','model_name':model_name,'pk':pk},request)

    elif model_name == "gurukulam_award":
        award = Gurukulam_Award.objects.get(id=pk,gurukulam=request.user.gurukulam)
        if request.method == 'POST':
            form = Gurukulam_Award_Form(request.POST,instance=award)
            if form.is_valid():                    
                form.save()  
                data['valid'] = True
                data['html'] = render_to_string('gurukulam/award.html',{},request)
                data['model_name'] = model_name            
            else:
                data['valid'] = False
                data['form'] = render_to_string('account/form.html',{'form':form,'operation':'Update','model':'Award','model_name':model_name,'pk':pk},request)
        else:
            form = Gurukulam_Award_Form(instance=award)
            data['form'] = render_to_string('account/form.html',{'form':form,'operation':'Update','model':'Award','model_name':model_name,'pk':pk},request)

    elif model_name == "troupe_skill":
        troupe_skill = Troupe_Skill.objects.get(id=pk,troupe=request.user.troupe)

        if request.method == "POST":
            form = Troupe_Skill_Form(request.POST,request=request,instance=troupe_skill)

            if form.is_valid():
                form.save()
                data['valid'] = True
                data['model_name'] = model_name
                troupe_skills = Troupe_Skill.objects.filter(troupe=request.user.troupe)
                data['html'] = render_to_string('troupe/troupe_skill.html',{'troupe_skills':troupe_skills,},request)
            else:
                data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Update",'model_name':model_name,'model':'Troupe Skill','pk':pk},request)
                data['valid'] = False

        else:
            form = Troupe_Skill_Form(request=request,instance=troupe_skill)

            data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Update",'model_name':model_name,'model':'Troupe Skill','pk':pk},request)
            data['valid'] = True


    elif model_name == "lecture_video":
        lecture_video = Lecture_Video.objects.get(id=pk,gurukulam=request.user.gurukulam)
        if request.method == 'POST':
            form = Lecture_Video_Form(request.POST,request=request,instance=lecture_video)
            if form.is_valid():
                lecture_video = form.save(commit=False)
                lecture_video.gurukulam = request.user.gurukulam     
                lecture_video.save()  
                data['model_name'] = model_name 

                lecture_videos = Lecture_Video.objects.filter(gurukulam=request.user.gurukulam)
                data['valid'] = True
                data['html'] = render_to_string('gurukulam/lecture_videos.html',{'lecture_videos':lecture_videos},request)
                
            else:
                
                data['valid'] = False
                data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Update",'model_name':model_name,'model':'Lecture Video','pk':pk,},request)
            
        else:
            form = Lecture_Video_Form(request=request,instance=lecture_video)
            data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Update",'model_name':model_name,'model':'Lecture Video','pk':pk,},request)


    elif model_name == "course":
        course = Course.objects.get(id=pk, gurukulam=request.user.gurukulam)
        if request.method == 'POST':
            form = Course_Form(request.POST,instance=course)
            if form.is_valid():
                course = form.save(commit=False)
                course.gurukulam = request.user.gurukulam     
                course.save() 
                data['model_name'] = model_name   

                courses = Course.objects.filter(gurukulam=request.user.gurukulam)
                data['valid'] = True
                data['html'] = render_to_string('gurukulam/courses.html',{'courses':courses},request)
                
            else:
                data['valid'] = False
                data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Update",'model_name':model_name,'model':'Course','pk':pk,},request)
                
        else:
            form = Course_Form(instance=course)
            data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Update",'model_name':model_name,'model':'Course','pk':pk,},request)

    elif model_name == "testimonial":
        testimonial = Gurukulam_Testimonial.objects.get(id=pk,gurukulam=request.user.gurukulam)
        if request.method == 'POST':
            form = Gurukulam_Testimonial_Form(request.POST,instance=testimonial)
            if form.is_valid():
                testimonial = form.save(commit=False)
                testimonial.gurukulam = request.user.gurukulam
                data['model_name'] = model_name 
                testimonial.save()   
                gurukulam_testimonials = Gurukulam_Testimonial.objects.filter(gurukulam=request.user.gurukulam)
                data['valid'] = True
                data['html'] = render_to_string('gurukulam/testimonials.html',{'testimonials':gurukulam_testimonials},request)
                
            else:
                data['valid'] = False
                data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Update",'model_name':model_name,'model':'Testimonial','pk':pk,},request)
            
        else:
            form = Gurukulam_Testimonial_Form(instance=testimonial)
            data['form'] = render_to_string('account/form.html',{'form':form,'operation':"Update",'model_name':model_name,'model':'Testimonial','pk':pk,},request)

    
    return JsonResponse(data)



def ajax_delete(request,model_name,pk):
    data =  dict()
    if model_name == 'musician_gurukulam':
        musician_gurukulam = Musician_Gurukulam.objects.get(id=pk,musician=request.user.musician)
        musician_gurukulam.delete()
        data['valid'] = True
        data['model_name'] = model_name
        data['html'] = render_to_string('account/musician_gurukulam.html',{},request)
    elif model_name == "musician_skill":
        musician_skill = Musician_Skill.objects.get(id=pk,musician=request.user.musician)
        musician_skill.delete()
        data['valid'] = True
        data['model_name'] = model_name
        data['html'] = render_to_string('musician/musician_skill.html',{},request)
    elif model_name == 'musician_award':
        musician_award =  Musician_Award.objects.get(id=pk,musician=request.user.musician)
        musician_award.delete()
        data['valid'] = True
        data['model_name'] = model_name
        data['html'] = render_to_string('musician/musician_award.html',{},request)
    elif model_name == 'highlight':
        highlight = Highlight.objects.get(id=pk,user=request.user)
        highlight.delete()
        data['valid'] = True
        data['model_name'] = model_name
        data['html'] = render_to_string('account/highlight.html',{},request)

    elif model_name == 'event_performer':
        event_performer = Event_Performer.objects.get(id=pk,event_organizer=request.user.event_organizer)
        event_performer.delete()
        data['valid'] = True
        data['model_name'] = model_name
        performers = Event_Performer.objects.filter(event_organizer=request.user.event_organizer)
        data['html'] = render_to_string('account/event_performer.html',{'performers':performers,},request)
    elif model_name == 'key_performer':
        key_performer = Key_Performer.objects.get(id=pk,troupe=request.user.troupe)
        key_performer.delete()
        data['valid'] = True
        data['model_name'] = model_name
        key_performers = Key_Performer.objects.filter(troupe=request.user.troupe)
        data['html'] = render_to_string('account/key_performer.html',{'key_performers':key_performers,},request)
    elif model_name == 'gurukulam_skill':
        skill = Gurukulam_Skill.objects.get(id=pk,gurukulam=request.user.gurukulam)
        skill.delete()
        data['valid'] = True
        data['model_name'] = model_name
        data['html'] = render_to_string('gurukulam/skill.html',{},request)

    elif model_name == 'gurukulam_award':
        award = Gurukulam_Award.objects.get(id=pk,gurukulam=request.user.gurukulam)
        award.delete()
        data['valid'] = True
        data['model_name'] = model_name
        data['html'] = render_to_string('gurukulam/award.html',{},request)
    elif model_name == 'troupe_skill':
        skill = Troupe_Skill.objects.get(id=pk,troupe=request.user.troupe)
        skill.delete()
        data['valid'] = True
        data['model_name'] = model_name
        troupe_skills = Troupe_Skill.objects.filter(troupe=request.user.troupe)
        data['html'] = render_to_string('troupe/troupe_skill.html',{'troupe_skills':troupe_skills,},request)

    elif model_name == 'lecture_video':
        lecture_video = Lecture_Video.objects.get(id=pk,gurukulam=request.user.gurukulam)
        lecture_video.delete()
        data['valid'] = True
        data['model_name'] = model_name 
        lecture_videos = Lecture_Video.objects.filter(gurukulam=request.user.gurukulam)
        data['valid'] = True
        data['html'] = render_to_string('gurukulam/lecture_videos.html',{'lecture_videos':lecture_videos},request)

    elif model_name == "course":
        course = Course.objects.get(id=pk,gurukulam=request.user.gurukulam)
        course.delete()
        data['valid'] = True
        data['model_name'] = model_name  
        courses = Course.objects.filter(gurukulam=request.user.gurukulam)
        data['valid'] = True
        data['html'] = render_to_string('gurukulam/courses.html',{'courses':courses},request)
    elif model_name == "testimonial":
        testimonial = Gurukulam_Testimonial.objects.get(id=pk,gurukulam=request.user.gurukulam)
        testimonial.delete()
        gurukulam_testimonials = Gurukulam_Testimonial.objects.filter(gurukulam=request.user.gurukulam)
        data['valid'] = True
        data['model_name'] = model_name
        data['html'] = render_to_string('gurukulam/testimonials.html',{'testimonials':gurukulam_testimonials},request)

    elif model_name == "musician_teacher_gurukulam":
        teacher = Gurukulam_Teacher.objects.get(id=pk,sender=request.user)
        teacher.delete()
        gurukulam_teachers = Gurukulam_Teacher.objects.filter(sender=request.user)
        data['valid'] = True
        data['model_name'] = model_name
        data['html'] = render_to_string('account/musician_teacher_gurukulam.html',{'gurukulam_teachers':gurukulam_teachers},request)
                
  
  
    return JsonResponse(data)


#authentication
def google_login(request):
    redirect_uri = "%s://%s%s" % (
        request.scheme, request.get_host(), reverse('google_login')
    )
    if('code' in request.GET):
        params = {
            'grant_type': 'authorization_code',
            'code': request.GET.get('code'),
            'redirect_uri': redirect_uri,
            'client_id': settings.GP_CLIENT_ID,
            'client_secret': settings.GP_CLIENT_SECRET
        }
        url = 'https://accounts.google.com/o/oauth2/token'
        response = requests.post(url, data=params)
        url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        access_token = response.json().get('access_token')
        response = requests.get(url, params={'access_token': access_token})
        user_data = response.json()
        email = user_data.get('email')
        if email:
            try:
                user= User.objects.get(email=str(email))
                login(request, user)
                return redirect(reverse('home'))
            except:
                messages.error(
                request,
                'Unable to login with Gmail Please try again'
                )
                return redirect('/')
                
        else:
            messages.error(
                request,
                'Unable to login with Gmail Please try again'
            )
        return redirect('/')
    else:
        url = "https://accounts.google.com/o/oauth2/auth?client_id=%s&response_type=code&scope=%s&redirect_uri=%s&state=google"
        scope = [
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email"
        ]
        scope = " ".join(scope)
        url = url % (settings.GP_CLIENT_ID, scope, redirect_uri)
        return redirect(url)
        
        
@login_required(login_url='signin')        
def report_people(request,pk):
    reported_user = User.objects.get(id=pk)
    data = dict()
    data['people'] = str(reported_user)
    if request.method == "POST":
        form = Report_People_Form(request.POST,request.FILES, request=request)
        if form.is_valid():
            form = form.save(commit=False)
            form.reported_by = request.user
            form.reported_user = reported_user
            form.save()
            data['valid'] = True
        else:
            data['valid'] = False
    else:
        form = Report_People_Form(request=request)
        data['form'] = render_to_string('account/report_people_form.html',{'form':form,'reported_user':reported_user,'operation':'Add'},request)
    return JsonResponse(data)


def get_inbox_chat(request,user):
    data = dict()
    receiver = User.objects.get(id=user)    
    blocked_list = Blocked_User.objects.filter(Q(blocked_by=receiver,blocked_user=request.user) | Q(blocked_by=request.user,blocked_user=receiver))
    blocked_by_receiver = False
    blocked_by_sender = False
    for blocked in blocked_list:
        if blocked.blocked_by == request.user:
            blocked_by_sender = True
        elif blocked.blocked_user == request.user:
            blocked_by_receiver = True
    try:
        conversation = Conversation.objects.get(Q(sender=request.user,receiver=receiver) | Q(sender=receiver,receiver=request.user))
        chats = Chat.objects.filter(conversation=conversation)
        make_read = Chat.objects.exclude(sender=request.user).filter(conversation=conversation,unread=True).update(unread=False)


    except:
        chats = None

    if request.GET.get('page')  == "inbox":    
        data['messages'] = render_to_string('account/get_all_chat.html',{'chats':chats,'receiver':receiver,'blocked_by_sender':blocked_by_sender,'blocked_by_receiver':blocked_by_receiver,},request)
        data['chat_panel'] = render_to_string('account/chat_panel.html',{'user_object':receiver,},request)

        
    else:
        data['messages'] = render_to_string('account/profile_message.html',{'chats':chats,'receiver':receiver,'blocked_by_sender':blocked_by_sender,'blocked_by_receiver':blocked_by_receiver,},request)

    return JsonResponse(data)


def chat_to(request,user):
    data= dict()
    message = request.POST['message']
    files = request.FILES
    chat_file = files.get('message-file', None)
    chat_to = User.objects.get(id=user)

    if chat_file:
        chat = Chat(sender=request.user,message=message,m_file=chat_file)
    else:
        chat = Chat(sender=request.user,message=message)

    chat.save(receiver=chat_to)

    conversation = Conversation.objects.get(id=chat.conversation.id)
    chats =  Chat.objects.filter(conversation=conversation)
    data['messages'] = data['messages'] = render_to_string('account/chat_message.html',{'chats':chats,'receiver':user,},request)
    data['valid'] = True
    return JsonResponse(data)



def ajax_block_unblock(request,pk):
    data =  dict()    
    blocked_user = User.objects.get(id=pk)
    status = Blocked_User.block_unblock(user=request.user,blocked_user=blocked_user)
    data['blocked'] = status
    return JsonResponse(data)


@login_required(login_url='signin')
def inbox(request):
    conversations = Conversation.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).distinct()
    chats = Chat.objects.filter(Q(conversation__sender=request.user) | Q(conversation__receiver=request.user)).annotate(last=Max('conversation__chat__date')).filter(date=F('last')).order_by('-conversation__date')
    unread_message_count = Message.unread_count(request.user) 
    readed_count = Chat.readed_count(request.user)
    inbox_count = Chat.unread_count(request.user)



    context={
        'chats':chats,
        'unread_message_count':unread_message_count,
        'inbox_count':inbox_count,
        'readed_message_count':readed_count,
    }
    return render(request,'inbox.html',context)


@login_required(login_url='signin')
def view_gurukulam_request(request):
    if request.method == "POST":
        status = request.POST.get('status')
        student_id = request.POST.get('student_id')

        if status == "A":
            status = Musician_Gurukulam.objects.filter(~Q(sender=request.user),musician=request.user.musician,id=student_id).update(status=status)
        elif status == "R":            
            status = Musician_Gurukulam.objects.filter(~Q(sender=request.user),musician=request.user.musician,id=student_id).update(status=status)

        students = Musician_Gurukulam.objects.filter(~Q(sender=request.user),musician=request.user.musician)
       
    else:
        students = Musician_Gurukulam.objects.filter(~Q(sender=request.user),musician=request.user.musician)

    context = {
        'students' : students,
    }

    return render(request, 'musician/view_gurukulam_request.html', context)



def musician_search(request):
    data = dict()

    musician_filter = Musician.objects.all()
    
    if request.method == 'POST':
            skill_level = [ast.literal_eval(i) for i in request.POST.getlist('skill_level')]        
            skill =   [ast.literal_eval(i) for i in request.POST.getlist('skill')]
            location = [ast.literal_eval(i) for i in request.POST.getlist('district')]
            vocal = request.POST.get('vocal')
            gender =  request.POST.getlist('gender')
            name = request.POST.get('name')

            exclude_musicians = ast.literal_eval(request.POST.get('musicians[]'))
            if skill:
                musician_filter = musician_filter.filter(musician_skill__skill__id__in=skill).distinct()
            if skill_level:                
                musician_filter = musician_filter.filter(musician_skill__skill_level__id__in=skill_level).distinct()             
            
            if location:
                musician_filter = musician_filter.filter(user__location__in=location)
            if gender:
                musician_filter = musician_filter.filter(gender__in=gender)
            if name:
                musician_filter = musician_filter.filter(Q(user__last_name__icontains=name) | Q(user__first_name__icontains=name))

      

            
            data['valid'] = True
            page = request.GET.get('page')
            if page == "eventcreation":
            
                data['html'] = render_to_string('event/creation/musician_list.html',{'musicians':musician_filter.exclude(id__in=exclude_musicians)},request)

            elif page == "ec":
                data['html'] = render_to_string('event/musician_list.html',{'musicians':musician_filter.exclude(id__in=exclude_musicians)},request)
            else:
                data['html'] = render_to_string('event/m_list.html',{'musicians':musician_filter.exclude(id__in=exclude_musicians)},request)
             
    else:
        data['valid'] = False

    return JsonResponse(data)




def troupe_search(request):    
    data = dict()    
    if request.method == 'POST':  
            skill = [ast.literal_eval(i) for i in request.POST.getlist('skill')]
            location = [ast.literal_eval(i) for i in request.POST.getlist('location')]
            name = request.POST.get('name')
             
            troupes_list  = Troupe.objects.all()
    
            if skill:
                troupes_list = troupes_list.filter(troupe_skill__skill__id__in=skill).distinct()          
            if location:
                troupes_list = troupes_list.filter(user__location__id__in=location).distinct()
            if name:
                troupes_list = troupes_list.filter(user__name__icontains=name).distinct()

            troupes = troupes_list 

            if len(name) == 0 and  len(skill) == 0 and len(location) == 0:
                troupes = None
                

            data['valid'] = True

            page = request.GET.get('page')
            if page == "ec":
                data['html'] = render_to_string('event/t_list.html',{'troupes':troupes},request)
            else:
                data['html'] = render_to_string('event/troupe_list.html',{'troupes':troupes},request)
             
    else:
        data['valid'] = False

    return JsonResponse(data)


def gurukulam_search(request):
    
    data = dict()
    
    if request.method == 'POST':  

            skill = [ast.literal_eval(i) for i in request.POST.getlist('skill')]
            location = [ast.literal_eval(i) for i in request.POST.getlist('location')]
            name = request.POST.get('name')    
            if skill:                
                if location:
                    if name:                            
                        gurukulas = Gurukulam.objects.filter(user__name__icontains=name,gurukulam_skill__skill__id__in=skill,user__location__id__in=location).distinct()
                    else:
                        gurukulas = Gurukulam.objects.filter(gurukulam_skill__skill__id__in=skill,user__location__id__in=location).distinct()
                elif name:
                    gurukulas = Gurukulam.objects.filter(user__name__icontains=name,gurukulam_skill__skill__id__in=skill).distinct()

                else:
                    gurukulas = Gurukulam.objects.filter(gurukulam_skill__skill__id__in=skill).distinct()
            elif location:
                if name:
                    gurukulas = Gurukulam.objects.filter(user__name__icontains=name,user__location__id__in=location).distinct()

                else:
                    gurukulas = Gurukulam.objects.filter(user__location__id__in=location).distinct()
            elif name:
                gurukulas = Gurukulam.objects.filter(user__name__icontains=name).distinct()
            
            else:
                gurukulas = None
    
            data['valid'] = True

            data['html'] = render_to_string('event/gurukulam_list.html',{'gurukulas':gurukulas},request)
             
    else:
        data['valid'] = False

    return JsonResponse(data)


def view_teacher_sent_request(request):
    pendind_requests =  Gurukulam_Teacher.objects.filter(sender=request.user,gurukulam=request.user.gurukulam,status="S")
    accepted_requests = Gurukulam_Teacher.objects.filter(sender=request.user,gurukulam=request.user.gurukulam,status="A")
    rejected_requests = Gurukulam_Teacher.objects.filter(sender=request.user,gurukulam=request.user.gurukulam,status="R")
    context = {
        'pendind_requests':pendind_requests,
        'accepted_requests':accepted_requests,
        'rejected_requests' : rejected_requests,
    }
    return render(request, 'gurukulam/view_teacher_sent_request.html', context)



def people_filter(request):
    data = dict()
    skill_category = request.POST.getlist('skill_category')
    skill = request.POST.getlist('skill')
    location = request.POST.get('location',None)
    page = request.GET.get('page',None)
    if location == "Choose Location":
        location = None

    name = request.POST.get('name', None)
    people_type= request.POST.get('people_type', None)
    
    if page:
    	user_list = User.objects.filter(groups__name__in=('Musician','Band','Music School','Event Organizer'))
    else:
    	user_list = User.objects.filter(groups__name__in=('Musician','Band','Music School','Event Organizer')).exclude(id=request.user.id)
    
    if name:
        user_list = user_list.filter(Q(last_name__icontains=name) | Q(first_name__icontains=name) | Q(name__icontains=name))
    
    group_list = ['Musician','Event Organizer','Band','Music School']
    if people_type:
        if people_type in group_list:

            user_list = user_list.filter(groups__name=people_type)
        else:
            user_list = user_list.filter(musician__musician_skill__teach=True).distinct()


    if location is not None:
        user_list = user_list.filter(location__id=location)

    if skill:
        user_list = user_list.filter(Q(musician__musician_skill__skill__id__in=skill) | Q(troupe__troupe_skill__skill__id__in=skill)).distinct()
        
    if page:
        data['html'] = render_to_string('landing/filter_people.html',{'users':user_list},request)
        data['valid'] = True
        event_filter = Event.objects.all()
        if skill:
            event_filter = event_filter.filter(event_skill__skill__id__in=skill).distinct()
        if location:   
            event_filter = event_filter.filter(location__id=location)
        if name:
            event_filter = event_filter.filter(name__icontains=name)
            data['event_html'] = render_to_string('landing/filter_event.html',{'events':event_filter},request)
        
        return JsonResponse(data)
    else:
    	data['html'] = render_to_string('account/people_list.html',{'users':user_list},request)
    data['valid'] = True

    return JsonResponse(data)

    

def event_list(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    location = request.GET.get('location',None)
    if location:
        location = int(location)
        events = Event.objects.filter(location__id=location,registration_close_date__gte=datetime.now())
    else:
        events = Event.objects.filter(registration_close_date__gte=datetime.now())

    page = request.GET.get('page',None)

    if page is None:
        page = 1


    paginator = Paginator(events, 5) # 5 users per page
    
    # We don't need to handle the case where the `page` parameter
    # is not an integer because our URL only accepts integers
    try:
        events = paginator.page(page)
    except EmptyPage:
        # if we exceed the page limit we return the last page 
        events = paginator.page(paginator.num_pages)


    locations = Location.objects.all()
    user_counts = User.objects.filter(groups__name__in=('Artist','Music School','Event Organizer','Band')).values('groups__name').annotate(total=Count('groups__name')).order_by('total')
    band_count = organizer_count = music_school_count = musician_count = 0
    for user_count in user_counts:
        if user_count['groups__name'] == "Band":
            band_count = user_count['total']
        elif user_count['groups__name'] == "Event Organizer":
            organizer_count = user_count['total']
        elif user_count['groups__name'] == "Music School":
            music_school_count = user_count['total']
        elif user_count['groups__name'] == "Artist":
            musician_count = user_count['total']

    
    popular_musicians = User.objects.filter(groups__name="Artist").annotate(numof_participating_event_count=Count('musician__minvitation')+Count('musician__minterest')).order_by('-numof_participating_event_count')[:5]




    context = {
        'events': events,
        'locations':locations,
        'location_id': location,
        'musician_count':musician_count,
        'band_count' : band_count,
        'music_school_count':music_school_count,
        'organizer_count':organizer_count,
        'popular_musicians':popular_musicians,


    }

    return render(request, 'display_events.html', context)
    
def show_location_based_events(request):
    data = dict()
    name = request.POST.get('name',None)
    location_id = request.POST.get('location_id',None)
    

    if location_id is not None:
        request.session['temp_location'] = location_id
    else:
        get_location = request.session['temp_location']
        location_id = get_location

    events = Event.objects.filter(location__id=location_id)

    data['html'] = render_to_string('event_list.html',{'events':events},request)

    data['location_id'] = location_id

    return JsonResponse(data)
    
    
def registered_successfully(request):

    return render(request, 'registration/registered.html', {})

    






def location_based_events(request):
    data = dict()
    location = request.POST.get('location',None)
    if location and location != "Select Location":
        location = int(location)
        events = Event.objects.filter(location__id=location,registration_close_date__gte=datetime.now())[:30]
    else:
        events = Event.objects.filter(registration_close_date__gte=datetime.now())[:30]
    data['html'] = render_to_string('landing/events-list.html',{'events':events},request)
    return JsonResponse(data)


def view_musicians(request):
    locations = Location.objects.all()
    location_id = request.GET.get('location','')
    if location_id and  location_id != "Select Location":
        users  = User.objects.filter(groups__name="Artist",location__id=location_id)
    else:
        users  = User.objects.filter(groups__name="Artist")

    page = request.GET.get('page',None)
    if page is None:
        page = 1
    paginator = Paginator(users, 20)
    try:
        users = paginator.page(page)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    if location_id == "Select Location" or location_id == "" :
        return render(request, 'landing/musician_list.html', {'users':users,'locations':locations,'location_id':location_id,'type':'Musician'})
    else:
        return render(request, 'landing/musician_list.html', {'users':users,'locations':locations,'location_id':int(location_id),'type':'Musician'})



def view_bands(request):
    locations = Location.objects.all()

    location_id = request.GET.get('location','')
    if location_id and  location_id != "Select Location":
        users  = User.objects.filter(groups__name="Band",location__id=location_id)
    else:
        users  = User.objects.filter(groups__name="Band")

    page = request.GET.get('page',None)
    if page is None:
        page = 1
    paginator = Paginator(users, 20)
    try:
        users = paginator.page(page)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'landing/musician_list.html', {'users':users,'locations':locations,'location_id':location_id,'type':'Musician'})



def view_organizers(request):
    locations = Location.objects.all()

    location_id = request.GET.get('location','')
    if location_id and  location_id != "Select Location":
        users  = User.objects.filter(groups__name="Event Organizers",location__id=location_id)
    else:
        users  = User.objects.filter(groups__name="Event Organizers")
    page = request.GET.get('page',None)
    if page is None:
        page = 1
    paginator = Paginator(users, 20)
    try:
        users = paginator.page(page)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'landing/musician_list.html', {'users':users,'locations':locations,'location_id':location_id,'type':'Musician'})

def view_music_schools(request):
    locations = Location.objects.all()

    location_id = request.GET.get('location','')
    if location_id and  location_id != "Select Location":
        users  = User.objects.filter(groups__name="Music School",location__id=location_id)
    else:
        users  = User.objects.filter(groups__name="Music School")

    page = request.GET.get('page',None)
    if page is None:
        page = 1
    paginator = Paginator(users, 20)
    try:
        users = paginator.page(page)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'landing/musician_list.html', {'users':users,'locations':locations,'location_id':location_id,'type':'Musician'})



def update_location(request):
    location  = request.GET.get('location',None)
    data  = User.update_location(request.user,location)
    return JsonResponse(data)

@login_required(login_url='signin')
def update_webtour(request):
    data = dict()
    user  = request.user
    user.webtour = True
    user.save()
    data['status'] = "Done"
    return JsonResponse(data)
    
    
    
    

def find_people(request):
	
    locations = Location.objects.all()
    skills = Skill.objects.all()
    skill_categories = Skill_Category.objects.all()
    users= User.objects.filter(is_active=True).exclude(Q(is_superuser=True))

    name = request.GET.get('name', None)
    people_type = request.GET.get('people_type', None)

    if name:
        users = User.objects.filter(Q(last_name__icontains=name) | Q(first_name__icontains=name) | Q(name__icontains=name), groups__name__in=('Musician','Band','Music School','Event Organizer')).exclude(id=request.user.id).distinct()
        events  = Event.objects.filter(name__icontains=name).order_by('-id')[:30]
    else:
        users = User.objects.filter(groups__name__in=('Musician','Music School')).distinct()[:10]
        events  = Event.objects.filter(registration_close_date__gte=datetime.now())[:30]
    
    


    user_groups = Group.objects.all()

    context = {
        'users' : users,
        'name' : name,
        'skills':skills,
        'people_type' : people_type,
        'locations':locations,
        'skill_categories':skill_categories,
        'user_groups':user_groups,
        'events':events,

    }    
    return render(request,'landing/find_people.html', context)



#apiview
#Login
class Login_View(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            serializer = UserSerializer(user,context={'request': request})
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key,'user':serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Location_API(APIView):
    def post(self, request):
        location = request.data.get('location', None)

        if location:

            location_instance = Location.objects.get(id=location)
            user = User.objects.filter(id=request.user.id).update(location=location_instance)
            return Response({'message': "Updated"}, status=status.HTTP_200_OK)


        return Response({"error":"Location Missing"}, status=status.HTTP_400_BAD_REQUEST)



    def get(self, request):
        locations = Location.objects.all()
        serializer = Location_Serializer(locations,many=True)
        skill_categories = Skill_Category.objects.all()
        skill_categories = Skill_Category_Serializer(skill_categories,many=True)
        event_categories = Event_Category.objects.all()
        event_categories  = Event_Category_Serializer(event_categories,many=True)
        skills = Skill.objects.all()
        skills = Skill_Serializer_Filter(skills,many=True)
   
        event_types = Event_Type.objects.all()
        event_types = Event_Type_Serializer(event_types,many=True)
        
        context = {
                    'locations' : serializer.data,
                    'event_types':event_types.data,
                    'event_categories':event_categories.data,
                    'skill_categories':skill_categories.data,
                    'skills':skills.data,
                }
        return Response(context)



#Signup
class Signup_View(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            first_name = serializer.validated_data.get('first_name')
            if not first_name:
                return Response({'message': 'First name is required.'}, status=status.HTTP_400_BAD_REQUEST)
            if len(password) < 8:
                return Response({'message': 'Password should be at least 8 characters long.'}, status=status.HTTP_400_BAD_REQUEST)
            user = serializer.save(username= email,is_active=True)
            user_object = User.objects.get(id=user.id)

            get_group = request.data['groups']
            groups = Group.objects.filter(id__in=get_group)

            for group in groups:                
                if group.name == "Artist":
                    musician = Musician.objects.create(user=user)
                elif group.name == "Music School":
                    ms = Gurukulam.objects.create(user=user)
                elif group.name == "Event Organizer":
                    organizer = Event_Organizer.objects.create(user=user)
                elif group.name == "Band":
                    troupe = Troupe.objects.create(user=user)
                elif group.name == "Music Lover":
                    music_lover = Music_Lover.objects.create(user=user)


            hashed_pwd = make_password(password)
            user = user_object
            user.password = hashed_pwd 
            user = user.save()
            print(user)
            user = user_object


            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('registration/account_active_email.html', {
                'user': user_object,
                'domain': current_site.domain,
                'uid': force_str(urlsafe_base64_encode(force_bytes(user_object.pk))),
                'token':account_activation_token.make_token(user_object),
            })
            to_email = user_object.email
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return Response({'message': 'Signup successful', 'user_id': user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        groups = Group.objects.exclude(name='Portal Admin')
        serializer = Group_Serializer(groups,many=True)
        locations = Location.objects.all()
        location_serializer = Location_Serializer(locations, many=True)
        context = {
                    'groups' : serializer.data,
                    'location': location_serializer.data,
                }
        return Response(context)

#view allows a user to request a password reset by providing their email address.
class Password_Reset(APIView):
    authentication_classes = ()
    permission_classes = ()
    
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            token = default_token_generator.make_token(user)

            current_site = get_current_site(request)
            mail_subject = 'Password Reset.'
            message = render_to_string('registration/password_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': force_str(urlsafe_base64_encode(force_bytes(user.pk))),
                'token':token,
                'protocol':"http"
            })
            to_email = user.email
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()

            # Send an email with a link containing uid and token
            # You can use Django's built-in Email API or a third-party library like Django-Allauth for this purpose.

            return Response({'success': 'Password reset email sent successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Profile View
class My_Profile_View(APIView):

    def get(self, request):
        user_groups = request.user.groups.all()
        for group in user_groups:
            if group.name == "Artist":

                troupes = Key_Performer.objects.filter(musician=request.user.musician)
                gurukulam_teachers = Gurukulam_Teacher.objects.filter(sender=request.user)
                about_me =  Musician.objects.get(user=request.user)
                my_skills = Musician_Skill.objects.filter(musician=request.user.musician)
                highlights = Highlight.objects.filter(user=request.user)
                awards = Musician_Award.objects.filter(musician=request.user.musician)
                schools = Musician_Gurukulam.objects.filter(musician=request.user.musician)
                my_profile_Serializer = My_profileSerializer(request.user,context={'request': request})
                aboutme_Serializer = Aboutme_Serializer(about_me)
                myskills_Serializer= Musician_Skill_Serializer(my_skills ,many=True)
                highlights_Serializer= Musician_Highlight_Serializer(highlights,many=True)
                award_Serializer = Musician_Award_Serializer(awards,many=True,context={'request': request})
                school_Serializer = Musician_School_Serializer(schools,many=True)
                troupe_serializer = KeyPerformerSerializer(troupes, many=True)
                gurukulam_teacher_serializer = GurukulamTeacherSerializer(gurukulam_teachers, many=True)
                context = {
                    'user' : my_profile_Serializer.data,
                    'about_me' : aboutme_Serializer.data,
                    'my_skills' : myskills_Serializer.data,
                    'highlights' : highlights_Serializer.data,
                    'awards' : award_Serializer.data,
                    'association_with_music_band': troupe_serializer.data,
                    'gurukulam_teachers': gurukulam_teacher_serializer.data,
                    'schools': school_Serializer.data,
                    'role': "Musician"

                }
                return Response(context)

            elif group.name == "Event Organizer":
                #performers = Event_Performer.objects.filter(event_organizer=request.user.event_organizer)
                event_about_me = Event_Organizer .objects.get(user=request.user)
                event_performers = Event_Performer.objects.filter(event_organizer=request.user.event_organizer)
                event_highlights = Highlight.objects.filter(user=request.user)
                event_profile_Serializer = Event_profileSerializer(request.user,context={'request': request})
                event_aboutme_Serializer = Event_aboutmeSerializer(event_about_me)
                event_performer_Serializer = Event_Performer_Serializer1(event_performers,many=True,context={'request': request})
                event_highlights_Serializer = Event_Highlight_Serializer(event_highlights,many=True)
                context = {
                    'user' : event_profile_Serializer.data,
                    'about_me': event_aboutme_Serializer.data,
                    'event_performers': event_performer_Serializer.data,
                    'highlights': event_highlights_Serializer.data,
                    'role': "Event Organizer"
                }
                return Response(context)

            elif group.name == "Music Lover":

                musiclover_about_me =  Music_Lover.objects.get(user=request.user)
                musiclover_profile_serializer = Musiclover_profileSerializer(request.user,context={'request': request})
                musiclover_aboutme_Serializer = Musiclover_aboutmeSerializer(musiclover_about_me)

                context ={
                    'user' : musiclover_profile_serializer.data,
                    'about_me': musiclover_aboutme_Serializer.data,
                    'role':  "Music Lover"

                }
                return Response(context)
 
            elif group.name == "Band":
                troupe_about_me = Troupe.objects.get(user=request.user)
                troupe_skills = Troupe_Skill.objects.filter(troupe=request.user.troupe)
                troupe_key_performer = Key_Performer.objects.filter(troupe=request.user.troupe)
                troupe_highlights =  Highlight.objects.filter(user=request.user)
                troupe_profile_Serializer = Troupe_profileSerializer(request.user,context={'request': request})
                troupe_aboutme_Serializer = Troupe_aboutmeSerializer(troupe_about_me)
                troupe_key_performer_Serializer = Troupe_Key_Performer_Serializer(troupe_key_performer,many=True)
                troupe_skills_Serializer= Troupe_Skill_Serializer(troupe_skills ,many=True)
                troupe_highlights_Serializer= Troupe_Highlight_Serializer(troupe_highlights,many=True)
                context = {
                    'user' : troupe_profile_Serializer.data,
                    'troupe_about_me' : troupe_aboutme_Serializer.data,
                    'troupe_skills': troupe_skills_Serializer.data,
                    'troupe_key_performer': troupe_key_performer_Serializer.data,
                    'troupe_highlights' : troupe_highlights_Serializer.data,
                    'role': "Band"
                }
                return Response(context)

            elif group.name == "Music School":
                lecture_videos = Lecture_Video.objects.filter(gurukulam=request.user.gurukulam)
                courses = Course.objects.filter(gurukulam=request.user.gurukulam)
                testimonials = Gurukulam_Testimonial.objects.filter(gurukulam=request.user.gurukulam)
                musicschool_about_me =  Gurukulam.objects.get(user=request.user)
                musicschool_skills = Gurukulam_Skill.objects.filter(gurukulam=request.user.gurukulam)
                musicschool_awards = Gurukulam_Award.objects.filter(gurukulam=request.user.gurukulam)
                musicschool_highlights = Highlight.objects.filter(user=request.user)
                musicschool_profile_Serializer = Musicschool_profileSerializer(request.user,context={'request': request})
                musicschool_aboutme_Serializer = Musicschool_aboutmeSerializer(musicschool_about_me )
                musicschool_skills_Serializer= Musicschool_Skill_Serializer1(musicschool_skills ,many=True)
                musicschool_award_Serializer = Musicschool_Award_Serializer(musicschool_awards,many=True,context={'request': request})
                musicschool_highlights_Serializer= Musicschool_Highlight_Serializer(musicschool_highlights,many=True)
                lecture_videos_serializer = LectureVideoSerializer(lecture_videos, many=True)
                courses_serializer = CourseSerializer(courses, many=True)
                testimonials_serializer = GurukulamTestimonialSerializer(testimonials, many=True)
                context = {
                    'user' : musicschool_profile_Serializer.data,
                    'musicschool_about_me': musicschool_aboutme_Serializer.data,
                    'musicschool_skills' : musicschool_skills_Serializer.data,
                    'musicschool_awards' : musicschool_award_Serializer.data,
                    'musicschool_highlights': musicschool_highlights_Serializer.data,
                    'lecture_videos': lecture_videos_serializer.data,
                    'courses': courses_serializer.data,
                    'testimonials': testimonials_serializer.data,
                    'role': "Music School"
                    
                }
                return Response(context)
        return Response({'message': 'Invalid user group.'})

#Profile Edit(Musician)
@method_decorator(csrf_exempt, name='dispatch')
class Musician_Edit_Api(APIView):
    def get(self, request):
        user  = User.objects.get(id=request.user.id)
        locations = Location.objects.all()
        location_serializer = Location_Serializer(locations, many=True)
        musician = Musician.objects.get(user=request.user)
        musician_serializer = Musician_edit_Serializer(musician)
        user_serializer = User_edit_Serializer(user,context={'request': request})
        context = {
                    'musician' : musician_serializer.data,
                    'user': user_serializer.data,
                    'location': location_serializer.data,
                }
        return Response(context)

    def put(self, request, format=None):
        user  = User.objects.get(id=request.user.id)
        musician = Musician.objects.get(user=request.user)
        user_serializer = User_edit_Serializer1(user, data=request.data,context={'request': request},partial=True)
        musician_serializer = Musician_edit_Serializer(musician, data=request.data,partial=True)
        if musician_serializer.is_valid() and user_serializer.is_valid():
            musician_serializer.save()
            user_serializer.save()
            serializer_dict = user_serializer.data
            response_data = {
                'message':serializer_dict,
            }
            return Response(response_data,status=status.HTTP_200_OK)
        else:
            if not musician_serializer.is_valid():
                return Response(musician_serializer.errors)
            elif not user_serializer.is_valid():
                return Response(user_serializer.errors)
        
            '''context = {
                   'musician_error' : musician_serializer.errors,
                    'user_error' : user_serializer.errors,
                    
                }
            return Response(context)'''


#Profile Edit(Music School)
@method_decorator(csrf_exempt, name='dispatch')
class Musicschool_Edit_Api(APIView):
    def get(self, request):
        user  = User.objects.get(id=request.user.id)
        locations = Location.objects.all()
        location_serializer = Location_Serializer(locations, many=True)
        musicschool = Gurukulam.objects.get(user=request.user)
        musicschool_serializer = Musicschool_edit_Serializer(musicschool)
        user_serializer = User_edit_Serializer(user,context={'request': request})
        context = {
                    'musicschool' : musicschool_serializer.data,
                    'user': user_serializer.data,
                    'location': location_serializer.data,
                }
        return Response(context)

    def put(self, request, format=None):
        user  = User.objects.get(id=request.user.id)
        musicschool = Gurukulam.objects.get(user=request.user)
        user_serializer = User_edit_Serializer1(user, data=request.data)
        musicschool_serializer = Musicschool_edit_Serializer(musicschool, data=request.data)
        if musicschool_serializer.is_valid() and user_serializer.is_valid():
            musicschool_serializer.save()
            user_serializer.save()
            serializer_dict = user_serializer.data
            response_data = {
                'message':serializer_dict,
            }
            return Response(response_data)
        else:
            return Response(musicschool_serializer.errors,user_serializer.errors)

@method_decorator(csrf_exempt, name='dispatch')
class Musiclover_Edit_Api(APIView):
    def get(self, request):
        user  = User.objects.get(id=request.user.id)
        locations = Location.objects.all()
        location_serializer = Location_Serializer(locations, many=True)
        musiclover = Music_Lover.objects.get(user=request.user)
        musiclover_serializer = Musiclover_edit_Serializer(musiclover)
        user_serializer = User_edit_Serializer(user,context={'request': request})
        context = {
                    'musiclover' : musiclover_serializer.data,
                    'user': user_serializer.data,
                    'location': location_serializer.data,
                }
        return Response(context)

    def put(self, request, format=None):
        user  = User.objects.get(id=request.user.id)
        musiclover = Music_Lover.objects.get(user=request.user)
        user_serializer = User_edit_Serializer1(user, data=request.data,context={'request': request},partial=True)
        musiclover_serializer = Musiclover_edit_Serializer(musiclover,data=request.data,partial=True)
        if musiclover_serializer.is_valid() and user_serializer.is_valid():
            musiclover_serializer.save()
            user_serializer.save()
            serializer_dict = user_serializer.data
            response_data = {
                'message':serializer_dict,
            }
            return Response(response_data)

        else:
            if not musiclover_serializer.is_valid():
                return Response(musiclover_serializer.errors)
            elif not user_serializer.is_valid():
                return Response(user_serializer.errors)

        

#Profile Edit(Band)
class Band_Edit_Api(APIView):
    def get(self, request):
        user  = User.objects.get(id=request.user.id)
        locations = Location.objects.all()
        location_serializer = Location_Serializer(locations, many=True)
        band = Troupe.objects.get(user=request.user)
        band_serializer = Troupe_edit_Serializer(band)
        user_serializer = User_edit_Serializer(user,context={'request': request})
        context = {
                    'band' : band_serializer.data,
                    'user': user_serializer.data,
                    'location': location_serializer.data,
                }
        return Response(context)

    def put(self, request, format=None):
        user  = User.objects.get(id=request.user.id)
        band = Troupe.objects.get(user=request.user)
        user_serializer = User_edit_Serializer1(user, data=request.data)
        band_serializer = Troupe_edit_Serializer(band, data=request.data)
        if band_serializer.is_valid() and user_serializer.is_valid():
            band_serializer.save()
            user_serializer.save()
            serializer_dict = user_serializer.data
            response_data = {
                'message':serializer_dict,
            }
            return Response(response_data)
        else:
            return Response(band_serializer.errors,user_serializer.errors)

#Profile Edit(Event Organizer)
@method_decorator(csrf_exempt, name='dispatch')
class Event_Edit_Api(APIView):
    #view
    def get(self, request):
        user  = User.objects.get(id=request.user.id)
        locations = Location.objects.all()
        location_serializer = Location_Serializer(locations, many=True)
        event = Event_Organizer.objects.get(user=request.user)
        event_serializer = Event_edit_Serializer(event)
        user_serializer = User_edit_Serializer(user,context={'request': request})
        context = {
                    'event' : event_serializer.data,
                    'user': user_serializer.data,
                    'location': location_serializer.data,
                }
        return Response(context)

    #update
    def put(self, request, format=None):
        user  = User.objects.get(id=request.user.id)
        event = Event_Organizer.objects.get(user=request.user)
        user_serializer = User_edit_Serializer1(user, data=request.data,context={'request': request},partial=True)
        event_serializer = Event_edit_Serializer(event, data=request.data,partial=True)
        if event_serializer.is_valid() and user_serializer.is_valid():
            event_serializer.save()
            user_serializer.save()  
            serializer_dict = user_serializer.data
            response_data = {
                'message':serializer_dict,
            }
            return Response(response_data,status=status.HTTP_200_OK)
        else:
            if not event_serializer.is_valid():
                return Response(event_serializer.errors)
            elif not user_serializer.is_valid():
                return Response(user_serializer.errors)

#View Profile Details
class View_Profile(APIView):
    authentication_classes = ()
    permission_classes = ()
    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except:
            return Response({'message': 'User Not Found..!'}, status=status.HTTP_404_NOT_FOUND)
        user_groups = user.groups.all()
        for group in user_groups:
            if group.name == "Artist":
                troupes = Key_Performer.objects.filter(musician=user.musician)                
                gurukulam_teachers = Gurukulam_Teacher.objects.filter(sender=user)
                about_me =  Musician.objects.get(user=user)
                my_skills = Musician_Skill.objects.filter(musician=user.musician)
                highlights = Highlight.objects.filter(user=user)
                awards = Musician_Award.objects.filter(musician=user.musician)
                posts = Post.objects.filter(user=user)
                schools = Musician_Gurukulam.objects.filter(musician=user.musician)
                my_profile_Serializer = My_profileSerializer(user, context={'request': request})
                aboutme_Serializer = Aboutme_Serializer(about_me)
                myskills_Serializer= Musician_Skill_Serializer(my_skills ,many=True)
                highlights_Serializer= Musician_Highlight_Serializer(highlights,many=True)
                award_Serializer = Musician_Award_Serializer(awards,many=True, context={'request': request})
                musician_post_Serializer = Musician_Post_Serializer(posts,many=True)
                school_Serializer = Musician_School_Serializer(schools,many=True)
                troupe_serializer = KeyPerformerSerializer(troupes, many=True)               
                gurukulam_teacher_serializer = GurukulamTeacherSerializer(gurukulam_teachers, many=True)
                context = {
                    'user' : my_profile_Serializer.data,
                    'about_me' : aboutme_Serializer.data,
                    'my_skills' : myskills_Serializer.data,
                    'highlights' : highlights_Serializer.data,
                    'awards' : award_Serializer.data,
                    'association_with_music_band': troupe_serializer.data,                   
                    'gurukulam_teachers': gurukulam_teacher_serializer.data,
                    'posts': musician_post_Serializer.data,
                    'schools': school_Serializer.data,
                    'role': "Musician"
                }
                return Response(context)
            elif group.name == "Event Organizer":
                event_posts = Post.objects.filter(user=user)
                event_about_me = Event_Organizer .objects.get(user=user)
                event_performers = Event_Performer.objects.filter(event_organizer=user.event_organizer)
                event_highlights = Highlight.objects.filter(user=user)
                event_profile_Serializer = Event_profileSerializer(user, context={'request': request})
                event_aboutme_Serializer = Event_aboutmeSerializer(event_about_me)
                event_performer_Serializer = Event_Performer_Serializer1(event_performers,many=True,context={'request': request})
                event_highlights_Serializer = Event_Highlight_Serializer(event_highlights,many=True)
                event_post_Serializer = Event_Post_Serializer(event_posts,many=True)
                context = {                    
                    'user' : event_profile_Serializer.data,
                    'about_me': event_aboutme_Serializer.data,
                    'posts': event_post_Serializer.data,                    
                    'event_performers': event_performer_Serializer.data,
                    'highlights': event_highlights_Serializer.data,
                    'role': "Event Organizer"
                }
                return Response(context)
            elif group.name == "Band":
                troupe_about_me = Troupe.objects.get(user=user)
                troupe_skills = Troupe_Skill.objects.filter(troupe=user.troupe)
                troupe_key_performer = Key_Performer.objects.filter(troupe=user.troupe)
                troupe_highlights =  Highlight.objects.filter(user=user)
                troupe_posts =  Post.objects.filter(user=user)
                troupe_profile_Serializer = Troupe_profileSerializer(user, context={'request': request})
                troupe_aboutme_Serializer = Troupe_aboutmeSerializer(troupe_about_me)
                troupe_key_performer_Serializer = Troupe_Key_Performer_Serializer(troupe_key_performer,many=True)
                troupe_skills_Serializer= Troupe_Skill_Serializer(troupe_skills ,many=True)
                troupe_highlights_Serializer= Troupe_Highlight_Serializer(troupe_highlights,many=True)
                troupe_post_Serializer = Troupe_Post_Serializer(troupe_posts,many=True)
                context = {
                    'user' : troupe_profile_Serializer.data,
                    'troupe_about_me' : troupe_aboutme_Serializer.data,
                    'troupe_skills': troupe_skills_Serializer.data,
                    'troupe_key_performer': troupe_key_performer_Serializer.data,
                    'troupe_highlights' : troupe_highlights_Serializer.data,
                    'troupe_posts': troupe_post_Serializer.data,
                    'role': "Band"
                }
                return Response(context)
            elif group.name == "Music School":
                lecture_videos = Lecture_Video.objects.filter(gurukulam=user.gurukulam)
                courses = Course.objects.filter(gurukulam=user.gurukulam)
                testimonials = Gurukulam_Testimonial.objects.filter(gurukulam=user.gurukulam)
                musicschool_about_me =  Gurukulam.objects.get(user=user)
                musicschool_skills = Gurukulam_Skill.objects.filter(gurukulam=user.gurukulam)
                musicschool_awards = Gurukulam_Award.objects.filter(gurukulam=user.gurukulam)
                musicschool_highlights = Highlight.objects.filter(user=user)
                musicschool_posts =  Post.objects.filter(user=user)
                musicschool_profile_Serializer = Musicschool_profileSerializer(user, context={'request': request})
                musicschool_aboutme_Serializer = Musicschool_aboutmeSerializer(musicschool_about_me )
                musicschool_skills_Serializer= Musicschool_Skill_Serializer(musicschool_skills ,many=True)
                musicschool_award_Serializer = Musicschool_Award_Serializer(musicschool_awards,many=True,context={'request': request})
                musicschool_highlights_Serializer= Musicschool_Highlight_Serializer(musicschool_highlights,many=True)
                musicschool__post_Serializer = Musicschool_Post_Serializer(musicschool_posts,many=True)
                lecture_videos_serializer = LectureVideoSerializer(lecture_videos, many=True)
                courses_serializer = CourseSerializer(courses, many=True)
                testimonials_serializer = GurukulamTestimonialSerializer(testimonials, many=True)
                context = {
                    'user' : musicschool_profile_Serializer.data,
                    'musicschool_about_me': musicschool_aboutme_Serializer.data,
                    'musicschool_skills' : musicschool_skills_Serializer.data,
                    'musicschool_awards' : musicschool_award_Serializer.data,
                    'musicschool_highlights': musicschool_highlights_Serializer.data,
                    'musicschool_posts':  musicschool__post_Serializer.data,
                    'lecture_videos': lecture_videos_serializer.data,
                    'courses': courses_serializer.data,
                    'testimonials': testimonials_serializer.data,
                    'role': "Music School"
                }
                return Response(context)
        return Response({'message': 'Invalid user group.'})

#Post View(Wall)
class Post_View(APIView):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get(self, request):
        posts = Post.objects.all()
        paginator = PageNumberPagination()
        # Paginate the queryset
        result_page = paginator.paginate_queryset(posts, request)  
        serializer = Post_Serializer(result_page, many=True,context={'request': request})
        return paginator.get_paginated_response(serializer.data)
    



#Commenting on post
class Post_Comment_Api(APIView):
    def post(self, request,pk):
        post = Post.objects.get(id=pk)
        serializer = Post_Comment_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user,post=post)
            return Response(serializer.data)
        return Response(serializer.errors)

#like and unlike the post
class Like_Unlike(APIView):
    def get(self,request,pk):
        data =  dict()
        post = Post.like_or_unlike(id=pk,user=request.user)
        post = Post.objects.get(id=pk)
        likes_count = post.user_likes.count()
        if post:
            data['liked'] = True
            data['like_count'] = likes_count
        else:
            data['like_count'] = likes_count
        return Response(data)

#Delete Comment of the post
class Post_Comment_Delete(APIView):
    def delete(self, request, pk):
        data = dict()
        try:
            comment = Post_Comment.objects.get(id=pk)
            if comment.user == request.user:
                post = comment.post.id
                comment.delete()
                post = Post.objects.get(id=post)
                data['valid'] = True
                data['comment_count'] = str(post.comment_count)
                data['post_id'] = post.id
            else:
                data['valid'] = False
            return Response(data,status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            data['valid'] = False
            data['error'] = "Comment not found"
            return Response(data,status=status.HTTP_404_NOT_FOUND)

#Load more post
class Load_More_Post(APIView):
    def post(self, request):
        data = dict()
        if request.method == "POST":
            count = int(request.POST['count'])
            limit = 10
            following_users = UserFollowing.objects.filter(user=request.user).values_list('following_user_id', flat=True)
            posts = Post.objects.all()[count:limit+count]
            serializer = Post_Serializer(posts,many=True)
            total_count = Post.objects.all().count()
            data['posts'] = serializer.data
            data['total_count'] = total_count
            data['valid'] = True
        else:
            data['valid'] = False
        return Response(data)

#Following VIew
class Following_API(APIView):
    def get(self, request):
        followings = UserFollowing.objects.filter(user=request.user)
        paginator = PageNumberPagination()
        # Paginate the queryset
        result_page = paginator.paginate_queryset(followings, request)        
        # Serialize the paginated data
        serializer = Following_Serializer(result_page, many=True,context={'request': request})        
        # Return the paginated response
        return paginator.get_paginated_response(serializer.data)
    

    def post(self, request):
        name = request.data['name']
        skill_category = request.data['skill_category']
        skill = request.data['skill']
        location = request.data['location']     
        people_type = request.data['people_type']



        followings = UserFollowing.objects.filter(user=request.user)
        
        if name:
            followings = followings.filter(Q(following_user_id__last_name__icontains=name) | Q(following_user_id__first_name__icontains=name))
    
        if people_type:
            followings = followings.filter(following_user_id__groups__id__in=people_type)
                     

        if location:
            followings = followings.filter(following_user_id__location__id__in=location)

        if skill:            
            followings = followings.filter(Q(following_user_id__musician__musician_skill__skill__id__in=skill) | Q(following_user_id__troupe__troupe_skill__skill__id__in=skill)).distinct()

        paginator = PageNumberPagination()
        # Paginate the queryset
        result_page = paginator.paginate_queryset(followings, request)        
        # Serialize the paginated data
        serializer = Following_Serializer(result_page, many=True,context={'request': request})        
        # Return the paginated response
        return paginator.get_paginated_response(serializer.data)


#Followers  View
class Followers_API(APIView):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get(self, request):
        followings = UserFollowing.objects.filter(following_user_id =request.user.id)
        paginator = PageNumberPagination()
        # Paginate the queryset
        result_page = paginator.paginate_queryset(followings, request)        
        # Serialize the paginated data
        serializer = Followers_Serializer(result_page, many=True,context={'request': request})        
        # Return the paginated response
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        name = request.data['name']

        skill = request.data['skill']
        location = request.data['location']     
        people_type = request.data['people_type']

        followings = UserFollowing.objects.filter(following_user_id =request.user.id)
        if name:
            followings = followings.filter(Q(user__last_name__icontains=name) | Q(user__first_name__icontains=name))
        
        if people_type:
            followings = followings.filter(user__groups__id__in=people_type)
                     

        if location:
            followings = followings.filter(user__location__id__in=location)

        if skill:            
            followings = followings.filter(Q(user__musician__musician_skill__skill__id__in=skill) | Q(user__troupe__troupe_skill__skill__id__in=skill)).distinct()



        paginator = PageNumberPagination()
        # Paginate the queryset
        result_page = paginator.paginate_queryset(followings, request)        
        # Serialize the paginated data
        serializer = Followers_Serializer(result_page, many=True,context={'request': request})        
        # Return the paginated response
        return paginator.get_paginated_response(serializer.data)



#Follow  View
class Follow_API(APIView):


    def get(self, request,pk):
        data = dict()

        if not  UserFollowing.objects.filter(user=request.user,following_user_id=pk).exists():
            user_object = User.objects.get(id=pk)
            follow = UserFollowing.objects.create(user=request.user,following_user_id=user_object)
            data['valid'] = True
        else:
            data['valid'] = False

        return JsonResponse(data)
    

class Unfollow_API(APIView):

    def get(self, request,pk):
        data = dict()

        try:
            follow = UserFollowing.objects.get(following_user_id=pk,user=request.user) 
            follow.delete()
            data['valid'] = True  
        except:
            data['valid'] = False

        return JsonResponse(data)
                
        followings = UserFollowing.objects.filter(following_user_id =request.user.id)
        paginator = PageNumberPagination()
        # Paginate the queryset
        result_page = paginator.paginate_queryset(followings, request)        
        # Serialize the paginated data
        serializer = Followers_Serializer(result_page, many=True,context={'request': request})        
        # Return the paginated response
        return paginator.get_paginated_response(serializer.data)



def ajax_follow(request,pk):
    data = dict()    
    if not  UserFollowing.objects.filter(user=request.user,following_user_id=pk).exists():
        user_object = User.objects.get(id=pk)
        follow = UserFollowing.objects.create(user=request.user,following_user_id=user_object)
        data['valid'] = True
    else:
        data['valid'] = False

    return JsonResponse(data)

def ajax_unfollow(request,pk):
    data = dict()

    try:
        follow = UserFollowing.objects.get(following_user_id=pk,user=request.user) 
        follow.delete()
        data['valid'] = True  
        

    except:
        data['valid'] = False

    return JsonResponse(data)

#All Peoples View
class All_People_API(APIView):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get(self, request,format=None):
        users = User.objects.filter(is_active=True).exclude(Q(id=request.user.id) | Q(is_superuser=True)).order_by('-id')
        paginator = PageNumberPagination()
        # Paginate the queryset
        result_page = paginator.paginate_queryset(users, request)        
        # Serialize the paginated data
        serializer = All_People_Serializer(result_page, many=True,context={'request': request})        
        # Return the paginated response
        return paginator.get_paginated_response(serializer.data)


#All Chats View with last message
class Chatbox_API(APIView):
    def get(self, request):
        conversations = Conversation.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).distinct()
        unread_message_count = Message.unread_count(request.user)
        readed_count = Chat.readed_count(request.user)
        inbox_count = Chat.unread_count(request.user)
        serializer = Conversation_Serializer(conversations, many=True,context={'request': request})
        paginator = PageNumberPagination()
        # Paginate the queryset
        result_page = paginator.paginate_queryset(conversations, request)        
        # Serialize the paginated data
        serializer = Conversation_Serializer(result_page, many=True,context={'request': request})        
        # Return the paginated response
        chat = paginator.get_paginated_response(serializer.data)

        context={
            'chats':chat.data,
            'unread_message_count':unread_message_count,
            'inbox_count':inbox_count,
            'readed_message_count':readed_count,
        }
        return Response(context)
    

    def post(self, request):
        name = request.data['name']
        conversations = Conversation.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).distinct()
        if name:           
            send_conversations = list(conversations.filter(Q(sender__last_name__icontains=name) | Q(sender__first_name__icontains=name),receiver=request.user).distinct().values_list("id",flat=True))
            rece_conversations = list(conversations.filter(Q(receiver__last_name__icontains=name) | Q(receiver__first_name__icontains=name),sender=request.user).distinct().values_list("id",flat=True))
            filtered_chat = send_conversations + rece_conversations        
            conversations = conversations.filter(id__in=filtered_chat)
        unread_message_count = Message.unread_count(request.user)
        readed_count = Chat.readed_count(request.user)
        inbox_count = Chat.unread_count(request.user)
        serializer = Conversation_Serializer(conversations, many=True,context={'request': request})
        paginator = PageNumberPagination()
        # Paginate the queryset
        result_page = paginator.paginate_queryset(conversations, request)        
        # Serialize the paginated data
        serializer = Conversation_Serializer(result_page, many=True,context={'request': request})        
        # Return the paginated response
        chat = paginator.get_paginated_response(serializer.data)

        context={
            'chats':chat.data,
            'unread_message_count':unread_message_count,
            'inbox_count':inbox_count,
            'readed_message_count':readed_count,
        }
        return Response(context)

#Conversation View
class Get_Message_API(APIView):
    def get(self, request,pk):
        chats  = Chat.objects.filter(conversation__id=pk)
        #invitation = Invitation.objects.get(id=pk)
        serializer = Chat_Serializer(chats, many=True, context={'request': request})
        #invitation_serializer = Invitation_Serializer(invitation,context={'request': request})
        context = {
                    'chat' : serializer.data,
                    #'invitation':invitation_serializer.data,
                }
        return Response(context)

#Message Sent
class Put_Message_API(APIView):
    def post(self, request,pk):
        data= dict()
        message = request.data['message']
        files = request.FILES
        chat_file = files.get('message-file', None)
        chat_to = User.objects.get(id=pk)
        chat = Chat(sender=request.user,message=message)
        chat.save(receiver=chat_to)
        conversation = Conversation.objects.get(id=chat.conversation.id)
        chats =  Chat.objects.filter(conversation=conversation)
        serializer = Chat_Serializer(chats, many=True, context={'request': request})
        data['messages']  = serializer.data
        return Response(data)    

#recommended people
class Recommended_People_API(APIView):
    def get(self,request):
        followers_friends = list(UserFollowing.objects.filter(following_user_id=request.user.id).values_list('user__id',flat=True).order_by('?')[:3])
        eventer  = Event_Skill.objects.filter(event__event_organizer__isnull=False).values_list('event__event_organizer__user__id', flat=True).order_by('?')[:2]
        recommended_peoples = list(followers_friends) + list(eventer)
        recommended_peoples = [*set(recommended_peoples)]
        recommended_peoples = User.objects.filter(id__in=recommended_peoples).exclude(id=request.user.id)[:5]
        recommended_peoples = All_People_Serializer(recommended_peoples,many=True)
        context = {
                    'recommended_peoples' : recommended_peoples.data,
                }
        return Response(context)

#recent followers
class Recent_Followers_API(APIView):
    def get(self, request):
        followings = UserFollowing.objects.filter(following_user_id =request.user.id).order_by('created')[:5]
        serilaizer  = Followers_Serializer(followings, many=True)

        return Response(serilaizer.data)

#Add Skill(Musician)
class Musician_Myskill_Add(APIView):
    def get(self,request):
        skills = Skill.objects.all()
        skill_levels = Skill_Level.objects.all()
        skill_serializer = Skill_Serializer(skills, many=True)
        skill_level_serializer = Skill_Level_Serializer(skill_levels,many=True)
        context = {
                    'skills': skill_serializer.data,
                    'skill_levels': skill_level_serializer.data,
                }
        return Response(context)

    def post(self, request):
        serializer = Add_Musician_Skill_Serializer(data=request.data)
        if serializer.is_valid():
            obj=serializer.save(musician=request.user.musician)
            #serializer = Musician_Skill_Serializer(Musician_Skill.objects.get(id=obj.pk))
            return Response({'id':obj.id})
        return Response(serializer.errors)

#Add Musicschool(Musician)
class Musician_Myschool_Add(APIView):
    def get(self,request):
        gurukulam = Gurukulam.objects.all()
        gurukulam_serializer = Gurukulam_Serializer(gurukulam,many=True)
        context = {
                    'gurukulam': gurukulam_serializer.data,
                }
        return Response(context)

    def post(self, request):
        serializer = Musician_Myschool_Serializer(data=request.data)
        if serializer.is_valid():
            obj=serializer.save(musician=request.user.musician,status='S')
            #serializer = Musician_Skill_Serializer(Musician_Skill.objects.get(id=obj.pk))
            return Response(serializer.data)
        return Response(serializer.errors)

#Add Awards(Musician)
class Musician_Myaward_Add(APIView):
    def post(self, request):
        serializer = Musician_Myaward_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(musician=request.user.musician)
            return Response(serializer.data)
        return Response(serializer.errors)

#Add Highlights
class Myhighlight_Add(APIView):
    def post(self, request):
        serializer = Myhighlight_Serializer(data=request.data)
        if serializer.is_valid():
            highlight = serializer.save(user=request.user)
            post_content = highlight.description + '<br>Video Link: <a href="' + str(highlight.video_link) + '">Watch Video</a>'
            post = Post.objects.create(highlight=highlight, user=request.user, content=post_content)
            data = {
                "message": "Highlight added successfully.",
                "highlight": serializer.data,
            }
            return Response(data)
        return Response(serializer.errors)

#Add Skill(Musicschool)
class Musicschool_Myskill_Add(APIView):
    def get(self,request):
        skills = Skill.objects.all()
        skill_serializer = Skill_Serializer(skills, many=True)
        context = {
                    'skills': skill_serializer.data,
                }
        return Response(context)

    def post(self,request):
        serializer = Musicschool_Skill_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(gurukulam=request.user.gurukulam)
            return Response(serializer.data)
        return Response(serializer.errors)

#Add Awards(Musicschool)
class Musicschool_Myaward_Add(APIView):
    def post(self, request):
        serializer = Musicschool_Myaward_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(gurukulam=request.user.gurukulam)
            return Response(serializer.data)
        return Response(serializer.errors)

#Add Lecture Videos(Musicschool)
class Musicschool_Lecture_Videos_Add(APIView):
    def post(self, request):
        serializer = Musicschool_Lecture_Videos_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(gurukulam=request.user.gurukulam)
            return Response(serializer.data)
        return Response(serializer.errors)

#Add Event Performer(Event Organizer)
class Event_Performer_Add(APIView):
    def get(self,request):
        musician = Musician.objects.all()
        troupe = Troupe.objects.all()
        musician_serializer = Musician_Serializer(musician, many=True)
        troupe_serializer = Troupe_Serializer(troupe,many=True)
        context = {
                    'musicians': musician_serializer.data,
                    'troupes': troupe_serializer.data,
                }
        return Response(context)

    def post(self, request):
        serializer = Event_Performer_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(event_organizer=request.user.event_organizer)
            return Response(serializer.data)
        return Response(serializer.errors)

#Add Skill(Band)
class Band_Myskill_Add(APIView):
    def get(self,request):
        skills = Skill.objects.all()
        skill_serializer = Skill_Serializer(skills, many=True)
        context = {
                    'skills': skill_serializer.data,
                }
        return Response(context)

    def post(self, request):
        serializer = Band_Skill_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(troupe=request.user.troupe)
            return Response(serializer.data)
        return Response(serializer.errors)

#Add Key Performer(Band)
class Band_Performer_Add(APIView):
    def get(self,request):
        musician = Musician.objects.all()
        musician_serializer = Musician_Serializer(musician, many=True)
        context = {
                    'musicians': musician_serializer.data,
                }
        return Response(context)

    def post(self, request):
        serializer = Band_Performer_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(troupe=request.user.troupe)
            return Response(serializer.data)
        return Response(serializer.errors)

#Delete(model)
class Delete(APIView):
    def post(self, request, model_name, pk):
        data = dict()
        if model_name == 'musician_gurukulam':
            musician_gurukulam = Musician_Gurukulam.objects.get(id=pk,musician=request.user.musician)
            musician_gurukulam.delete()
            data['valid'] = True
            data['model_name'] = model_name
        elif model_name == "musician_skill":
            musician_skill = Musician_Skill.objects.get(id=pk,musician=request.user.musician)
            musician_skill.delete()
            data['valid'] = True
            data['model_name'] = model_name
        elif model_name == 'musician_award':
            musician_award =  Musician_Award.objects.get(id=pk,musician=request.user.musician)
            musician_award.delete()
            data['valid'] = True
            data['model_name'] = model_name
        elif model_name == 'highlight':
            highlight = Highlight.objects.get(id=pk,user=request.user)
            highlight.delete()
            data['valid'] = True
            data['model_name'] = model_name
        elif model_name == 'event_performer':
            event_performer = Event_Performer.objects.get(id=pk,event_organizer=request.user.event_organizer)
            event_performer.delete()
            data['valid'] = True
            data['model_name'] = model_name
            performers = Event_Performer.objects.filter(event_organizer=request.user.event_organizer)
        elif model_name == 'key_performer':
            key_performer = Key_Performer.objects.get(id=pk,troupe=request.user.troupe)
            key_performer.delete()
            data['valid'] = True
            data['model_name'] = model_name
            key_performers = Key_Performer.objects.filter(troupe=request.user.troupe)
        elif model_name == 'gurukulam_skill':
            skill = Gurukulam_Skill.objects.get(id=pk,gurukulam=request.user.gurukulam)
            skill.delete()
            data['valid'] = True
            data['model_name'] = model_name
        elif model_name == 'gurukulam_award':
            award = Gurukulam_Award.objects.get(id=pk,gurukulam=request.user.gurukulam)
            award.delete()
            data['valid'] = True
            data['model_name'] = model_name
        elif model_name == 'troupe_skill':
            skill = Troupe_Skill.objects.get(id=pk,troupe=request.user.troupe)
            skill.delete()
            data['valid'] = True
            data['model_name'] = model_name
            troupe_skills = Troupe_Skill.objects.filter(troupe=request.user.troupe)
        elif model_name == 'lecture_video':
            lecture_video = Lecture_Video.objects.get(id=pk,gurukulam=request.user.gurukulam)
            lecture_video.delete()
            data['valid'] = True
            data['model_name'] = model_name
            lecture_videos = Lecture_Video.objects.filter(gurukulam=request.user.gurukulam)
            data['valid'] = True
        elif model_name == "course":
            course = Course.objects.get(id=pk,gurukulam=request.user.gurukulam)
            course.delete()
            data['valid'] = True
            data['model_name'] = model_name
            courses = Course.objects.filter(gurukulam=request.user.gurukulam)
            data['valid'] = True
        elif model_name == "musician_teacher_gurukulam":
            teacher = Gurukulam_Teacher.objects.get(id=pk,sender=request.user)
            teacher.delete()
            gurukulam_teachers = Gurukulam_Teacher.objects.filter(sender=request.user)
            data['valid'] = True
            data['model_name'] = model_name
        return Response(data,status=status.HTTP_200_OK)

#Edit skill(Musician)
class Musician_Myskill_Edit(APIView):
    def get(self,request,pk):
        skills = Skill.objects.all()
        skill_levels = Skill_Level.objects.all()
        musician_skills = Musician_Skill.objects.get(id=pk,musician=self.request.user.musician)
        skill_serializer = Skill_Serializer(skills, many=True)
        skill_level_serializer = Skill_Level_Serializer(skill_levels,many=True)
        musician_skills_serializer = Add_Musician_Skill_Serializer(musician_skills)
        context = {
                    'skills': skill_serializer.data,
                    'skill_levels': skill_level_serializer.data,
                    'musician_myskills':musician_skills_serializer.data,
                }
        return Response(context)

    def put(self, request, pk):
        musician_skill = Musician_Skill.objects.get(id=pk,musician=request.user.musician)
        skill_serializer = Add_Musician_Skill_Serializer(musician_skill, data=request.data, partial=True)
        if skill_serializer.is_valid():
            skill_serializer.save()
            response_data = {
                'message':skill_serializer.data,
            }
            return Response(response_data)
        else:
            return Response(skill_serializer.errors)

#Edit Musicschool(Musician)
class Musician_Myschool_Edit(APIView):
    def get(self,request,pk):
        gurukulam = Gurukulam.objects.all()
        myschool = Musician_Gurukulam.objects.get(id=pk,musician=self.request.user.musician)
        musician_myschool = Musician_Myschool_Serializer(myschool)
        gurukulam_serializer = Gurukulam_Serializer(gurukulam,many=True)
        context = {
                    'musician_myschool' : musician_myschool.data,
                    'gurukulam': gurukulam_serializer.data,
                }
        return Response(context)

    def put(self, request, pk):
        musician_myschool= Musician_Gurukulam.objects.get(id=pk,musician=request.user.musician)
        myschool_serializer = Musician_Myschool_Serializer(musician_myschool, data=request.data, partial=True)
        if myschool_serializer.is_valid():
            myschool_serializer.save()
            response_data = {
                'message':myschool_serializer.data,
            }
            return Response(response_data)
        else:
            return Response(myschool_serializer.errors)

#Edit Award(Musician)
class Musician_Myaward_Edit(APIView):
    def get(self,request,pk):
        musician_myawards = Musician_Award.objects.get(id=pk,musician=self.request.user.musician)
        musician_myaward_serializer = Musician_Myaward_Serializer(musician_myawards)
        context = {
                    'musician_awards':musician_myaward_serializer.data,
                }
        return Response(context)

    def put(self, request, pk):
        musician_award = Musician_Award.objects.get(id=pk,musician=request.user.musician)
        myawards_serializer = Musician_Myaward_Serializer(musician_award,data=request.data, partial=True)
        if myawards_serializer.is_valid():
            myawards_serializer.save()
            response_data = {
                'message':myawards_serializer.data,
            }
            return Response(response_data)

        else:
            return Response(myawards_serializer.errors)

#Edit Highlights
class Myhighlight_Edit(APIView):
    def get(self,request,pk):
        myhighlights = Highlight.objects.get(id=pk,user=self.request.user)
        myhighlight_serializer = Myhighlight_Serializer(myhighlights)
        context = {
                    'highlights':myhighlight_serializer.data,
                }
        return Response(context)

    def put(self, request, pk):
        highlights = Highlight.objects.get(id=pk,user=request.user)
        myhighlights_serializer = Myhighlight_Serializer(highlights,data=request.data, partial=True)
        if myhighlights_serializer.is_valid():
            myhighlights_serializer.save()
            response_data = {
                'message': myhighlights_serializer.data,
            }
            return Response(response_data)
        else:
            return Response(myhighlights_serializer.errors)

#Edit skill(Musicschool)
class Musicschool_Myskill_Edit(APIView):
    def get(self,request,pk):
        skills = Skill.objects.all()
        musicschool_skills = Gurukulam_Skill.objects.get(id=pk,gurukulam=self.request.user.gurukulam)
        skill_serializer = Skill_Serializer(skills, many=True)
        musicschool_skills_serializer = Musicschool_Skill_Serializer(musicschool_skills)
        context = {
                    'skills': skill_serializer.data,
                    'musicschool_myskills':musicschool_skills_serializer.data,
                }
        return Response(context)

    def put(self, request, pk):
        musicschool_skill = Gurukulam_Skill.objects.get(id=pk,gurukulam=request.user.gurukulam)
        skill_serializer = Musicschool_Skill_Serializer(musicschool_skill, data=request.data, partial=True)
        if skill_serializer.is_valid():
            skill_serializer.save()
            response_data = {
                'message':skill_serializer.data,
            }
            return Response(response_data)
        else:
            return Response(skill_serializer.errors)

#Edit Award(Musicschool)
class Musicschool_Award_Edit(APIView):
    def get(self,request,pk):
        musicschool_myawards = Gurukulam_Award.objects.get(id=pk,gurukulam=self.request.user.gurukulam)
        musicschool_myaward_serializer = Musicschool_Myaward_Serializer(musicschool_myawards)
        context = {
                    'musicschool_awards':musicschool_myaward_serializer.data,
                }
        return Response(context)

    def put(self, request, pk):
        musicschool_award = Gurukulam_Award.objects.get(id=pk,gurukulam=request.user.gurukulam)
        myawards_serializer = Musicschool_Myaward_Serializer(musicschool_award,data=request.data, partial=True)
        if myawards_serializer.is_valid():
            myawards_serializer.save()
            response_data = {
                'message':myawards_serializer.data,
            }
            return Response(response_data)
        else:
            return Response(myawards_serializer.errors)

#Edit lecture videos(Musicschool)
class Musicschool_Lecture_Videos_Edit(APIView):
    def get(self,request,pk):
        musicschool_lecture_videos = Lecture_Video.objects.get(id=pk,gurukulam=self.request.user.gurukulam)
        musicschool_lecture_videos_serializer = Musicschool_Lecture_Videos_Serializer(musicschool_lecture_videos)
        context = {
                    'musicschool_lecture_videos':musicschool_lecture_videos_serializer.data,
                }
        return Response(context)

    def put(self, request, pk):
        musicschool_lecture_videos = Lecture_Video.objects.get(id=pk,gurukulam=request.user.gurukulam)
        lecture_videos_serializer = Musicschool_Lecture_Videos_Serializer(musicschool_lecture_videos,data=request.data, partial=True)
        if lecture_videos_serializer.is_valid():
            lecture_videos_serializer.save()
            response_data = {
                'message':lecture_videos_serializer.data,
            }
            return Response(response_data)
        else:
            return Response(lecture_videos_serializer.errors)

#Edit Event performer(Event Organizer)
class Event_Performer_Edit(APIView):
    def get(self,request,pk):
        musician = Musician.objects.all()
        troupe = Troupe.objects.all()
        event_performer = Event_Performer.objects.get(id=pk,event_organizer =self.request.user.event_organizer)
        musician_serializer = Musician_Serializer(musician, many=True)
        troupe_serializer = Troupe_Serializer(troupe,many=True)
        event_performer_serializer = Event_Performer_Serializer(event_performer)
        context = {
                    'musicians': musician_serializer.data,
                    'troupes': troupe_serializer.data,
                    'event_performer':event_performer_serializer.data,
                }
        return Response(context)

    def put(self, request, pk):
        event_performer = Event_Performer.objects.get(id=pk,event_organizer=request.user.event_organizer)
        event_performer_serializer = Event_Performer_Serializer(event_performer, data=request.data, partial=True)
        if event_performer_serializer.is_valid():
            event_performer_serializer.save()
            response_data = {
                'message':event_performer_serializer.data,
            }
            return Response(response_data)
        else:
            return Response(event_performer_serializer.errors)

#Edit skill(Band)
class Band_Myskill_Edit(APIView):
    def get(self,request,pk):
        skills = Skill.objects.all()
        band_skills = Troupe_Skill.objects.get(id=pk,troupe=self.request.user.troupe)
        skill_serializer = Skill_Serializer(skills, many=True)
        band_skills_serializer = Band_Skill_Serializer(band_skills)
        context = {
                    'skills': skill_serializer.data,
                    'band_skills':band_skills_serializer.data,
                }
        return Response(context)

    def put(self, request, pk):
        band_skill = Troupe_Skill.objects.get(id=pk,troupe=request.user.troupe)
        skill_serializer = Band_Skill_Serializer(band_skill, data=request.data, partial=True)
        if skill_serializer.is_valid():
            skill_serializer.save()
            response_data = {
                'message':skill_serializer.data,
            }
            return Response(response_data)
        else:
            return Response(skill_serializer.errors)

#Edit key performer(Band)
class Band_Performer_Edit(APIView):
    def get(self,request,pk):
        musician = Musician.objects.all()
        band_performer = Key_Performer.objects.get(id=pk,troupe=self.request.user.troupe)
        musician_serializer = Musician_Serializer(musician, many=True)
        band_performer_serializer = Band_Performer_Serializer(band_performer)
        context = {
                    'musicians': musician_serializer.data,
                    'band_performer':band_performer_serializer.data,
                }
        return Response(context)

    def put(self, request, pk):
        band_performer = Key_Performer.objects.get(id=pk,troupe=request.user.troupe)
        band_performer_serializer = Band_Performer_Serializer(band_performer,data=request.data, partial=True)
        if band_performer_serializer.is_valid():
            band_performer_serializer.save()
            response_data = {
                'message':band_performer_serializer.data,
            }
            return Response(response_data)
        else:
            return Response(band_performer_serializer.errors)

#Add Association_Musicschool(Musician)
class Musician_Association_Myschool_Add(APIView):
    def get(self,request):
        gurukulam = Gurukulam.objects.all()
        gurukulam_serializer = Gurukulam_Serializer(gurukulam,many=True)
        context = {    
                    'gurukulam': gurukulam_serializer.data,              
                }
        return Response(context)

    def post(self, request):
        serializer = Musician_Association_Myschool_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user, musician=request.user.musician, status='A')
            return Response({'message': 'Association added successfully.'}, status=status.HTTP_201_CREATED)
        else:  
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class Report_People_API(APIView):
    def post(self, request, pk):
        reported_user = User.objects.get(id=pk)
        serializer = Report_People_Serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(reported_by=request.user, reported_user=reported_user)
            return Response({'valid': True}, status=status.HTTP_201_CREATED)
        else:
            return Response({'valid': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class People_Filter_API(APIView):

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def post(self, request):
        data = dict()
        skill_category = request.data['skill_category']
        skill = request.data['skill']
        location = request.data['location']       
        name = request.data['name']   
        people_type = request.data['people_type']
       
        user_list = User.objects.filter(groups__name__in=('Musician', 'Band', 'Music School', 'Event Organizer')).exclude(id=request.user.id).order_by('-id')
        
        if name:
            user_list = user_list.filter(Q(last_name__icontains=name) | Q(first_name__icontains=name) | Q(name__icontains=name)).order_by('-id')

    
        if people_type:
            user_list = user_list.filter(groups__id__in=people_type).order_by('-id')        

        if location:
            user_list = user_list.filter(location__id__in=location).order_by('-id')

        if skill:
            user_list = user_list.filter(Q(musician__musician_skill__skill__id__in=skill) | Q(troupe__troupe_skill__skill__id__in=skill)).distinct().order_by('-id')

        paginator = PageNumberPagination()
        # Paginate the queryset
        result_page = paginator.paginate_queryset(user_list, request)        
        # Serialize the paginated data
        serializer = All_People_Serializer(result_page, many=True,context={'request': request})        
        # Return the paginated response
        return paginator.get_paginated_response(serializer.data)
        

    def get(self,request):
        people_types = Group.objects.all().exclude(name__in=['Portal Admin'])
        people_types = Group_Serializer(people_types,many=True)

        locations = Location.objects.all()
        locations = Location_Serializer(locations,many=True)
        skill_categories = Skill_Category.objects.all()
        skill_categories = Skill_Category_Serializer(skill_categories,many=True)
        skills = Skill.objects.all()
        skills = Skill_Serializer_Filter(skills,many=True)
        skills = Skill.objects.all()
        skill_serializer = Skill_Serializer(skills, many=True)
        context = {
                    'skill_categories':skill_categories.data,
                    'skills': skill_serializer.data,
                    'people_types':people_types.data,
                    'locations':locations.data,
                }
        return Response(context)

class Event_Like_Unlike_API(APIView):
    def post(self, request, pk):
        event = Event.objects.get(id=pk)
        user = request.user

        if user in event.user_likes.all():
            event.user_likes.remove(user)
            liked = False
        else:
            event.user_likes.add(user)
            liked = True
        data = {
            'liked': liked,
            'like_count': event.user_likes.count(),
        }
        return Response(data, status=status.HTTP_200_OK)


class Musiclover_API(APIView):
    def get(self, request):
        user = request.user
        user_groups = user.groups.all()
        user_location = user.location

        top_events = Event.objects.annotate(like_count=Count('user_likes')).order_by('-like_count')[:5]
        top_peoples = User.objects.filter(location=user_location, groups__name__in=('Musician', 'Event Organizer', 'Gurukulam', 'Troupe')).exclude(id=user.id)[:5]
        events_at_location = Event.objects.filter(location=user_location)[:5]
        following = UserFollowing.objects.filter(user=user).order_by('-id')[:8]
        liked_events = Event.objects.filter(user_likes=user)
        following_user_ids = UserFollowing.objects.filter(user=request.user).values_list('following_user_id', flat=True)

        organizer_events = Event.objects.filter(
            Q(event_organizer__user__in=following_user_ids) | Q(gurukulam__user__in=following_user_ids)
        )

        participant_events = Event.objects.filter(
            Q(interest__musician__user__in=following_user_ids, interest__status="A") | 
            Q(interest__troupe__user__in=following_user_ids, interest__status="A") |
            Q(invitation__musician__user__in=following_user_ids, invitation__status="A") |
            Q(invitation__troupe__user__in=following_user_ids, invitation__status="A")
        ).distinct()

        recommended_events = list(set(organizer_events) | set(participant_events))

        # Serializing data
        top_events_serializer = EventSerializer2(top_events, many=True,context={'request': request})
        #top_peoples_serializer = UserSerializer(top_peoples, many=True)
        events_at_location_serializer = EventSerializer2(events_at_location, many=True,context={'request': request})
        #following_serializer = UserFollowingSerializer(following, many=True)
        liked_events_serializer = EventSerializer2(liked_events, many=True,context={'request': request})
        recommended_events_serializer = EventSerializer2(recommended_events, many=True,context={'request': request})

        response_data = {
            'top_events': top_events_serializer.data,
            #'top_peoples': top_peoples_serializer.data,
            'events_at_location': events_at_location_serializer.data,
            #'following': following_serializer.data,
            'my_events': liked_events_serializer.data,
            'recommended_events':recommended_events_serializer.data,
        }

        return Response(response_data)
