# coding=utf-8
"""
    @project: EgretWind
    @Author：鹭岛听风
    @file： __init__.py
    @date：2025/11/19 21:44
    @desc:
"""

from django.db.models import QuerySet
from rest_framework import serializers

from article.models import Article
from common.database.search import page_search


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class ArticleSerializers(serializers.Serializer):


    class Query(serializers.Serializer):



        def get_queryset(self):
            self.is_valid(raise_exception=True)
            query_set = QuerySet(Article)

            return query_set

        def list(self):
            return [ArticleSerializer(row).data for row in self.get_queryset()]
            # return list(map(lambda row: ArticleSerializer(row).data, self.get_queryset()))

        def page(self, current_page: int, page_size: int):
            query_set = self.get_queryset()
            handler = lambda row: ArticleSerializer(row).data
            return page_search(current_page, page_size, query_set, handler)
