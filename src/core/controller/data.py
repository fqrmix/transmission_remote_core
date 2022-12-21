class DownloadPathProperties(type):

    @property
    def default(cls) -> str:
        return cls._default

    @property
    def music(cls) -> str:
        return cls._music
    
    @property
    def tvshows(cls) -> str:
        return cls._tvshows

    @property
    def movies(cls) -> str:
        return cls._movies

class CategoryProperties(type):

    @property
    def unknown(cls) -> str:
        return cls._unknown

    @property
    def music(cls) -> str:
        return cls._music
    
    @property
    def tvshow(cls) -> str:
        return cls._tvshow

    @property
    def movie(cls) -> str:
        return cls._movie

class TorrentTypeProperties(type):

    @property
    def magnet(cls) -> str:
        return cls._magnet

    @property
    def rutracker(cls) -> str:
        return cls._rutracker
    
    @property
    def direct(cls) -> str:
        return cls._direct

class TorrentType(object, metaclass=TorrentTypeProperties):
    _magnet = 'Magnet'
    _rutracker = 'RuTracker'
    _direct = 'Direct'

class DownloadPath(object, metaclass=DownloadPathProperties):
    _default = '/path/to/default'
    _music = '/path/to/music'
    _tvshows = '/path/to/tvshows'
    _movies = '/path/to/movies'

class Category(object, metaclass=CategoryProperties):
    _unknown = 'Unknown'
    _music = 'Music'
    _tvshows = 'TV Show'
    _movies = 'Movie'


class Torrent:
    def __init__(self) -> None:
        self._url = None
        self._type = None
        self._category = None
        self._download_path = None

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, val):
        self._url = val

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, val):
        self._type = val

    @property
    def category(self) -> str:
        return self._category

    @category.setter
    def category(self, val: Category):
        self._category = val

    @property
    def download_path(self) -> str:
        return self._download_path

    @download_path.setter
    def download_path(self, val: DownloadPath):
        self._download_path = val