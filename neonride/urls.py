from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rides import views as ride_views   # import your home view

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # Root → home view
    path('', ride_views.home, name='home'),

    # Include rides app URLs
    path('rides/', include(('rides.urls', 'rides'), namespace='rides')),
    
]
