# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from main.models import ShortenedUrl


class ShortenedUrlAdmin(admin.ModelAdmin):
    list_display = ['url', 'hash', 'auto_hashed']


admin.site.register(ShortenedUrl, ShortenedUrlAdmin)
