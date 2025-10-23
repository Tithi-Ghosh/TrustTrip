from django.contrib import admin

# Register your models here.from django.contrib import admin
from .models import BookingDriverSide, BookingUserSide, Payment, Review

admin.site.register(BookingDriverSide)
admin.site.register(BookingUserSide)
admin.site.register(Payment)
admin.site.register(Review)

