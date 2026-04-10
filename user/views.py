import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login

User = get_user_model()

class GoogleLoginAPIView(APIView):
    permission_classes = []
    
    def post(self, request):
        access_token = request.data.get('access_token')
        
        if not access_token:
            return Response({"error": "Se requiere un access_token"}, status=status.HTTP_400_BAD_REQUEST)

        google_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
        response = requests.get(google_url, params={'access_token': access_token})

        if not response.ok:
            return Response({"error": "El token de Google es inválido o expiró"}, status=status.HTTP_400_BAD_REQUEST)

        user_data = response.json()
        email = user_data.get('email')
        first_name = user_data.get('given_name', '')
        last_name = user_data.get('family_name', '')
        
        try:
            user = User.objects.get(email=email)
            if user.auth_provider != User.AuthProviders.GOOGLE:
                user.auth_provider = User.AuthProviders.GOOGLE
                user.save()
        except User.DoesNotExist:
            user = User.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                auth_provider=User.AuthProviders.GOOGLE
            )

       
        update_last_login(None, user)

        refresh = RefreshToken.for_user(user)

        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'role': user.role
            }
        }, status=status.HTTP_200_OK)


class EmployeeLoginAPIView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email y contraseña son obligatorios"}, status=status.HTTP_400_BAD_REQUEST)

        
        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({"error": "Este usuario está inactivo"}, status=status.HTTP_403_FORBIDDEN)

        
        allowed_roles = [User.Roles.ADMIN, User.Roles.MANAGER, User.Roles.EMPLOYEE]
        if user.role not in allowed_roles and not user.is_superuser:
            return Response({"error": "No tienes permisos para acceder al Dashboard"}, status=status.HTTP_403_FORBIDDEN)

        # Registramos el último ingreso
        update_last_login(None, user)

      
        refresh = RefreshToken.for_user(user)

        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'role': user.role
            }
        }, status=status.HTTP_200_OK)