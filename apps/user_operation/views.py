from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework import mixins
from .models import UserFav,UserLeavingMessage,UserAddress
from .serializers import UserFavSerializer,UserFavDetailSerializer,LeavingSerializer,AddressSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication
from utils.permissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication

class UserFavViewset(mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    用户收藏功能
    """
    # queryset = UserFav.objects.all()
    # IsAuthenticated：必须登录用户；IsOwnerOrReadOnly：必须是当前登录的用户
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    serializer_class = UserFavSerializer
    # auth使用来做用户认证的
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    # 搜索的字段
    lookup_field = "goods_id"

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer

        return UserFavSerializer



class LeavingMessageViewset(mixins.ListModelMixin,mixins.DestroyModelMixin,mixins.CreateModelMixin,viewsets.GenericViewSet):
    """
    list:
        获取用户留言
    create:
        添加留言
    delete:
        删除留言功能
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    serializer_class = LeavingSerializer
    #只能看到自己留言
    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


# class AddressViewset(mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
class AddressViewset(viewsets.ModelViewSet):
    """
    收货地址管理
    list:
        获取收货地址
    create:
        添加收货地址
    delete:
        删除收货地址
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    serializer_class = AddressSerializer
    #只能看到自己留言
    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
