from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Model, CASCADE, ForeignKey, ImageField
from django.db.models.enums import TextChoices
from django.db.models.fields import CharField, FloatField, DateTimeField, DecimalField, PositiveIntegerField, TextField, \
    PositiveSmallIntegerField, BooleanField

from base.model import TimeBasedModel, Payment


class Article(Model):
    class ArticleCategory(TextChoices):
        COVID_19 = 'covid_19', 'Covid_19'
        DIET = 'diet', 'Diet'
        FITNESS = 'fitness', 'Fitness'

    title = CharField(max_length=255)
    content = TextField()
    category = CharField(choices=ArticleCategory.choices)
    image = ImageField(upload_to="articles/", blank=True, null=True)
    published_date = DateTimeField(auto_now_add=True)
    amount_of_views = PositiveIntegerField(help_text="Ko'rishlar soni", default=0, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = '-amount_of_views',


class Product(Model):
    class MedicineType(TextChoices):
        PAIN_RELIEF = "pain_relief", "Pain Relief"
        ANTIBIOTICS = "antibiotics", "Antibiotics"
        CARDIOVASCULAR_MEDICATIONS = "cardiovascular_medications", "Cardiovascular Medications"
        ANTI_DIABETIC_MEDICATIONS = "anti_diabetic_medications", "Anti-Diabetic Medications"
        RESPIRATORY_MEDICATIONS = "respiratory_medications", "Respiratory Medications"
        GASTROINTESTINAL_MEDICATIONS = "gastrointestinal_medications", "Gastrointestinal Medications"
        MENTAL_HEALTH_MEDICATIONS = "mental_health_medications", "Mental Health Medications"
        ANTI_INFLAMMATORY_DRUGS = "anti_inflammatory_drugs", "Anti-Inflammatory Drugs"
        VITAMINS_SUPPLEMENTS = "vitamins_supplements", "Vitamins & Supplements"
        ANTIHISTAMINES = "antihistamines", "Antihistamines"

    name = CharField(max_length=255)
    description = TextField(null=True, blank=True)
    price = DecimalField(max_digits=10, decimal_places=2)
    quantity = PositiveIntegerField(default=1)
    image = ImageField(upload_to="medicines/", blank=True, null=True)
    medicine_type = CharField(choices=MedicineType.choices)
    stars = PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], null=True, blank=True,
                                      editable=False)
    wight = CharField(max_length=50, blank=True, null=True, help_text='Masalan 75ml')
    like = BooleanField(default=False, editable=False)
    amount_sales = PositiveIntegerField(help_text="Nechta sotilganligi", editable=False, default=0)
    is_on_sale = BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def star(self):
        return self.stars / 2

    class Meta:
        ordering = '-amount_sales',


class Order(Payment):
    taxes = PositiveSmallIntegerField(default=1)
    location = ForeignKey('shops.Location', on_delete=CASCADE, related_name='orders')
    user = ForeignKey('users.User', on_delete=CASCADE, related_name='orders')

    @property
    def total_price(self):
        total = sum(item.sub_amount for item in self.order_items.all())
        return total


class OrderItem(Model):
    order = ForeignKey(Order, CASCADE, related_name='order_items', null=True)
    product = ForeignKey('shops.Product', CASCADE,
                         related_name='order_items')
    user = ForeignKey('users.User', CASCADE, related_name='order_items')
    quantity = PositiveIntegerField(default=1)

    def __str__(self):
        return f"OrderItem {self.id} - {self.product.name} | User: {self.user.email}"

    @property
    def sub_amount(self):
        return self.quantity * self.product.price


class Cart(TimeBasedModel):
    taxes = PositiveSmallIntegerField(default=1)
    user = ForeignKey('users.User', CASCADE, related_name='user_cart')
    product = ForeignKey('shops.Product', CASCADE)
    quantity = PositiveSmallIntegerField(db_default=1)

    @property
    def sub_amount(self):
        return self.quantity * self.product.price


class Favourite(TimeBasedModel):
    user = ForeignKey('users.User', CASCADE)
    product = ForeignKey('shops.Product', CASCADE)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.email} - {self.product.name} | {self.created_at}"


class Location(TimeBasedModel):
    latitude = FloatField()
    longitude = FloatField()

    def __str__(self):
        return f"{self.latitude},{self.longitude}"
