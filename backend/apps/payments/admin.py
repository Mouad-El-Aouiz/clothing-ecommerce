from django.contrib import admin
from django.utils.html import format_html
from .models import Payment, PaymentTransaction

class PaymentTransactionInline(admin.TabularInline):
    model = PaymentTransaction
    extra = 0
    readonly_fields = ['transaction_type', 'transaction_id', 'amount', 'status', 'created_at']
    can_delete = False

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'user', 'payment_method', 'payment_status', 'amount_display', 'created_at']
    list_filter = ['payment_method', 'payment_status', 'created_at']
    search_fields = ['order__order_number', 'user__username', 'transaction_id', 'payment_intent_id']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [PaymentTransactionInline]
    
    fieldsets = (
        ('Informations paiement', {
            'fields': ('order', 'user', 'payment_method', 'payment_status', 'amount')
        }),
        ('Détails transaction', {
            'fields': ('transaction_id', 'payment_intent_id', 'metadata')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def amount_display(self, obj):
        return f"{obj.amount} MAD"
    amount_display.short_description = 'Montant'
    
    actions = ['mark_as_completed', 'mark_as_refunded', 'mark_as_failed']
    
    def mark_as_completed(self, request, queryset):
        for payment in queryset:
            payment.mark_as_completed()
    mark_as_completed.short_description = 'Marquer comme "Complété"'
    
    def mark_as_refunded(self, request, queryset):
        for payment in queryset:
            payment.refund()
    mark_as_refunded.short_description = 'Marquer comme "Remboursé"'
    
    def mark_as_failed(self, request, queryset):
        queryset.update(payment_status='FAILED')
    mark_as_failed.short_description = 'Marquer comme "Échoué"'

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment', 'transaction_type', 'transaction_id', 'amount_display', 'status', 'created_at']
    list_filter = ['transaction_type', 'status']
    search_fields = ['transaction_id', 'payment__order__order_number']
    readonly_fields = ['created_at']
    
    def amount_display(self, obj):
        return f"{obj.amount} MAD"
    amount_display.short_description = 'Montant'