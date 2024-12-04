from __future__ import annotations

from enum import UNIQUE, Enum, EnumMeta, verify
from os import PathLike
from pathlib import Path
from tomllib import load, loads
from typing import Callable, KeysView, TypeVar, ValuesView

from _pedantics import check_if_can_be_well_formatted
from platformdirs import user_data_dir, user_data_path

_CT = TypeVar("_CT", bound="Configuration")


class UnformattedPath:
    def __init__(self, path: str) -> None:
        check_if_can_be_well_formatted(path, "year", "day")
        self.unformatted_path = path

    def format_with_date(self, year: int, day: int):
        return Path(self.unformatted_path.format(year=year, day=day))

    @staticmethod
    def join_path(year: int, day: int, *paths: PathLike | UnformattedPath | str):
        path = Path()
        for p in paths:
            if isinstance(p, UnformattedPath):
                path /= p.format_with_date(year=year, day=day)
                continue
            path /= p
        return path


@verify(UNIQUE)
class SupportedConfigurationFormats(Enum):
    AOC_CONFIGURATION_FILE = ".advent"
    PYPROJECT_TOML = "pyproject.toml"


class Configuration:
    DEFAULTS = {"DATA_PATH": (user_data_dir(appname="advent-tools"), UnformattedPath("/data/{year}/{date}.txt"))}

    def __init__(self, file: Path, format: SupportedConfigurationFormats):
        self._config = self.DEFAULTS
        self._populate(file, format)

    def download_path(self) -> tuple[str | UnformattedPath, ...]:
        ret = self._config["DATA_PATH"]
        if isinstance(ret, tuple):
            return ret
        return (ret,)

    def _populate(self, file: Path, format: SupportedConfigurationFormats):
        with open(file, "rt") as fp:
            data = loads(fp.read())
            if format is format.PYPROJECT_TOML:
                data = data.get("tool", {}).get("advent", {})
        self._config.update(data)

    @classmethod
    def from_supported_configuration(
        cls: type[_CT], base_path: Path, format: type[SupportedConfigurationFormats] = SupportedConfigurationFormats
    ) -> _CT:
        supported = {supportedfile.value: key for key, supportedfile in format.__members__.items()}
        for file in base_path.iterdir():
            if file.name in supported:
                print(f"Found {file.name}")
                return cls(file, format[supported[file.name]])
        raise FileNotFoundError(f"Could not find any of the supported configuration files: {supported} in {base_path}")


print(Configuration.from_supported_configuration(Path.cwd()))