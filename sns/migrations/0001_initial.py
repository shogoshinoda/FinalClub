# Generated by Django 3.2.9 on 2022-06-15 02:48

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=40, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Boards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture1', models.FileField(blank=True, null=True, upload_to='board_pictures/%Y/%m/%d/')),
                ('picture2', models.FileField(blank=True, null=True, upload_to='board_pictures/%Y/%m/%d/')),
                ('picture3', models.FileField(blank=True, null=True, upload_to='board_pictures/%Y/%m/%d/')),
                ('picture4', models.FileField(blank=True, null=True, upload_to='board_pictures/%Y/%m/%d/')),
                ('picture5', models.FileField(blank=True, null=True, upload_to='board_pictures/%Y/%m/%d/')),
                ('picture6', models.FileField(blank=True, null=True, upload_to='board_pictures/%Y/%m/%d/')),
                ('picture7', models.FileField(blank=True, null=True, upload_to='board_pictures/%Y/%m/%d/')),
                ('picture8', models.FileField(blank=True, null=True, upload_to='board_pictures/%Y/%m/%d/')),
                ('picture9', models.FileField(blank=True, null=True, upload_to='board_pictures/%Y/%m/%d/')),
                ('picture10', models.FileField(blank=True, null=True, upload_to='board_pictures/%Y/%m/%d/')),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('create_at', models.DateTimeField(default=datetime.datetime(2022, 6, 15, 11, 48, 38, 664430))),
                ('update_at', models.DateTimeField(default=datetime.datetime(2022, 6, 15, 11, 48, 38, 664440))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'boards',
            },
        ),
        migrations.CreateModel(
            name='DMBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(default=datetime.datetime(2022, 6, 15, 11, 48, 38, 665504))),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partner', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'dm_box',
            },
        ),
        migrations.CreateModel(
            name='UserProfiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('user_icon', models.FileField(upload_to='user_icon/%Y/%m/%d/')),
                ('introduction', models.TextField(blank=True, max_length=255, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'profiles',
            },
        ),
        migrations.CreateModel(
            name='UserInviteToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invite_token', models.UUIDField(db_index=True)),
                ('available', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'invite_token',
            },
        ),
        migrations.CreateModel(
            name='UserAffiliation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_of_admission', models.CharField(max_length=5)),
                ('department', models.CharField(max_length=10)),
                ('course', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_affiliation',
            },
        ),
        migrations.CreateModel(
            name='UserActivateTokens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.UUIDField(db_index=True)),
                ('expired_at', models.DateTimeField(default=datetime.datetime(2022, 6, 15, 12, 48, 38, 663564))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_activate_tokens',
            },
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_id', models.IntegerField()),
                ('action_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='action_user', to=settings.AUTH_USER_MODEL)),
                ('board', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sns.boards')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'notifications',
            },
        ),
        migrations.CreateModel(
            name='FollowFollowerUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(default=datetime.datetime(2022, 6, 15, 11, 48, 38, 665278))),
                ('follow_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_user', to=settings.AUTH_USER_MODEL)),
                ('follower_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'follow_follower_user',
            },
        ),
        migrations.CreateModel(
            name='DMMessages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('sender', models.IntegerField()),
                ('create_at', models.DateTimeField(default=datetime.datetime(2022, 6, 15, 11, 48, 38, 665723))),
                ('dm_box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sns.dmbox')),
            ],
            options={
                'db_table': 'dm_message',
            },
        ),
        migrations.CreateModel(
            name='BoardsLikes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sns.boards')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'boards_likes',
            },
        ),
        migrations.CreateModel(
            name='BoardsComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=100)),
                ('create_at', models.DateTimeField(default=datetime.datetime(2022, 6, 15, 11, 48, 38, 665046))),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sns.boards')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'boards_comments',
            },
        ),
    ]
