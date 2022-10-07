from django.urls import path
from . import views


urlpatterns = [
    path('',views.HelloAuthView.as_view(),name = 'hello_auth'),
    path('register/',views.UserCreationView.as_view(),name = 'user_creation')
]