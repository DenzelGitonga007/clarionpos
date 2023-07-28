from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'), # home view/ landing page
    path('register/', views.register_user, name='register'), #registration form
    path('login/', views.login_user, name='login'), #login page
    path('logout/', views.logout_user, name='logout'), #logout page
]