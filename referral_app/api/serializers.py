from rest_framework import serializers

from .models import User
from .utils.generate_code import generate_authorization_code, generate_invite_code


class ReferralLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_number"]


class UserProfileSerializer(serializers.ModelSerializer):
    referred_users = ReferralLinkSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["phone_number", "invite_code", "referral_activated", "referred_users"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["referred_users"] = ReferralLinkSerializer(
            instance.referred_users.all(), many=True
        ).data
        return representation


class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("phone_number", "authorization_code", "token")

        read_only_fields = ("token",)


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("phone_number", "authorization_code")

    def create(self, validated_data):
        validated_data["invite_code"] = generate_invite_code()
        validated_data["authorization_code"] = generate_authorization_code()

        return super().create(validated_data)
