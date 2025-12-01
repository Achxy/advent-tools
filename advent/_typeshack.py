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

Type stubs to make Advent[YEAR:DAY] syntax work with type checkers.

The Advent class uses a metaclass that overrides __getitem__ to accept
slice syntax for date specification. This module provides type hints
to make this pattern compatible with static analysis tools.

Without this, type checkers would complain about `Advent[2022:1]` since
the default Generic.__class_getitem__ expects type parameters, not slices.
"""

from typing import Generic, TypeVar

# Fake type variable used to satisfy Generic's requirement for a type parameter
FakeType = TypeVar("FakeType")

# Alias for Generic that allows our __getitem__ override to work
FakeGenericForGetItemSupport = Generic
