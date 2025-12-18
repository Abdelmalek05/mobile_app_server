from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProspectViewSet, ContactViewSet, AuthView

router = DefaultRouter()
router.register(r'prospects', ProspectViewSet)
router.register(r'contacts', ContactViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Auth endpoints
    path('auth/<str:action_type>/', AuthView.as_view(), name='auth_action'),
]
