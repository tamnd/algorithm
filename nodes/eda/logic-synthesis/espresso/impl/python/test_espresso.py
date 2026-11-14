# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/espresso/. The authors are listed in prov/70F55E.jsonl.

import itertools
import random

from espresso import complement, cost, covered, espresso, expand, irredundant, reduce, tautology


def cells(c: str) -> set[int]:
    n = len(c)
    return {m for m in range(2 ** n) if all(ch == "-" or int(ch) == (m >> (n - 1 - i)) & 1 for i, ch in enumerate(c))}


def points(cover: list[str], n: int) -> set[int]:
    out: set[int] = set()
    for c in cover:
        out |= cells(c)
    return out


def minterms(n: int, ms: set[int]) -> list[str]:
    return [format(m, "b").zfill(n) for m in sorted(ms)]


def brute_min_cost(n: int, on: set[int], dc: set[int]) -> tuple[int, int]:
    if not on:
        return (0, 0)
    allowed = on | dc
    imps = [c for c in ("".join(t) for t in itertools.product("01-", repeat=n)) if cells(c) <= allowed]
    primes = [c for c in imps if not any(cells(c) < cells(d) for d in imps)]
    masks = [sum(1 << m for m in cells(p)) for p in primes]
    lits = [sum(ch != "-" for ch in p) for p in primes]
    target = sum(1 << m for m in on)
    for k in range(1, len(primes) + 1):
        best = None
        for s in itertools.combinations(range(len(primes)), k):
            got = 0
            for j in s:
                got |= masks[j]
            if got & target == target:
                t = sum(lits[j] for j in s)
                best = t if best is None or t < best else best
        if best is not None:
            return (k, best)
    raise AssertionError("no cover")


def check(n: int, on: set[int], dc: set[int], G: list[str]) -> None:
    """G is correct on the care set, every cube is prime, and no cube is redundant."""
    allowed = on | dc
    assert on <= points(G, n) <= allowed
    for c in G:
        for i, ch in enumerate(c):
            if ch != "-":
                assert not cells(c[:i] + "-" + c[i + 1:]) <= allowed, (G, c)
        rest = [e for e in G if e != c]
        assert not (cells(c) & on) <= points(rest, n), (G, c)


def test_bcd_digit_at_least_five() -> None:
    # Inputs a b c d hold a BCD digit; codes 10 to 15 never occur.
    on, dc = {5, 6, 7, 8, 9}, set(range(10, 16))
    G = espresso(4, minterms(4, on), minterms(4, dc))
    assert sorted(G) == ["-1-1", "-11-", "1---"]
    assert cost(G) == (3, 5)


def test_cyclic_function() -> None:
    on = {0, 1, 2, 5, 6, 7}
    G = espresso(3, minterms(3, on))
    check(3, on, set(), G)
    assert len(G) in (3, 4)


def test_steps() -> None:
    F = ["000", "001", "011"]
    R = complement(F, 3)
    assert points(R, 3) == {2, 4, 5, 6, 7}
    E = expand(F, R)
    assert sorted(E) == ["0-1", "00-"]
    assert irredundant(["00-", "0-1", "001"], []) == ["00-", "0-1"]
    # The first cube in the order shrinks to its own part; the second keeps 001 then.
    assert sorted(reduce(["00-", "0-1"], [], 3)) == ["0-1", "000"]


def test_tautology_and_containment() -> None:
    assert tautology(["1-", "0-"], 2)
    assert not tautology(["1-", "-1"], 2)
    assert covered(["1-", "-1"], "11")
    assert not covered(["1-", "-1"], "0-")


def test_edges() -> None:
    assert espresso(3, []) == []
    assert espresso(3, minterms(3, set(range(8)))) == ["---"]
    assert espresso(2, ["00"], ["01", "10", "11"]) == ["--"]
    odd = {m for m in range(16) if bin(m).count("1") % 2}
    assert cost(espresso(4, minterms(4, odd))) == (8, 32)


def test_all_three_variable_functions() -> None:
    for bits in range(2 ** 8):
        on = {m for m in range(8) if bits >> m & 1}
        G = espresso(3, minterms(3, on))
        check(3, on, set(), G)
        assert cost(G) >= brute_min_cost(3, on, set())


def test_random_with_dont_cares() -> None:
    rng = random.Random(41)
    for n, trials in ((3, 150), (4, 60), (5, 25)):
        for _ in range(trials):
            on = {m for m in range(2 ** n) if rng.random() < 0.4}
            dc = {m for m in range(2 ** n) if m not in on and rng.random() < 0.2}
            G = espresso(n, minterms(n, on), minterms(n, dc))
            check(n, on, dc, G)
            if n <= 4:
                assert cost(G) >= brute_min_cost(n, on, dc)


def test_input_given_as_cubes() -> None:
    # The same function given as a cover of overlapping cubes gives a correct answer.
    F = ["1-0-", "11--", "-1-1", "0101"]
    G = espresso(4, F)
    assert points(G, 4) == points(F, 4)
    check(4, points(F, 4), set(), G)
