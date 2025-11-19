# coding=utf-8
"""
    @project: EgretWind
    @Author：鹭岛听风
    @file： user_test.py
    @date：2025/11/19 22:38
    @desc:
"""
from rest_framework import serializers

from ..models import User


class UserTestSerializer(serializers.Serializer):

    # 获取全部用户列表
    @staticmethod
    def list():
        return list(User.objects.all().values("username", "location"))