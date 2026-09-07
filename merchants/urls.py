from django.urls import path

from . import views

app_name = 'merchants'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('store/setup/', views.store_setup_view, name='store_setup'),
    path('foods/', views.food_list_view, name='food_list'),
    path('foods/add/', views.food_create_view, name='food_create'),
    path('foods/<int:pk>/edit/', views.food_edit_view, name='food_edit'),
    path('foods/<int:pk>/delete/', views.food_delete_view, name='food_delete'),
    path('categories/', views.category_manage_view, name='categories'),
    path('orders/', views.order_manage_view, name='orders'),
    path('orders/<int:pk>/', views.order_update_status_view, name='order_detail'),
    path('store/<int:pk>/', views.store_detail_view, name='store_detail'),
]
