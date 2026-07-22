from django.http import JsonResponse


def home(request):
    return JsonResponse({
        "message": "FinTrack API is working"
    })


urlpatterns = [
    path("", home),
]