from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, ProductVariant

class ProductImageInline(admin.TabularInline):
    """Affiche les images dans la page du produit"""
    model = ProductImage
    extra = 1
    fields = ['image', 'is_primary', 'alt_text']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        """Affiche un aperçu de l'image dans l'admin"""
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "Pas d'image"
    image_preview.short_description = 'Aperçu'

class ProductVariantInline(admin.TabularInline):
    """Affiche les variants dans la page du produit"""
    model = ProductVariant
    extra = 1
    fields = ['size', 'color', 'sku', 'stock', 'price_adjustment']
    readonly_fields = ['final_price_display']
    
    def final_price_display(self, obj):
        """Affiche le prix final calculé"""
        if obj.id:
            return f"{obj.final_price} MAD"
        return "-"
    final_price_display.short_description = 'Prix final'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'gender', 'parent', 'is_active', 'created_at']
    list_filter = ['gender', 'is_active', 'parent']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'slug', 'gender', 'parent', 'description')
        }),
        ('Image', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
        ('Statut', {
            'fields': ('is_active',),
        }),
        ('Dates', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('parent')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'gender', 'price_display', 'stock', 'is_featured', 'is_active']
    list_filter = ['category', 'gender', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'is_active']
    inlines = [ProductImageInline, ProductVariantInline]
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'slug', 'category', 'gender', 'description')
        }),
        ('Prix', {
            'fields': ('price', 'discount_price'),
            'classes': ('wide',)
        }),
        ('Stock', {
            'fields': ('stock',),
        }),
        ('Statut', {
            'fields': ('is_active', 'is_featured'),
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def price_display(self, obj):
        """Affiche le prix avec/sans promo"""
        if obj.discount_price:
            return format_html('<span style="color: red;">{} MAD</span> <span style="text-decoration: line-through;">{} MAD</span>', 
                             obj.discount_price, obj.price)
        return f"{obj.price} MAD"
    price_display.short_description = 'Prix'
    
    actions = ['mark_as_featured', 'unmark_as_featured', 'activate', 'deactivate']
    
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
    mark_as_featured.short_description = 'Marquer comme "Vedette"'
    
    def unmark_as_featured(self, request, queryset):
        queryset.update(is_featured=False)
    unmark_as_featured.short_description = 'Retirer des "Vedettes"'
    
    def activate(self, request, queryset):
        queryset.update(is_active=True)
    activate.short_description = 'Activer'
    
    def deactivate(self, request, queryset):
        queryset.update(is_active=False)
    deactivate.short_description = 'Désactiver'

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_preview', 'is_primary', 'alt_text']
    list_filter = ['is_primary']
    search_fields = ['product__name', 'alt_text']
    list_editable = ['is_primary']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "Pas d'image"
    image_preview.short_description = 'Aperçu'

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'color', 'sku', 'stock', 'price_adjustment', 'final_price_display']
    list_filter = ['size', 'color']
    search_fields = ['sku', 'product__name']
    list_editable = ['stock', 'price_adjustment']
    
    def final_price_display(self, obj):
        return f"{obj.final_price} MAD"
    final_price_display.short_description = 'Prix final'