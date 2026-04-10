from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from .serializers import *
from user.permissions import IsDashboardStaff, IsAdmin 

User = get_user_model()

class CustomerListAPIView(generics.ListAPIView):
   
    serializer_class = CustomerListSerializer
    permission_classes = [IsDashboardStaff]
    
    def get_queryset(self):
        return User.objects.filter(role='CUS').select_related('profile').order_by('-id')

class CustomerDetailAPIView(generics.RetrieveUpdateAPIView):

    serializer_class = CustomerDetailSerializer
    permission_classes = [IsDashboardStaff]
    
    def get_queryset(self):
        return User.objects.filter(role='CUS').select_related('profile')

class CustomerBulkDeleteAPIView(APIView):
  
    permission_classes = [IsAdmin]

    def post(self, request):
        user_ids = request.data.get('ids', [])
        if not user_ids:
            return Response({"error": "No se seleccionaron clientes"}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user.id in user_ids:
            return Response({"error": "No puedes eliminar tu propia cuenta"}, status=status.HTTP_403_FORBIDDEN)

        User.objects.filter(id__in=user_ids, role='CUS').delete()
        return Response({"message": "Clientes eliminados exitosamente"}, status=status.HTTP_200_OK)