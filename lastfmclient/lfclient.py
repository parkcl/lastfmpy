import requests


API_URL = "http://ws.audioscrobbler.com/2.0/"


class LastfmClient:
    """A Last.fm Client used to make calls to the API."""

    def __init__(self, api_key, api_sig=None, isAuth=False):
        self.api_key = api_key
        self.isAuth = isAuth
        self.api_sig = api_sig
        self.apiKeyParam = {'api_key': self.api_key}

        # TODO auth

    def make_api_call(self, method, data=None):
        method = method.lower()
        req_call = getattr(requests, method)
        response = None

        if method == 'get':
            response = req_call(API_URL, params={**self.apiKeyParam, **data})
            print(response.url)

        return response.json() if response is not None else ""

    def user_getPlayingNow(self, user):
        key = '@attr'
        val = 'nowplaying'
        data = self.user_getRecentPlayed(user, limit=1, extended=1)

        if len(data['recenttracks']['track']) is 0:
            return None

        data = data['recenttracks']['track'][0]

        if key in data and data[key][val] == 'true':
            track_name = data['name']
            track_artist = data['artist']['name']
            track_album = data['album']['#text']
            track_isLoved = data['loved']

            return (track_artist, track_name, track_album, track_isLoved)
        else:
            return None

    def user_getRecentPlayed(self, user, limit=50,
                             page_number=1, _from=None,
                             extended=0, to=None,
                             _format='json'):
        method = "user.getrecenttracks"

        if _from is None and to is None:
            return self.make_api_call("GET", {
                'user': user,
                'limit': limit,
                'page_number': page_number,
                'extended': extended,
                'method': method,
                'format': _format
            })
        else:
            return self.make_api_call("GET", {
                'user': user,
                'limit': limit,
                'page_number': page_number,
                'extended': extended,
                'to': to,
                'from': _from,
                'method': method,
                'format': _format
            })

    def user_getFriends(self, user, recent_tracks=0,
                        limit=50, page_number=1, _format='json'):
        method = "user.getFriends"

        return self.make_api_call("GET", {
            'user': user,
            'recenttracks': recent_tracks,
            'limit': limit,
            'page_number': page_number,
            'method': method,
            'format': _format
        })

    # todo
    def validate_user(self):
        pass
