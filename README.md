# Transmission Remote Core

This is an interface class through which you can interact with remote transmission-daemon

## Installation
Just clone this repository into your project folder

```bash
cd /path/to/your/project
git clone https://github.com/fqrmix/transmission_remote_core.git
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
