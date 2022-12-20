
import re
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from core.rutracker_api import RutrackerApi
from .data import Torrent
from .exception import (ParseErorr, TopicIdIsEmpty, 
                        InvalidMagnetLink, InvalidRuTrackerLink)

class ControllerGateway:
    load_dotenv()
    rutracker_client = RutrackerApi()
    rutracker_client.login(
        username=os.environ.get('RUTRACKER_LOGIN'), 
        password=os.environ.get('RUTRACKER_PASSWORD')
    )

    @classmethod
    def get_torrent_object(cls, url) -> Torrent:
        current_url = urlparse(url)
        torrent = Torrent

        if current_url.scheme == "magnet":
            torrent.type = "magnet"
            torrent.url = url
            return torrent

        elif current_url.netloc == 'rutracker.org':
            topic_id = cls._get_rutracker_topic_id(url)
            if not topic_id:
                raise TopicIdIsEmpty
            torrent.type = "rutracker"
            torrent.url = cls.rutracker_client.topic(topic_id)[0].get_magnet()
            return torrent
        
        elif url.endswith('.torrent'):
            torrent.type = "direct"
            torrent.url = url
            return torrent
        
        else:
            raise ParseErorr

    @staticmethod
    def _get_rutracker_topic_id(url):
        if re.match(r'^(t=)([0-9]+)', urlparse(url).query):
            return re.findall(r'([0-9]+)', urlparse(url).query)[0]
        return None
