import re
from datetime import datetime
from string import ascii_uppercase, ascii_lowercase, digits

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import (Users, UserProfiles, Boards,
                     BoardsComments, DMMessages)


# アドミン画面ユーザ作成
class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Password再入力', widget=forms.PasswordInput)

    class Meta:
        model = Users
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
        model = Users
        fields = ('email', 'password', 'is_staff', 'is_active', 'is_superuser')

    def clean_password(self):
        # すでに登録されているパスワードを返す
        return self.initial['password']


def contain_any(password, condition_list):
    return any([i in password for i in condition_list])


# ユーザ登録
class SignInForm(forms.ModelForm):
    email = forms.EmailField(label='メールアドレス', required=True)
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='パスワード(確認)', widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ['email', 'password', 'confirm_password']

    # パスワードの確認
    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        bool_length = len(password) >= 6
        if not all([contain_any(password, ascii_lowercase),
                    contain_any(password, ascii_uppercase),
                    contain_any(password, digits),
                    bool_length]):
            raise forms.ValidationError('6文字以上で半角英語、全角英語、数字を含めてください')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('パスワードが一致しません')
        return confirm_password

    # メールアドレスの確認
    def clean_email(self):
        email = self.cleaned_data['email']
        meijo_email: str = '@ccmailg.meijo-u.ac.jp'
        student_number = email[:9]
        if not student_number.isdecimal():
            raise forms.ValidationError('正しいメールアドレスを入力してください')
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


# 本登録画面フォーム
class InviteVerificationForm(forms.Form):
    invite_user = forms.CharField(label='招待主', required=True)
    invite_code = forms.UUIDField(label='招待コード',required=True)
    agree = forms.BooleanField(label='同意',required=True)


# ユーザログイン
class LoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    remember = forms.BooleanField(label='ログイン状態維持', required=False)


# プロフィール作成フォーム
class ProfileForm(forms.ModelForm):
    username = forms.CharField(label='ユーザネーム')
    nickname = forms.CharField(label='名前')
    user_icon = forms.ImageField(label='ユーザアイコン')
    introduction = forms.CharField(label='自己紹介', widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}))

    class Meta:
        model = UserProfiles
        fields = ['username', 'nickname', 'user_icon', 'introduction']


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
