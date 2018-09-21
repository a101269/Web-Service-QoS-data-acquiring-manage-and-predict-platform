from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .conf import settings
from .managers import UserInheritanceManager, UserManager

from datetime import datetime
import json,time

def birthday_filter(birthday): #从生日导出年龄
    t=time.time()
    dt=datetime.fromtimestamp(t)#当前时间
    '''new_minute=str(dt.mintue)
    if dt.minute<10:
    new_mintue='0'+str(dt.mintue)
    return u'[发布于%s年%s月%s日%s:%s] '%(dt.year,dt.month,dt.day,dt.hour.dt.minute
    '''
    b_year=birthday[:4]
    b_month=birthday[4:6]
    b_day=birthday[6:]
    age=int(dt.year)-int(b_year)-1 #年龄为当前年份-出生年份-1
    if int(b_month)>(int(dt.month)-1):
        if int(b_day)>(int(dt.day)-1):
            age+=1
    return age


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    USERS_AUTO_ACTIVATE = not settings.USERS_VERIFY_EMAIL

    email = models.EmailField(
        _('电子邮箱'), max_length=255, unique=True, db_index=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'))

    is_active = models.BooleanField(
        _('active'), default=USERS_AUTO_ACTIVATE,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    user_type = models.ForeignKey(ContentType, null=True, editable=False)

    objects = UserInheritanceManager()
    base_objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        abstract = True

    def get_full_name(self):
        """ Return the email."""
        return self.email

    def get_short_name(self):
        """ Return the email."""
        return self.email

    def email_user(self, subject, message, from_email=None):
        """ Send an email to this User."""
        send_mail(subject, message, from_email, [self.email])

    def activate(self):
        self.is_active = True
        self.save()

    def save(self, *args, **kwargs):
        if not self.user_type_id:
            self.user_type = ContentType.objects.get_for_model(self, for_concrete_model=False)
        super(AbstractUser, self).save(*args, **kwargs)


class User(AbstractUser):

    """
    Concrete class of AbstractUser.
    Use this if you don't need to extend User.
    """
    name=models.CharField(max_length=20,default='丁一')#姓名
    sex=models.CharField(max_length=3,default='男')#性别
    birthday = models.CharField(max_length=20, default='1970-10-10')  # 生日
    job= models.CharField(max_length=30, default='架构师')  # 工作
    job_city=models.CharField(max_length=20,default='北京') # 工作地点
    xueli=models.CharField(max_length=20,default='本科')#学历
    collage=models.CharField(max_length=80,default='北京大学')#学校
    graduate_date=models.CharField(max_length=20,default='2000-10-10')#毕业时间
    join_job_date=models.CharField(max_length=20,default='2000-10-30')#入职时间python manage.py syncdb


    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.name
    def age(self):
        return birthday_filter(self.birthday)  #从生日导出年龄