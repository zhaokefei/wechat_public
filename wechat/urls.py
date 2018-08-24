from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from wechat import views

urlpatterns = [
    url(r'^$', csrf_exempt(views.WechatRequest.as_view()), name='home')
]
