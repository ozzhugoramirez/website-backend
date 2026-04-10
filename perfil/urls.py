from django.urls import path
from .views import *
urlpatterns = [
    #
    path('customers/', CustomerListAPIView.as_view(), name='customer_list'),
    
    
    path('customers/bulk-delete/', CustomerBulkDeleteAPIView.as_view(), name='customer_bulk_delete'),
    
  
    path('customers/<int:pk>/', CustomerDetailAPIView.as_view(), name='customer_detail'),
]