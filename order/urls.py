from django.urls import path

from . import views

urlpatterns = [
    path("order_summary/", views.order_summary, name="order-summary"),
    path("place_order/", views.place_order, name="place-order"),
  
    
    path("payment/success/", views.payment_success, name="payment-success"),
    path("payment/failed/", views.payment_failed, name="payment-failed"),
    
    
    path("order_complete", views.order_complete, name="order_complete"),
    path("cancel/<str:order_id>/", views.order_cancel_user, name="order_cancel_user"),
    path("return/<str:order_id>/", views.order_return_user, name="order_return_user"),
    
    
    
    
    
]