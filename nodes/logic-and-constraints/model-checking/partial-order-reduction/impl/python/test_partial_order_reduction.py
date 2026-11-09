# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partial-order-reduction/. The authors are listed in prov/K3M7D5.jsonl.

import random

from partial_order_reduction import full_search, partial_order_reduction, reduced_search


def random_program(rng, loops: bool):
    prog = []
    for _ in range(rng.randint(2, 3)):
        code = []
        for k in range(rng.randint(1, 4)):
            r = rng.random()
            if r < 0.3:
                code.append(("w", rng.randrange(2), rng.randint(1, 2)))
            elif r < 0.45:
                code.append(("r", rng.randrange(2)))
            elif r < 0.55:
                code.append(("wr", rng.randrange(2)))
            elif r < 0.7:
                code.append(("lock", rng.randrange(2)))
            elif r < 0.85:
                code.append(("unlock", rng.randrange(2)))
            elif loops and k > 0:
                code.append(("jmp", rng.randrange(k)))
            else:
                code.append(("w", 2 + rng.randrange(2), 1))  # a private variable
        prog.append(code)
    return prog


def test_independent_counters() -> None:
    # n threads, each with k - 1 private steps: k^n states, but one path when reduced.
    for n, k in ((2, 4), (3, 3), (4, 3)):
        prog = [[("w", i, c) for c in range(1, k)] for i in range(n)]
        full, dead = full_search(prog, n, 0)
        red, rdead = reduced_search(prog, n, 0)
        assert len(full) == k**n
        assert len(red) == n * (k - 1) + 1
        assert rdead == dead and len(dead) == 1


def test_deadlocks_preserved() -> None:
    rng = random.Random(1990)
    total_full = total_red = 0
    for _ in range(600):
        prog = random_program(rng, loops=False)
        full, dead = full_search(prog, 4, 2)
        red, rdead = reduced_search(prog, 4, 2)
        assert red <= full
        assert rdead == dead
        total_full += len(full)
        total_red += len(red)
    assert total_red < total_full


def test_invariant_verdicts_preserved_with_loops() -> None:
    rng = random.Random(1993)
    for _ in range(600):
        prog = random_program(rng, loops=True)
        full, dead = full_search(prog, 4, 2)
        x, c = rng.randrange(2), rng.randint(0, 2)
        y, d = rng.randrange(2), rng.randint(0, 2)

        def bad(vals, x=x, c=c, y=y, d=d):
            return vals[x] == c and vals[y] == d

        expected = any(bad(s[1]) for s in full)
        assert partial_order_reduction(prog, 4, 2, bad, visible={x, y}) == expected
        red, rdead = reduced_search(prog, 4, 2, visible={x, y})
        assert rdead == dead


def test_cycle_proviso_is_needed() -> None:
    # Thread 0 loops forever on a local jump; thread 1 writes x = 1.
    prog = [[("jmp", 0)], [("w", 0, 1)]]
    ok = partial_order_reduction(prog, 1, 0, lambda v: v[0] == 1, visible={0})
    assert ok is True
    seen, _ = reduced_search(prog, 1, 0, visible={0}, proviso=False)
    assert not any(s[1][0] == 1 for s in seen)  # the ignoring problem


def test_visibility_condition() -> None:
    # Both orders of the two writes must be kept when x is visible.
    prog = [[("w", 0, 1)], [("w", 0, 2)]]
    seen, _ = reduced_search(prog, 1, 0, visible={0})
    assert {s[1][0] for s in seen} == {0, 1, 2}
    assert len(seen) == len(full_search(prog, 1, 0)[0])
