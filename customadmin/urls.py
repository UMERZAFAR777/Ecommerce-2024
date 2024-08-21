from django.contrib import admin
from django.urls import path,include
from customadmin.views import *
from . import views
urlpatterns = [

    path('',views.admin_login,name='admin_login'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout/',views.logout_admin,name='logout_admin')

]

