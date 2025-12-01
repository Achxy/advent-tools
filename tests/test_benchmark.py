"""Tests for the _benchmark module."""

import pytest

from advent._benchmark import benchmark_and_print


class TestBenchmarkAndPrint:
    def test_returns_function_result(self) -> None:
        def add(a: int, b: int) -> int:
            return a + b

        result = benchmark_and_print(add, 2, 3)
        assert result == 5

    def test_prints_timing_info(self, capsys: pytest.CaptureFixture[str]) -> None:
        def simple() -> str:
            return "hello"

        benchmark_and_print(simple)
        captured = capsys.readouterr()

        assert "simple" in captured.out
        assert "ms" in captured.out
        assert "hello" in captured.out

    def test_handles_kwargs(self) -> None:
        def greet(name: str, greeting: str = "Hello") -> str:
            return f"{greeting}, {name}!"

        result = benchmark_and_print(greet, "World", greeting="Hi")
        assert result == "Hi, World!"
