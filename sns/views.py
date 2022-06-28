from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib import messages

from .models import (FollowFollowerUser, Users, UserProfiles, UserAffiliation,
                     UserActivateTokens, UserInviteToken, Boards,
                     BoardsLikes, BoardsComments)
from .forms import (SignInForm, InviteVerificationForm, LoginForm,
                    ProfileForm, BoardsForm)


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

    def post(self, request, *args, **kwargs):
        create_profile_form = self.create_profile_form_class(request.POST or None, request.FILES or None)
        if create_profile_form.is_valid():
            username = request.POST.get('username')
            nickname = request.POST.get('nickname')
            user_icon = request.FILES.get('user_icon')
            user = self.request.user
            introduction = request.POST.get('introduction')
            self.form_save(username, nickname, user_icon, user, introduction)
            return redirect('sns:home')
        else:
            context = {
                'create_profile_form': create_profile_form
            }
            return render(self.request, 'sns/create_profile.html', context)

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


# ログアウト
class LogoutView(LogoutView):
    pass


# ホーム画面
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'sns/home.html'
    board_form_class = BoardsForm

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        username = UserProfiles.objects.get(user=self.request.user).username
        boards = Boards.objects.all()
        board_form = self.board_form_class
        board_items = []
        for i in boards:
            likes = BoardsLikes.objects.filter(board=i).all().count()
            like_first_people = BoardsLikes.objects.filter(board=i).first()
            comments = BoardsComments.objects.filter(board=i).all()
            items = {
                'item': i,
                'likes': likes,
                'like_first_people': like_first_people,
                'comments': comments
            }
            board_items.append(items)
        context['boards'] = board_items
        context['board_form'] = board_form
        context['username'] = username
        return context
    
    def post(self, request, *args, **kwargs):
        board_form = self.board_form_class(request.POST or None, request.FILES or None)
        user = Users.objects.get(id=self.request.user.id)
        user_profile = UserProfiles.objects.get(user=self.request.user.id)
        if board_form.is_valid():
            print()
            print('success')
            print()
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
            # boards = Boards.objects.all()
            # tempBoards = []
            # for i in range(len(boards)):
            #     tempBoards.append(self.boards_to_dictionary(boards[i]))
            # boards = tempBoards
            # board = self.boards_to_dictionary(new_board)
            # params = {
            #     'description': new_board.description,
            #     'boards': boards
            # }
            return redirect('sns:home')
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


# 個人画面
class UserHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'sns/user_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        host_user = UserProfiles.objects.get(username=self.kwargs.get('host_user'))
        boards = Boards.objects.filter(user=host_user.user)
        number_of_board = boards.count()
        count_follow = FollowFollowerUser.objects.count_follow(follow_user=host_user.user)
        count_follower = FollowFollowerUser.objects.count_follower(follower_user=host_user.user)
        username = UserProfiles.objects.get(user=self.request.user).username
        context['host_user'] = host_user
        context['boards'] = boards
        context['number_of_board'] = number_of_board
        context['count_follow'] = count_follow
        context['count_follower'] = count_follower
        context['username'] = username
        return context
    




