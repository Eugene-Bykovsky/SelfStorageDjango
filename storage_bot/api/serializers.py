from rest_framework import serializers
from core.models import (User, Consent, StorageRate, PickupLocation, Contract,
                         Call)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'phone_number', 'telegram_id',
                  'telegram_username', 'is_active']

    def create(self, validated_data):
        telegram_id = validated_data.get('telegram_id')
        user = User.objects.filter(telegram_id=telegram_id).first()
        if not user:
            user = super().create(validated_data)
        return user


class ConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consent
        fields = '__all__'

    def create(self, validated_data):
        # Извлекаем пользователя из данных
        user = validated_data.get('user')

        # Убеждаемся, что пользователь существует
        if not User.objects.filter(id=user.id).exists():
            raise serializers.ValidationError("Пользователь не найден.")

        # Создаём согласие
        consent = super().create(validated_data)

        # Если согласие дано, активируем пользователя
        if consent.consent_given:
            user.is_active = True
            user.save()

        return consent


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
    place_address = serializers.CharField(source='place.address',
                                          read_only=True)

    class Meta:
        model = Contract
        fields = [
            'id', 'owner_name', 'storage_rate',
            'start_date', 'expiration_date', 'qr_code',
            'place', 'place_address', 'content'
        ]


class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = '__all__'
