from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.models import User
from apps.users.serializer import UserSerializer, VerifyAccountSerializer

from apps.users.emails import send_otp_email


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass


class LoginUser(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterUser(APIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_otp_email(serializer.data["email"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTP(APIView):
    serializer_class = VerifyAccountSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data["email"]
        user = User.objects.filter(email=email).first()

        user.is_verified = True
        user.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUserProfile(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)
