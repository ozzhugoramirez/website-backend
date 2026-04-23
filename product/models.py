from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    # ==========================
    # 📌 INFORMACIÓN BÁSICA
    # ==========================
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True) # Para URLs amigables (ej: silo.com/taza-ceramica)
    description = models.TextField()
    sku = models.CharField(max_length=50, unique=True) # Código único de inventario
    
    # ==========================
    # 💰 PRECIOS Y STOCK
    # ==========================
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True) # Si es False, es un "Borrador" o está oculto
    
    # ==========================
    # 📈 MÉTRICAS E INTERACCIÓN
    # ==========================
    views = models.PositiveIntegerField(default=0) # Contador de visitas
    sales_count = models.PositiveIntegerField(default=0) # Para saber cuáles son los más vendidos
    # Relación ManyToMany para que los usuarios puedan darle "Me gusta" o guardar en favoritos
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favorite_products', blank=True)

    # ==========================
    # ⏱️ METADATA
    # ==========================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    """ Para permitir múltiples imágenes por producto (Galería) """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False) # Para marcar cuál es la foto de portada

    def save(self, *args, **kwargs):
        
        if self.is_main:
            ProductImage.objects.filter(product=self.product).update(is_main=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Imagen de {self.product.name}"