from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import (
    CustomUserModel,
    EmailConfirmationControl,
    LoggedDevice,
    PasswordRecoveryEmail,
    PreRegister,
    ResetPasswordControl,
)
from .serializers import (
    CustomUserListSerializer,
    CustomUserSerializer,
    EmailConfirmationControlSerializer,
    LoggedDeviceSerializer,
    PasswordRecoveryEmailSerializer,
    PreRegisterSerializer,
    ResetPasswordControlSerializer,
)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer that adds additional user information to the token payload.
    
    Extends the default TokenObtainPairSerializer to include user email and username
    in the JWT token claims for easier client-side user identification.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token["email"] = user.email
        token["username"] = user.username
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Enhanced JWT token obtain view with custom user information.
    
    Provides JWT authentication tokens that include additional user data
    in the token payload for improved client-side functionality.
    """
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all users",
        description="Retrieve a paginated list of all users in the system. Requires authentication.",
        tags=["Users"]
    ),
    create=extend_schema(
        summary="Create new user",
        description="Register a new user account. This endpoint allows anonymous access for user registration.",
        tags=["Users"]
    ),
    retrieve=extend_schema(
        summary="Get user details",
        description="Retrieve detailed information about a specific user by their ID.",
        tags=["Users"]
    ),
    update=extend_schema(
        summary="Update user",
        description="Update user information. Only authenticated users can update their own profile.",
        tags=["Users"]
    ),
    partial_update=extend_schema(
        summary="Partially update user",
        description="Partially update user information with PATCH method.",
        tags=["Users"]
    ),
    destroy=extend_schema(
        summary="Delete user",
        description="Delete a user account. Requires appropriate permissions.",
        tags=["Users"]
    ),
)
class CustomUserViewSet(viewsets.ModelViewSet):
    """
    User management endpoints for registration, authentication, and profile management.
    
    This ViewSet provides comprehensive user management functionality including:
    - User registration (anonymous access)
    - User profile retrieval and updates (authenticated access)
    - Current user information endpoint
    - User list for administrative purposes
    
    The user model includes support for:
    - Email-based authentication
    - Avatar/profile picture upload
    - Credit system integration
    - Stripe payment integration
    - Email confirmation workflow
    - Device tracking and management
    """
    queryset = CustomUserModel.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return CustomUserListSerializer
        return CustomUserSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @extend_schema(
        summary="Get current user profile",
        description="Retrieve the profile information of the currently authenticated user.",
        tags=["Users"]
    )
    @action(detail=False, methods=["get"], url_path="me")
    def current_user(self, request):
        """Get current user details"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @extend_schema(
        summary="Update current user profile",
        description="Update the profile information of the currently authenticated user.",
        tags=["Users"]
    )
    @action(detail=False, methods=["put", "patch"], url_path="me/update")
    def update_current_user(self, request):
        """Update current user"""
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        summary="List password reset requests",
        description="Retrieve all password reset control records.",
        tags=["Password Management"]
    ),
    create=extend_schema(
        summary="Create password reset request",
        description="Create a new password reset request for a user.",
        tags=["Password Management"]
    ),
    retrieve=extend_schema(
        summary="Get password reset request",
        description="Retrieve details of a specific password reset request.",
        tags=["Password Management"]
    ),
)
class ResetPasswordControlViewSet(viewsets.ModelViewSet):
    """
    Password reset control management.
    
    Handles password reset requests including creation, tracking, and validation
    of password reset tokens and emails.
    """
    queryset = ResetPasswordControl.objects.all()
    serializer_class = ResetPasswordControlSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(
    list=extend_schema(
        summary="List password recovery emails",
        description="Retrieve all password recovery email templates.",
        tags=["Password Management"]
    ),
    create=extend_schema(
        summary="Create password recovery email",
        description="Create a new password recovery email template.",
        tags=["Password Management"]
    ),
)
class PasswordRecoveryEmailViewSet(viewsets.ModelViewSet):
    """
    Password recovery email template management.
    
    Manages email templates used for password recovery communications,
    including subject lines, body content, and recipient information.
    """
    queryset = PasswordRecoveryEmail.objects.all()
    serializer_class = PasswordRecoveryEmailSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(
    list=extend_schema(
        summary="List email confirmations",
        description="Retrieve all email confirmation control records.",
        tags=["Email Management"]
    ),
    create=extend_schema(
        summary="Create email confirmation",
        description="Create a new email confirmation request.",
        tags=["Email Management"]
    ),
)
class EmailConfirmationControlViewSet(viewsets.ModelViewSet):
    """
    Email confirmation control management.
    
    Handles email confirmation requests and tracking for user email verification.
    """
    queryset = EmailConfirmationControl.objects.all()
    serializer_class = EmailConfirmationControlSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(
    list=extend_schema(
        summary="List pre-registrations",
        description="Retrieve all pre-registration records.",
        tags=["Registration"]
    ),
    create=extend_schema(
        summary="Create pre-registration",
        description="Create a new pre-registration entry. Allows anonymous access for email collection.",
        tags=["Registration"]
    ),
)
class PreRegisterViewSet(viewsets.ModelViewSet):
    """
    Pre-registration management for email collection.
    
    Allows collection of email addresses from interested users before
    full registration is available. Useful for waitlists and early access.
    """
    queryset = PreRegister.objects.all()
    serializer_class = PreRegisterSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


@extend_schema_view(
    list=extend_schema(
        summary="List user devices",
        description="Retrieve all logged devices for the current user.",
        tags=["Device Management"]
    ),
    create=extend_schema(
        summary="Register new device",
        description="Register a new device for the current user.",
        tags=["Device Management"]
    ),
    retrieve=extend_schema(
        summary="Get device details",
        description="Retrieve details of a specific device.",
        tags=["Device Management"]
    ),
)
class LoggedDeviceViewSet(viewsets.ModelViewSet):
    """
    Device management for user login tracking.
    
    Tracks and manages devices that users have logged in from,
    including device type (mobile/desktop), device name, and
    last login timestamps.
    """
    queryset = LoggedDevice.objects.all()
    serializer_class = LoggedDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter devices by current user"""
        return LoggedDevice.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Auto-assign current user when creating device"""
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Update device login time",
        description="Update the last login timestamp for a specific device.",
        tags=["Device Management"]
    )
    @action(detail=True, methods=["post"])
    def update_login(self, request, pk=None):
        """Update last login time for device"""
        device = self.get_object()
        device.update_last_login()
        return Response({"message": "Login time updated"}, status=status.HTTP_200_OK)
