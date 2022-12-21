from transmission_rpc import Client as TransmissionClient
from transmission_rpc import Torrent, Session
from .gateway import ControllerGateway
from .data import TorrentObject
from dotenv import load_dotenv
import os

class TransmissionFacade:
    def exception_handler(func):
        def _wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                print(error)
        return _wrapper

    @exception_handler
    def __init__(self) -> None:
        load_dotenv()
        self.transmission_client = TransmissionClient(
            username=os.environ.get('TRANSMISSION_LOGIN'),
            password=os.environ.get('TRANSMISSION_PASSWORD'),
            host=os.environ.get('TRANSMISSION_HOST'),
            port=os.environ.get('TRANSMISSION_PORT')
        )

    @exception_handler
    def add_torrent(self, torrent_object: TorrentObject) -> TorrentObject:
        torrent = self.transmission_client.add_torrent(
            torrent=torrent_object.url,
            download_dir=torrent_object.download_path,
        )
        return torrent

    @exception_handler
    def get_torrent_object(self, url: str) -> TorrentObject:
        return ControllerGateway.get_torrent_object(url)

    @exception_handler
    def get_torrent_list(self) -> list[Torrent]:
        return self.transmission_client.get_torrents()

    @exception_handler
    def start_downloading(self):
        return self.transmission_client.start_all()

    @exception_handler
    def set_download_speed_limit(self, speed: int) -> Session:
        self.transmission_client.set_session(
            speed_limit_down=speed,
            speed_limit_down_enabled=True
        )
        return self.transmission_client.get_session()
    
    @exception_handler
    def disable_speed_limit(self) -> Session:
        self.transmission_client.set_session(
            speed_limit_down_enabled=False
        )
        return self.transmission_client.get_session()
    
    @exception_handler
    def enable_speed_limit(self) -> Session:
        self.transmission_client.set_session(
            speed_limit_down_enabled=True
        )
        return self.transmission_client.get_session()
