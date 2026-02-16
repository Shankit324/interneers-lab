from django.http import JsonResponse
from .adapters import GreetingAdapter

def greeting_view(request):
    if request.method == "GET":
        adapter = GreetingAdapter()
        # Pass the raw GET parameters to the adapter
        result = adapter.execute_logic(request.GET)
        return JsonResponse(result)