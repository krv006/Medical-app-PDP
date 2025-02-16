from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Model, ImageField, ForeignKey, CASCADE, SET_NULL
from django.db.models.fields import CharField, TextField, PositiveSmallIntegerField

from base.model import TimeBasedModel, Payment


class Category(TimeBasedModel):
    name = CharField(max_length=120)
    icon = ImageField(upload_to="icons/", blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Doctor(TimeBasedModel):
    full_name = CharField(max_length=255)
    specialty = CharField(max_length=255)  # Mutaxassislik (masalan, kardiolog, psixolog)
    distance = CharField(max_length=50, blank=True, null=True)  # Masofa (masalan, 800m away)
    about = TextField(null=True, blank=True)
    image = ImageField(upload_to="doctors/", blank=True, null=True)  # Profil rasmi
    arrival_time = CharField(max_length=255, help_text='ish vaqtingizni kiriting kelish vaqti')  # Ish kelish
    leave_time = CharField(max_length=255, help_text='ish vaqtingizni kiriting ketish vaqti')  # Ish ketish
    stars = PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], null=True, blank=True)
    category = ForeignKey('medical.Category', CASCADE, related_name='doctors')
    user = ForeignKey('users.User', SET_NULL, related_name='doctors', null=True, blank=True)

    def __str__(self):
        return f"Dr. {self.full_name} - {self.specialty}"

    @property
    def star(self):
        return self.stars / 2


class BookAppointment(Payment):
    amount = PositiveSmallIntegerField(db_default=60)  # 60$ per hours
    admin_fee = PositiveSmallIntegerField(db_default=1)
    doctor = ForeignKey('medical.Doctor', CASCADE, related_name='book_appointments')
    user = ForeignKey('users.User', CASCADE, related_name='book_appointments')

    def __str__(self):
        return f"Admin Fee {self.admin_fee}$"

# class HealthArticle(Model):
#     title = CharField(max_length=255)  # Maqola sarlavhasi
#     content = TextField()  # Maqola matni
#     image = ImageField(upload_to="articles/", blank=True, null=True)  # Rasmlar
#     published_date = DateTimeField(auto_now_add=True)  # Yaratilgan sanasi
#
#     def __str__(self):
#         return self.title

