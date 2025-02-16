from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Model, CASCADE, ForeignKey, ImageField
from django.db.models.fields import CharField, FloatField, DateTimeField, DecimalField, PositiveIntegerField, TextField, \
    PositiveSmallIntegerField, BooleanField

from base.model import TimeBasedModel, Payment


class Article(Model):
    title = CharField(max_length=255)  # Maqola nomi
    content = TextField()  # Matn
    category = CharField(max_length=100, choices=[
        ("covid-19", "Covid-19"),
        ("diet", "Diet"),
        ("fitness", "Fitness"),
    ])  # Kategoriya
    image = ImageField(upload_to="articles/", blank=True, null=True)  # Rasm
    published_date = DateTimeField(auto_now_add=True)  # Sana

    def __str__(self):
        return self.title


class Product(Model):
    name = CharField(max_length=255)  # Dori nomi
    description = TextField()  # Tavsif
    price = DecimalField(max_digits=10, decimal_places=2)  # Narx
    stock = PositiveIntegerField(default=0)  # Soni
    image = ImageField(upload_to="medicines/", blank=True, null=True)  # Rasm
    stars = PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], null=True, blank=True)
    size = CharField(max_length=50, blank=True, null=True, help_text='Masalan 75ml')  # O'lchami (masalan, 75ml)
    like = BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def star(self):
        return self.stars / 2


class Order(Payment):
    quantity = PositiveIntegerField(default=1)  # Miqdor
    added_at = DateTimeField(auto_now_add=True)  # Qo‘shilgan vaqt
    taxes = PositiveSmallIntegerField(db_default=1)
    location = ForeignKey('shops.Location', CASCADE, related_name='orders')
    product = ForeignKey('shops.Product', CASCADE, related_name='orders')  # Dori
    user = ForeignKey('users.User', CASCADE, related_name='orders')  # Foydalanuvchi

    def total_price(self):
        return self.product.price * self.quantity + self.taxes

    def __str__(self):
        return f"{self.user.email} - {self.product.name} and {self.taxes}$"


class OrderItem(Model):
    order = ForeignKey(Order, CASCADE, related_name='order_items')
    product = ForeignKey('shops.Product', CASCADE,
                         related_name='order_items')  # Har bir `OrderItem` maxsus mahsulotni bog‘laydi
    user = ForeignKey('users.User', CASCADE, related_name='order_items')
    quantity = PositiveIntegerField(default=1)  # Kamida 1 bo‘lishi lozim

    def __str__(self):
        return f"OrderItem {self.id} - {self.product.name} | User: {self.user.email}"

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
    latitude = FloatField()  # Kenglik
    longitude = FloatField()  # Uzunlik

    def __str__(self):
        return f"{self.latitude},{self.longitude}"
