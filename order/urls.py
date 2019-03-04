from django.conf.urls import url
from order import views

urlpatterns = [
    url(r'^info/', views.order_info, name='info'),
    url('^wait/pay/', views.order_wait_pay, name='wait_pay'),
    url('^payed/', views.order_payed, name='payed'),
]