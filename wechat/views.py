# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import thread

import time
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views import View
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
# Create your views here.
from wechat.generate_wechat_image import GenerateWechatImage

wechat_instance = WechatBasic(
    token='feifeiwechat',
    appid='wxde12b488de883dab',
    appsecret='7b638241ad308dab37f1f2fe7ea97103'
)


class WechatRequest(View):

    def get(self, request, *args, **kwargs):
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        echostr = request.GET.get('echostr', '')
        if not wechat_instance.check_signature(
                signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest('Verify Failed')

        return HttpResponse(echostr, content_type="text/plain")

    def post(self, request, *args, **kwargs):
        try:
            wechat_instance.parse_data(data=request.body)
        except ParseError:
            return HttpResponseBadRequest('Invalid XML Data')

        # 获取解析好的微信请求信息
        message = wechat_instance.get_message()
        from_user_name = message.source

        # 关注事件以及不匹配时的默认回复
        response = wechat_instance.response_text(
            content=(
                '感谢您的关注！\n回复【功能】两个字查看支持的功能，还可以回复任意内容开始聊天'
            ))
        if isinstance(message, TextMessage):
            content = message.content.strip()
            if content == '功能':
                reply_text = '目前支持的功能：\n1. 回复【二维码】获取登录二维码\n' \
                             '2. 扫码成功后，回复【头像】获取头像'
                response = wechat_instance.response_text(content=reply_text)
            elif content == '二维码':
                user = GenerateWechatImage(user_name=from_user_name)
                thread.start_new_thread(user.try_login, ())
                count = 0
                while not user.qrcode:
                    time.sleep(0.7)
                    count += 1
                    print('wait...')
                    if count >= 5:
                        print('timeout...')
                        return HttpResponse(response, content_type="application/xml")
                media_id = wechat_instance.upload_media(
                    'image', user.qrcode)['media_id']
                print('get media_id: %s' % media_id)
                response = wechat_instance.response_image(media_id=media_id)
            elif content == '头像':
                file_path = '/'.join([from_user_name, 'multi_img.jpg'])
                exist_path = os.path.exists(file_path)
                if not exist_path:
                    reply_text = '头像生成中...请耐心等待(若未扫码登录则无法获取头像哦!)'
                    response = wechat_instance.response_text(content=reply_text)
                else:
                    read_file = open(file_path, str('r+'))
                    media_id = wechat_instance.upload_media(
                        'image', read_file)['media_id']
                    print('get media_id: %s' % media_id)
                    response = wechat_instance.response_image(media_id=media_id)
        return HttpResponse(response, content_type="application/xml")

