from django.urls import path
from useraccount.views import UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,ForgotPasswordView,ResetPasswordView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('forgotpassword/', ForgotPasswordView.as_view(), name='forgotpassword'),
    path('resetpassword/<user_id>/<token>/', ResetPasswordView.as_view(), name='resetpassword'),

]
