import requests

API_URL = "http://ws.audioscrobbler.com/2.0/"


class Track:

    def __init__(self, artist, title):
        self.artist = artist
        self.title = title

class LastfmClient:
    """A Last.fm Client used to make calls to the API."""

    def __init__(self, api_key):
        self.api_key = api_key
        self.defaults = {
            'artist': {
                'mbid': None,
                'autocorrect': 1,
                'page': 1,
                'limit': 50,
                'format': 'json'
            },
            'user': {
                'limit': 50,
                'page': 1,
                'format': 'json'
            }

        }

    def make_api_call(self, method, data=None):
        method = method.lower()
        req_call = getattr(requests, method)
        response = None

        if method == 'get':
            response = req_call(API_URL, params={**{"api_key" : self.api_key}, **data})
            print(response.url)

        return response.json() if response is not None else ""

    def getToken(self):
        return self.make_api_call("GET", {'method': 'auth.getToken',
                                          'api_key': self.api_key,
                                          'format': 'json'})['token']

    def _buildPayload(self, method, payload, pkey, **kwargs):
        payload['method'] = method

        if pkey in self.defaults:
            for k, v in self.defaults[pkey].items():
                if k in kwargs:
                    payload[k] = kwargs[k]
                elif v is not None:
                    payload[k] = v

    def user_loveTrack(self, track):
        session = self._authenticate()

        if session is None:
            print("Session is none. Did you set api_sig?")
            return

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

    def user_getRecentPlayed(self, user, to=None, _from=None,
                             extended=1, **kwargs):
        method = "user.getRecentTracks"

        payload = {'user': user, 'extended': extended}
        if to is not None:
            payload['to']: to
        if _from is not None:
            payload['from']: _from

        self._buildPayload(method, payload, 'user', **kwargs)
        return self.make_api_call("GET", payload)

    def user_getFriends(self, user, recenttracks=0, **kwargs):
        method = "user.getFriends"

        payload = {'user': user, 'recenttracks': recenttracks}
        self._buildPayload(method, payload, 'user', **kwargs)
        return self.make_api_call("GET", payload)

    def user_getInfo(self, user, _format='json'):
        method = "user.getInfo"

        return self.make_api_call("GET", {
            'user': user,
            'method': method,
            'format': _format
        })

    def user_getLovedTracks(self, user, **kwargs):
        method = "user.getLovedTracks"

        payload = {'user': user}
        self._buildPayload(method, payload, 'user', **kwargs)
        return self.make_api_call("GET", payload)

    def user_getPersonalTags(self, user, tag, taggingtype, **kwargs):
        method = "user.getPersonalTags"

        payload = {'user': user, 'tag': tag, 'taggingtype': taggingtype}
        self._buildPayload(method, payload, 'user', **kwargs)
        return self.make_api_call("GET", payload)

    def user_getTopAlbums(self, user, period='overall', **kwargs):
        '''
            Return top albums for user.

            Params:
                user: the lastfm username
                period: time period in (default=overall):
                    {overall | 7day | 1month | 3month | 6month | 12month}
                kwargs: additional keyword args
        '''

        method = "user.getTopAlbums"

        payload = {'user': user, 'period': period}
        self._buildPayload(method, payload, 'user', **kwargs)
        return self.make_api_call("GET", payload)

    def user_getTopArtists(self, user, period='overall', **kwargs):
        '''
            Return top artists for user.

            Params:
                user: the lastfm username
                period: time period in (default=overall):
                    {overall | 7day | 1month | 3month | 6month | 12month}
                kwargs: additional keyword args
        '''
        method = "user.getTopArtists"

        payload = {'user': user, 'period': period}
        self._buildPayload(method, payload, 'user', **kwargs)
        return self.make_api_call("GET", payload)

    def user_getTopTracks(self, user, period='overall', **kwargs):
        '''
            Return top tracks for user.

            Params:
                user: the lastfm username
                period: time period in (default=overall):
                    {overall | 7day | 1month | 3month | 6month | 12month}
                kwargs: additional keyword args
        '''
        method = "user.getTopTracks"

        payload = {'user': user, 'period': period}
        self._buildPayload(method, payload, 'user', **kwargs)
        return self.make_api_call("GET", payload)

    def user_getWeeklyAlbumChart(self, user, _from=None, to=None, _format='json'):
        '''
            Return weekly album chart for user. If no time period
            is specified using _from and to params, the most recent
            chart will be return.

            Params:
                user: the lastfm username
                _from: starting time point
                to: ending time point
                _format: format to return
        '''
        method = "user.getWeeklyAlbumChart"
        payload = {'user': user, 'format': _format, 'method': method}
        if _from is not None:
            payload['from'] = _from
        if to is not None:
            payload['to']: to

        return self.make_api_call("GET", payload)

    def user_getWeeklyTrackChart(self, user, _from=None, to=None, _format='json'):
        '''
            Return weekly album chart for user. If no time period
            is specified using _from and to params, the most recent
            chart will be return.

            Params:
                user: the lastfm username
                _from: starting time point
                to: ending time point
                _format: format to return
        '''
        method = "user.getWeeklyTrackChart"
        payload = {'user': user, 'format': _format, 'method': method}
        if _from is not None:
            payload['from'] = _from
        if to is not None:
            payload['to']: to

        return self.make_api_call("GET", payload)

    def user_getWeeklyArtistChart(self, user, _from=None, to=None, _format='json'):
        '''
            Return weekly album chart for user. If no time period
            is specified using _from and to params, the most recent
            chart will be return.

            Params:
                user: the lastfm username
                _from: starting time point
                to: ending time point
                _format: format to return
        '''
        method = "user.getWeeklyArtistChart"
        payload = {'user': user, 'format': _format, 'method': method}
        if _from is not None:
            payload['from'] = _from
        if to is not None:
            payload['to']: to

        return self.make_api_call("GET", payload)

    def artist_getSimilar(self, artist, **kwargs):
        method = "artist.getSimilar"

        payload = {
            'method': method,
            'artist': artist
        }

        self._buildPayload(payload, 'artist', **kwargs)
        return self.make_api_call("GET", payload)

    def artist_getInfo(self, artist, **kwargs):
        method = "artist.getInfo"

        payload = {
            'method': method,
            'artist': artist
        }

        self._buildPayload(payload, 'artist', **kwargs)
        return self.make_api_call("GET", payload)

    def artist_search(self, artist, **kwargs):
        method = "artist.search"

        payload = {
            'method': method,
            'artist': artist
        }

        self._buildPayload(payload, 'artist', **kwargs)
        return self.make_api_call("GET", payload)

    def artist_getTopTracks(self, artist, **kwargs):
        method = "artist.getTopTracks"

        payload = {
            'artist': artist,
            'method': method
        }

        self._buildPayload(payload, 'artist', **kwargs)
        return self.make_api_call("GET", payload)

    def artist_getCorrection(self, artist, _format='json'):
        method = "artist.getCorrection"

        payload = {
            'artist': artist,
            'method': method,
            'format': _format
        }

        return self.make_api_call("GET", payload)
