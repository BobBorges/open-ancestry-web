from django.contrib.auth import views as auth_views
from django.urls import path
from . import views as authentication_views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='authentication/logout.html'), name='logout'),
    path('me-in-the-database/', authentication_views.I_am_Person, name='user-in-database'),
    path('register/', authentication_views.register_view, name='register')
]