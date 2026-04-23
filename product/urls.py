from django.urls import path
from .views import *

urlpatterns = [
    # ---- RUTAS PÚBLICAS (TIENDA NEXT.JS) ----
    path('store/products/', PublicProductListView.as_view(), name='public_product_list'),
    path('store/products/<slug:slug>/', PublicProductDetailView.as_view(), name='public_product_detail'),
    path('store/products/<int:product_id>/like/', ProductLikeToggleView.as_view(), name='product_like_toggle'),

    # ---- RUTAS PRIVADAS (DASHBOARD) ----
    path('dashboard/products/', DashboardProductListCreateView.as_view(), name='dash_product_list'),
    path('dashboard/products/<int:pk>/', DashboardProductDetailUpdateDeleteView.as_view(), name='dash_product_detail'),
    # ... tus otras rutas del dashboard ...
    path('dashboard/images/', DashboardImageUploadView.as_view(), name='dash_image_upload'),
    path('dashboard/images/<int:pk>/', DashboardImageDeleteView.as_view(), name='dash_image_delete'),
    path('dashboard/images/<int:pk>/set-main/', DashboardImageSetMainView.as_view(), name='dash_image_set_main'),
]