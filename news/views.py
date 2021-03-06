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
from .forms import NewsArticleForm,NEWSLETTERFORM
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import  MoringaMerch
from .serializer import MerchSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly




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
    form = NEWSLETTERFORM()
    return render(request, 'all-news/todays-news.html', {"date": date, "news": news, "letterForm": form})
def newsletter(request):
    name = request.POST.get('your_name')
    email = request.POST.get('email')
    recipient =NewsLetterRecipient(name=name, email=email)
    recipient.save()
    send_welcome_email(name, email)
    data = {'success': 'You have been successfully added to mailing list'}
    return JsonResponse(data)

# def news_today(request):
#     date = dt.date.today()
#     news = Article.todays_news()
#     form=NEWSLETTERFORM()
#     if request.method == 'POST':
#         form =NEWSLETTERFORM(request.POST)
#         if form.is_valid():
#             name=form.cleaned_data['your_name']
#             email=form.cleaned_data['email']
#             recipient=NewsLetterRecipient(name=name,email=email)
#             recipient.save()
#             send_welcome_email(name,email)
#             HttpResponseRedirect('news_today')
#     else:
#         form = NEWSLETTERFORM() 
#     return render(request, 'all-news/todays-news.html', {"date": date,"news":news,"letterForm":form})


   
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
def article(request, article_id):
    try:
        article = Article.objects.get(id = article_id)
    except Article.DoesNotExist:
        raise Http404()
    return render(request,"all-news/article.html", {"article":article})

# @login_required(login_url='/accounts/login')
# def new_article(request):
#     current_user=request.user
#     if request.method=='POST':
#         form=NewsArticleForm(request.POST,request.FILES)
#         if form.is_valid():
#             article=form.save(commit=False)
#             article.editor=current_user
#             article.save()
#         return redirect('NewsToday')    
#     else:
#         form=NewsArticleForm()
#     return render(request, 'new_article.html', {"form": form})
@login_required(login_url='/accounts/login/')
def new_article(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewsArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.editor = current_user
            article.save()
        return redirect('NewsToday')

    else:
        form = NewsArticleForm()
    return render(request, 'new_article.html', {"form": form}) 

class MerchList(APIView):
   def post(self, request, format=None):
        serializers = MerchSerializer(data=request.data)
        permission_classes = (IsAdminOrReadOnly,)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class MerchDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_merch(self, pk):
        try:
            return MoringaMerch.objects.get(pk=pk)
        except MoringaMerch.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        merch = self.get_merch(pk)
        serializers = MerchSerializer(merch)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        merch = self.get_merch(pk)
        serializers = MerchSerializer(merch, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk,format=None):
        merch=self.get_merch(pk)
        merch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


