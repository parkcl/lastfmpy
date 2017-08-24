# lastfmpy
This is a Last.fm client written in Python that makes use of Last.fm API available here: http://www.last.fm/api.

# installation
`python setup.py install`

# examples / usage
```python
import lastfmpy

lf = lastfmpy.LastfmClient('your api key')
t = lf.get_autocorrected_track('radiohead', 'pyramid song')
print(t.get_duration())
```
