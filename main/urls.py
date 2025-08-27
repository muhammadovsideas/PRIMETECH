from django.urls import path
from main.views import *

urlpatterns = [
    path('category/', CategoryListAPIView.as_view(), name='api-category-list'),
    path('products/', ProductListAPIView.as_view(), name='api-product-list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='api-category-detail'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='api-product-detail'),
    path("carts/", CartListAPIView.as_view(), name="carts-list"),
    path("cart-add/", CartCreateAPIView.as_view(), name="cart-add"),
    path("cart/<int:pk>/delete/", CartDeleteAPIView.as_view(), name="cart-delete"),

]
