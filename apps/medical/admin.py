from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.safestring import mark_safe

from medical.models import MainCategory, Category, Doctor, BookAppointment, Payment


@admin.register(MainCategory)
class MainCategoryModelAdmin(ModelAdmin):
    list_display = "name", "cat_image"

    @admin.display(description="Category image")
    def cat_image(self, obj: MainCategory):
        icon = obj.icon
        if icon:
            return mark_safe(f"<img src={icon.url} alt='img' width='60px' height='60px'")
        return "None icon"


@admin.register(Category)
class CategoryModelAdmin(ModelAdmin):
    list_display = "name", "cat_image"

    @admin.display(description="Category image")
    def cat_image(self, obj: MainCategory):
        icon = obj.icon
        if icon:
            return mark_safe(f"<img src={icon.url} alt='img' width='60px' height='60px'")
        return "None icon"


@admin.register(Doctor)
class DoctorModelAdmin(ModelAdmin):
    list_display = 'full_name', 'specialty', 'about', 'category', 'doctor_photo', 'stars'

    @admin.display(description='Doctor Image')
    def doctor_photo(self, obj: Doctor):
        photo = obj.image
        if photo:
            return mark_safe(f"<img src={photo.url} alt='img' width='60px' height='60px'")


@admin.register(BookAppointment)
class BookAppointmentModelAdmin(ModelAdmin):
    pass


@admin.register(Payment)
class PaymentModelAdmin(ModelAdmin):
    list_display = 'payment_method', 'icon_image'

    @admin.display(description="Icon")
    def icon_image(self, obj: Payment):
        icon = obj.method_icon
        if icon:
            return mark_safe(f"<img src={icon.url} alt='img' width='60px' height='60px'")
