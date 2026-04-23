from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from user.permissions import IsDashboardStaff 
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser


class PublicProductListView(generics.ListAPIView):
    """ Lista solo productos activos para la tienda """
    serializer_class = ProductSerializer
    permission_classes = [] 

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('category').prefetch_related('images').order_by('-created_at')

class PublicProductDetailView(generics.RetrieveAPIView):
    """ Detalle del producto. Al consultarlo, suma +1 a las vistas """
    serializer_class = ProductSerializer
    permission_classes = []
    lookup_field = 'slug'

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
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
#  VISTAS DEL DASHBOARD (Para empleados/Admin)
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
   



class DashboardImageUploadView(generics.CreateAPIView):
    """ Permite subir una imagen asociada a un producto """
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsDashboardStaff]
    parser_classes = (MultiPartParser, FormParser) 

class DashboardImageDeleteView(generics.DestroyAPIView):
    """ Elimina una imagen """
    queryset = ProductImage.objects.all()
    permission_classes = [IsDashboardStaff]

class DashboardImageSetMainView(APIView):
    """ Marca una imagen como principal """
    permission_classes = [IsDashboardStaff]

    def post(self, request, pk):
        image = get_object_or_404(ProductImage, id=pk)
        image.is_main = True
        image.save() 
        return Response({"message": "Imagen marcada como principal"}, status=status.HTTP_200_OK)