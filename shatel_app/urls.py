"""GchartProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.auth.views import login
from django.shortcuts import redirect
from django.views.generic.base import RedirectView
import views


urlpatterns = [
    url(r'^dashboard/$', views.Dashboard),
    url(r'^OperatorAnalysis/$', views.Operator_analysis),
    url(r'^PrefixAnalysis/$', views.Prefix_analysis),
    url(r'^Myquery/$', views.Myquery),
    url(r'^dailyshatel/$', views.dailyshatel),
    url(r'^Periodshatel/$', views.Periodshatel),
    url(r'^dynamic/$', views.dynamic),
    url(r'^$', RedirectView.as_view(url='/dashboard')),
]
