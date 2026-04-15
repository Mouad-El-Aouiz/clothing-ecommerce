from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.utils import timezone 
from .models import CartItem, Cart

@receiver([pre_save, post_delete], sender=CartItem)
def update_cart_updated_at(sender, instance, **kwargs):
    """Met à jour la date de modification du panier"""
    if instance.cart:
        instance.cart.updated_at = timezone.now()
        instance.cart.save(update_fields=['updated_at'])