from typing import Optional, Callable, List, Tuple, TypeVar

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
