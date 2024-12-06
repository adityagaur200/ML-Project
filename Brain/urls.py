from django.contrib import admin
from django.urls import path, include  # 'include' allows us to include app-level URL configurations
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin page for the project
    path('admin/', admin.site.urls),

    # Main index page where the HTML form resides (served by 'index' view from 'my_app')
    path('', include('detection.urls')),  # All routes from 'my_app/urls.py' will be included here

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # To serve media files during development
