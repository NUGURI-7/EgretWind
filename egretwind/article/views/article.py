# coding=utf-8
"""
    @project: EgretWind
    @Author：鹭岛听风
    @file： user_test.py
    @date：2025/11/19 21:44
    @desc:
"""
from rest_framework.request import Request
from rest_framework.views import APIView

from article.serializer.article import ArticleSerializers
from common.result import result


class ArticleView(APIView):

    # 获取全部文章列表
    def get(self, request: Request):
        return result.success(
            ArticleSerializers.Query(data={}).list()
        )

    # 分页获取文章列表
    class Page(APIView):
        def get(self, request: Request, current_page: int, page_size: int):
            return result.success(
                ArticleSerializers.Query(data={}).page(current_page,page_size)
            )
