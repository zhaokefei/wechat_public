# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from wechat.models import *


class AccountAdmin(admin.ModelAdmin):
    # list页面要显示的字段
    list_display = ['name', 'open_id']


class UserAdmin(admin.ModelAdmin):
    # list页面要显示的字段
    list_display = ['account', 'open_id',
                    'free_count', 'buy_count', 'status']


class MessageAdmin(admin.ModelAdmin):
    # list页面要显示的字段
    list_display = ['account', 'user', 'type']


class CategoryAdmin(admin.ModelAdmin):
    # list页面要显示的字段
    list_display = ['account', 'name']


class ResourcesAdmin(admin.ModelAdmin):
    # list页面要显示的字段
    list_display = ['category', 'name']


class KeywordsAdmin(admin.ModelAdmin):
    # list页面要显示的字段
    list_display = ['name',]


class ResourceKeywordsMapAdmin(admin.ModelAdmin):
    # list页面要显示的字段
    list_display = ['resource', 'keyword']


class ManageUserAdmin(admin.ModelAdmin):
    # list页面要显示的字段
    list_display = ['account', 'name']


admin.site.register(Account, AccountAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Resources, ResourcesAdmin)
admin.site.register(Keywords, KeywordsAdmin)
admin.site.register(ResourceKeywordsMap, ResourceKeywordsMapAdmin)
admin.site.register(ManageUser, ManageUserAdmin)
