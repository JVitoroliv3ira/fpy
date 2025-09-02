import pytest
from typing import Optional
from fpy.option import Option, Some, Nothing, some, nothing, from_optional

class TestSome:
    def test_is_some(self) -> None:
        option = Some('foo')
        assert option.is_some()

    def test_is_not_none(self) -> None:
        option = Some('bar')
        assert not option.is_none()

    def test_unwrap_value(self) -> None:
        expected = 'baz'
        option = Some('baz')
        assert option.unwrap() == expected

    def test_equality(self) -> None:
        assert Some(314) == Some(314)

    def test_inequality(self) -> None:
        assert Some('abc') != Some('xyz')

    def test_unwrap_or_keeps_value(self) -> None:
        expected = 314
        option = Some(314)
        assert option.unwrap_or(628) == expected

    def test_unwrap_or_keeps_none_value(self) -> None:
        option: Option[Optional[int]] = Some(None)
        assert option.unwrap_or(314) is None

    def test_map_applies_function(self) -> None:
        option = Some('foo')
        result = option.map(str.upper)
        assert isinstance(result, Option)
        assert result == Some('FOO')

    def test_identity(self) -> None:
        option = Some(314)
        identity = lambda x: x
        assert option.map(identity) == option

    def test_composition(self) -> None:
        option = Some('foo')
        f = len
        g = lambda n: n * 2
        left = option.map(f).map(g)
        right = option.map(lambda x: g(f(x)))
        assert left == right


class TestNothing:
    def test_is_not_some(self) -> None:
        option = Nothing()
        assert not option.is_some()

    def test_is_none(self) -> None:
        option = Nothing()
        assert option.is_none()

    def test_unwrap_raises_error(self) -> None:
        option = Nothing()
        with pytest.raises(ValueError, match='unwrap'):
            option.unwrap()

    def test_equality(self) -> None:
        assert Nothing() == Nothing()

    def test_inequality(self) -> None:
        assert Nothing() != Some('xyz')

    def test_unwrap_or_returns_default(self) -> None:
        assert Nothing().unwrap_or('bar') == 'bar'

    def test_map_returns_nothing(self) -> None:
        option = Nothing()
        result =  option.map(lambda x: x + 5)
        assert isinstance(result, Nothing)
        assert result.is_none()


class TestSomeHelper:
    def test_returns_option_instance(self) -> None:
        option = some('foo')
        assert isinstance(option, Option)

    def test_result_is_some(self) -> None:
        option = some('bar')
        assert option.is_some()

    def test_result_is_not_none(self) -> None:
        option = some('baz')
        assert not option.is_none()

    def test_result_unwrap_value(self) -> None:
        expected = 'foo'
        option = some('foo')
        assert option.unwrap() == expected


class TestNothingHelper:
    def test_returns_option_instance(self) -> None:
        option = nothing()
        assert isinstance(option, Option)

    def test_is_not_some(self) -> None:
        option = nothing()
        assert not option.is_some()

    def test_is_none(self) -> None:
        option = nothing()
        assert option.is_none()

    def test_unwrap_raises_error(self) -> None:
        option = nothing()
        with pytest.raises(ValueError, match='unwrap'):
            option.unwrap()


class TestFromOptional:
    def test_with_value_returns_some(self):
        option = from_optional('foo')
        assert isinstance(option, Some) 
        assert option.is_some()

    def test_with_no_value_returns_nothing(self):
        option = from_optional(None)
        assert isinstance(option, Nothing)
        assert option.is_none()


