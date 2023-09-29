from rest_framework.test import APITestCase
from django.test import TestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from django.utils import timezone
from datetime import timedelta

from events.serializers import UserSerializer
from events.models import User, Event, Venue, Registration
from events.serializers import UserSerializer, EventSerializer, VenueSerializer, RegistrationSerializer, RegistrationExportSerializer
from events.utils import CATEGORY_CHOICES

class UserSerializerTest(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_serializer(self):
        serializer = UserSerializer(instance=self.user)
        keys = ["username", "password", "email"]

        for key in keys:
            self.assertIn(key, serializer.data)


class EventSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.venue = Venue.objects.create(
            name='Test Venue',
            capacity=100,
            amenities='Amenity 1, Amenity 2'
        )

    def test_event_serializer_create(self):

        data = {
            'title': 'Test Event',
            'description': 'Test Description',
            'date': (timezone.now().date() + timedelta(days=1)).isoformat(),
            'time': '14:00:00',
            'location': self.venue.id,
            'capacity': 50,
            'category': CATEGORY_CHOICES[0][0],
        }

        request = self.factory.post('/events/', data, format='json')
        request.user = self.user

        serializer = EventSerializer(data=data, context={'request': request})
        self.assertTrue(serializer.is_valid())
        event = serializer.save(created_by=self.user)

        self.assertEqual(event.title, 'Test Event')
        self.assertEqual(event.description, 'Test Description')
        self.assertEqual(event.location, self.venue)
        self.assertEqual(event.capacity, 50)
        self.assertEqual(event.category, CATEGORY_CHOICES[0][0])
        self.assertEqual(event.created_by, self.user)

    def test_event_serializer_validate_date(self):
        past_date = (timezone.now().date() - timedelta(days=1)).isoformat()
        data = {
            'title': 'Test Event',
            'description': 'Test Description',
            'date': past_date,
            'time': '14:00:00',
            'location': self.venue.id,
            'capacity': 50,
            'category': CATEGORY_CHOICES[0][0],
        }
        request = self.factory.post('/events/', data, format='json')
        request.user = self.user

        serializer = EventSerializer(data=data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('date', serializer.errors)


class VenueSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.venue = Venue.objects.create(
            name='Test Venue',
            capacity=100,
            amenities='Amenity 1, Amenity 2'
        )

    def test_venue_serializer(self):
        serializer = VenueSerializer(instance=self.venue)

        expected_data = {
            'id': self.venue.id,
            'name': 'Test Venue',
            'capacity': 100,
            'amenities': 'Amenity 1, Amenity 2',
            'available_dates': ['No bookings'],
            'events': [],
        }
        for key in expected_data:
            self.assertEqual(expected_data[key], serializer.data[key])


class RegistrationSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.venue = Venue.objects.create(
            name='Test Venue',
            capacity=100,
            amenities='Amenity 1, Amenity 2'
        )
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            date=timezone.now().date() + timedelta(days=1),
            time=timezone.now().time(),
            location=self.venue,
            capacity=50,
            category=CATEGORY_CHOICES[0][0],
            created_by=self.user
        )

    def test_registration_serializer_create(self):
        data = {
            'user': self.user.id,
            'event': self.event.id,
            'accepted': False,
        }

        request = self.factory.post('/registrations/', data, format='json')
        request.user = self.user
        serializer = RegistrationSerializer(data=data, context={'request': request})

        self.assertTrue(serializer.is_valid())
        registration = serializer.save()

        self.assertEqual(registration.user, self.user)
        self.assertEqual(registration.event, self.event)
        self.assertFalse(registration.accepted)


class RegistrationExportSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.venue = Venue.objects.create(
            name='Test Venue',
            capacity=100,
            amenities='Amenity 1, Amenity 2'
        )
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            date=timezone.now().date() + timedelta(days=1),
            time=timezone.now().time(),
            location=self.venue,
            capacity=50,
            category='YourCategoryChoiceHere',  # Replace with your category choice
            created_by=self.user
        )
        self.registration = Registration.objects.create(
            user=self.user,
            event=self.event,
            registration_date=timezone.now(),
            accepted=True
        )

    def test_registration_export_serializer(self):
        serializer = RegistrationExportSerializer(instance=self.registration)

        expected_data = {
            'user_username': 'testuser',
            'event_title': 'Test Event',
            'registration_date': self.registration.registration_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'accepted': True,
        }

        self.assertEqual(serializer.data, expected_data)
