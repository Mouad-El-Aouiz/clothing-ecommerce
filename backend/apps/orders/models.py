from django.db import models
from django.contrib.auth.models import User
from apps.products.models import ProductVariant
import uuid

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('PROCESSING', 'En traitement'),
        ('CONFIRMED', 'Confirmée'),
        ('SHIPPED', 'Expédiée'),
        ('DELIVERED', 'Livrée'),
        ('CANCELLED', 'Annulée'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('PAID', 'Payée'),
        ('FAILED', 'Échouée'),
        ('REFUNDED', 'Remboursée'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_postal_code = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} - {self.user.username}"
    
    # ✅ MÉTHODES DÉPLACÉES ICI (dans Order, pas OrderItem)
    def can_cancel(self):
        """Vérifie si la commande peut être annulée"""
        return self.status in ['PENDING', 'PROCESSING']
    
    def cancel(self):
        """Annule la commande et restaure le stock"""
        if self.can_cancel():
            self.status = 'CANCELLED'
            # Restaurer le stock
            for item in self.items.all():
                item.variant.stock += item.quantity
                item.variant.save()
            self.save()
            return True
        return False
    
    def update_status(self, new_status):
        """Met à jour le statut avec validation"""
        if new_status in dict(self.STATUS_CHOICES):
            self.status = new_status
            self.save()
            return True
        return False

    def get_status_display_fr(self):
        """Retourne le statut en français"""
        status_map = {
            'PENDING': 'En attente',
            'PROCESSING': 'En traitement',
            'CONFIRMED': 'Confirmée',
            'SHIPPED': 'Expédiée',
            'DELIVERED': 'Livrée',
            'CANCELLED': 'Annulée',
        }
        return status_map.get(self.status, self.status)
    
    def get_payment_status_display_fr(self):
        """Retourne le statut paiement en français"""
        status_map = {
            'PENDING': 'En attente',
            'PAID': 'Payée',
            'FAILED': 'Échouée',
            'REFUNDED': 'Remboursée',
        }
        return status_map.get(self.payment_status, self.payment_status)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)
    product_name = models.CharField(max_length=200)
    product_image = models.CharField(max_length=500, blank=True)

    @property
    def total_price(self):
        return self.price_at_time * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"