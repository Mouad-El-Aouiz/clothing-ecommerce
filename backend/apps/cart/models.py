from django.db import models
from django.contrib.auth.models import User
from apps.products.models import ProductVariant
from django.core.exceptions import ValidationError

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_items(self):
        """Optimisé avec une seule requête"""
        return self.items.aggregate(total=models.Sum('quantity'))['total'] or 0
    
    def get_total_price(self):
        """Optimisé avec une seule requête"""
        total = 0
        for item in self.items.select_related('variant__product'):
            total += item.variant.final_price * item.quantity
        return total
    
    def add_item(self, variant, quantity=1):
        """Ajoute un article au panier avec validation de stock"""
        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            variant=variant,
            defaults={'quantity': 0}
        )
        
        new_quantity = quantity if created else cart_item.quantity + quantity
        
        if new_quantity > variant.stock:
            raise ValueError(f'Stock insuffisant. Maximum: {variant.stock}')
        
        cart_item.quantity = new_quantity
        cart_item.save()
        return cart_item
    
    def remove_item(self, variant):
        """Supprime un article du panier"""
        self.items.filter(variant=variant).delete()
    
    def clear(self):
        """Vide complètement le panier"""
        self.items.all().delete()
    
    def is_empty(self):
        """Vérifie si le panier est vide"""
        return self.items.count() == 0

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ['cart', 'variant']

    def clean(self):
        """Validation avant sauvegarde"""
        if self.quantity > self.variant.stock:
            raise ValidationError({
                'quantity': f'Stock insuffisant. Maximum: {self.variant.stock}'
            })

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        return self.variant.final_price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.variant.product.name}"