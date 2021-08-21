from django.contrib import auth, messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import request
from django.urls import path
from django.views.generic.base import TemplateView, View
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . forms import UserLogin , UserPasswordChange
from django.urls import path, re_path, include, reverse_lazy
from django.contrib import messages

urlpatterns = [
   
    path('',views.ProductView.as_view(),name='home'),

    path('product-detail/<int:pk>',views.ProductDetailView.as_view(), name='product-detail'),
    
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    
    path('showcart/', views.show_cart, name='showcart'),

    path('plusminuscart/',views.plus_minus),



    path('buy/', views.buy_now, name='buy-now'),

    path('profile/',views.ProfileView.as_view(),name='profile'),

    
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    
    path('education/', views.education, name='education'),
    path('education/<slug:data>', views.education, name='educationdata'),

    path('comic/', views.comic, name='comic'),
    path('comic/<slug:data>', views.comic, name='comicdata'),

    
    path('magazine/', views.magazine, name='magazine'),
    path('magazine/<slug:data>', views.magazine, name='magazinedata'),

    
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name ='app/login.html',
    authentication_form= UserLogin ),name='Login'),
    path('logout/',auth_views.LogoutView.as_view(next_page = 'Login'),name='logout'),
  
    path('passwordchange/' ,auth_views.PasswordChangeView.as_view(template_name = 'app/passwordchange.html',
    form_class = UserPasswordChange ,success_url = '/profile/') , 
    name='changepassword', ),

    path('registration/',views.CustomerRegistrationView.as_view(), name = 'customerregistration'),

] +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
