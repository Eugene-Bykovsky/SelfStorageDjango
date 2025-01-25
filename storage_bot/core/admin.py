from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import (User, StorageRate, Contract, PickupLocation,
                         Call)


@admin.register(StorageRate)
class StorageRateAdmin(admin.ModelAdmin):
    list_display = ('volume_category', 'cost_per_day')
    list_editable = ('cost_per_day',)


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        'owner_name',
        'owner_phone',
        'storage_rate',
        'place',
        'expiration_date'
    )


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
    list_display = ('user', 'call_type', 'requested_at', 'processed')
    list_filter = ('call_type', 'processed')
    search_fields = ('user__username', 'user__telegram_id')
