# from django.conf.urls import url
from django.urls import re_path

from . import views

urlpatterns=[
    re_path('^$',views.news_of_day,name='newsToday'),
    re_path(r'^archives/(\d{4}-\d{2}-\d{2})/$',views.past_days_news,name = 'pastNews')
    ]
