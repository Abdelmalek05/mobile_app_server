from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PhoneNumberViewSet, OTPViewSet, ContactViewSet, ProspectViewSet

router = DefaultRouter()
router.register(r'phone-numbers', PhoneNumberViewSet)
router.register(r'otps', OTPViewSet, basename='otps')
router.register(r'contacts', ContactViewSet)
router.register(r'prospects', ProspectViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
