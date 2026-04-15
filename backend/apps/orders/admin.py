from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'quantity', 'price_at_time', 'total_price_display']
    can_delete = False
    
    def total_price_display(self, obj):
        return f"{obj.total_price} MAD"
    total_price_display.short_description = 'Total'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'payment_status', 'total_amount_display', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email', 'phone']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Informations commande', {
            'fields': ('order_number', 'user', 'status', 'payment_status', 'total_amount')
        }),
        ('Adresse de livraison', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_postal_code', 'shipping_country')
        }),
        ('Contact', {
            'fields': ('phone', 'email', 'notes')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def total_amount_display(self, obj):
        return f"{obj.total_amount} MAD"
    total_amount_display.short_description = 'Total'
    
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled']
    
    def mark_as_processing(self, request, queryset):
        queryset.update(status='PROCESSING')
    mark_as_processing.short_description = 'Marquer comme "En traitement"'
    
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='SHIPPED')
    mark_as_shipped.short_description = 'Marquer comme "Expédiée"'
    
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='DELIVERED')
    mark_as_delivered.short_description = 'Marquer comme "Livrée"'
    
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='CANCELLED')
    mark_as_cancelled.short_description = 'Marquer comme "Annulée"'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'quantity', 'price_at_time', 'total_price_display']
    list_filter = ['order__status']
    search_fields = ['product_name', 'order__order_number']
    readonly_fields = ['total_price_display']
    
    def total_price_display(self, obj):
        return f"{obj.total_price} MAD"
    total_price_display.short_description = 'Total'