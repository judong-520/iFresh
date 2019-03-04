from django.conf.urls import url
from market import views

urlpatterns = [
    url(r'^index', views.index, name='index'),
    url(r'^market/(\d+)/(\d+)/(\d+)', views.market, name='market'),
    url(r'^add_num', views.add_goods_num, name='add_num'),
    url(r'^sub_num', views.sub_goods_num, name='sub_num'),
]
