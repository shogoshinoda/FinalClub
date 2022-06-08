import re
from datetime import datetime

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import (Users, UserProfiles, Boards,
                     BoardsComments, DMMessages)

User = get_user_model()


# アドミン画面ユーザ作成
class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Password再入力', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('パスワードが一致しません')

    def save(self, commit=False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        user.save()
        return user


# アドミン画面ユーザ変更
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_staff', 'is_active', 'is_superuser')

    def clean_password(self):
        # すでに登録されているパスワードを返す
        return self.initial['password']


# ユーザ登録
class SignInForm(forms.ModelForm):
    email = forms.EmailField(label='メールアドレス', required=True)
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='パスワード(確認)', widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ['email', 'password', 'confirm_password']

    # パスワードの確認
    def clean_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('パスワードが一致しません')
        return password

    # メールアドレスの確認
    def clean_email(self):
        email = self.cleaned_data['email']
        meijo_email: str = '@ccmailg.meijo-u.ac.jp'
        if not re.search(f'{ meijo_email }\Z', email):
            raise forms.ValidationError('名城大学のメールアドレスを入力してください')
        return email

    # 保存
    def save(self, commit=False):
        user = super().save(commit=False)
        password = self.cleaned_data['password']
        user.set_password(password)
        user.save()
        return user


# ユーザログイン
class UserLoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    remember = forms.BooleanField(label='ログイン状態維持', required=False)


# プロフィール作成フォーム
class ProfileForm(forms.ModelForm):
    user_id = forms.CharField(label='ユーザID')
    username = forms.CharField(label='ユーザ名')
    user_icon = forms.FileField(label='ユーザアイコン')
    introduction = forms.CharField(label='自己紹介', widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}))

    class Meta:
        model = UserProfiles
        fields = ['user_id', 'username', 'user_icon', 'introduction']


# プロフィール更新フォーム
class UpdateProfileForm(forms.ModelForm):
    username = forms.CharField(label='ユーザ名')
    user_icon = forms.FileField(label='ユーザアイコン')
    introduction = forms.CharField(label='自己紹介', widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}))

    class Meta:
        model = UserProfiles
        fields = ['username', 'user_icon', 'introduction']


# 提示版作成フォーム
class BoardsForm(forms.ModelForm):
    picture1 = forms.FileField(label='')
    picture2 = forms.FileField(label='')
    picture3 = forms.FileField(label='')
    picture4 = forms.FileField(label='')
    picture5 = forms.FileField(label='')
    picture6 = forms.FileField(label='')
    picture7 = forms.FileField(label='')
    picture8 = forms.FileField(label='')
    picture9 = forms.FileField(label='')
    picture10 = forms.FileField(label='')
    description = forms.CharField(label='コメント', widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}))

    class Meta:
        model = Boards
        fields = ['picture1', 'picture2', 'picture3', 'picture4', 'picture5',
                  'picture6', 'picture7', 'picture8', 'picture9', 'picture10',
                  'description']

    def save(self, commit=True):
        boards = super().save(commit=False)
        boards.create_at = datetime.now()
        boards.update_at = datetime.now()
        boards.save()
        return boards


# 掲示板更新フォーム
class BoardsUpdateForm(forms.ModelForm):
    description = forms.CharField(label='コメント', widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}))

    class Meta:
        models = Boards
        fields = ['description']

    def save(self, *args, **kwargs):
        boards = super(BoardsUpdateForm, self).save(commit=False)
        boards.update_at = datetime.now()
        boards.save()
        return boards


# 提示版コメントフォーム
class BoardsCommentForm(forms.ModelForm):
    comment = forms.CharField(label='コメント', widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}))

    class Meta:
        models = BoardsComments
        fields = ['comment']


# DMメッセージフォーム
class DMMessageForm(forms.ModelForm):
    message = forms.CharField()

    class Meta:
        models = DMMessages
        fields = ['message']



