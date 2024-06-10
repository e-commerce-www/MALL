import requests
from django.conf import settings

def get_disqus_comment_count(disqus_id):
    api_url = 'https://disqus.com/api/3.0/threads/details.json'
    params = {
        'api_key': settings.DISQUS_API_KEY,
        'forum': settings.DISQUS_SHORTNAME,
        'thread:ident': disqus_id
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['response']['posts']
    return 0
