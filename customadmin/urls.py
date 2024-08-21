from django.contrib import admin
from django.urls import path,include
from customadmin.views import *
from . import views
urlpatterns = [

    path('',views.admin_login,name='admin_login'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout/',views.logout_admin,name='logout_admin'),
    path('product/',views.product_admin,name='product_admin'),
    path('user/',views.user_admin,name='user_admin'),
    path('group/',views.group_admin,name='group_admin'),

]

