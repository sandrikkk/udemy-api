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
        email = serializer.data["email"]
        send_otp_email.delay(email)

    def _response(self, data, status_code):
        return Response(data, status=status_code)


class VerifyOTP(APIView):
    serializer_class = VerifyAccountSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data["email"]
        user = self._get_user(email)

        if user:
            self._verify_user(user)
            return self._response(serializer.data, status.HTTP_200_OK)
        else:
            return self._response(
                {"detail": "User not found"}, status.HTTP_404_NOT_FOUND
            )

    def _get_user(self, email):
        return User.objects.filter(email=email).first()

    def _verify_user(self, user):
        user.is_verified = True
        user.save()

    def _response(self, data, status_code):
        return Response(data, status=status_code)


class GetUserProfile(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)
