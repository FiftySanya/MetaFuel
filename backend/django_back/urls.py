from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication endpoints
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    
    # API endpoints
    path('api/users/', include('users.urls')),
    path('api/foods/', include('foods.urls')),
    path('api/exercises/', include('exercises.urls')),
    path('api/plans/', include('plans.urls'))
]
