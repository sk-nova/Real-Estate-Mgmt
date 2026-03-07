from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Schema for OpenAPI Specs
schema_view = get_schema_view(
    openapi.Info(
        title="Karim Apartments API",
        default_version="v1",
        description="Apartment Management System",
        contact=openapi.Contact(email="karimshadaab510@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("core_apps.users.urls")),
]


admin.site.site_header = "Karim Apartments"
admin.site.site_title = "Karim Apartments Admin Portal"
admin.site.index_title = "Welcome to Karim Apartments Admin Portal"
