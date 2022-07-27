import os
import requests
from analaytics.models import Visitor

from django.core.cache import cache

CACHE_TTL = 60 * 15


def geo_info(ip_address):
    # use cache to store the geo info
    geo_info = cache.get('geo_info_%s' % ip_address)
    if geo_info:
        return geo_info
    try:
        url = os.getenv('IPGEOLOCATION_URL')
        params = {
            'ip': ip_address,
            'apiKey': os.getenv('IPGEOLOCATION_APIKEY')
        }
        res = requests.get(f'{url}/ipgeo', params=params)
        if res.status_code == 200:
            geo_info = res.json()
            cache.set('geo_info_%s' % ip_address, geo_info, CACHE_TTL)
            return geo_info
    except Exception as e:
        print('Error when getting geo info:', e)

    return None


def track_visitor(request):
    page = str(request.path)
    if 'admin/' in page:
        return None

    user_agent = request.headers['User-Agent']
    ip_address = request.META['REMOTE_ADDR']
    user = request.user if request.user.is_authenticated else None
    os = 'Other'

    if 'window' in user_agent.lower():
        os = 'Window'
    elif 'android' in user_agent.lower():
        os = 'Android'
    elif 'iphone' in user_agent.lower():
        os = 'Iphone'
    elif 'linux' in user_agent.lower():
        os = 'Linux'
    elif 'mac' in user_agent.lower():
        os = 'Mac'

    geo_location = geo_info(ip_address)
    data = {}
    if geo_location:
        data = {
            'country': geo_location['country_name'],
            'city': geo_location['city'],
            'isp': geo_location['isp'],
            'country_code3': geo_location['country_code3']
        }

    Visitor.objects.create(
        description=user_agent, ip_address=ip_address, page=page,
        user_id=user.id if user else None, os=os, **data
    )


class TrackerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)
        track_visitor(request)

        return response

def observe_request(request):
    print('show request:', request)
    return True