from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('add/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('update/<int:pk>/', views.UpdateCartItemView.as_view(), name='update-cart-item'),
    path('remove/<int:pk>/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('clear/', views.ClearCartView.as_view(), name='clear-cart'),  # AJOUTÉ
]