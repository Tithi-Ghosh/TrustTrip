from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('request/', views.create_ride, name='create_ride'),
    path('<int:ride_id>/', views.ride_detail, name='ride_detail'),
    path('<int:ride_id>/join-share/', views.join_share, name='join_share'),
    path('<int:ride_id>/assign/', views.assign_driver, name='assign_driver'),
    path('driver/login/', views.driver_login, name='driver_login'),
    path('driver/dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('rider/signup/', views.rider_signup, name='rider_signup'),
    path('driver/signup/', views.driver_signup, name='driver_signup'),
]
