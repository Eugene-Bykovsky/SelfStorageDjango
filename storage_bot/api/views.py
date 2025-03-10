from datetime import timedelta

from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from core.models import (User, Consent, StorageRate, PickupLocation, Contract,
                         Call)
from api.serializers import (
    UserSerializer, ConsentSerializer, StorageRateSerializer,
    PickupLocationSerializer, ContractSerializer, CallSerializer
)
from django.utils.timezone import now


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['telegram_id']


class ConsentViewSet(ModelViewSet):
    queryset = Consent.objects.all()
    serializer_class = ConsentSerializer


class StorageRateViewSet(ModelViewSet):
    queryset = StorageRate.objects.all()
    serializer_class = StorageRateSerializer


class PickupLocationViewSet(ModelViewSet):
    queryset = PickupLocation.objects.all()
    serializer_class = PickupLocationSerializer


class ContractViewSet(ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['owner_name']

    @action(detail=False, methods=['get'])
    def expired(self, request):
        """Список просроченных заказов"""
        expired_contracts = self.queryset.filter(
            expiration_date__lt=now().date())
        serializer = self.get_serializer(expired_contracts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def expiring_in_14_days(self, request):
        """Список заказов, у которых срок аренды заканчивается через 14 дней"""
        today = now().date()
        reminder_date = today + timedelta(days=14)
        contracts_in_14_days = self.queryset.filter(expiration_date=reminder_date)
        serializer = self.get_serializer(contracts_in_14_days, many=True)
        return Response(serializer.data)


class CallViewSet(ModelViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer
