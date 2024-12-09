# [advent-tools](https://github.com/Achxy/advent-tools)
Python interface to conveniently download and interact with advent data with a high-level-wrapper.

### Installation
Note: A [Virtual Environment](https://docs.python.org/3/library/venv.html) is strongly recommended to install the library

```bash
# Linux/macOS
python3 -m pip install -U advent-tools

# Windows
py -3 -m pip install -U advent-tools
```

### Quickstart
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