# coding=utf-8
"""
    @project: EgretWind
    @Author：鹭岛听风
    @file： urls.py
    @date：2025/11/19 21:34
    @desc:
"""
from django.urls import path
from .views.article import ArticleView

urlpatterns = [
    path("article/list", ArticleView.as_view(), name='文章列表'),
    path("article/page/<int:current_page>/<int:page_size>", ArticleView.Page.as_view(), name='分页获取文章列表'),
]

