from cgitb import html
import email
from email.mime import image
from django.shortcuts import render,redirect
from django.http  import HttpResponse,Http404,HttpResponseRedirect
import datetime as dt
from .models import Article, NewsLetterRecipient
from .forms import NEWSLETTERFORM
from .emails import send_welcome_email
from django.contrib.auth.decorators import login_required



# Create your views here.
def welcome(request):
    return render(request,'welcome.html')

# def news_of_day(request):
#     date = dt.date.today()
    #function to convert date object to find the exact day
    # return render(request, 'all-news/todays-news.html', {"date": date,})

def news_today(request):
    date = dt.date.today()
    news = Article.todays_news()
    if request.method == 'POST':
        form =NEWSLETTERFORM(request.POST)
        if form.is_valid():
            name=form.cleaned_data['your_name']
            email=form.cleaned_data['email']
            recipient=NewsLetterRecipient(name=name,email=email)
            recipient.save()
            send_welcome_email(name,email)
            HttpResponseRedirect('news_today')
    else:
        form = NEWSLETTERFORM() 
    return render(request, 'all-news/todays-news.html', {"date": date,"news":news,"letterForm":form})
   
def news_all(request):

    all_news= Article.objects.all()
    if request.method=='POST':
        form =NEWSLETTERFORM(request.POST)
        if form.is_valid:
            print('valid')
        else:
            form=NEWSLETTERFORM()    

    return render(request, 'all-news/all_news.html', {"all_news": all_news}) 

    return day
def past_days_news(request,past_date):
    try:
        # Converts data from the string Url
        date = dt.datetime.strptime(past_date,'%Y-%m-%d').date()
      

    except ValueError:
        # Raise 404 error when ValueError is thrown
        raise Http404()
    if date ==dt.date.today():
        return redirect(news_today)
    
    news = Article.days_news(date)
    return render(request,'all-news/past-news.html',{"date": date,"news":news}) 

def search_results(request):

    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'all-news/search.html',{"message":message,"articles": searched_articles})

    else:
        message = "You haven't searched for any term"
 
        return render(request, 'all-news/search.html',{"message":message})

@login_required(login_url='/accounts/login/')
def article(request,article_id):
    try:
        article = Article.objects.get(id = article_id)
    except Article.DoesNotExist:
        raise Http404()
    return render(request,"all-news/article.html", {"article":article})







