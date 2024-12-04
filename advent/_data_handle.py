from _downloader import Downloader
from _config_reader import Configuration, UnformattedPath


DOWNLOAD_PATH = Configuration.download_path


def get(year: int, day: int) -> str | None:
    fullpath = UnformattedPath.join_path(year=year, day=day)
    if fullpath.exists():
        return fullpath.read_text()

def fetch(year: int, day: int):
    fullpath = UnformattedPath.join_path(year=year, day=day)
    

def getch(year: int, day: int):
    ...
