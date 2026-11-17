# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coalescent-simulation/. The authors are listed in prov/V8W27B.jsonl.

import random

import pytest

from biostoch import check_mean, chi2_sf, mean_var
from coalescent_simulation import (
    leaves_below,
    place_mutations,
    simulate,
    simulate_genealogy,
    tmrca,
    total_branch_length,
)


def harmonic(n, power=1):
    return sum(1.0 / i ** power for i in range(1, n))


def chi2_stat(observed, expected):
    return sum((o - e) ** 2 / e for o, e in zip(observed, expected))


def test_tree_structure():
    rng = random.Random(1)
    for n in (1, 2, 3, 7, 20):
        parent, time = simulate_genealogy(rng, n)
        assert len(parent) == 2 * n - 1
        assert parent.count(-1) == 1 and parent[-1] == -1
        for v, p in enumerate(parent):
            if p >= 0:
                assert p > v and time[p] > time[v]
        kids = [0] * len(parent)
        for p in parent:
            if p >= 0:
                kids[p] += 1
        assert kids[:n] == [0] * n and kids[n:] == [2] * (n - 1)
        assert leaves_below(parent, n)[-1] == (1 << n) - 1


def test_same_seed_same_sample():
    a = simulate(random.Random(42), 8, 3.0)
    b = simulate(random.Random(42), 8, 3.0)
    assert a == b


def test_columns_are_tree_splits():
    rng = random.Random(3)
    n = 9
    parent, time, positions, haps = simulate(rng, n, 6.0)
    assert positions == sorted(positions)
    assert all(0.0 <= x < 1.0 for x in positions)
    splits = set(leaves_below(parent, n)[:-1])
    for j in range(len(positions)):
        mask = sum(1 << r for r in range(n) if haps[r][j] == "1")
        assert mask in splits
        assert 1 <= bin(mask).count("1") <= n - 1


def test_times_and_lengths():
    rng = random.Random(10)
    n, reps = 10, 20000
    ts, ls = [], []
    for _ in range(reps):
        parent, time = simulate_genealogy(rng, n)
        ts.append(tmrca(time))
        ls.append(total_branch_length(parent, time))
    var_t = sum(4.0 / (k * (k - 1)) ** 2 for k in range(2, n + 1))
    m, _ = mean_var(ts)
    assert 2.0 * (1 - 1.0 / n) == pytest.approx(1.8)
    assert check_mean(m, 1.8, var_t, reps)
    m, _ = mean_var(ls)
    assert 2 * harmonic(n) == pytest.approx(5.657937, abs=1e-6)
    assert check_mean(m, 2 * harmonic(n), 4 * harmonic(n, 2), reps)


def test_root_split():
    # The side of the root that holds copy 0 has i copies with
    # probability 2 i / (n (n - 1)).
    rng = random.Random(77)
    n, reps = 6, 12000
    counts = [0] * n
    for _ in range(reps):
        parent, _ = simulate_genealogy(rng, n)
        below = leaves_below(parent, n)
        v = 0
        while parent[parent[v]] != -1:
            v = parent[v]
        counts[bin(below[v]).count("1")] += 1
    expected = [reps * 2 * i / (n * (n - 1)) for i in range(1, n)]
    assert chi2_sf(chi2_stat(counts[1:], expected), n - 2) > 0.001


def test_segregating_sites_and_spectrum():
    rng = random.Random(2002)
    n, theta, reps = 10, 5.0, 8000
    a, b = harmonic(n), harmonic(n, 2)
    ss = []
    xi = [[] for _ in range(n)]
    for _ in range(reps):
        _, _, positions, haps = simulate(rng, n, theta)
        ss.append(len(positions))
        row = [0] * n
        for j in range(len(positions)):
            row[sum(h[j] == "1" for h in haps)] += 1
        for i in range(1, n):
            xi[i].append(row[i])
    m, _ = mean_var(ss)
    assert check_mean(m, theta * a, theta * a + theta * theta * b, reps)
    for i in range(1, n):
        m, v = mean_var(xi[i])
        assert check_mean(m, theta / i, v, reps)


def test_two_copies_geometric():
    # For n = 2, P(S = k) = (1 / (1 + theta)) (theta / (1 + theta))^k.
    rng = random.Random(5)
    theta, reps, top = 1.0, 20000, 6
    counts = [0] * (top + 1)
    for _ in range(reps):
        s = len(simulate(rng, 2, theta)[2])
        counts[min(s, top)] += 1
    q = theta / (1 + theta)
    probs = [(1 - q) * q ** k for k in range(top)]
    probs.append(1 - sum(probs))
    expected = [reps * p for p in probs]
    assert chi2_sf(chi2_stat(counts, expected), top) > 0.001


def test_fixed_number_of_sites():
    rng = random.Random(8)
    parent, time = simulate_genealogy(rng, 7)
    positions, haps = place_mutations(rng, parent, time, 7, 0.0, segsites=12)
    assert len(positions) == 12 and all(len(h) == 12 for h in haps)
    assert place_mutations(rng, parent, time, 7, 0.0) == ([], [""] * 7)
    with pytest.raises(ValueError):
        place_mutations(rng, parent, time, 7, -1.0)
