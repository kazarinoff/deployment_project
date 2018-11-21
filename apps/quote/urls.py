from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('regval/',views.regval, name='regval'),
    path('loginval/',views.loginval, name='loginval'),
    path('quotes/',views.quotes, name='quotes'),
    path('',views.index, name='index'),
    path('postquote/',views.postquote, name='postquote'),
    path('logout/',views.logout, name='logout'),
    path('myaccount/',views.edituser,name='edituser'),
    path('update/',views.updateuser,name='updateuser'),
    path('like/',views.like,name='like'),
    path('user/<userid>/',views.userview,name='userview'),
    path('delete/',views.deletequote, name='deletequote')

]