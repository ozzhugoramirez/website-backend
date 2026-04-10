from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

# --------------------------------------------------------
# 1. SERIALIZADOR COMPLETO DEL PERFIL (Para el Drawer)
# --------------------------------------------------------
class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # Excluimos 'user' porque ya va a estar anidado
        exclude = ['user', 'id']

class CustomerDetailSerializer(serializers.ModelSerializer):
    """ Este manda absolutamente toda la data del cliente al panel lateral """
    profile = ProfileDetailSerializer(read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    is_online = serializers.BooleanField(read_only=True)
    compras_totales = serializers.IntegerField(source='total_purchases', read_only=True)

    date_joined = serializers.DateTimeField(source='profile.created_at', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'is_active', 'date_joined',  'date_joined',
            'last_login', 'is_online', 'compras_totales', 'profile'
        ]

# --------------------------------------------------------
# 2. SERIALIZADOR RESUMIDO 
# --------------------------------------------------------
class CustomerListSerializer(serializers.ModelSerializer):
    """ Este es liviano para no saturar la red si tenés 5000 clientes """
    coins = serializers.DecimalField(source='profile.coins', max_digits=10, decimal_places=2, read_only=True)
    phone = serializers.CharField(source='profile.phone', read_only=True)
    ranking = serializers.CharField(source='profile.ranking', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    is_online = serializers.BooleanField(read_only=True)
    compras_totales = serializers.IntegerField(source='total_purchases', read_only=True)

   

    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'coins', 'phone',
            'is_active', 'compras_totales', 'ranking', 'is_online'
        ]


