from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import LoginSerializer, RegisterModelSerializer, VerifyCodeSerializer, \
    RessetVerifyCodeSerializer, ResetPasswordSerializer, ConfirmPasswordSerializer


@extend_schema(tags=['auth'], description="""
API for login users that already exists in database
""")
class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tokens = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(tokens.access_token),
                "refresh": str(tokens)
            },
            status=HTTP_200_OK
        )


@extend_schema(tags=['auth'], description="""
API for users registrations
""")
class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterModelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = User(**serializer.validated_data)
        user.set_password(password)
        user.save()
        return Response({f"Verification code sent to you email: {email}"})


@extend_schema(tags=['auth'], description="""
API for verify code
""")
class VerifyCodeApiView(GenericAPIView):
    serializer_class = VerifyCodeSerializer

    def post(self, request, *args, **kwargs):
        serialize = self.get_serializer(data=request.data)
        serialize.is_valid(raise_exception=True)
        return Response({"Successfully verified code!"}, status=HTTP_200_OK)


@extend_schema(tags=['auth'], description="""
API for reset verification code
""")
class ResetVerificationCodeAPIView(GenericAPIView):
    serializer_class = RessetVerifyCodeSerializer

    def post(self, request, *args, **kwargs):
        serialize = self.get_serializer(data=request.data)
        serialize.is_valid(raise_exception=True)
        return Response({"Successfully resend verification code!"}, status=HTTP_200_OK)


@extend_schema(tags=['auth'], description="""
API for reset user password
""")
class ResetPasswordAPIView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        phone = serializer.validated_data.get('phone')
        if email:
            return Response({"message": f"Sent verification code to your email: {email}"})
        return Response({"message": f"Sent via SMS verification code to your phone: {phone}"})


@extend_schema(tags=['auth'], description="""
API for user confirm new password
""")
class ConfirmNewPasswordAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ConfirmPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "✅Successfully updated your password!"})
