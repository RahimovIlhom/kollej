from django.urls import path
from . import views
from .views import NewDetailView

# app_name = 'app_users'
urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('about-school/', views.about_school_view, name='about_school'),
    path('about-us/', views.about_us_view, name='about_us'),
    path('news/', views.news_view, name="news"),
    path('new/<int:pk>/', NewDetailView.as_view(), name='new_detail'),
    path('changepassword/', views.change_password, name='change_password'),
    path('editprofile/', views.edit_profile, name='edit_profile'),
    path('profile/', views.profile, name='profile'),
    path('comments/', views.CommentsListView.as_view(), name='comments'),
]
