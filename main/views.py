# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from main.models import ShortenedUrl
from django.http import JsonResponse
from hashids import Hashids
import json


def home_page(request):
    """ Serves the home page """
    return render(request, 'main/home.html')


def shorten_url(request):
    """ Shortens URLs given a longer URL with optional hash """
    # Parse request body
    data = json.loads(request.body)
    url = data.get('url', '')
    hash = data.get('hash', '')
    if hash:
        # If hash exists, create or retrieve based on url and hash combination
        # If such combination exists, a new row will not be created
        shortened_url, _ = ShortenedUrl.objects.get_or_create(
            url=url,
            hash=hash
        )
    else:
        # If only the URL is given, get or create based on that URL
        # It's created only when the URL does not exist yet
        shortened_url, created = ShortenedUrl.objects.get_or_create(
            url=url,
            auto_hashed=True
        )
        if created:
            # This is a new URL so create a hash
            hashids = Hashids(min_length=8)
            shortened_url.hash = hashids.encode(shortened_url.id)
            shortened_url.save()
    # Form the short URL response
    domain = request.build_absolute_uri('/')[:-1]
    short_url = domain + '/' + shortened_url.hash
    response = {
        'short_url': short_url
    }
    return JsonResponse(response)


def redirect_url(request, hash):
    """ Redirects a short URL to the stored long URL """
    shortened_url = ShortenedUrl.objects.get(
        hash=hash
    )
    return redirect(shortened_url.url)
