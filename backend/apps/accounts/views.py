# apps/accounts/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .serializers import RegisterSerializer, UserProfileSerializer, WishlistSerializer, ChangePasswordSerializer
from .models import Wishlist, EmailConfirmationToken
from apps.products.models import Product

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        
        # Créer un token de confirmation (valable 24h)
        token = EmailConfirmationToken.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(days=1)
        )
        
        # Envoyer l'email de confirmation
        self.send_confirmation_email(user, token)
        
    def send_confirmation_email(self, user, token):
        """Envoie l'email de confirmation avec lien d'activation"""
        subject = "Confirmez votre inscription - FashionStore"
        
        # Lien de confirmation
        frontend_url = settings.FRONTEND_URL or "http://localhost:5173"
        confirmation_link = f"{frontend_url}/confirm-email/{token.token}/"
        
        # Construction du message HTML
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Confirmation d'inscription</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #4f46e5; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; background: #4f46e5; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; margin: 20px 0; }}
                .footer {{ text-align: center; font-size: 12px; color: #6b7280; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>✨ FashionStore ✨</h1>
                </div>
                <div class="content">
                    <p>Bonjour <strong>{user.username}</strong>,</p>
                    <p>Merci de vous être inscrit sur FashionStore !</p>
                    <p>Pour finaliser votre inscription et activer votre compte, veuillez cliquer sur le bouton ci-dessous :</p>
                    <div style="text-align: center;">
                        <a href="{confirmation_link}" style="background: #4f46e5; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; display: inline-block;">Activer mon compte</a>
                    </div>
                    <p style="margin-top: 20px;">Ce lien expire dans 24 heures.</p>
                    <p>Si vous n'êtes pas à l'origine de cette inscription, ignorez simplement cet email.</p>
                </div>
                <div class="footer">
                    <p>© 2024 FashionStore - Tous droits réservés</p>
                    <p>{settings.DEFAULT_FROM_EMAIL}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        plain_message = f"""
        Bonjour {user.username},
        
        Merci de vous être inscrit sur FashionStore !
        
        Pour finaliser votre inscription et activer votre compte, veuillez cliquer sur le lien ci-dessous :
        
        {confirmation_link}
        
        Ce lien expire dans 24 heures.
        
        Si vous n'êtes pas à l'origine de cette inscription, ignorez simplement cet email.
        
        Cordialement,
        L'équipe FashionStore
        """
        
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            print(f"📧 Email de confirmation envoyé à {user.email} via {settings.EMAIL_HOST_USER}")
        except Exception as e:
            print(f"❌ Erreur envoi email: {e}")


class ConfirmEmailView(APIView):
    """Vue pour confirmer l'email et activer le compte"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, token):
        try:
            confirmation_token = EmailConfirmationToken.objects.get(token=token)
            
            if not confirmation_token.is_valid():
                return Response({
                    'error': 'Ce lien de confirmation a expiré. Veuillez vous réinscrire.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Activer le compte
            user = confirmation_token.user
            user.is_active = True
            user.save()
            
            # Marquer l'email comme vérifié
            user.profile.email_verified = True
            user.profile.save()
            
            # Supprimer le token
            confirmation_token.delete()
            
            return Response({
                'message': 'Votre compte a été activé avec succès ! Vous pouvez maintenant vous connecter.'
            }, status=status.HTTP_200_OK)
            
        except EmailConfirmationToken.DoesNotExist:
            return Response({
                'error': 'Lien de confirmation invalide.'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user.profile

class WishlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wishlist = Wishlist.objects.filter(user=request.user).select_related('product')
        serializer = WishlistSerializer(wishlist, many=True)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get('product_id')
        
        if not product_id:
            return Response({'error': 'product_id est requis'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=request.user,
                product=product
            )
            if created:
                return Response({
                    'message': 'Produit ajouté aux favoris',
                    'product_id': product_id
                }, status=status.HTTP_201_CREATED)
            return Response({
                'message': 'Produit déjà dans les favoris'
            }, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Produit non trouvé'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, product_id=None):
        product_id = product_id or request.data.get('product_id')
        
        if not product_id:
            return Response({'error': 'product_id est requis'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            wishlist_item = Wishlist.objects.get(user=request.user, product_id=product_id)
            wishlist_item.delete()
            return Response({'message': 'Produit retiré des favoris'}, status=status.HTTP_200_OK)
        except Wishlist.DoesNotExist:
            return Response({'error': 'Produit non trouvé dans les favoris'}, status=status.HTTP_404_NOT_FOUND)

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        
        if not user.check_password(old_password):
            return Response({'error': 'Ancien mot de passe incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        
        return Response({'message': 'Mot de passe changé avec succès'}, status=status.HTTP_200_OK)