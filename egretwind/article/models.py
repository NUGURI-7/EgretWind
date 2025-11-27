from django.db import models

from common.mixins.app_model_mixin import BaseModel
from user.models import User


# Create your models here.

class Article(BaseModel):
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
    ]

    title = models.CharField(max_length=200, verbose_name='标题')
    # summary = models.TextField(max_length=500, verbose_name='摘要')
    content = models.TextField(verbose_name='内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name='作者')
    # category = models.ForeignKey('articles.Category', on_delete=models.SET_NULL, null=True, blank=True,
    #                              related_name='articles', verbose_name='分类')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='发布时间')
    # views = models.PositiveIntegerField(default=0, verbose_name='浏览数')

    class Meta:
        ordering = ['published_at']
        verbose_name = '文章'
        verbose_name_plural = '文章'
        db_table = 'articles'

    def __str__(self):
        return self.title