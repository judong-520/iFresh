from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.cache import cache
# Create your views here.
from django.urls import reverse
from user.models import Goods, FoodType


def index(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('market:market', args=(104749, 0, 0)))


def market(request, typeid, childid, sortid):
    """
    :param typeid: 种类排序、一级分类
    :param childid: 种类子排序、二级分类
    :param sortid: 分类排序、比如：价格排序、销量排序
    """
    data = cache.get('market_data', None)
    if data is None:
        all_food_types = FoodType.objects.all()

        food_type = FoodType.objects.filter(typeid=typeid).first()
        child_type_names = food_type.childtypenames
        child_type_list = child_type_names.split('#')
        type_id_list = []
        for child_type in child_type_list:
            type_id = str(child_type).split(':')
            type_id_list.append(type_id)

        if childid == '0':
            all_goods = Goods.objects.filter(categoryid=typeid)
        else:
            all_goods = Goods.objects.filter(categoryid=typeid, childcid=childid)

        if sortid == '1':
            all_goods = all_goods.order_by('productnum')
        elif sortid == '2':
            all_goods = all_goods.order_by('-price')
        elif sortid == '3':
            all_goods = all_goods.order_by('price')
        data = {'all_food_types': all_food_types,
                'type_id_list': type_id_list,
                'typeid': typeid,
                'childid': childid,
                'all_goods': all_goods}
        cache.set('market_data', data)
    return render(request, 'market/market.html', data)


def add_goods_num(request):
    if request.method == 'POST':
        goods_id = request.POST.get('goods_id')
        num = int(request.POST.get('num'))
        goods = Goods.objects.filter(id=goods_id).first()
        store_num = goods.storenums
        if num < store_num:
            num += 1
            # goods.storenums = goods.storenums - num
            # goods.save()
            data = {'code': 200, 'msg': 'OK', 'num': num}
            return JsonResponse(data)
        else:
            data = {'code': 1090, 'msg': '不能超过该商品的最大库存量'}
            return JsonResponse(data)


def sub_goods_num(request):
    goods_id = request.POST.get('goods_id')
    num = int(request.POST.get('num'))
    goods = Goods.objects.filter(id=goods_id).first()
    if num > 0:
        num -= 1
        # goods.storenums = goods.storenums - num
        # goods.save()
        data = {'code': 200, 'msg': 'OK', 'num': num}
        return JsonResponse(data)
    else:
        data = {'code': 1080, 'msg': '商品数量不能小于0'}
        return JsonResponse(data)

