from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('patient/', include('patientsApp.urls')),
    path('doctor/', include('doctorsApp.urls'))
]
