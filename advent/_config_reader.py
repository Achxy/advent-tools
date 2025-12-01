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

import sys
from enum import Enum, unique
from os import environ
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, TypeVar, cast

from dotenv import dotenv_values
from platformdirs import user_data_dir

from ._exceptions import ConfigurationError, SessionTokenError
from ._pedantics import check_if_can_be_well_formatted

# Define the type for toml_loads for type checking
if TYPE_CHECKING:
    from collections.abc import Callable

    _TomlLoads = Callable[[str], dict[str, Any]]

# Python 3.11+ has tomllib in stdlib
if sys.version_info >= (3, 11):
    from tomllib import loads as _toml_loads
else:
    from tomli import loads as _toml_loads  # type: ignore[import-not-found]

toml_loads = cast("_TomlLoads", _toml_loads)

_CT = TypeVar("_CT", bound="Configuration")


def get_session_token() -> str:
    """Retrieve the AOC session token from environment or .env file."""
    env: dict[str, str | None] = {**dotenv_values(), **environ}
    raw_token = env.get("AOC_SESSION")
    if raw_token:
        token = raw_token.strip()
        if token:
            return token
    raise SessionTokenError("No session token found. Set AOC_SESSION environment variable or add it to .env file.")


class UnformattedPath:
    """A path template that can be formatted with year and day values."""

    def __init__(self, path: str) -> None:
        check_if_can_be_well_formatted(path, "year", "day")
        self.unformatted_path = path

    def format_with_date(self, year: int, day: int) -> Path:
        return Path(self.unformatted_path.format(year=year, day=day))

    @staticmethod
    def join_path(year: int, day: int, *paths: "UnformattedPath | str") -> Path:
        result = Path()
        for p in paths:
            if isinstance(p, UnformattedPath):
                result /= p.format_with_date(year=year, day=day)
            else:
                result /= Path(p)
        return result


@unique
class SupportedConfigurationFormats(Enum):
    AOC_CONFIGURATION_FILE = ".advent"
    PYPROJECT_TOML = "pyproject.toml"


class Configuration:
    """Configuration manager for advent-tools."""

    DEFAULTS: ClassVar[dict[str, Any]] = {
        "DATA_PATH": (user_data_dir(appname="advent-tools"), UnformattedPath("data/{year}/{day}.txt"))
    }

    def __init__(self, file: Path, fmt: SupportedConfigurationFormats) -> None:
        self._config: dict[str, Any] = dict(self.DEFAULTS)
        self._populate(file, fmt)

    def download_path(self) -> tuple[str | UnformattedPath, ...]:
        ret: str | tuple[str | UnformattedPath, ...] = self._config["DATA_PATH"]
        if isinstance(ret, tuple):
            return ret
        return (ret,)

    def _populate(self, file: Path, fmt: SupportedConfigurationFormats) -> None:
        raw_data = toml_loads(file.read_text())
        config_data: dict[str, Any]
        if fmt is SupportedConfigurationFormats.PYPROJECT_TOML:
            tool_data = raw_data.get("tool")
            if isinstance(tool_data, dict):
                tool_dict: dict[str, Any] = tool_data
                advent_data = tool_dict.get("advent")
                config_data = advent_data if isinstance(advent_data, dict) else {}
            else:
                config_data = {}
        else:
            config_data = raw_data
        self._config.update(config_data)

    @classmethod
    def from_supported_configuration(
        cls: type[_CT],
        base_path: Path,
        formats: type[SupportedConfigurationFormats] = SupportedConfigurationFormats,
    ) -> _CT:
        supported = {fmt.value: name for name, fmt in formats.__members__.items()}
        for file in base_path.iterdir():
            if file.name in supported:
                return cls(file, formats[supported[file.name]])
        raise ConfigurationError(
            f"No configuration file found in {base_path}. Expected one of: {', '.join(supported.keys())}"
        )


def get_configuration() -> Configuration:
    """Get the configuration, lazily loaded and cached."""
    return Configuration.from_supported_configuration(Path.cwd(), SupportedConfigurationFormats)
