from rest_framework import viewsets, filters, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .filters import ProductFilter

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True, parent__isnull=True)
    serializer_class = CategorySerializer

    @action(detail=True)
    def products(self, request, pk=None):
        category = self.get_object()
        products = Product.objects.filter(category=category, is_active=True)
        page = self.paginate_queryset(products)
        serializer = ProductSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'  # ← AJOUTEZ CETTE LIGNE ICI
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['price', 'created_at', 'name', 'final_price']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Gérer le tri par final_price
        ordering = self.request.query_params.get('ordering', '')
        if ordering == 'final_price':
            queryset = queryset.extra(
                select={'final_price': "COALESCE(discount_price, price)"}
            ).order_by('final_price')
        elif ordering == '-final_price':
            queryset = queryset.extra(
                select={'final_price': "COALESCE(discount_price, price)"}
            ).order_by('-final_price')
        
        return queryset

    # Vos actions existantes...
    @action(detail=False)
    def featured(self, request):
        featured = self.queryset.filter(is_featured=True)[:8]
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def new_arrivals(self, request):
        new_arrivals = self.queryset.order_by('-created_at')[:12]
        serializer = self.get_serializer(new_arrivals, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def related(self, request, pk=None):
        product = self.get_object()
        related = self.queryset.filter(
            category=product.category,
            gender=product.gender
        ).exclude(id=product.id)[:8]
        serializer = self.get_serializer(related, many=True)
        return Response(serializer.data)
    
    # AJOUTER cette action pour la recherche avancée
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Recherche avancée avec paramètres"""
        queryset = self.get_queryset()
        
        # Recherche par mot-clé
        q = request.query_params.get('q', '')
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q)
            )
        
        # Filtrage par genre
        gender = request.query_params.get('gender')
        if gender:
            queryset = queryset.filter(gender=gender)
        
        # Filtrage par prix
        min_price = request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(
                Q(discount_price__gte=min_price) |
                Q(discount_price__isnull=True, price__gte=min_price)
            )
        
        max_price = request.query_params.get('max_price')
        if max_price:
            queryset = queryset.filter(
                Q(discount_price__lte=max_price) |
                Q(discount_price__isnull=True, price__lte=max_price)
            )
        
        # Pagination
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_gender(self, request):
        """Récupère les produits par genre (M, F, U)"""
        gender = request.query_params.get('gender', '').upper()
        
        if gender not in ['M', 'F', 'U']:
            return Response({'error': 'Genre invalide. Utilisez M, F ou U'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        products = self.queryset.filter(gender=gender)
        page = self.paginate_queryset(products)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)