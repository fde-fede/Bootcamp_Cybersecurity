from collections.abc import Iterable

def ft_reduce(function_to_apply, iterable):
    """Apply function of two arguments cumulatively.
    Args:
        function_to_apply: a function taking an iterable.
        iterable: an iterable object (list, tuple, iterator).
    Return:
        A value, of same type of elements in the iterable parameter.
        None if the iterable can not be used by the function.
    """
    if not isinstance(iterable, Iterable):
        raise TypeError("Expected an iterable")
    if not iterable:
        raise TypeError("reduce() of empty sequence with no initial value")
    for i, elem in enumerate(iterable):
        if i:
            reduced = function_to_apply(reduced, elem)
        else:
            reduced = elem
    return reduced