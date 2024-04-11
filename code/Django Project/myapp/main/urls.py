from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('user/', views.user_dashboard, name='user_dashboard'),
    path('user/about/', views.about_us, name='about_us'),
    path('user/service/', views.user_service, name='user_service'),
    path('user/contact/', views.contact_us, name='contact_us'),
    path('ageprogression/', views.age_progression, name='age_progression'),
    path('ageprogressioncheck/', views.progress_age, name='progress_age'),
]
