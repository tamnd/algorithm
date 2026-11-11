# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/collision-finding/. The authors are listed in prov/45XBR0.jsonl.
"""Three generic collision finders on an n-bit function, with their costs counted.

For study only. The code is not constant time, and it runs only on SHA-256
truncated to a few bits, a toy target. For real hashing use SHA-256 or SHA-3
from the standard library (hashlib), a FIPS 140 validated module, or libsodium.

Each finder returns (x1, x2, evaluations, stored): x1 != x2 with f(x1) == f(x2),
the number of calls of f, and the peak number of items held in memory.

  table_search      the plain birthday attack: about 1.25 * 2^(n/2) calls, as many stored
  rho_search        Floyd cycle finding on x -> f(x): about 3 * 1.25 * 2^(n/2) calls, O(1) stored
  dp_search         van Oorschot and Wiener distinguished points: walks stop at points
                    whose low d bits are zero; about 2^(n/2) + 2^(d+1) calls, about 2^(n/2 - d) stored
"""

import hashlib
import random
from typing import Callable

Fn = Callable[[int], int]


def truncated_sha256(n: int, salt: bytes = b"") -> Fn:
    """f(x) = top n bits of SHA-256(salt || x as 8 bytes), as an integer below 2^n."""
    nbytes = (n + 7) // 8

    def f(x: int) -> int:
        d = hashlib.sha256(salt + x.to_bytes(8, "big")).digest()
        return int.from_bytes(d[:nbytes], "big") >> (8 * nbytes - n)

    return f


def table_search(f: Fn, n: int, rng: random.Random) -> tuple[int, int, int, int]:
    seen: dict[int, int] = {}
    calls = 0
    while True:
        x = rng.getrandbits(n)
        y = f(x)
        calls += 1
        if y in seen and seen[y] != x:
            return seen[y], x, calls, len(seen)
        seen[y] = x


def rho_search(f: Fn, x0: int) -> tuple[int, int, int, int] | None:
    """Floyd on x -> f(x) from x0 (inputs are n-bit integers). None if x0 is on the cycle."""
    calls = 0

    def g(x: int) -> int:
        nonlocal calls
        calls += 1
        return f(x)

    tortoise, hare = g(x0), g(g(x0))
    while tortoise != hare:
        tortoise, hare = g(tortoise), g(g(hare))
    tortoise = x0
    if tortoise == hare:
        return None
    while True:
        a, b = g(tortoise), g(hare)
        if a == b:
            return tortoise, hare, calls, 2
        tortoise, hare = a, b


def dp_search(f: Fn, n: int, d: int, rng: random.Random, max_walk: int | None = None) -> tuple[int, int, int, int]:
    """Distinguished points: walk x -> f(x) until the low d bits are zero; store
    (point -> start, length). Two walks that reach one point merged; replay them."""
    mask = (1 << d) - 1
    limit = max_walk or 20 << d
    table: dict[int, tuple[int, int]] = {}
    calls = 0
    while True:
        start = x = rng.getrandbits(n)
        steps = 0
        while x & mask and steps < limit:
            x = f(x)
            calls += 1
            steps += 1
        if x & mask:
            continue  # the walk fell into a cycle with no distinguished point; drop it
        if x in table:
            s2, l2 = table[x]
            found, extra = _locate(f, start, steps, s2, l2)
            calls += extra
            if found is not None:
                return found[0], found[1], calls, len(table)
            continue  # the second walk started on the first walk (a "Robin Hood"); go on
        table[x] = (start, steps)


def _locate(f: Fn, a: int, la: int, b: int, lb: int) -> tuple[tuple[int, int] | None, int]:
    """Two walks of lengths la and lb end at one point. Align them and step until they meet."""
    calls = 0
    while la > lb:
        a, la, calls = f(a), la - 1, calls + 1
    while lb > la:
        b, lb, calls = f(b), lb - 1, calls + 1
    if a == b:
        return None, calls
    while True:
        fa, fb = f(a), f(b)
        calls += 2
        if fa == fb:
            return (a, b), calls
        a, b = fa, fb
