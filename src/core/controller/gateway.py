
import re
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from ..rutracker_api import RutrackerApi
from .data import Torrent, DownloadPath, Category, TorrentType
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
    def get_torrent_object(cls, url: str) -> Torrent:
        current_url = urlparse(url)
        torrent = Torrent()

        if current_url.scheme == "magnet":
            torrent.url = url
            torrent.type = TorrentType.magnet
            torrent.category = Category.unknown
            torrent.download_path = DownloadPath.default
            return torrent

        elif current_url.netloc == 'rutracker.org':
            topic_id = cls._get_rutracker_topic_id(url)
            if not topic_id:
                raise TopicIdIsEmpty(
                    "Incorrect link for rutracker.org resource! Can't parse the topic ID."
                )
            torrent.type = TorrentType.rutracker
            torrent.category = Category.tvshow
            torrent.download_path = DownloadPath.tvshows
            torrent.url = cls.rutracker_client.topic(topic_id)[0].get_magnet()
            return torrent
        
        elif url.endswith('.torrent'):
            torrent.type = TorrentType.direct
            torrent.category = Category.unknown
            torrent.download_path = DownloadPath.default
            torrent.url = url
            return torrent
        
        else:
            raise ParseErorr(
                "Incorrent link for torrent! You can use:\n"\
                "- Any magnet link\n"\
                "- Rutracker.org link with topic ID\n"\
                "- Direct link to .torrent file"
            )

    @staticmethod
    def _get_rutracker_topic_id(url):
        if re.match(r'^(t=)([0-9]+)', urlparse(url).query):
            return re.findall(r'([0-9]+)', urlparse(url).query)[0]
        return None
