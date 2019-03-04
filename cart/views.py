from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from user.models import UserInfoModel, CartModel, Goods
from user.views import login_required


@login_required
def cart(request):
    if request.method == 'GET':
        user_id = request.session['user_id']
        infos = UserInfoModel.objects.filter(user_id=user_id).all()
        carts = CartModel.objects.filter(user_id=user_id).all()
        return render(request, 'cart/cart.html', {'infos': infos, 'carts': carts})


@login_required
def add_goods_num(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        goods_id = request.POST.get('goods_id')
        goods = Goods.objects.filter(id=goods_id).first()
        cart = CartModel.objects.filter(user_id=user_id, goods_id=goods_id).first()
        if cart.c_num <= goods.storenums:
            data = {'code': 200, 'msg': 'OK'}
            cart.c_num += 1
            cart.save()
            data['c_num'] = cart.c_num
            return JsonResponse(data)
        else:
            data = {'code': 1090, 'msg': '不能超过该商品的最大库存量'}
            return JsonResponse(data)


@login_required
def sub_goods_num(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        goods_id = request.POST.get('goods_id')
        cart = CartModel.objects.filter(goods_id=goods_id, user_id=user_id).first()
        if cart.c_num > 1:
            data = {'code': 200, 'msg': 'ok'}
            cart.c_num -= 1
            cart.save()
            data['c_num'] = cart.c_num
            return JsonResponse(data)
        else:
            data = {'code': 1080, 'msg': '商品选购数量不能小于1'}
            return JsonResponse(data)


@login_required
def change_status(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        cart = CartModel.objects.filter(id=cart_id).first()
        data = {'code': 200, 'msg': 'ok'}
        is_select = cart.is_select
        is_select = not is_select
        data['is_select'] = is_select
        cart.is_select = is_select
        cart.save()
        return JsonResponse(data)


@login_required
def select_all(request):
    if request.method == 'POST':
        sign = request.POST.get('sign')
        data = {'code': 200,'msg': 'OK'}
        user_id = request.session.get('user_id')
        carts = CartModel.objects.filter(user_id=user_id).all()
        ids = []
        if sign:
            for cart in carts:
                cart.is_select = False
                cart.save()
                ids.append(cart.id)
        else:
            for cart in carts:
                cart.is_select = True
                cart.save()
                ids.append(cart.id)
        data['sign'] = not sign
        data['ids'] = ids
        return JsonResponse(data)


@login_required
def total_price(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        carts = CartModel.objects.filter(user_id=user_id, is_select=True).all()
        total = 0
        for cart in carts:
            price = Goods.objects.filter(id=cart.goods_id).first().price
            total += price * cart.c_num
        data = {'code': 200, 'msg': 'ok', 'total': total}
        return JsonResponse(data)





