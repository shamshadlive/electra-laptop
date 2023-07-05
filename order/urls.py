from django.urls import path

from . import views

urlpatterns = [
    path("place_order/", views.place_order, name="place-order"),
    path("payment/<str:method>/<str:order_number>", views.payment, name="payment"),
    path("order_complete", views.order_complete, name="order_complete"),
    path("cancel/<str:order_id>/", views.order_cancel_user, name="order_cancel_user"),
    
    
    
    
    
]