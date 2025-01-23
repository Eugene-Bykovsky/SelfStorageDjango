from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)


class Consent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    consent_text = models.TextField(help_text="Я даю согласие на обработку моих персональных данных")
    consent_file = models.FileField(
        upload_to='consents/', blank=True, null=True, help_text="PDF файл для согласия"
    )
    consent_given = models.BooleanField(default=False, help_text="Пользователь дал согласие")
    given_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Согласие от {self.user.email or self.user.username} датируемое {self.given_at}"
    

class StorageRate(models.Model):
    VOLUME_CHOICES = [
        ('small', 'До 1 м³'),
        ('medium', 'От 1 до 5 м³'),
        ('large', 'Больше 5 м³'),
    ]

    volume_category = models.CharField(
        max_length=10, choices=VOLUME_CHOICES, unique=True, verbose_name="Категория объёма"
    )
    cost_per_day = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Стоимость (₽/день)"
    )

    class Meta:
        verbose_name = "Тариф хранения"
        verbose_name_plural = "Тарифы хранения"

    def __str__(self):
        return f"{self.get_volume_category_display()} - {self.cost_per_day} ₽/день"
    

class PickupLocation(models.Model):
    address = models.CharField(verbose_name="адрес", max_length=200, blank=True)
    latitude = models.FloatField(verbose_name="широта", null=True)
    longitude = models.FloatField(verbose_name="долгота", null=True)

    def __str__(self):
        return f"Точка самовывоза: {self.address}"
    

class Contract(models.Model):
    owner_name = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='имя владельца', related_name='owner_name_contracts'
        )
    owner_phone = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='телефон владельца', related_name='owner_phone_contracts'
        )
    storage_rate = models.ForeignKey(
        StorageRate, on_delete=models.CASCADE, verbose_name='тариф заказа', related_name='contracts'
        )
    start_date = models.DateField(null=True, verbose_name='дата начала хранения')
    expiration_date = models.DateField(null=True, verbose_name='дата окончания хранения')
    qr_code = models.BooleanField(default=False, verbose_name='был ли запрошен QR-код')
    place = models.ForeignKey(
        PickupLocation, on_delete=models.CASCADE, verbose_name='место хранения', related_name='contracts'
        )
    
    def __str__(self):
        return f'Заказ от {self.owner_name}, дата конца хранения: {self.expiration_date}'

