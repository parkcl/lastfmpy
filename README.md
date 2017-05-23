# lastfmpy
This is a Last.fm client written in Python that makes use of Last.fm API available here: http://www.last.fm/api.

# installation
`python setup.py install`

Use of `pip` command will follow shortly.

# examples / usage
```python
import lastfmpy

lf = lastfmpy.LastfmClient('your api key')
print(lf.artist_getSimilar('Radiohead'))
```
