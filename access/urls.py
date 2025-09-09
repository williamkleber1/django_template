from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from django.urls import include, path

from .views import (
    CustomTokenObtainPairView,
    CustomUserViewSet,
    EmailConfirmationControlViewSet,
    LoggedDeviceViewSet,
    PasswordRecoveryEmailViewSet,
    PreRegisterViewSet,
    ResetPasswordControlViewSet,
)

router = DefaultRouter()
router.register(r"users", CustomUserViewSet)
router.register(r"reset-password-control", ResetPasswordControlViewSet)
router.register(r"password-recovery-email", PasswordRecoveryEmailViewSet)
router.register(r"email-confirmation-control", EmailConfirmationControlViewSet)
router.register(r"pre-register", PreRegisterViewSet)
router.register(r"logged-devices", LoggedDeviceViewSet)

urlpatterns = [
    path("api/access/", include(router.urls)),
    path(
        "api/access/auth/login/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("api/access/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
