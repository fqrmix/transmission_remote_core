from core.rutracker_api import RutrackerApi
from transmission_rpc import Client as TransmissionClient
from urllib.parse import urlencode, unquote_plus, urlparse
from dotenv import load_dotenv
import os
import re

class Controller:
    def exception_handler(func):
        def _wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception as error:
                print(error)
        return _wrapper

    @exception_handler
    def __init__(self) -> None:
        load_dotenv()
        rutracker_client = RutrackerApi()
        rutracker_client.login(
            username=os.environ.get('RUTRACKER_LOGIN'), 
            password=os.environ.get('RUTRACKER_PASSWORD')
        )

        self.transmission_client = TransmissionClient(
            username=os.environ.get('TRANSMISSION_LOGIN'),
            password=os.environ.get('TRANSMISSION_PASSWORD'),
            host=os.environ.get('TRANSMISSION_HOST'),
            port=os.environ.get('TRANSMISSION_PORT')
        )

    @exception_handler
    def add_torrent(self, url):
        ...

    def _parse_url(url, schema):
        ...

    def _get_rutracker_topic_id(url):
        if re.match(r'^(t=)([0-9]+)', urlparse(url).query):
            return re.findall(r'([0-9]+)', urlparse(url).query)[0]
        return None
