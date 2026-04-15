from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Wishlist

class UserProfileInline(admin.StackedInline):
    """Affiche le profil dans la page de l'utilisateur"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profil'

class CustomUserAdmin(BaseUserAdmin):
    """Personnalise l'affichage des utilisateurs dans l'admin"""
    inlines = [UserProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'country', 'created_at']
    list_filter = ['country', 'city']
    search_fields = ['user__username', 'user__email', 'phone', 'address']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Informations utilisateur', {
            'fields': ('user',)
        }),
        ('Coordonnées', {
            'fields': ('phone', 'address', 'city', 'postal_code', 'country')
        }),
        ('Avatar', {
            'fields': ('avatar',)
        }),
        ('Dates', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__name']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'product')

# Réenregistrer User avec la configuration personnalisée
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)