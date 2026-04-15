from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderListView.as_view(), name='orders'),
    path('create/', views.CreateOrderView.as_view(), name='create-order'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('<int:pk>/cancel/', views.CancelOrderView.as_view(), name='cancel-order'),
    path('track/<str:order_number>/', views.OrderTrackingView.as_view(), name='track-order'),
]