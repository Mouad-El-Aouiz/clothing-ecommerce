from django.urls import path
from . import views

urlpatterns = [
    path('', views.PaymentListView.as_view(), name='payments'),
    path('create/', views.CreatePaymentView.as_view(), name='create-payment'),
    path('<int:pk>/', views.PaymentDetailView.as_view(), name='payment-detail'),
    
    # Stripe integration
    path('create-payment-intent/', views.CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('stripe/webhook/', views.StripeWebhookView.as_view(), name='stripe-webhook'),
]