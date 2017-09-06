# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps
from django.contrib import admin


# Register your models here.
from models import *

class Admin(admin.ModelAdmin):
    list_display = ['id','stime', 'duration', 'ocgpn', 'ocdpn', 'crinfo', 'idesc', 'odesc']
    search_fields = ['id','stime', 'duration', 'ocgpn', 'ocdpn', 'crinfo', 'idesc', 'odesc']
    list_filter = ['crinfo', 'idesc', 'odesc']


app = apps.get_app_config('shatel_raw_app')

for model_name, model in app.models.items():
    admin.site.register(model, Admin)
