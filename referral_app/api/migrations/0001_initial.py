# Generated by Django 4.2.4 on 2023-08-18 17:48

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ReferralLink",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        max_length=11,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Phone number format: 7xxxxxxxxxx, with digits from 0 to 9 instead of x",
                                regex="^7\\d{10}$",
                            )
                        ],
                        verbose_name="Phone number",
                    ),
                ),
                (
                    "invite_code",
                    models.CharField(
                        blank=True, max_length=6, verbose_name="Invite code"
                    ),
                ),
                ("referral_activated", models.BooleanField(default=False)),
                (
                    "authorization_code",
                    models.CharField(
                        blank=True, max_length=4, verbose_name="Authorization code"
                    ),
                ),
                ("last_login", models.DateTimeField(auto_now=True)),
                (
                    "referred_users",
                    models.ManyToManyField(through="api.ReferralLink", to="api.user"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="referrallink",
            name="from_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="link_made_by",
                to="api.user",
            ),
        ),
        migrations.AddField(
            model_name="referrallink",
            name="to_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="link_refer_to",
                to="api.user",
            ),
        ),
    ]
