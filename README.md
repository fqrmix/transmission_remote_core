# Transmission Remote Core

This is an interface class through which you can interact with remote transmission-daemon

## Installation
1) Clone this repository into your project folder

```bash
cd /path/to/your/project
git clone https://github.com/fqrmix/transmission_remote_core.git
```
2) Create .env file into transmission_remote_core/core/controller which must include auth data
```bash
touch ./transmission_remote_core/src/core/controller/.env &&\
echo -e \
"RUTRACKER_LOGIN=*RuTracker username*
RUTRACKER_PASSWORD=*RuTracker password*\n
TRANSMISSION_HOST=*transmission-daemon host*
TRANSMISSION_PORT=*transmission-daemon port*
TRANSMISSION_LOGIN=*transmission-daemon username*
TRANSMISSION_PASSWORD=*transmission-daemon password*" >> ./transmission_remote_core/src/core/controller/.env
```


## Usage
```python
from transmission_remote_core.src import TransmissionFacade
...

transmission_facade = TransmissionFacade()

url = 'https://rutracker.org/...' # Path to RuTracker topic
# Also you can use magnet link and direct link to .torrent_file

torrent_object = transmission_facade.get_torrent_object(url)
transmission_facade.add_torrent(torrent_object)

print(transmission_facade.get_torrent_list())

```
