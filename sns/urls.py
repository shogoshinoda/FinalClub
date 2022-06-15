from django.urls import path
from .views import (
    SignInView
)
app_name = 'sns'
urlpatterns = [
    path('SignIn/', SignInView.as_view(), name='SignIn'),

]
