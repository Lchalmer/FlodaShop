from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class HomePagination(PageNumberPagination):
    page_size = 8
    page_query_param = 'page_size'

    def next_page(self, page):
        try:
            res = page.next_page_number()
        except:
            res = None
        return res

    def previous_page(self, page):
        try:
            res = page.previous_page_number()
        except:
            res = None
        return res

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('num_pages', self.page.paginator.num_pages),  # 总页数
            ('count', self.page.paginator.count),  # 总数据条数
            # 上一页页码数
            ('previous_page', self.previous_page(self.page)),
            ('previous', self.get_previous_link()),  # 上一页链接
            ('NowNumber', self.page.number),  # 当前页码数
            # 下一页页码数
            ('next_page', self.next_page(self.page)),
            ('next', self.get_next_link()),  # 下一页链接
            ('results', data)  # 结果数据
        ]))
