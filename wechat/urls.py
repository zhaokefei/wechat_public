from django.conf.urls import url
from werobot import WeRoBot
from werobot.contrib.django import make_view

robot = WeRoBot(
    token='feifeiwechat',
    app_id='wxde12b488de883dab',
    app_secret='7b638241ad308dab37f1f2fe7ea97103')

urlpatterns = [
    url(r'^$', make_view(robot), name='robot')
]

from wechat.views import *
