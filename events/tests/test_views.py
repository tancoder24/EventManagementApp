from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient, APITestCase
from django.utils import timezone
from datetime import datetime

from events.models import User, Venue, Event, Registration
from events.serializers import UserSerializer, VenueSerializer, EventSerializer, RegistrationSerializer, RegistrationExportSerializer
from events.views import UserViewSet, VenueViewSet, EventViewSet, RegistrationViewSet, RegistrationExportViewSet
from events.utils import CATEGORY_CHOICES

class VenueViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword'
        )
        self.venue_data = {
            'name': 'Test Venue',
            'capacity': 100,
            'amenities': 'Amenity 1, Amenity 2'
        }
        self.venue = Venue.objects.create(**self.venue_data)

    # Unauthenticated
    def test_unauthenticated_retrieve_venue(self):
        url = reverse(
            "venues-detail", kwargs={"pk": self.venue.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_unauthenticated_partial_update_venue(self):
        url = reverse(
            "venues-detail", kwargs={"pk": self.venue.id}
        )
        update_data = {
            "name": "Test Venue Updated"
        }
        response = self.client.patch(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_unauthenticated_update_venue(self):
        url = reverse(
            "venues-detail", kwargs={"pk": self.venue.id}
        )
        updated_venue_data = {
            'name': 'Test Venue Updated',
            'capacity': 1000,
            'amenities': 'Amenity 1, Amenity 2, All'
        }
        response = self.client.put(url, updated_venue_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_unauthenticated_delete_venue(self):
        url = reverse(
            "venues-detail", kwargs={"pk": self.venue.id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_unauthenticated_list_venue(self):
        url = reverse("venues-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_unauthenticated_create_venue(self):
        url = reverse("venues-list")
        data = {
            "name": "NEW VENUE",
            "capacity": 200,
            "amenities": "ALL"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )
    
    # Normal User
    def test_authenticated_normal_user_retrieve_venue(self):
        self.client.force_authenticate(user=self.user)
        url = reverse(
            "venues-detail", kwargs={"pk": self.venue.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "You do not have permission to perform this action."
        )

    def test_authenticated_normal_user_partial_update_venue(self):
        self.client.force_authenticate(user=self.user)
        url = reverse(
            "venues-detail", kwargs={"pk": self.venue.id}
        )
        update_data = {
            "name": "Test Venue Updated"
        }

        response = self.client.patch(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "You do not have permission to perform this action."
        )

    def test_authenticated_normal_user_update_venue(self):
        self.client.force_authenticate(user=self.user)
        url = reverse(
            "venues-detail", kwargs={"pk": self.venue.id}
        )
        updated_venue_data = {
            'name': 'Test Venue Updated',
            'capacity': 1000,
            'amenities': 'Amenity 1, Amenity 2, All'
        }
        response = self.client.put(url, updated_venue_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "You do not have permission to perform this action."
        )

    def test_authenticated_normal_user_delete_venue(self):
        self.client.force_authenticate(user=self.user)
        url = reverse(
            "venues-detail", kwargs={"pk": self.venue.id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "You do not have permission to perform this action."
        )

    def test_authenticated_normal_user_list_venue(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("venues-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "You do not have permission to perform this action."
        )

    def test_authenticated_normal_user_create_venue(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("venues-list")
        data = {
            "name": "NEW VENUE",
            "capacity": 200,
            "amenities": "ALL"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "You do not have permission to perform this action."
        )

    # Admin User
    def test_authenticated_admin_user_retrieve_venue(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse(
            "venues-detail", kwargs={"pk": self.venue.id}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for key in self.venue_data:
            self.assertEqual(self.venue_data[key], response.json()[key])

    def test_authenticated_admin_user_partial_update_venue(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse(
            "venues-detail", kwargs={"pk": self.venue.id}
        )

        update_data = {
            "name": "Test Venue Updated"
        }

        response = self.client.patch(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_data["name"], response.json()["name"])

    def test_authenticated_admin_user_update_venue(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse(
            "venues-detail", kwargs={"pk": self.venue.id}
        )

        updated_venue_data = {
            'name': 'Test Venue Updated',
            'capacity': 1000,
            'amenities': 'Amenity 1, Amenity 2, All'
        }

        response = self.client.put(url, updated_venue_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for key in updated_venue_data:
            self.assertEqual(updated_venue_data[key], response.json()[key])

    def test_authenticated_admin_user_delete_venue(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse(
            "venues-detail", kwargs={"pk": self.venue.id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authenticated_admin_user_list_venue(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("venues-list")
        response = self.client.get(url)
        expected_data = VenueSerializer([self.venue], many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data["results"]), str(expected_data))

    def test_authenticated_admin_user_create_venue(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("venues-list")
        data = {
            "name": "NEW VENUE",
            "capacity": 200,
            "amenities": "ALL"
        }
        response = self.client.post(url, data)
        for key in data:
            self.assertEqual(data[key], response.json()[key])
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

##############################################################################

class EventViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword'
        )
        self.venue_data = {
            'name': 'Test Venue',
            'capacity': 100,
            'amenities': 'Amenity 1, Amenity 2'
        }
        self.venue = Venue.objects.create(**self.venue_data)
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            date=timezone.now().date() + timezone.timedelta(days=2),
            time=timezone.now().time(),
            location=self.venue,
            capacity=100,
            category=CATEGORY_CHOICES[0][0],
            created_by=self.admin_user
        )

    # Unauthenticated
    def test_unauthenticated_retrieve_event(self):
        url = reverse(
            "events-detail", kwargs={"pk": self.event.id}
        )

        event_data = EventSerializer(self.event).data

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for key in event_data:
            self.assertEqual(event_data[key], response.json()[key])

    def test_unauthenticated_partial_update_event(self):
        url = reverse(
            "events-detail", kwargs={"pk": self.event.id}
        )
        update_data = {
            "title": "Test Event Updated"
        }
        response = self.client.patch(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_unauthenticated_update_event(self):
        url = reverse(
            "events-detail", kwargs={"pk": self.event.id}
        )
        updated_event_data = {
            'title': 'Test Event Updated',
            'description': 'Test Description',
            'date': timezone.now().date() + timezone.timedelta(days=2),
            'time': timezone.now().time(),
            'location': self.venue,
            'capacity': 100,
            'category': CATEGORY_CHOICES[0][0]
        }
        response = self.client.put(url, updated_event_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_unauthenticated_delete_event(self):
        url = reverse(
            "events-detail", kwargs={"pk": self.event.id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_unauthenticated_list_event(self):
        url = reverse("events-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_create_event(self):
        url = reverse("events-list")
        data = {
            'title': 'Test Event Updated',
            'description': 'Test Description',
            'date': timezone.now().date() + timezone.timedelta(days=2),
            'time': timezone.now().time(),
            'location': self.venue,
            'capacity': 100,
            'category': CATEGORY_CHOICES[0][0]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )
    
    # Normal User
    def test_authenticated_normal_user_partial_update_event(self):
        self.client.force_authenticate(user=self.user)
        url = reverse(
            "events-detail", kwargs={"pk": self.event.id}
        )
        update_data = {
            "title": "Test Event Updated"
        }

        response = self.client.patch(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "You do not have permission to perform this action."
        )

    def test_authenticated_normal_user_update_event(self):
        self.client.force_authenticate(user=self.user)
        url = reverse(
            "events-detail", kwargs={"pk": self.event.id}
        )
        updated_event_data = {
            'title': 'Test Event Updated',
            'description': 'Test Description',
            'date': timezone.now().date() + timezone.timedelta(days=2),
            'time': timezone.now().time(),
            'location': self.venue,
            'capacity': 100,
            'category': CATEGORY_CHOICES[0][0]
        }
        response = self.client.put(url, updated_event_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "You do not have permission to perform this action."
        )

    def test_authenticated_normal_user_delete_event(self):
        self.client.force_authenticate(user=self.user)
        url = reverse(
            "events-detail", kwargs={"pk": self.event.id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "You do not have permission to perform this action."
        )

    def test_authenticated_normal_user_create_event(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("events-list")
        data = {
            'title': 'Test Event Updated',
            'description': 'Test Description',
            'date': timezone.now().date() + timezone.timedelta(days=2),
            'time': timezone.now().time(),
            'location': self.venue,
            'capacity': 100,
            'category': CATEGORY_CHOICES[0][0]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "You do not have permission to perform this action."
        )

    # Admin User
    def test_authenticated_admin_user_partial_update_event(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse(
            "events-detail", kwargs={"pk": self.event.id}
        )

        update_data = {
            "title": "Test Event Updated"
        }

        response = self.client.patch(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_data["title"], response.json()["title"])

    def test_authenticated_admin_user_update_event(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse(
            "events-detail", kwargs={"pk": self.event.id}
        )

        updated_event_data = {
            'title': 'Test Event Updated',
            'description': 'Test Description',
            'date': timezone.now().date() + timezone.timedelta(days=2),
            'time': timezone.now().time(),
            'location': self.venue.id,
            'capacity': 100,
            'category': CATEGORY_CHOICES[0][0]
        }

        response = self.client.put(url, updated_event_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for key in updated_event_data:
            if key == "date":
                self.assertEqual(updated_event_data[key], datetime.strptime(response.json()[key], '%Y-%m-%d').date())
            elif key == "time":
                self.assertEqual(updated_event_data[key], datetime.strptime(response.json()[key], '%H:%M:%S.%f').time())
            else:
                self.assertEqual(updated_event_data[key], response.json()[key])

    def test_authenticated_admin_user_delete_event(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse(
            "venues-detail", kwargs={"pk": self.venue.id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authenticated_admin_user_create_event(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("events-list")
        data = {
            'title': 'Test Event Updated',
            'description': 'Test Description',
            'date': timezone.now().date() + timezone.timedelta(days=2),
            'time': timezone.now().time(),
            'location': self.venue.id,
            'capacity': 100,
            'category': CATEGORY_CHOICES[0][0]
        }
        response = self.client.post(url, data)
        for key in data:
            if key == "date":
                self.assertEqual(data[key], datetime.strptime(response.json()[key], '%Y-%m-%d').date())
            elif key == "time":
                self.assertEqual(data[key], datetime.strptime(response.json()[key], '%H:%M:%S.%f').time())
            else:
                self.assertEqual(data[key], response.json()[key])
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

###############################################################################

class RegistrationViewSetTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpassword1'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpassword2'
        )
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword'
        )
        self.venue_data = {
            'name': 'Test Venue',
            'capacity': 100,
            'amenities': 'Amenity 1, Amenity 2'
        }
        self.venue = Venue.objects.create(**self.venue_data)

        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            date=timezone.now().date() + timezone.timedelta(days=2),
            time=timezone.now().time(),
            location=self.venue,
            capacity=100,
            category=CATEGORY_CHOICES[0][0],
            created_by=self.admin_user
        )

        self.registration = Registration.objects.create(
            user = self.user1,
            event = self.event,
        )

    # Unauthenticated
    def test_unauthenticated_retrieve_registration(self):
        url = reverse(
            "registrations-detail", kwargs={"pk": self.registration.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_unauthenticated_partial_update_registration(self):
        url = reverse(
            "registrations-detail", kwargs={"pk": self.registration.id}
        )
        update_data = {
            "accepted": True
        }
        response = self.client.patch(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_unauthenticated_list_registration(self):
        url = reverse("registrations-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_unauthenticated_create_registration(self):
        url = reverse("registrations-list")
        data = {
            'event': self.event
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )
    
    # Normal User
    def test_authenticated_normal_user_retrieve_registration(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse(
            "registrations-detail", kwargs={"pk": self.registration.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_other_user_retrieve_registration(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse(
            "registrations-detail", kwargs={"pk": self.registration.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json()["detail"], "Not found."
        )

    def test_authenticated_normal_user_partial_update_registration(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse(
            "registrations-detail", kwargs={"pk": self.registration.id}
        )
        update_data = {
            "accepted": True
        }

        response = self.client.patch(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "You do not have permission to perform this action."
        )

    def test_authenticated_normal_user_list_registration(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse("registrations-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_normal_user_create_registration(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse("registrations-list")
        data = {
            "event": self.event.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Admin User
    def test_authenticated_admin_user_retrieve_registration(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse(
            "registrations-detail", kwargs={"pk": self.event.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_admin_user_partial_update_registration(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse(
            "registrations-detail", kwargs={"pk": self.event.id}
        )
        update_data = {
            "accepted": True
        }
        response = self.client.patch(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_data["accepted"], response.json()["accepted"])

    def test_authenticated_admin_user_list_registration(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("registrations-list")
        response = self.client.get(url)
        expected_data = RegistrationSerializer([self.registration], many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data["results"]), str(expected_data))

    def test_authenticated_admin_user_create_registration(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("registrations-list")
        data = {
            "event": self.event.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

###############################################################################

class UserViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword'
        )

    # Unauthenticated
    def test_unauthenticated_retrieve_user(self):
        url = reverse(
            "users-detail", kwargs={"pk": self.user.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_unauthenticated_partial_update_user(self):
        url = reverse(
            "users-detail", kwargs={"pk": self.user.id}
        )
        update_data = {
            "first_name": "updated name"
        }
        response = self.client.patch(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_unauthenticated_delete_user(self):
        url = reverse(
            "users-detail", kwargs={"pk": self.user.id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_unauthenticated_list_users(self):
        url = reverse("users-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_unauthenticated_create_user(self):
        url = reverse("users-list")
        data = {
            "password": "Abcd@1234",
            "username": "temp_user"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # Normal User
    def test_authenticated_normal_user_retrieve_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse(
            "users-detail", kwargs={"pk": self.user.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_other_user_retrieve_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse(
            "users-detail", kwargs={"pk": self.admin_user.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_normal_user_partial_update_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse(
            "users-detail", kwargs={"pk": self.user.id}
        )
        update_data = {
            "first_name": "Updated Name"
        }

        response = self.client.patch(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "You do not have permission to perform this action."
        )

    def test_authenticated_normal_user_delete_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse(
            "users-detail", kwargs={"pk": self.user.id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "You do not have permission to perform this action."
        )

    def test_authenticated_normal_user_list_users(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("users-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "You do not have permission to perform this action."
        )

    # Admin User
    def test_authenticated_admin_user_retrieve_other_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse(
            "users-detail", kwargs={"pk": self.user.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_admin_user_partial_update_user(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse(
            "users-detail", kwargs={"pk": self.user.id}
        )

        update_data = {
            "first_name": "Updated Name"
        }

        response = self.client.patch(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_data["first_name"], response.json()["first_name"])

    def test_authenticated_admin_user_delete_user(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse(
            "users-detail", kwargs={"pk": self.user.id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authenticated_admin_user_list_users(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("users-list")
        response = self.client.get(url)
        expected_data = UserSerializer([self.user, self.admin_user], many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data["results"]), str(expected_data))
