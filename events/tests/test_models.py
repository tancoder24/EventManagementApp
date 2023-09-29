from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from events.models import User, Venue, Registration, Event
from events import utils

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpassword'))

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')


class VenueModelTest(TestCase):
    def setUp(self):
        self.venue = Venue.objects.create(
            name='Test Venue',
            capacity=100,
            amenities='Amenity 1, Amenity 2'
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_venue_creation(self):
        self.assertEqual(self.venue.name, 'Test Venue')
        self.assertEqual(self.venue.capacity, 100)
        self.assertEqual(self.venue.amenities, 'Amenity 1, Amenity 2')

    def test_venue_str(self):
        self.assertEqual(str(self.venue), 'Test Venue')

    def test_get_all_events(self):
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            date=timezone.now().date() + timedelta(days=1),
            time=timezone.now().time(),
            location=self.venue,
            capacity=50,
            category=utils.CATEGORY_CHOICES[0][0],
            created_by=self.user
        )
        self.assertEqual(list(self.venue.get_all_events()), [event])

    def test_get_booked_dates(self):
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            date=timezone.now().date() + timedelta(days=1),
            time=timezone.now().time(),
            location=self.venue,
            capacity=50,
            category=utils.CATEGORY_CHOICES[0][0],
            created_by=self.user
        )
        self.assertEqual(list(self.venue.get_booked_dates()), [event.date])

    def test_get_available_dates(self):
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            date=timezone.now().date() + timedelta(days=1),
            time=timezone.now().time(),
            location=self.venue,
            capacity=50,
            category=utils.CATEGORY_CHOICES[0][0],
            created_by=self.user
        )
        available_dates = self.venue.get_available_dates()
        self.assertNotIn(event.date, available_dates)


class EventModelTest(TestCase):
    def setUp(self):
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

    def test_event_creation(self):
        event = Event(
            title='Test Event',
            description='Test Description',
            date=timezone.now().date() + timedelta(days=1),
            time=timezone.now().time(),
            location=self.venue,
            capacity=50,
            category=utils.CATEGORY_CHOICES[0][0],  # Use the first category choice
            created_by=self.user
        )
        event.save()

        self.assertEqual(event.title, 'Test Event')
        self.assertEqual(event.description, 'Test Description')
        self.assertEqual(event.location, self.venue)
        self.assertEqual(event.capacity, 50)
        self.assertEqual(event.category, utils.CATEGORY_CHOICES[0][0])
        self.assertEqual(event.created_by, self.user)


class RegistrationModelTest(TestCase):
    def setUp(self):
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
            category=utils.CATEGORY_CHOICES[0][0],
            created_by=self.user
        )

    def test_registration_creation_and_uniques_constrain(self):
        registration = Registration.objects.create(
            user=self.user,
            event=self.event,
            accepted=False
        )

        self.assertEqual(registration.user, self.user)
        self.assertEqual(registration.event, self.event)
        self.assertFalse(registration.accepted)

        with self.assertRaises(IntegrityError):
            Registration.objects.create(
                user=self.user,
                event=self.event,
                accepted=False
            )

