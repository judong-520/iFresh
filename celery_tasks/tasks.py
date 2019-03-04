import time
from email.header import Header
from email.mime.text import MIMEText
from smtplib import SMTP
from django.template import loader, RequestContext
from celery import Celery

import os
import django
from django.shortcuts import render

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "axf.settings")
django.setup()

from user.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow
from axf import settings
celery = Celery('tasks', broker='redis://47.98.173.29:6379/1', backend='redis://47.98.173.29:6379/1')


@celery.task
def send_email(receivers, topic, msg, sender='930047011@qq.com'):
    """
    :param receivers: 收件人列表
    :param topic:  邮件主题
    :param msg:  邮件小提提
    :param sender: 邮件发送者
    :return:
    """
    for receiver in receivers:
        try:
            start = time.time()
            message = MIMEText(msg, 'plain', 'utf-8')  # 构建MINEtext对象
            message['From'] = Header(sender, 'utf-8')  # 编辑发件人
            message['To'] = Header(receiver, 'utf-8')  # 编辑收件人
            message['Subject'] = Header(topic, 'utf-8')

            smtper = SMTP('smtp.qq.com', 25)
            smtper.login(sender, 'urrvfqmfeyolbcga')  # login()方法用来登录SMTP服务器
            smtper.sendmail(sender, receiver, message.as_string())
            smtper.quit()
            time.sleep(10)
            end = time.time()
            print('邮件发至：%s， 成功……, 耗时%s秒' % (receiver, end - start))
        except Exception as err:
            print('邮件发至：%s， 失败……错误信息为：%s' % (receiver, err))
            continue


@celery.task
def build_staic_html():
    """celery生成静态页面"""
    print('生成静态页面开始')
    main_wheel = MainWheel.objects.all()
    main_nav = MainNav.objects.all()
    must_buy = MainMustBuy.objects.all()
    main_shop = MainShop.objects.all()
    main_show = MainShow.objects.all()
    temp = loader.get_template('staic_html/staic_home.html')  # 加载模板文件，生成模板实例
    # context = RequestContext(request, {'main_wheel': main_wheel,
    #                                    'main_nav': main_nav,
    #                                    'must_buy': must_buy,
    #                                    'main_shop': main_shop,
    #                                    'main_show': main_show})  # 定义模板上下文
    # staic_home = temp.render(context)
    staic_home = temp.render({'main_wheel': main_wheel,
                              'main_nav': main_nav,
                              'must_buy': must_buy,
                              'main_shop': main_shop,
                              'main_show': main_show})  # 渲染模板
    save_path = os.path.join(settings.BASE_DIR, 'static/home.html')  # 生成静态文件
    print(save_path)
    with open(save_path, 'w') as f:
        f.write(staic_home)
    print('生成静态页面结束')


# celery -A celery_tasks.tasks --pool=eventlet worker --loglevel=info
# celery -A celery_tasks.tasks --pool=eventlet worker -l info
