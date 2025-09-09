from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from .models import (
    CustomUserModel, ResetPasswordControl, PasswordRecoveryEmail,
    EmailConfirmationControl, PreRegister, LoggedDevice
)
from .serializers import (
    CustomUserSerializer, CustomUserListSerializer, ResetPasswordControlSerializer,
    PasswordRecoveryEmailSerializer, EmailConfirmationControlSerializer,
    PreRegisterSerializer, LoggedDeviceSerializer
)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['username'] = user.username
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUserModel.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return CustomUserListSerializer
        return CustomUserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], url_path='me')
    def current_user(self, request):
        """Get current user details"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'], url_path='me/update')
    def update_current_user(self, request):
        """Update current user"""
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordControlViewSet(viewsets.ModelViewSet):
    queryset = ResetPasswordControl.objects.all()
    serializer_class = ResetPasswordControlSerializer
    permission_classes = [permissions.IsAuthenticated]


class PasswordRecoveryEmailViewSet(viewsets.ModelViewSet):
    queryset = PasswordRecoveryEmail.objects.all()
    serializer_class = PasswordRecoveryEmailSerializer
    permission_classes = [permissions.IsAuthenticated]


class EmailConfirmationControlViewSet(viewsets.ModelViewSet):
    queryset = EmailConfirmationControl.objects.all()
    serializer_class = EmailConfirmationControlSerializer
    permission_classes = [permissions.IsAuthenticated]


class PreRegisterViewSet(viewsets.ModelViewSet):
    queryset = PreRegister.objects.all()
    serializer_class = PreRegisterSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class LoggedDeviceViewSet(viewsets.ModelViewSet):
    queryset = LoggedDevice.objects.all()
    serializer_class = LoggedDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter devices by current user"""
        return LoggedDevice.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Auto-assign current user when creating device"""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def update_login(self, request, pk=None):
        """Update last login time for device"""
        device = self.get_object()
        device.update_last_login()
        return Response({'message': 'Login time updated'}, status=status.HTTP_200_OK)
