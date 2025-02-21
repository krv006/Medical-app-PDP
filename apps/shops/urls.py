from django.urls import path

from shops.views import ArticleListAPIView, ArticleDetailAPIView, TopProductListAPIView, ProductOnSaleListAPIView, \
    ProductDetailAPIView

urlpatterns = [
    path('articles-list', ArticleListAPIView.as_view(), name="articles_list"),
    path('article/<int:pk>', ArticleDetailAPIView.as_view(), name="articles_detail"),
    path('top-product-list', TopProductListAPIView.as_view(), name="top_product_list"),
    path('on-sale-product-list', ProductOnSaleListAPIView.as_view(), name="on_sale_product_list"),
    path('product/<int:pk>', ProductDetailAPIView.as_view(), name="product_detail"),
]
