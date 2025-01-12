from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('signup/', views.signup_view, name='signup'),
    path('about/',views.about,name='about'),
    path('refar/',views.refar,name='refar'),
    path('terms/',views.terms,name='terms'),
    path('contact/',views.contact,name='contact'),
    path('privacy/',views.privacy,name='privacy'),
    path('logout/', views.logout_view, name='logout'),
    path('payment/', views.payment_screen,name='payment'),
    path('product-scheme-manage/', views.product_scheme_manage, name='product_scheme_manage'),
    path('services/',views.services_view,name='services'),
]
