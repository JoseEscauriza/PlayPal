from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('login/success/', views.logged_view, name='logged_view'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile_own, name='own_profile'),
    path('edit-profile/', views.edit_user_profile_own, name='edit_own_profile'),
    path('register/', views.UserRegister.as_view(), name='user_registration'),
    path('user-profile/<uuid:user_uuid>/', views.other_user_profile, name='other_user_profile'),
]
