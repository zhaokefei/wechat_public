# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
import html

from django.http import HttpResponseForbidden, HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from werobot import WeRoBot


robot = WeRoBot(
    token='feifeiwechat',
    app_id='wxde12b488de883dab',
    app_secret='7b638241ad308dab37f1f2fe7ea97103')


@csrf_exempt
def werobot_view(request):
    timestamp = request.GET.get("timestamp", "")
    nonce = request.GET.get("nonce", "")
    signature = request.GET.get("signature", "")

    if not robot.check_signature(
            timestamp=timestamp, nonce=nonce, signature=signature
    ):
        return HttpResponseForbidden(
            robot.make_error_page(
                html.escape(request.build_absolute_uri())
            )
        )
    if request.method == "GET":
        return HttpResponse(request.GET.get("echostr", ""))
    elif request.method == "POST":
        message = robot.parse_message(
            request.body,
            timestamp=timestamp,
            nonce=nonce,
            msg_signature=request.GET.get("msg_signature", "")
        )
        return HttpResponse(
            robot.get_encrypted_reply(message),
            content_type="application/xml;charset=utf-8"
        )
    return HttpResponseNotAllowed(['GET', 'POST'])



