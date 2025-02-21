from datetime import datetime

from rest_framework.fields import SerializerMethodField, HiddenField, CurrentUserDefault, IntegerField, CharField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from medical.models import MainCategory, Category, Doctor, BookAppointment


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
    empty_hours = SerializerMethodField(required=False)

    class Meta:
        model = Doctor
        fields = 'full_name', 'specialty', 'distance', 'category', 'stars', 'about', 'arrival_time', 'leave_time', 'empty_hours'

    def get_empty_hours(self, obj):
        return self.context.get('empty_hours', [])


class CreateAppointmentModelSerializer(ModelSerializer):
    doctor = PrimaryKeyRelatedField(queryset=Doctor.objects.all())
    user = HiddenField(default=CurrentUserDefault())
    admin_fee = IntegerField(read_only=True)
    amount = IntegerField(read_only=True)
    appointment_date = CharField(help_text="Soatni 14:20 ko'rinishida kiritiladi")
    total = SerializerMethodField(read_only=True)

    class Meta:
        model = BookAppointment
        fields = "__all__"
        extra_fields = "total",

    def get_total(self, obj: BookAppointment):
        fee = obj.amount + obj.admin_fee
        if obj.additional_discount:
            return fee - fee * obj.additional_discount / 100
        return fee

    def validate(self, attrs):
        attrs = super().validate(attrs)
        appointment_time = attrs.get('appointment_date')
        at_the_moment = datetime.now()
        if appointment_time:
            time_obj = datetime.strptime(appointment_time, '%H:%M')
            attrs['appointment_date'] = datetime(at_the_moment.year, at_the_moment.month, at_the_moment.day,
                                                 hour=time_obj.hour)
        return attrs
