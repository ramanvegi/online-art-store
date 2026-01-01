from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add/<int:pid>/', views.add_to_cart),
    path('register/', views.register_user),
    path('login/', views.login_user),
    path('logout/', views.logout_user),
    path('remove/<int:index>/', views.remove_from_cart),
    path('buy/', views.buy_now),


]
