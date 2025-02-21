from django.urls import path

from shops.views import ArticleListAPIView, ArticleDetailAPIView, TopProductListAPIView, ProductOnSaleListAPIView, \
    ProductDetailAPIView, AddProductToCartAPIView, PaymentMethodsListAPIView, CreateOrderItemAPIView, CreateOrderAPIView

urlpatterns = [
    path('articles-list', ArticleListAPIView.as_view(), name="articles_list"),
    path('article/<int:pk>', ArticleDetailAPIView.as_view(), name="articles_detail"),
    path('top-product-list', TopProductListAPIView.as_view(), name="top_product_list"),
    path('on-sale-product-list', ProductOnSaleListAPIView.as_view(), name="on_sale_product_list"),
    path('product/<int:pk>', ProductDetailAPIView.as_view(), name="product_detail"),
    path('cart-add', AddProductToCartAPIView.as_view(), name="cart_add"),
    path('create-order-item', CreateOrderItemAPIView.as_view(), name="create_order_item"),
    path('create-order', CreateOrderAPIView.as_view(), name="create_order"),
    path('payment-methods', PaymentMethodsListAPIView.as_view(), name="payment_methods"),
]
