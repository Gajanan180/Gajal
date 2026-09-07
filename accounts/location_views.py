from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json


@require_POST
def save_location_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    request.session['user_location'] = {
        'city': data.get('city', ''),
        'area': data.get('area', ''),
        'lat': data.get('lat'),
        'lng': data.get('lng'),
    }
    request.session.modified = True
    return JsonResponse({'ok': True, 'location': request.session['user_location']})
