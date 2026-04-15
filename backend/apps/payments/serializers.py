from rest_framework import serializers
from .models import Payment, PaymentTransaction

class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = ['id', 'transaction_type', 'transaction_id', 'amount', 'status', 'created_at']

class PaymentSerializer(serializers.ModelSerializer):
    transactions = PaymentTransactionSerializer(many=True, read_only=True)
    payment_method_display = serializers.SerializerMethodField()
    payment_status_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Payment
        fields = ['id', 'order', 'payment_method', 'payment_method_display', 
                  'payment_status', 'payment_status_display', 'amount', 
                  'transaction_id', 'transactions', 'created_at']
    
    def get_payment_method_display(self, obj):
        return dict(Payment.PAYMENT_METHOD_CHOICES).get(obj.payment_method, obj.payment_method)
    
    def get_payment_status_display(self, obj):
        return dict(Payment.PAYMENT_STATUS_CHOICES).get(obj.payment_status, obj.payment_status)

class CreatePaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(choices=Payment.PAYMENT_METHOD_CHOICES)
    
    def validate_order_id(self, value):
        from apps.orders.models import Order
        try:
            order = Order.objects.get(id=value)
            if order.payment_status == 'PAID':
                raise serializers.ValidationError("Cette commande a déjà été payée")
            return value
        except Order.DoesNotExist:
            raise serializers.ValidationError("Commande non trouvée")