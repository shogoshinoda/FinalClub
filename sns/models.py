from django.db import models
from django.contrib.auth.models import (
BaseUserManager, AbstractBaseUser, PermissionsMixin
)

class UserManager(BaseUserManager):

    # 普通のアカウントを作成する際に用いられる
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('メールアドレスを入力してください')
        user = self.model(
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # スーパーユーザのアカウントを作成する際に用いられる
    def create_superuser(self, email, password=None):
        user = self.model(
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
    email = models.EmailField(max_length=40, unique=True)
    is_active = models.