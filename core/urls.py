from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.user_login),
    path('logout/', views.user_logout),
    path('knowledge/', views.knowledge_list),
    path('knowledge/<int:article_id>/', views.article_detail),

]
