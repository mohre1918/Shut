# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps
from django.contrib import admin


# Register your models here.
from models import *

class Admin(admin.ModelAdmin):
    list_display = ['id','stime', 'duration', 'ocgpn', 'ocdpn', 'crinfo', 'idesc', 'odesc', 'caller', 'called']
    search_fields = ['id','stime', 'duration', 'ocgpn', 'ocdpn', 'crinfo', 'idesc', 'odesc', 'caller', 'called']
    list_filter = ['crinfo', 'idesc', 'odesc', 'caller', 'called']
class Admin2(admin.ModelAdmin):
    list_display = ['id','stime', 'duration', 'ocgpn', 'ocdpn',  'caller', 'called']
    search_fields = ['id','stime', 'duration', 'ocgpn', 'ocdpn',  'caller', 'called']
    list_filter = ['caller', 'called']

#
# admin.site.unregister(MgwAbzKrj)
# admin.site.unregister(MgwArbPc)
# admin.site.unregister(MgwBouBhmn)
# admin.site.unregister(MgwCmbPc)
# admin.site.unregister(MgwEsfEmam1)
# admin.site.unregister(MgwEsfEmam2)


app = apps.get_app_config('shatel_app')

for model_name, model in app.models.items():
    if model.__name__ == 'AvaBcfCdr':
        admin.site.register(model, Admin2)
    else:
        admin.site.register(model, Admin)
