from django.conf import settings
from django.db import models
from django.utils import timezone

class RideStatus(models.TextChoices):
    REQUESTED = 'REQUESTED', 'Requested'
    MATCHED = 'MATCHED', 'Matched'
    ONGOING = 'ONGOING', 'Ongoing'
    COMPLETED = 'COMPLETED', 'Completed'
    CANCELLED = 'CANCELLED', 'Cancelled'

class RideType(models.TextChoices):
    PERSONAL = 'PERSONAL', 'Personal'
    SHARING = 'SHARING', 'Sharing'

class RideRequest(models.Model):
    rider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ride_requests')
    pickup_address = models.CharField(max_length=255)
    dropoff_address = models.CharField(max_length=255)
    pickup_time = models.DateTimeField(default=timezone.now)
    ride_type = models.CharField(max_length=10, choices=RideType.choices)
    status = models.CharField(max_length=12, choices=RideStatus.choices, default=RideStatus.REQUESTED)
    base_fare = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    distance_km = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    is_share_open = models.BooleanField(default=False)  # True if first person picked SHARING
    shared_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='shared_rides')
    created_at = models.DateTimeField(auto_now_add=True)

    def fare(self):
        # Simple fare model: base + per-km
        per_km = 15.0  # in local currency unit
        calc = float(self.base_fare) + per_km * float(self.distance_km)
        if self.ride_type == RideType.SHARING and self.shared_by:
            return round(calc / 2, 2)
        return round(calc, 2)

    def can_accept_share(self):
        return self.ride_type == RideType.SHARING and self.is_share_open and self.shared_by is None and self.status == RideStatus.REQUESTED

class Driver(models.Model):
    name = models.CharField(max_length=100)
    vehicle_plate = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

class Assignment(models.Model):
    ride = models.OneToOneField(RideRequest, on_delete=models.CASCADE, related_name='assignment')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
