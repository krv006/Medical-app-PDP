from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.safestring import mark_safe

from shops.models import Article, Product


@admin.register(Article)
class ArticleModelAdmin(ModelAdmin):
    list_display = 'title', 'category', 'amount_of_views_designed', 'designed_image'

    @admin.display(description="👁Ko'rishlar soni")
    def amount_of_views_designed(self, obj: Article):
        views = obj.amount_of_views
        if views is not None:
            return views

    @admin.display(description="Rasmi")
    def designed_image(self, obj: Article):
        image = obj.image
        if image:
            return mark_safe(f"<img src={image.url} alt='img' width='60px' height='60px'")
        return 'Rasm mavjud emas'


@admin.register(Product)
class ProductModelAdmin(ModelAdmin):
    list_display = 'name', 'price', 'quantity', 'designed_image', 'medicine_type', 'wight', 'stars', 'amount_sales'

    @admin.display(description="Image")
    def designed_image(self, obj: Product):
        image = obj.image
        if image:
            return mark_safe(f"<img src={image.url} alt='img' width='60px' height='60px'")
        return 'None image'
