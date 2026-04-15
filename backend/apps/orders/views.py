from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Order, OrderItem
from .serializers import OrderSerializer, CreateOrderSerializer
from apps.cart.models import Cart
from rest_framework.views import APIView
from datetime import timedelta  


class OrderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class CreateOrderView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateOrderSerializer

    @transaction.atomic
    def post(self, request):
        try:
            print("=== CREATE ORDER DEBUG ===")
            print("User:", request.user)
            print("Request data:", request.data)
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            print("Serializer valid")
            
            cart = Cart.objects.get(user=request.user)
            print(f"Cart items: {cart.items.count()}")
            
            if cart.items.count() == 0:
                return Response({'error': 'Le panier est vide'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                total_amount=cart.total_price,
                **serializer.validated_data
            )
            print(f"Order created: {order.order_number}")
            
            # Create order items
            for cart_item in cart.items.all():
                # 🔧 RÉCUPÉRER L'IMAGE EN UTILISANT LA FONCTION EXISTANTE
                product_image = self._get_product_image(cart_item)
                
                OrderItem.objects.create(
                    order=order,
                    variant=cart_item.variant,
                    quantity=cart_item.quantity,
                    price_at_time=cart_item.variant.final_price,
                    product_name=cart_item.variant.product.name,
                    product_image=product_image  # ← ICI : UTILISER L'IMAGE RÉCUPÉRÉE
                )
                
                # Update stock
                cart_item.variant.stock -= cart_item.quantity
                cart_item.variant.save()
            
            # Clear cart
            cart.items.all().delete()
            
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _get_product_image(self, cart_item):
        """Extrait l'image du produit de façon sécurisée"""
        try:
            primary_image = cart_item.variant.product.images.filter(is_primary=True).first()
            if primary_image:
                return primary_image.image.url
            first_image = cart_item.variant.product.images.first()
            if first_image:
                return first_image.image.url
        except:
            pass
        return ''

class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Commande non trouvée'}, status=status.HTTP_404_NOT_FOUND)
        
        if order.cancel():
            return Response({'message': 'Commande annulée avec succès'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Cette commande ne peut pas être annulée'}, 
                          status=status.HTTP_400_BAD_REQUEST)

class OrderTrackingView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, order_number):
        try:
            order = Order.objects.get(order_number=order_number, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Commande non trouvée'}, status=status.HTTP_404_NOT_FOUND)
        
        tracking_data = {
            'order_number': order.order_number,
            'status': order.get_status_display_fr(),
            'payment_status': order.get_payment_status_display_fr(),
            'created_at': order.created_at,
            'estimated_delivery': order.created_at + timedelta(days=5),
            'timeline': [
                {'status': 'COMMANDÉE', 'date': order.created_at, 'completed': True},
                {'status': 'CONFIRMÉE', 'date': order.created_at, 'completed': order.status != 'PENDING'},
                {'status': 'EXPÉDIÉE', 'date': None, 'completed': order.status in ['SHIPPED', 'DELIVERED']},
                {'status': 'LIVRÉE', 'date': None, 'completed': order.status == 'DELIVERED'},
            ]
        }
        return Response(tracking_data)