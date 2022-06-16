from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import UserChangeForm, UserCreationForm

from .models import (
    Users, UserActivateTokens, UserInviteToken, UserProfiles,
    Boards, FollowFollowerUser, DMBox, Notifications, UserAffiliation
)

admin.site.register(Users)
admin.site.register(UserActivateTokens)
admin.site.register(UserInviteToken)
admin.site.register(UserProfiles)
admin.site.register(Boards)
admin.site.register(FollowFollowerUser)
admin.site.register(DMBox)
admin.site.register(Notifications)
admin.site.register(UserAffiliation)
