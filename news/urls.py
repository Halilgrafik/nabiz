from django.urls import path

from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('read/<int:article_id>/', views.read_article, name='read_article'),
    path('nabiz/', views.dashboard, name='dashboard'),
]
