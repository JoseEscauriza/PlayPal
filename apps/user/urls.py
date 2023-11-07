from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('login/success/', views.logged_view, name='logged_view'),
    path('logout/', views.user_logout, name='logout'),
]
