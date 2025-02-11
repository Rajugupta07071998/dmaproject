from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import random
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string




# OTP Generation Function
def generate_otp():
    return str(random.randint(100000, 999999))  # 6-digit OTP


def send_otp_email(context_data):
    subject = context_data.get('subject')
    message = render_to_string(context_data.get('html'), context_data)

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [context_data.get('email'), 'armyfriend8372@gmail.com']

    email = EmailMessage(subject, message, from_email, recipient_list)
    email.content_subtype = "html"

    # image_path = '/home/user/Desktop/project/ecommerce/account/static/account/images/logo3.png'  # Change this to the path of your image
    # email.attach_file(image_path)
    email.send()



User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = data.get('username')
        email = data.get('email')
        mobile_number = data.get('mobile_number')
        user_type = data.get('user_type')
        password = data.get('password')

        if not all([username, email, mobile_number, user_type, password]):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(mobile_number=mobile_number).exists():
            return Response({"error": "Mobile number already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate OTP and save it in Redis (cache)
        otp = generate_otp()
        cache.set(email, otp, timeout=300)  # OTP valid for 5 minutes

        # Send OTP to user's email
        context_data = {
                'subject': 'Your OTP for Registration!',
                'html': 'account/send-otp-email.html',
                'email': email,
                'otp': f'Your OTP for registration is: {otp}',
                'username': username,
            }
        send_otp_email(context_data)

        return Response({"message": "OTP sent to email, please verify."}, status=200)
    


class VerifyOtpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = data.get('username')
        email = data.get('email')
        mobile_number = data.get('mobile_number')
        user_type = data.get('user_type')
        password = data.get('password')
        otp = data.get('otp')  # OTP sent by the user

        # Check if OTP matches
        cached_otp = cache.get(email)
        if not cached_otp:
            return Response({"error": "OTP expired or invalid."}, status=status.HTTP_400_BAD_REQUEST)

        if cached_otp != otp:
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        # Check for duplicate data
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(mobile_number=mobile_number).exists():
            return Response({"error": "Mobile number already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            username=username,
            email=email,
            mobile_number=mobile_number,
            user_type=user_type,
            password=make_password(password)
        )

        # Clear OTP from Redis after use
        cache.delete(email)

        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "mobile_number": user.mobile_number,
                    "user_type": user.user_type,
                },
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
    


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "mobile_number": user.mobile_number,
                    "user_type": user.user_type,
                },
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    


# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             refresh_token = request.data.get("refresh")
#             refresh_token = request.headers.get("Authorization").split(" ")[1]
#             if not refresh_token:
#                 return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

#             token = RefreshToken(refresh_token)
#             token.blacklist()  # Blacklist the refresh token

#             return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
