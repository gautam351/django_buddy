from django.urls import path
from .views import testView,userRegister,VerfiyOTP,resendOTP,logout
urlpatterns = [
    path("test",testView.as_view(),name="test"),
    path("register",userRegister.as_view(),name="register"),
    path("verifyOTP",VerfiyOTP.as_view(),name="verifyOTP"),
    path("resendOTP",resendOTP.as_view(),name="resendOTP"),
    path("logout",logout.as_view(),name="logout"),
    
    
    
   
    
]
