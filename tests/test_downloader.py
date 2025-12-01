"""Tests for the _downloader module."""

# respx library has incomplete type stubs for the respond() method
# pyright: reportUnknownMemberType=false
import httpx
import pytest
import respx

from advent._downloader import Downloader
from advent._exceptions import DownloadError


class TestDownloader:
    def test_initializes_with_session_cookie(self) -> None:
        dl = Downloader("test-session")
        assert dl.cookies == {"session": "test-session"}

    def test_custom_timeout(self) -> None:
        dl = Downloader("test", timeout=60.0)
        assert dl.timeout == 60.0

    def test_has_user_agent(self) -> None:
        dl = Downloader("test")
        assert "User-Agent" in dl.headers
        assert "advent-tools" in dl.headers["User-Agent"]

    @respx.mock
    def test_get_content_success(self) -> None:
        url = "https://adventofcode.com/2022/day/1/input"
        respx.get(url).respond(text="puzzle input data")

        dl = Downloader("valid-session")
        # Use get_content directly to avoid date validation
        result = dl.get_content(url)

        assert result == "puzzle input data"

    @respx.mock
    def test_get_content_400_error(self) -> None:
        url = "https://example.com/test"
        respx.get(url).respond(status_code=400)

        dl = Downloader("invalid-session")
        with pytest.raises(DownloadError, match=r"Bad request.*invalid or expired session token"):
            dl.get_content(url)

    @respx.mock
    def test_get_content_404_error(self) -> None:
        url = "https://example.com/test"
        respx.get(url).respond(status_code=404)

        dl = Downloader("session")
        with pytest.raises(DownloadError, match="not found"):
            dl.get_content(url)

    @respx.mock
    def test_get_content_network_error(self) -> None:
        url = "https://example.com/test"
        respx.get(url).mock(side_effect=httpx.ConnectError("Connection failed"))

        dl = Downloader("session")
        with pytest.raises(DownloadError, match="Network error"):
            dl.get_content(url)
