from uuid import uuid4

import stripe

from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

from general.abstract_models import BaseModel
from general.storage_backends import PrivateMediaStorage


class CustomUserModelManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates a custom user with the given fields
        """

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password=password)

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


def default_notification_settings():
    """Retorna a estrutura padrão dos settings de notificação."""
    return {
        "email": {"updates": False, "tips": False, "payment": False},
        "push": {"updates": False, "tips": False, "payment": False},
    }


class CustomUserModel(AbstractUser, PermissionsMixin):
    userId = models.CharField(
        max_length=64, default=uuid4, primary_key=True, editable=False
    )
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    avatar = models.ImageField(storage=PrivateMediaStorage(), null=True, blank=True)
    stripeCustomerId = models.CharField(max_length=100, null=True, blank=True)
    dalle_credits = models.IntegerField(default=0, null=False, blank=False)
    subscription_credits = models.IntegerField(default=0, null=False, blank=False)
    domainShopperId = models.CharField(max_length=100, null=True, blank=True)
    is_deactivated = models.BooleanField(default=False)
    is_complimentary_plan = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created = models.DateTimeField("Data Criação", auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(
        "Data Atualização", auto_now=True, auto_now_add=False
    )

    objects = CustomUserModelManager()

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True,
        help_text="Número de telefone no formato E.164",
    )

    birth_date = models.DateField(blank=True, null=True)

    is_email_confirmed = models.BooleanField(
        default=False,
        verbose_name=("Email Confirmed"),
        help_text=("Indica se o e-mail do usuário foi confirmado."),
    )
    notification_settings = models.JSONField(
        default=default_notification_settings, blank=True, null=True
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Custom User"

    @property
    def whoami(self):
        return {
            "email": self.email,
            "username": self.username,
            "avatar": self.avatar.url if self.avatar else None,
            "credits": self.dalle_credits,
        }


class ResetPasswordControl(models.Model):
    request_id = models.CharField(
        max_length=64, default=uuid4, primary_key=True, editable=False
    )
    email = models.EmailField(max_length=200, unique=False, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {} - {} - {}".format(
            self.pk,
            self.request_id,
            self.email,
            self.date,
        )


class PasswordRecoveryEmail(models.Model):
    name = models.CharField("Name", max_length=100)
    body = models.TextField("Body")
    subject = models.CharField("Subject", max_length=200)
    email_address = models.EmailField("Address", max_length=200)

    def __str__(self):
        return self.name


class EmailConfirmationControl(models.Model):
    email = models.EmailField(verbose_name=("Email"))
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=("Date of Request"),
        help_text=("Data e hora em que a solicitação foi realizada."),
    )

    class Meta:
        verbose_name = "Email Confirmation Control"
        verbose_name_plural = "Email Confirmation Controls"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.email} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"


class PreRegister(BaseModel):
    email = models.EmailField(max_length=200, unique=True, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class LoggedDevice(BaseModel):
    DEVICE_TYPE_CHOICES = (
        ("desktop", "Desktop"),
        ("mobile", "Mobile"),
    )
    user = models.ForeignKey(
        CustomUserModel,
        related_name="logged_devices",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="Usuário associado a este dispositivo.",
    )

    device_type = models.CharField(
        max_length=10,
        choices=DEVICE_TYPE_CHOICES,
        blank=True,
        null=True,
        help_text="Tipo de dispositivo: 'desktop' ou 'mobile'.",
    )

    device_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Nome ou identificação do dispositivo (ex: browser).",
    )

    last_login_at = models.DateTimeField(
        default=timezone.now,
        blank=True,
        null=True,
        help_text="Data e hora do último login neste dispositivo.",
    )

    place = models.CharField(
        max_length=100,
        default="unknown",
        blank=True,
        null=True,
    )

    class Meta:
        unique_together = ("user", "device_type", "device_name")
        ordering = ["-last_login_at"]
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"

    def update_last_login(self):
        """Atualiza o campo last_login_at para o horário atual."""
        self.last_login_at = timezone.now()
        self.save(update_fields=["last_login_at"])

    def __str__(self):
        return f"{self.device_name} ({self.device_type})"
