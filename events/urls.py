from django.urls import path, include
from django.urls import path

from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from .views import VenueViewSet, EventViewSet, RegistrationViewSet, RegistrationExportViewSet, UserViewSet

router = SimpleRouter()
router.register(r'venues', VenueViewSet, basename="venues")
router.register(r'events', EventViewSet, basename="events")
router.register(r'registrations', RegistrationViewSet, basename="registrations")
router.register(r'users', UserViewSet, basename="users")

urlpatterns = (
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/registration_export/", RegistrationExportViewSet.as_view({'get': 'list'}), name="registration_export"),
)
