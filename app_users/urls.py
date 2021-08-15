from django.urls import path
from . import views


# app_name = 'app_users'
urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('about-school/', views.about_school_view, name='about_school'),
    path('about-us/', views.about_us_view, name='about_us'),
    path('news/', views.news_view, name="news")
]
