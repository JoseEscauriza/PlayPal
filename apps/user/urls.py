from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('login/success/', views.logged_view, name='logged_view'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile_own, name='own_profile'),
    path('user-profile/<uuid:user_uuid>/', views.other_user_profile, name='other_user_profile'),
    path('swiping/', views.user_swiping, name='swiping'),
    path('record_action/', views.record_action, name='record_action'),
]
