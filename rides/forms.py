from django import forms
from .models import RideRequest, RideType

class RideRequestForm(forms.ModelForm):
    class Meta:
        model = RideRequest
        fields = ['pickup_address','dropoff_address','pickup_time','ride_type','distance_km']
        widgets = {
            'pickup_time': forms.DateTimeInput(attrs={'type':'datetime-local'}),
        }

