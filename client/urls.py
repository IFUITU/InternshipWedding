from django.urls import path
from .views import signup, SignInOutView, ChangePswrdView

app_name = 'client'
urlpatterns = [
    path("signup", signup, name="signup"),
    path("log", SignInOutView.as_view(), name="log"),
    path("change-password/", ChangePswrdView.as_view(), name="change-pswrd"),
    
]