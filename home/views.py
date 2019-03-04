from django.shortcuts import render
from django.core.cache import cache

# Create your views here.
from user.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow


def home(request):
    data = cache.get('home_data', None)  # 从缓存中拿数据
    # print('判断缓存')
    if data is None:
        # print('设置缓存')
        main_wheel = MainWheel.objects.all()
        main_nav = MainNav.objects.all()
        must_buy = MainMustBuy.objects.all()
        main_shop = MainShop.objects.all()
        main_show = MainShow.objects.all()
        data = {'main_wheel': main_wheel,
                'main_nav': main_nav,
                'must_buy': must_buy,
                'main_shop': main_shop,
                'main_show': main_show}
        cache.set('home_data', data, 3600)   # 设置缓存
    return render(request, 'home/home.html', data)
