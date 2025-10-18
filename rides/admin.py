from django.contrib import admin
from .models import RideRequest, Driver, Assignment

@admin.register(RideRequest)
class RideRequestAdmin(admin.ModelAdmin):
    list_display = ('id','rider','pickup_address','dropoff_address','ride_type','status','is_share_open','shared_by','distance_km')
    list_filter = ('ride_type','status','is_share_open')
    search_fields = ('pickup_address','dropoff_address','rider__username')

admin.site.register(Driver)
admin.site.register(Assignment)
