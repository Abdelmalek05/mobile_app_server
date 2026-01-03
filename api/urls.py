from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PhoneNumberViewSet, OTPViewSet, ContactViewSet, ProspectViewSet, ActivityViewSet

router = DefaultRouter()
router.register(r'phone-numbers', PhoneNumberViewSet)
router.register(r'otps', OTPViewSet, basename='otps')
router.register(r'contacts', ContactViewSet, basename='contacts')
router.register(r'prospects', ProspectViewSet, basename='prospects')
router.register(r'activities', ActivityViewSet, basename='activities')

urlpatterns = [
    path('', include(router.urls)),
]
