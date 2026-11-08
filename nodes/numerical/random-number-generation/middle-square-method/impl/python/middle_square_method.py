# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/middle-square-method/. The authors are listed in prov/0TYC2R.jsonl.

"""Von Neumann's middle-square method for n-digit numbers in base b (n even)."""


def middle_square_step(x: int, n: int, base: int = 10) -> int:
    """The middle n digits of the 2n-digit square of x (padded with leading zeros)."""
    if n <= 0 or n % 2:
        raise ValueError("n must be a positive even number")
    if not 0 <= x < base**n:
        raise ValueError("x must have at most n digits")
    sq = x * x  # @line L1
    return (sq // base ** (n // 2)) % base**n  # @line L2


class MiddleSquare:
    def __init__(self, seed: int, n: int, base: int = 10) -> None:
        middle_square_step(seed, n, base)  # validates the arguments
        self.x, self.n, self.base = seed, n, base

    def next(self) -> int:
        self.x = middle_square_step(self.x, self.n, self.base)  # @line L3
        return self.x  # @line L4

    def uniform(self) -> float:
        return self.next() / self.base**self.n


def tail_and_period(f, s: int) -> tuple[int, int]:
    """(mu, rho) of the sequence s, f(s), f(f(s)), ... by recording first visits."""
    seen: dict[int, int] = {}
    i = 0
    while s not in seen:
        seen[s] = i
        s = f(s)
        i += 1
    return seen[s], i - seen[s]


def cycles(f, size: int) -> list[tuple[int, int]]:
    """All cycles of f on range(size), as (length, smallest member), sorted. Iterative."""
    color = bytearray(size)  # 0 new, 1 on the current path, 2 done
    out = []
    for s in range(size):
        if color[s]:
            continue
        path = []
        x = s
        while not color[x]:
            color[x] = 1
            path.append(x)
            x = f(x)
        if color[x] == 1:
            cyc = path[path.index(x):]
            out.append((len(cyc), min(cyc)))
        for y in path:
            color[y] = 2
    return sorted(out)
