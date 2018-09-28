# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from wechat.models import Account


class AccountAdmin(admin.ModelAdmin):
    # list页面要显示的字段
    list_display = ['name', 'open_id']

admin.site.register(Account, AccountAdmin)
