# Create your views here.
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="auth_app/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), {"next_page": settings.LOGOUT_REDIRECT_URL},  name="logout"),
    path('register/', views.register, name="register"),
]
