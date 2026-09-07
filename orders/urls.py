from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:food_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/update/<int:food_id>/', views.update_cart_view, name='update_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('my-orders/', views.my_orders_view, name='my_orders'),
    path('<int:pk>/', views.order_detail_view, name='order_detail'),
]
