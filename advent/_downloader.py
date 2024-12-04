from pathlib import Path

import aiofiles
import aiohttp


class Downloader:
    URL_FORMAT = "https://adventofcode.com/{year}/day/{day}/input"

    def __init__(self, *, session_cookie: str):
        self.session = aiohttp.ClientSession(cookies={"session": session_cookie})

    async def download_input_for_date(self, year: int, day: int, path: Path, overwrite: bool = False):
        if not overwrite and path.is_file():
            return
        url = f"https://adventofcode.com/{year}/day/{day}"
        return await self.download(url.format(year=year, day=day), path)

    async def download(self, url: str, path: Path):
        async with self.session.get(url) as response:
            async with aiofiles.open(path, "wt") as file:
                await file.write((await response.read()).decode("utf-8"))

    async def close(self):
        await self.session.close()
