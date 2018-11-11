from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.signup_login, name='signup_login'),
    path('upload/', views.upload, name='upload'),
    path('upload/download/', views.download, name='download'),
    url(r'^download/', views.download, name='download'),
]