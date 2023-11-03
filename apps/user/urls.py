from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('login/success/', views.logged_view, name='logged_view'),

]
