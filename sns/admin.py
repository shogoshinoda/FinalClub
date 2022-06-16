from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import UserChangeForm, UserCreationForm

from .models import (
    UserActivateTokens, UserInviteToken, UserProfiles,
    Boards, FollowFollowerUser, DMBox, Notifications
)
User = get_user_model()


class CustomizeUserAdmin(UserAdmin):
    form = UserChangeForm  # ユーザ編集画面でつかうForm
    add_form = UserCreationForm  # ユーザ作成画面

    # 一覧画面で表示する
    list_display = ('email', 'is_staff')

    # ユーザ編集画面で表示する要素
    fieldsets = (
        ('ユーザ情報', {'fields': ('email', 'password')}),
        ('パーミッション', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )

    add_fieldsets = (
        ('ユーザ情報', {
            'fields': ('username', 'email', 'password', 'confirm_password')
        }),
    )


admin.site.register(User, CustomizeUserAdmin)
admin.site.register(UserActivateTokens)
admin.site.register(UserInviteToken)
admin.site.register(UserProfiles)
admin.site.register(Boards)
admin.site.register(FollowFollowerUser)
admin.site.register(DMBox)
admin.site.register(Notifications)
