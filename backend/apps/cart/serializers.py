from rest_framework import serializers
from .models import Cart, CartItem
from apps.products.serializers import ProductVariantSerializer

class CartItemSerializer(serializers.ModelSerializer):
    variant_details = ProductVariantSerializer(source='variant', read_only=True)
    product_name = serializers.CharField(source='variant.product.name', read_only=True)
    product_slug = serializers.CharField(source='variant.product.slug', read_only=True)  # AJOUTÉ
    product_id = serializers.IntegerField(source='variant.product.id', read_only=True)   # AJOUTÉ
    product_image = serializers.SerializerMethodField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    unit_price = serializers.DecimalField(source='variant.final_price', read_only=True, max_digits=10, decimal_places=2)  # AJOUTÉ

    class Meta:
        model = CartItem
        fields = ['id', 'variant', 'variant_details', 'quantity', 'total_price', 
                  'unit_price', 'product_name', 'product_slug', 'product_id', 'product_image']

    def get_product_image(self, obj):
        try:
            primary = obj.variant.product.images.filter(is_primary=True).first()
            if primary:
                return primary.image.url
            first = obj.variant.product.images.first()
            if first:
                return first.image.url
        except:
            pass
        return None

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_items', 'total_price']