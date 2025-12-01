"""Tests for the _exceptions module."""

from advent._exceptions import (
    AdventError,
    ConfigurationError,
    DataNotFoundError,
    DateValidationError,
    DownloadError,
    SessionTokenError,
)


class TestExceptionHierarchy:
    def test_all_inherit_from_advent_error(self) -> None:
        assert issubclass(ConfigurationError, AdventError)
        assert issubclass(SessionTokenError, AdventError)
        assert issubclass(DateValidationError, AdventError)
        assert issubclass(DataNotFoundError, AdventError)
        assert issubclass(DownloadError, AdventError)

    def test_advent_error_is_exception(self) -> None:
        assert issubclass(AdventError, Exception)

    def test_can_catch_specific_exception(self) -> None:
        try:
            raise SessionTokenError("test")
        except SessionTokenError as e:
            assert str(e) == "test"

    def test_can_catch_base_exception(self) -> None:
        try:
            raise DateValidationError("test")
        except AdventError as e:
            assert str(e) == "test"
