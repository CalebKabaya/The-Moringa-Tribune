"""tribune URL Configuration

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
# from django.conf.urls import include
from django.conf.urls import include
from django.urls import re_path





from django.contrib.auth import views 

from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'',include('news.urls')),
    re_path(r'^accounts/', include('registration.backends.simple.urls')),
    # re_path(r'^logout/$', views.logout, {"next_page": '/'}), 
    re_path(r'^tinymce/', include('tinymce.urls')),
    re_path(r'^api-token-auth/', obtain_auth_token)




]
    # "token": "adcce2e43221327e1ead7fc8659bb7f7e1c85650"
