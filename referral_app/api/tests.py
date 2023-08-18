from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APIClient,
    APIRequestFactory,
    APITestCase,
    force_authenticate,
)

from referral_app.api.models import User
from referral_app.api.utils.exceptions import ReferralAlreadyExist
from referral_app.api.views import UserProfileAPIViewSet


class UserInitializationAPIViewTest(APITestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.data = {"phone_number": "77891231234"}
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)

        self.phone_init_api = reverse("phone_init")
        self.verify_code_api = reverse("verify_code")
        self.user_profile_api = reverse("user_profile")
        self.user_add_referral_api = reverse("add_referral")

    def test_authentication_user_by_phone(self):
        response = self.client.post(self.phone_init_api, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        auth_code = response.data.get("Authentication code")
        self.assertRegex(auth_code, r"\d{4}")
        self.data.update({"authorization_code": auth_code})

        response = self.client.post(self.verify_code_api, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, text="token")

    def test_initialize_user_by_incorrect_phone(self):
        data = {"phone_number": 7789123123}
        response = self.client.post(self.phone_init_api, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_verification_missing_auth_code(self):
        self.client.post(self.phone_init_api, self.data, format="json")
        response = self.client.post(self.verify_code_api, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_profile(self):
        data = {
            "phone_number": self.user1.phone_number,
            "authorization_code": self.user1.authorization_code,
        }
        response = self.client.post(self.verify_code_api, data, format="json")
        token = response.data.get("token")
        request = self.factory.get(self.user_profile_api)
        force_authenticate(request, self.user1, token)
        view = UserProfileAPIViewSet.as_view({"get": "profile"})
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get("user").get("phone_number"), self.user1.phone_number
        )
        self.assertContains(response, text="invite_code")

    def test_user_add_referral(self):
        data = {
            "phone_number": self.user1.phone_number,
            "authorization_code": self.user1.authorization_code,
        }
        response = self.client.post(self.verify_code_api, data, format="json")
        token = response.data.get("token")
        request = self.factory.patch(
            self.user_add_referral_api,
            {"invite_code": self.user2.invite_code},
        )
        force_authenticate(request, self.user1, token)
        view = UserProfileAPIViewSet.as_view({"patch": "add_referral"})
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, text="Referrer added successfully")

        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaises(ReferralAlreadyExist)
        self.assertEqual(self.user1.referral_activated, True)
