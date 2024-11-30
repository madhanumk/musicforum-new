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

    path('event_like_unlike/<int:pk>/',views.event_ajax_like_unlike, name="event_like_unlike"),
    path('bookmark/<int:event_id>/', views.bookmark_event, name='bookmark_event'),
    


    #new 
    path('get_event_message/<str:messagetype>/<int:pk>',views.get_event_message,name="get_event_message"),

    path('create_event/', views.create_event, name='create_event'),
    path('edit_event/<int:pk>', views.edit_event, name='edit_event'),



    
    #api
    path('api/events/', views.Event_View.as_view(), name='event_api'),
    path('api/interest/', views.Send_Interest_Api.as_view(), name='api_interest'),
    path('api/create_event/', views.Create_Event_Api.as_view(), name='api_create_event'),
    path('api/edit_event/<int:pk>/', views.Edit_Event_Api.as_view(), name='api_edit_event'),
    path('api/event_details/<int:pk>/',views.Event_Detail_Api.as_view(), name='event_details_api'),
    path('api/event_inbox/<str:type>/',views.Event_Inbox_Api.as_view(),name='event_inbox_api'),
    path('api/get_message/<str:messagetype>/<int:pk>/', views.Get_Message_Api.as_view(), name='api_get_message_api'),
    path('api/event_put_message/',views.Put_Message_Api.as_view(), name='api_put_message_api'),

    path('api/recent_events/', views.Recent_Event_View.as_view(), name='recent_event_api'),
    path('api/all_events/', views.All_Event_View.as_view(), name='all_event_api'),
    path('api/view_event/<int:pk>/<str:type>/', views.View_Event_API.as_view(), name='view_event_api'),
    path('api/event_invite/<int:pk>/', views.Event_Invite_API.as_view(), name='event_invite_api'),
    #event invitation
    path('api/musician_search/<int:pk>/',views.Musician_Search_API.as_view(), name="musician_search_api"),
    path('api/musician_request/<int:pk>/',views.Musician_Request_API.as_view(), name="musician_request_api"),

    path('api/troupe_search/<int:pk>/',views.Troupe_Search_API.as_view(), name="troupe_search_api"),
    path('api/troupe_request/<int:pk>/',views.Troupe_Request_API.as_view(), name="troupe_request_api"),

    path('api/gurukulam_search/<int:pk>/',views.Gurukulam_Search_API.as_view(), name="gurukulam_search_api"),
    path('api/music_school_request/<int:pk>/',views.Music_School_Request_API.as_view(), name="music_school_request_api"),
    #search event for home page
    path('api/event_search/',views.Search_Event_API.as_view(), name="event_search_api"),

    path('api/musician_search_ec/',views.Musician_Search_EC_API.as_view(), name="musician_search_api_ec"),
    path('api/band_search_ec/',views.Band_Search_EC_API.as_view(), name="musician_search_api_ec"),
    path('api/music_school_search_ec/',views.Music_School_Search_EC_API.as_view(), name="music_school_search_api_ec"),
    
]