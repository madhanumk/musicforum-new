from django.contrib import admin
from django.urls import path, re_path

from . import views 
from django.contrib.auth import views as auth_views


urlpatterns = [ 
    path('',views.event_list, name="event_list"),
    path('show_location_based_events/',views.show_location_based_events, name="show_location_based_events"),
    path('search/',views.search, name="search"),
    path('signup/',views.signup, name="signup"),
    path('registered/',views.registered, name="registered"),
    path('activate/<slug:uidb64>/<slug:token>/',views.activate_account, name='activate'),
    path('login/',views.CustomLoginView.as_view(), name='signin',kwargs={'redirect_authenticated_user': True}),
    path('login/',views.CustomLoginView.as_view(), name='login',kwargs={'redirect_authenticated_user': True}),
    path('logout/',views.logout, name="logout"),
    path('home/',views.home, name="home"),
    path('musician_edit_profile/',views.edit_profile, name="musician_edit_profile"),
    path('gurukulam_edit_profile/',views.gurukulam_edit_profile, name="gurukulam_edit_profile"),
    path('troupe_edit_profile/',views.troupe_edit_profile, name="troupe_edit_profile"),
    path('event_organizer_edit_profile/',views.event_organizer_edit_profile, name="event_organizer_edit_profile"),
    path('music_lover_edit_profile',views.edit_profile_music_lover, name="music_lover_edit_profile"),
    path('set_location/',views.set_location, name="set_location"), 
    path('search_top_peoples/',views.search_top_peoples, name="search_top_peoples"),    

    #Musician Profile
    path('my_opportunities/<str:type>',views.my_opportunities, name="my_opportunities"),
    path('view_student/',views.view_student, name="view_student"),
    path('view_student/sent_request',views.view_sent_request, name="view_sent_request"),    

    #gurukulam
    path('view_teacher/',views.view_teacher, name="view_teacher"),
    path('view_teacher/sent-request',views.view_teacher_sent_request, name="view_teacher_sent_request"),

    #troupe
    path('troupe_invitation/<int:pk>/',views.troupe_invitation, name="troupe_invitation"),

    #event_organizer   
    path('ajax_event_edit/<str:model_name>/<int:pk>/',views.ajax_event_edit, name="ajax_event_edit"),
    path('ajax_event_delete/<str:model_name>/<int:pk>/',views.ajax_event_delete, name="ajax_event_delete"),
    path('ajax_create_event_organizer_highlight/',views.ajax_create_event_organizer_highlight, name="ajax_create_event_organizer_highlight"),
    path('ajax_edit_event_organizer_highlight/<int:pk>/',views.ajax_edit_event_organizer_highlight, name="ajax_edit_event_organizer_highlight"),
    path('ajax_delete_eventer_highlight/<int:pk>/',views.ajax_delete_eventer_highlight, name="ajax_delete_eventer_highlight"),
    path('ajax_add_event_performer/',views.ajax_add_event_performer, name="ajax_add_event_performer"),
    path('ajax_delete_event_performer/<int:pk>/',views.ajax_delete_event_performer, name="ajax_delete_event_performer"),
    path('event_performer_invitation/<int:pk>/',views.event_performer_invitation, name="event_performer_invitation"),

    #Profile
    path('follow/<int:pk>/',views.ajax_follow, name="follow"),
    path('unfollow/<int:pk>/',views.ajax_unfollow, name="unfollow"),

    #Post
    path('like/<int:pk>/',views.ajax_like, name="like"),
    path('unlike/<int:pk>/',views.ajax_unlike, name="unlike"),
    path('comment/<int:pk>/',views.ajax_comment, name="comment"),
    path('reply/<int:pk>/',views.ajax_reply, name="reply"),
    path('delete_comment/<int:pk>/',views.ajax_delete_comment, name="delete_comment"),
    path('delete_reply/<int:pk>/',views.ajax_delete_reply, name="delete_reply"),
    path('post-likes/<int:pk>/',views.post_likes, name="post-likes"),
    path('load-more-post/',views.load_more_post, name="load-more-post"),

    #Account
    path('following/',views.following, name="following"),
    path('followers/',views.followers, name="followers"),
    path('following/<int:pk>',views.user_following, name="user_following"),
    path('followers/<int:pk>',views.user_followers, name="user_followers"),   
    path('search/musician/',views.search_musician, name="musician-search"),
    path('search/event_organizer/',views.search_eventer, name="eventer-search"),
    path('search/gurukulam/',views.search_gurukulam, name="gurukulam-search"),
    path('search/troupe/',views.search_troupe, name="troupe-search"),
    path('event-finder/<int:pk>/',views.event_finder, name="event-finder"),
    path('my_profile/',views.my_profile, name="my_profile"),
   
    path('home_post_filter/',views.post_filter, name="home_post_filter"),
    path('follow_unfollow/<int:pk>',views.ajax_follow_unfollow, name="follow_unfollow"),
    path('search_people/',views.search_people, name="search_people"),
    path('like_unlike/<int:pk>/',views.ajax_like_unlike, name="like_unlike"),
    path('home_event_filter/',views.home_event_filter, name="home_event_filter"),
    path('all_peoples/',views.all_peoples, name="all_peoples"),
    path('ajax_add/<str:model_name>/',views.ajax_add, name="ajax_add"),
    path('ajax_edit/<str:model_name>/<int:pk>/',views.ajax_edit, name="ajax_edit"),
    path('ajax_delete/<str:model_name>/<int:pk>/',views.ajax_delete, name="ajax_delete"),

    #dummy
    path('ajax_add/<str:model_name>/',views.ajax_add, name="ajax_add"),  
    path('profile/<int:pk>',views.profile, name="profile"),    
    path('report_people/<int:pk>',views.report_people, name="report_people"),
    #authentication
    re_path(r'^google-login/$', views.google_login, name="google_login"),     
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "registration/reset_password.html",from_email='Music Forum <noreply@screenwriters.in>'), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "registration/password_reset_sent.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "registration/password_reset_form.html"), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "registration/password_reset_done.html"), name ='password_reset_complete'),
    path('get_inbox_chat/<int:user>/',views.get_inbox_chat, name="get_inbox_chat"),
    path('chat_to/<int:user>/',views.chat_to, name="chat_to"),
    path('block_unblock/<int:pk>/',views.ajax_block_unblock, name="block_unblock"),
    path('inbox/',views.inbox, name="inbox"),
    path('view_gurukulam_request/',views.view_gurukulam_request, name="view_gurukulam_request"),    
    path('home_musician_search/',views.musician_search, name="event_home_musician_search"),
    path('home_troupe_search/',views.troupe_search, name="event_home_troupe_search"),
    path('home_gurukulam_search/',views.gurukulam_search, name="event_home_gurukulam_search"),

    path('people_filter/',views.people_filter, name="people_filter"),
    path('registered-successfully/',views.registered_successfully, name="registered-successfully"),
    
    path('location_based_events/',views.location_based_events, name="location_based_events"),

    path('view_musicians/',views.view_musicians, name="view_musicians"),
    path('view_bands/',views.view_bands, name="view_bands"),
    path('view_organizers/',views.view_organizers, name="view_organizers"),
    path('view_music_schools/',views.view_music_schools, name="view_music_schools"),

    #new
    path('update_location/',views.update_location, name="update_location"), 
    path('update_webtour/',views.update_webtour, name="update_webtour"),
    
    path('landing-search/',views.find_people, name="find_people"),
    #path('bookmark/<int:event_id>/', views.bookmark_event, name='bookmark_event'),
    
    #apiviews
    path('api/login/',views.Login_View.as_view(), name='api_login'),
    path('api/signup/', views.Signup_View.as_view(), name='api_signup'),
    path('api/password_reset/', views.Password_Reset.as_view(), name='password_reset'),
    path('api/location/', views.Location_API.as_view(), name='api_location'),
    path('api/my_profile/',views.My_Profile_View.as_view(), name="api_my_profile"),
    path('api/musician_edit/',views.Musician_Edit_Api.as_view(), name="api_musician_edit"),
    path('api/musicschool_edit/',views.Musicschool_Edit_Api.as_view(), name="api_musicschool_edit"),
    path('api/band_edit/',views.Band_Edit_Api.as_view(), name="api_band_edit"),
    path('api/musiclover_edit/',views.Musiclover_Edit_Api.as_view(), name="api_musiclover_edit"),
    path('api/event_organizer_edit/',views.Event_Edit_Api.as_view(), name="api_event_edit"),
    path('api/view_profile/<int:pk>/',views.View_Profile.as_view(), name="api_view_profile"),
    path('api/posts/',views.Post_View.as_view(), name='post_view'),
    path('api/post_comment/<int:pk>/',views.Post_Comment_Api.as_view(), name="api_post_comment"),
    path('api/like_unlike/<int:pk>/',views.Like_Unlike.as_view(), name="api_like_unlike"),
    path('api/post_comment_delete/<int:pk>/',views.Post_Comment_Delete.as_view(), name="api_post_comment_delete"),
    path('api/load_more_post/',views.Load_More_Post.as_view(), name="api_load_more_post"),
    path('api/following/',views.Following_API.as_view(), name="api_following"),
    path('api/followers/',views.Followers_API.as_view(), name="api_followers"),
    path('api/musiclover/',views.Musiclover_API.as_view(), name="api_musiclover"),
    path('api/event_like_unlike/<int:pk>/',views.Event_Like_Unlike_API.as_view(), name="api_event_like_unlike"),

    path('api/follow/<int:pk>/',views.Follow_API.as_view(), name="api_follow"),
    path('api/unfollow/<int:pk>/',views.Unfollow_API.as_view(), name="api_unfollow"),

    path('api/all_people/',views.All_People_API.as_view(), name="api_all_people"),
    path('api/chat_box/',views.Chatbox_API.as_view(), name="api_chatbox"),
    path('api/get_message/<int:pk>/',views.Get_Message_API.as_view(), name="api_getmessage"),
    path('api/put_message/<int:pk>/',views.Put_Message_API.as_view(), name="api_putmessage"),
    path('api/recommended_peoples/',views.Recommended_People_API.as_view(), name="api_recommended_peoples"),
    path('api/recent_followers/',views.Recent_Followers_API.as_view(), name="api_recent_followers"),
    path('api/people_filter/', views.People_Filter_API.as_view(), name='api_people_filter'),


    #add
    path('api/musician_skill_add/',views.Musician_Myskill_Add.as_view(), name="api_musician_myskill_add"),
    path('api/musician_school_add/',views.Musician_Myschool_Add.as_view(), name="api_musician_myshool_add"),
    path('api/musician_award_add/',views.Musician_Myaward_Add.as_view(), name="api_musician_myaward_add"),
    path('api/myhighlight_add/',views.Myhighlight_Add.as_view(), name="api_myhighlight_add"),
    path('api/musicschool_skill_add/',views.Musicschool_Myskill_Add.as_view(), name="api_musicschool_myskill_add"),
    path('api/musicschool_award_add/',views.Musicschool_Myaward_Add.as_view(), name="api_musicschool_myaward_add"),
    path('api/musicschool_lecture_videos_add/',views.Musicschool_Lecture_Videos_Add.as_view(), name="api_musicschool_lecture_videos_add"),
    path('api/event_performer_add/',views.Event_Performer_Add.as_view(), name="api_event_performer_add"),
    path('api/band_skill_add/',views.Band_Myskill_Add.as_view(), name="api_band_myskill_add"),
    path('api/band_performer_add/',views.Band_Performer_Add.as_view(), name="api_band_performer_add"),

    #edit
    path('api/musician_skill_edit/<int:pk>/',views.Musician_Myskill_Edit.as_view(), name="api_musician_myskill_edit"),
    path('api/musician_school_edit/<int:pk>/',views.Musician_Myschool_Edit.as_view(), name="api_musician_myshool_edit"),
    path('api/musician_award_edit/<int:pk>/',views.Musician_Myaward_Edit.as_view(), name="api_musician_myaward_edit"),
    path('api/highlight_edit/<int:pk>/',views.Myhighlight_Edit.as_view(), name="api_myhighlight_edit"),
    path('api/musicschool_skill_edit/<int:pk>/',views.Musicschool_Myskill_Edit.as_view(), name="api_musicschool_myskill_edit"),
    path('api/musicschool_award_edit/<int:pk>/',views.Musicschool_Award_Edit.as_view(), name="api_musicschool_award_edit"),
    path('api/musicschool_lecture_videos_edit/<int:pk>/',views.Musicschool_Lecture_Videos_Edit.as_view(), name="api_musicschool_lecture_videos_edit"),
    path('api/event_performer_edit/<int:pk>/',views.Event_Performer_Edit.as_view(), name="api_event_performer_edit"),
    path('api/band_skill_edit/<int:pk>/',views.Band_Myskill_Edit.as_view(), name="api_band_myskill_edit"),
    path('api/band_performer_edit/<int:pk>/',views.Band_Performer_Edit.as_view(), name="api_band_performer_edit"),

    #delete
    path('api/delete/<str:model_name>/<int:pk>/',views.Delete.as_view(), name="api_delete"),

    path('api/musician_association_school_add/',views.Musician_Association_Myschool_Add.as_view(), name="api_musician_association_myshool_add"),

    path('api/report_people/<int:pk>/',views.Report_People_API.as_view(), name="report_people_api"),

    path('update_name',views.update_name, name="update_name"),

    
        
]