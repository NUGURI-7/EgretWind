# coding=utf-8
"""
    @project: EgretWind
    @Author：鹭岛听风
    @file： app_model_mixin.py
    @date：2025/11/27 21:05
    @desc:
"""
from django.db import models


class BaseModel(models.Model):
    objects = models.Manager()

    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, db_index=True)
    update_time = models.DateTimeField(verbose_name="修改时间", auto_now=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ['create_time']