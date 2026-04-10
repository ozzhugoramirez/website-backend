from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer
from user.permissions import IsDashboardStaff # El permiso que creamos antes
from rest_framework.permissions import IsAuthenticated
# =======================================================
# 🌐 VISTAS PÚBLICAS (Para los clientes en la tienda)
# =======================================================

class PublicProductListView(generics.ListAPIView):
    """ Lista solo productos activos para la tienda """
    serializer_class = ProductSerializer
    permission_classes = [] 

    def get_queryset(self):
        # Le agregamos el order_by para que los más nuevos salgan primero y Django no se queje
        return Product.objects.filter(is_active=True).select_related('category').prefetch_related('images').order_by('-created_at')

class PublicProductDetailView(generics.RetrieveAPIView):
    """ Detalle del producto. Al consultarlo, suma +1 a las vistas """
    serializer_class = ProductSerializer
    permission_classes = []
    lookup_field = 'slug' # Buscamos por URL amigable, no por ID

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # 📈 Sumamos una vista cada vez que alguien entra a la página del producto
        instance.views += 1
        instance.save(update_fields=['views'])
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ProductLikeToggleView(APIView):
    """ Permite a un cliente logueado dar o quitar Like a un producto """
    
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        if request.user in product.likes.all():
            product.likes.remove(request.user)
            return Response({"message": "Like quitado", "liked": False})
        else:
            product.likes.add(request.user)
            return Response({"message": "Like agregado", "liked": True})


# =======================================================
# 🛡️ VISTAS DEL DASHBOARD (Para empleados/Admin)
# =======================================================

class DashboardProductListCreateView(generics.ListCreateAPIView):
    """ Los empleados pueden ver TODOS los productos (incluso inactivos) y crear nuevos """
    serializer_class = ProductSerializer
    permission_classes = [IsDashboardStaff]

    def get_queryset(self):
        # Ordenamos por los más nuevos primero
        return Product.objects.all().select_related('category').prefetch_related('images').order_by('-created_at')

class DashboardProductDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """ Los empleados pueden modificar, ocultar o eliminar productos """
    serializer_class = ProductSerializer
    permission_classes = [IsDashboardStaff]
    queryset = Product.objects.all()
    # Acá sí buscamos por ID, que es más seguro para un panel de administración