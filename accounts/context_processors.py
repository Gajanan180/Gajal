def user_location(request):
    loc = request.session.get('user_location', {})
    return {
        'user_city': loc.get('city') or 'Detecting location...',
        'user_area': loc.get('area') or 'Allow location in browser',
    }
