import datetime
import os

import jwt
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")


class User(AbstractBaseUser):
    password = None
    phone_number_validator = RegexValidator(
        regex=r"^7\d{10}$",
        message=_(
            "Phone number format: 7xxxxxxxxxx, with digits from 0 to 9 instead of x"
        ),
    )

    phone_number = models.CharField(
        max_length=11,
        unique=True,
        null=False,
        blank=False,
        validators=[phone_number_validator],
        verbose_name=_("Phone number"),
    )
    invite_code = models.CharField(
        max_length=6, blank=True, verbose_name=_("Invite code")
    )
    referral_activated = models.BooleanField(default=False)
    authorization_code = models.CharField(
        max_length=4,
        blank=True,
        verbose_name=_("Authorization code"),
    )
    last_login = models.DateTimeField(auto_now=True)
    referred_users = models.ManyToManyField(
        "self", through="ReferralLink", symmetrical=False
    )

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["phone_number"]

    def __str__(self):
        return _("User with phone number: ") + self.phone_number

    @property
    def token(self):
        payload_data = {
            "phone_number": self.phone_number,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=90),
        }

        return jwt.encode(payload_data, SECRET_KEY, algorithm="HS256")


class ReferralLink(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="link_made_by"
    )

    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="link_refer_to"
    )
