from django.contrib import admin
from .models import StorageRate

@admin.register(StorageRate)
class StorageRateAdmin(admin.ModelAdmin):
    list_display = ('volume_category', 'cost_per_day')
    list_editable = ('cost_per_day',)
