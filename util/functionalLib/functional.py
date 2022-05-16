# https://burgaud.com/foldl-foldr-python/
# https://book.pythontips.com/en/latest/map_filter.html

import functools
from collections import Callable
from typing import Any


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


def compose(*functions):
    """
    (b -> c) -> (a -> b) -> a -> c
    Composes a list of functions that have exactly one parameter as argument
    :param functions: Iterable of functions
    :return: composed function
    """
    return foldl(lambda f, g: lambda x: f(g(x)), lambda x: x, functions)


def append(acc, x):
    """
    [a] -> a -> [a] ++ [a]
    Adds element to tail
    :param acc: List
    :param x: Element
    :return: A new list with x appended to its tail
    """
    return acc + [x]
