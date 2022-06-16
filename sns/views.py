from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.template import loader
from django.http import Http404
from django.core.mail import send_mail

from .models import (Users, UserProfiles, UserAffiliation,
                     UserActivateTokens, UserInviteToken)
from .forms import SignInForm, InviteVerificationForm


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
            print(email)
            print(user)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invite_verification_form = InviteVerificationForm()
        context['invite_verification_form'] = invite_verification_form
        return context
    
    def get(self, *args, **kwargs):
        user = Users.objects.get(id=self.request.user.id)
        activate_token_user = UserActivateTokens.objects.get(token=self.kwargs.get('token'))
        if user.id == activate_token_user.user.id:
            Http404('このページは見つかりません')
        return super().get(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        invite_verification_form = InviteVerificationForm(request.POST or None)
        if invite_verification_form.is_valid():
            invite_user = invite_verification_form.invite_user
            invite_code = invite_verification_form.invite_code
            if UserInviteToken.objects.filter(user=invite_user, invite_token=invite_code).exists():
                user_invite_token = UserInviteToken.objects.get(invite_token=invite_code)
                if user_invite_token.available:
                    user_invite_token.available = False
                    user_activate_token = UserActivateTokens.objects.activate_user_by_token(self.kwargs.get('token'))
                    return redirect('sns:login')
            raise forms.ValidationError('招待主または招待コードが異なります。')



# ベース
# class SnsBaseView(LoginRequiredMixin, View):

#     def get(self, request, *args, **kwargs):
#         user = Users.objects.get(id=self.request.user.id)






