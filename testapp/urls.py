from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name="home"),
    path('register/',views.register,name="register"),
    path('registered/',views.doregister,name='doregister'),
    path('login/',views.login,name="login"),
    path('loggedin/',views.dologin,name='dologin'),
    path('upcoming/',views.upcoming,name='upcoming'),
    path('brand/<bname>/',views.brand,name='brand'),
    path('pay/', views.initiate_payment, name='pay'),
    path('callback/', views.callback, name='callback'),

]
