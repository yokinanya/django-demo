from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include  # add this
# from django.conf.urls import handler400, handler403, handler404, handler500
import notifications.urls

urlpatterns = [
    path('admin/', admin.site.urls),          
    path("auth/", include("authentication.urls")), # Auth routes - login / register
    path("", include("sales.urls")),
    path('api/', include('Api.urls')),
    # path('comment/', include('comment.urls', namespace='comment')),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
]
