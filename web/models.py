from django.db import models

# Create your models here.

class UserInfo(models.Model):
    username = models.CharField(max_length=50,verbose_name='用户名')
    email = models.EmailField(verbose_name='邮箱地址',max_length=50)
    password = models.CharField(verbose_name='密码',max_length=50)