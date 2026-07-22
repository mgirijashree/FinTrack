from django.contrib import admin
from django.urls import path
from django.http import JsonResponse


def home(request):
    return JsonResponse({
        "message": "FinTrack API is running"
    })


urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
]