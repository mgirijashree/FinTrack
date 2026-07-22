from django.http import JsonResponse
from django.urls import path


def home(request):
    return JsonResponse({
        "message": "FinTrack API is working"
    })


urlpatterns = [
    path("", home),
]