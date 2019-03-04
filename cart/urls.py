from django.conf.urls import url
from cart import views

urlpatterns = [
    url(r'^index/', views.cart, name='index'),
    url(r'^add_num/', views.add_goods_num, name='add_num'),
    url(r'^sub_num/', views.sub_goods_num, name='sub_num'),
    url(r'^change_status/', views.change_status, name='change_status'),
    url(r'^select_all/', views.select_all, name='select_all'),
    url(r'^total_price/', views.total_price, name='total_price'),
]