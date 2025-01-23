from rest_framework import serializers
from core.models import User, Consent, StorageRate, PickupLocation, Contract


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'phone_number']


class ConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consent
        fields = '__all__'


class StorageRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageRate
        fields = '__all__'


class PickupLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickupLocation
        fields = '__all__'


class ContractSerializer(serializers.ModelSerializer):
    storage_rate = StorageRateSerializer(read_only=True)

    class Meta:
        model = Contract
        fields = [
            'id', 'owner_name', 'owner_phone', 'storage_rate',
            'start_date', 'expiration_date', 'qr_code', 'place'
        ]
