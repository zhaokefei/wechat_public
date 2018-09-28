from django.conf.urls import url
from werobot.contrib.django import make_view
from werobot import WeRoBot

from wechat.views import werobot_view

robot = WeRoBot(
    token='feifeiwechat',
    app_id='wxde12b488de883dab',
    app_secret='7b638241ad308dab37f1f2fe7ea97103')

urlpatterns = [
    url(r'^$', werobot_view, name='robot')
]
