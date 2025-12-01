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

import httpx

from ._exceptions import DownloadError
from ._pedantics import check_if_viable_date

# Be respectful to the AOC servers
DEFAULT_TIMEOUT = 30.0
USER_AGENT = "advent-tools/1.0 (https://github.com/Achxy/advent-tools)"


class Downloader:
    """Downloads puzzle input from adventofcode.com."""

    URL_FORMAT = "https://adventofcode.com/{year}/day/{day}/input"

    def __init__(self, session_cookie: str, *, timeout: float = DEFAULT_TIMEOUT) -> None:
        self.cookies = {"session": session_cookie}
        self.timeout = timeout
        self.headers = {"User-Agent": USER_AGENT}

    def get_content_for_date(self, year: int, day: int) -> str:
        """Download puzzle input for a specific date."""
        check_if_viable_date(year=year, day=day)
        url = self.URL_FORMAT.format(year=year, day=day)
        return self.get_content(url)

    def get_content(self, url: str) -> str:
        """Perform HTTP GET request and return response text."""
        try:
            response = httpx.get(
                url,
                cookies=self.cookies,
                headers=self.headers,
                timeout=self.timeout,
                follow_redirects=True,
            )
            response.raise_for_status()
            return response.text
        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            if status == 400:
                raise DownloadError(
                    "Bad request (HTTP 400). This often indicates an invalid or expired session token."
                ) from exc
            if status == 404:
                raise DownloadError(f"Puzzle not found at {url}. The puzzle may not exist yet.") from exc
            if status == 500:
                raise DownloadError("Server error (HTTP 500). The Advent of Code server may be overloaded.") from exc
            raise DownloadError(f"HTTP error {status}: {exc}") from exc
        except httpx.RequestError as exc:
            raise DownloadError(f"Network error while fetching {url}: {exc}") from exc
