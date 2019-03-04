from django.shortcuts import render

from user.models import UserModel, OrderModel
from user.views import login_required

# Create your views here.


def mine(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id', None)
        try:
            user = UserModel.objects.get(id=user_id)
        except Exception as e:
            user = None
        if user:
            # 0 待付款， 1 待收货  2 待评价  3 退款/售后
            wait_for_paying = OrderModel.objects.filter(user_id=user_id, o_status=0).count()
            wait_for_receiving = OrderModel.objects.filter(user_id=user_id, o_status=1).count()
            wait_for_evaluating = OrderModel.objects.filter(user_id=user_id, o_status=2).count()
            refund = OrderModel.objects.filter(user_id=user_id, o_status=3).count()
            return render(request, 'mine/mine.html', {'user': user,
                                                      'wait_for_paying': wait_for_paying,
                                                      'wait_for_receiving': wait_for_receiving,
                                                      'wait_for_evaluating': wait_for_evaluating,
                                                      'refund': refund
                                                      })
        return render(request, 'mine/mine.html')
