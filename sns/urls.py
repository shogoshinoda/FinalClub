from django.urls import path
from .views import (
    SigninView, TemporaryRegistView, MainRegistView, LoginView,
    RegistCompleteView, CreateProfileView, HomeView, LogoutView,
    UserHomeView, BoardView, AccountsEditView, AccountsPasswordChangeView,
    FollowListView, FollowerListView
)
app_name = 'sns'
urlpatterns = [
    path('signin/', SigninView.as_view(), name='signin'),
    path('temporary_regist/', TemporaryRegistView.as_view(), name='temporary_regist'),
    path('main_regist/<uuid:token>', MainRegistView.as_view(), name='main_regist'),
    path('regist_complete/', RegistCompleteView.as_view(), name='regist_complete'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('', HomeView.as_view(), name='home'),
    path('<str:host_user>/', UserHomeView.as_view(), name='user_home'),
    path('p/<str:board_id>/', BoardView.as_view(), name='board'),
    path('accounts/edit/', AccountsEditView.as_view(), name='accounts_edit'),
    path('accounts/password/change', AccountsPasswordChangeView.as_view(), name='accounts_password_change'),
    path('<str:host_user>/follow/', FollowListView.as_view(), name='follow_list'),
    path('<str:host_user>/follower/', FollowerListView.as_view(), name='follower_list'),
]