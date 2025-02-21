from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST

from base.pagination import CustomPageNumberPagination
from medical.filters import ProductFilterSet
from medical.models import Payment
from shops.models import Article, Product, Cart, Order, OrderItem
from shops.serializers import ArticleModelSerializer, ArticleDetailModelSerializer, TopProductModelSerializer, \
    ProductDetailModelSerializer, AddToCartModelSerializer, PaymentMethodsModelSerializer, CreateOrderModelSerializer


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


@extend_schema(tags=['Online Pharmacy'], description="""
API for add product to cart and get list
""")
class AddProductToCartAPIView(ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = AddToCartModelSerializer
    permission_classes = IsAuthenticated,

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset().filter(user=self.request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['sub_total'] = sum(c.sub_amount for c in Cart.objects.filter(user=self.request.user))
        return ctx


@extend_schema(tags=['Online Pharmacy'], description="""
API for create order
""")
class CreateOrderAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = CreateOrderModelSerializer
    permission_classes = IsAuthenticated,

    def post(self, request, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        order = Order(latitude=data.get('latitude'),
                      longitude=data.get('longitude'),
                      user=user,
                      taxes=data.get('taxes'),
                      payment_method=data.get('payment_method'))
        order.save()
        order_items = OrderItem.objects.filter(user=user, order_id=None)
        if not order_items:
            return Response('No order items', status=HTTP_400_BAD_REQUEST)
        order_items.update(order=order)
        return Response("Successfully created order")


@extend_schema(tags=['Online Pharmacy'], description="""
API for create order-item
""")
class CreateOrderItemAPIView(GenericAPIView):
    queryset = OrderItem.objects.all()
    permission_classes = IsAuthenticated,

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user_cart = Cart.objects.filter(user=user)
        if user_cart:
            for i in user_cart:
                OrderItem.objects.create(
                    user=user,
                    product=i.product,
                    quantity=i.quantity
                )
            else:
                user_cart.delete()
                return Response({"message": "Successfully created order-items"}, HTTP_204_NO_CONTENT)


@extend_schema(tags=['Online Pharmacy'], description="""
API for get payment methods
""")
class PaymentMethodsListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentMethodsModelSerializer
    permission_classes = IsAuthenticated,
