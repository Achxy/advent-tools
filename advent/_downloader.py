import requests

from ._pedantics import check_if_viable_date


class Downloader:
    URL_FORMAT = "https://adventofcode.com/{year}/day/{day}/input"

    def __init__(self, session_cookie: str) -> None:
        self.cookies = {"session": session_cookie}

    def get_content_for_date(self, year: int, day: int) -> str:
        check_if_viable_date(year=year, day=day)
        url = self.URL_FORMAT.format(year=year, day=day)
        return self.get_content(url)

    def get_content(self, url: str) -> str:
        req = requests.get(url, cookies=self.cookies)
        req.raise_for_status()
        return req.text
