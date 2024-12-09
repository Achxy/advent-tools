# [advent-tools](https://github.com/Achxy/advent-tools)
Python interface to conveniently download and interact with advent data with a high-level-wrapper.

### Installation
A [Virtual Environment](https://docs.python.org/3/library/venv.html) is strongly recommended to install the library

```bash
# Linux/macOS
python3 -m pip install -U advent-tools

# Windows
py -3 -m pip install -U advent-tools
```

---
### Quickstart
First we need to get the `session` cookie (🍪), in order to do that
1) Open your broswer's Devtools ([Chrome](https://developer.chrome.com/docs/devtools/open) / [Firefox](https://firefox-source-docs.mozilla.org/devtools-user/) guide)
2) Head on over to `Application` tab, then to `Cookies`
3) Find and copy `session` cookie value
!["Steps to get session cookie"](./assets/steps_to_get_session_cookie.jpg)
4) set `AOC_SESSION=<session-cookie-value>` environment variable (make sure terminal restart doesn't reset the value)\
**OR**\
Enter the following command in your terminal which will create an `.env` file storing your session cookie.
```bash
# Same for all Windows, Linux and macOS
echo AOC_SESSION=<session-cookie-value> > .env
# Make sure to replace <session-cookie-value> with your cookie value
```
Make sure version control system ignores your token container in case you are using one, cause your token is sensitive and can be used for log-ins.

---
### Usage
`year` and `day` can be given as kwargs when subclassing `advent.Advent` or can be provided using it's `__getitem__` behaviour like `Advent[year:day]`
```py
from advent import Advent


class Solution(Advent, year=2020, day=3):
    def __init__(self, data: str) -> None:
        self.data = ...

    def part_1(self):
        ...

    def part_2(self):
        ...
```
Example 1:
```py
from advent import Advent


class Solution(Advent, year=2022, day=2):
    PLAY = {"A": ["Z", "X", "Y"], "B": ["X", "Y", "Z"], "C": ["Y", "Z", "X"]}

    def __init__(self, data: str) -> None:
        self.data = [line.split() for line in data.splitlines()]

    def part_1(self):
        return sum(self.PLAY[oppo].index(me) * 3 + ord(me) - 87 for oppo, me in self.data)

    def part_2(self):
        return sum((fate := ord(res) - 88) * 3 + ord(self.PLAY[oppo][fate]) - 87 for oppo, res in self.data)
```
Example 2:
```python
from heapq import nlargest
from advent import Advent

class Solution(Advent[2022:1]):
    def __init__(self, data: str) -> None:
        self.max, *self.top = nlargest(3, [sum(map(int, chunk.split())) for chunk in data.split("\n\n")])

    def part_1(self):
        return self.max

    def part_2(self):
        return self.max + sum(self.top)
```
