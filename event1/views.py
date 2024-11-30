#from account.views import musician
from django.core.checks import messages
from django.shortcuts import redirect, render
from .models import Message, Event, Event_Type, Invitation, Interest, Event_Category, Subscription, Subscription_Type, Event_Skill
from .forms import Event_Form
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from account.models import Gurukulam, Musician, Musician_Skill, Post, Skill_Category, Skill_Level, Skill, Location, Troupe, UserFollowing
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



# Create your views here.
gender_options = (('','Choose Gender'),('M','Male'),('F','Female'),('T','Transgender'),('N','None'))



def event_details(request,pk):
    event = Event.objects.get(id=pk)
    invitations = Invitation.objects.filter(event=event,status="A")
    interests = Interest.objects.filter(event=event,status="A")

    skill_categories = None
    related_category_events = Event.objects.filter(event_category=event.event_category)    
    event_created_by_me = False



    if invitations or interests:
        is_any_participant = True
    else:
        is_any_participant = False


    if event.event_organizer:
        related_events = Event.objects.filter(event_organizer=event.event_organizer)
        skill_categories = Skill_Category.objects.all()
    elif event.gurukulam:
        related_events = Event.objects.filter(gurukulam=event.gurukulam)
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
        events = Event.objects.filter(event_organizer=request.user.event_organizer).order_by('-from_date')
    elif request.user.groups.filter(name='Music School').exists():
        events = Event.objects.filter(gurukulam=request.user.gurukulam).order_by('-from_date')
    else:
        HttpResponse("Access Denied")

    skill_categories = Skill_Category.objects.all()
    context = {
        'events' : events, 
        'page' : 'all_event',
        'skill_categories':skill_categories,
    }
    return render(request,'event/all_events.html', context) 


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
            
        elif user.groups.filter(name='Gurukulam').exists():
            event = Event.objects.get(id=pk,gurukulam=request.user.gurukulam)
            
        sent_requests = Invitation.objects.filter(event_id=pk,status__in=status_filter)

        page = request.GET.get('page', 1)
             
        paginator = Paginator(sent_requests, 20)
        try:
            sent_requests = paginator.page(page)
        except PageNotAnInteger:
            sent_requests = paginator.page(1)
        except EmptyPage:
            sent_requests = paginator.page(paginator.num_pages)
     


        context = {
            'sent_requests' : sent_requests,
            'page' : page,
            'status': status,
            'event':event,
            'object_id' : pk,
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
        elif user.groups.filter(name='Gurukulam').exists():
            event = Event.objects.get(id=pk,gurukulam=request.user.gurukulam)
            received_requests = Interest.objects.filter(event__gurukulam= request.user.gurukulam,event__id=pk,status__in=status_filter)

        page = request.GET.get('page', 1)
             
        paginator = Paginator(received_requests, 20)
        try:
            received_requests = paginator.page(page)
        except PageNotAnInteger:
            received_requests = paginator.page(1)
        except EmptyPage:
            received_requests = paginator.page(paginator.num_pages)
     


        context = {
            'received_requests' : received_requests,
            'page' : page,
            'status': status,
            'object_id' : pk,
            'event' : event,
            'interest_tab_active': True,
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
    elif user.groups.filter(name='Gurukulam').exists():
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
        skill =[ast.literal_eval(i) for i in request.POST.getlist('skill')] 
        location =request.POST.get('location')
        print(location)
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
        print(event_filter_type)

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
            print(following)
       
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
            print(location)
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

        event_filter = event_filter.order_by('-id')[:100]

        print(event_filter)



        data['valid'] = True
        data['html'] = render_to_string('event/event_list.html',{'events':event_filter,'user_type':user_type,},request)
    else:
        pass
    
    return JsonResponse(data)
    


def event_request_send(request):   
    data = dict()
    if request.method == 'POST':
        events = request.POST.getlist('event')
        message_text = request.POST.get('message', None) 

        if request.user.groups.filter(name='Musician').exists(): 
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
                    send_email(subject,mail_to,message)

                

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
            district = [ast.literal_eval(i) for i in request.POST.getlist('district')]
            name = request.POST.get('name')
             
            troupes_list  = Troupe.objects.exclude(id__in=troupe_exclude_list).distinct()
    
            if skill:
                troupes_list = troupes_list.filter(troupe_skill__skill__id__in=skill)            
            if district:
                troupes_list = troupes_list.filter(user__district__id__in=district)
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
    
            if skill:                
                if district:
                    if name:                            
                        gurukulas = Gurukulam.objects.filter(user__name__icontains=name,gurukulam_skill__skill__id__in=skill,user__district__id__in=district).exclude(id__in=gurukulam_exclude_list).distinct()
                    else:
                        gurukulas = Gurukulam.objects.filter(gurukulam_skill__skill__id__in=skill,user__district__id__in=district).exclude(id__in=gurukulam_exclude_list).distinct()
                elif name:
                    gurukulas = Gurukulam.objects.filter(user__name__icontains=name,gurukulam_skill__skill__id__in=skill).exclude(id__in=gurukulam_exclude_list).distinct()

                else:
                    gurukulas = Gurukulam.objects.filter(gurukulam_skill__skill__id__in=skill).exclude(id__in=gurukulam_exclude_list).distinct()
            elif district:
                if name:
                    gurukulas = Gurukulam.objects.filter(user__name__icontains=name,user__district__id__in=district).exclude(id__in=gurukulam_exclude_list)

                else:
                    gurukulas = Gurukulam.objects.filter(user__district__id__in=district).exclude(id__in=gurukulam_exclude_list)
            elif name:
                gurukulas = Gurukulam.objects.filter(user__name__icontains=name).exclude(id__in=gurukulam_exclude_list)
            
            else:
                gurukulas = None
    
            data['valid'] = True

            data['html'] = render_to_string('event/gurukulam_list.html',{'gurukulas':gurukulas},request)
             
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
                    post =Post.objects.create(location=invitation.event.district,user=invitation.musician.user,content='I am going to participate <a  href="/event_details/' + str(invitation.event.id) + '/">' + str(invitation.event)  +  '</a> <br> <img class="img-fluid" src="'+invitation.event.poster_image.url+'">' )
                elif invitation.troupe:
                    post =Post.objects.create(location=invitation.event.district,user=invitation.troupe.user,content='I am going to participate <a  href="/event_details/' + str(invitation.event.id) + '/">' + str(invitation.event)  +  '</a> <br> <img class="img-fluid" src="'+invitation.event.poster_image.url+'">' )
                elif invitation.gurukulam:
                    post =Post.objects.create(location=invitation.event.district,user=invitation.gurukulam.user,content='I am going to participate <a  href="/event_details/' + str(invitation.event.id) + '/">' + str(invitation.event)  +  '</a> <br> <img class="img-fluid" src="'+invitation.event.poster_image.url+'">'  )


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
    elif request.user.groups.filter(name='Gurukulam').exists() and request.user ==  invitation.event.gurukulam.user:
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
    elif request.user.groups.filter(name='Gurukulam').exists() and request.user == interest.event.gurukulam.user:
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
        if user.groups.filter(name='Musician').exists() and interest.musician.user == user:
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
        context = {
            'page'   : 'recent_event',
            'events' : events,
            'skill_categories':skill_categories,
          }
        return render(request,'event/recent_events.html', context)
    elif user.groups.filter(name='Music School').exists():
        events = Event.objects.filter(gurukulam=request.user.gurukulam,to_date__gte=datetime.now()).order_by('-from_date')
        skill_categories = Skill_Category.objects.all()
        context = {
            'events' : events,
            'page'   : 'home',
            'skill_categories':skill_categories,
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

            data['html'] = render_to_string('invitation.html',context)
            return JsonResponse(data)
    elif messagetype == 'Interest':
        interest = Interest.objects.get(id=pk)
        Message.objects.filter(interest=interest,unread=True).exclude(user=request.user).update(unread=False)
        if authorize_interest(request,interest):
            context = {
            'interest':interest,
            }           
            data['html'] = render_to_string('interest.html',context)
            data['has_access'] = True        
            return JsonResponse(data)
    
    data['has_access'] = False
    return JsonResponse(data)
