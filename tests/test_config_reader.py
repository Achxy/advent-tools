"""Tests for the _config_reader module."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from advent._config_reader import (
    UnformattedPath,
    get_session_token,
)
from advent._exceptions import SessionTokenError


class TestGetSessionToken:
    def test_returns_token_from_env(self) -> None:
        with patch.dict(os.environ, {"AOC_SESSION": "test-token"}, clear=False):
            token = get_session_token()
            assert token == "test-token"

    def test_raises_when_missing(self) -> None:
        with (
            patch.dict(os.environ, {}, clear=True),
            patch("advent._config_reader.dotenv_values", return_value={}),
            pytest.raises(SessionTokenError, match="No session token"),
        ):
            get_session_token()

    def test_strips_whitespace(self) -> None:
        with patch.dict(os.environ, {"AOC_SESSION": "  token-with-spaces  "}, clear=False):
            token = get_session_token()
            assert token == "token-with-spaces"


class TestUnformattedPath:
    def test_format_with_date(self) -> None:
        uf = UnformattedPath("data/{year}/{day}.txt")
        result = uf.format_with_date(2022, 1)
        assert result == Path("data/2022/1.txt")

    def test_invalid_format_string_raises(self) -> None:
        with pytest.raises(ValueError, match="missing keys"):
            UnformattedPath("data/{invalid}/file.txt")

    def test_join_path_mixed(self) -> None:
        base = "/tmp"
        pattern = UnformattedPath("{year}/{day}")

        result = UnformattedPath.join_path(2022, 5, base, pattern, "input.txt")
        assert result == Path("/tmp/2022/5/input.txt")

    def test_join_path_strings_only(self) -> None:
        result = UnformattedPath.join_path(2022, 5, "a", "b", "c")
        assert result == Path("a/b/c")
