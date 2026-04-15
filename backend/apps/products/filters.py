import django_filters
from django.db.models import Q
from .models import Product, Category

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(method='filter_min_price')
    max_price = django_filters.NumberFilter(method='filter_max_price')
    category = django_filters.CharFilter(method='filter_by_category_including_children')
    gender = django_filters.CharFilter(field_name='gender')
    size = django_filters.CharFilter(field_name='variants__size', lookup_expr='iexact')
    color = django_filters.CharFilter(field_name='variants__color', lookup_expr='iexact')
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Product
        fields = ['category', 'gender', 'is_featured', 'is_active']

    def filter_by_category_including_children(self, queryset, name, value):
        """
        Filtre par catégorie en incluant TOUTES les sous-catégories
        """
        try:
            # Récupère la catégorie par son slug
            category = Category.objects.get(slug=value)
            
            # Récupère les IDs de la catégorie et de TOUS ses enfants
            category_ids = [category.id]
            
            # Ajoute les IDs de toutes les sous-catégories (récursif)
            def get_child_ids(parent):
                for child in parent.children.all():
                    category_ids.append(child.id)
                    get_child_ids(child)  # Pour les sous-sous-catégories
            
            get_child_ids(category)
            
            # Filtre les produits dans toutes ces catégories
            return queryset.filter(category_id__in=category_ids)
            
        except Category.DoesNotExist:
            return queryset.none()

    def filter_min_price(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(discount_price__gte=value) | 
                Q(discount_price__isnull=True, price__gte=value)
            )
        return queryset

    def filter_max_price(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(discount_price__lte=value) | 
                Q(discount_price__isnull=True, price__lte=value)
            )
        return queryset

    def filter_search(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(name__icontains=value) |
                Q(description__icontains=value) |
                Q(category__name__icontains=value)
            )
        return queryset

    @property
    def qs(self):
        return super().qs.filter(is_active=True).distinct()