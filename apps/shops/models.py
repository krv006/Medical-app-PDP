from django.db import models
from django.contrib.auth.models import User
from django.db.models import Model, OneToOneField, CASCADE, ForeignKey, ImageField
from django.db.models.fields import CharField, FloatField, DateTimeField, DecimalField, PositiveIntegerField, TextField


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


class Medicine(Model):
    name = CharField(max_length=255)  # Dori nomi
    description = TextField()  # Tavsif
    price = DecimalField(max_digits=10, decimal_places=2)  # Narx
    stock = PositiveIntegerField(default=0)  # Ombordagi soni
    image = ImageField(upload_to="medicines/", blank=True, null=True)  # Rasm
    rating = FloatField(default=0.0)  # Reyting
    size = CharField(max_length=50, blank=True, null=True)  # O'lchami (masalan, 75ml)

    def __str__(self):
        return self.name


class Cart(Model):
    user = ForeignKey('users.User', CASCADE)  # Foydalanuvchi
    medicine = ForeignKey('medical.Medicine', CASCADE)  # Dori
    quantity = PositiveIntegerField(default=1)  # Miqdor
    added_at = DateTimeField(auto_now_add=True)  # Qo‘shilgan vaqt

    def total_price(self):
        return self.medicine.price * self.quantity

    def __str__(self):
        return f"{self.user.username} - {self.medicine.name}"


class Order(Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("delivered", "Delivered"),
    ]

    user = ForeignKey('users.User', CASCADE)  # Buyurtmachi
    total_price = DecimalField(max_digits=10, decimal_places=2)  # Jami narx
    status = CharField(max_length=20, choices=STATUS_CHOICES, default="pending")  # Holati
    created_at = DateTimeField(auto_now_add=True)  # Yaralgan sana
    payment_method = CharField(max_length=50, default="Visa")  # To‘lov turi

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.status}"


class Location(Model):
    user = OneToOneField('users.User', CASCADE)  # Foydalanuvchi
    address = CharField(max_length=255)  # Manzil
    latitude = FloatField()  # Kenglik
    longitude = FloatField()  # Uzunlik

    def __str__(self):
        return f"{self.user.username} - {self.address}"
