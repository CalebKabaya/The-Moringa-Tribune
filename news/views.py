from cgitb import html
from email.mime import image
from django.shortcuts import render,redirect
from django.http  import HttpResponse,Http404
import datetime as dt

# Create your views here.
def welcome(request):
    return render(request,'welcome.html')

def news_of_day(request):
    date = dt.date.today()
    #function to convert date object to find the exact day
    return render(request, 'all-news/today-news.html', {"date": date,})

   


    return day
def past_days_news(request,past_date):
    try:
        # Converts data from the string Url
        date = dt.datetime.strptime(past_date,'%Y-%m-%d').date()
      

    except ValueError:
        # Raise 404 error when ValueError is thrown
        raise Http404()
    if date ==dt.date.today():
        return redirect(news_of_day)
    
      
    return redirect('request','all-news/past-news.html',{"date": date})  



