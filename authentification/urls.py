from django.urls import path
from .views import (Account, SignUp)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path("signup", SignUp.as_view(), name="signup"),
    path("account", Account.as_view(), name="account"),
    path('token/get', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='refresh_token'),
    path('token/verify', TokenVerifyView.as_view(), name='verify_token'),
]
