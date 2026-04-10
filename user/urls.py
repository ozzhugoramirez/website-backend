from django.urls import path
from .views import GoogleLoginAPIView, EmployeeLoginAPIView

urlpatterns = [
    path('auth/google/', GoogleLoginAPIView.as_view(), name='google_login'),
    path('auth/employee-login/', EmployeeLoginAPIView.as_view(), name='employee_login'),
]