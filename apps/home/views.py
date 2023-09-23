# -*- encoding: utf-8 -*-
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import requests
import random
import json 
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from jdatetime import datetime as jdatetime
from datetime import datetime



def get_statistic_data(host):
    url =  f"http://{host}/get_statistics"

    # querystring = {
    #     'time_filter':time_filter
    # }
    payload = {}
    headers = {
    'accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload,
                                # params=querystring
                                )

    resp = json.loads(response.text)
    context = {
        "label_chart11" : resp["label_chart11"] ,
        "data_chart11" : resp["data_chart11"] ,
        "label_chart12" : resp["label_chart12"] ,
        "data_chart12" : resp["data_chart12"] ,
        "label_chart13" : resp["label_chart13"] ,
        "data_chart13" : resp["data_chart13"] ,
        "label_chart2" : resp["label_chart2"] ,
        "data_chart2" : resp["data_chart2"] ,
        "label_chart3" : resp["label_chart3"] ,
        "data_chart3" : resp["data_chart3"] ,
        "label_chart4" : resp["label_chart4"] ,
        "data_chart4" : resp["data_chart4"] ,
    }
    return context

def get_sunburst_data( host):
    url =  f"http://{host}/sunbert_churt_data"
    # querystring = {
    #     'time_filter':time_filter
    # }
    payload = {}
    headers = {
    'accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, 
                                # params=querystring
                                )

    context = json.loads(response.text)

    return context


def search_get_news( host,query ,time_filtering='6m', page=1):
    url = f"http://{host}/search"

    querystring = {
        "page":page,
        "query":query,
        "time_filtering":time_filtering
    }

    payload = ""
    headers = {"accept": "application/json"}

    response = requests.request("POST", url, data=payload, headers=headers, 
                                params=querystring
                                )

    data = json.loads(response.text)
    return data['news'],data['pages']


def get_news(host,
            page=1,
            sentiment='',
            category='',
            inteligence_service_category='',
            time_filtering='6m'):
    url = f"http://{host}/get_news"

    querystring = {
        "page":page,
        "sentiment":sentiment,
        "category":category,
        "inteligence_service_category":inteligence_service_category,
        "time_filtering":time_filtering
    }

    payload = ""
    headers = {"accept": "application/json"}

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring
                                )

    data = json.loads(response.text)
    return data['news'] ,data['pages']

def get_data_access_token():
    url = "http://94.182.215.123:10001/token"
    payload = 'grant_type=&username=mahdi&password=mahdi0059&scope=&client_id=&client_secret='
    headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return f"Bearer {json.loads(response.text)['access_token']}"

# token = get_data_access_token()

def get_for_labeling(platform):
    # token = get_data_access_token()
    category_list = ["اقتصادی","سیاسی","اجتماعی"]
    category = random.choice(category_list)
    url = f"http://94.182.215.123:10001/{platform}?category={category}&time_filtering=6m&count=1"
    payload = {}
    headers = {
    'accept': 'application/json',
    # 'Authorization': token
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        result = json.loads(response.text)
        return result['news'][0]

def update_info_service_label(platform,record_id,label):
    url = f"http://94.182.215.123:10001/{platform}_add_info_service_tag?record_id={record_id}&label={label}"
    # url = f"http://192.168.111.170:10001/{platform}_add_info_service_tag?record_id={record_id}&label={label}"
    payload = {}
    headers = {
    'accept': 'application/json',
    # 'Authorization': token
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        result = json.loads(response.text)
        return result


@login_required(login_url="/login/")
def index(request):
    time_filtering = request.GET.get('time_filtering', '6m') 
    platform = request.GET.get('platform', '') 
    instagram_host = f"{settings.STATISTIC_INSTAGRAM_API_URL}:10011"
    twitter_host = f"{settings.STATISTIC_TWITTER_API_URL}:10010"
    telegram_group_host = f"{settings.STATISTIC_TELEGRAM_GROUP_API_URL}:10012"
    telegram_channel_host = f"{settings.STATISTIC_TELEGRAM_CHANNEL_API_URL}:10013"
    news_agency_host = f"{settings.STATISTIC_NEWS_AGENCY_API_URL}:10014"
    host = news_agency_host
    if platform:
        if platform == "instagram":
            host = instagram_host
        elif platform == 'twitter':
            host = twitter_host
        elif platform == 'telgram_group':
            host = telegram_group_host
        elif platform == 'telegram_channel':
            host = telegram_channel_host
        elif platform == 'news_agency':
            host = news_agency_host
    # time_filtering = request.GET.get('time_filtering', '6m') 
    query = request.GET.get('query', '') 
    page = request.GET.get('page', '') 
    if query:
        news_list,pages = search_get_news(host=host,time_filtering=time_filtering,query=query,page=page)
        context = {
            "pages":pages,
            'news_list1':news_list[:int(len(news_list)/2)],
            'news_list2':news_list[int(len(news_list)/2):],
            }
        html_template = loader.get_template('home/notifications.html')
        return HttpResponse(html_template.render(context, request))
    context = {}
    # context = get_statistic_data()
    # sunburst_chart = get_sunburst_data()
    # news_list, _ = get_news()
    # context['rank_news_list1'] = news_list[:5]
    # context['rank_news_list2'] = news_list[5:]
    # context['sunburst'] = sunburst_chart
    
    # context['sunburst_parents'] =  sunburst_chart['parents']
    # context['sunburst_values'] =    sunburst_chart['values']  
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def filtered_news(request):
    context = {}
    # ---------query params--------------
    time_filtering = request.GET.get('time_filtering', '6m') 
    platform = request.GET.get('platform', '') 
    time_filtering = request.GET.get('time_filtering', '6m') 
    query = request.GET.get('query', '') 
    page = request.GET.get('page', '') 
    sentiment = request.GET.get('sentiment', '') 
    category = request.GET.get('category', '') 
    inteligence_service_category = request.GET.get('inteligence_service_category', '')     

    context['platform'] = platform
    context['time_filtering'] = time_filtering
    context['query'] = query
    context['page'] = page
    context['sentiment'] = sentiment
    context['category'] = category
    context['inteligence_service_category'] = inteligence_service_category
    # -----------------------------------

    instagram_host = f"{settings.STATISTIC_INSTAGRAM_API_URL}:10011"
    twitter_host = f"{settings.STATISTIC_TWITTER_API_URL}:10010"
    telegram_group_host = f"{settings.STATISTIC_TELEGRAM_GROUP_API_URL}:10012"
    telegram_channel_host = f"{settings.STATISTIC_TELEGRAM_CHANNEL_API_URL}:10013"
    news_agency_host = f"{settings.STATISTIC_NEWS_AGENCY_API_URL}:10014"
    host = news_agency_host
    if platform:
        if platform == "instagram":
            host = instagram_host
        elif platform == 'twitter':
            host = twitter_host
        elif platform == 'telgram_group':
            host = telegram_group_host
        elif platform == 'telegram_channel':
            host = telegram_channel_host
        elif platform == 'news_agency':
            host = news_agency_host

    if query:
        news_list,pages = search_get_news(host,query,time_filtering,page)
        context["pages"]=pages
        context['news_list1']=news_list[:int(len(news_list)/2)]
        context['news_list2']=news_list[int(len(news_list)/2):]
        html_template = loader.get_template('home/notifications.html')
        return HttpResponse(html_template.render(context, request))
    
    news_list , pages= get_news(host=host,
                            page=page,
                         sentiment=sentiment,
                         category=category,
                         inteligence_service_category=inteligence_service_category,
                         time_filtering=time_filtering)
    context["pages"]=pages
    context['news_list1']=news_list[:int(len(news_list)/2)]
    context['news_list2']=news_list[int(len(news_list)/2):]
    
    html_template = loader.get_template('home/notifications.html')
    return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def news_cards(request):
    platform = request.GET.get('platform', '') 
    time_filtering = request.GET.get('time_filtering', '6m') 
    instagram_host = f"{settings.STATISTIC_INSTAGRAM_API_URL}:10011"
    twitter_host = f"{settings.STATISTIC_TWITTER_API_URL}:10010"
    telegram_group_host = f"{settings.STATISTIC_TELEGRAM_GROUP_API_URL}:10012"
    telegram_channel_host = f"{settings.STATISTIC_TELEGRAM_CHANNEL_API_URL}:10013"
    news_agency_host = f"{settings.STATISTIC_NEWS_AGENCY_API_URL}:10014"
    host = news_agency_host
    if platform:
        if platform == "instagram":
            host = instagram_host
        elif platform == 'twitter':
            host = twitter_host
        elif platform == 'telgram_group':
            host = telegram_group_host
        elif platform == 'telegram_channel':
            host = telegram_channel_host
        elif platform == 'news_agency':
            host = news_agency_host
    time_filtering = request.GET.get('time_filtering', '6m') 
    query = request.GET.get('query', '') 
    page = request.GET.get('page', '') 
    if query:
        news_list,pages = search_get_news(host,query,time_filtering,page)
        context = {
            "pages":pages,
            'news_list1':news_list[:int(len(news_list)/2)],
            'news_list2':news_list[int(len(news_list)/2):],
            }
        html_template = loader.get_template('home/notifications.html')
        return HttpResponse(html_template.render(context, request))

    
    # instagram_host = f"{settings.STATISTIC_INSTAGRAM_API_URL}:10011"
    # twitter_host = f"{settings.STATISTIC_TWITTER_API_URL}:10010"
    # telegram_group_host = f"{settings.STATISTIC_TELEGRAM_GROUP_API_URL}:10012"
    # telegram_channel_host = f"{settings.STATISTIC_TELEGRAM_CHANNEL_API_URL}:10013"
    news_agency_host = f"{settings.STATISTIC_NEWS_AGENCY_API_URL}:10014"
    news_list , pages = get_news(host=news_agency_host,time_filtering=time_filtering)
    
    context = {'news_list1':news_list[:int(len(news_list)/2)],
                'news_list2':news_list[int(len(news_list)/2):],
                'pages':pages
               }
    
    html_template = loader.get_template('home/notifications.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):

    time_filtering = request.GET.get('time_filtering', '6m') 
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    # try:
    context = {}
    load_template = request.path.split('/')[-1]

    if load_template == 'admin':
        return HttpResponseRedirect(reverse('admin:index'))
    context['segment'] = load_template

    html_template = loader.get_template('home/' + load_template)
    return HttpResponse(html_template.render(context, request))

    # except template.TemplateDoesNotExist:

    #     html_template = loader.get_template('home/page-404.html')
    #     return HttpResponse(html_template.render(context, request))

    # except:
    #     html_template = loader.get_template('home/page-500.html')
    #     return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def instagram_dashboard(request):
    time_filtering = request.GET.get('time_filtering', '6m') 
    platform = request.GET.get('platform', '') 
    instagram_host = f"{settings.STATISTIC_INSTAGRAM_API_URL}:10011"
    twitter_host = f"{settings.STATISTIC_TWITTER_API_URL}:10010"
    telegram_group_host = f"{settings.STATISTIC_TELEGRAM_GROUP_API_URL}:10012"
    telegram_channel_host = f"{settings.STATISTIC_TELEGRAM_CHANNEL_API_URL}:10013"
    news_agency_host = f"{settings.STATISTIC_NEWS_AGENCY_API_URL}:10014"
    host = instagram_host
    if platform:
        if platform == "instagram":
            host = instagram_host
        elif platform == 'twitter':
            host = twitter_host
        elif platform == 'telgram_group':
            host = telegram_group_host
        elif platform == 'telegram_channel':
            host = telegram_channel_host
        elif platform == 'news_agency':
            host = news_agency_host
    time_filtering = request.GET.get('time_filtering', '6m') 
    query = request.GET.get('query', '') 
    page = request.GET.get('page', '') 
    host = f"{settings.STATISTIC_INSTAGRAM_API_URL}:10011"
    if query:
        news_list,pages = search_get_news(host,query,time_filtering,page)
        context = {
            "pages":pages,
            'news_list1':news_list[:int(len(news_list)/2)],
            'news_list2':news_list[int(len(news_list)/2):],
            }
        html_template = loader.get_template('home/notifications.html')
        return HttpResponse(html_template.render(context, request))
    
    context = get_statistic_data(host)
    sunburst_chart = get_sunburst_data(host)
    news_list, _ = get_news(host=host,time_filtering=time_filtering)
    context['rank_news_list1'] = news_list[:5]
    context['rank_news_list2'] = news_list[5:]
    context['sunburst_data'] = sunburst_chart
    
    # context['sunburst_parents'] =  sunburst_chart['parents']
    # context['sunburst_values'] =    sunburst_chart['values']  
    html_template = loader.get_template('home/dash_instagram.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def twitter_dashboard(request):
    time_filtering = request.GET.get('time_filtering', '6m') 
    platform = request.GET.get('platform', '') 
    instagram_host = f"{settings.STATISTIC_INSTAGRAM_API_URL}:10011"
    twitter_host = f"{settings.STATISTIC_TWITTER_API_URL}:10010"
    telegram_group_host = f"{settings.STATISTIC_TELEGRAM_GROUP_API_URL}:10012"
    telegram_channel_host = f"{settings.STATISTIC_TELEGRAM_CHANNEL_API_URL}:10013"
    news_agency_host = f"{settings.STATISTIC_NEWS_AGENCY_API_URL}:10014"
    host = twitter_host
    if platform:
        if platform == "instagram":
            host = instagram_host
        elif platform == 'twitter':
            host = twitter_host
        elif platform == 'telgram_group':
            host = telegram_group_host
        elif platform == 'telegram_channel':
            host = telegram_channel_host
        elif platform == 'news_agency':
            host = news_agency_host
    time_filtering = request.GET.get('time_filtering', '6m') 
    query = request.GET.get('query', '') 
    page = request.GET.get('page', '') 
    if query:
        news_list,pages = search_get_news(host,query,time_filtering,page)
        context = {
            "pages":pages,
            'news_list1':news_list[:int(len(news_list)/2)],
            'news_list2':news_list[int(len(news_list)/2):],
            }
        html_template = loader.get_template('home/notifications.html')
        return HttpResponse(html_template.render(context, request))
    
    context = get_statistic_data(host)
    sunburst_chart = get_sunburst_data(host)
    news_list, _ = get_news(host=host,time_filtering=time_filtering)
    context['rank_news_list1'] = news_list[:5]
    context['rank_news_list2'] = news_list[5:]
    context['sunburst_data'] = sunburst_chart
    
    # context['sunburst_parents'] =  sunburst_chart['parents']
    # context['sunburst_values'] =    sunburst_chart['values']  
    html_template = loader.get_template('home/dash_twitter.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def agency_news_dashboard(request):
    time_filtering = request.GET.get('time_filtering', '6m') 
    platform = request.GET.get('platform', '') 
    instagram_host = f"{settings.STATISTIC_INSTAGRAM_API_URL}:10011"
    twitter_host = f"{settings.STATISTIC_TWITTER_API_URL}:10010"
    telegram_group_host = f"{settings.STATISTIC_TELEGRAM_GROUP_API_URL}:10012"
    telegram_channel_host = f"{settings.STATISTIC_TELEGRAM_CHANNEL_API_URL}:10013"
    news_agency_host = f"{settings.STATISTIC_NEWS_AGENCY_API_URL}:10014"
    host = news_agency_host
    if platform:
        if platform == "instagram":
            host = instagram_host
        elif platform == 'twitter':
            host = twitter_host
        elif platform == 'telgram_group':
            host = telegram_group_host
        elif platform == 'telegram_channel':
            host = telegram_channel_host
        elif platform == 'news_agency':
            host = news_agency_host
    time_filtering = request.GET.get('time_filtering', '6m') 
    query = request.GET.get('query', '') 
    page = request.GET.get('page', '') 
    host = f"{settings.STATISTIC_NEWS_AGENCY_API_URL}:10014"
    if query:
        news_list,pages = search_get_news(host,query,time_filtering,page)
        context = {
            "pages":pages,
            'news_list1':news_list[:int(len(news_list)/2)],
            'news_list2':news_list[int(len(news_list)/2):],
            }
        html_template = loader.get_template('home/notifications.html')
        return HttpResponse(html_template.render(context, request))
    
    context = get_statistic_data(host)
    sunburst_chart = get_sunburst_data(host)
    news_list, _ = get_news(host=host,time_filtering=time_filtering)
    context['rank_news_list1'] = news_list[:5]
    context['rank_news_list2'] = news_list[5:]
    context['sunburst_data'] = sunburst_chart
    
    # context['sunburst_parents'] =  sunburst_chart['parents']
    # context['sunburst_values'] =    sunburst_chart['values']  
    html_template = loader.get_template('home/dash_news_agency.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def telegram_group_dashboard(request):
    time_filtering = request.GET.get('time_filtering', '6m') 
    platform = request.GET.get('platform', '') 
    instagram_host = f"{settings.STATISTIC_INSTAGRAM_API_URL}:10011"
    twitter_host = f"{settings.STATISTIC_TWITTER_API_URL}:10010"
    telegram_group_host = f"{settings.STATISTIC_TELEGRAM_GROUP_API_URL}:10012"
    telegram_channel_host = f"{settings.STATISTIC_TELEGRAM_CHANNEL_API_URL}:10013"
    news_agency_host = f"{settings.STATISTIC_NEWS_AGENCY_API_URL}:10014"
    host = telegram_group_host
    if platform:
        if platform == "instagram":
            host = instagram_host
        elif platform == 'twitter':
            host = twitter_host
        elif platform == 'telgram_group':
            host = telegram_group_host
        elif platform == 'telegram_channel':
            host = telegram_channel_host
        elif platform == 'news_agency':
            host = news_agency_host
    time_filtering = request.GET.get('time_filtering', '6m') 
    query = request.GET.get('query', '') 
    page = request.GET.get('page', '') 
    host = f"{settings.STATISTIC_TELEGRAM_GROUP_API_URL}:10012"
    if query:
        news_list,pages = search_get_news(host,query,time_filtering,page)
        context = {
            "pages":pages,
            'news_list1':news_list[:int(len(news_list)/2)],
            'news_list2':news_list[int(len(news_list)/2):],
            }
        html_template = loader.get_template('home/notifications.html')
        return HttpResponse(html_template.render(context, request))
    
    context = get_statistic_data(host)
    sunburst_chart = get_sunburst_data(host)
    news_list, _ = get_news(host=host,time_filtering=time_filtering)
    context['rank_news_list1'] = news_list[:5]
    context['rank_news_list2'] = news_list[5:]
    context['sunburst_data'] = sunburst_chart
    
    # context['sunburst_parents'] =  sunburst_chart['parents']
    # context['sunburst_values'] =    sunburst_chart['values']  
    html_template = loader.get_template('home/dash_telegram_group.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def telegram_chanel_dashboard(request):
    time_filtering = request.GET.get('time_filtering', '6m') 
    platform = request.GET.get('platform', '') 
    instagram_host = f"{settings.STATISTIC_INSTAGRAM_API_URL}:10011"
    twitter_host = f"{settings.STATISTIC_TWITTER_API_URL}:10010"
    telegram_group_host = f"{settings.STATISTIC_TELEGRAM_GROUP_API_URL}:10012"
    telegram_channel_host = f"{settings.STATISTIC_TELEGRAM_CHANNEL_API_URL}:10013"
    news_agency_host = f"{settings.STATISTIC_NEWS_AGENCY_API_URL}:10014"
    host = telegram_channel_host
    if platform:
        if platform == "instagram":
            host = instagram_host
        elif platform == 'twitter':
            host = twitter_host
        elif platform == 'telgram_group':
            host = telegram_group_host
        elif platform == 'telegram_channel':
            host = telegram_channel_host
        elif platform == 'news_agency':
            host = news_agency_host
    time_filtering = request.GET.get('time_filtering', '6m') 
    query = request.GET.get('query', '') 
    page = request.GET.get('page', '') 
    host = f"{settings.STATISTIC_TELEGRAM_CHANNEL_API_URL}:10013"
    if query:
        news_list,pages = search_get_news(host,query,time_filtering,page)
        context = {
            "pages":pages,
            'news_list1':news_list[:int(len(news_list)/2)],
            'news_list2':news_list[int(len(news_list)/2):],
            }
        html_template = loader.get_template('home/notifications.html')
        return HttpResponse(html_template.render(context, request))
    
    context = get_statistic_data(host)
    sunburst_chart = get_sunburst_data(host)
    news_list, _ = get_news(host=host,time_filtering=time_filtering)
    context['rank_news_list1'] = news_list[:5]
    context['rank_news_list2'] = news_list[5:]
    context['sunburst_data'] = sunburst_chart
    
    # context['sunburst_parents'] =  sunburst_chart['parents']
    # context['sunburst_values'] =    sunburst_chart['values']  
    html_template = loader.get_template('home/dash_telegram_channel.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def labeling(request):
    info_service_label = request.GET.get('info_service_label', '') 
    record_id = request.GET.get('record_id', '') 
    record_platform = request.GET.get('platform', '') 
    if info_service_label and record_id and record_platform:
        update_info_service_label(record_platform,record_id,info_service_label) 
    platform_list = ["instagram","twitter","telegram_group","telegram_channel","news_agency"]
    platform = random.choice(platform_list)
    record = get_for_labeling(platform=platform)
    format_string = "%Y-%m-%dT%H:%M:%S.%f"
    # Define Farsi day and month names
    farsi_day_names = ["شنبه", "یک‌شنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه"]
    farsi_month_names = [
        "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
        "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
    ]
    created_at = datetime.strptime(record['created_at'], format_string)
    jalali_datetime = jdatetime.fromgregorian(datetime=created_at)
    # Format the Jalali datetime in Farsi
    formatted_jalali_datetime = farsi_day_names[jalali_datetime.weekday()] + "، " + \
                                str(jalali_datetime.day) + " " + \
                                farsi_month_names[jalali_datetime.month - 1] + " " + \
                                str(jalali_datetime.year) + " - " + \
                                jalali_datetime.strftime("%H:%M")
    # context['jcreated_at'] = jalali_datetime.strftime("%A, %d %B %Y - %H:%M")
    context = {}
    context['jcreated_at'] = formatted_jalali_datetime
    context['platform'] = platform
    context['record'] = record
    context['record_id'] = record['_id']

    html_template = loader.get_template('home/labeling.html')
    return HttpResponse(html_template.render(context, request))


