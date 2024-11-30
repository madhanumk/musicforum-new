#from account.views import musician
from django.core.checks import messages
from django.shortcuts import redirect, render
from .models import Message, Bookmark,Event, Event_Type, Invitation, Interest, Event_Category, Subscription, Subscription_Type, Event_Skill
from .forms import Event_Form
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from account.models import Gurukulam, Musician, Musician_Skill, Post, Skill_Category, Skill_Level, Skill, Location, Troupe, UserFollowing, Event_Organizer, Skill
from django.db.models import Q
import ast
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import datetime as dt
from itertools import chain
from django.core.mail import send_mail
from django.conf import settings 
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import  get_object_or_404
from datetime import date
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import  Event_Serializer1,EventSerializer,Create_Event_Serializer,EventSkill_Serializer,Event_Details_Serializer,Event_Skill_Serializer,Event_Organizer_Serializer,Related_Event_Serializer,Invitation_Serializer,Interest_Serializer,Message_Serializer,Event_Serializer,Organizer_Invitation_Serializer, Organizer_Interest_Serializer,Edit_Event_Serializer,Edit_Event_Serializer1,Troupe_Search_Serializer,Gurukulam_Search_Serializer,Event_Category_Serializer,Location_Serializer, Event_Category_Serializer, Event_Type_Serializer, My_Event_Serializer, Event_Skill_Serializer1
from .models import Event,Event_Skill, Event_Type
from account.serializers import LocationSerializer, SkillSerializer, SkillLevelSerializer, MusicianSerializer, Skill_Category_Serializer, Skill_Serializer_Filter
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from account.serializers import Location_Serializer
from account.models import Location



# Create your views here.
gender_options = (('','Choose Gender'),('M','Male'),('F','Female'),('T','Transgender'),('N','None'))
choose_gender = (('M','Male'),('F','Female'),('T','Transgender'))



def event_details(request,pk):
    event = Event.objects.get(id=pk)
    invitations = Invitation.objects.filter(event=event,status="A")
    interests = Interest.objects.filter(event=event,status="A")

    skill_categories = None
    related_category_events = Event.objects.filter(event_category=event.event_category).exclude(id=pk)[:5]    
    event_created_by_me = False

    if invitations or interests:
        is_any_participant = True
    else:
        is_any_participant = False
    
    related_events = None


    if event.event_organizer:
        related_events = Event.objects.filter(event_organizer=event.event_organizer).exclude(id=pk)[:5]
        skill_categories = Skill_Category.objects.all()
    elif event.gurukulam:
        related_events = Event.objects.filter(gurukulam=event.gurukulam).exclude(id=pk)[:5]
        skill_categories = Skill_Category.objects.all()



    if request.user.is_authenticated:
        user = request.user
        unread_message_count = Message.unread_count(request.user)        
        


        if Event.objects.filter(gurukulam__user=request.user,id=pk).exists():
            event_created_by_me = True
        elif Event.objects.filter(event_organizer__user=request.user,id=pk).exists(): 
            event_created_by_me = True
        

        context = {
            'event' : event, 
            'is_any_participant':is_any_participant,
            'invitations': invitations,
            'interests': interests,
            'related_category_events' : related_category_events,
            'related_events':related_events,
            'skill_categories':skill_categories,
            'unread_message_count':unread_message_count,
            'event_created_by_me':event_created_by_me,
        }
    else:
        unread_message_count = 0
        
        context = {
            'event' : event, 
            'is_any_participant':is_any_participant,
            'invitations': invitations,
            'interests': interests,
            'related_category_events' : related_category_events,
            'related_events':related_events,
            'skill_categories':skill_categories,
            'unread_message_count':unread_message_count,
            'event_created_by_me':event_created_by_me,
        }
    return render(request,'event/event_details.html', context) 



def all_events(request):
    if request.user.groups.filter(name='Event Organizer').exists():
        events = Event.objects.filter(event_organizer=request.user.event_organizer,to_date__lte=datetime.now()).order_by('-from_date')
        invitations  = Invitation.objects.filter(event__event_organizer=request.user.event_organizer,status="A").order_by('-timestamp').distinct()[:10]
        interests = Interest.objects.filter(event__event_organizer=request.user.event_organizer,status="A").order_by('-timestamp').distinct()[:10]
     
    elif request.user.groups.filter(name='Music School').exists():
        events = Event.objects.filter(gurukulam=request.user.gurukulam,to_date__lte=datetime.now()).order_by('-from_date')
        invitations  = Invitation.objects.filter(event__gurukulam=request.user.gurukulam,status="A").order_by('-timestamp').distinct()[:10]
        interests = Interest.objects.filter(event__gurukulam=request.user.gurukulam,status="A").order_by('-timestamp').distinct()[:10]
    
    else:
        HttpResponse("Access Denied")

    skill_categories = Skill_Category.objects.all()
    context = {
        'events' : events, 
        'page' : 'all_event',
        'skill_categories':skill_categories,
        'invitations':invitations,
        'interests':interests,
    }
    return render(request,'event/all_events.html', context) 

@login_required
def bookmark_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, event=event)
    if not created:
        bookmark.delete()
        return JsonResponse({'bookmarked': False})
    return JsonResponse({'bookmarked': True})
    
@login_required
def event_ajax_like_unlike(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user in event.user_likes.all():
        event.user_likes.remove(request.user)
        liked = False
    else:
        event.user_likes.add(request.user)
        liked = True
    
    data = {
        'liked': liked,
        'like_count': event.user_likes.count(),
    }
    return JsonResponse(data)



def ajax_get_skill(request):
    data = dict()
    skill_category_id=request.GET.get('skill_category')   
    event_id=request.GET.get('event_id') 
    if event_id:
        skill_id=Event_Skill.objects.filter(event__id=event_id).values_list('skill__id', flat=True)        
        if skill_id:
            skills = Skill.objects.filter(skill_category__id=skill_category_id).exclude(id__in=skill_id)
        else:
            skills = Skill.objects.filter(skill_category__id=skill_category_id)
    else:
        skills = Skill.objects.filter(skill_category__id=skill_category_id)

    context={            
            'skills' : skills,      
        }
    data['skill'] = render_to_string('event/load_skill.html', context) 

    return JsonResponse(data)
    
@csrf_exempt
def ajax_remove_skill(request,pk):
    user = request.user
    data = dict()    
    data['valid'] = False
    if user.groups.filter(name='Event Organizer').exists():
        event_skill= Event_Skill.objects.get(id=pk,event__event_organizer=user.event_organizer)
        event_skill.delete()
        data['valid'] = True
    elif user.groups.filter(name='Gurukulam').exists():
        event_skill= Event_Skill.objects.get(id=pk,event__gurukulam=user.gurukulam)
        event_skill.delete()
        data['valid'] = True

    return JsonResponse(data)


def ajax_create_event(request):
    user = request.user
    data = dict()
    if request.method == 'POST':
        form = Event_Form(request.POST,request.FILES)
        skill_id = request.POST.getlist("skill")       

        if form.is_valid():
            event = form.save(commit=False)
            if user.groups.filter(name='Event Organizer').exists():
                event.event_organizer = user.event_organizer      
                event.save()
                for skill in skill_id:
                    skill = Skill.objects.get(id=skill)
                    event_skill = Event_Skill.objects.create(event=event,skill=skill)

                place=request.GET.get('place', None)
                if place == "home":
                    events = Event.objects.filter(event_organizer=request.user.event_organizer,to_date__gte=datetime.now())
                elif place == "event_all":
                    events = Event.objects.filter(event_organizer=request.user.event_organizer).order_by('-from_date')
                else:
                    events = Event.objects.filter(event_organizer=request.user.event_organizer,to_date__gte=datetime.now()).order_by('-from_date')

            
            elif user.groups.filter(name='Music School').exists():
                event.gurukulam = user.gurukulam      
                event.save()
                for skill in skill_id:
                    skill = Skill.objects.get(id=skill)
                    event_skill = Event_Skill.objects.create(event=event,skill=skill)

                place=request.GET.get('place', None)
                if place == "home":
                    events = Event.objects.filter(gurukulam=request.user.gurukulam,to_date__gte=datetime.now())
                elif place == "event_all":
                    events = Event.objects.filter(gurukulam=request.user.gurukulam)
                else:
                    events = Event.objects.filter(gurukulam=request.user.gurukulam,to_date__gte=datetime.now())

            data['valid'] = True
            data['html'] = render_to_string('event_organizer/events.html',{'events':events},request)
            
        else:
            print(form.errors.as_data())
            data['valid'] = False
            data['form'] = render_to_string('event/create_event_form.html',{'form':form,'operation':'Add','model_name':"event",},request)
        
    else:
        form = Event_Form()
        data['form'] = render_to_string('event/create_event_form.html',{'form':form,'operation':'Add','model_name':"event",},request)

    return JsonResponse(data)




def view_event(request,pk,type):
    user = request.user
    if type == "invitation":
        status = request.GET.get('status')
        if not status:
            status_filter = ('R','A','S')
        else:
            status_filter = status
        if user.groups.filter(name='Event Organizer').exists():            
            event = Event.objects.get(id=pk,event_organizer=request.user.event_organizer)
            
        elif user.groups.filter(name='Music School').exists():
            event = Event.objects.get(id=pk,gurukulam=request.user.gurukulam)
            
        sent_requests = Invitation.objects.filter(event_id=pk,status__in=status_filter)

        print(sent_requests)

        page = request.GET.get('page', 1)
        '''
             
        paginator = Paginator(sent_requests, 20)
        try:
            sent_requests = paginator.page(page)
        except PageNotAnInteger:
            sent_requests = paginator.page(1)
        except EmptyPage:
            sent_requests = paginator.page(paginator.num_pages)

        '''

        context = {
            'sent_requests' : sent_requests,
            'page' : page,
            'status': status,
            'event':event,
            'object_id' : pk,
            'type': type,
         }
        return render(request,'event/view_event.html', context)

    elif type == "interest":
        status = request.GET.get('status')
        if not status:
            status_filter = ('R','A','S')
        else:
            status_filter = status

        if user.groups.filter(name='Event Organizer').exists():
            event = Event.objects.get(id=pk,event_organizer=request.user.event_organizer)
            received_requests = Interest.objects.filter(event__event_organizer=request.user.event_organizer,event__id=pk,status__in=status_filter)
        elif user.groups.filter(name='Music School').exists():
            event = Event.objects.get(id=pk,gurukulam=request.user.gurukulam)
            received_requests = Interest.objects.filter(event__gurukulam= request.user.gurukulam,event__id=pk,status__in=status_filter)
        
      
        page = request.GET.get('page', 1)
        '''
             
        paginator = Paginator(received_requests, 20)
        try:
            received_requests = paginator.page(page)
        except PageNotAnInteger:
            received_requests = paginator.page(1)
        except EmptyPage:
            received_requests = paginator.page(paginator.num_pages)
        '''
     


        context = {
            'received_requests' : received_requests,
            'page' : page,
            'status': status,
            'object_id' : pk,
            'event' : event,
            'interest_tab_active': True,
            'type': type,
         }
        return render(request,'event/view_event.html', context)


    if request.user.groups.filter(name='Event Organizer').exists():
        event = Event.objects.get(id=pk,event_organizer=request.user.event_organizer)
        received_requests = Interest.objects.filter(event__event_organizer=request.user.event_organizer,event__id=pk)
    elif request.user.groups.filter(name='Gurukulam').exists():
        event = Event.objects.get(id=pk,gurukulam=request.user.gurukulam)
        received_requests = Interest.objects.filter(event__gurukulam= request.user.gurukulam,event__id=pk)

    if request.method == "POST":
        status = request.POST.get('status')
        request_id = request.POST.get('request_id')
        status = Interest.objects.filter(id=request_id).update(status=status)
       
    else:
        pass

    sent_requests = Invitation.objects.filter(event_id=pk)
    tab=request.GET.get('tab', None)
    if tab:
        tab = tab
    else:
        tab = None
    
    context = {
        'event' : event,
        'sent_requests' : sent_requests,
        'object_id' : pk,
        'received_requests':received_requests,
        'tab' :tab,
    }
    
    return render(request,'event/view_event.html', context)

def event_invite(request,pk):
    musician_exclude = [] 
    troupe_exclude =[]
    gurukulam_exclude = []
    user = request.user

    if user.groups.filter(name='Event Organizer').exists():
        event = Event.objects.get(id=pk,event_organizer=request.user.event_organizer)
    elif user.groups.filter(name='Music School').exists():
        event = Event.objects.get(id=pk,gurukulam=request.user.gurukulam)   
        gurukulam_exclude.append(request.user.gurukulam.id) 
    
    skill_levels = Skill_Level.objects.all()
    skills = Skill.objects.all()
    gender = gender_options
    sent_requests = Invitation.objects.filter(event=event)
    get_requests = Interest.objects.filter(event=event)
    event_skills=Event_Skill.objects.filter(event=event).values_list('skill__id', flat=True)
    
    
        

    for sent_request in sent_requests:
        if sent_request.musician:
            musician_exclude.append(sent_request.musician.id)
        elif sent_request.troupe:
            troupe_exclude.append(sent_request.troupe.id)
        else:
            gurukulam_exclude.append(sent_request.gurukulam.id)

    for get_request in get_requests:
        if get_request.musician:
            musician_exclude.append(get_request.musician.id)
        elif get_request.troupe:
            troupe_exclude.append(get_request.troupe.id)


    
    districts = Location.objects.all()

    if musician_exclude and event_skills:
        musicians = Musician.objects.filter(musician_skill__skill__id__in=event_skills).exclude(id__in=musician_exclude).distinct()[:50]
    elif musician_exclude:
        musicians = Musician.objects.all().order_by('?').exclude(id__in=musician_exclude)[:50]
    elif event_skills:
        musicians = Musician.objects.filter(musician_skill__skill__id__in=event_skills).distinct()[:50]
    else:
        musicians = Musician.objects.all().order_by('?')[:50]

    if troupe_exclude and event_skills:
        troups = Troupe.objects.filter(troupe_skill__skill__id__in=event_skills).distinct().exclude(id__in=troupe_exclude)[:50]
    elif troupe_exclude:
        troups = Troupe.objects.all().order_by('?').exclude(id__in=troupe_exclude)[:50]
    elif event_skills:
        troups = Troupe.objects.filter(troupe_skill__skill__id__in=event_skills).distinct()[:50]
    else:
        troups = Troupe.objects.all().order_by('?')[:50]
    

    if  gurukulam_exclude and event_skills:
        gurukulas = Gurukulam.objects.filter(gurukulam_skill__skill__id__in=event_skills).distinct().exclude(id__in=gurukulam_exclude)[:50]
    elif gurukulam_exclude:
        gurukulas = Gurukulam.objects.all().order_by('?').exclude(id__in=gurukulam_exclude)[:50]
    elif event_skills:
        gurukulas = Gurukulam.objects.filter(gurukulam_skill__skill__id__in=event_skills).distinct()[:50]
    else:
        gurukulas = Gurukulam.objects.all().order_by('?')[:50]

    
    context = {

            'event' : event,
            'object_id' : pk,
            'skill_levels' : skill_levels,
            'skills' : skills,
            'gender' : gender,            
            'districts' : districts,
            'musicians': musicians,
            'troups':troups,
            'gurukulas':gurukulas,
          
    }


        
    return render(request,'event_organizer/event_invite.html', context)

def musician_search(request,pk):
    data = dict()
    if request.user.groups.filter(name='Event Organizer').exists():
        event = Event.objects.get(id=pk,event_organizer=request.user.event_organizer)
    elif request.user.groups.filter(name='Gurukulam').exists():
        event = Event.objects.get(id=pk,gurukulam=request.user.gurukulam) 

    sent_requests = Invitation.objects.filter(event__id=pk,musician__isnull=False).values_list('musician__id', flat=True)
    get_requests = Interest.objects.filter(event__id=pk,musician__isnull=False).values_list('musician__id', flat=True)
    musician_exclude_ids_list = chain(sent_requests, get_requests)

    musician_filter = Musician.objects.all().exclude(id__in=musician_exclude_ids_list)
    
    if request.method == 'POST':
            skill_level = [ast.literal_eval(i) for i in request.POST.getlist('skill_level')]        
            skill =   [ast.literal_eval(i) for i in request.POST.getlist('skill')]
            district = [ast.literal_eval(i) for i in request.POST.getlist('district')]
            vocal = request.POST.get('vocal')
            gender =  request.POST.getlist('gender')
            name = request.POST.get('name')


            if skill:
                musician_filter = musician_filter.filter(musician_skill__skill__id__in=skill).distinct()
            if skill_level:                
                musician_filter = musician_filter.filter(musician_skill__skill_level__id__in=skill_level).distinct()             
            
            if district:
                musician_filter = musician_filter.filter(user__district__in=district)
            if gender:
                musician_filter = musician_filter.filter(gender__in=gender)
            if name:
                musician_filter = musician_filter.filter(Q(user__last_name__icontains=name) | Q(user__first_name__icontains=name))

            
            data['valid'] = True


            data['html'] = render_to_string('event/musician_list.html',{'musicians':musician_filter},request)
             
    else:
        data['valid'] = False

    return JsonResponse(data)


def musician_request(request,pk):

    data = dict()
    user= request.user
    if user.groups.filter(name='Event Organizer').exists():
        event = Event.objects.get(id=pk,event_organizer=request.user.event_organizer)
    elif user.groups.filter(name='Gurukulam').exists():
        event = Event.objects.get(id=pk,gurukulam=request.user.gurukulam) 

    if request.method == 'POST':
        musicians = request.POST.getlist('musician')     
        message_text = request.POST.get('message', None)            
   
        for musician in musicians:
            musician_instance= Musician.objects.get(id=musician)
            if not (Invitation.objects.filter(event=event,musician=musician).exists() or Interest.objects.filter(event=event,musician=musician).exists()):
                invitation =Invitation.objects.create(event=event,musician=musician_instance,status="S")
                message_obj = Message(user=request.user, invitation=invitation, text=message_text)
                message_obj.save()

                #email                
                link= str(request.META['HTTP_HOST'])+'/get_message/Invitation/'+str(invitation.id)    
                mail_to = musician_instance.user.email      
                subject = 'Event Invitation - Reg'
                message ='You have been invited to this event'+str(invitation.event)+'; please accept or decline by clicking here. Link: {}'.format(link)     
                send_email(subject,mail_to,message)


        data['valid'] = True


    else:
        data['valid'] = False


    return JsonResponse(data)

def invitation(request,pk):
    sent_request = Invitation.objects.get(id=pk)
    event = Event.objects.get(id=sent_request.event.id)

    if request.method == 'POST':
        status = request.POST.get('status')
        status = Invitation.objects.filter(id=pk).update(status=status)
        return redirect('invitation',pk=pk)      
        
    else:
        pass
        
    context ={
        'event' : event,
        'sent_request': sent_request,
    }   

    return render(request,'event/view_invitation.html', context)


def ajax_skill_filter(request):
    data = dict()
    if request.method == "POST":
        data=dict()
        skill_categories =[ast.literal_eval(i) for i in request.POST.getlist('skill_category')] 
        if skill_categories:
            skills = Skill.objects.filter(skill_category__id__in=skill_categories)
        else:
            skills = Skill.objects.all()
        data['valid'] = True

        data['html'] = render_to_string('event/skill_list.html',{'skills':skills},request)        
        
    else:
        data['valid'] = False 

    return JsonResponse(data)


def search_event(request): 
    user_groups = request.user.groups.all()

    event_filter_type = request.POST.get('event_filter')
    for group in user_groups:
        if group.name == "Artist":
            sent_requests = Interest.objects.filter(musician=request.user.musician).values_list('event__id', flat=True)
            received_requests = Invitation.objects.filter(musician=request.user.musician).values_list('event__id', flat=True)
            user_type = "musician"
            musician_skills = Musician_Skill.objects.filter(musician=request.user.musician).values_list('skill__id', flat=True)
            
        elif group.name == "Band":
            sent_requests = Interest.objects.filter(troupe=request.user.troupe).values_list('event__id', flat=True)
            received_requests = Invitation.objects.filter(troupe=request.user.troupe).values_list('event__id', flat=True)
            user_type = "troupe"
        elif group.name == "Event Organizer":
            sent_requests = None
            received_requests = None
            user_type = "event_organizer"

        elif group.name == "Music School":
            sent_requests = None
            received_requests = None
            user_type = "gurukulam"


    if request.method == "POST":
        data=dict()
        skill =[ast.literal_eval(i) for i in request.POST.getlist('skill')] 
        location =request.POST.get('location')
 
        if location == "Choose Location":
            location = None

        city =request.POST.get('city')
        if city == "Choose City":
            city = None

        event_types =[ast.literal_eval(i) for i in request.POST.getlist('event_type')]
        event_categories =[ast.literal_eval(i) for i in request.POST.getlist('event_category')]
        name =  request.POST.get('name')
        from_date =  request.POST.get('after_date')
        to_date =  request.POST.get('to_date')
        filter_by =  request.POST.get('filterBy',None)
   


        if event_filter_type == "recent":            
            if not sent_requests and  not received_requests:
                event_filter= Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False)
            elif  sent_requests and  not received_requests:
                event_filter = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False).exclude(id__in=sent_requests)
            elif not sent_requests and  received_requests:
                event_filter = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False).exclude(id__in=received_requests)
        
            else:
                event_exclude_ids_list = chain(sent_requests, received_requests)
                event_filter = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False).exclude(id__in=event_exclude_ids_list)
        
        elif event_filter_type == "interest":

            if user_type == "musician":
                interests = list(Musician_Skill.objects.filter(musician=request.user.musician).values_list('skill',flat=True).distinct())
            
            if not sent_requests and  not received_requests:
                event_filter= Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False,event_skill__skill__in=interests).distinct()
            elif  sent_requests and  not received_requests:
                event_filter = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False,event_skill__skill__in=interests).exclude(id__in=sent_requests).distinct()
            elif not sent_requests and  received_requests:
                event_filter = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False,event_skill__skill__in=interests).exclude(id__in=received_requests).distinct()
        
            else:
                event_exclude_ids_list = chain(sent_requests, received_requests)
                event_filter = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False,event_skill__skill__in=interests).exclude(id__in=event_exclude_ids_list).distinct()
        
            
        elif event_filter_type == "i_follow":
            following = UserFollowing.objects.filter(user=request.user,following_user_id__groups__name__in=('Event Organizer','Gurukulam')).values_list('following_user_id__id',flat=True)
 
       
            if not sent_requests and  not received_requests:
                event_filter= Event.objects.filter(Q(gurukulam__user__id__in=following) | Q(event_organizer__user__id__in=following),registration_close_date__gte=datetime.now(),self_reference=False).distinct()
            elif  sent_requests and  not received_requests:
                event_filter = Event.objects.filter(Q(gurukulam__user__id__in=following) | Q(event_organizer__user__id__in=following),registration_close_date__gte=datetime.now(),self_reference=False).exclude(id__in=sent_requests).distinct()
            elif not sent_requests and  received_requests:
                event_filter = Event.objects.filter(Q(gurukulam__user__id__in=following) | Q(event_organizer__user__id__in=following),registration_close_date__gte=datetime.now(),self_reference=False).exclude(id__in=received_requests).distinct()
        
            else:
                event_exclude_ids_list = chain(sent_requests, received_requests)
                event_filter = Event.objects.filter(Q(gurukulam__user__id__in=following) | Q(event_organizer__user__id__in=following),registration_close_date__gte=datetime.now(),self_reference=False).exclude(id__in=event_exclude_ids_list).distinct()
        

        
        if skill:
            event_filter = event_filter.filter(event_skill__skill__id__in=skill).distinct()
        if location:
   
            event_filter = event_filter.filter(location__id=location)

        if event_types:
            event_filter = event_filter.filter(event_type__id__in=event_types)
        if event_categories:
            event_filter = event_filter.filter(event_category__id__in=event_categories)
        if name:
            event_filter = event_filter.filter(name__icontains=name)
        if from_date:
          
            event_filter = event_filter.filter(from_date__gte=from_date)
        if to_date:
            event_filter = event_filter.filter(to_date__lte=to_date)

        if filter_by:
           
            todaydate = date.today()
            if filter_by == "today":
                event_filter = event_filter.filter(from_date__date__range=(todaydate, todaydate)).distinct()
            elif filter_by == "thisweek":
                event_filter = event_filter.filter(from_date__date__range=(todaydate, todaydate + timedelta(days=7))).distinct()

        event_filter = event_filter.order_by('-id')[:100]
        data['valid'] = True
        data['html'] = render_to_string('event/event_list.html',{'events':event_filter,'user_type':user_type,},request)
    else:
        pass
    
    return JsonResponse(data)
    

@csrf_exempt
def event_request_send(request):   
    data = dict()
    if request.method == 'POST':
        events = request.POST.get('event')
        events = [int(events)]
        message_text = request.POST.get('message', None) 

        if request.user.groups.filter(name='Artist').exists(): 
            data['user'] ="Musician"
            for event in events:
                event_instance= Event.objects.get(id=event)

                if not (Invitation.objects.filter(event=event,musician=request.user.musician).exists() or Interest.objects.filter(event=event,musician=request.user.musician).exists()):
                    interest =Interest.objects.create(event=event_instance,musician=request.user.musician,status="S")
                    message_obj = Message(user=request.user, interest=interest, text=message_text)
                    message_obj.save()

                    #email                    
                    link= str(request.META['HTTP_HOST'])+'/get_message/Interest/'+str(interest.id)
                    if  event_instance.event_organizer:
                        mail_to = event_instance.event_organizer.user.email
                    else:
                        mail_to = event_instance.gurukulam.user.email       

                    subject = 'Event Intrest - Reg'
                    message = str(request.user) +' has expressed interest in this event('+str( event_instance)+'); please accept or reject his offer by clicking here. Link: {}'.format(link)     
                    #send_email(subject,mail_to,message)

                

        elif request.user.groups.filter(name='Band').exists():
             data['user'] ="Troupe"
             for event in events:
                event_instance= Event.objects.get(id=event)
                if not (Invitation.objects.filter(event=event,troupe=request.user.troupe).exists() or Interest.objects.filter(event=event,troupe=request.user.troupe).exists()):
                    interest =Interest.objects.create(event=event_instance,troupe=request.user.troupe,status="S")
                    message_obj = Message(user=request.user, interest=interest, text=message_text)
                    message_obj.save()

                    #email                    
                    link= str(request.META['HTTP_HOST'])+'/get_message/Interest/'+str(interest.id)
                    if  event_instance.event_organizer:
                        mail_to = event_instance.event_organizer.user.email
                    else:
                        mail_to = event_instance.gurukulam.user.email       

                    subject = 'Event Intrest - Reg'
                    message = str(request.user) +' has expressed interest in this event('+str( event_instance)+'); please accept or reject his offer by clicking here. Link: {}'.format(link)     
                    #send_email(subject,mail_to,message)

        data['valid'] = True

    else:
        data['valid'] = False

    return JsonResponse(data)


def troupe_request(request,pk):
    data = dict()
    if request.user.groups.filter(name='Event Organizer').exists(): 
        event = Event.objects.get(id=pk,event_organizer=request.user.event_organizer)
    if request.user.groups.filter(name='Gurukulam').exists(): 
        event = Event.objects.get(id=pk,gurukulam=request.user.gurukulam) 

    if request.method == 'POST':
        troupes = request.POST.getlist('troupe')  
        message_text = request.POST.get('message', None)              

        for troupe in troupes:
            troupe_instance= Troupe.objects.get(id=troupe)

            if not (Invitation.objects.filter(event=event,troupe=troupe).exists() or Interest.objects.filter(event=event,troupe=troupe).exists()):
                invitation =Invitation.objects.create(event=event,troupe=troupe_instance,status="S")
                message_obj = Message(user=request.user, invitation=invitation, text=message_text)
                message_obj.save()

                #email                
                link= str(request.META['HTTP_HOST'])+'/get_message/Invitation/'+str(invitation.id)    
                mail_to = troupe_instance.user.email      
                subject = 'Event Invitation - Reg'
                message ='You have been invited to this event'+str(invitation.event)+'; please accept or decline by clicking here. Link: {}'.format(link)     
                send_email(subject,mail_to,message)
                

            
       
        data['valid'] = True


    else:
        data['valid'] = False


    return JsonResponse(data)


def troupe_search(request,pk):
    
    data = dict()
    if request.user.groups.filter(name='Event Organizer').exists(): 
        event = Event.objects.get(id=pk,event_organizer=request.user.event_organizer)
    if request.user.groups.filter(name='Gurukulam').exists(): 
        event = Event.objects.get(id=pk,gurukulam=request.user.gurukulam) 

    sent_requests = Invitation.objects.filter(event__id=pk,troupe__isnull=False).values_list('troupe__id', flat=True)
    get_requests = Interest.objects.filter(troupe__isnull=False,event__id=pk).values_list('troupe__id', flat=True)
    troupe_exclude_list = chain(sent_requests, get_requests)
    
    if request.method == 'POST':  
            skill = [ast.literal_eval(i) for i in request.POST.getlist('skill')]
            district = [ast.literal_eval(i) for i in request.POST.getlist('location')]
            name = request.POST.get('name')
             
            troupes_list  = Troupe.objects.exclude(id__in=troupe_exclude_list).distinct()
    
            if skill:
                troupes_list = troupes_list.filter(troupe_skill__skill__id__in=skill)            
            if district:
                troupes_list = troupes_list.filter(user__location__id__in=district)
            if name:
                troupes_list = troupes_list.filter(user__name__icontains=name)

            troupes = troupes_list 

            if len(name) == 0 and  len(skill) == 0 and len(district) == 0:
                troupes = None
                

            data['valid'] = True

            print(troupes)


            data['html'] = render_to_string('event/troupe_list.html',{'troupes':troupes},request)
             
    else:
        data['valid'] = False

    return JsonResponse(data)


def gurukulam_search(request,pk):
    
    data = dict()
    if request.user.groups.filter(name='Event Organizer').exists():
        event = Event.objects.get(id=pk,event_organizer=request.user.event_organizer)
        gurukulam_id =[]
    elif request.user.groups.filter(name='Gurukulam').exists():
        event = Event.objects.get(id=pk,gurukulam=request.user.gurukulam) 
        gurukulam_id = request.user.gurukulam.id
    
    
    sent_requests = Invitation.objects.filter(event=event,gurukulam__isnull=False).values_list('gurukulam__id', flat=True)
    get_requests = Interest.objects.filter(event=event,event__gurukulam__isnull=False).values_list('event__gurukulam__id', flat=True)
    
    gurukulam_exclude_list = chain(sent_requests, get_requests,gurukulam_id)
    
    if request.method == 'POST':  

            skill = [ast.literal_eval(i) for i in request.POST.getlist('skill')]
            district = [ast.literal_eval(i) for i in request.POST.getlist('district')]
            name = request.POST.get('name')
            print(name)

            gurukulam_filter  = Gurukulam.objects.all()
    
            if skill: 
                gurukulam_filter  = gurukulam_filter.filter(gurukulam_skill__skill__id__in=skill).distinct()
            if district:
                gurukulam_filter  = gurukulam_filter.filter(user__district__id__in=district)

            if name:
                gurukulam_filter  = gurukulam_filter.filter(Q(user__last_name__icontains=name) | Q(user__first_name__icontains=name))

    
            data['valid'] = True

            data['html'] = render_to_string('event/gurukulam_list.html',{'gurukulas':gurukulam_filter},request)
             
    else:
        data['valid'] = False

    return JsonResponse(data)


def gurukulam_request(request,pk):
    data = dict()
    user=request.user
    if user.groups.filter(name='Event Organizer').exists():
        event = Event.objects.get(id=pk,event_organizer=request.user.event_organizer)
    elif user.groups.filter(name='Gurukulam').exists():
        event = Event.objects.get(id=pk,gurukulam=request.user.gurukulam) 

    if request.method == 'POST':
        gurukulas = request.POST.getlist('gurukulam')   
        message_text = request.POST.get('message', None)
           

        for gurukulam in gurukulas:
            gurukulam_instance= Gurukulam.objects.get(id=gurukulam)
            invitation =Invitation.objects.create(event=event,gurukulam=gurukulam_instance,status="S")  
            message_obj = Message(user=request.user, invitation=invitation, text=message_text)
            message_obj.save()

            #email                
            link= str(request.META['HTTP_HOST'])+'/get_message/Invitation/'+str(invitation.id)    
            mail_to = gurukulam_instance.user.email      
            subject = 'Event Invitation - Reg'
            message ='You have been invited to this event'+str(invitation.event)+'; please accept or decline by clicking here. Link: {}'.format(link)     
            send_email(subject,mail_to,message)



        data['valid'] = True


    else:
        data['valid'] = False


    return JsonResponse(data)


def get_message(request,messagetype, pk):
    
    if messagetype == 'Invitation':
        invitation = Invitation.objects.get(id=pk)
        #update read status
        Message.objects.filter(invitation=invitation,unread=True).exclude(user=request.user).update(unread=False)
        if authorize_invitation(request,invitation):

            context = {
            'invitation':invitation,
            }
            return render(request,'invitation.html',context)
    elif messagetype == 'Interest':
        interest = Interest.objects.get(id=pk)
        Message.objects.filter(interest=interest,unread=True).exclude(user=request.user).update(unread=False)
        if authorize_interest(request,interest):
            context = {
            'interest':interest,
            }
            return render(request,'interest.html',context)
    return HttpResponse("Error")


def put_message(request):
    data = dict()
    messagetype = request.GET.get('messagetype')
    pk = request.GET.get('pk')
    message = request.GET.get('message')
    status = request.GET.get('status')

   
    if messagetype == 'Invitation':
        invitation = Invitation.objects.get(id=pk)
        if authorize_invitation(request,invitation):
            message_obj = Message(user=request.user, invitation=invitation, text=message)
            message_obj.save()
            if status and status == "A":
                status = Invitation.objects.filter(id=pk).update(status=status)
                if invitation.musician:
                    post =Post.objects.create(location=invitation.event.location,user=invitation.musician.user,content='I am going to participate <a  href="/event_details/' + str(invitation.event.id) + '/">' + str(invitation.event)  +  '</a> <br> <img class="img-fluid" src="'+invitation.event.poster_image.url+'">' )
                elif invitation.troupe:
                    post =Post.objects.create(location=invitation.event.location,user=invitation.troupe.user,content='I am going to participate <a  href="/event_details/' + str(invitation.event.id) + '/">' + str(invitation.event)  +  '</a> <br> <img class="img-fluid" src="'+invitation.event.poster_image.url+'">' )
                elif invitation.gurukulam:
                    post =Post.objects.create(location=invitation.event.location,user=invitation.gurukulam.user,content='I am going to participate <a  href="/event_details/' + str(invitation.event.id) + '/">' + str(invitation.event)  +  '</a> <br> <img class="img-fluid" src="'+invitation.event.poster_image.url+'">'  )


            elif status:
                status = Invitation.objects.filter(id=pk).update(status=status)


            context = {
                'obj':invitation,
                'user' : request.user,
            }
            data['html'] = render_to_string('message.html',context)
        else:
            data['html'] = "Error"
    elif messagetype == 'Interest':
        interest = Interest.objects.get(id=pk)
        if authorize_interest(request,interest):
            message_obj = Message(user=request.user, interest=interest, text=message)
            message_obj.save()

            if status and status == "A":
                status = Interest.objects.filter(id=pk).update(status="A")
                if interest.musician:
                    post =Post.objects.create(location=interest.event.location,user=interest.musician.user,content='I am going to participate <a  href="/event_details/' + str(interest.event.id) + '/">' + str(interest.event)  +  '</a> <br> <img class="img-fluid" src="'+interest.event.poster_image.url+'">' )
                elif interest.troupe:
                    post =Post.objects.create(location=interest.event.location,user=interest.troupe.user,content='I am going to participate <a  href="/event_details/' + str(interest.event.id) + '/">' + str(interest.event)  +  '</a> <br> <img class="img-fluid" src="'+interest.event.poster_image.url+'">' )
              
       
            elif status:                
                status = Interest.objects.filter(id=pk).update(status="R")
                

            context = {
                'obj':interest,
                'user' : request.user,
            }
            data['html'] = render_to_string('message.html',context)
        else:
            data['html'] = "Error"
    return JsonResponse(data)


def authorize_invitation(request,invitation):

    
    if request.user.groups.filter(name='Event Organizer').exists() and request.user ==   invitation.event.event_organizer.user:
        return True
    elif request.user.groups.filter(name='Music School').exists() and request.user ==  invitation.event.gurukulam.user:
        return True
    elif invitation.musician!=None and invitation.musician.user == request.user:
        
        return True
    elif invitation.troupe != None and invitation.troupe.user == request.user:
        return True
    elif invitation.gurukulam != None and invitation.event.gurukulam.user == request.user:
        return True
    else:
        return False

def authorize_interest(request,interest):
    
    if request.user.groups.filter(name='Event Organizer').exists() and request.user == interest.event.event_organizer.user:
        return True
    elif request.user.groups.filter(name='Music School').exists() and request.user == interest.event.gurukulam.user:
        return True
  
    elif interest.musician!=None and interest.musician.user == request.user:
        
        return True
    elif interest.troupe != None and interest.troupe.user == request.user:
        return True
   
    else:
        return False


def delete_message(request):
    pk = request.GET.get('pk')
    message = Message.objects.get(id=pk)
    invitation = message.invitation
    interset = message.interest
    if message.user == request.user:
        message.delete()
        if message.invitation != None:
            obj = Invitation.objects.get(id=message.invitation.id)
        elif message.interest != None:
            obj = Interest.objects.get(id=message.invitation.id)
    
        context = {
                'obj':obj
            }
        data['html'] = render_to_string('message.html',context)
    
    else:
        data['html'] = "Error"
    return JsonResponse(data)


def request_delete(request,delete_type, pk):
    data = dict()    
    
    if delete_type == 'Invitation':        
        invitation = Invitation.objects.get(id=pk)
        user=request.user
        if user.groups.filter(name='Event Organizer').exists() and invitation.event.event_organizer == user.event_organizer:
            invitation.delete()
            data['valid'] = True
            
        elif user.groups.filter(name='Gurukulam').exists() and invitation.event.gurukulam == user.gurukulam:
            invitation.delete()
            data['valid'] = True
        else:
            data['valid'] = False
        
        return JsonResponse(data)

            
    elif delete_type == 'Interest':
        interest = Interest.objects.get(id=pk)
        user=request.user
        if user.groups.filter(name='Artist').exists() and interest.musician.user == user:
            interest.delete()
            data['valid'] = True
            
        elif user.groups.filter(name='Troupe').exists() and interest.event.troupe.user == user:
            interest.delete()
            data['valid'] = True
        else:
            data['valid'] = False
        
        return JsonResponse(data)


def send_email(subject,mail_to,message):
    email_from = settings.EMAIL_HOST_USER 
    recipient_list = [ mail_to, ] 
    send_mail( subject, message, email_from, recipient_list )
    return "Done"


def recent_events(request):
    user = request.user
    if user.groups.filter(name='Event Organizer').exists():
        events = Event.objects.filter(event_organizer=request.user.event_organizer,to_date__gte=datetime.now()).order_by('-from_date')
        skill_categories = Skill_Category.objects.all()
        invitations  = Invitation.objects.filter(event__event_organizer=request.user.event_organizer,status="A").order_by('-timestamp').distinct()[:4]
        interests = Interest.objects.filter(event__event_organizer=request.user.event_organizer,status="A").order_by('-timestamp').distinct()[:4]
        context = {
            'page'   : 'recent_event',
            'events' : events,
            'skill_categories':skill_categories,
            'invitations':invitations,
            'interests':interests,


          }
        return render(request,'event/recent_events.html', context)
    elif user.groups.filter(name='Music School').exists():
        events = Event.objects.filter(gurukulam=request.user.gurukulam,to_date__gte=datetime.now()).order_by('-from_date')
        skill_categories = Skill_Category.objects.all()
        invitations  = Invitation.objects.filter(event__gurukulam=request.user.gurukulam,status="A").order_by('-timestamp').distinct()[:4]
        interests = Interest.objects.filter(event__gurukulam=request.user.gurukulam,status="A").order_by('-timestamp').distinct()[:4]
    

        context = {
            'events' : events,
            'page'   : 'home',
            'skill_categories':skill_categories,
            'invitations':invitations,
            'interests':interests,

          }
        return render(request,'event/recent_events.html', context)
    



def get_event_message(request,messagetype, pk):
    data = dict()
    
    if messagetype == 'Invitation':
        invitation = Invitation.objects.get(id=pk)
        #update read status
        Message.objects.filter(invitation=invitation,unread=True).exclude(user=request.user).update(unread=False)
        if authorize_invitation(request,invitation):

            context = {
            'invitation':invitation,
            }
            data['has_access'] = True

            data['html'] = render_to_string('invitation.html',context,request)
            return JsonResponse(data)
    elif messagetype == 'Interest':
        interest = Interest.objects.get(id=pk)
        Message.objects.filter(interest=interest,unread=True).exclude(user=request.user).update(unread=False)
        if authorize_interest(request,interest):
            context = {
            'interest':interest,
            }           
            data['html'] = render_to_string('interest.html',context,request)
            data['has_access'] = True        
            return JsonResponse(data)
    
    data['has_access'] = False
    return JsonResponse(data)


@login_required
def create_event(request):
    skill_categories = Skill_Category.objects.all()

    event_categories = Event_Category.objects.all()
    skills = Skill.objects.all()
    locations = Location.objects.all()
    event_types = Event_Type.objects.all()
   
    musicians = Musician.objects.filter().exclude(user=request.user)[:5]
    troupes = Troupe.objects.filter().exclude(user=request.user)[:5]
    gurukulas = Gurukulam.objects.filter().exclude(user=request.user)[:5]
    skill_levels = Skill_Level.objects.all()

    if request.method == 'POST':
        form = Event_Form(request.POST,request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.host = request.user
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event_details', pk=event.pk)
    else:
        form = Event_Form()
    return render(request, 'event_organizer/event_creation.html', {'operation':"Add",'form': form,'skill_categories':skill_categories,'skill_levels':skill_levels,'gurukulas':gurukulas,'troupes':troupes,'musicians':musicians,'locations':locations,'skills':skills,})

@login_required
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = Event_Form(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
         
            event.save()
            #messages.success(request, 'Event updated successfully.')
            return redirect('recent_events')
    else:
        form = Event_Form(instance=event)
    return render(request, 'event/edit_event.html', {'form': form})



#apiviews
#Events View
class Event_View(APIView):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


    def get(self, request):
        user_groups = request.user.groups.all()
        user = request.user

        for group in user_groups:
            if group.name == "Musician":       
                sent_requests = Interest.objects.filter(musician=request.user.musician).values_list('event__id', flat=True)
                received_requests = Invitation.objects.filter(musician=request.user.musician).values_list('event__id', flat=True)
                musician_skills = Musician_Skill.objects.filter(musician=request.user.musician).values_list('skill__id', flat=True)    
                if not sent_requests and  not received_requests:
                    events = Event.objects.filter(location=user.location,registration_close_date__gte=datetime.now(),event_skill__skill__id__in=musician_skills,self_reference=False).distinct()[:50]
                elif  sent_requests and  not received_requests:
                    events = Event.objects.filter(location=user.location,registration_close_date__gte=datetime.now(),event_skill__skill__id__in=musician_skills,self_reference=False).distinct().exclude(id__in=sent_requests)[:50]
                elif not sent_requests and  received_requests:
                    events = Event.objects.filter(location=user.location,registration_close_date__gte=datetime.now(),event_skill__skill__id__in=musician_skills,self_reference=False).distinct().exclude(id__in=received_requests)[:50]    
                else:
                    event_exclude_ids_list = chain(sent_requests, received_requests)
                    events = Event.objects.filter(location=user.location,registration_close_date__gte=datetime.now(),event_skill__skill__id__in=musician_skills,self_reference=False).distinct().exclude(id__in=event_exclude_ids_list)[:50]

            elif group.name == "Event Organizer":
                form = Event_Form()            
                events = Event.objects.filter(location=user.location,registration_close_date__gte=datetime.now())[:20]
                 
            elif group.name == "Music School":
                events = Event.objects.filter(location=user.location,registration_close_date__gte=datetime.now()).order_by('-id')[:30]
                form = Event_Form()      
            elif group.name == "Band":
                events = Event.objects.filter(location=user.location,registration_close_date__gte=datetime.now(),self_reference=False).exclude(Q(invitation__troupe=request.user.troupe) | Q(interest__troupe=request.user.troupe))
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(events, request) 
        serializer = EventSerializer(result_page, many=True,context={'request': request})
        return paginator.get_paginated_response(serializer.data)

#Sending Interest for Events
class Send_Interest_Api(APIView):
    def post(self, request, format=None):
        event_ids = request.data['event_ids'] 
        message = request.data['message']
        status = "S"
        events = event_ids
        already_sent_events = []
        new_events = []
        if request.user.groups.filter(name='Artist').exists():   
            for event in events:
                event_instance= Event.objects.get(id=event)
                if not (Invitation.objects.filter(event=event,musician=request.user.musician).exists() or Interest.objects.filter(event=event,musician=request.user.musician).exists()):
                    interest =Interest.objects.create(event=event_instance,musician=request.user.musician,status="S")
                    message_obj = Message(user=request.user, interest=interest, text=message)
                    message_obj.save()
                    new_events.append(event_instance.name)
                else:
                    already_sent_events.append(event_instance.name)
        elif request.user.groups.filter(name='Band').exists():   
             for event in events:
                event_instance= Event.objects.get(id=event)
                if not (Invitation.objects.filter(event=event,troupe=request.user.troupe).exists() or Interest.objects.filter(event=event,troupe=request.user.troupe).exists()):
                    interest =Interest.objects.create(event=event_instance,troupe=request.user.troupe,status="S")
                    message_obj = Message(user=request.user, interest=interest, text=message)
                    message_obj.save()
                    new_events.append(event_instance.name)
                else:
                    already_sent_events.append(event_instance.name)
        response_message = ''
        if already_sent_events:
            response_message += 'Interest already sent for the following events: {}. '.format(', '.join(already_sent_events))
        if new_events:
            response_message += 'Interest sent successfully for the following new events: {}. '.format(', '.join(new_events))

        return Response({'message': response_message})

#Create New Event
class Create_Event_Api(APIView):
    def post(self, request):
        status = request.data['auto_accept']
 
        event_serializer = Create_Event_Serializer(data=request.data) 
        skill_data = request.POST.getlist('skill')
        skill_data = eval(skill_data[0])

        musician_data = request.POST.getlist('musician')
        musician_data = eval(musician_data[0])

        band_data = request.POST.getlist('band')
        band_data = eval(band_data[0])

        music_school_data = request.POST.getlist('music_school')
        music_school_data = eval(music_school_data[0])

        auto_accept = request.data['auto_accept']
        message = request.data['message']




        skill_serializer = EventSkill_Serializer(data=request.data, many=True)
        #skill_serializer = EventSkill_Serializer(data=request.data)
        if event_serializer.is_valid():
            #event_skill = request.data.get('skill')  
            event = event_serializer.save()

            if request.user.groups.filter(name='Event Organizer').exists():
                event.event_organizer = request.user.event_organizer
            else:
                event.gurukulam = request.user.gurukulam

            event.save()


            if skill_data:
                for skill in skill_data:
                    try:
                        skill = Skill.objects.get(id=skill)
                        skill = Event_Skill.objects.create(event=event,skill=skill)
                    except:
                        pass   

            for musician in  musician_data:
                invitation = Invitation.objects.create(event=event,status=status,musician=Musician.objects.get(id=musician))
                message_obj = Message(user=request.user, invitation=invitation, text=message)
                message_obj.save()
                    

            for gurukulam in  music_school_data:
                invitation = Invitation.objects.create(event=event,status=status,gurukulam=Gurukulam.objects.get(id=gurukulam))
                message_obj = Message(user=request.user, invitation=invitation, text=message)
                message_obj.save()

            for troupe in  band_data:
                invitation = Invitation.objects.create(event=event,status=status,troupe=Troupe.objects.get(id=troupe))
                message_obj = Message(user=request.user, invitation=invitation, text=message)
                message_obj.save()
            
            response_data = {
                'event_id': event.id,
                'message': 'Event created successfully',
              
            }
            return Response(response_data)

        else:
            errors = dict()
            print(errors)

            if event_serializer.errors:
                errors['event_error'] = event_serializer.errors

            if not skill_serializer.is_valid():
                errors['skill_error'] = skill_serializer.errors

            return Response(errors)

    def get(self,request):

        event_categories = Event_Category.objects.all()
        event_categories  = Event_Category_Serializer(event_categories,many=True)
        
        event_types = Event_Type.objects.all()

        event_types  = Event_Type_Serializer(event_types,many=True)

        locations = Location.objects.all()
        locations = Location_Serializer(locations,many=True)
        
        skill_categories = Skill_Category.objects.all()
        skill_categories = Skill_Category_Serializer(skill_categories,many=True)
        skills  = Skill.objects.all()
        skills  = Skill_Serializer_Filter(skills,many=True)


        context = {
            "event_categories":event_categories.data,
            "event_types":event_types.data,
            "locations":locations.data,
            "skill_categories":skill_categories.data,
            "skills":skills.data
        }
        return Response(context)





#Event Detail View
class Event_Detail_Api(APIView):
    def get(self, request, pk):
        try:
            event = Event.objects.get(id=pk)
            skills = Event_Skill.objects.filter(event=event)
            #organizer = Event_Organizer.objects.get(id=event.event_organizer.id)
            #gurukulam = Gurukulam.objects.get(id=event.gurukulam.id)
            if event.event_organizer:
                more_events_by = Event.objects.filter(event_organizer=event.event_organizer).exclude(id=pk)[:5]
                organizer = Event_Organizer.objects.get(id=event.event_organizer.id)
            
            elif event.gurukulam:
                more_events_by = Event.objects.filter(gurukulam=event.gurukulam).exclude(id=pk)[:5]
                organizer = None
                
           #more_events_by = Event.objects.filter(event_organizer=event.event_organizer).exclude(id=pk)[:5]
            related_events = Event.objects.filter(event_category=event.event_category).exclude(id=pk)[:5] 
            event_detail = Event_Details_Serializer(event,context={'request': request})
            event_skill = Event_Skill_Serializer(skills,many=True)
            event_organizer = Event_Organizer_Serializer(organizer)
            more_event_by =  Related_Event_Serializer(more_events_by,many=True,context={'request': request})
            related_event = Related_Event_Serializer(related_events,many=True,context={'request': request})
            #mobile_no = event.event_organizer.user.mobile_no
            #email = event.event_organizer.user.email
            response_data = {
                    'event': event_detail.data,
                    'skill': event_skill.data,
                    'organizer': {
                    #'mobile_no': mobile_no,
                    #'email': email,
                },
                    'more_events_by':more_event_by.data,
                    'related_events': related_event.data,
                    #'created_by_me': event.event_organizer.user == request.user
                }
            return Response(response_data)
        except Event.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)


# Event Invitations and Interest
class Event_Inbox_Api(APIView):

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get(self, request, type):
        user = request.user
        if type == "invitation":
            status = request.GET.get('status')
            if not status:
                status_filter = ('R', 'A', 'S')
            else:
                status_filter = status

            interest_count = interest_accepted_count = interest_rejected_count = pending_interest_count = invitation_count = accepted_invitation_count = rejected_invitation_count = pending_invitation_count = 0

                
            if user.groups.filter(name='Artist').exists():
                invitations = Invitation.objects.filter(musician=user.musician, status__in=status_filter)
                interest_count = Interest.objects.filter(musician=user.musician).count() 
                interest_accepted_count= Interest.objects.filter(status="A",musician=user.musician).count()
                interest_rejected_count = Interest.objects.filter(status="R",musician=user.musician).count()
                pending_interest_count = Interest.objects.filter(status="S",musician=user.musician).count()

                invitation_count = Invitation.objects.filter(musician=user.musician).count()
                accepted_invitation_count = Invitation.objects.filter(musician=user.musician,status="A").count()
                rejected_invitation_count = Invitation.objects.filter(musician=user.musician,status="R").count()
                pending_invitation_count = Invitation.objects.filter(musician=user.musician,status="S").count()



            elif user.groups.filter(name='Band').exists():
                invitations = Invitation.objects.filter(troupe=user.troupe, status__in=status_filter)

                interest_count  = Interest.objects.filter(troupe=user.troupe).count()
                interest_accepted_count= Interest.objects.filter(status="A",troupe=user.troupe).count()
                interest_rejected_count = Interest.objects.filter(status="R",troupe=user.troupe).count()
                pending_interest_count = Interest.objects.filter(status="S",troupe=user.troupe).count()

                invitation_count = Invitation.objects.filter(troupe=user.troupe).count()
                accepted_invitation_count = Invitation.objects.filter(troupe=user.troupe,status="A").count()
                rejected_invitation_count = Invitation.objects.filter(troupe=user.troupe,status="R").count()
                pending_invitation_count = Invitation.objects.filter(troupe=user.troupe,status="S").count()


            
            serializer = Invitation_Serializer(invitations, many=True)

            paginator = PageNumberPagination()
            # Paginate the queryset
            result_page = paginator.paginate_queryset(invitations, request)        
            # Serialize the paginated data
            serializer = Invitation_Serializer(result_page, many=True,context={'request': request})        
            # Return the paginated response
            serializer = paginator.get_paginated_response(serializer.data)

            context  = {
                'invitation':serializer.data,
                'interest_count':interest_count,
                'interest_accepted_count':interest_accepted_count,
                'interest_rejected_count':interest_rejected_count,
                'pending_interest_count':pending_interest_count,
                'invitation_count':invitation_count,
                'accepted_invitation_count':accepted_invitation_count,
                'rejected_invitation_count':rejected_invitation_count,
                'pending_invitation_count':pending_invitation_count,
            }
            
            return Response(context)

        elif type == "interest":
            status = request.GET.get('status')
            if not status:
                status_filter = ('R', 'A', 'S')
            else:
                status_filter = status
            interest_count = interest_accepted_count = interest_rejected_count = pending_interest_count = invitation_count = accepted_invitation_count = rejected_invitation_count = pending_invitation_count = 0
            if user.groups.filter(name='Artist').exists():
                interests = Interest.objects.filter(musician=user.musician, status__in=status_filter)

                interest_accepted_count= Interest.objects.filter(status="A",musician=user.musician).count()
                interest_rejected_count = Interest.objects.filter(status="R",musician=user.musician).count()
                pending_interest_count = Interest.objects.filter(status="S",musician=user.musician).count()

                invitation_count = Invitation.objects.filter(musician=user.musician).count()
                accepted_invitation_count = Invitation.objects.filter(musician=user.musician,status="A").count()
                rejected_invitation_count = Invitation.objects.filter(musician=user.musician,status="R").count()
                pending_invitation_count = Invitation.objects.filter(musician=user.musician,status="S").count()

            elif user.groups.filter(name='Band').exists():
                interests = Interest.objects.filter(troupe=user.troupe, status__in=status_filter)

                interest_count  = Interest.objects.filter(troupe=user.troupe).count()
                interest_accepted_count= Interest.objects.filter(status="A",troupe=user.troupe).count()
                interest_rejected_count = Interest.objects.filter(status="R",troupe=user.troupe).count()
                pending_interest_count = Interest.objects.filter(status="S",troupe=user.troupe).count()

                invitation_count = Invitation.objects.filter(troupe=user.troupe).count()
                accepted_invitation_count = Invitation.objects.filter(troupe=user.troupe,status="A").count()
                rejected_invitation_count = Invitation.objects.filter(troupe=user.troupe,status="R").count()
                pending_invitation_count = Invitation.objects.filter(troupe=user.troupe,status="S").count()

            
            
            
            paginator = PageNumberPagination()
            # Paginate the queryset
            result_page = paginator.paginate_queryset(interests, request)        
            # Serialize the paginated data
            serializer = Interest_Serializer(result_page, many=True,context={'request': request})        
            # Return the paginated response
            serializer = paginator.get_paginated_response(serializer.data)
            
            context  = {
                'interest':serializer.data,
                'interest_count':interest_count,
                'interest_accepted_count':interest_accepted_count,
                'interest_rejected_count':interest_rejected_count,
                'pending_interest_count':pending_interest_count,
                'invitation_count':invitation_count,
                'accepted_invitation_count':accepted_invitation_count,
                'rejected_invitation_count':rejected_invitation_count,
                'pending_invitation_count':pending_invitation_count,
            }
            
            return Response(context)
        

    def post(self, request, type):
        user = request.user

        name = request.data['name']
        organizer_name = name 


        if type == "invitation":
            status = request.GET.get('status')
            if not status:
                status_filter = ('R', 'A', 'S')
            else:
                status_filter = status
            if user.groups.filter(name='Artist').exists():
                invitations = Invitation.objects.filter(musician=user.musician, status__in=status_filter)
            elif user.groups.filter(name='Band').exists():
                invitations = Invitation.objects.filter(troupe=user.troupe, status__in=status_filter)


            if organizer_name:
                org_invitations = list(invitations.filter(Q(event__name__icontains=name) | Q(event__event_organizer__user__last_name__icontains=name) | 
                                                        Q(event__event_organizer__user__first_name__icontains=name)).distinct().values_list("id", flat=True))

                gur_invitations = list(invitations.filter(Q(event__name__icontains=name) | Q(event__gurukulam__user__last_name__icontains=name) | 
                                                        Q(event__gurukulam__user__first_name__icontains=name)).distinct().values_list("id", flat=True))

                in_ids = org_invitations + gur_invitations
                invitations = invitations.filter(id__in=in_ids).distinct()

            serializer = Invitation_Serializer(invitations, many=True)

            paginator = PageNumberPagination()
            # Paginate the queryset
            result_page = paginator.paginate_queryset(invitations, request)        
            # Serialize the paginated data
            serializer = Invitation_Serializer(result_page, many=True,context={'request': request})        
            # Return the paginated response
            serializer = paginator.get_paginated_response(serializer.data)
            
            return Response(serializer.data)

        elif type == "interest":
            status = request.GET.get('status')
            if not status:
                status_filter = ('R', 'A', 'S')
            else:
                status_filter = status
            if user.groups.filter(name='Artist').exists():
                interests = Interest.objects.filter(musician=user.musician, status__in=status_filter)
            elif user.groups.filter(name='Band').exists():
                interests = Interest.objects.filter(troupe=user.troupe, status__in=status_filter)
            


            if organizer_name:
                org_invitations = list(interests.filter(Q(event__name__icontains=name) | Q(event__event_organizer__user__last_name__icontains=name) | 
                                                        Q(event__event_organizer__user__first_name__icontains=name)).distinct().values_list("id", flat=True))

                gur_invitations = list(interests.filter(Q(event__name__icontains=name) | Q(event__gurukulam__user__last_name__icontains=name) | 
                                                        Q(event__gurukulam__user__first_name__icontains=name)).distinct().values_list("id", flat=True))

                in_ids = org_invitations + gur_invitations
                interests = interests.filter(id__in=in_ids).distinct()

            
            paginator = PageNumberPagination()
            # Paginate the queryset
            result_page = paginator.paginate_queryset(interests, request)        
            # Serialize the paginated data
            serializer = Interest_Serializer(result_page, many=True,context={'request': request})        
            # Return the paginated response
            serializer = paginator.get_paginated_response(serializer.data)
            
        
            return Response(serializer.data)


#Message view(Invitation and Interest)
class Get_Message_Api(APIView):
    def get(self, request, messagetype, pk):
        data = {}
        if messagetype == 'Invitation':
            invitation = Invitation.objects.get(id=pk)

            messages = Message.objects.filter(invitation=invitation)
            if authorize_invitation(request,invitation):
                serializer = Message_Serializer(messages,many=True,context={'request': request})
                invitation_serializer = Invitation_Serializer(invitation,context={'request': request})
                data['messages'] = serializer.data
                data['invitation'] = invitation_serializer.data
            else:
                data['error'] = "Error"
        elif messagetype == 'Interest':
            interest = Interest.objects.get(id=pk)
            messages = Message.objects.filter(interest=interest)
            if authorize_interest(request,interest):
                serializer = Message_Serializer(messages,many=True,context={'request': request})
                interest_serializer = Interest_Serializer(interest,context={'request': request})
                data['messages'] = serializer.data
                data['interest'] = interest_serializer.data
            else:
                data['error'] = "Error"
        return Response(data)

#Message sending(Invitation and Interest)
class Put_Message_Api(APIView):
    def post(self, request):
        data = {}
        messagetype = request.data['messagetype']
        pk = request.data['pk']
        message_text = request.data['message']
        status_value = request.data['status']

        try:
            if messagetype == 'Invitation':
                invitation = Invitation.objects.get(id=pk)
                if authorize_invitation(request, invitation):
                    message_obj = Message(user=request.user, invitation=invitation, text=message_text)
                    message_obj.save()
                    if status_value:
                        Invitation.objects.filter(id=pk).update(status=status_value)   

                    messages = Message.objects.filter(invitation=invitation) 
                    serializer = Message_Serializer(messages,many=True,context={'request': request})
                    data['messages'] = serializer.data
                else:
                    data['error'] = "Authorization error"
            elif messagetype == 'Interest':
                interest = Interest.objects.get(id=pk)
                if authorize_interest(request, interest):
                    message_obj = Message(user=request.user, interest=interest, text=message_text)
                    message_obj.save()
                    if status_value:
                        Interest.objects.filter(id=pk).update(status=status_value) 
                    messages = Message.objects.filter(interest=interest)
                    serializer = Message_Serializer(messages,many=True,context={'request': request})
                    data['interest'] = serializer.data
                else:
                    data['error'] = "Authorization error"
            else:
                data['error'] = "Invalid messagetype. Supported values are 'Invitation' and 'Interest'."
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            return Response(data, status=status.HTTP_200_OK)
        except Invitation.DoesNotExist:
            data['error'] = "Invitation not found"
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        except Interest.DoesNotExist:
            data['error'] = "Interest not found"
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            data['error'] = str(e)

#MyEvents View(recent events)
class Recent_Event_View(APIView):

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get(self, request):
        user = request.user
        if user.groups.filter(name='Event Organizer').exists():
            events = Event.objects.filter(event_organizer=request.user.event_organizer,to_date__gte=datetime.now()).order_by('-from_date')
        elif user.groups.filter(name='Music School').exists():
            events = Event.objects.filter(gurukulam=request.user.gurukulam,to_date__gte=datetime.now()).order_by('-from_date')
        

        paginator = PageNumberPagination()
        # Paginate the queryset
        result_page = paginator.paginate_queryset(events, request)        
        # Serialize the paginated data
        serializer = My_Event_Serializer(result_page, many=True,context={'request': request})        
        # Return the paginated response
        return paginator.get_paginated_response(serializer.data)



#All Events View    
class All_Event_View(APIView):

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


    def get(self, request):
        if request.user.groups.filter(name='Event Organizer').exists():
            events = Event.objects.filter(event_organizer=request.user.event_organizer,to_date__lte=datetime.now()).order_by('-from_date')
      
        elif request.user.groups.filter(name='Music School').exists():
            events = Event.objects.filter(gurukulam=request.user.gurukulam,to_date__lte=datetime.now()).order_by('-from_date')   
         
        else:
            events = None


        paginator = PageNumberPagination()
        # Paginate the queryset
        result_page = paginator.paginate_queryset(events, request)        
        # Serialize the paginated data
        serializer = My_Event_Serializer(result_page, many=True,context={'request': request})        
        # Return the paginated response
        return paginator.get_paginated_response(serializer.data)
                  
        return Response(context)

#Invitation and Interest of Event    
class View_Event_API(APIView):

    def get(self,request,pk,type):
        user = request.user
        if type == "invitation":
            status = request.GET.get('status')
            if not status:
                status_filter = ('R','A','S')
            else:
                status_filter = status
            if user.groups.filter(name='Event Organizer').exists():            
                event = Event.objects.get(id=pk,event_organizer=request.user.event_organizer)                
            elif user.groups.filter(name='Music School').exists():
                event = Event.objects.get(id=pk,gurukulam=request.user.gurukulam)                
            sent_requests = Invitation.objects.filter(event_id=pk,status__in=status_filter)
            sent_requests = Organizer_Invitation_Serializer(sent_requests,many=True)
            event = Event_Serializer1(event)

            context = {
                'sent_requests' : sent_requests.data,
                'status': status,
                'event':event.data,
            }

        elif type == "interest":
            status = request.GET.get('status')
            if not status:
                status_filter = ('R','A','S')
            else:
                status_filter = status
            if user.groups.filter(name='Event Organizer').exists():
                event = Event.objects.get(id=pk,event_organizer=request.user.event_organizer)
                received_requests = Interest.objects.filter(event__event_organizer=request.user.event_organizer,event__id=pk,status__in=status_filter)
            elif user.groups.filter(name='Music School').exists():
                event = Event.objects.get(id=pk,gurukulam=request.user.gurukulam)
                received_requests = Interest.objects.filter(event__gurukulam= request.user.gurukulam,event__id=pk,status__in=status_filter)        
            received_requests = Organizer_Interest_Serializer(received_requests,many=True)
            event = Event_Serializer1(event)
            context = {
                'received_requests' : received_requests.data,   
                'event':event.data,          
            }
        return Response(context)

    def post(self,request,pk,type):
        user = request.user
        name = request.data['name']  

        
            
        if type == "invitation":
            status = request.GET.get('status')
            if not status:
                status_filter = ('R','A','S')
            else:
                status_filter = status
            if user.groups.filter(name='Event Organizer').exists():            
                event = Event.objects.get(id=pk,event_organizer=request.user.event_organizer)                
            elif user.groups.filter(name='Music School').exists():
                event = Event.objects.get(id=pk,gurukulam=request.user.gurukulam)    
            
            sent_requests = Invitation.objects.filter(event_id=pk,status__in=status_filter)

            if name:
                musician_sent_requests = list(
                Invitation.objects.filter(
                    Q(musician__user__last_name__icontains=name) | Q(musician__user__first_name__icontains=name),
                    event_id=pk, status__in=status_filter
                ).values_list('id', flat=True).distinct()
            )

                troupe_sent_requests = list(
                    Invitation.objects.filter(
                        Q(troupe__user__last_name__icontains=name) | Q(troupe__user__first_name__icontains=name),
                        event_id=pk, status__in=status_filter
                    ).values_list('id', flat=True).distinct()
                )

                gurukulam_sent_requests = list(
                    Invitation.objects.filter(
                        Q(gurukulam__user__last_name__icontains=name) | Q(gurukulam__user__first_name__icontains=name),
                        event_id=pk, status__in=status_filter
                    ).values_list('id', flat=True).distinct()
                )  
                ids = musician_sent_requests + troupe_sent_requests + gurukulam_sent_requests
                sent_requests = Invitation.objects.filter(id__in=ids,event_id=pk,status__in=status_filter)
            else:
                sent_requests = Invitation.objects.filter(event_id=pk,status__in=status_filter)


            sent_requests = Organizer_Invitation_Serializer(sent_requests,many=True)
            event = Event_Serializer1(event)

            context = {
                'sent_requests' : sent_requests.data,
                'status': status,
                'event':event.data,
            }

        elif type == "interest":
            status = request.GET.get('status')
            name = request.data['name']
            if not status:
                status_filter = ('R','A','S')
            else:
                status_filter = status
            if user.groups.filter(name='Event Organizer').exists():
                event = Event.objects.get(id=pk,event_organizer=request.user.event_organizer)
                received_requests = Interest.objects.filter(event__event_organizer=request.user.event_organizer,event__id=pk,status__in=status_filter)
            elif user.groups.filter(name='Music School').exists():
                event = Event.objects.get(id=pk,gurukulam=request.user.gurukulam)
                received_requests = Interest.objects.filter(event__gurukulam= request.user.gurukulam,event__id=pk,status__in=status_filter)        
            
            if name:
                musician_received_requests = received_requests.filter(
                    Q(musician__user__last_name__icontains=name) | Q(musician__user__first_name__icontains=name)
                ).values_list("id", flat=True)

                troupe_received_requests = received_requests.filter(
                    Q(troupe__user__last_name__icontains=name) | Q(troupe__user__first_name__icontains=name)
                ).values_list("id", flat=True)
                musician_ids = set(musician_received_requests)
                troupe_ids = set(troupe_received_requests)
                combined_ids = musician_ids.union(troupe_ids)

                received_ids = list(combined_ids)   
                received_requests = received_requests.filter(id__in=received_ids).distinct()
            received_requests = Organizer_Interest_Serializer(received_requests,many=True)

            event = Event_Serializer1(event)
            context = {
                'received_requests' : received_requests.data,   
                'event':event.data,          
            }
        return Response(context)


#New Invitation (Events)
class Event_Invite_API(APIView):    
    def get(self,request,pk):
        event = Event.objects.get(pk=pk)
        skills = Skill.objects.all()
        skill_levels = Skill_Level.objects.all()
        locations = Location.objects.all()
        gender = choose_gender
        events = Event_Serializer1(event)
        locations = LocationSerializer(locations, many=True)
        skills = SkillSerializer(skills,many=True)
        skill_levels = SkillLevelSerializer(skill_levels,many=True)
        context = {
            "skills": skills.data,
            "skill_levels": skill_levels.data,
            "locations": locations.data,
            'gender': gender,
            "events": events.data
        }
        return Response(context)

#Search by musician
class Musician_Search_API(APIView):

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def post(self,request,pk):
        data = dict()
        if request.user.groups.filter(name='Event Organizer').exists():
            event = Event.objects.get(id=pk,event_organizer=request.user.event_organizer)
        elif request.user.groups.filter(name='Gurukulam').exists():
            event = Event.objects.get(id=pk,gurukulam=request.user.gurukulam) 

        sent_requests = Invitation.objects.filter(event__id=pk,musician__isnull=False).values_list('musician__id', flat=True)
        get_requests = Interest.objects.filter(event__id=pk,musician__isnull=False).values_list('musician__id', flat=True)
        musician_exclude_ids_list = chain(sent_requests, get_requests)
        musician_filter = Musician.objects.all().exclude(id__in=musician_exclude_ids_list)        
        
        if request.method == 'POST':
                skill_level = request.data['skill_level']                        
                skill =   request.data['skill'] 
                district = request.data['location']
                gender =  request.data['gender']
                name = request.data['name']
                if skill:
                    musician_filter = musician_filter.filter(musician_skill__skill__id__in=skill).distinct()
                if skill_level:                
                    musician_filter = musician_filter.filter(musician_skill__skill_level__id__in=skill_level).distinct()             
                if district:
                    musician_filter = musician_filter.filter(user__location__in=district)
                if gender:
                    musician_filter = musician_filter.filter(gender__in=gender)
                if name:
                    musician_filter = musician_filter.filter(Q(user__last_name__icontains=name) | Q(user__first_name__icontains=name))
                data['valid'] = True


                print(musician_filter)
                paginator = PageNumberPagination()
                # Paginate the queryset
                result_page = paginator.paginate_queryset(musician_filter, request)        
                # Serialize the paginated data
                serializer = MusicianSerializer(result_page, many=True,context={'request': request})        
                # Return the paginated response

                return paginator.get_paginated_response(serializer.data)      
          
            
        
        else:
            data['valid'] = False
        return Response(data)

#Search by Troupe
class Troupe_Search_API(APIView):
    
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def post(self, request, pk):
        data = dict()

        if request.user.groups.filter(name='Event Organizer').exists():
            event = Event.objects.get(id=pk, event_organizer=request.user.event_organizer)
        elif request.user.groups.filter(name='Gurukulam').exists():
            event = Event.objects.get(id=pk, gurukulam=request.user.gurukulam)

        sent_requests = Invitation.objects.filter(event__id=pk, troupe__isnull=False).values_list('troupe__id', flat=True)
        get_requests = Interest.objects.filter(event__id=pk, troupe__isnull=False).values_list('troupe__id', flat=True)
        troupe_exclude_list = chain(sent_requests, get_requests)

        if request.method == 'POST':
            skill = request.data['skill']
            district = request.data['location']
            name = request.data['name']

            troupes_list = Troupe.objects.exclude(id__in=troupe_exclude_list).distinct()

            if skill:
                troupes_list = troupes_list.filter(troupe_skill__skill__id__in=skill)

            if district:
                troupes_list = troupes_list.filter(user__location__id__in=district)

            if name:
                troupes_list = troupes_list.filter(user__name__icontains=name)

            troupes = troupes_list


            paginator = PageNumberPagination()
            # Paginate the queryset
            result_page = paginator.paginate_queryset(troupes, request)        
            # Serialize the paginated data
            serializer = Troupe_Search_Serializer(result_page, many=True,context={'request': request})        
            # Return the paginated response
      
            
            data['valid'] = True
            return paginator.get_paginated_response(serializer.data)
        else:
            data['valid'] = False
        return Response(data)

#Search by Gurukulam
class Gurukulam_Search_API(APIView):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def post(self, request, pk):
        data = dict()

        if request.user.groups.filter(name='Event Organizer').exists():
            event = Event.objects.get(id=pk, event_organizer=request.user.event_organizer)
            gurukulam_id = []
        elif request.user.groups.filter(name='Music School').exists():
            event = Event.objects.get(id=pk, gurukulam=request.user.gurukulam)
            gurukulam_id = [request.user.gurukulam.id]

        sent_requests = Invitation.objects.filter(event=event, gurukulam__isnull=False).values_list('gurukulam__id', flat=True)
        get_requests = Interest.objects.filter(event=event, event__gurukulam__isnull=False).values_list('event__gurukulam__id', flat=True)

        gurukulam_exclude_list = chain(sent_requests, get_requests, gurukulam_id)

        if request.method == 'POST':
            skill = request.data['skill']
            district = request.data['location']
            name = request.data['name']

            gurukulam_filter = Gurukulam.objects.all()

            if skill:
                gurukulam_filter = gurukulam_filter.filter(gurukulam_skill__skill__id__in=skill).distinct()
            if district:
                gurukulam_filter = gurukulam_filter.filter(user__location__id__in=district)

            if name:
                gurukulam_filter = gurukulam_filter.filter(Q(user__last_name__icontains=name) | Q(user__first_name__icontains=name))

            data['valid'] = True


            paginator = PageNumberPagination()
            # Paginate the queryset
            result_page = paginator.paginate_queryset(gurukulam_filter, request)        
            # Serialize the paginated data
            serializer = Gurukulam_Search_Serializer(result_page, many=True,context={'request': request})        
            # Return the paginated response
      
            
            data['valid'] = True
            return paginator.get_paginated_response(serializer.data)


        else:
            data['valid'] = False

        return Response(data)

#Requesting Musician(Event)     
class Musician_Request_API(APIView):
    def post(self,request,pk):
            data = dict()
            user= request.user
            if user.groups.filter(name='Event Organizer').exists():
                event = Event.objects.get(id=pk,event_organizer=request.user.event_organizer)
            elif user.groups.filter(name='Music School').exists():
                event = Event.objects.get(id=pk,gurukulam=request.user.gurukulam) 

            if request.method == 'POST':
                musicians = request.data['musician']    
                message_text = request.data['message']    
                     
                for musician in musicians:                 
                    musician_instance= Musician.objects.get(id=musician)
                    if not (Invitation.objects.filter(event=event,musician=musician).exists() or Interest.objects.filter(event=event,musician=musician).exists()):
                        invitation =Invitation.objects.create(event=event,musician=musician_instance,status="S")
                        message_obj = Message(user=request.user, invitation=invitation, text=message_text)
                        message_obj.save()
                    #email                
                        link= str(request.META['HTTP_HOST'])+'/get_message/Invitation/'+str(invitation.id)    
                        mail_to = musician_instance.user.email      
                        subject = 'Event Invitation - Reg'
                        message ='You have been invited to this event'+str(invitation.event)+'; please accept or decline by clicking here. Link: {}'.format(link)     
                        
                data['valid'] = True
            else:
                data['valid'] = False
            return Response(data)
    

class Troupe_Request_API(APIView):
    def post(self,request,pk):
        data = dict()
        if request.user.groups.filter(name='Event Organizer').exists(): 
            event = Event.objects.get(id=pk,event_organizer=request.user.event_organizer)
        if request.user.groups.filter(name='Music School').exists(): 
            event = Event.objects.get(id=pk,gurukulam=request.user.gurukulam) 

        if request.method == 'POST':
            troupes = request.data['troupe']  
            message_text = request.data['message']              

            for troupe in troupes:
                troupe_instance= Troupe.objects.get(id=troupe)

                if not (Invitation.objects.filter(event=event,troupe=troupe).exists() or Interest.objects.filter(event=event,troupe=troupe).exists()):
                    invitation =Invitation.objects.create(event=event,troupe=troupe_instance,status="S")
                    message_obj = Message(user=request.user, invitation=invitation, text=message_text)
                    message_obj.save()

                    #email                
                    link= str(request.META['HTTP_HOST'])+'/get_message/Invitation/'+str(invitation.id)    
                    mail_to = troupe_instance.user.email      
                    subject = 'Event Invitation - Reg'
                    message ='You have been invited to this event'+str(invitation.event)+'; please accept or decline by clicking here. Link: {}'.format(link)     
                    #send_email(subject,mail_to,message)
                    

            data['valid'] = True


        else:
            data['valid'] = False

        return Response(data)


class Music_School_Request_API(APIView):
    def post(self,request,pk):
        data = dict()
        user=request.user
        if user.groups.filter(name='Event Organizer').exists():
            event = Event.objects.get(id=pk,event_organizer=request.user.event_organizer)
        elif user.groups.filter(name='Music School').exists():
            event = Event.objects.get(id=pk,gurukulam=request.user.gurukulam) 

        if request.method == 'POST':
            gurukulas = request.data['music_school']   
            message_text = request.data['message']
            

            for gurukulam in gurukulas:
                gurukulam_instance= Gurukulam.objects.get(id=gurukulam)
                invitation =Invitation.objects.create(event=event,gurukulam=gurukulam_instance,status="S")  
                message_obj = Message(user=request.user, invitation=invitation, text=message_text)
                message_obj.save()

                #email                
                link= str(request.META['HTTP_HOST'])+'/get_message/Invitation/'+str(invitation.id)    
                mail_to = gurukulam_instance.user.email      
                subject = 'Event Invitation - Reg'
                message ='You have been invited to this event'+str(invitation.event)+'; please accept or decline by clicking here. Link: {}'.format(link)     
                #send_email(subject,mail_to,message)

            data['valid'] = True


        else:
            data['valid'] = False


        return JsonResponse(data)



#home page event filter
class Search_Event_API(APIView):

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def post(self,request):
        user_groups = request.user.groups.all()
        event_filter_type = request.data.get('event_filter')
        for group in user_groups:
            if group.name == "Musician":
                sent_requests = Interest.objects.filter(musician=request.user.musician).values_list('event__id', flat=True)
                received_requests = Invitation.objects.filter(musician=request.user.musician).values_list('event__id', flat=True)
                user_type = "musician"
                musician_skills = Musician_Skill.objects.filter(musician=request.user.musician).values_list('skill__id', flat=True)
                
            elif group.name == "Band":
                sent_requests = Interest.objects.filter(troupe=request.user.troupe).values_list('event__id', flat=True)
                received_requests = Invitation.objects.filter(troupe=request.user.troupe).values_list('event__id', flat=True)
                user_type = "troupe"
            elif group.name == "Event Organizer":
                sent_requests = None
                received_requests = None
                user_type = "event_organizer"
            elif group.name == "Music School":
                sent_requests = None
                received_requests = None
                user_type = "gurukulam"

        if request.method == "POST":
         
            data=dict()
            skill = request.data['skill'] 
            location =request.data['location']
            event_types = request.data['event_type']
        
            event_categories = request.data['event_category']
            name =  request.data['name']
            from_date =  request.data['after_date']
            to_date =  request.data['to_date']

            if event_filter_type == "recent":            
                if not sent_requests and  not received_requests:
                    event_filter= Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False)
                elif  sent_requests and  not received_requests:
                    event_filter = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False).exclude(id__in=sent_requests)
                elif not sent_requests and  received_requests:
                    event_filter = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False).exclude(id__in=received_requests)
                else:
                    event_exclude_ids_list = chain(sent_requests, received_requests)
                    event_filter = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False).exclude(id__in=event_exclude_ids_list)
            
            elif event_filter_type == "interest":
                if user_type == "musician":
                    interests = list(Musician_Skill.objects.filter(musician=request.user.musician).values_list('skill',flat=True).distinct())                
                if not sent_requests and  not received_requests:
                    event_filter= Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False,event_skill__skill__in=interests).distinct()
                elif  sent_requests and  not received_requests:
                    event_filter = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False,event_skill__skill__in=interests).exclude(id__in=sent_requests).distinct()
                elif not sent_requests and  received_requests:
                    event_filter = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False,event_skill__skill__in=interests).exclude(id__in=received_requests).distinct()
                else:
                    event_exclude_ids_list = chain(sent_requests, received_requests)
                    event_filter = Event.objects.filter(registration_close_date__gte=datetime.now(),self_reference=False,event_skill__skill__in=interests).exclude(id__in=event_exclude_ids_list).distinct()
            
            elif event_filter_type == "i_follow":
                following = UserFollowing.objects.filter(user=request.user,following_user_id__groups__name__in=('Event Organizer','Gurukulam')).values_list('following_user_id__id',flat=True)
        
                if not sent_requests and  not received_requests:
                    event_filter= Event.objects.filter(Q(gurukulam__user__id__in=following) | Q(event_organizer__user__id__in=following),registration_close_date__gte=datetime.now(),self_reference=False).distinct()
                elif  sent_requests and  not received_requests:
                    event_filter = Event.objects.filter(Q(gurukulam__user__id__in=following) | Q(event_organizer__user__id__in=following),registration_close_date__gte=datetime.now(),self_reference=False).exclude(id__in=sent_requests).distinct()
                elif not sent_requests and  received_requests:
                    event_filter = Event.objects.filter(Q(gurukulam__user__id__in=following) | Q(event_organizer__user__id__in=following),registration_close_date__gte=datetime.now(),self_reference=False).exclude(id__in=received_requests).distinct()
                else:
                    event_exclude_ids_list = chain(sent_requests, received_requests)
                    event_filter = Event.objects.filter(Q(gurukulam__user__id__in=following) | Q(event_organizer__user__id__in=following),registration_close_date__gte=datetime.now(),self_reference=False).exclude(id__in=event_exclude_ids_list).distinct()

            if skill:
                event_filter = event_filter.filter(event_skill__skill__id__in=skill).distinct()
            if location:
                event_filter = event_filter.filter(location__id__in=location)
            if event_types:
                event_filter = event_filter.filter(event_type__id__in=event_types)
            if event_categories:
                event_filter = event_filter.filter(event_category__id__in=event_categories)
            if name:
                event_filter = event_filter.filter(name__icontains=name)
            if from_date:
                event_filter = event_filter.filter(from_date__gte=from_date)
            if to_date:
                event_filter = event_filter.filter(to_date__lte=to_date)

            events = event_filter.order_by('-id')
       
            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(events, request) 
            serializer = EventSerializer(result_page, many=True,context={'request': request})
            return paginator.get_paginated_response(serializer.data)


        else:
            pass  
        return Response(data)


class Edit_Event_Api(APIView):
    def get(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        
        locations = Location.objects.all()
        location_serializer = Location_Serializer(locations, many=True)
        event_category = Event_Category.objects.all()
        event_category_serializer = Event_Category_Serializer(event_category, many=True)
        event_serializer = Edit_Event_Serializer(event, context={'request': request})


        skill_categories = Skill_Category.objects.all()
        skill_categories = Skill_Category_Serializer(skill_categories,many=True)
        skills  = Skill.objects.all()
        skills  = Skill_Serializer_Filter(skills,many=True)

        event_skills = Event_Skill.objects.filter(event=event)
        event_skills = Event_Skill_Serializer1(event_skills,many=True)

        context = {
                    'event' : event_serializer.data,
                    'event_skills':event_skills.data,
                    'event_category': event_category_serializer.data,
                    'location': location_serializer.data,
                    "skill_categories":skill_categories.data,
                    "skills":skills.data
                }
        return Response(context)

    def put(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        

        skill_data = request.POST.getlist('skill')
        skill_data = eval(skill_data[0])

        if (event.event_organizer and event.event_organizer.user != request.user and event.gurukulam and event.gurukulam.user != request.user):
            return Response({'error': 'You do not have permission to edit this event'}, status=status.HTTP_403_FORBIDDEN)
        event_serializer = Edit_Event_Serializer1(event, data=request.data, context={'request': request},partial=True)   
        if event_serializer.is_valid():
            event_serializer.save()
            #delete all event related skills
            Event_Skill.objects.filter(event=event).delete()


            if skill_data:
                for skill in skill_data:
                    try:
                        skill = Skill.objects.get(id=skill)
                        skill = Event_Skill.objects.create(event=event,skill=skill)
                    except:
                        pass   

            return Response(event_serializer.data)
        else:
            return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



#Musucian search for event creation
#Search by musician
class Musician_Search_EC_API(APIView):

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000
    
    def post(self,request):
        data = dict()
        musician_exclude_ids_list = []
        musician_filter = Musician.objects.all().exclude(id__in=musician_exclude_ids_list)        
        
        if request.method == 'POST':
                skill_level = request.data.get('skill_level', [])                        
                skill =   request.data.get('skill', []) 
                district = request.data.get('location', [])
                gender =  request.data.get('gender')
                name = request.data.get('name')
                if skill:
                    musician_filter = musician_filter.filter(musician_skill__skill__id__in=skill).distinct()
                if skill_level:                
                    musician_filter = musician_filter.filter(musician_skill__skill_level__id__in=skill_level).distinct()             
                if district:
                    musician_filter = musician_filter.filter(user__location__in=district)
                if gender:
                    musician_filter = musician_filter.filter(gender__in=gender)
                if name:
                    musician_filter = musician_filter.filter(Q(user__last_name__icontains=name) | Q(user__first_name__icontains=name))
                data['valid'] = True
            
                paginator = PageNumberPagination()
                # Paginate the queryset
                result_page = paginator.paginate_queryset(musician_filter, request)        
                # Serialize the paginated data
                serializer = MusicianSerializer(result_page, many=True,context={'request': request})        
                # Return the paginated response
                return paginator.get_paginated_response(serializer.data)
                    
        else:
            data['valid'] = False
        return Response(data)
    

    def get(self,request):
        locations = Location.objects.all()
        locations = Location_Serializer(locations,many=True)

        skills = Skill.objects.all()
        skill_levels = Skill_Level.objects.all()
        locations = Location.objects.all()
        gender = choose_gender
        locations = LocationSerializer(locations, many=True)
        skills = SkillSerializer(skills,many=True)
        skill_levels = SkillLevelSerializer(skill_levels,many=True)

        context = {
            "locations":locations.data,
            "skills":skills.data,
            "skill_levels":skill_levels.data,
            "gender":gender,
        }
        return Response(context)
    


#Search by Troupe
class Band_Search_EC_API(APIView):

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def post(self, request):
        data = dict()

        troupe_exclude_list = []

        if request.method == 'POST':
            skill = request.data.get('skill', [])
            district = request.data.get('location', [])
            name = request.data.get('name')

            troupes_list = Troupe.objects.exclude(id__in=troupe_exclude_list).distinct()

            if skill:
                troupes_list = troupes_list.filter(troupe_skill__skill__id__in=skill)

            if district:
                troupes_list = troupes_list.filter(user__location__id__in=district)

            if name:
                troupes_list = troupes_list.filter(user__name__icontains=name)

            troupes = troupes_list
            
    
            paginator = PageNumberPagination()
            # Paginate the queryset
            result_page = paginator.paginate_queryset(troupes, request)        
            # Serialize the paginated data
            serializer = Troupe_Search_Serializer(result_page, many=True,context={'request': request})        
            # Return the paginated response
            return paginator.get_paginated_response(serializer.data)


        else:
            data['valid'] = False
        return Response(data)
    

    def get(self,request):
        locations = Location.objects.all()
        locations = Location_Serializer(locations,many=True)

        skills = Skill.objects.all()
 
        locations = Location.objects.all()
   
        locations = LocationSerializer(locations, many=True)
        skills = SkillSerializer(skills,many=True)
  

        context = {
            "locations":locations.data,
            "skills":skills.data,
          
        }
        return Response(context)


#Search by Music school
class Music_School_Search_EC_API(APIView):

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def post(self, request):
        data = dict()

        gurukulam_exclude_list = []

        if request.method == 'POST':
            skill = request.data.get('skill', [])
            district = request.data.get('location', [])
            name = request.data.get('name')

            gurukulam_filter = Gurukulam.objects.all()

            if skill:
                gurukulam_filter = gurukulam_filter.filter(gurukulam_skill__skill__id__in=skill).distinct()
            if district:
                gurukulam_filter = gurukulam_filter.filter(user__location__id__in=district)

            if name:
                gurukulam_filter = gurukulam_filter.filter(Q(user__last_name__icontains=name) | Q(user__first_name__icontains=name))

            
    
            paginator = PageNumberPagination()
            # Paginate the queryset
            result_page = paginator.paginate_queryset(gurukulam_filter, request)        
            # Serialize the paginated data
            serializer = Gurukulam_Search_Serializer(result_page, many=True,context={'request': request})        
            # Return the paginated response
            return paginator.get_paginated_response(serializer.data)


        else:
            data['valid'] = False
        return Response(data)
    

    def get(self,request):
        locations = Location.objects.all()
        locations = Location_Serializer(locations,many=True)

        skills = Skill.objects.all()
 
        locations = Location.objects.all()
   
        locations = LocationSerializer(locations, many=True)
        skills = SkillSerializer(skills,many=True)
  

        context = {
            "locations":locations.data,
            "skills":skills.data,
          
        }
        return Response(context)


