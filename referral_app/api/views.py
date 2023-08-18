from drf_yasg.utils import swagger_auto_schema
from rest_framework import decorators, mixins, status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import CreateUserSerializer, UserAuthSerializer, UserProfileSerializer
from .utils.add_referral_link import add_referral
from .utils.authentication import JWTAuthentication, authenticate_user


class UserInitializationAPIView(CreateAPIView):
    """Initialize user via phone number.

    :Parameter: phone number
    :Returns: authorization code
    """

    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    @decorators.action(detail=False, methods=["POST"])
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            {
                "Authentication code": serializer.data.get("authorization_code"),
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class UserVerificationAPIView(APIView):
    @staticmethod
    @swagger_auto_schema(
        request_body=UserAuthSerializer,
        operation_summary="Verify the authorization code",
        operation_description="Return auth token",
    )
    def post(request):
        user = authenticate_user(request)

        if user:
            serializer = UserAuthSerializer(user)
            return Response(serializer.data, status.HTTP_200_OK)


class UserProfileAPIViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(
        query_serializer=UserProfileSerializer,
        operation_summary="Api for adding the referral link",
        operation_description="Return ",
    )
    @decorators.action(methods=["get"], detail=True)
    def profile(self, request):
        user = request.user
        serializer = self.serializer_class(user)

        return Response({"user": serializer.data})

    @swagger_auto_schema(
        methods=["patch"],
        request_body=UserProfileSerializer(required=["phone_number", "invite_code"]),
        operation_summary="Api for adding the referral link",
        operation_description="Return ",
    )
    @decorators.action(methods=["patch"], detail=True)
    def add_referral(self, request):
        invite_code = request.data.get("invite_code")
        response = add_referral(request=request, invite_code=invite_code)
        return Response(response)
