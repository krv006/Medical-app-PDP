from django.urls import path

from users.views import LoginAPIView, RegisterAPIView, VerifyCodeApiView, ResetVerificationCodeAPIView, \
    ResetPasswordAPIView, ConfirmNewPasswordAPIView

urlpatterns = [
    path('login', LoginAPIView.as_view(), name='login'),
    path('register', RegisterAPIView.as_view(), name='register'),
    path('verify-code', VerifyCodeApiView.as_view(), name='verify_code'),
    path('reset-code', ResetVerificationCodeAPIView.as_view(), name='reset_code'),
    path('reset-password', ResetPasswordAPIView.as_view(), name='reset_password'),
    path('confirm-password', ConfirmNewPasswordAPIView.as_view(), name='confirm_password'),
]
