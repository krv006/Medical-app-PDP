from django.db.models import Model, DateTimeField, CharField, TextChoices


class TimeBasedModel(Model):
    updated_at = DateTimeField(auto_now_add=True)
    created_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Payment(Model):
    class PaymentMethod(TextChoices):
        VISA = 'visa', 'VISA'
        PAYME = 'payme', 'Payme'
        CLICK = 'click', 'Click'
        CASH = 'cash', 'Cash'

    payment_method = CharField(max_length=120, choices=PaymentMethod.choices, default=PaymentMethod.CASH)

    class Meta:
        abstract = True
