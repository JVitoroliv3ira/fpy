from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, TypeVar, Generic
from dataclasses import dataclass

T = TypeVar('T')
U = TypeVar('U')

class Option(Generic[T], ABC):
    @abstractmethod
    def is_some(self) -> bool: ... # pragma: no cover

    def is_none(self) -> bool:
        return not self.is_some()

    @abstractmethod
    def unwrap(self) -> T: ... # pragma: no cover

    @abstractmethod
    def unwrap_or(self, default: T) -> T: ... # pragma: no cover

    @abstractmethod
    def map(self, fn: Callable[[T], U]) -> Option[U]: ... # pragma: no cover


@dataclass(frozen=True)
class Some(Option[T]):
    value: T

    def is_some(self) -> bool:
        return True

    def unwrap(self) -> T:
        return self.value

    def unwrap_or(self, default: T) -> T:
        _ = default
        return self.value 

    def map(self, fn: Callable[[T], U]) -> Option[U]:
        return Some(fn(self.value))


@dataclass(frozen=True)
class Nothing(Option[T]):
    def is_some(self) -> bool:
        return False

    def unwrap(self) -> T:
        raise ValueError('Called unwrap on Nothing')

    def unwrap_or(self, default: T) -> T:
        return default

    def map(self, fn: Callable[[T], U]) -> Option[U]:
        _ = fn
        return Nothing()


def some(value: T) -> Option[T]:
    return Some(value)

def nothing() -> Option:
    return Nothing()

def from_optional(value: T | None) -> Option[T]:
    return Some(value) if value is not None else Nothing()

