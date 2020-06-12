from typing import Callable, List, TypeVar
from collections import Counter

T = TypeVar("T")


def list_filters(filters: List[Callable[[T], bool]], apply_to: List[T]) -> List[T]:
    """
    Apply multiple filters to list.

    Parameters
    ----------
    filters : List[Callable[[T], bool]]
        Multiple filters
    apply_to : List[T]
        A list to apply filters to.

    Returns
    -------
    List[T]
        A list after multiple filters are applied.

    Notes
    -----
    .. versionadded:: 0.1.0
    """
    l: List[T] = apply_to.copy()
    for _filter in filters:
        l = list(filter(_filter, l))
    return l


S = TypeVar("S")
T = TypeVar("T")


def compare_hashable_list(s: List[S], t: List[T]) -> bool:
    """
    Compare hashable list. O(n).

    Parameters
    ----------
    s : List[S]
        List 1
    t : List[T]
        List 2

    Returns
    -------
    bool
        True if lists are same.

    Notes
    -----
    .. versionadded:: 0.1.0

    References
    ----------
    https://stackoverflow.com/questions/7828867/how-to-efficiently-compare-two-unordered-lists-not-sets-in-python
    """
    return Counter(s) == Counter(t)


def compare_orderable_list(s: List[S], t: List[T]) -> bool:
    """
    Compare orderable list. O(n log n)

    Parameters
    ----------
    s : List[S]
        List 1
    t : List[T]
        List 2

    Returns
    -------
    bool
        True if lists are same.

    Notes
    -----
    .. versionadded:: 0.1.0

    References
    ----------
    https://stackoverflow.com/questions/7828867/how-to-efficiently-compare-two-unordered-lists-not-sets-in-python
    """
    return sorted(s) == sorted(t)
