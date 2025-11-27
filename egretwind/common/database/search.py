# coding=utf-8
"""
    @project: EgretWind
    @Author：鹭岛听风
    @file： database.py
    @date：2025/11/27 21:34
    @desc:
"""
from django.db.models import QuerySet

from common.result.result import Page


def page_search(current_page: int, page_size: int, queryset: QuerySet, post_records_handler):
    """
    ORM分页查询
    :param current_page:    当前页
    :param page_size:       每页大小
    :param queryset:        查询集
    :param post_records_handler: 数据处理器
    :return: 分页结果
    """
    total_count: int = QuerySet(query=queryset.query.clone(), model=queryset.model).count()
    offset: int = (current_page - 1) * page_size
    result = queryset.all()[offset: (current_page * page_size)]
    # More Pythonic
    records = [post_records_handler(row) for row in result]
    # return Page(total_count, list(map(post_records_handler,result)),current_page,page_size)
    return Page(total_count, records, current_page, page_size)