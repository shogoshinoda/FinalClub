from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.template import loader
from .models import Users, UserProfiles, UserAffiliation


# ベース
class SnsBaseView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = Users.objects.get(id=self.request.user.id)







        def post(self, request, *args, **kwargs):
            book_form = forms.BookForm(request.POST or None)
            if book_form.is_valid():
                book_form.save()
            return render(request, 'index.html', context={
                'book_form': book_form,
            })