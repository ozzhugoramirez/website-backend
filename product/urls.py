from django.urls import path
from .views import (
    PublicProductListView, PublicProductDetailView, ProductLikeToggleView,
    DashboardProductListCreateView, DashboardProductDetailUpdateDeleteView
)

urlpatterns = [
    # ---- RUTAS PÚBLICAS (TIENDA NEXT.JS) ----
    path('store/products/', PublicProductListView.as_view(), name='public_product_list'),
    path('store/products/<slug:slug>/', PublicProductDetailView.as_view(), name='public_product_detail'),
    path('store/products/<int:product_id>/like/', ProductLikeToggleView.as_view(), name='product_like_toggle'),

    # ---- RUTAS PRIVADAS (DASHBOARD) ----
    path('dashboard/products/', DashboardProductListCreateView.as_view(), name='dash_product_list'),
    path('dashboard/products/<int:pk>/', DashboardProductDetailUpdateDeleteView.as_view(), name='dash_product_detail'),
]