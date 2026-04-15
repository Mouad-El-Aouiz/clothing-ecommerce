from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['variant', 'quantity', 'total_price_display']
    can_delete = True
    
    def total_price_display(self, obj):
        return f"{obj.total_price} MAD"
    total_price_display.short_description = 'Total'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_items_display', 'total_price_display', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'total_items_display', 'total_price_display']
    inlines = [CartItemInline]
    
    def total_items_display(self, obj):
        return obj.total_items
    total_items_display.short_description = 'Nombre d\'articles'
    
    def total_price_display(self, obj):
        return f"{obj.total_price} MAD"
    total_price_display.short_description = 'Total'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'variant', 'quantity', 'total_price_display']
    list_filter = ['cart__user']
    search_fields = ['variant__product__name', 'variant__sku', 'cart__user__username']
    readonly_fields = ['total_price_display']
    
    def total_price_display(self, obj):
        return f"{obj.total_price} MAD"
    total_price_display.short_description = 'Total'