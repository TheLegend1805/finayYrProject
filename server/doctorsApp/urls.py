from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from .views import (register_doctor, verify_doctor_otp, doctor_login, verify_doctor_login_otp)

urlpatterns = [
    path('register/', register_doctor, name='doctor-register'),
    path('verify-otp/', verify_doctor_otp, name='doctor-verify-otp'),
    path('login/', doctor_login, name='doctor-login'),
    path('verify-login-otp/', verify_doctor_login_otp, name='doctor-verify-login-otp'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]