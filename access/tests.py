from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (
    CustomUserModel, ResetPasswordControl, PasswordRecoveryEmail,
    EmailConfirmationControl, PreRegister, LoggedDevice
)
from .serializers import (
    CustomUserSerializer, ResetPasswordControlSerializer,
    PasswordRecoveryEmailSerializer, EmailConfirmationControlSerializer,
    PreRegisterSerializer, LoggedDeviceSerializer
)


class CustomUserModelTests(TestCase):
    """Test the CustomUserModel"""

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }

    def test_create_user(self):
        """Test creating a regular user"""
        user = CustomUserModel.objects.create_user(**self.user_data)
        
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.active)

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = CustomUserModel.objects.create_superuser(**self.user_data)
        
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_user_string_representation(self):
        """Test the user string representation"""
        user = CustomUserModel.objects.create_user(**self.user_data)
        self.assertEqual(str(user), user.email)

    def test_whoami_property(self):
        """Test the whoami property"""
        user = CustomUserModel.objects.create_user(**self.user_data)
        whoami = user.whoami
        
        self.assertEqual(whoami['email'], user.email)
        self.assertEqual(whoami['username'], user.username)
        self.assertEqual(whoami['credits'], user.dalle_credits)
        self.assertIsNone(whoami['avatar'])


class ResetPasswordControlTests(TestCase):
    """Test the ResetPasswordControl model"""

    def test_create_reset_password_control(self):
        """Test creating a reset password control"""
        reset_control = ResetPasswordControl.objects.create(
            email='test@example.com'
        )
        
        self.assertEqual(reset_control.email, 'test@example.com')
        self.assertIsNotNone(reset_control.request_id)
        self.assertIsNotNone(reset_control.date)

    def test_string_representation(self):
        """Test the string representation"""
        reset_control = ResetPasswordControl.objects.create(
            email='test@example.com'
        )
        expected_str = "{} - {} - {} - {}".format(
            reset_control.pk,
            reset_control.request_id,
            reset_control.email,
            reset_control.date,
        )
        self.assertEqual(str(reset_control), expected_str)


class LoggedDeviceTests(TestCase):
    """Test the LoggedDevice model"""

    def setUp(self):
        self.user = CustomUserModel.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_create_logged_device(self):
        """Test creating a logged device"""
        device = LoggedDevice.objects.create(
            user=self.user,
            device_type='desktop',
            device_name='Chrome Browser',
            place='São Paulo'
        )
        
        self.assertEqual(device.user, self.user)
        self.assertEqual(device.device_type, 'desktop')
        self.assertEqual(device.device_name, 'Chrome Browser')
        self.assertEqual(device.place, 'São Paulo')

    def test_update_last_login(self):
        """Test updating last login"""
        device = LoggedDevice.objects.create(
            user=self.user,
            device_type='desktop',
            device_name='Chrome Browser'
        )
        original_login = device.last_login_at
        device.update_last_login()
        
        self.assertNotEqual(device.last_login_at, original_login)

    def test_string_representation(self):
        """Test the string representation"""
        device = LoggedDevice.objects.create(
            user=self.user,
            device_type='desktop',
            device_name='Chrome Browser'
        )
        expected_str = f"{device.device_name} ({device.device_type})"
        self.assertEqual(str(device), expected_str)


class PreRegisterTests(TestCase):
    """Test the PreRegister model"""

    def test_create_pre_register(self):
        """Test creating a pre-register"""
        pre_register = PreRegister.objects.create(
            email='test@example.com'
        )
        
        self.assertEqual(pre_register.email, 'test@example.com')
        self.assertIsNotNone(pre_register.id)
        self.assertIsNotNone(pre_register.created)

    def test_string_representation(self):
        """Test the string representation"""
        pre_register = PreRegister.objects.create(
            email='test@example.com'
        )
        self.assertEqual(str(pre_register), 'test@example.com')


class APITests(APITestCase):
    """Test the API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }
        self.user = CustomUserModel.objects.create_user(
            username='apiuser',
            email='api@example.com',
            password='apipass123'
        )
        self.token = self.get_token()

    def get_token(self):
        """Get JWT token for authentication"""
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)

    def test_user_registration(self):
        """Test user registration endpoint"""
        url = reverse('customusermodel-list')
        response = self.client.post(url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUserModel.objects.count(), 2)  # Including setup user

    def test_user_login(self):
        """Test JWT login endpoint"""
        url = reverse('token_obtain_pair')
        login_data = {
            'email': 'api@example.com',
            'password': 'apipass123'
        }
        response = self.client.post(url, login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_current_user_endpoint(self):
        """Test getting current user details"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        url = reverse('customusermodel-current-user')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_pre_register_creation(self):
        """Test pre-register creation (no auth required)"""
        url = reverse('preregister-list')
        data = {'email': 'preregister@example.com'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PreRegister.objects.count(), 1)

    def test_logged_device_creation(self):
        """Test logged device creation"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        url = reverse('loggeddevice-list')
        data = {
            'device_type': 'desktop',
            'device_name': 'Test Browser',
            'place': 'Test City'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LoggedDevice.objects.count(), 1)
        
        device = LoggedDevice.objects.first()
        self.assertEqual(str(device.user.userId), str(self.user.userId))

    def test_reset_password_control_creation(self):
        """Test reset password control creation"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        url = reverse('resetpasswordcontrol-list')
        data = {'email': 'reset@example.com'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ResetPasswordControl.objects.count(), 1)

    def test_unauthorized_access(self):
        """Test that protected endpoints require authentication"""
        url = reverse('customusermodel-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_password_recovery_email_crud(self):
        """Test password recovery email CRUD operations"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # Create
        url = reverse('passwordrecoveryemail-list')
        data = {
            'name': 'Test Recovery',
            'body': 'Test email body',
            'subject': 'Test Subject',
            'email_adress': 'recovery@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Read
        recovery_id = response.data['id']
        detail_url = reverse('passwordrecoveryemail-detail', kwargs={'pk': recovery_id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Update
        updated_data = data.copy()
        updated_data['name'] = 'Updated Recovery'
        response = self.client.put(detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Recovery')
        
        # Delete
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_email_confirmation_control_crud(self):
        """Test email confirmation control CRUD operations"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # Create
        url = reverse('emailconfirmationcontrol-list')
        data = {'email': 'confirm@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Read list
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class SerializerTests(TestCase):
    """Test the serializers"""

    def setUp(self):
        self.user = CustomUserModel.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_custom_user_serializer_create(self):
        """Test creating user with serializer"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123'
        }
        serializer = CustomUserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()
        self.assertEqual(user.email, data['email'])
        self.assertTrue(user.check_password(data['password']))

    def test_custom_user_serializer_password_mismatch(self):
        """Test password mismatch validation"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'password_confirm': 'differentpass'
        }
        serializer = CustomUserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

    def test_logged_device_serializer_unique_constraint(self):
        """Test logged device unique constraint validation"""
        # Create first device
        LoggedDevice.objects.create(
            user=self.user,
            device_type='desktop',
            device_name='Chrome'
        )
        
        # Try to create duplicate
        data = {
            'device_type': 'desktop',
            'device_name': 'Chrome'
        }
        
        # Create mock request with user
        from unittest.mock import Mock
        request = Mock()
        request.user = self.user
        
        serializer = LoggedDeviceSerializer(data=data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
