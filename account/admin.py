from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import User, Music_Lover, Troupe, Event_Organizer, Gurukulam, Location, Musician, Musician_Award, Musician_Highlight, Highlight_Category, Musician_Skill, Skill, Skill_Level, Skill_Category, Musician_Gurukulam, Gurukulam_Skill, Gurukulam_Award, Gurukulam_Testimonial, Lecture_Video, Course,Troupe_Highlight, Key_Performer, Troupe_Skill, Event_Organizer_Highlight, Event_Performer, Post, UserFollowing, Reply, Post_Comment,  Highlight, Gurukulam_Teacher,Report_People, Conversation
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from import_export import resources, fields
from import_export.widgets import  ForeignKeyWidget,ManyToManyWidget

# Register your models here.

admin.site.site_header = "CARNATIC MUSIC FORUM"
admin.site.site_title = "CARNATIC MUSIC FORUM"

admin.site.register(Music_Lover)

class MusicianInlineAdmin(admin.TabularInline):
    model = Musician
    

class OrganizerInlineAdmin(admin.TabularInline):
    model = Event_Organizer

class MusicschoolInlineAdmin(admin.TabularInline):
    model = Gurukulam


class BandInlineAdmin(admin.TabularInline):
    model = Troupe




class UserResource(resources.ModelResource):

  location = fields.Field(
    column_name ="location",
    attribute='location',
    widget= ForeignKeyWidget(Location,'name')
  )

                    
  def before_import_row(self,row, **kwargs):
      row['password'] = make_password(row['password'])        
                    
      group=Group.objects.get(name=row['user_groups'])
      row['groups'] = group.id 
      



  class Meta:
    model = User
    exclude = ('name','last_login','is_superuser','user_permissions','last_name','verified_email','profile_picture','cover_picture','instagram','twitter','email_subscription')
    #fields = ['id','usernname','password','first_name','groups','is_staff','address','mobile_no','location','is_active']

    skip_unchanged = True
    report_skipped = True

    def skip_row(self, instance, original):
        return True if User.objects.filter(username=instance.email).exists() else False




@admin.register(User)
class UserModelAdmin(ImportExportModelAdmin):
    resource_class = UserResource
    list_display = ['username']
    list_filter = ['groups',]
    inlines = [MusicianInlineAdmin,OrganizerInlineAdmin,MusicschoolInlineAdmin,BandInlineAdmin]


    def save_model(self, request, obj, form, change):       

        if 'password' in form.changed_data:
            obj.password = make_password(form.cleaned_data.get('password'))    
                    
        obj.username= form.cleaned_data.get('email')
        super().save_model(request, obj, form, change)


@admin.register(UserFollowing)
class UserFollowingModelAdmin(admin.ModelAdmin):
    list_filter = ['following_user_id',]





@admin.register(Conversation)
class ConversationModelAdmin(admin.ModelAdmin):
    list_display = ['sender','receiver']


class MusicianResource(resources.ModelResource):
  user = fields.Field(
    column_name ="username",
    attribute='user',
    widget= ForeignKeyWidget(User,'username')
  )

  class Meta:
    model = Musician
    exclude = ('dob','gender','about_me',)
    #fields = ['id','usernname','password','first_name','groups','is_staff','address','mobile_no','location','is_active']

    skip_unchanged = True
    report_skipped = True

    def skip_row(self, instance, original):
        return True if Musician.objects.filter(username=instance.user.username).exists() else False




@admin.register(Musician)
class MusicianModelAdmin(ImportExportModelAdmin):
    resource_class = MusicianResource
    list_display = ['user','dob']
    list_filter = ['musician_skill','user__location','gender','musician_skill__skill_level']




class GurukulamResource(resources.ModelResource):
  user = fields.Field(
    column_name ="username",
    attribute='user',
    widget= ForeignKeyWidget(User,'username')
  )

  class Meta:
    model = Gurukulam
    exclude = ('dob','about_us',)
    #fields = ['id','usernname','password','first_name','groups','is_staff','address','mobile_no','location','is_active']

    skip_unchanged = True
    report_skipped = True

    def skip_row(self, instance, original):
        return True if Gurukulam.objects.filter(username=instance.user.username).exists() else False


@admin.register(Gurukulam)
class GurukulamModelAdmin(ImportExportModelAdmin):
    resource_class = GurukulamResource
    list_display = ['user',]



class TroupeResource(resources.ModelResource):
  user = fields.Field(
    column_name ="username",
    attribute='user',
    widget= ForeignKeyWidget(User,'username')
  )

  class Meta:
    model = Troupe
    exclude = ('president','about_us',)

    skip_unchanged = True
    report_skipped = True

    def skip_row(self, instance, original):
        return True if Troupe.objects.filter(username=instance.user.username).exists() else False


@admin.register(Troupe)
class TroupeModelAdmin(ImportExportModelAdmin):
    resource_class = TroupeResource
    list_display = ['user',]


class Event_OrganizerResource(resources.ModelResource):
  user = fields.Field(
    column_name ="username",
    attribute='user',
    widget= ForeignKeyWidget(User,'username')
  )

  class Meta:
    model = Event_Organizer
    exclude = ('president','about_us',)

    skip_unchanged = True
    report_skipped = True

    def skip_row(self, instance, original):
        return True if Troupe.objects.filter(username=instance.user.username).exists() else False


@admin.register(Event_Organizer)
class TroupeModelAdmin(ImportExportModelAdmin):
    resource_class = Event_OrganizerResource
    list_display = ['user',]
    

@admin.register(Musician_Skill)
class MusicianSkillModelAdmin(ImportExportModelAdmin):    
    list_display = ['musician','skill','skill_level','teach','perform']
    list_filter = ['musician','skill','skill_level','teach','perform']


admin.site.register(Troupe_Skill)
admin.site.register(Location)
admin.site.register(Event_Performer)
admin.site.register(Musician_Award)
admin.site.register(Musician_Highlight)
admin.site.register(Highlight_Category)

admin.site.register(Skill)
admin.site.register(Skill_Level)
admin.site.register(Skill_Category)
admin.site.register(Musician_Gurukulam)
admin.site.register(Gurukulam_Skill)
admin.site.register(Gurukulam_Award)
admin.site.register(Gurukulam_Testimonial)
admin.site.register(Lecture_Video)
admin.site.register(Course)
admin.site.register(Troupe_Highlight)
admin.site.register(Key_Performer)
admin.site.register(Event_Organizer_Highlight)


admin.site.register(Post)
admin.site.register(Post_Comment)
admin.site.register(Reply)
admin.site.register(Highlight)
admin.site.register(Gurukulam_Teacher)
admin.site.register(Report_People)