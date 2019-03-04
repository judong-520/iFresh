import time
import uuid
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from user.models import UserModel
from celery_tasks.tasks import send_email


def rename_files(filename):
    end_name = str(filename).split('.')[-1]
    now = time.strftime('%Y%m%d%H%M%S', time.localtime())
    sign = uuid.uuid4().hex
    full_name = now + sign + '.' + end_name
    return full_name


def login_required(view_fuc):
    def inner(request, *args, **kwargs):
        try:
            user_id = request.session.get('user_id', None)
            if user_id:
                return view_fuc(request, *args, **kwargs)
            else:
                return redirect(reverse('user:login'))
        except Exception as err:
            print('装饰器异常：', err)
            return redirect(reverse('user:login'))
    return inner


def register(request):
    if request.method == 'GET':
        return render(request, 'user/user_register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pwd = request.POST.get('password')
        face = request.FILES.get('icon')
        if not all([username, email, pwd]):
            msg = '用户名、邮箱或密码不能为空'
            return render(request, 'user/user_register.html', {'msg': msg})

        name_count = UserModel.objects.filter(username=username).count()
        if name_count != 0:
            msg = '该昵称已被注册'
            return render(request, 'user/user_register.html', {'msg': msg})

        email_count = UserModel.objects.filter(email=email).count()
        if email_count != 0:
            msg = '该邮箱已被注册'
            return render(request, 'user/user_register.html', {'msg': msg})

        user = UserModel()
        user.username = username
        user.email = email
        user.password = make_password(pwd)
        if face:
            user.icon = face
        user.save()
        # 发送邮件
        receivers = [email]
        topic = '爱鲜蜂'
        msg = '欢迎注册爱鲜蜂，希望你每天购物愉快'
        send_email.delay(receivers, topic, msg)   # 使用celery异步发送邮件
        return redirect(reverse('user:login'))


def login(request):
    if request.method == 'GET':
        return render(request, 'user/user_login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = UserModel.objects.get(username=username)
        # print(username, password, user.password, check_password(password, user.password))
        if not all([username, password]):
            msg = '用户名或密码不能为空'
            return render(request, 'user/user_login.html', {'msg': msg})

        if not user:
            msg = '该用户不存在'
            render(request, 'user/user_login.html', {'msg': msg})

        if check_password(password, user.password):
            request.session['user_id'] = user.id
            request.session['user'] = user.username
            request.session.set_expiry(60*60*24*3)  # 过期时间3天
            url_path = request.get_full_path()
            return redirect(reverse('mine:index'))
        msg = '密码错误'
        return render(request, 'user/user_login.html', {'msg': msg})


def logout(request):
    request.session.clear()
    return redirect(reverse('user:login'))


