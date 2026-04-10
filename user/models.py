import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from uuid import uuid4

def user_avatar_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower() or ".jpg"
    return f"avatars/{uuid4().hex}{ext}"

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un email')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        
       
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
            
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("role", UserAccount.Roles.ADMIN)
        extra_fields.setdefault("auth_provider", UserAccount.AuthProviders.LOCAL)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class UserAccount(AbstractBaseUser, PermissionsMixin):

    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        MANAGER = "MGR", "Manager"
        EMPLOYEE = "EMP", "Empleado"
        CUSTOMER = "CUS", "Cliente"


    class AuthProviders(models.TextChoices):
        LOCAL = "LOCAL", "Email y Contraseña"
        GOOGLE = "GOOGLE", "Google OAuth"

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    
    avatar = models.ImageField(
        upload_to=user_avatar_upload_path,
        blank=True,
        null=True,
    )

    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.CUSTOMER,
        db_index=True,
    )

    auth_provider = models.CharField(
        max_length=10,
        choices=AuthProviders.choices,
        default=AuthProviders.LOCAL,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    total_visitas = models.PositiveIntegerField(default=0)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return "https://ui-avatars.com/api/?name=" + self.get_short_name()

    def _sync_flags_with_role(self):
        if self.role in (self.Roles.ADMIN, self.Roles.MANAGER):
            self.is_staff = True
        else:
            self.is_staff = False

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_staff = True
        else:
            self._sync_flags_with_role()
        super().save(*args, **kwargs)

    def get_full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip() or self.email

    def get_short_name(self):
        return self.first_name or self.email.split("@")[0]

    def __str__(self):
        return self.email