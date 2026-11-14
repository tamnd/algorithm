# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tilos/. The authors are listed in prov/Q10RHR.jsonl.

import random
from fractions import Fraction
from itertools import product

from tilos import Circuit, area, critical_path, delay, path_delay, tilos


def brute_force(ckt, target):
    """Least area over every assignment of discrete sizes that meets target."""
    best = None
    for x in product(*ckt.sizes):
        if delay(ckt, list(x)) <= target:
            ar = area(ckt, list(x))
            if best is None or ar < best:
                best = ar
    return best


def random_circuit(rng, n):
    fanin = [[]] + [sorted(rng.sample(range(i), rng.randint(1, min(2, i)))) for i in range(1, n)]
    p = [rng.randint(0, 2) for _ in range(n)]
    r = [rng.randint(1, 3) for _ in range(n)]
    c = [rng.randint(1, 2) for _ in range(n)]
    a = [rng.randint(1, 3) for _ in range(n)]
    has_fanout = {i for ins in fanin for i in ins}
    f = [0 if i in has_fanout else rng.randint(4, 16) for i in range(n)]
    sizes = [[1]] + [[1, 2, 3, 4] for _ in range(n - 1)]  # gate 0 is a fixed driver
    return Circuit(fanin, p, r, c, a, f, sizes)


def test_against_enumeration(rng=random.Random(1985)):
    found = optimal = 0
    for _ in range(250):
        ckt = random_circuit(rng, rng.randint(2, 5))
        slow = delay(ckt, [s[0] for s in ckt.sizes])
        target = Fraction(rng.randint(1, int(slow) + 2))
        best = brute_force(ckt, target)
        x = tilos(ckt, target)
        if best is None:
            assert x is None  # nothing meets the target, so TILOS cannot
            continue
        if x is not None:
            found += 1
            assert all(s in ckt.sizes[i] for i, s in enumerate(x))
            assert delay(ckt, x) <= target
            assert area(ckt, x) >= best  # a heuristic: never below the optimum
            optimal += area(ckt, x) == best
    assert found > 50 and optimal > 0


def test_loose_target_keeps_minimum_sizes(rng=random.Random(7)):
    for _ in range(50):
        ckt = random_circuit(rng, 5)
        x0 = [s[0] for s in ckt.sizes]
        assert tilos(ckt, delay(ckt, x0)) == x0


def test_critical_path_is_longest(rng=random.Random(8)):
    for _ in range(100):
        ckt = random_circuit(rng, 5)
        x = [rng.choice(s) for s in ckt.sizes]
        path = critical_path(ckt, x)
        assert path_delay(ckt, x, path) == delay(ckt, x)
        assert ckt.fanin[path[0]] == []
        assert all(path[k] in ckt.fanin[path[k + 1]] for k in range(len(path) - 1))
        # the local gain of the implementation equals the change of the whole path
        for g in path:
            y = list(x)
            y[g] += 1
            whole = path_delay(ckt, x, path) - path_delay(ckt, y, path)
            touched = [g] + [k for k in ckt.fanin[g] if k in path]
            assert whole == path_delay(ckt, x, touched) - path_delay(ckt, y, touched)


def example():
    return Circuit([[], [0], [1], [2]], [1, 1, 1, 1], [3, 1, 2, 3], [1, 1, 1, 1], [2, 1, 3, 1],
                   [0, 0, 0, 12], [[1], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]])


def test_example_of_the_page():
    ckt = example()
    assert delay(ckt, [1, 1, 1, 1]) == 46
    x = tilos(ckt, 24)
    assert x == [1, 1, 2, 4] and delay(ckt, x) == 22 and area(ckt, x) == 13
    assert brute_force(ckt, 24) == 12
    assert delay(ckt, [1, 1, 2, 3]) == 24 and area(ckt, [1, 1, 2, 3]) == 12


def test_failure_although_a_sizing_exists():
    ckt = Circuit([[], [0], [1], [2]], [1, 1, 1, 1], [1, 3, 3, 1], [1, 1, 1, 1], [1, 1, 1, 1],
                  [0, 0, 0, 6], [[1], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]])
    assert delay(ckt, [1, 1, 1, 1]) == 17
    assert tilos(ckt, 16) is None  # stuck at sizes (1, 2, 1, 1) with delay 33/2
    assert delay(ckt, [1, 2, 1, 1]) == Fraction(33, 2)
    assert delay(ckt, [1, 2, 2, 2]) == 15 and brute_force(ckt, 16) == 7
