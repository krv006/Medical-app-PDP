from rest_framework.serializers import ModelSerializer

from shops.models import Article, Product


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
