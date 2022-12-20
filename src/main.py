from core.rutracker_api import RutrackerApi

api = RutrackerApi()

api.login("username", "password")
search = api.search("test request")

print(search)
