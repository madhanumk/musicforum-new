# Generated by Django 3.2.2 on 2023-04-04 14:27

import account.managers
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=60, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('name', models.CharField(blank=True, max_length=400, verbose_name='name')),
                ('email', models.EmailField(max_length=254, null=True, unique=True, verbose_name='email address')),
                ('verified_email', models.BooleanField(default=False)),
                ('address', models.TextField(blank=True, null=True)),
                ('mobile_no', models.CharField(blank=True, max_length=10, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='')),
                ('cover_picture', models.ImageField(blank=True, null=True, upload_to='')),
                ('registered_on', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', account.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Blocked_User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('message', models.TextField()),
                ('unread', models.BooleanField(default=True)),
                ('m_file', models.FileField(blank=True, null=True, upload_to='message_file')),
            ],
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=100)),
                ('age_limit', models.PositiveIntegerField()),
                ('overview', models.TextField()),
                ('prerequisite', models.TextField()),
                ('learning_outcome', models.TextField()),
                ('others', models.TextField()),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Event_Organizer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about_us', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event_Organizer_Highlight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('video_link', models.URLField()),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Event_Performer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('', 'Choose Status'), ('A', 'Accept'), ('R', 'Reject'), ('S', 'Sent')], default='A', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Gurukulam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_no', models.CharField(blank=True, max_length=10, null=True)),
                ('about_us', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gurukulam_Award',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('photo', models.ImageField(upload_to='gurukulam/award')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Gurukulam_Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Gurukulam_Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('', 'Choose '), ('A', 'Accept'), ('R', 'Reject'), ('S', 'Sent')], max_length=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gurukulam_Testimonial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testimonial', models.TextField()),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Highlight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('video_link', models.URLField()),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Highlight_Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Key_Performer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('profile_photo', models.ImageField(blank=True, upload_to='')),
                ('status', models.CharField(choices=[('', 'Choose '), ('A', 'Accept'), ('R', 'Reject'), ('S', 'Sent')], max_length=1, null=True)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Lecture_Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('video', models.URLField()),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Musician',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateField(blank=True, help_text='Date of Birth', null=True)),
                ('gender', models.CharField(choices=[('', 'Choose Gender'), ('M', 'Male'), ('F', 'Female'), ('T', 'Transgender'), ('N', 'None')], max_length=1, null=True)),
                ('profession', models.CharField(max_length=50)),
                ('about_me', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Musician_Award',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(null=True, upload_to='musician_award')),
            ],
        ),
        migrations.CreateModel(
            name='Musician_Gurukulam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('', 'Choose '), ('A', 'Accept'), ('R', 'Reject'), ('S', 'Sent')], max_length=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Musician_Highlight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('video_link', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Musician_Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teach', models.BooleanField(default=False)),
                ('perform', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('posted_on', models.DateTimeField(auto_now_add=True)),
                ('likes', models.PositiveIntegerField(default=0)),
                ('highlight', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.highlight')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Post_Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('commented_on', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Skill_Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Skill_Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Troupe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('president', models.CharField(blank=True, max_length=100)),
                ('about_us', models.TextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='troupe', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserFollowing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('following_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Troupe_Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.skill')),
                ('troupe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='troupe_skill', to='account.troupe')),
            ],
        ),
        migrations.CreateModel(
            name='Troupe_Highlight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400)),
                ('video_link', models.URLField()),
                ('highlight_category', models.ManyToManyField(to='account.Highlight_Category')),
                ('troupe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.troupe')),
            ],
        ),
        migrations.AddField(
            model_name='skill',
            name='skill_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.skill_category'),
        ),
        migrations.CreateModel(
            name='Report_People',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reported_on', models.DateField(auto_now=True)),
                ('complaint', models.TextField(blank=True)),
                ('report_file', models.FileField(blank=True, upload_to='report file')),
                ('is_active', models.BooleanField(default=True)),
                ('reported_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_by', to=settings.AUTH_USER_MODEL)),
                ('reported_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('reply', models.TextField(max_length=1000)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.post_comment')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
