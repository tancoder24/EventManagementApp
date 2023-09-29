from rest_framework.exceptions import PermissionDenied
from rest_framework import serializers
from django.utils import timezone

from .models import Venue, Event, Registration, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ("password",)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ("created_by",)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)

    def validate_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Event date must be in the future.")
        return value

class VenueSerializer(serializers.ModelSerializer):

    booked_dates = serializers.SerializerMethodField()
    available_dates = serializers.SerializerMethodField()
    events = EventSerializer(many=True, read_only=True, source='event_set')

    class Meta:
        model = Venue
        fields = '__all__'

    def get_booked_dates(self, obj):
        return obj.get_booked_dates()

    def get_available_dates(self, obj):
        return obj.get_available_dates()
    
    def get_events(self, obj):
        return obj.get_all_events()


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'
        read_only_fields = ("user",)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        validated_data["accepted"] = False
        return super().create(validated_data)


class RegistrationExportSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    event_title = serializers.ReadOnlyField(source='event.title')

    class Meta:
        model = Registration
        fields = ['user_username', 'event_title', 'registration_date', 'accepted']
