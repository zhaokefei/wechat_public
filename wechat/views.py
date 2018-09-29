#! /usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
from werobot.replies import TextReply, ImageReply
from wechat.urls import robot as bot
from wechat.models import *
from wechat_public.settings import BASE_DIR

SUBSCRIBE_CONTENT = """欢迎关注, 输入【功能】查看可支持的功能, \n随意输入字符可视为关键字查询现有资源。\n 免费查看资源额度为3次，如需再次查看，请联系xxx购买资源次数"""
FUNCTION_SUPPORT = """输入中括号内字符查看对应的项目\n【分类】: 可查询的资源类目\n【购买资源】: 推送助手微信号，添加购买"""
MATCH_PATTERN = r'R(\s*)(\d+)'
DEFAULT_CONTACT = '公众小助手\nzhao546109656'
pattern = re.compile(MATCH_PATTERN)

client = bot.client


def generate_media(media_type, media_file):
    file = open(media_file, 'rb')
    data = client.upload_media(media_type, file)
    media_id = data.get('media_id')
    if media_id:
        return media_id
    return False


@bot.text
def handle_text(message):
    account = Account.objects.get(open_id=message.target)
    user, _ = User.objects.get_or_create(open_id=message.source, account=account)
    content = message.content.strip()
    if content == '功能':
        reply_content = FUNCTION_SUPPORT
    elif content == '购买资源':
        manage_users = ManageUser.objects.filter(account=account)
        if manage_users.exists():
            qrcode_url = os.path.join(BASE_DIR, manage_users.first().qrcode.url)
            media_id = generate_media('image', qrcode_url)
            if media_id:
                return ImageReply(message=message, media_id=media_id)
            else:
                return TextReply(message=message, content='\n'.join([manage_users.first().name,
                                                                     manage_users.first().wechat_id]))
        reply_content = DEFAULT_CONTACT
    elif content == '分类':
        categories = Category.objects.filter(account=account)
        if not categories.exists():
            reply_content = '未找到分类信息'
        else:
            item = [str(category.id) + '. ' + category.name for category in categories]
            content = '\n'.join(item)
            reply_content = '可根据分类编号查看具体分类信息\n' + content
    elif content.isdigit():
        resources = Resources.objects.filter(
            category__account=account, category_id=content.isdigit())
        if not resources.exists():
            reply_content = '未找到该分类下的资源信息'
        else:
            item = ['R' + str(resource.id) + '. ' + resource.name for resource in resources]
            content = '\n'.join(item)
            reply_content = '可根据资源编号查询具体资源信息\n' + content
    elif pattern.match(content):
        resource_id = pattern.match(content).group(2)
        try:
            resource = Resources.objects.get(id=int(resource_id))
            if user.free_count:
                user.free_count = user.free_count - 1
                user.save()
                reply_content = ' '.join([resource.name,
                                 resource.share_url, resource.share_password])
            elif user.buy_count:
                user.free_count = user.free_count - 1
                user.save()
                reply_content = ' '.join([resource.name,
                                 resource.share_url, resource.share_password])
            else:
                reply_content = '没有可用额度, 请联系xxx购买额度获取资源'
        except Resources.DoesNotExist:
            reply_content = '未找到对应的资源信息，请确认是否输入正确'
    else:
        resources = Resources.objects.filter(
            category__account=account, name__icontains=content)
        if not resources.exists():
            reply_content = '未找到改关键字下的资源信息'
        else:
            item = ['R' + str(resource.id) + '. ' + resource.name for resource in resources]
            content = '\n'.join(item)
            reply_content = '可根据资源编号查询具体资源信息\n' + content
    return TextReply(message=message, content=reply_content)


@bot.subscribe
def handle_subscribe(message):
    account = Account.objects.get(open_id=message.target)
    user, _ = User.objects.update_or_create(
        account=account, open_id=message.source,
        defaults={'status': UserStatus.SUBSCRIBE})
    return TextReply(message=message, content=SUBSCRIBE_CONTENT)


@bot.unsubscribe
def handle_unsubscribe(message):
    account = Account.objects.get(open_id=message.target)
    User.objects.update_or_create(
        account=account, open_id=message.source,
        defaults={'status': UserStatus.UNSUBSCRIBE})
    return TextReply(message=message, content='欢迎再次关注')


