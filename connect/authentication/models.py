import requests
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import JSONField
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from connect.storages import AvatarUserMediaStorage


class UserManager(BaseUserManager):
    def _create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        if not username:
            raise ValueError("The given nick must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email"), unique=True, help_text=_("User's email."))

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    photo = models.ImageField(
        _("photo user"), storage=AvatarUserMediaStorage(), null=True
    )

    language = models.CharField(
        verbose_name=_("Language"),
        max_length=64,
        choices=settings.LANGUAGES,
        default=settings.DEFAULT_LANGUAGE,
        help_text=_("The primary language used by this user"),
    )

    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)

    joined_at = models.DateField(_("joined at"), auto_now_add=True)

    short_phone_prefix = models.IntegerField(
        verbose_name=_("Phone Prefix Country"),
        help_text=_("Phone prefix of the user"),
        null=True,
    )

    phone = models.BigIntegerField(
        verbose_name=_("Telephone Number"),
        help_text=_("Phone number of the user; include area code"),
        null=True,
    )

    last_update_profile = models.DateTimeField(
        verbose_name=_("Last Updated Profile"),
        null=True,
    )

    utm = JSONField(verbose_name=_("UTM Marketing"), default=dict)
    email_marketing = models.BooleanField(
        verbose_name=_("Allows receiving marketing emails"), default=True
    )

    objects = UserManager()

    @property
    def token_generator(self):
        return PasswordResetTokenGenerator()

    def check_password_reset_token(self, token):
        return self.token_generator.check_token(self, token)

    def send_change_password_email(self):
        if not settings.SEND_EMAILS:
            return False  # pragma: no cover
        context = {"name": self.first_name}
        send_mail(
            _("Password changed"),
            render_to_string("authentication/emails/change_password.txt"),
            None,
            [self.email],
            html_message=render_to_string(
                "authentication/emails/change_password.html", context
            ),
        )

    def send_email_nickname_changed(self, before_nickname: str, new_nickname: str):
        if not settings.SEND_EMAILS:
            return False
        context = {
            "user_name": self.first_name,
            "before_nickname": before_nickname,
            "new_nickname": new_nickname
        }
        send_mail(
            _("Nickname changed"),
            render_to_string("authentication/emails/nickname_changed.txt"),
            None,
            [self.email],
            html_message=render_to_string(
                "authentication/emails/nickname_changed.html", context
            ),
        )

    def send_request_flow_user_info(self):
        if not settings.SEND_REQUEST_FLOW:
            return False  # pragma: no cover
        requests.post(
            url=f"{settings.FLOWS_URL}api/v2/flow_starts.json",
            json={
                "flow": settings.FLOW_MARKETING_UUID,
                "params": {
                    "first_name": self.first_name,
                    "last_name": self.last_name,
                    "email": self.email,
                    "language": self.language,
                    "short_phone_prefix": self.short_phone_prefix,
                    "phone": self.phone,
                    "utm": self.utm,
                    "email_marketing": self.email_marketing,
                },
                "urns": [f"mailto:{self.email}"],
            },
            headers={
                "Authorization": f"Token {settings.TOKEN_AUTHORIZATION_FLOW_MARKETING}"
            },
        )

    @property
    def photo_url(self):
        if self.photo and hasattr(self.photo, "url"):
            return self.photo.url
