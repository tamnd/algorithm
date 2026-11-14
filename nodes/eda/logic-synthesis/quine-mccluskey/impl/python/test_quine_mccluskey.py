# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quine-mccluskey/. The authors are listed in prov/N0CYS5.jsonl.

import itertools
import random

from quine_mccluskey import cost, cube_minterms, minimum_cover, prime_implicants, quine_mccluskey


def all_cubes(n: int) -> list[str]:
    return ["".join(t) for t in itertools.product("01-", repeat=n)]


def mask(c: str) -> int:
    out = 0
    for m in cube_minterms(c):
        out |= 1 << m
    return out


def brute_primes(n: int, on: set[int], dc: set[int]) -> list[str]:
    """Every cube inside on | dc that no larger such cube contains."""
    allowed = sum(1 << m for m in on | dc)
    imps = [c for c in all_cubes(n) if mask(c) & ~allowed == 0 and mask(c)]
    out = []
    for c in imps:
        bigger = (c[:i] + "-" + c[i + 1:] for i in range(n) if c[i] != "-")
        if not any(mask(d) & ~allowed == 0 for d in bigger):
            out.append(c)
    return sorted(out)


def brute_min_cost(n: int, on: set[int], dc: set[int]) -> tuple[int, int]:
    """The least (cubes, literals) over all sets of implicants that cover the on-set."""
    if not on:
        return (0, 0)
    allowed = sum(1 << m for m in on | dc)
    target = sum(1 << m for m in on)
    imps = [c for c in all_cubes(n) if mask(c) and mask(c) & ~allowed == 0]
    masks = [mask(c) for c in imps]
    lits = [sum(ch != "-" for ch in c) for c in imps]
    for k in range(1, len(imps) + 1):
        best = None
        for combo in itertools.combinations(range(len(imps)), k):
            got = 0
            for j in combo:
                got |= masks[j]
            if got & target == target:
                s = sum(lits[j] for j in combo)
                if best is None or s < best:
                    best = s
        if best is not None:
            return (k, best)
    raise AssertionError("no cover")


def is_cover(n: int, cover: list[str], on: set[int], dc: set[int]) -> bool:
    got: set[int] = set()
    for c in cover:
        got |= set(cube_minterms(c))
    return on <= got <= on | dc


def test_textbook_example() -> None:
    # f = sum of m(4, 8, 10, 11, 12, 15) + d(9, 14)
    on, dc = {4, 8, 10, 11, 12, 15}, {9, 14}
    assert sorted(prime_implicants(4, on, dc)) == sorted(["-100", "10--", "1--0", "1-1-"])
    cover = quine_mccluskey(4, on, dc)
    # Two covers tie at 3 cubes and 7 literals.
    assert cover in (["-100", "10--", "1-1-"], ["-100", "1--0", "1-1-"])
    assert cost(cover) == (3, 7)


def test_cyclic_core() -> None:
    # Every minterm is in two primes and no prime is essential.
    on = {0, 1, 2, 5, 6, 7}
    assert sorted(prime_implicants(3, on)) == sorted(["-01", "0-0", "00-", "1-1", "11-", "-10"])
    cover = quine_mccluskey(3, on)
    assert cost(cover) == (3, 6)
    assert is_cover(3, cover, on, set())


def test_edges() -> None:
    assert quine_mccluskey(3, set()) == []
    assert quine_mccluskey(3, set(range(8))) == ["---"]
    assert quine_mccluskey(2, {0}, {1, 2, 3}) == ["--"]
    assert quine_mccluskey(0, {0}) == [""]
    # Parity needs every minterm as its own cube.
    odd = {m for m in range(16) if bin(m).count("1") % 2}
    assert cost(quine_mccluskey(4, odd)) == (8, 32)


def test_primes_against_brute_force() -> None:
    rng = random.Random(7)
    for n in range(1, 5):
        for _ in range(60):
            on = {m for m in range(2 ** n) if rng.random() < 0.4}
            dc = {m for m in range(2 ** n) if m not in on and rng.random() < 0.2}
            assert sorted(prime_implicants(n, on, dc)) == brute_primes(n, on, dc)


def test_all_three_variable_functions() -> None:
    for bits in range(2 ** 8):
        on = {m for m in range(8) if bits >> m & 1}
        cover = quine_mccluskey(3, on)
        assert is_cover(3, cover, on, set())
        assert cost(cover) == brute_min_cost(3, on, set())


def test_random_with_dont_cares() -> None:
    rng = random.Random(11)
    for n, trials in ((3, 200), (4, 80)):
        for _ in range(trials):
            on = {m for m in range(2 ** n) if rng.random() < 0.35}
            dc = {m for m in range(2 ** n) if m not in on and rng.random() < 0.25}
            cover = quine_mccluskey(n, on, dc)
            assert is_cover(n, cover, on, dc)
            assert set(cover) <= set(prime_implicants(n, on, dc))
            assert cost(cover) == brute_min_cost(n, on, dc)


def test_minimum_cover_given_primes() -> None:
    on = {0, 1, 2, 5, 6, 7}
    primes = prime_implicants(3, on)
    cover = minimum_cover(on, primes)
    assert len(cover) == 3 and is_cover(3, cover, on, set())
