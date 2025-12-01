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

import json
from functools import cache

# Use importlib.resources for package data access (available since Python 3.9)
from importlib.resources import files

from ._config_reader import UnformattedPath, get_configuration, get_session_token
from ._downloader import Downloader
from ._exceptions import DateValidationError
from ._pedantics import check_if_viable_date

# Dates before this didn't have the entire example data in one piece,
# and more often than not had two separate examples for part 1 and part 2.
# To have a consistent experience and unified approach, we only support
# example data from 2020 onwards.
EXAMPLE_DATA_CUTOFF = 2020


def get(year: int, day: int) -> str | None:
    """Get cached puzzle input if it exists locally."""
    fullpath = UnformattedPath.join_path(year, day, *get_configuration().download_path())
    if fullpath.exists():
        content = fullpath.read_text()
        return content if content else None
    return None


def fetch(year: int, day: int) -> str:
    """Download puzzle input from adventofcode.com and cache it locally."""
    fullpath = UnformattedPath.join_path(year, day, *get_configuration().download_path())
    token = get_session_token()
    content = Downloader(token).get_content_for_date(year, day)
    fullpath.parent.mkdir(parents=True, exist_ok=True)
    fullpath.write_text(content)
    return content


def getch(year: int, day: int) -> str:
    """Get puzzle input from cache, or fetch and cache it if not available."""
    if data := get(year, day):
        return data
    return fetch(year, day)


@cache
def _load_example_data() -> dict[str, dict[str, str]]:
    """Load example data from package resources."""
    package_files = files("advent")
    resource = package_files.joinpath("examplary_data.json")
    content = resource.read_text()
    result: dict[str, dict[str, str]] = json.loads(content)
    return result


def get_example_data(year: int, day: int) -> str:
    """Get example puzzle input for testing solutions."""
    if year < EXAMPLE_DATA_CUTOFF:
        raise DateValidationError(
            f"Example data only available from {EXAMPLE_DATA_CUTOFF} onwards. "
            f"Earlier puzzles had inconsistent example formats."
        )
    check_if_viable_date(year, day)

    data = _load_example_data()
    year_data = data.get(str(year), {})
    day_data = year_data.get(str(day))

    if day_data is None:
        raise DateValidationError(f"No example data available for {year} day {day}")

    return day_data
