# https://burgaud.com/foldl-foldr-python/
# https://book.pythontips.com/en/latest/map_filter.html

import functools


def foldl(f, acc, xs):
    """
    (a -> b -> a) -> a -> [b] -> a
    It takes the second argument and the first item of the list and applies the function to them, then feeds the
    function with this result and the second argument and so on.
    :param f: function
    :param acc: accumulator
    :param xs: iterable object
    :return: (a -> b -> a) -> a -> [b] -> a
    """
    return functools.reduce(f, xs, acc)
