
import re
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from ..rutracker_api import RutrackerApi
from .data import TorrentObject, DownloadPath, Category, TorrentType
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
    def get_torrent_object(cls, url: str) -> TorrentObject:
        current_url = urlparse(url)
        torrent = TorrentObject()

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
            rutracker_torrent = cls.rutracker_client.topic(topic_id)[0]
            torrent.type = TorrentType.rutracker
            torrent.category = cls._get_rutracker_category(rutracker_torrent)
            torrent.download_path = DownloadPath.by_category(torrent.category)
            torrent.url = rutracker_torrent.get_magnet()
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

    @classmethod
    def _get_rutracker_category(cls, rutracker_torrent):
        dict = rutracker_torrent.as_dict()
        forum_id = dict['forum_id']
        category = cls.rutracker_client.forum(forum_id)[0]['forum_name']
        if re.match(r'.+музыка.+', category, re.IGNORECASE):
            return Category.music
        elif re.match(r'(.+фильмы.+|.+кино.+)', category, re.IGNORECASE):
            return Category.movie
        elif re.match(r'.+сериалы.+', category, re.IGNORECASE):
            return Category.tvshow
        else:
            return Category.unknown
