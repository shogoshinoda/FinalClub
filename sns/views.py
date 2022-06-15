from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.base import View
from django.template import loader
from .models import Users, UserProfiles, UserAffiliation
from .forms import SignInForm


# ユーザ登録
class SignInView(CreateView):
    template_name = 'sns/sing_in.html'
    form_class = SignInForm








# ベース
class SnsBaseView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = Users.objects.get(id=self.request.user.id)






