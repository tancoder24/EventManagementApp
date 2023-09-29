from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Venue, Event, Registration, User

admin.site.register(User)

class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'amenities', 'display_available_dates')
 
    # Custom method to display available dates in the admin panel
    def display_available_dates(self, obj):
        available_dates = obj.get_available_dates()
        return ', '.join(map(str, available_dates))
    display_available_dates.short_description = 'Available Dates'

admin.site.register(Venue, VenueAdmin)


class EventAdmin(admin.ModelAdmin):
    actions=[]
    list_display = ('title', 'date', 'location', 'created_by')
    readonly_fields = ('created_by',)

    def save_model(self, request, obj, form, change):
        if change and obj.created_by != request.user:
            raise ValidationError("Event creator can only update")
        
        obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        if obj.created_by != request.user:
            raise ValidationError("Event Owner can only delete it")
        obj.delete()

admin.site.register(Event, EventAdmin)


admin.site.register(Registration)
