from django.urls import path

from .views import (
    UserInitializationAPIView,
    UserProfileAPIViewSet,
    UserVerificationAPIView,
)

urlpatterns = [
    path("auth/phone/", UserInitializationAPIView.as_view(), name="phone_init"),
    path("auth/verify_code/", UserVerificationAPIView.as_view(), name="verify_code"),
    path(
        "user/profile/",
        UserProfileAPIViewSet.as_view({"get": "profile"}),
        name="user_profile",
    ),
    path(
        "user/profile/add_referral/",
        UserProfileAPIViewSet.as_view({"patch": "add_referral"}),
        name="add_referral",
    ),
]
