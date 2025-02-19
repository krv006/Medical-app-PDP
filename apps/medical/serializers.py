from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from medical.models import MainCategory, Category, Doctor


class MainCategoriesModelSerializer(ModelSerializer):
    class Meta:
        model = MainCategory
        exclude = ()


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        exclude = "created_at", "updated_at"


class DoctorsModelSerializer(ModelSerializer):
    category = CategoryModelSerializer()

    class Meta:
        model = Doctor
        fields = 'full_name', 'specialty', 'distance', 'category', 'stars'


class RecentDoctorsModelSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = 'id',


class DoctorDetailModelSerializer(ModelSerializer):
    category = PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Doctor
        fields = 'full_name', 'specialty', 'distance', 'category', 'stars', 'about', 'arrival_time', 'leave_time'
