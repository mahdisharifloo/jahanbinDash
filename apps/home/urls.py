# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('news',views.news_cards,name='news'),
    path('instagram',views.instagram_dashboard ,name='instagram'),
    path('twitter',views.twitter_dashboard ,name='twitter'),
    path('agency_news',views.agency_news_dashboard ,name='agency_news'),
    path('telegram_group',views.telegram_group_dashboard ,name='telegram_group'),
    path('telegram_chanel',views.telegram_chanel_dashboard ,name='telegram_chanel'),
    path('labeling',views.labeling ,name='labeling'),
    path('news/',views.filtered_news,name='filtered_news'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
