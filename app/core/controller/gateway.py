
import re
import os
from dotenv import load_dotenv
from urllib.parse import urlparse, unquote_plus
from ..rutracker_api import RutrackerApi
from .data import TorrentObject, DownloadPath, Category, TorrentType
from .exception import (ParseErorr, TopicIdIsEmpty, 
                        InvalidMagnetLink, InvalidRuTrackerLink)

class ControllerGateway:
    load_dotenv()
    try: 
        rutracker_client = RutrackerApi()
        rutracker_client.login(
            username=os.environ.get('RUTRACKER_LOGIN'), 
            password=os.environ.get('RUTRACKER_PASSWORD')
        )
    except Exception as e:
        print(e)
        print('Failed to connect to Rutracker API, passed.')

    @classmethod
    def get_torrent_object(cls, url: str) -> TorrentObject:
        current_url = urlparse(url)
        print(current_url)
        torrent = TorrentObject()

        if current_url.scheme == "magnet":
            torrent.url = url
            torrent.name = cls._get_torrrent_name_by_magnet(url)
            torrent.type = TorrentType.magnet
            torrent.category = Category.unknown
            torrent.download_path = DownloadPath.default
            return torrent

        elif current_url.netloc == 'rutracker.net':
            topic_id = cls._get_rutracker_topic_id(url)
            if not topic_id:
                raise TopicIdIsEmpty(
                    "Incorrect link for rutracker.org resource! Can't parse the topic ID."
                )
            rutracker_torrent = cls.rutracker_client.topic(topic_id)[0]
            torrent.type = TorrentType.rutracker
            torrent.name = rutracker_torrent.title
            torrent.category = cls._get_rutracker_category(rutracker_torrent)
            torrent.download_path = DownloadPath.by_category(torrent.category)
            torrent.url = rutracker_torrent.get_magnet()
            return torrent
        
        elif url.endswith('.torrent'):
            torrent.name = 'Unknown'
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
    def set_torrent_category(torrent_object: TorrentObject, category: str) -> TorrentObject:
        if category == 'movie':
            torrent_object.category = Category.movie
            torrent_object.download_path = DownloadPath.by_category(Category.movie)

        if category == 'tvshow':
            torrent_object.category = Category.tvshow
            torrent_object.download_path = DownloadPath.by_category(Category.tvshow)

        if category == 'music':
            torrent_object.category = Category.music
            torrent_object.download_path = DownloadPath.by_category(Category.music)

        return torrent_object

    @staticmethod
    def _get_torrrent_name_by_magnet(url):
        match = re.findall(r'dn=.+', urlparse(url).query)
        if match:
            return unquote_plus(match[0].replace('dn=', ''))

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
