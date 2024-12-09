from ._config_reader import CONFIGURATION, UnformattedPath, get_session_token
from ._downloader import Downloader


def get(year: int, day: int) -> str | None:
    fullpath = UnformattedPath.join_path(year, day, *CONFIGURATION.download_path())
    if fullpath.exists():
        return fullpath.read_text() or None


def fetch(year: int, day: int) -> str:
    fullpath = UnformattedPath.join_path(year, day, *CONFIGURATION.download_path())
    token = get_session_token()
    content: str = Downloader(token).get_content_for_date(year, day)
    fullpath.parent.mkdir(parents=True, exist_ok=True)
    fullpath.write_text(content)
    return content


def getch(year: int, day: int) -> str:
    if data := get(year, day):
        return data
    return fetch(year, day)


def get_example_data(year: int, day: int) -> str:
    raise NotImplementedError("Example data not implemented yet")
