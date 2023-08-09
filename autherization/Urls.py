from django.urls import path
from .views import testView,userRegister,VerfiyOTP,resendOTP,logout,login,forgetPassword
urlpatterns = [
    path("test",testView.as_view(),name="test"),
    path("register",userRegister.as_view(),name="register"),
    path("verifyOTP",VerfiyOTP.as_view(),name="verifyOTP"),
    path("resendOTP",resendOTP.as_view(),name="resendOTP"),
    path("logout",logout.as_view(),name="logout"),
    path("login",login.as_view(),name="login"),
    path("forgetPassword",forgetPassword.as_view(),name="forget"),
    
    
    
    
    
   
    
]
