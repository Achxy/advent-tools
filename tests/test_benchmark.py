"""Tests for the _benchmark module."""

import io
import sys

from advent._benchmark import benchmark_and_print


class TestBenchmarkAndPrint:
    def test_returns_function_result(self) -> None:
        def add(a: int, b: int) -> int:
            return a + b

        result = benchmark_and_print(add, 2, 3)
        assert result == 5

    def test_prints_timing_info(self) -> None:
        def simple() -> str:
            return "hello"

        captured = io.StringIO()
        sys.stdout = captured
        try:
            benchmark_and_print(simple)
        finally:
            sys.stdout = sys.__stdout__

        output = captured.getvalue()
        assert "simple" in output
        assert "ms" in output
        assert "hello" in output

    def test_handles_kwargs(self) -> None:
        def greet(name: str, greeting: str = "Hello") -> str:
            return f"{greeting}, {name}!"

        result = benchmark_and_print(greet, "World", greeting="Hi")
        assert result == "Hi, World!"
