# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from models import *
# Create your views here.

# msg = Messages.objects.filter(reciever = request.user)
def fraud(request):
    a = MgwAbzKrjRaw.objects.filter(ocgpn__icontains="9100")[0].ocgpn
    print a
    return HttpResponse("salam")
