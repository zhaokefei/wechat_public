#! /usr/bin/env python
# -*- coding:utf-8 -*-
import re
from werobot.replies import TextReply

from wechat.urls import robot as bot
from wechat.models import *

SUBSCRIBE_CONTENT = '欢迎关注'
MATCH_PATTERN = r'R(\s*)(\d+)'
pattern = re.compile(MATCH_PATTERN)


@bot.text
def handle_text(message):
    account = Account.objects.get(open_id=message.target)
    user = User.objects.get(open_id=message.source)
    content = message.content.strip()
    if content == '分类':
        categories = Category.objects.filter(account=account)
        if not categories.exists():
            return '未找到分类信息'
        item = [category.id + '. ' + category.name for category in categories]
        content = '\n'.join(item)
        reply_content = '可根据分类编号查看具体分类信息\n' + content
        return reply_content
    elif content.isdigit():
        resources = Resources.objects.filter(
            category__account=account, category_id=content.isdigit())
        if not resources.exists():
            return '未找到该分类下的资源信息'
        item = ['R' + resource.id + '. ' + resource.name for resource in resources]
        content = '\n'.join(item)
        reply_content = '可根据资源编号查询具体资源信息\n' + content
        return reply_content
    elif pattern.match(content):
        resource_id = pattern.match(content).group(2)
        try:
            resource = Resources.objects.get(id=resource_id)
            if user.free_count:
                user.free_count = user.free_count - 1
                user.save()
                return ' '.join([resource.name,
                                 resource.share_url, resource.share_password])
            elif user.buy_count:
                user.free_count = user.free_count - 1
                user.save()
                return ' '.join([resource.name,
                                 resource.share_url, resource.share_password])
            else:
                return '没有可用额度, 请购买额度获取资源'
        except Resources.DoesNotExist:
            return '未找到对应的资源信息，请确认是否输入正确'
    else:
        resources = Resources.objects.filter(
            category__account=account, name__icontains=content)
        if not resources.exists():
            return '未找到该分类下的资源信息'
        item = ['R' + resource.id + '. ' + resource.name for resource in resources]
        content = '\n'.join(item)
        reply_content = '可根据资源编号查询具体资源信息\n' + content
        return reply_content


@bot.image
def handle_image(message):
    pass


@bot.subscribe
def handle_subscribe(message):
    account = Account.objects.get(open_id=message.target)
    user, created = User.objects.update_or_create(
        account=account, open_id=message.source,
        defaults={'status': UserStatus.SUBSCRIBE})
    if created:
        user.free_count = 10
        user.save()
    return TextReply(message=message, content=SUBSCRIBE_CONTENT)


@bot.unsubscribe
def handle_unsubscribe(message):
    account = Account.objects.get(open_id=message.target)
    User.objects.update_or_create(
        account=account, open_id=message.source,
        defaults={'status': UserStatus.UNSUBSCRIBE})
