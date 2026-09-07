from django.urls import path

from . import views

app_name = 'payments'

urlpatterns = [
    path('pay/<int:order_id>/', views.pay_view, name='pay'),
    path('success/<int:payment_id>/', views.payment_success_view, name='success'),
]
