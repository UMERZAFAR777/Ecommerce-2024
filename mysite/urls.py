
from django.contrib import admin
from django.urls import path,include
from mysite import views
from django.conf import settings
from django.conf.urls.static import static


from django.urls import path, include



urlpatterns = [

    path('admin/',include('customadmin.urls')), 

    path('dj-admin/', admin.site.urls),
    path('',views.home,name='home'),

    path('product_detail/<slug:slug>',views.product_detail,name='product_detail'),

    path('error404',views.error404,name='error404'),

    path('account/my_account/',views.my_account,name='my_account'),

    path('login',views.login_user,name='handlelogin'),    
    path('logout',views.logout_user,name='handlelogout'),    
    path('register',views.register,name='handleregister'),    



    path('accounts/', include('django.contrib.auth.urls')),



    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('shop',views.shop,name='shop'),


    path('product/filter-data',views.filter_data,name="filter-data"),



    # path('cart',views.cart,name='cart'),



    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),


    path('checkout',views.checkout,name='checkout'),
    path('order_success',views.order_success,name='order_success'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
