from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    
    # ==========================================
    #  DATOS DE CONTACTO Y LOGÍSTICA (ENVÍOS)
    # ==========================================
    phone = models.CharField(max_length=20, blank=True, null=True)
    alt_phone = models.CharField(max_length=20, blank=True, null=True) # Clave por si el correo falla en la entrega
    
    address = models.CharField(max_length=255, blank=True, null=True)
    address_reference = models.CharField(max_length=255, blank=True, null=True) # Ej: "Casa con rejas negras, timbre roto"
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True) # Provincia
    country = models.CharField(max_length=100, default='Argentina')
    zip_code = models.CharField(max_length=20, blank=True, null=True) # Código Postal
    
    # ==========================================
    #  DATOS FISCALES / FACTURACIÓN
    # ==========================================
    # Vital en Argentina para emitir Factura A o B automáticamente en el futuro
    document_type = models.CharField(max_length=10, choices=[('DNI', 'DNI'), ('CUIL', 'CUIL'), ('CUIT', 'CUIT')], default='DNI')
    document_number = models.CharField(max_length=50, blank=True, null=True)

    # ==========================================
    #  FIDELIZACIÓN Y MARKETING
    # ==========================================
    coins = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    birth_date = models.DateField(blank=True, null=True) # Para mandarle un cupón automático el día de su cumpleaños
    newsletter_subscribed = models.BooleanField(default=True) # Si acepta recibir correos de promociones (Legalmente necesario)

    # ==========================================
    #  METADATA INTERNA
    # ==========================================
    notes = models.TextField(blank=True, null=True) # Solo visible para el Admin (Ej: "Cliente problemático, revisar pagos")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perfil de {self.user.email}"

    @property
    def ranking(self):
        """Calcula el nivel de fidelidad basado en los Silo Coins."""
        if self.coins >= 1000: return "Platino"
        elif self.coins >= 500: return "Oro"
        elif self.coins >= 100: return "Plata"
        return "Bronce"