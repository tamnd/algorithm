# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-moment-diagram/. The authors are listed in prov/NFC4FF.jsonl.

import random

from binary_moment_diagram import BMD


def word(n: int, offset: int, width: int) -> list[int]:
    """The table of the unsigned number with bits x_offset .. x_(offset + width - 1)."""
    return [(a >> offset) & ((1 << width) - 1) for a in range(1 << n)]


def test_add_mul_against_tables() -> None:
    rng = random.Random(1995)
    checked = 0
    for _ in range(600):
        n = rng.randrange(0, 7)
        b = BMD(n)
        s = [rng.randrange(-3, 4) for _ in range(1 << n)]
        t = [rng.randrange(-3, 4) for _ in range(1 << n)]
        f, g = b.from_table(s), b.from_table(t)
        assert [b.evaluate(f, a) for a in range(1 << n)] == s
        h = b.add(f, g)
        assert h == b.from_table([x + y for x, y in zip(s, t)])
        k = b.mul(f, g)
        assert k == b.from_table([x * y for x, y in zip(s, t)])
        assert [b.evaluate(k, a) for a in range(1 << n)] == [x * y for x, y in zip(s, t)]
        b.check_invariant()
        checked += 1
    assert checked >= 500


def test_words_and_products() -> None:
    for w in range(1, 6):
        n = 2 * w
        b = BMD(n)
        x = b.from_table(word(n, 0, w))
        y = b.from_table(word(n, w, w))
        # a word: one node per bit, its weight terminal, and the terminal 0
        assert b.size(x) == 2 * w + 1
        p = b.mul(x, y)
        assert p == b.from_table([u * v for u, v in zip(word(n, 0, w), word(n, w, w))])
        # the plain BMD of x * y: w nodes for x, w nodes per y-chain, terminals 2^(i+j)
        assert b.size(p) == w + w * w + (2 * w - 1) + 1
