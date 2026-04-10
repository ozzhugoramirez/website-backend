from django.urls import path
from .views import CustomerListAPIView, CustomerProfileDetailAPIView

urlpatterns = [
    
    path('customers/', CustomerListAPIView.as_view(), name='customer_list'),
    
  
    path('customers/<int:user_id>/profile/', CustomerProfileDetailAPIView.as_view(), name='customer_profile_detail'),
]