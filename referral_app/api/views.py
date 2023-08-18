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
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

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

    @decorators.action(methods=["get"], detail=True)
    def profile(self, request):
        user = request.user
        serializer = self.serializer_class(user)

        return Response({"user": serializer.data})

    @decorators.action(methods=["patch"], detail=True)
    def add_referral(self, request):
        invite_code = request.data.get("invite_code")
        response = add_referral(request=request, invite_code=invite_code)
        return Response(response)
