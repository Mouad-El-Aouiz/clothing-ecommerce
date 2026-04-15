from django.db import models
from django.contrib.auth.models import User
from apps.orders.models import Order

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('STRIPE', 'Carte Bancaire'),
        ('PAYPAL', 'PayPal'),
        ('COD', 'Paiement à la livraison'),
        ('BANK_TRANSFER', 'Virement bancaire'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('PROCESSING', 'En traitement'),
        ('COMPLETED', 'Complété'),
        ('FAILED', 'Échoué'),
        ('REFUNDED', 'Remboursé'),
        ('CANCELLED', 'Annulé'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_intent_id = models.CharField(max_length=100, blank=True, null=True)  # Pour Stripe
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment {self.id} - Order {self.order.order_number}"
    
    def mark_as_completed(self, transaction_id=None):
        self.payment_status = 'COMPLETED'
        if transaction_id:
            self.transaction_id = transaction_id
        self.save()
        # Mettre à jour le statut de la commande
        self.order.payment_status = 'PAID'
        self.order.save()
    
    def mark_as_failed(self, error_message=None):
        self.payment_status = 'FAILED'
        if error_message:
            self.metadata['error'] = error_message
        self.save()
    
    def refund(self):
        if self.payment_status == 'COMPLETED':
            self.payment_status = 'REFUNDED'
            self.order.payment_status = 'REFUNDED'
            self.order.save()
            self.save()
            return True
        return False

class PaymentTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('AUTHORIZATION', 'Autorisation'),
        ('CAPTURE', 'Capture'),
        ('REFUND', 'Remboursement'),
        ('VOID', 'Annulation'),
    ]
    
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    response_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.transaction_type} - {self.transaction_id}"