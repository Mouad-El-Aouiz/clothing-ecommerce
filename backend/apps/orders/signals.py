from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Order

@receiver(post_save, sender=Order)
def send_order_confirmation_email(sender, instance, created, **kwargs):
    """Envoie un email de confirmation quand une commande est créée"""
    if created:
        try:
            # Préparer le contexte pour le template
            context = {
                'order': instance,
                'site_name': 'FashionStore',
                'site_url': 'http://localhost:5173',
            }
            
            # Rendre le template HTML
            html_message = render_to_string('emails/order_confirmation.html', context)
            plain_message = strip_tags(html_message)
            
            # Envoyer l'email
            send_mail(
                subject=f'✨ Confirmation de votre commande #{instance.order_number}',
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                html_message=html_message,
                fail_silently=False,
            )
            print(f"📧 Email de confirmation envoyé à {instance.email}")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'envoi de l'email: {e}")