from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import status

#rest framework分页
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import CursorPagination
#rest framework搜索
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


from django.http import HttpResponse
from .models import Goods,GoodsCategory,HotSearchWords,Banner
from .serializers import GoodsSerializer,CategorySerializer,HotWordsSerializer,BannerSerializer,IndexCategorySerializer
from .filter import GoodsFilter
from django_redis import get_redis_connection
from django.core.cache import  cache

from rest_framework_extensions.mixins import CacheResponseAndETAGMixin
import json




# class GoodsListView(mixins.ListModelMixin,generics.GenericAPIView):

class GoodsPagination(PageNumberPagination):
    page_size = 12

    page_query_param = 'page'

    page_size_query_param = 'page_size'

    max_page_size = 100

class GoodsListViewSet(CacheResponseAndETAGMixin,mixins.ListModelMixin,viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    """
    商品列表,分页，搜索，过滤，排序
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination  #分页
    # authentication_classes = (TokenAuthentication,)
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    #filters.OrderingFilter排序，filters.SearchFilter搜索过滤
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)
    filter_class = GoodsFilter
    search_fields=('name','goods_brief','goods_desc')
    ordering_fields = ('sold_num','shop_price')

    #商品点击数 + 1
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

# class GoodsListView(generics.ListAPIView):
#     """
#     商品列表
#     """
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     pagination_class = GoodsPagination
#
#     def get(self,request,*args,**kwargs):
#
#         # goods=Goods.objects.all()[:20]
#         # ser=GoodsSerializer(instance=goods,many=True,context={'request': request})
#         # ret=json.dumps(ser.data,ensure_ascii=False)
#         # return Response(ret.data)
#         # return Response(ser.data)
#         return self.list(self,request,*args,**kwargs)


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    list:
        商品分类列表数据
    '''

    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class HotSearchsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    热搜
    """
    queryset = HotSearchWords.objects.all().order_by("-index")
    serializer_class = HotWordsSerializer


class BannerViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    获取轮播图列表
    """

    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer

class IndexCategoryViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    首页商品分类数据
    """
    # 获取is_tab=True（导航栏）里面的分类下的商品数据
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer