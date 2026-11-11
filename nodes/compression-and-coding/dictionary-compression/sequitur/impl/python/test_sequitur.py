# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sequitur/. The authors are listed in prov/ZP2YY9.jsonl.

import random

from sequitur import Sequitur, expand, sequitur, size


def invariant_error(g):
    """Check digram uniqueness and rule utility by brute force. Return None if both hold."""
    seen = {}
    for rid, body in g.items():
        for i in range(len(body) - 1):
            seen.setdefault((body[i], body[i + 1]), []).append((rid, i))
    for key, places in seen.items():
        for a in range(len(places)):
            for b in range(a + 1, len(places)):
                (r1, i1), (r2, i2) = places[a], places[b]
                if not (r1 == r2 and abs(i1 - i2) == 1):  # only overlaps such as aaa may repeat
                    return f"digram {key} occurs at {places}"
    uses = {}
    for body in g.values():
        for s in body:
            if s < 0:
                uses[-s] = uses.get(-s, 0) + 1
    for rid, body in g.items():
        if rid and uses.get(rid, 0) < 2:
            return f"rule {rid} is used {uses.get(rid, 0)} times"
        if rid and len(body) < 2:
            return f"rule {rid} is too short"
    if set(uses) - set(g):
        return "a use of a deleted rule"
    return None


def run_checked(w):
    s = Sequitur()
    for i, c in enumerate(w):
        s.append(c)
        g = s.grammar()
        err = invariant_error(g)
        assert err is None, (w[: i + 1], err)
        assert expand(g) == list(w[: i + 1])
    return s.grammar()


def test_worked_example() -> None:
    w = [ord(c) for c in "abcdbcabcd"]
    g = run_checked(w)
    a, b, c, d = map(ord, "abcd")
    assert g == {0: [-3, -1, -3], 1: [b, c], 3: [a, -1, d]}
    assert size(g) == 8


def test_edges() -> None:
    assert sequitur([]) == {0: []}
    assert sequitur([4]) == {0: [4]}
    assert sequitur([4, 4]) == {0: [4, 4]}
    assert sequitur([4, 4, 4]) == {0: [4, 4, 4]}  # the two digrams overlap
    assert sequitur([4, 4, 4, 4]) == {0: [-1, -1], 1: [4, 4]}
    for n in range(0, 70):
        run_checked([0] * n)


def test_long_runs_and_fibonacci() -> None:
    w = [0] * 300 + [1] * 200 + [0] * 300
    assert expand(sequitur(w)) == w
    a, b = [0], [0, 1]
    while len(b) < 1597:
        a, b = b, b + a
    g = sequitur(b)
    assert expand(g) == b
    assert invariant_error(g) is None
    assert len(g) == 13 and size(g) == 35
    run_checked(b[:233])


def test_random_invariants_after_each_symbol() -> None:
    rng = random.Random(7)
    for _ in range(500):
        n = rng.randrange(0, 50)
        k = rng.choice([1, 2, 2, 3, 4])
        w = [rng.randrange(k) for _ in range(n)]
        if rng.random() < 0.3:
            w = [s for s in w for _ in range(rng.randrange(1, 5))]
        if rng.random() < 0.2 and w:
            u = w[: rng.randrange(1, 6)]
            w = (u * 20)[:n]
        run_checked(w)


def test_random_round_trip() -> None:
    rng = random.Random(31)
    for _ in range(300):
        n = rng.randrange(1, 400)
        w = [rng.randrange(3) for _ in range(rng.randrange(1, 12))]
        while len(w) < n:
            i = rng.randrange(len(w))
            j = rng.randrange(i, len(w) + 1)
            w += w[i:j] if j > i else [rng.randrange(3)]
        g = sequitur(w)
        assert expand(g) == w
        assert invariant_error(g) is None


def test_bad_input() -> None:
    try:
        sequitur([1, -2])
    except ValueError:
        return
    raise AssertionError("a negative terminal must be rejected")
