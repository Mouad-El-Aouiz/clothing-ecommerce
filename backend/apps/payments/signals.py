from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Payment

@receiver(post_save, sender=Payment)
def send_payment_confirmation_email(sender, instance, created, **kwargs):
    """Envoie une confirmation de paiement par email"""
    if created and instance.payment_status == 'COMPLETED':
        try:
            subject = f'💳 Paiement confirmé - Commande #{instance.order.order_number}'
            
            context = {
                'payment': instance,
                'order': instance.order,
                'site_name': 'FashionStore',
            }
            
            html_message = render_to_string('emails/payment_confirmation.html', context)
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.order.email],
                html_message=html_message,
                fail_silently=False,
            )
            print(f"📧 Email de paiement envoyé à {instance.order.email}")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'envoi de l'email: {e}")