from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.user_login),
    path('logout/', views.user_logout),
    path('knowledge/', views.knowledge_list),
    path('knowledge/<int:article_id>/', views.article_detail),
    path('notifications/mark-read/<int:notif_id>/', views.mark_notification_read),
    path('ivr/', views.ivr),
    path('ivr/save-recording/', views.ivr_save_recording),
    path('chatbot/', views.chatbot),
    path('crop-disease/', views.crop_disease),

]
