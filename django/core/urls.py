from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/pv1/docs/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/pv1/docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/pv1/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/token/", obtain_auth_token, name="api_token_auth"),
    path("admin/", admin.site.urls),
    path("", include("company.urls")),
]
