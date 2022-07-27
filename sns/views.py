import string
import random
from datetime import datetime, timedelta
from xmlrpc.client import FastMarshaller
from string import ascii_uppercase, ascii_lowercase, digits
import pytz
import re

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.utils.timezone import now
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import (FollowFollowerUser, Users, UserProfiles, UserAffiliation,
                     UserActivateTokens, UserInviteToken, Boards,
                     BoardsLikes, BoardsComments, Notifications)
from .forms import (SignInForm, InviteVerificationForm, LoginForm,
                    ProfileForm, BoardsForm,)


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
            try:
                invite_user = Users.objects.get(email=invite_user_email)
            except:
                messages.error(self.request, '招待主または招待コードが異なります。')
                context = {
                    'invite_verification_form': invite_verification_form
                }
                return render(self.request, 'sns/main_regist.html', context)
            invite_code = request.POST.get('invite_code')
            if UserInviteToken.objects.filter(invite_token=invite_code, user=invite_user).exists():
                user_invite_token = UserInviteToken.objects.get(invite_token=invite_code)
                if user_invite_token.available:
                    UserInviteToken.objects.available_false(token=invite_code)
                    user_activate_token = UserActivateTokens.objects.activate_user_by_token(self.kwargs.get('token'))
                    return redirect('sns:regist_complete')
                else:
                    messages.error(self.request, '招待コードが有効ではありません。')
                    context = {
                        'invite_verification_form': invite_verification_form
                    }
                    return render(self.request, 'sns/main_regist.html', context)
            else:
                messages.error(self.request, '招待主または招待コードが異なります。')
                context = {
                    'invite_verification_form': invite_verification_form
                }
                return render(self.request, 'sns/main_regist.html', context)
        else:
            context = {
                'invite_verification_form': invite_verification_form
            }
            return render(self.request, 'sns/main_regist.html', context)


# 本登録完了画面
class RegistCompleteView(TemplateView):
    template_name = 'sns/regist_complete.html'


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
            email = request.POST.get('email')
            password = request.POST.get('password')
            remember = request.POST.get('remember')
            if remember:
                self.request.session.set_expiry(10368000)  # ログイン状態保持にチェックがある場合120日ログイン状態保持
            user = authenticate(email=email, password=password)
            next_url = request.POST.get('next')
            if user is not None and user.is_active:
                login(request, user)
            else:
                messages.error(self.request, 'メールアドレスもしくはパスワードが間違っています。')
                context = {
                    'login_form': login_form
                }
                return render(self.request, 'sns/login.html', context)
            try:
                UserProfiles.objects.get(user_id=self.request.user.id)
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('sns:home')
            except:
                return redirect('sns:create_profile')
        else:
            context = {
                'login_form': login_form
            }
            return render(self.request, 'sns/login.html', context)


# プロフィール作成画面
class CreateProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'sns/create_profile.html'
    create_profile_form_class = ProfileForm
    login_url = reverse_lazy('sns:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_profile_form'] = self.create_profile_form_class
        return context
    
    def get(self, request, *args, **kwargs):
        user = Users.objects.get(id=self.request.user.id)
        if UserProfiles.objects.filter(user=user):
            return redirect('sns:home')
        return render(self.request, 'sns/home.html')

    def post(self, request, *args, **kwargs):
        user_icon = request.FILES.get('user_icon')
        username = request.POST.get('username')
        nickname = request.POST.get('nickname')
        user = self.request.user
        introduction = request.POST.get('introduction')
        print(user_icon)
        json_data = dict()
        error_messages = []
        if UserProfiles.objects.filter(username=username):
            error_messages.append('not_username_unique')
        if not self.match(username):
            error_messages.append('only_number_english')
        json_data['error_messages'] = error_messages
        if error_messages:
            json_data['success'] = False
            return JsonResponse(json_data)
        else:
            json_data['success'] = True
            self.form_save(username, nickname, user_icon, user, introduction)
            return JsonResponse(json_data)

    def form_save(self, username, nickname, user_icon, user, introduction):
        create_profile = UserProfiles(
            username=username,
            nickname=nickname,
            user_icon=user_icon,
            user=user, 
            introduction=introduction
        )
        create_profile.save()
        return create_profile

    def match(self, text):
        return all(re.findall('[a-zA-Z0-9\-\_.]', i) for i in text)

# ログアウト
class LogoutView(LogoutView):
    pass


# ホーム画面
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'sns/home.html'
    board_form_class = BoardsForm
    login_url = reverse_lazy('sns:login')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        user = Users.objects.get(id=self.request.user.id)
        username = UserProfiles.objects.get(user=user).username
        boards = Boards.objects.all().order_by('create_at').reverse()
        board_form = self.board_form_class
        board_items = []
        for board in boards:
            likes = BoardsLikes.objects.filter(board=board).all().count()
            like_first_people = BoardsLikes.objects.filter(board=board).first()
            comments = BoardsComments.objects.filter(board=board).all()[:2]
            comment_count = comments.count()
            if BoardsLikes.objects.filter(board=board, user=user):
                liked = 1
            else:
                liked = 0
            if FollowFollowerUser.objects.filter(follow_user=user, follower_user=board.user):
                followed = 'followed'
            elif board.user == user:
                followed = 'mine'
            else:
                followed = 'follow'
            items = {
                'item': board,
                'likes': likes,
                'liked': liked,
                'like_first_people': like_first_people,
                'comments': comments,
                'comment_count': comment_count,
                'followed': followed
            }
            board_items.append(items)
        context['boards'] = board_items
        context['board_form'] = board_form
        context['username'] = username
        notification_items = []
        notifications = Notifications.objects.filter(receiver_id=user)
        for notification in notifications:
            action_user = Users.objects.get(id=notification.action_user_id)
            action_user_profile = UserProfiles.objects.get(user=action_user)
            receiver_user = Users.objects.get(id=notification.receiver_id)
            receiver_user_profile = UserProfiles.objects.get(user=receiver_user)
            board = ''
            date = (now() - notification.create_at)
            date_days = date.days
            date_second = date.seconds
            date_minute = date_second // 60
            date_hour = date_minute // 60
            if date_second < 60:
                day = str(date_second) + '秒前'
            elif date_minute < 60:
                day = str(date_minute) + '分前'
            elif date_hour < 60:
                day = str(date_hour) + '時間前'
            else:
                for i in range(1, 8):
                    if date_days <= i * 7:
                        if i == 1:
                            day = str(date_days) + '日前'
                        day = str(i) + '週間前'
            if notification.action_id != 1:
                board = Boards.objects.get(id=notification.board_id)
            followed = ''
            if notification.action_id == 1:
                followed = FollowFollowerUser.objects.filter(follow_user=receiver_user, follower_user=action_user)
                if followed:
                    followed = True
                else:
                    followed = False
            comment = ''
            if notification.action_id == 3:
                comment = notification.comment
            items = {
                'action_id': notification.action_id,
                'action_user_profile': action_user_profile,
                'receiver_user_profile': receiver_user_profile,
                'board': board,
                'day': day,
                'followed': followed,
                'comment': comment
            }
            notification_items.append(items)
        context['notifications'] = notification_items
        return context
    
    def post(self, request, *args, **kwargs):
        user = Users.objects.get(id=self.request.user.id)
        user_profile = UserProfiles.objects.get(user=self.request.user.id)
        if request.POST.get('action_type') == 'board':
            print('success')
            picture1 = request.FILES.get('picture1')
            picture2 = request.FILES.get('picture2')
            picture3 = request.FILES.get('picture3')
            picture4 = request.FILES.get('picture4')
            picture5 = request.FILES.get('picture5')
            picture6 = request.FILES.get('picture6')
            picture7 = request.FILES.get('picture7')
            picture8 = request.FILES.get('picture8')
            picture9 = request.FILES.get('picture9')
            picture10 = request.FILES.get('picture10')
            description = request.POST.get('description')
            new_board = self.boards_form_save(user, user_profile, picture1, picture2, picture3, picture4, picture5,picture6,
                                  picture7, picture8, picture9, picture10, description)
            user_home_url = f'/{user_profile.username}/'
            data = dict()
            data['username'] = user_profile.username
            data['user_img'] = user_profile.user_icon.url
            data['user_home_url'] = user_home_url
            data['create_at'] = new_board.create_at.strftime('%Y年%m月%d日%H:%M')
            picture_count = 0
            for i in range(1, 11):
                picture = 'picture' + str(i)
                new_board_obj = 'new_board.' + picture
                new_board_obj_url = 'new_board.' + picture +'.url'
                if eval(new_board_obj):
                    data[picture] = eval(new_board_obj_url)
                    picture_count += 1
            if new_board.description:
                data['description'] = new_board.description
            data['picture_count'] = picture_count
            data['board_id'] = new_board.id
            return JsonResponse(data)
        if request.POST.get('action_type') == 'search_user':
            search_text = request.POST.get('search_text')
            results = UserProfiles.objects.filter(Q(username__icontains = search_text) | Q(nickname__icontains = search_text))
            data = dict()
            users_data = []
            count = 0
            for result in results:
                if count == 50:
                    break
                user_data = dict()
                user_data['user_icon']= result.user_icon.url
                user_data['username'] = result.username
                user_data['nickname'] = result.nickname
                user_data['user_home_url'] = f'/{result.username}/'
                users_data.append(user_data)
                count += 1
            data['users'] = users_data
            print('success')
            return JsonResponse(data)
        if request.POST.get('action_type') == 'like':
            board_id = request.POST.get('board_id')
            board = Boards.objects.get(id = board_id)
            action_user = Users.objects.get(id = self.request.user.id)
            user_profile = UserProfiles.objects.get(user=action_user)
            liking = BoardsLikes.objects.filter(board=board, user=action_user)
            like = BoardsLikes.objects.filter(board=board)
            like_count = like.count()
            json_data = dict()
            if liking:
                liking.delete()
                json_data['liked'] = 0
                json_data['like_count'] = like_count - 1
                if like_count >= 3:
                    json_data['type'] = 2
                    first_like = like.first()
                    json_data['first_like'] = first_like.user_profile.username
                    return JsonResponse(json_data)
                elif like_count == 2:
                    json_data['type'] = 1
                    first_like = like.first()
                    json_data['first_like'] = first_like.user_profile.username
                    return JsonResponse(json_data)
                else:
                    json_data['type'] = 0
                    return JsonResponse(json_data)
            else:
                board_like = BoardsLikes(
                    board = board,
                    user = action_user,
                    user_profile=user_profile,
                )
                board_like.save()
                first_like = like.first()
                json_data['first_like'] = first_like.user_profile.username
                json_data['liked'] = 1
                json_data['like_count'] = like_count + 1
                if like_count >= 1:
                    json_data['type'] = 2
                else:
                    json_data['type'] = 1
                return JsonResponse(json_data)
        if request.POST.get('action_type') == 'comment':
            board_id = request.POST.get('board_id')
            board = Boards.objects.get(id = board_id)
            comment = request.POST.get('comment')
            action_user = Users.objects.get(id=self.request.user.id)
            user_prof = UserProfiles.objects.get(user=action_user)
            board_comments = BoardsComments(
                user = action_user,
                user_profile = user_prof,
                board = board,
                comment=comment
            )
            board_comments.save()
            json_data = dict()
            json_data['username'] = user_prof.username
            json_data['user_home_url'] = f'/{user_prof.username}/'
            json_data['comment'] = comment
            return JsonResponse(json_data)
        if request.POST.get('action_type') == 'follow':
            username = request.POST.get('username')
            follower_user = UserProfiles.objects.get(username=username).user
            follow = FollowFollowerUser(
                follow_user = user,
                follower_user = follower_user
            )
            follow.save()
            count_follower = FollowFollowerUser.objects.count_follower(follower_user=follower_user)
            return JsonResponse({'count_follower': count_follower})
        if request.POST.get('action_type') == 'clear_follow':
            username = request.POST.get('username')
            follower_user = UserProfiles.objects.get(username=username).user
            clear_follow = FollowFollowerUser.objects.filter(follow_user=user, follower_user=follower_user)
            clear_follow.delete()
            count_follower = FollowFollowerUser.objects.count_follower(follower_user=follower_user)
            return JsonResponse({'count_follower': count_follower})
        return redirect('sns:home')


    def boards_to_dictionary(self, boards):
        picture_exits = []
        for i in range(1, 11):
            word = eval('boards.picture' + str(i))
            try:
                word = word.url
                picture_exits.append(i)
            except:
                continue
        output = {}
        output['user'] = boards.user.id
        for i in picture_exits:
            output['picture'+str(i)] = eval('boards.picture' + str(i) + '.url')
        output['description'] = boards.description
        output['create_at'] = boards.create_at
        output['update_at'] = boards.update_at
        return output

    
    def boards_form_save(self, user, user_profile, picture1, picture2, picture3, picture4, picture5,
                         picture6, picture7, picture8, picture9, picture10,
                         description):
                         create_boards = Boards(
                            user=user, user_profile=user_profile, picture1=picture1, picture2=picture2,
                            picture3=picture3, picture4=picture4, picture5=picture5,
                            picture6=picture6, picture7=picture7, picture8=picture8,
                            picture9=picture9, picture10=picture10, description=description
                         )
                         create_boards.save()
                         return create_boards

    def randomname_png_path(self, n):
        randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
        dt = datetime.datetime.now()
        picture_name = ''.join(randlst) + '.jpg'
        if len(str(dt.month)) == 2:
            if len(str(dt.day)) == 2:
                path = f'board_pictures/{dt.year}/{dt.month}/{dt.day}/{picture_name}'
            else:
                path = f'board_pictures/{dt.year}/{dt.month}/0{dt.day}/{picture_name}'
        else:
            if len(str(dt.day)) == 2:
                path = f'board_pictures/{dt.year}/0{dt.month}/{dt.day}/{picture_name}'
            else:
                path = f'board_pictures/{dt.year}/0{dt.month}/0{dt.day}/{picture_name}'           
        return path

# 個人画面
class UserHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'sns/user_home.html'
    login_url = reverse_lazy('sns:login')

    def get_context_data(self, **kwargs):
        user = Users.objects.get(id=self.request.user.id)
        context = super().get_context_data(**kwargs)
        host_user = UserProfiles.objects.get(username=self.kwargs.get('host_user'))
        boards = Boards.objects.filter(user=host_user.user)
        number_of_board = boards.count()
        count_follow = FollowFollowerUser.objects.count_follow(follow_user=host_user.user)
        count_follower = FollowFollowerUser.objects.count_follower(follower_user=host_user.user)
        self_user = UserProfiles.objects.get(user=self.request.user)
        username = self_user.username
        if host_user == self_user:
            context['follow'] = 'self'
        elif FollowFollowerUser.objects.filter(follow_user=self_user.user, follower_user=host_user.user):
            context['follow'] = 'followed'
        else:
            context['follow'] = 'follow'
        context['host_user'] = host_user
        context['boards'] = boards
        context['number_of_board'] = number_of_board
        context['count_follow'] = count_follow
        context['count_follower'] = count_follower
        context['username'] = username
        notification_items = []
        notifications = Notifications.objects.filter(receiver_id=user)
        for notification in notifications:
            action_user = Users.objects.get(id=notification.action_user_id)
            action_user_profile = UserProfiles.objects.get(user=action_user)
            receiver_user = Users.objects.get(id=notification.receiver_id)
            receiver_user_profile = UserProfiles.objects.get(user=receiver_user)
            board = ''
            date = (now() - notification.create_at)
            date_days = date.days
            date_second = date.seconds
            date_minute = date_second // 60
            date_hour = date_minute // 60
            if date_second < 60:
                day = str(date_second) + '秒前'
            elif date_minute < 60:
                day = str(date_minute) + '分前'
            elif date_hour < 60:
                day = str(date_hour) + '時間前'
            else:
                for i in range(1, 8):
                    if date_days <= i * 7:
                        if i == 1:
                            day = str(date_days) + '日前'
                        day = str(i) + '週間前'
            if notification.action_id != 1:
                board = Boards.objects.get(id=notification.board_id)
            followed = ''
            if notification.action_id == 1:
                followed = FollowFollowerUser.objects.filter(follow_user=receiver_user, follower_user=action_user)
                if followed:
                    followed = True
                else:
                    followed = False
            comment = ''
            if notification.action_id == 3:
                comment = notification.comment
            items = {
                'action_id': notification.action_id,
                'action_user_profile': action_user_profile,
                'receiver_user_profile': receiver_user_profile,
                'board': board,
                'day': day,
                'followed': followed,
                'comment': comment
            }
            notification_items.append(items)
        context['notifications'] = notification_items
        return context
    
    def post(self, request, *args, **kwargs):
        user = Users.objects.get(id=self.request.user.id)
        if request.POST.get('action_type') == 'search_user':
            search_text = request.POST.get('search_text')
            results = UserProfiles.objects.filter(Q(username__icontains = search_text) | Q(nickname__icontains = search_text))
            data = dict()
            users_data = []
            count = 0
            for result in results:
                if count == 50:
                    break
                user_data = dict()
                user_data['user_icon']= result.user_icon.url
                user_data['username'] = result.username
                user_data['nickname'] = result.nickname
                user_data['user_home_url'] = f'/{result.username}/'
                users_data.append(user_data)
                count += 1
            data['users'] = users_data
            print('success')
            return JsonResponse(data)
        if request.POST.get('action_type') == 'follow':
            username = request.POST.get('username')
            follower_user = UserProfiles.objects.get(username=username).user
            follow = FollowFollowerUser(
                follow_user = user,
                follower_user = follower_user
            )
            follow.save()
            count_follower = FollowFollowerUser.objects.count_follower(follower_user=follower_user)
            return JsonResponse({'count_follower': count_follower})
        if request.POST.get('action_type') == 'clear_follow':
            username = request.POST.get('username')
            follower_user = UserProfiles.objects.get(username=username).user
            clear_follow = FollowFollowerUser.objects.filter(follow_user=user, follower_user=follower_user)
            clear_follow.delete()
            count_follower = FollowFollowerUser.objects.count_follower(follower_user=follower_user)
            return JsonResponse({'count_follower': count_follower})

            


# 掲示板画面
class BoardView(LoginRequiredMixin, TemplateView):
    template_name = 'sns/board.html'
    login_url = reverse_lazy('sns:login')

    def get_context_data(self, **kwargs):
        user = Users.objects.get(id=self.request.user.id)
        username = UserProfiles.objects.get(user=user).username
        context = super().get_context_data(**kwargs)
        board = Boards.objects.get(id=self.kwargs.get('board_id'))
        like = BoardsLikes.objects.filter(board=board)
        if like.count() >= 2:
            like_count = 2
        elif like.count() == 0:
            like_count = 0
        else:
            like_count = 1
        if BoardsLikes.objects.filter(board=board, user=user):
            liked = 1
        else:
            liked = 0
        comment = BoardsComments.objects.filter(board=board)
        context['board'] = board
        context['like'] = like.first()
        context['like_count'] = like_count
        context['comments'] = comment
        context['username'] = username
        context['liked'] = liked
        notification_items = []
        notifications = Notifications.objects.filter(receiver_id=user)
        for notification in notifications:
            action_user = Users.objects.get(id=notification.action_user_id)
            action_user_profile = UserProfiles.objects.get(user=action_user)
            receiver_user = Users.objects.get(id=notification.receiver_id)
            receiver_user_profile = UserProfiles.objects.get(user=receiver_user)
            board = ''
            date = (now() - notification.create_at)
            date_days = date.days
            date_second = date.seconds
            date_minute = date_second // 60
            date_hour = date_minute // 60
            if date_second < 60:
                day = str(date_second) + '秒前'
            elif date_minute < 60:
                day = str(date_minute) + '分前'
            elif date_hour < 60:
                day = str(date_hour) + '時間前'
            else:
                for i in range(1, 8):
                    if date_days <= i * 7:
                        if i == 1:
                            day = str(date_days) + '日前'
                        day = str(i) + '週間前'
            if notification.action_id != 1:
                board = Boards.objects.get(id=notification.board_id)
            followed = ''
            if notification.action_id == 1:
                followed = FollowFollowerUser.objects.filter(follow_user=receiver_user, follower_user=action_user)
                if followed:
                    followed = True
                else:
                    followed = False
            comment = ''
            if notification.action_id == 3:
                comment = notification.comment
            items = {
                'action_id': notification.action_id,
                'action_user_profile': action_user_profile,
                'receiver_user_profile': receiver_user_profile,
                'board': board,
                'day': day,
                'followed': followed,
                'comment': comment
            }
            notification_items.append(items)
        context['notifications'] = notification_items
        return context
    
    def post(self, request, *args, **kwargs):

        if request.POST.get('action_type') == 'like':
            board_id = request.POST.get('board_id')
            board = Boards.objects.get(id = board_id)
            action_user = Users.objects.get(id = self.request.user.id)
            user_profile = UserProfiles.objects.get(user=action_user)
            liking = BoardsLikes.objects.filter(board=board, user=action_user)
            like = BoardsLikes.objects.filter(board=board)
            like_count = like.count()
            json_data = dict()
            if liking:
                liking.delete()
                json_data['liked'] = 0
                json_data['like_count'] = like_count - 1
                if like_count >= 3:
                    json_data['type'] = 2
                    first_like = like.first()
                    json_data['first_like'] = first_like.user_profile.username
                    return JsonResponse(json_data)
                elif like_count == 2:
                    json_data['type'] = 1
                    first_like = like.first()
                    json_data['first_like'] = first_like.user_profile.username
                    return JsonResponse(json_data)
                else:
                    json_data['type'] = 0
                    return JsonResponse(json_data)
            else:
                board_like = BoardsLikes(
                    board = board,
                    user = action_user,
                    user_profile=user_profile,
                )
                board_like.save()
                first_like = like.first()
                json_data['first_like'] = first_like.user_profile.username
                json_data['liked'] = 1
                json_data['like_count'] = like_count + 1
                if like_count >= 1:
                    json_data['type'] = 2
                else:
                    json_data['type'] = 1
                return JsonResponse(json_data)
        if request.POST.get('action_type') == 'comment':
            board_id = request.POST.get('board_id')
            board = Boards.objects.get(id = board_id)
            comment = request.POST.get('comment')
            action_user = Users.objects.get(id=self.request.user.id)
            user_prof = UserProfiles.objects.get(user=action_user)
            board_comments = BoardsComments(
                user = action_user,
                user_profile = user_prof,
                board = board,
                comment=comment
            )
            board_comments.save()
            json_data = dict()
            json_data['username'] = user_prof.username
            json_data['user_home_url'] = f'/{user_prof.username}/'
            json_data['user_icon_url'] = user_prof.user_icon.url
            json_data['comment'] = comment
            return JsonResponse(json_data)
        if request.POST.get('action_type') == 'search_user':
            search_text = request.POST.get('search_text')
            results = UserProfiles.objects.filter(Q(username__icontains = search_text) | Q(nickname__icontains = search_text))
            data = dict()
            users_data = []
            count = 0
            for result in results:
                if count == 50:
                    break
                user_data = dict()
                user_data['user_icon']= result.user_icon.url
                user_data['username'] = result.username
                user_data['nickname'] = result.nickname
                user_data['user_home_url'] = f'/{result.username}/'
                users_data.append(user_data)
                count += 1
            data['users'] = users_data
            print('success')
            return JsonResponse(data)
        return redirect('sns:home')

# アカウント設定画面
class AccountsEditView(LoginRequiredMixin, TemplateView):
    template_name = 'sns/accounts_edit.html'
    login_url = reverse_lazy('sns:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.id
        user_profile = UserProfiles.objects.get(user=user)
        context['user_profile'] = user_profile
        context['username'] = user_profile.username
        notification_items = []
        notifications = Notifications.objects.filter(receiver_id=user)
        for notification in notifications:
            action_user = Users.objects.get(id=notification.action_user_id)
            action_user_profile = UserProfiles.objects.get(user=action_user)
            receiver_user = Users.objects.get(id=notification.receiver_id)
            receiver_user_profile = UserProfiles.objects.get(user=receiver_user)
            board = ''
            date = (now() - notification.create_at)
            date_days = date.days
            date_second = date.seconds
            date_minute = date_second // 60
            date_hour = date_minute // 60
            if date_second < 60:
                day = str(date_second) + '秒前'
            elif date_minute < 60:
                day = str(date_minute) + '分前'
            elif date_hour < 60:
                day = str(date_hour) + '時間前'
            else:
                for i in range(1, 8):
                    if date_days <= i * 7:
                        if i == 1:
                            day = str(date_days) + '日前'
                        day = str(i) + '週間前'
            if notification.action_id != 1:
                board = Boards.objects.get(id=notification.board_id)
            followed = ''
            if notification.action_id == 1:
                followed = FollowFollowerUser.objects.filter(follow_user=receiver_user, follower_user=action_user)
                if followed:
                    followed = True
                else:
                    followed = False
            comment = ''
            if notification.action_id == 3:
                comment = notification.comment
            items = {
                'action_id': notification.action_id,
                'action_user_profile': action_user_profile,
                'receiver_user_profile': receiver_user_profile,
                'board': board,
                'day': day,
                'followed': followed,
                'comment': comment
            }
            notification_items.append(items)
        context['notifications'] = notification_items
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('action_type') == 'change_profile': 
            user = self.request.user
            profile = UserProfiles.objects.get(user=user)
            user_icon = request.FILES.get('user_icon')
            if not user_icon:
                user_icon = profile.user_icon
            username = request.POST.get('username')
            nickname = request.POST.get('nickname')
            introduction = request.POST.get('introduction')
            json_data = dict()
            error_messages = []
            if username != profile.username:
                if UserProfiles.objects.filter(username=username):
                    error_messages.append('not_username_unique')
            if not self.match(username):
                error_messages.append('only_number_english')
            json_data['error_messages'] = error_messages
            if error_messages:
                json_data['success'] = False
                json_data['username'] = profile.username
                return JsonResponse(json_data)
            else:
                json_data['success'] = True
                profile.user_icon = user_icon
                profile.username = username
                profile.nickname = nickname
                profile.introduction = introduction
                profile.save()
                json_data['username'] = profile.username
                return JsonResponse(json_data)
        if request.POST.get('action_type') == 'search_user':
            search_text = request.POST.get('search_text')
            results = UserProfiles.objects.filter(Q(username__icontains = search_text) | Q(nickname__icontains = search_text))
            data = dict()
            users_data = []
            count = 0
            for result in results:
                if count == 50:
                    break
                user_data = dict()
                user_data['user_icon']= result.user_icon.url
                user_data['username'] = result.username
                user_data['nickname'] = result.nickname
                user_data['user_home_url'] = f'/{result.username}/'
                users_data.append(user_data)
                count += 1
            data['users'] = users_data
            print('success')
            return JsonResponse(data)

    def match(self, text):
        return all(re.findall('[a-z0-9\_.]', i) for i in text)


# パスワード変更画面
class AccountsPasswordChangeView(TemplateView, LoginRequiredMixin):
    template_name = 'sns/accounts_password_change.html'
    login_url = reverse_lazy('sns:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_profile = UserProfiles.objects.get(user=user)
        context['user_profile'] = user_profile
        context['username'] = user_profile.username
        context['accounts_password_change_form'] = PasswordChangeForm(user=self.request.user)
        notification_items = []
        notifications = Notifications.objects.filter(receiver_id=user)
        for notification in notifications:
            action_user = Users.objects.get(id=notification.action_user_id)
            action_user_profile = UserProfiles.objects.get(user=action_user)
            receiver_user = Users.objects.get(id=notification.receiver_id)
            receiver_user_profile = UserProfiles.objects.get(user=receiver_user)
            board = ''
            date = (now() - notification.create_at)
            date_days = date.days
            date_second = date.seconds
            date_minute = date_second // 60
            date_hour = date_minute // 60
            if date_second < 60:
                day = str(date_second) + '秒前'
            elif date_minute < 60:
                day = str(date_minute) + '分前'
            elif date_hour < 60:
                day = str(date_hour) + '時間前'
            else:
                for i in range(1, 8):
                    if date_days <= i * 7:
                        if i == 1:
                            day = str(date_days) + '日前'
                        day = str(i) + '週間前'
            if notification.action_id != 1:
                board = Boards.objects.get(id=notification.board_id)
            followed = ''
            if notification.action_id == 1:
                followed = FollowFollowerUser.objects.filter(follow_user=receiver_user, follower_user=action_user)
                if followed:
                    followed = True
                else:
                    followed = False
            comment = ''
            if notification.action_id == 3:
                comment = notification.comment
            items = {
                'action_id': notification.action_id,
                'action_user_profile': action_user_profile,
                'receiver_user_profile': receiver_user_profile,
                'board': board,
                'day': day,
                'followed': followed,
                'comment': comment
            }
            notification_items.append(items)
        context['notifications'] = notification_items
        return context
    
    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if request.POST.get('action_type') == 'change_password':
            form = PasswordChangeForm(self.request.user, request.POST or None)
            old_password = request.POST.get('old_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            if new_password1 != new_password2:
                return JsonResponse({'error_type': 'not_correct'})
            bool_length = len(new_password1) >= 6
            if not all([self.contain_any(new_password1, ascii_lowercase),
                    self.contain_any(new_password1, ascii_uppercase),
                    self.contain_any(new_password1, digits),
                    bool_length]):
                return JsonResponse({'error_type': 'danger'})
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return JsonResponse({'error_type': False})
            else:
                return JsonResponse({'error_type': 'not_authenticate'})
        if request.POST.get('action_type') == 'search_user':
            search_text = request.POST.get('search_text')
            results = UserProfiles.objects.filter(Q(username__icontains = search_text) | Q(nickname__icontains = search_text))
            data = dict()
            users_data = []
            count = 0
            for result in results:
                if count == 50:
                    break
                user_data = dict()
                user_data['user_icon']= result.user_icon.url
                user_data['username'] = result.username
                user_data['nickname'] = result.nickname
                user_data['user_home_url'] = f'/{result.username}/'
                users_data.append(user_data)
                count += 1
            data['users'] = users_data
            print('success')
            return JsonResponse(data)
        return render(self.request, 'sns/accounts_password_change.html', context)
    
    def contain_any(self, password, condition_list):
        return any([i in password for i in condition_list])


# フォロー一覧画面
class FollowListView(LoginRequiredMixin, TemplateView):
    template_name = 'sns/follow_list.html'
    login_url = reverse_lazy('sns:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        host_user_profile = UserProfiles.objects.get(username=self.kwargs.get('host_user'))
        host_user = host_user_profile.user
        follows = FollowFollowerUser.objects.filter(follow_user=host_user)
        user_profile = UserProfiles.objects.get(user=user)
        follow_items = []
        for follow in follows:
            follow_item = dict()
            follow_profile = UserProfiles.objects.get(user=follow.follower_user)
            followed = 'not_followed'
            if FollowFollowerUser.objects.filter(follow_user=user, follower_user=follow_profile.user):
                followed = 'followed'
            if user == follow_profile.user:
                followed = 'me'
            print(followed)
            follow_item['user_icon'] = follow_profile.user_icon
            follow_item['username'] = follow_profile.username
            follow_item['nickname'] = follow_profile.nickname
            follow_item['followed'] = followed
            follow_item['user_home_url'] = f'/{follow_profile.username}/'
            follow_items.append(follow_item)
        context['follow_items'] = follow_items
        context['username'] = user_profile.username
        context['host_username'] = host_user_profile.username
        notification_items = []
        notifications = Notifications.objects.filter(receiver_id=user)
        for notification in notifications:
            action_user = Users.objects.get(id=notification.action_user_id)
            action_user_profile = UserProfiles.objects.get(user=action_user)
            receiver_user = Users.objects.get(id=notification.receiver_id)
            receiver_user_profile = UserProfiles.objects.get(user=receiver_user)
            board = ''
            date = (now() - notification.create_at)
            date_days = date.days
            date_second = date.seconds
            date_minute = date_second // 60
            date_hour = date_minute // 60
            if date_second < 60:
                day = str(date_second) + '秒前'
            elif date_minute < 60:
                day = str(date_minute) + '分前'
            elif date_hour < 60:
                day = str(date_hour) + '時間前'
            else:
                for i in range(1, 8):
                    if date_days <= i * 7:
                        if i == 1:
                            day = str(date_days) + '日前'
                        day = str(i) + '週間前'
            if notification.action_id != 1:
                board = Boards.objects.get(id=notification.board_id)
            followed = ''
            if notification.action_id == 1:
                followed = FollowFollowerUser.objects.filter(follow_user=receiver_user, follower_user=action_user)
                if followed:
                    followed = True
                else:
                    followed = False
            comment = ''
            if notification.action_id == 3:
                comment = notification.comment
            items = {
                'action_id': notification.action_id,
                'action_user_profile': action_user_profile,
                'receiver_user_profile': receiver_user_profile,
                'board': board,
                'day': day,
                'followed': followed,
                'comment': comment
            }
            notification_items.append(items)
        context['notifications'] = notification_items
        return context
    
    def post(self, request, *args, **kwargs):
        user = self.request.user
        if request.POST.get('action_type') == 'search_user':
            search_text = request.POST.get('search_text')
            results = UserProfiles.objects.filter(Q(username__icontains = search_text) | Q(nickname__icontains = search_text))
            data = dict()
            users_data = []
            count = 0
            for result in results:
                if count == 50:
                    break
                user_data = dict()
                user_data['user_icon']= result.user_icon.url
                user_data['username'] = result.username
                user_data['nickname'] = result.nickname
                user_data['user_home_url'] = f'/{result.username}/'
                users_data.append(user_data)
                count += 1
            data['users'] = users_data
            print('success')
            return JsonResponse(data)
        if request.POST.get('action_type') == 'follow':
            username = request.POST.get('username')
            follower_user = UserProfiles.objects.get(username=username).user
            follow = FollowFollowerUser(
                follow_user = user,
                follower_user = follower_user
            )
            follow.save()
            count_follower = FollowFollowerUser.objects.count_follower(follower_user=follower_user)
            return JsonResponse({'count_follower': count_follower})
        if request.POST.get('action_type') == 'clear_follow':
            username = request.POST.get('username')
            follower_user = UserProfiles.objects.get(username=username).user
            clear_follow = FollowFollowerUser.objects.filter(follow_user=user, follower_user=follower_user)
            clear_follow.delete()
            count_follower = FollowFollowerUser.objects.count_follower(follower_user=follower_user)
            return JsonResponse({'count_follower': count_follower})


# フォロワー一覧画面
class FollowerListView(LoginRequiredMixin, TemplateView):
    template_name = 'sns/follower_list.html'
    login_url = reverse_lazy('sns:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        host_user_profile = UserProfiles.objects.get(username=self.kwargs.get('host_user'))
        host_user = host_user_profile.user
        follows = FollowFollowerUser.objects.filter(follower_user=host_user)
        user_profile = UserProfiles.objects.get(user=user)
        follow_items = []
        for follow in follows:
            follow_item = dict()
            follow_profile = UserProfiles.objects.get(user=follow.follow_user)
            followed = 'not_followed'
            if FollowFollowerUser.objects.filter(follow_user=user, follower_user=follow_profile.user):
                followed = 'followed'
            if user == follow_profile.user:
                followed = 'me'
            follow_item['user_icon'] = follow_profile.user_icon
            follow_item['username'] = follow_profile.username
            follow_item['nickname'] = follow_profile.nickname
            follow_item['followed'] = followed
            follow_item['user_home_url'] = f'/{follow_profile.username}/'
            follow_items.append(follow_item)
        context['follow_items'] = follow_items
        context['username'] = user_profile.username
        context['host_username'] = host_user_profile.username
        notification_items = []
        notifications = Notifications.objects.filter(receiver_id=user)
        for notification in notifications:
            action_user = Users.objects.get(id=notification.action_user_id)
            action_user_profile = UserProfiles.objects.get(user=action_user)
            receiver_user = Users.objects.get(id=notification.receiver_id)
            receiver_user_profile = UserProfiles.objects.get(user=receiver_user)
            board = ''
            date = (now() - notification.create_at)
            date_days = date.days
            date_second = date.seconds
            date_minute = date_second // 60
            date_hour = date_minute // 60
            if date_second < 60:
                day = str(date_second) + '秒前'
            elif date_minute < 60:
                day = str(date_minute) + '分前'
            elif date_hour < 60:
                day = str(date_hour) + '時間前'
            else:
                for i in range(1, 8):
                    if date_days <= i * 7:
                        if i == 1:
                            day = str(date_days) + '日前'
                        day = str(i) + '週間前'
            if notification.action_id != 1:
                board = Boards.objects.get(id=notification.board_id)
            followed = ''
            if notification.action_id == 1:
                followed = FollowFollowerUser.objects.filter(follow_user=receiver_user, follower_user=action_user)
                if followed:
                    followed = True
                else:
                    followed = False
            comment = ''
            if notification.action_id == 3:
                comment = notification.comment
            items = {
                'action_id': notification.action_id,
                'action_user_profile': action_user_profile,
                'receiver_user_profile': receiver_user_profile,
                'board': board,
                'day': day,
                'followed': followed,
                'comment': comment
            }
            notification_items.append(items)
        context['notifications'] = notification_items
        return context
    
    def post(self, request, *args, **kwargs):
        user = self.request.user
        if request.POST.get('action_type') == 'search_user':
            search_text = request.POST.get('search_text')
            results = UserProfiles.objects.filter(Q(username__icontains = search_text) | Q(nickname__icontains = search_text))
            data = dict()
            users_data = []
            count = 0
            for result in results:
                if count == 50:
                    break
                user_data = dict()
                user_data['user_icon']= result.user_icon.url
                user_data['username'] = result.username
                user_data['nickname'] = result.nickname
                user_data['user_home_url'] = f'/{result.username}/'
                users_data.append(user_data)
                count += 1
            data['users'] = users_data
            print('success')
            return JsonResponse(data)
        if request.POST.get('action_type') == 'follow':
            username = request.POST.get('username')
            follower_user = UserProfiles.objects.get(username=username).user
            follow = FollowFollowerUser(
                follow_user = user,
                follower_user = follower_user
            )
            follow.save()
            return JsonResponse({'a': 'a'})
        if request.POST.get('action_type') == 'clear_follow':
            username = request.POST.get('username')
            follower_user = UserProfiles.objects.get(username=username).user
            clear_follow = FollowFollowerUser.objects.filter(follow_user=user, follower_user=follower_user)
            clear_follow.delete()
            return JsonResponse({'a': 'a'})
        