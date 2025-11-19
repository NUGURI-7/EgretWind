import hashlib

from django.db import models

# Create your models here.


from django.db import models



def password_encrypt(row_password: str):
    """
    密码 md5加密
    :param row_password: 密码
    :return:  加密后密码
    """
    md5 = hashlib.md5()  # 2，实例化md5() 方法
    md5.update(row_password.encode())  # 3，对字符串的字节类型加密
    result = md5.hexdigest()  # 4，加密
    return result

class User(models.Model):
    username = models.CharField(max_length=64, unique=True, null=False, verbose_name='用户名')
    email = models.EmailField(max_length=128, unique=True, null=False, verbose_name='邮箱')
    password = models.CharField(max_length=256, null=False, verbose_name='密码')
    phone_number = models.CharField(max_length=32, blank=True, null=True, unique=True, verbose_name='手机号')
    nickname = models.CharField(max_length=64, blank=True, null=True, verbose_name='昵称')
    avatar = models.URLField(max_length=256, blank=True, null=True, verbose_name='头像URL')
    gender = models.SmallIntegerField(choices=[(0, '未知'), (1, '男'), (2, '女')], default=0, verbose_name='性别')
    bio = models.CharField(max_length=512, blank=True, null=True, verbose_name='个人简介')
    location = models.CharField(max_length=128, blank=True, null=True, verbose_name='位置/所在地')
    is_active = models.BooleanField(default=True, verbose_name='是否激活/启用')
    is_admin = models.BooleanField(default=False, verbose_name='是否管理员')
    status = models.SmallIntegerField(choices=[(0, '正常'), (1, '禁用'), (2, '待审核')], default=0, verbose_name='用户状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='信息最后更新时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        db_table = 'user'
        ordering = ['-created_time']

    def set_password(self, row_password: str):
        self.password = password_encrypt(row_password)
        self._password = row_password


    def __str__(self):
        return self.username
