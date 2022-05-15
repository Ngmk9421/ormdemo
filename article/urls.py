from django.urls import path

from article import views

app_name = 'article'

urlpatterns = [
    path('publish', views.publish, name='publish'),
    path('article_type/<int:type_id>', views.article_type, name='article_type'),
    path('leave', views.leave, name='leave'),
    path('article_info/<int:id>', views.article_info, name='article_info'),
    path('like_article', views.like_article, name='like_article'),
    path('del_article', views.del_article, name='del_article')
]
