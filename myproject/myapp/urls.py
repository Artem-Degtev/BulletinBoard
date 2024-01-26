"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path
from django.urls import path
from . import views
from .views import login_view
from .views import home_view

urlpatterns = [
    path('register/', views.register, name='register'),
    path('create_announcement/', views.create_announcement, name='create_announcement'),
    path('announcement_created/<int:announcement_id>/', views.announcement_created, name='announcement_created'),
    path('edit_announcement/<int:announcement_id>/', views.edit_announcement, name='edit_announcement'),
    path('user_responses/<int:announcement_id>/', views.user_responses, name='user_responses'),
    path('response_detail/<int:response_id>/', views.response_detail, name='response_detail'),
    path('accept_response/<int:response_id>/', views.accept_response, name='accept_response'),
    path('news_subscription/', views.news_subscription, name='news_subscription'),
    path('register/', views.register, name='register'),
    path('login/', login_view, name='login'),
    path('/', home_view, name='home'),
    re_path(r'^verify/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
]
