from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    login_id = models.CharField("사용자 아이디", max_length=100, primary_key=True, null=False, blank=False)
    username = models.CharField("사용자 이름", max_length=100)
    password =  models.CharField("비밀번호", max_length=100, null=False, blank=False)
    email = models.EmailField("이메일", max_length=30, null=False, blank=False)
    is_superuser = models.BooleanField("슈퍼유저 여부", default=False)
    is_active = models.BooleanField("활성 여부", default=True)
    is_staff = models.BooleanField("스테프 여부", default=False)
    created_at = models.DateTimeField("회원가입 시기", auto_now=True)
    updated_at = models.DateTimeField("업데이트 시기", auto_now=True)
    objects = UserManager()

    # 사용자가 로그인할 때 사용하는 id로 어떤 것을 사용할래? 라는 것에 지정을 해준 것.
    # 물론 다른 값으로도 사용 가능하다!!
    USERNAME_FIELD = 'login_id'

    # 슈퍼계정을 생성할 때 입력해야 할 값들을 지정할 수 있음.
    # 사용하지 않아도 되지만, 선언은 해야 함
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.login_id
    # 로그인 사용자의 특정 테이블의 crud 권한을 설정, perm table의 crud 권한이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_perm(self, perm, obj=None):
        return True
    # 로그인 사용자의 특정 app에 접근 가능 여부를 설정, app_label에는 app 이름이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_module_perms(self, app_label):
        return True

    # admin 권한 설정
#    @property
#    def is_staff(self):
#        return self.is_admin
    class Meta:
        db_table = 'user'