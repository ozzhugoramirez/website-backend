from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class ProfileUpdateSerializer(serializers.ModelSerializer):
    """ Serializador para cuando queramos editar el perfil (ej. sumar coins o cambiar teléfono) """
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'city', 'coins']

class CustomerListSerializer(serializers.ModelSerializer):
    """ Serializador que combina datos del Usuario y su Perfil para la tabla del Dashboard """
    
    # Extraemos campos del Profile asociado
    coins = serializers.DecimalField(source='profile.coins', max_digits=10, decimal_places=2, read_only=True)
    phone = serializers.CharField(source='profile.phone', read_only=True)
    
    # Formateamos la fecha de creación del perfil para que Next.js no tenga que lidiar con fechas feas
    registro = serializers.DateTimeField(source='profile.created_at', format="%d/%m/%Y", read_only=True)
    
    # Unimos el nombre para facilitar las cosas en el frontend
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'coins', 'phone', 'registro', 'is_active']
        
    def get_full_name(self, obj):
        return obj.get_full_name()