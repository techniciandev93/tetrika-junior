from functools import wraps
from inspect import signature
from typing import get_type_hints


def strict(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = signature(func)
        related_args = sig.bind(*args, **kwargs)
        type_hints = get_type_hints(func)
        for argument, value in related_args.arguments.items():
            if not isinstance(value, type_hints[argument]):
                raise TypeError(
                    f"Аргумент '{argument}': не соответствует аннотации {type_hints[argument]},"
                    f" получен {type(value)} (значение: {repr(value)})"
                )
        result = func(*args, **kwargs)
        return result
    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


def run_tests():
    try:
        assert sum_two(1, 2) == 3
        print("Test 1 passed")
    except AssertionError:
        print("Test 1 failed: sum_two(1, 2) != 3")

    try:
        sum_two(1, 2.4)
        print("Test 2 failed: sum_two(1, 2.4) did not raise TypeError")
    except TypeError:
        print("Test 2 passed")

    try:
        sum_two("1", "2")
        print("Test 3 failed: sum_two('1', '2') did not raise TypeError")
    except TypeError:
        print("Test 3 passed")

    try:
        sum_two(None, None)
        print("Test 4 failed: sum_two(None, None) did not raise TypeError")
    except TypeError:
        print("Test 4 passed")


if __name__ == '__main__':
    run_tests()
