from django.conf.urls import url
from wechat.views import werobot_view


urlpatterns = [
    url(r'^$', werobot_view, name='robot')
]
