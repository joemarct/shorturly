# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class ShortenedUrl(models.Model):
    url = models.URLField(max_length=300)
    hash = models.CharField(max_length=15)
    auto_hashed = models.BooleanField(default=False)