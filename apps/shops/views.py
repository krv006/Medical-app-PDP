from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from base.pagination import CustomPageNumberPagination
from medical.filters import ProductFilterSet
from shops.models import Article, Product
from shops.serializers import ArticleModelSerializer, ArticleDetailModelSerializer, TopProductModelSerializer, \
    ProductDetailModelSerializer


@extend_schema(tags=['Online Pharmacy'], description="""
API for get articles list
""")
class ArticleListAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer
    permission_classes = AllowAny,
    filter_backends = SearchFilter, DjangoFilterBackend
    search_fields = 'title', 'content'


@extend_schema(tags=['Online Pharmacy'], description="""
API for get articles detail
""")
class ArticleDetailAPIView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailModelSerializer

    def get_object(self):
        obj = super().get_object()
        obj.amount_of_views += 1
        obj.save()
        return obj


@extend_schema(tags=['Online Pharmacy'], description="""
API for get products list
""")
class TopProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = TopProductModelSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = SearchFilter, DjangoFilterBackend
    search_fields = 'medicine_type', 'name'
    filterset_class = ProductFilterSet


@extend_schema(tags=['Online Pharmacy'], description="""
API for get products list
""")
class ProductOnSaleListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = TopProductModelSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = SearchFilter, DjangoFilterBackend
    search_fields = 'medicine_type', 'name'
    filterset_class = ProductFilterSet

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_on_sale=True)


@extend_schema(tags=['Online Pharmacy'], description="""
API for get product detail
""")
class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailModelSerializer

