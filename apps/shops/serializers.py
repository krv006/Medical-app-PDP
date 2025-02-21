from rest_framework.fields import HiddenField, CurrentUserDefault, SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from medical.models import Payment
from shops.models import Article, Product, Cart, Order, Location


class ArticleModelSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class ArticleDetailModelSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = 'image', 'content', 'amount_of_views'


class TopProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = 'image', 'wight', 'price', 'name', 'medicine_type'


class ProductDetailModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class AddToCartModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    sub_total = SerializerMethodField(read_only=True)
    total = SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'

    def get_sub_total(self, obj):
        return self.context.get('sub_total', [])

    def get_total(self, obj: Cart):
        return obj.taxes + int(self.context.get('sub_total', []))


# class CreateOrderItemModelSerializer(ModelSerializer):
#     user = HiddenField(default=CurrentUserDefault())
#
#     class Meta:
#         model = OrderItem
#         fields = '__all__'

class CreateOrderModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Order
        fields = '__all__'


class PaymentMethodsModelSerializer(ModelSerializer):
    class Meta:
        model = Payment
        exclude = 'created_at', 'updated_at'
