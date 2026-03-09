from django.urls import path , include
from .views import SendOtpView , VerifyOtpView , LogoutView

urlpatterns = [
    path('send-otp/',SendOtpView.as_view(),name='send_otp'),
    path('verify-otp/',VerifyOtpView.as_view(),name='verify_otp'),
    path('logout/',LogoutView.as_view(),name='logout')
        
]
