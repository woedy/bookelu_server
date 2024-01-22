from django.urls import path

from accounts.api.views import register_user

app_name = 'accounts'

urlpatterns = [
    path('register-user/', register_user, name="register_user"),
    # path('verify-user-email/', verify_user_email, name="verify_user_email"),
    # path('login-user/', UserLogin.as_view(), name="login_user"),




]
