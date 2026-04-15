from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db import transaction
from django.conf import settings
from .models import Payment, PaymentTransaction
from .serializers import PaymentSerializer, CreatePaymentSerializer
from apps.orders.models import Order
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# ==================== VUES POUR LES PAIEMENTS ====================

class PaymentListView(generics.ListAPIView):
    """Liste tous les paiements de l'utilisateur connecté"""
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by('-created_at')


class PaymentDetailView(generics.RetrieveAPIView):
    """Affiche les détails d'un paiement spécifique"""
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


class CreatePaymentView(APIView):
    """Crée un nouveau paiement"""
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request):
        serializer = CreatePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        order_id = serializer.validated_data['order_id']
        payment_method = serializer.validated_data['payment_method']
        
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Commande non trouvée'}, status=status.HTTP_404_NOT_FOUND)
        
        # Vérifier que la commande n'est pas déjà payée
        if order.payment_status == 'PAID':
            return Response({'error': 'Cette commande a déjà été payée'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Créer le paiement
        payment = Payment.objects.create(
            user=request.user,
            order=order,
            payment_method=payment_method,
            amount=order.total_amount,
            payment_status='PENDING'
        )
        
        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)


class CreatePaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            amount = request.data.get('amount')
            
            print(f"=== CREATE PAYMENT INTENT ===")
            print(f"User: {request.user.email}")
            print(f"Amount received: {amount}")
            print(f"Stripe API Key configured: {bool(stripe.api_key)}")
            
            if not amount:
                return Response(
                    {'error': 'Le montant est requis'}, 
                    status=400
                )
            
            # Convertir en centimes
            try:
                amount_in_cents = int(float(amount) * 100)
                print(f"Amount in cents: {amount_in_cents}")
            except ValueError:
                return Response(
                    {'error': 'Montant invalide'}, 
                    status=400
                )
            
            # Vérifier que la clé Stripe est configurée
            if not settings.STRIPE_SECRET_KEY:
                return Response(
                    {'error': 'Stripe non configuré. Clé secrète manquante.'}, 
                    status=500
                )
            
            # Créer l'intention de paiement
            intent = stripe.PaymentIntent.create(
                amount=amount_in_cents,
                currency='mad',
                metadata={
                    'user_id': request.user.id,
                    'user_email': request.user.email
                }
            )
            
            print(f"Payment intent created: {intent.id}")
            
            return Response({
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id
            })
            
        except stripe.error.AuthenticationError as e:
            print(f"Stripe auth error: {e}")
            return Response(
                {'error': 'Erreur d\'authentification Stripe. Vérifiez votre clé API.'}, 
                status=500
            )
        except stripe.error.InvalidRequestError as e:
            print(f"Stripe invalid request: {e}")
            return Response(
                {'error': f'Requête invalide: {str(e)}'}, 
                status=400
            )
        except Exception as e:
            print(f"Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                {'error': f'Erreur: {str(e)}'}, 
                status=500
            )


class StripeWebhookView(APIView):
    """Webhook pour recevoir les confirmations Stripe"""
    permission_classes = []  # Pas d'authentification pour les webhooks
    
    def post(self, request):
        payload = request.body
        sig_header = request.headers.get('Stripe-Signature')
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            return Response({'error': 'Invalid payload'}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError:
            return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Traiter l'événement
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            self.handle_successful_payment(payment_intent)
        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            self.handle_failed_payment(payment_intent)
        
        return Response({'status': 'success'})
    
    def handle_successful_payment(self, payment_intent):
        """Gère un paiement réussi"""
        metadata = payment_intent.get('metadata', {})
        user_id = metadata.get('user_id')
        payment_intent_id = payment_intent.get('id')
        
        # Trouver le paiement correspondant
        try:
            payment = Payment.objects.get(payment_intent_id=payment_intent_id)
            payment.mark_as_completed(payment_intent_id)
            print(f"Paiement {payment.id} marqué comme complété")
        except Payment.DoesNotExist:
            print(f"Paiement avec intent {payment_intent_id} non trouvé")
        
    def handle_failed_payment(self, payment_intent):
        """Gère un paiement échoué"""
        # Logique pour gérer les paiements échoués
        pass