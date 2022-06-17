from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login

from .models import (Users, UserProfiles, UserAffiliation,
                     UserActivateTokens, UserInviteToken)
from .forms import (SignInForm, InviteVerificationForm, LoginForm)


# ユーザ登録
class SigninView(TemplateView):
    template_name = 'sns/signin.html'
    signin_form_class = SignInForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['signin_form'] = self.signin_form_class
        return context

    def post(self, request,  *args, **kwargs):
        signin_form = self.signin_form_class(request.POST or None)
        context = self.get_context_data(signin_form=signin_form)
        if signin_form.is_valid():
            self.form_save(signin_form)
            email = request.POST.get('email')
            user = Users.objects.get(email=email)
            create_user_token = UserActivateTokens.objects.create_user_by_token(user=user)
            create_user_affiliation = UserAffiliation.objects.create_user_affiliation(user=user)
            user_activate_token = UserActivateTokens.objects.get(user=user)
            subject = '仮登録受付完了'
            message = f'http://127.0.0.1:8000/main_regist/{user_activate_token.token}'
            from_email = 'meijo.sns@gmail.com'
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            return redirect('sns:temporary_regist')
        else:
            context = {
                'signin_form': signin_form
            }
            return render(self.request, 'sns/signin.html', context)
    
    def form_save(self, form):
        obj = form.save()
        return obj


# 仮登録
class TemporaryRegistView(TemplateView):
    template_name = 'sns/temporary_regist.html'


# 本登録画面
class MainRegistView(TemplateView):
    template_name = 'sns/main_regist.html'
    invite_verification_form_class = InviteVerificationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invite_verification_form'] = self.invite_verification_form_class
        return context
    
    def post(self, request, *args, **kwargs):
        user = UserActivateTokens.objects.get(token=self.kwargs.get('token')).user
        invite_verification_form = self.invite_verification_form_class(request.POST or None)
        if invite_verification_form.is_valid():
            invite_user_email = request.POST.get('invite_user')
            invite_user = Users.objects.get(email=invite_user_email)
            invite_code = request.POST.get('invite_code')
            if UserInviteToken.objects.filter(invite_token=invite_code, user=invite_user).exists():
                user_invite_token = UserInviteToken.objects.get(invite_token=invite_code)
                if user_invite_token.available:
                    UserInviteToken.objects.available_false(token=invite_code)
                    user_activate_token = UserActivateTokens.objects.activate_user_by_token(self.kwargs.get('token'))
                    return redirect('sns:login')
                else:
                    raise forms.ValidationError('招待コードが有効ではありません。')
            else:
                raise forms.ValidationError('招待主または招待コードが異なります。')
        else:
            context = {
                'invite_verification_form': invite_verification_form
            }
            return render(self.request, 'sns/main_regist.html', context)

# ログイン画面
class LoginView(TemplateView):
    template_name = 'sns/login.html'
    login_form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = self.login_form_class
        return context

    def post(self, request, *args, **kwargs):
        login_form = self.login_form_class(request.POST or None)
        if login_form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            remember = request.POST['remember']
            if remember:
                self.request.session.set_expiry(10368000) # ログイン状態保持にチェックがある場合120日ログイン状態保持
            user = authenticate(email=email, password=password)
            next_url = request.POST.get('next')
            if user is not None and user.is_active:
                login(request, user)
            else:
                raise ValueError('メールアドレスもしくはパスワードが間違っています。')
            try:
                UserProfiles.objects.get(user_id=self.request.user.id)
                if next_url:
                    return redirect(next_url)
                else:
                    redirect('sns:home')
            except:
                return redirect('sns:create_profile')
        else:
            context = {
                'login_form': login_form
            }
            return render(self.request, 'sns/login.html', context)