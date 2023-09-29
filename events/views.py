from rest_framework import viewsets, permissions, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from io import BytesIO
import pandas as pd

from .models import Venue, Event, Registration, User
from .serializers import VenueSerializer, EventSerializer, RegistrationSerializer, UserSerializer, RegistrationExportSerializer


class VenueViewSet(viewsets.ModelViewSet):
    http_method_names = ("get", "post", "put", "patch", "delete")
    queryset = Venue.objects.all().order_by("pk")
    serializer_class = VenueSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        PageNumberPagination.page_size = self.request.query_params.get('page_size',10)
        return super().list(self, request, *args, **kwargs)


class EventViewSet(viewsets.ModelViewSet):
    http_method_names = ("get", "post", "put", "patch", "delete")
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category", "date", "location",]
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in self.permission_classes]

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated: return super().list(self, request, *args, **kwargs)
        
        PageNumberPagination.page_size = self.request.query_params.get('page_size',10)
        event_list = self.filter_queryset(self.get_queryset())

        previous_record = Registration.objects.filter(user=request.user, accepted=True)
        previous_category_list = set([record.event.category for record in previous_record])

        matching_category_events = []
        other_events = []

        for event in event_list:
            if event.category in previous_category_list:
                matching_category_events.append(event)
            else:
                other_events.append(event)

        ordered_events = matching_category_events + other_events

        page = self.paginate_queryset(ordered_events)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(ordered_events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.created_by == request.user:
            serializer = self.get_serializer(instance, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        return Response(
            {"detail": "Only the event creator can update the event."},
            status=status.HTTP_403_FORBIDDEN
        )

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.created_by == request.user:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        return Response(
            {"detail": "Only the event creator can partially update the event."},
            status=status.HTTP_403_FORBIDDEN
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.created_by == request.user:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": "Only the event creator can delete the event."},
            status=status.HTTP_403_FORBIDDEN
        )


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ("get", "patch", "post", "delete")
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action in ('partial_update', 'destroy', 'list'):
            self.permission_classes = [permissions.IsAdminUser]
        elif self.action in ('retrieve',):
            self.permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in self.permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        return User.objects.filter(username=user.username)
    
    def list(self, request, *args, **kwargs):
        PageNumberPagination.page_size = self.request.query_params.get('page_size',10)
        return super().list(self, request, *args, **kwargs)


class RegistrationViewSet(viewsets.ModelViewSet):
    http_method_names = ("get", "patch", "post")
    serializer_class = RegistrationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("user", "event")
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action == 'partial_update':
            self.permission_classes = [permissions.IsAdminUser]
        elif self.action in ('create', 'list', 'retrieve'):
            self.permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in self.permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Registration.objects.all().order_by("pk")
        return Registration.objects.filter(user=user).order_by("pk")
    
    def list(self, request, *args, **kwargs):
        PageNumberPagination.page_size = self.request.query_params.get('page_size',10)
        return super().list(self, request, *args, **kwargs)


class RegistrationExportViewSet(viewsets.ModelViewSet):
    http_method_names = ("get",)
    permission_classes = [permissions.IsAdminUser]
    serializer_class = RegistrationExportSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("user", "event")
    queryset = Registration.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        df = pd.DataFrame(serializer.data)

        # Create a BytesIO object to hold the Excel data
        excel_data = BytesIO()

        # Save the DataFrame to the BytesIO object
        df.to_excel(excel_data, index=False)

        # Reset the file pointer position to the beginning of the BytesIO object
        excel_data.seek(0)

        # Prepare the response with the BytesIO data
        response = HttpResponse(excel_data.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="registrations.xlsx"'

        return response
