from datetime import datetime, timedelta
from uuid import uuid4
import os

from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.urls import reverse_lazy
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


# ユーザマネージャー
class UserManager(BaseUserManager):

    # 普通のアカウントを作成する際に用いられる
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('メールアドレスを入力してください')
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # スーパーユーザのアカウントを作成する際に用いられる
    def create_superuser(self, username, email, password=None):
        user = self.model(
            username=username,
            email=email,
            password=password
        )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


# ユーザ登録
class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=40, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()


# ユーザ登録トークンマネージャー
class UserActivateTokenManager(models.Manager):

    # ユーザをアクティベイトする処理
    def activate_user_by_token(self, token):
        user_activate_token = self.filter(
            token=token,
            expired_at__gte=datetime.now()  # 現在時刻以上のものを取り出す
        ).first()
        user = user_activate_token.user
        user.is_active = True
        user.save()


# ユーザ登録トークン
class UserActivateTokens(models.Model):
    token = models.UUIDField(db_index=True)
    expired_at = models.DateTimeField(default=datetime.now() + timedelta(hours=1))
    user = models.ForeignKey(
        'Users', on_delete=models.CASCADE
    )

    objects = UserActivateTokenManager()

    class Meta:
        db_table = 'user_activate_tokens'


# トークンの発行
@receiver(post_save, sender=Users)
def publish_token(sender, instance, **kwargs):
    user_activate_token = UserActivateTokens(
        user=instance,
        token=str(uuid4()),
        expired_at=datetime.now() + timedelta(days=1)
    )
    user_activate_token.save()


# 学生情報
class UserAffiliation(models.Model):
    user = models.OneToOneField(
        'Users', on_delete=models.CASCADE
    )
    year_of_admission = models.CharField(max_length=5)
    department = models.CharField(max_length=10)
    course = models.CharField(max_length=20)

    class Meta:
        db_table = 'user_affiliation'


# メールから学部学科を検出する
def detective_affiliation(email):
    departments = {'00': '所属なし', '01': '法', '02': '経営', '03': '経済', '04': '理工',
                   '05': '農', '07': '都市情報', '08': '人間', '09': '薬', '10': '外国語',
                   '12': '情報工'}
    courses = {'00': '識別不要', '01': '法', '11': '経営', '12': '国際経営', '21': '経済',
               '22': '産業社会', '40': '数学', '42': '電気電子工学', '43': '材料機能工学', '44': '応用化学',
               '45': '機械工学', '46': '交通機械工学', '47': 'メカトロニクス工学', '48': '社会基盤デザイン工学',
               '49': '環境創造工学', '50': '建築', '61': '生物資源', '62': '応用生物化学', '63': '生物環境科学',
               '81': '都市情報', '91': '人間', '73': '薬', '95': '国際英語', '05': '情報工学'}
    year = email[:2]
    department = departments[email[2:4]]
    course = courses[email[4:6]]
    return year, department, course


# 学生情報作成
@receiver(post_save, sender=Users)
def create_user_affiliation(sender, instance, **kwargs):
    user = instance
    year_of_admission, department, course = detective_affiliation(user.email)
    user_affiliation = UserAffiliation(
        user=instance,
        year_of_admission=year_of_admission,
        department=department,
        course=course
    )
    user_affiliation.save()


# プロフィールのマネージャー
class UserProfilesManager(models.Manager):

    def filter_by_profile(self, user_id):
        return self.filter(user_id=user_id).first()


# プロフィール
class UserProfiles(models.Model):
    username = models.CharField(max_length=150)
    user_icon = models.FileField(upload_to='user_icon/%Y/%m/%d/')
    user = models.OneToOneField(
        'Users', on_delete=models.CASCADE
    )
    introduction = models.TextField(null=True, blank=True, max_length=255)

    objects = UserProfilesManager()

    class Meta:
        db_table = 'profiles'


# 提示版のマネージャー
class BoardsManager(models.Manager):

    def filter_by_boards(self, user_id):
        return self.filter(user_id=user_id).all()

    def count_boards(self, user):
        return self.filter(user=user).all().count()


# 提示版
class Boards(models.Model):
    user = models.ForeignKey(
        'Users', on_delete=models.CASCADE
    )
    picture1 = models.FileField(upload_to='board_pictures/%Y/%m/%d/', null=True, blank=True)
    picture2 = models.FileField(upload_to='board_pictures/%Y/%m/%d/', null=True, blank=True)
    picture3 = models.FileField(upload_to='board_pictures/%Y/%m/%d/', null=True, blank=True)
    picture4 = models.FileField(upload_to='board_pictures/%Y/%m/%d/', null=True, blank=True)
    picture5 = models.FileField(upload_to='board_pictures/%Y/%m/%d/', null=True, blank=True)
    picture6 = models.FileField(upload_to='board_pictures/%Y/%m/%d/', null=True, blank=True)
    picture7 = models.FileField(upload_to='board_pictures/%Y/%m/%d/', null=True, blank=True)
    picture8 = models.FileField(upload_to='board_pictures/%Y/%m/%d/', null=True, blank=True)
    picture9 = models.FileField(upload_to='board_pictures/%Y/%m/%d/', null=True, blank=True)
    picture10 = models.FileField(upload_to='board_pictures/%Y/%m/%d/', null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    create_at = models.DateTimeField(default=datetime.now())
    update_at = models.DateTimeField(default=datetime.now())

    objects = BoardsManager()

    class Meta:
        db_table = 'boards'


# データが削除されたらmediaのboards_pictureが消える
@receiver(post_delete, sender=Boards)
def delete_picture(sender, instance, **kwargs):
    for i in range(1, 11):
        db_name = 'picture' + str(i)
        if instance.db_name:
            if os.path.isfile(instance.db_name.path):
                os.remove(instance.db_name.path)


# 提示版いいねマネージャー
class BoardsLikesManager(models.Manager):

    def count_like(self, board):
        return self.filter(board=board).all().count()


# 提示版いいね
class BoardsLikes(models.Model):
    board = models.ForeignKey(
        'Boards', on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        'Users', on_delete=models.CASCADE
    )

    objects = BoardsLikesManager

    class Meta:
        db_table = 'boards_likes'


# 掲示板コメント
class BoardsComments(models.Model):
    user = models.ForeignKey(
        'Users', on_delete=models.CASCADE
    )
    board = models.ForeignKey(
        'Boards', on_delete=models.CASCADE
    )
    comment = models.TextField(max_length=100)
    create_at = models.DateTimeField(default=datetime.now())

    class Meta:
        db_table = 'boards_comments'


# follow Manager
class FollowFollowerUserManager(models.Manager):

    def count_follow(self, follow_user):
        return self.filter(follow_user=follow_user).all().count()

    def count_follower(self, follower_user):
        return self.filter(follower_user=follower_user).all().count()


# follow
class FollowFollowerUser(models.Model):
    follow_user = models.ForeignKey(
        'Users', on_delete=models.CASCADE, related_name='follow_user'
    )
    follower_user = models.ForeignKey(
        'Users', on_delete=models.CASCADE, related_name='follower_user'
    )
    create_at = models.DateTimeField(default=datetime.now())

    objects = FollowFollowerUserManager()

    class Meta:
        db_table = 'follow_follower_user'


# dm
class DMBox(models.Model):
    user = models.ForeignKey(
        'Users', on_delete=models.CASCADE, related_name='user'
    )
    partner = models.ForeignKey(
        'Users', on_delete=models.CASCADE, related_name='partner'
    )
    create_at = models.DateTimeField(default=datetime.now())

    class Meta:
        db_table = 'dm_box'


# dmの内容
class DMMessages(models.Model):
    dm_box = models.ForeignKey(
        DMBox, on_delete=models.CASCADE
    )
    message = models.TextField()
    sender = models.IntegerField()
    create_at = models.DateTimeField(default=datetime.now())

    class Meta:
        db_table = 'dm_message'


# 招待コードマネージャー
class UserInviteTokenManager(models.Manager):

    # 招待コードを発行できるかどうかを判定
    def can_publish_invite_token(self, user):
        count = self.filter(user=user).all().count
        if count >= 2:
            return False
        return True

    # 招待コードを発行
    def publish_invite_token(self, user):
        user_invite_token = self.model(
            user=user,
            token=str(uuid4()),
            available=True
        )
        user_invite_token.save()


# 招待コード
class UserInviteToken(models.Model):
    user = models.ForeignKey(
        'Users', on_delete=models.CASCADE
    )
    invite_token = models.UUIDField(db_index=True)
    available = models.BooleanField()

    objects = UserActivateTokenManager()

    class Meta:
        db_table = 'invite_token'


# 通知
class Notifications(models.Model):
    receiver = models.ForeignKey(
        'Users', on_delete=models.CASCADE, related_name='receiver'
    )
    action_user = models.ForeignKey(
        'Users', on_delete=models.CASCADE, related_name='action_user'
    )
    action_id = models.IntegerField()
    board = models.ForeignKey(
        'Boards', on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        db_table = 'notifications'


@receiver(post_save, sender=FollowFollowerUserManager)
def create_follow_notification(sender, instance, **kwargs):
    user = instance
    follower_user = user.follower
    follow_user = user.follow
    follow_notification = Notifications(
        user=follower_user,
        action_user=follow_user,
        action_id=1
    )
    follow_notification.save()


@receiver(post_save, sender=BoardsLikes)
def create_like_notification(sender, instance, **kwargs):
    ins = instance
    user = ins.board.user
    action_user = ins.user
    action_id = 2
    board = ins.board
    like_notification = Notifications(
        user=user,
        action_user=action_user,
        action_id=action_id,
        board=board
    )
    like_notification.save()


@receiver(post_save, sender=BoardsComments)
def create_comment_notification(sender, instance, **kwargs):
    ins = instance
    user = ins.board.user
    action_user = ins.user
    action_id = 3
    board = ins.board
    comment_notification = Notifications(
        user=user,
        action_user=action_user,
        action_id=3,
        board=board
    )
    comment_notification.save()

