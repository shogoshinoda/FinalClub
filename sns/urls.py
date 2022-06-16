from django.urls import path
from .views import (
    SigninView, TemporaryRegistView, MainRegistView
)
app_name = 'sns'
urlpatterns = [
    path('signin/', SigninView.as_view(), name='signin'),
    path('temporary_regist/', TemporaryRegistView.as_view(), name='temporary_regist'),
    path('main_regist/<uuid:token>', MainRegistView.as_view(), name='main_regist'),
    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
]
