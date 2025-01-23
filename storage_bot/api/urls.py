from rest_framework.routers import DefaultRouter
from django.urls import path, include
from api.views import (UserViewSet, ConsentViewSet, StorageRateViewSet,
                       PickupLocationViewSet, ContractViewSet)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('consents', ConsentViewSet)
router.register('storage-rates', StorageRateViewSet)
router.register('pickup-locations', PickupLocationViewSet)
router.register('contracts', ContractViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
