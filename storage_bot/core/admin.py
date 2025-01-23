from django.contrib import admin
from core.models import StorageRate, Contract, PickupLocation


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

    
