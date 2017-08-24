import requests


class Base:
    API_URL = "http://ws.audioscrobbler.com/2.0/"

    def __init__(self, api_key):
        self.api_key = api_key

    def _make_api_call(self, method, api_method, data):
        data['method'] = api_method
        data['api_key'] = self.api_key
        data['format'] = 'json'
        method = method.lower()
        req_call = getattr(requests, method)

        if method == "get":
            response = req_call(self.API_URL, params=data)
            print(response.url)
            return response.json()


class Commons:
    def _parse_track_mbid(self, data):
        if 'mbid' in data['track']:
            return data['track']['mbid']

    def _parse_track_isloved(self, data):
        return data['track']['userloved'] == "1"

    def _parse_user_playcount(self, data):
        if 'userplaycount' in data['track']:
            return data['track']['userplaycount']

    def _parse_track_corrected(self, data):
        if 'error' in data['track']:
            return None
        return {
            'track': data['track']['name'],
            'artist': data['track']['artist']['name']
        }

    def _parse_trackduration(self, data):
        return None if 'track' not in data else data['track']['duration']

class LastfmClient(Base, Commons):
    INVALID_API_KEY_CODE = 10

    def __init__(self, api_key, username=None):
        super().__init__(api_key)
        self.api_key = api_key
        self.username = username

    def set_user_context(self, username):
        self.username = username

    def get_track(self, artist, track):
        return Track(artist, track, self)
    
    def get_autocorrected_track(self, artist, track):
        params = {
            'artist': artist,
            'track': track,
            'autocorrect': 1
        }
        d = super()._parse_track_corrected(self._make_api_call('get', 'track.getInfo', params))
        
        if not d:
            return
        return Track(d['artist'], d['track'], self)

    def is_valid_apikey(self):
        rd = self.get_track('', '').get_raw_track_data()
        return not rd['error'] == self.INVALID_API_KEY_CODE if 'error' in rd else True


class Track(Commons):

    def __init__(self, artist, track, client):
        self.artist = artist
        self.track = track
        self.params = {
            'artist': self.artist,
            'track': self.track
        }
        self.client = client
        self.prefix = 'track'

    def get_mbid(self):
        return super()._parse_track_mbid(self._get_request())

    def get_isloved(self):
        if not self.client.username:
            return None
        self.params['username'] = self.client.username
        return super()._parse_track_isloved(self._get_request())

    def get_user_playcount(self):
        if not self.client.username:
            return None
        self.params['username'] = self.client.username
        return super()._parse_user_playcount(self._get_request())

    def get_duration(self):
        return super()._parse_trackduration(self._get_request())

    def get_raw_track_data(self):
        return self._get_request()

    def _get_request(self):
        req = getattr(self.client, '_make_api_call')
        return req('get', self.prefix + '.getInfo', self.params)

    def __str__(self):
        return self.artist + ' : ' + self.track