from datetime import datetime, timedelta
from uuid import uuid4
import os

from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.urls import reverse_lazy


# ユーザマネージャー
class UserManager(BaseUserManager):

    # 普通のアカウントを作成する際に用いられる
    def create_user(self, id, email, password=None):
        if not email:
            raise ValueError('メールアドレスを入力してください')
        user = self.model(
            id=id,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # スーパーユーザのアカウントを作成する際に用いられる
    def create_superuser(self, id, email, password=None):
        user = self.model(
            id=id,
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
    id = models.UUIDField(primary_key=True, default=uuid4(), editable=False)
    email = models.EmailField(max_length=40, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def get_absolute_url(self):
        return reverse_lazy('sns:temporary')


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
    id = models.UUIDField(primary_key=True, default=uuid4(), editable=False)
    token = models.UUIDField(db_index=True)
    expired_at = models.DateTimeField(default=datetime.now()+timedelta(hours=1))
    user = models.ForeignKey(
        'Users', on_delete=models.CASCADE
    )

    objects = UserActivateTokenManager()

    class Meta:
        db_table = 'user_activate_tokens'


def dir_path_name(instance, filename, dirname):
    date_time = datetime.now()  # 現在の時刻を取得
    date_dir = date_time.strftime('%Y/%m/%d')  # 年/月/日のフォーマットの作成
    time_stamp = date_time.strftime('%H-%M-%S')  # 時-分-秒のフォーマットを作成
    new_filename = time_stamp + filename  # 実際のファイル名と結合
    dir_path = os.path.join(dirname, date_dir, new_filename)  # 階層構造にする
    return dir_path


# プロフィールのマネージャー
class UserProfilesManager(models.Manager):
    def filter_by_profile(self, user_id):
        return self.filter(user_id=user_id).first()


# プロフィール
class UserProfiles(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4(), editable=False)
    username = models.CharField(db_index=True, max_length=150, unique=True)
    nickname = models.CharField(max_length=150)
    user_icon = models.FileField(upload_to=dir_path_name(dirname='user_icon'))
    user = models.OneToOneField(
        Users, on_delete=models.CASCADE
    )
    introduction = models.TextField(null=True, blank=True, max_length=255)

    objects = UserProfilesManager

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
        Users, on_delete=models.CASCADE
    )
    picture1 = models.FileField(upload_to=dir_path_name(dirname='boards'),null=True, blank=True)
    picture2 = models.FileField(upload_to=dir_path_name(dirname='boards'), null=True, blank=True)
    picture3 = models.FileField(upload_to=dir_path_name(dirname='boards'), null=True, blank=True)
    picture4 = models.FileField(upload_to=dir_path_name(dirname='boards'), null=True, blank=True)
    picture5 = models.FileField(upload_to=dir_path_name(dirname='boards'), null=True, blank=True)
    picture6 = models.FileField(upload_to=dir_path_name(dirname='boards'), null=True, blank=True)
    picture7 = models.FileField(upload_to=dir_path_name(dirname='boards'), null=True, blank=True)
    picture8 = models.FileField(upload_to=dir_path_name(dirname='boards'), null=True, blank=True)
    picture9 = models.FileField(upload_to=dir_path_name(dirname='boards'), null=True, blank=True)
    picture10 = models.FileField(upload_to=dir_path_name(dirname='boards'), null=True, blank=True)


