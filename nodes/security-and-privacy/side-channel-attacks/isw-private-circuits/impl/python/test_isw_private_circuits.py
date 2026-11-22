# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isw-private-circuits/. The authors are listed in prov/F6CSK5.jsonl.

import itertools
import random
from collections import Counter

import pytest
from isw_private_circuits import (
    eval_masked,
    eval_plain,
    isw_and,
    isw_and_wires,
    naive_and_wires,
    share,
    unshare,
    wrong_order_wires,
)


def all_runs(gadget, n, randomized=True):
    """For each secret (a, b), the list of wire vectors over all shares and random bits."""
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    runs = {}
    for a, b in itertools.product((0, 1), repeat=2):
        vecs = []
        for sa in itertools.product((0, 1), repeat=n - 1):
            for sb in itertools.product((0, 1), repeat=n - 1):
                xa = list(sa) + [a ^ (sum(sa) & 1)]
                xb = list(sb) + [b ^ (sum(sb) & 1)]
                for rb in itertools.product((0, 1), repeat=len(pairs) if randomized else 0):
                    if randomized:
                        c, w = gadget(xa, xb, dict(zip(pairs, rb)))
                    else:
                        c, w = gadget(xa, xb)
                    assert unshare(c) == a & b
                    vecs.append(w)
        runs[(a, b)] = vecs
    return runs


def leaking_sets(runs, t):
    """Every set of at most t wires whose joint distribution depends on (a, b)."""
    names = [name for name, _ in runs[(0, 0)][0]]
    out = []
    for size in range(1, t + 1):
        for probe in itertools.combinations(range(len(names)), size):
            dists = [Counter(tuple(w[p][1] for p in probe) for w in vecs) for vecs in runs.values()]
            if any(d != dists[0] for d in dists[1:]):
                out.append(tuple(names[p] for p in probe))
    return out


def test_worked_example() -> None:
    c, wires = isw_and_wires([1, 0], [0, 1], {(0, 1): 1})
    assert c == [1, 0]
    assert dict(wires)["r10"] == 0
    assert len(wires) == 13


def test_one_probe_two_shares_is_secure() -> None:
    assert leaking_sets(all_runs(isw_and_wires, 2), 1) == []


def test_two_probes_three_shares_is_secure() -> None:
    # t + 1 = 3 shares are enough against t = 2 probes (Rivain and Prouff 2010).
    runs = all_runs(isw_and_wires, 3)
    assert len(runs[(0, 0)][0]) == 30
    assert leaking_sets(runs, 2) == []


def test_t_probes_on_t_shares_leak() -> None:
    assert ("a0", "a1") in leaking_sets(all_runs(isw_and_wires, 2), 2)


def test_naive_gadget_leaks_with_one_probe() -> None:
    for n in (2, 3):
        leaks = leaking_sets(all_runs(naive_and_wires, n, randomized=False), 1)
        # The last partial sum of c_0 is a_0 AND b.
        assert (f"c0 after a0b{n - 1}",) in leaks


def test_wrong_order_leaks() -> None:
    assert ("a0b1+a1b0",) in leaking_sets(all_runs(wrong_order_wires, 2), 1)
    runs3 = all_runs(wrong_order_wires, 3)
    assert leaking_sets(runs3, 1) == []
    leaks = leaking_sets(runs3, 2)
    assert len(leaks) == 9 and ("a2", "a0b1+a1b0") in leaks
    runs = all_runs(wrong_order_wires, 2)
    k = [name for name, _ in runs[(0, 0)][0]].index("a0b1+a1b0")
    assert all(w[k][1] == 0 for w in runs[(0, 0)])
    assert sum(w[k][1] for w in runs[(1, 1)]) * 2 == len(runs[(1, 1)])


def test_output_is_a_uniform_sharing() -> None:
    for n in range(1, 5):
        pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
        rng = random.Random(n)
        a = [rng.randrange(2) for _ in range(n)]
        b = [rng.randrange(2) for _ in range(n)]
        outs = Counter()
        for rb in itertools.product((0, 1), repeat=len(pairs)):
            outs[tuple(isw_and_wires(a, b, dict(zip(pairs, rb)))[0])] += 1
        assert len(outs) == 2 ** (n - 1)
        assert len(set(outs.values())) == 1
        assert all(unshare(list(c)) == unshare(a) & unshare(b) for c in outs)


def test_cost_counts() -> None:
    for n in range(1, 7):
        a, b = [0] * n, [0] * n
        r = {(i, j): 0 for i in range(n) for j in range(i + 1, n)}
        _, wires = isw_and_wires(a, b, r)
        names = [name for name, _ in wires][2 * n:]
        ands = [x for x in names if x.startswith("a") and "+" not in x]
        rand = [x for x in names if x.startswith("r") and "+" not in x and int(x[1]) < int(x[2])]
        xors = [x for x in names if "+" in x or "after" in x or (x.startswith("r") and int(x[1]) > int(x[2]))]
        assert len(ands) == n * n
        assert len(rand) == n * (n - 1) // 2
        assert len(xors) == 2 * n * (n - 1)


def test_and_against_oracle() -> None:
    rng = random.Random(20240506)
    for _ in range(500):
        n = rng.randrange(1, 7)
        x, y = rng.randrange(2), rng.randrange(2)
        c = isw_and(rng, share(rng, x, n), share(rng, y, n))
        assert len(c) == n and unshare(c) == x & y
    with pytest.raises(ValueError):
        isw_and(rng, [0, 1], [1])


def test_masked_circuit_against_plain() -> None:
    rng = random.Random(7)
    for _ in range(500):
        k = rng.randrange(1, 5)
        gates = []
        for g in range(rng.randrange(1, 9)):
            op = rng.choice(["xor", "and", "not"])
            gates.append((op, rng.randrange(k + g), rng.randrange(k + g)))
        bits = [rng.randrange(2) for _ in range(k)]
        n = rng.randrange(1, 5)
        out = eval_masked(rng, gates, [share(rng, v, n) for v in bits])
        assert unshare(out) == eval_plain(gates, bits)
