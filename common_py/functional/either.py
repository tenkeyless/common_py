from __future__ import annotations

# https://github.com/alleycat-at-git/monad/blob/master/python/src/either.py
from typing import TypeVar, Generic, Callable, Optional
from common_py.functional.monad import Monad


R = TypeVar("R")
R2 = TypeVar("R2")
L = TypeVar("L")


class Either(Monad, Generic[R, L]):
    def __init__(self, right: Optional[R], left: Optional[L]):
        self.right: R = right
        self.left: L = left

    # pure :: a -> Either a
    @staticmethod
    def pure(right: R) -> Either[R, L]:
        return Right(right)

    # flat_map :: # Either a -> (a -> Either b) -> Either b
    def flat_map(self, f: Callable[[R], Either[R2, L]]) -> Either[R2, L]:
        if self.left is not None:
            return self
        else:
            return f(self.right)


class Right(Either):
    def __init__(self, right: R):
        super(Right, self).__init__(right, None)


class Left(Either):
    def __init__(self, left: L):
        super(Left, self).__init__(None, left)
