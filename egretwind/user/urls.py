# coding=utf-8
"""
    @project: EgretWind
    @Author：鹭岛听风
    @file： user_test.py
    @date：2025/11/19 21:44
    @desc:
"""


from django.urls import path
from .views.user_test import UserTest

urlpatterns = [
    path("user/test", UserTest.as_view(), name='test'),
]









