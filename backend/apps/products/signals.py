from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ProductVariant, Product

@receiver([post_save, post_delete], sender=ProductVariant)
def update_product_stock(sender, instance, **kwargs):
    """Met à jour le stock total du produit basé sur ses variants"""
    product = instance.product
    total_stock = product.variants.aggregate(total=models.Sum('stock'))['total'] or 0
    product.stock = total_stock
    product.save(update_fields=['stock'])