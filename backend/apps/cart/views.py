from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from apps.products.models import ProductVariant
from rest_framework.views import APIView

class CartView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

class AddToCartView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def post(self, request):
        try:
            cart, created = Cart.objects.get_or_create(user=request.user)
            variant_id = request.data.get('variant_id')
            quantity = int(request.data.get('quantity', 1))

            if not variant_id:
                return Response({'error': 'variant_id est requis'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                variant = ProductVariant.objects.get(id=variant_id)
            except ProductVariant.DoesNotExist:
                return Response({'error': 'Variante non trouvée'}, status=status.HTTP_404_NOT_FOUND)

            # Vérifier le stock
            if quantity > variant.stock:
                return Response({'error': f'Stock insuffisant. Maximum: {variant.stock}'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                variant=variant,
                defaults={'quantity': quantity}
            )
            
            if not created:
                new_quantity = cart_item.quantity + quantity
                if new_quantity > variant.stock:
                    return Response({'error': f'Stock insuffisant. Maximum: {variant.stock}'}, 
                                  status=status.HTTP_400_BAD_REQUEST)
                cart_item.quantity = new_quantity
                cart_item.save()
            
            # Recharger le panier avec tous les items
            cart.refresh_from_db()
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"Error in AddToCartView: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateCartItemView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def update(self, request, *args, **kwargs):
        cart_item = self.get_object()
        quantity = int(request.data.get('quantity', cart_item.quantity))
        
        # Validation
        if quantity < 0:
            return Response({'error': 'La quantité ne peut pas être négative'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Vérifier le stock
        if quantity > cart_item.variant.stock:
            return Response({
                'error': f'Stock insuffisant. Maximum disponible: {cart_item.variant.stock}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if quantity == 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()
        
        cart = Cart.objects.get(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class RemoveFromCartView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def delete(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart_item.delete()
        cart = Cart.objects.get(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        cart = Cart.objects.get(user=request.user)
        cart.items.all().delete()
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)