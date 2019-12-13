from rest_framework import routers
router = routers.DefaultRouter()

from accounting.viewsets import CurrencyViewSet, RateViewSet, PaymentMethodViewSet
router.register(r'currency', CurrencyViewSet)
router.register(r'rate', RateViewSet)
router.register(r'payment-method', PaymentMethodViewSet)

from protocol.viewsets import AttendanceViewSet, ClaimViewSet
router.register(r'attendance', AttendanceViewSet)
router.register(r'claim', ClaimViewSet)

from rating.viewsets import PersonViewSet, TeamViewSet, TournamentViewSet
router.register(r'person', PersonViewSet)
router.register(r'team', TeamViewSet)
router.register(r'tournament', TournamentViewSet)

from user_settings.viewsets import UserSettingsViewSet
router.register(r'user-settings', UserSettingsViewSet)

from venue.viewset import LocationViewSet, EventViewSet
router.register(r'location', LocationViewSet)
router.register(r'event', EventViewSet)
