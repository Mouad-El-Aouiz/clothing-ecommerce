from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'quantity', 'price_at_time', 'total_price', 'product_image']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.SerializerMethodField()
    payment_status_display = serializers.SerializerMethodField()
    created_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'status', 'status_display', 'payment_status', 
                  'payment_status_display', 'total_amount', 'shipping_address', 
                  'shipping_city', 'shipping_postal_code', 'shipping_country', 
                  'phone', 'email', 'notes', 'items', 'created_at', 'created_at_formatted']

    def get_status_display(self, obj):
        return obj.get_status_display_fr()
    
    def get_payment_status_display(self, obj):
        return obj.get_payment_status_display_fr()
    
    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime('%d/%m/%Y à %H:%M')


class CreateOrderSerializer(serializers.Serializer):
    shipping_address = serializers.CharField(required=True)
    shipping_city = serializers.CharField(required=True)
    shipping_postal_code = serializers.CharField(required=True)
    shipping_country = serializers.CharField(default='Maroc')
    phone = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate_phone(self, value):
        """Validation du numéro de téléphone (formats marocains)"""
        import re
        # Nettoie le numéro
        value = re.sub(r'[\s\-\(\)]', '', value)
        
        # Format +212XXXXXXXXX
        if re.match(r'^\+212[0-9]{9}$', value):
            return value
        
        # Format 0XXXXXXXXX
        if re.match(r'^0[5-7][0-9]{8}$', value):
            return value
        
        # Format sans indicatif 6XXXXXXXX (9 chiffres)
        if re.match(r'^[6-7][0-9]{8}$', value):
            return '0' + value
        
        raise serializers.ValidationError('Numéro de téléphone invalide (ex: 0612345678 ou +212612345678)')
    
    def validate_shipping_postal_code(self, value):
        import re
        if not re.match(r'^[0-9]{5}$', value):
            raise serializers.ValidationError('Code postal invalide (5 chiffres)')
        return value