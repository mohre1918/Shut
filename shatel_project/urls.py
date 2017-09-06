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


from django.conf.urls import url, include
from django.contrib import admin
from shatel_app import views
from django.contrib.auth import views as auth_views

from shatel_app.forms import LoginForm


urlpatterns = [

    url(r'^admin/', admin.site.urls),
    # url(r'^gchart/', Gchart_view.gchart),
    url(r'', include('shatel_app.urls')),
    url(r'raw_data/', include('shatel_raw_app.urls')),
    # url(r'^login/$', views.login, {'template_name': 'login.html'}),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name = "login"),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login'}),

]
