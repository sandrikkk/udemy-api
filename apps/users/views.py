from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.models import User
from apps.users.serializer import UserSerializer, VerifyAccountSerializer
from apps.users.tasks import send_otp_email


class LoginUser(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class RegisterUser(APIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self._create_user(serializer)
        self._send_otp_email(serializer)
        return self._response(serializer.data, status.HTTP_201_CREATED)

    def _create_user(self, serializer):
        serializer.save()

    def _send_otp_email(self, serializer):
        email = serializer.data.get("email")
        send_otp_email.delay(email)

    def _response(self, data, status_code):
        return Response(data, status=status_code)


class VerifyOTP(APIView):
    permissions = [IsAuthenticated]
    serializer_class = VerifyAccountSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data.get("email")
        user = User.objects.filter(email=email).first()

        user.is_verified = True
        user.save()

        return Response(
            data={"message": "you have successfully completed the verification process"},
            status=status.HTTP_200_OK,
        )


class GetUserProfile(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)
