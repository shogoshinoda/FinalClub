from datetime import datetime, timedelta
from uuid import uuid4
import os

from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.urls import reverse_lazy
from django.dispatch import receiver
from django.db.models.signals import post_save


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
    expired_at = models.DateTimeField(default=datetime.now() + timedelta(hours=1))
    user = models.ForeignKey(
        'Users', on_delete=models.CASCADE
    )

    objects = UserActivateTokenManager()

    class Meta:
        db_table = 'user_activate_tokens'


# 学生情報
class UserAffiliation(models.Model):
    user = models.OneToOneField(
        'User', on_delete=models.CASCADE
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
    id = models.UUIDField(primary_key=True, default=uuid4(), editable=False)
    user_id = models.CharField(db_index=True, max_length=150, unique=True)
    username = models.CharField(max_length=150)
    user_icon = models.FileField(upload_to='user_icon/%Y/%m/%d/')
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
    description = models.TextField(max_length=200, null=True, brank=True)
    create_at = models.DateTimeField(default=datetime.now())
    update_at = models.DateTimeField(default=datetime.now())

    objects = BoardsManager()

    class Meta:
        db_table = 'boards'


# データが削除されたらmediaのboards_pictureが消える
@receiver(models.signals.post_delete, sender=Boards)
def delete_picture(sender, instance, **kwargs):
    for i in range(1, 11):
        db_name = 'picture' + str(i)
        if instance.db_name:
            if os.path.isfile(instance.db_name.path):
                os.remove(instance.db_name.path)


# 掲示板コメント
class BoardsComments(models.Model):
    boards = models.ForeignKey(
        Boards, on_delete=models.CASCADE
    )
    comment = models.CharField(max_length=100)
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
        Users, on_delete=models.CASCADE
    )
    follower_user = models.ForeignKey(
        Users, on_delete=models.CASCADE
    )

    objects = FollowFollowerUserManager

    class Meta:
        db_table = 'follow_follower_user'
