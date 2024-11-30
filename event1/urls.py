from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
    path('recent_events/',views.recent_events, name="recent_events"),
    path('all_events/',views.all_events, name="all_events"),
    path('event_details/<int:pk>/',views.event_details, name="event_details"),
    path('ajax_create_event/',views.ajax_create_event, name="ajax_create_event"),
    path('view_event/<int:pk>/<str:type>/',views.view_event, name="view_event"),
    path('event_invite/<int:pk>',views.event_invite, name="event_invite"),
    path('musician_search/<int:pk>',views.musician_search, name="musician_search"),
    path('musician_request/<int:pk>',views.musician_request, name="musician_request"),
    path('invitation/<int:pk>',views.invitation, name="invitation"),
    path('search_event/',views.search_event, name="search_event"),
    path('ajax_skill_filter/',views.ajax_skill_filter, name="ajax_skill_filter"),
    
    path('event_request_send/',views.event_request_send, name="event_request_send"),
    path('troupe_request/<int:pk>',views.troupe_request, name="troupe_request"),
    path('troupe_search/<int:pk>',views.troupe_search, name="troupe_search"),
    path('gurukulam_search/<int:pk>',views.gurukulam_search, name="gurukulam_search"),
    path('gurukulam_request/<int:pk>',views.gurukulam_request, name="gurukulam_request"),

    path('ajax_get_skill/',views.ajax_get_skill, name="ajax_get_skill"),
    path('ajax_remove_skill/<int:pk>',views.ajax_remove_skill, name="ajax_remove_skill"),

    path('put_message/',views.put_message,name="put_message"),
    path('get_message/<str:messagetype>/<int:pk>',views.get_message,name="get_message"),
    path('request_delete/<str:delete_type>/<int:pk>',views.request_delete,name="request_delete"),


    #new 
    path('get_event_message/<str:messagetype>/<int:pk>',views.get_event_message,name="get_event_message"),


    
]