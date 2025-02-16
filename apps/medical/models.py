from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Model, ImageField, ForeignKey, CASCADE
from django.db.models.fields import CharField, DateTimeField, TextField, FloatField, PositiveSmallIntegerField


class Category:
    name = CharField(max_length=120)

    def __str__(self):
        return f"{self.name}"


class Doctor(Model):
    name = CharField(max_length=255)
    specialty = CharField(max_length=255)  # Mutaxassislik (masalan, kardiolog, psixolog)
    rating = FloatField(default=0.0)  # Reyting (masalan, 4.7)
    distance = CharField(max_length=50, blank=True, null=True)  # Masofa (masalan, 800m away)
    image = ImageField(upload_to="doctors/", blank=True, null=True)  # Profil rasmi
    available_time = CharField(max_length=255, blank=True, null=True)  # Ish vaqti
    stars = PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    category = ForeignKey('medical.Category', CASCADE, related_name='doctors')

    def __str__(self):
        return f"Dr. {self.name} - {self.specialty}"

    @property
    def star(self):
        return self.stars / 2


class HealthArticle(Model):
    title = CharField(max_length=255)  # Maqola sarlavhasi
    content = TextField()  # Maqola matni
    image = ImageField(upload_to="articles/", blank=True, null=True)  # Rasmlar
    published_date = DateTimeField(auto_now_add=True)  # Yaratilgan sanasi

    def __str__(self):
        return self.title


class ServiceCategory(Model):
    name = CharField(max_length=255)  # Xizmat turi (Doctor, Pharmacy, Hospital, Ambulance)
    icon = ImageField(upload_to="icons/", blank=True, null=True)  # Xizmat belgilari uchun rasm

    def __str__(self):
        return self.name
