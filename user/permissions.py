# user/permissions.py
from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'ADMIN' or request.user.is_superuser
        )
    

class IsDashboardStaff(permissions.BasePermission):
  
    def has_permission(self, request, view):
        allowed_roles = ['ADMIN', 'MGR', 'EMP']
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.role in allowed_roles or request.user.is_superuser)
        )

class IsLogistics(permissions.BasePermission):
    def has_permission(self, request, view):
        
        allowed = ['ADMIN', 'MANAGER', 'LOGISTICS'] 
        return request.user.is_authenticated and (
            request.user.role in allowed or request.user.is_superuser
        )
    


"""
from .permissions import IsAdmin, IsLogistics

class InventarioView(APIView):
    permission_classes = [IsLogistics] # Logística y Admin pueden ver esto
    
    def get(self, request):
        return Response({"data": "Productos de logística"})

class FinanzasView(APIView):
    permission_classes = [IsAdmin] # SOLO Admin puede ver esto
    
    def get(self, request):
        return Response({"data": "Datos sensibles de dinero"})

"""