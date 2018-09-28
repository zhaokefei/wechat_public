# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class UserStatus():
    SUBSCRIBE = 1
    UNSUBSCRIBE = 2
    CHOICES = (
        (SUBSCRIBE, '关注中'),
        (UNSUBSCRIBE, '取消关注'),
    )


class Account(models.Model):
    """账号表"""
    name = models.CharField(max_length=50, help_text='账号名称')
    open_id = models.CharField(max_length=50, unique=True, help_text='账号openID')
    token_id = models.CharField(max_length=50, help_text='账号token')
    app_id = models.CharField(max_length=50, help_text='账号ID')
    app_secret = models.CharField(max_length=255, help_text='账号密钥')
    related_url = models.CharField(max_length=255, help_text='关联的url地址')
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'account'


class User(models.Model):
    """用户表"""
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='users', help_text='关联账号')
    open_id = models.CharField(max_length=50)
    free_count = models.IntegerField(default=10, help_text='免费使用额度')
    buy_count = models.IntegerField(default=0, help_text='购买使用额度')
    status = models.IntegerField(default=1, help_text='用户状态')
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.open_id

    class Meta:
        unique_together = ('account', 'open_id')
        db_table = 'user'


class Message(models.Model):
    """用户聊天消息表"""
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='messages', help_text='关联账号')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', help_text='消息用户')
    type = models.IntegerField(help_text='消息类型')
    content = models.CharField(max_length=1000, help_text='消息内容')

    class Meta:
        db_table = 'message'


class Category(models.Model):
    """资源分类表"""
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='categories', help_text='关联账号')
    name = models.CharField(max_length=50, unique=True, help_text='资源分类名称')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'


class Resources(models.Model):
    """资源表"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='resources', help_text='关联分类')
    name = models.CharField(max_length=50, help_text='资源名称')
    image = models.ImageField(upload_to='resource_imgs', null=True, help_text='资源图片')
    type = models.IntegerField(help_text='资源类型')
    description = models.TextField(help_text='资源描述', null=True)
    share_url = models.CharField(max_length=255, help_text='分享链接')
    share_password = models.CharField(max_length=36, help_text='分享码')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'resources'


class Keywords(models.Model):
    """关键字表"""
    name = models.CharField(max_length=50, help_text='关键字名称')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'keywords'


class ResourceKeywordsMap(models.Model):
    """资源关键字对应表"""
    resource = models.ForeignKey(Resources, on_delete=models.CASCADE, related_name='resource_keywords_map', help_text='关联资源')
    keyword = models.ForeignKey(Keywords, on_delete=models.CASCADE, related_name='resource_keywords_map', help_text='关联关键字')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'resource_keywords_map'


class ManageUser(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='manageUsers', help_text='关联账号')
    name = models.CharField(max_length=50)
    qrcode = models.ImageField(upload_to='user_qrcode')
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'manage_user'
