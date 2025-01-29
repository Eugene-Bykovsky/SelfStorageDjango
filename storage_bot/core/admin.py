from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import (User, StorageRate, Contract, PickupLocation,
                         Call, AdLink)
from datetime import date
from django.utils.safestring import mark_safe
from core.utils import get_clicks_count
from asgiref.sync import async_to_sync


@admin.register(StorageRate)
class StorageRateAdmin(admin.ModelAdmin):
    list_display = ('volume_category', 'cost_per_day')
    list_editable = ('cost_per_day',)


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        'owner_name',
        'storage_rate',
        'place',
        'expiration_date',
        'is_expired'
    )

    # Фильтрация по дате окончания хранения
    list_filter = ('expiration_date',)

    # Подсветка просроченных заказов
    def is_expired(self, obj):
        if obj.expiration_date and obj.expiration_date < date.today():
            return "Просрочен"
        return "В процессе"
    is_expired.admin_order_field = 'expiration_date'
    is_expired.short_description = 'Статус'

    # Настройка цветовой подсветки для просроченных заказов
    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        for field in list_display:
            if field == 'is_expired':
                # Подсветка красным для просроченных
                def colored_expired_status(obj):
                    status = self.is_expired(obj)
                    if obj.expiration_date and obj.expiration_date < date.today():
                        return mark_safe(f'<span style="color: red;">{status}</span>')
                    return status
                colored_expired_status.allow_tags = True
                return [colored_expired_status if field == 'is_expired'
                        else field for field in list_display]
        return list_display


@admin.register(PickupLocation)
class PickupLocationAdmin(admin.ModelAdmin):
    list_display = ('address',)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'name', 'phone_number', 'telegram_id',
                    'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('name', 'phone_number', 'telegram_id',
                       'telegram_username'),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('name', 'phone_number', 'telegram_id',
                       'telegram_username'),
        }),
    )


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ('user', 'call_type', 'requested_at', 'processed',
                    'pre_order')
    list_filter = ('call_type', 'processed')
    search_fields = ('user__username', 'user__telegram_id')


@admin.register(AdLink)
class AdLinkAdmin(admin.ModelAdmin):
    list_display = ('link', 'clicks_count')
    search_fields = ('link',)

    def get_queryset(self, request):
        """
        Обновление статистики переходов при загрузке списка объектов.
        """
        queryset = super().get_queryset(request)

        # Обновляем статистику для всех объектов
        for ad_link in queryset:
            ad_link.clicks_count = async_to_sync(get_clicks_count)(ad_link.link)
            ad_link.save()

        return queryset
