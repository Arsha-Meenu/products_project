from django.urls import path
from . import views
urlpatterns = [
    path('',views.HelloOrderView.as_view(),name = 'hello_orders'),
    path('create-list-orders/',views.CreateListOrderView.as_view(),name = 'create-order'),
    path('details-orders/<int:order_id>/', views.OrderDetailView.as_view(), name='details-orders'),
    path('update-orderstatus/<int:order_id>/', views.UpdateOrderStatusView.as_view(), name='update-orderstatus'),
    path('user/<int:user_id>/orders/', views.UserOrdersView.as_view(), name='user_orders'),
    path('user/<int:user_id>/order/<int:order_id>/', views.UserOrderDetailsView.as_view(), name="user's_specific_order"),

]