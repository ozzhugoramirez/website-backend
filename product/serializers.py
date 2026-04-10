from rest_framework import serializers
from .models import Category, Product, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_main']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    images = ProductImageSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_in_stock = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'sku', 'price', 'discount_price',
            'stock', 'is_in_stock', 'is_active', 'views', 'sales_count', 
            'likes_count', 'category', 'category_id', 'images', 'created_at'
        ]
        # Protegemos estas métricas para que nadie las modifique manualmente desde una API
        read_only_fields = ['views', 'sales_count', 'likes_count', 'slug']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_in_stock(self, obj):
        return obj.stock > 0