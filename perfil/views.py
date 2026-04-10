from rest_framework import generics
from django.contrib.auth import get_user_model
from .models import Profile
from .serializers import CustomerListSerializer, ProfileUpdateSerializer

# Importamos el permiso de seguridad que creamos en el paso 1
from user.permissions import IsDashboardStaff 

User = get_user_model()

class CustomerListAPIView(generics.ListAPIView):
    """
    GET: Lista todos los usuarios que son clientes (CUS).
    Protegido: Solo accesible por staff del dashboard.
    """
    serializer_class = CustomerListSerializer
    permission_classes = [IsDashboardStaff]
    
    def get_queryset(self):
        # select_related('profile') hace que la base de datos traiga el perfil en la misma 
        # consulta SQL, evitando el problema de "N+1 queries" (optimización clave)
        return User.objects.filter(role='CUS').select_related('profile').order_by('-id')


class CustomerProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    """
    GET: Trae el perfil detallado de un cliente específico.
    PUT/PATCH: Actualiza el perfil (por ejemplo, para cargarle Silo Coins).
    Protegido: Solo accesible por staff del dashboard.
    """
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsDashboardStaff]
    queryset = Profile.objects.all()
    
    # En vez de buscar por ID de perfil, buscamos por ID de usuario que es más intuitivo
    lookup_field = 'user_id'