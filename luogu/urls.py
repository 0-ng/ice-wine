"""sch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path
from . import views as luogu
from django.contrib.auth.views import LoginView

app_name = 'luogu'
urlpatterns = [
    path('', luogu.index),
    path('index.html', luogu.index),
    path('购物车.html', luogu.shopping_cart),
    path('shopping_cart_change', luogu.shopping_cart_change),
    path('个人中心.html', luogu.personal_center),
    path('订单结算.html/<int:order_id>', luogu.order_settlement),
    path('get_address/<int:id>', luogu.get_address),
    path('订单详情.html/<int:order_id>', luogu.order_details),
    path('订单管理.html', luogu.order_management),
    path('用户登录.html', luogu.user_login),
    path('用户注册.html', luogu.user_register),
    path('new_address', luogu.new_address),
    path('地址管理.html', luogu.address_management),
    path('商品详情页.html/<int:product_id>', luogu.product_details),
    path('商品分类.html', luogu.product_classification),
    path('人气推荐.html', luogu.popular_recommendation),
    path('选择支付方式.html/<int:order_id>', luogu.payment_method_selection),
    path('第三方支付.html/<int:order_id>', luogu.third_party_payment),
    path('相似商品.html', luogu.similar_products),
    path('用户隐私协议.html', luogu.user_privacy_agreement),
    path('我的收藏.html', luogu.collection),
    path('感兴趣都分类.html', luogu.interested_classification),
    path('在线客服.html', luogu.online_service),
    path('购物常见问题.html', luogu.help_center),
    path('支付成功.html/<int:order_id>', luogu.successful_payment),
    # url(r'^login/$', luogu.login),
    # url('logout$', luogu.logout),
    # url('^404$', luogu.error),
    # url('register$', luogu.register),
    # url('forgetPassword$', luogu.forgetPassword),
    # url('changePassword$', luogu.changePassword),
    # url(r'^scratchpaper/$', luogu.scratchpaper),
    # url(r'^hub/$', luogu.hub),
    # path(r'detail/', luogu.detail),
    # url('feedback$', luogu.feedback),
    # path('hub/<hubno>', luogu.detail),
    # path('user/<name>/', luogu.personalPage),
    # path('write_note/<no>/', luogu.write_note),
    # path('notes/<name>/', luogu.notes_list),
    # path('show-<int:sid>.html', luogu.note_show, name='show'),  # 内容页
    # path('delete_note', luogu.delete_note),  # 删除笔记
    #
    # path('xadmin/test_view', luogu.test),
    path('test', luogu.test),
    path('init', luogu.init),
    url(r'^data/(?P<id>\d+)/$', luogu.data),
    url(r'^update/', luogu.update)
]