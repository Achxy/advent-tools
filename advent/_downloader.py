"""
MIT License

Copyright (c) 2022-present Achyuth Jayadevan <achyuth@jayadevan.in>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

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
