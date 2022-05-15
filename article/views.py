from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from article.models import Type, Article
from user.models import User


def publish(request):
    if request.method == 'POST':
        type_id = request.POST.get('type_id')
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        content = request.POST.get('content')
        username = request.session.get('username')
        user = User.objects.filter(username=username).first()
        user_id = user.id

        Article.objects.create(title=title, desc=desc, text=content, type_id=type_id, user_id=user_id)
        return redirect(reverse('article:publish'))
    else:
        username = request.session.get('username')
        user = User.objects.filter(username=username).first()
        types = Type.objects.all()
        return render(request, 'article/publish.html', {'types': types, 'user': user})


def article_type(request, type_id):
    username = request.session.get('username')
    user = User.objects.filter(username=username).first()
    articles = Article.objects.filter(is_delete=False, type_id=type_id).all()
    types = Type.objects.all()
    page_html = 'article/article_clown.html'
    if type_id == 2:
        page_html = 'article/article_life.html'
    elif type_id == 3:
        page_html = 'article/article_science.html'
    print(type_id)
    return render(request, page_html, {'articles': articles, 'types': types, 'user': user})


def leave(request):
    username = request.session.get('username')
    user = User.objects.filter(username=username).first()
    return render(request, 'article/leave.html', {'user': user})


def article_info(request, id):
    article = Article.objects.get(pk=id)
    article.visit_num += 1
    article.save()
    username = request.session.get('username')
    user = User.objects.filter(username=username).first()
    return render(request, 'article/article_info.html', {'article': article, 'user': user})


def like_article(request):
    article_id = request.POST.get('id')
    like = int(request.POST.get('like'))

    article = Article.objects.get(pk=article_id)

    if like:
        article.like_num += 1
    else:
        article.like_num -= 1
    article.save()
    return JsonResponse({'mes': 'ok', 'like_num': article.like_num})


def del_article(request):
    article_id = request.GET.get('id')
    article = Article.objects.get(pk=article_id)
    article.is_delete = True
    article.save()
    return HttpResponse('删除成功')
