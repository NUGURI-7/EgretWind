# coding=utf-8
"""
    @project: EgretWind
    @Author：鹭岛听风
    @file： user_test.py
    @date：2025/11/19 21:44
    @desc:
"""
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializer.user_test import UserTestSerializer


class UserTest(APIView):

    def get(self, request: Request):


        return Response(UserTestSerializer.list())
