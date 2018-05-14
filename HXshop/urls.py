"""HXshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
import xadmin

from django.conf.urls import url,include
from goods.views_base import GoodsListView
from goods.views import GoodsListViewSet,CategoryViewSet,HotSearchsViewset,BannerViewset,IndexCategoryViewset
from users.views import SmsCodeViewset,UserViewset
from user_operation.views import UserFavViewset,LeavingMessageViewset,AddressViewset
from trade.views import ShoppingCartViewset,OrderViewset,AliPayView
from django.views.static import serve
from HXshop.settings import MEDIA_ROOT
from rest_framework.documentation import include_docs_urls

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
from django.views.generic import TemplateView
router = DefaultRouter()
#配置goods的url
router.register(r'goods', GoodsListViewSet,base_name="goods")
#配置Category的url
router.register(r'categorys', CategoryViewSet,base_name="categorys")
# 配置codes的url
router.register(r'code', SmsCodeViewset, base_name="code")
#配置用户的url
router.register(r'users', UserViewset, base_name="users")
# 热搜词
router.register(r'hotsearchs', HotSearchsViewset, base_name="hotsearchs")

#收藏
router.register(r'userfavs',UserFavViewset,base_name='userfavs')

#地址
router.register(r'address',AddressViewset,base_name='address')

#用户留言
router.register(r'messages', LeavingMessageViewset, base_name="messages")

#购物车
router.register(r'shopcarts', ShoppingCartViewset, base_name="shopcarts")

#订单相关
router.register(r'orders', OrderViewset, base_name="orders")

#轮播图
router.register(r'banners', BannerViewset, base_name="banners")

# 首页系列商品展示url
router.register(r'indexgoods', IndexCategoryViewset, base_name="indexgoods")
# goods_list = GoodsListViewSet.as_view({
#     'get': 'list',
# })
urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('ueditor/', include('DjangoUeditor.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
    # 文件
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
    #商品列表页
    # url(r'goods/$',GoodsListView.as_view(),name="good-list"),
    #文档
    url(r'docs/',include_docs_urls(title="海鲜商城")),

    url(r'^', include(router.urls)),
    #drf自带的token认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),
    #JWT的认证接口
    url(r'^login/', obtain_jwt_token),
    # url(r'goods/$',GoodsListViewSet.as_view())
    # url(r'^goods/$', goods_list, name='goods-list'),
    # 首页
    url(r'^index/', TemplateView.as_view(template_name="index.html"), name="index"),
    # 配置支付宝支付相关接口的url
    path('alipay/return/', AliPayView.as_view()),
]
