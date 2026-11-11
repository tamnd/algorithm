# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incompressibility-argument/. The authors are listed in prov/DZF65X.jsonl.
"""The counting behind the incompressibility argument, for binary strings."""

import itertools
from typing import Callable, Iterable


def all_strings(n: int) -> list[str]:
    """The 2^n binary strings of length n."""
    return ["".join(t) for t in itertools.product("01", repeat=n)]


def shorter_strings(n: int) -> list[str]:
    """The 2^n - 1 binary strings of length less than n, the empty string included."""
    return [s for m in range(n) for s in all_strings(m)]


def count_shorter(n: int) -> int:
    return (1 << n) - 1


def search_injection_into_shorter(n: int) -> tuple[dict | None, int]:
    """Backtracking search over all partial injective maps from {0,1}^n into the strings of length < n.

    Return (a map, nodes) if one exists, else (None, nodes), where nodes counts
    the partial maps that the search visited. The search is exhaustive, so a
    result of None is a proof by enumeration for this n.
    """
    sources, targets = all_strings(n), shorter_strings(n)
    used = [False] * len(targets)
    image: list[int] = []
    nodes = 0

    def go(i: int) -> bool:
        nonlocal nodes
        nodes += 1
        if i == len(sources):
            return True
        for t in range(len(targets)):
            if not used[t]:
                used[t] = True
                image.append(t)
                if go(i + 1):
                    return True
                image.pop()
                used[t] = False
        return False

    if go(0):
        return {s: targets[t] for s, t in zip(sources, image)}, nodes
    return None, nodes


def is_injective(f: Callable[[str], str], domain: Iterable[str]) -> bool:
    seen = set()
    for x in domain:
        y = f(x)
        if y in seen:
            return False
        seen.add(y)
    return True


def max_compressed_by(n: int, c: int) -> int:
    """The most n-bit strings that one injective map can send to strings of length at most n - c.

    This is the number of strings of length at most n - c, which is 2^(n - c + 1) - 1, for 1 <= c <= n.
    """
    if not 1 <= c <= n:
        raise ValueError("need 1 <= c <= n")
    return (1 << (n - c + 1)) - 1


def max_compressed_by_prefix_free(n: int, c: int) -> int:
    """The same count when the outputs must form a prefix-free set: at most 2^(n - c), by the Kraft inequality."""
    if not 0 <= c <= n:
        raise ValueError("need 0 <= c <= n")
    return 1 << (n - c)
