from django.shortcuts import render
from user.models import OrderModel
from user.views import login_required

# Create your views here.
# 0 待付款， 1 待收货  2 待评价  3 退款/售后


@login_required
def order_info(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        orders = OrderModel.objects.filter(user_id=user_id).all()
        return render(request, 'order/order_info.html', {'orders': orders})


@login_required
def order_wait_pay(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        orders = OrderModel.objects.filter(user_id=user_id, o_status=0).all()
        return render(request, 'order/order_list_wait_pay.html', {'orders': orders})


@login_required
def order_payed(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        orders = OrderModel.objects.filter(user_id=user_id, o_status=1).all()
        return render(request, 'order/order_list_payed.html', {'orders': orders})
