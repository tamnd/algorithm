# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/holoclean/. The authors are listed in prov/DV1WKR.jsonl.

import itertools
import math
import random

from holoclean import (
    cooccurrence,
    detect_errors,
    gibbs,
    holoclean,
    joint_model,
    log_weight,
    prune_domain,
    relaxed_violations,
    violates,
)

# Zip -> City and Zip -> State as two denial constraints over attributes 0, 1, 2.
DCS = [[(0, "=", 0), (1, "!=", 1)], [(0, "=", 0), (2, "!=", 2)]]


def synthetic(seed, n=80, nzips=10, p=0.06):
    """Clean rows (zip, city, state) where zip fixes city and state, and a dirty copy."""
    rng = random.Random(seed)
    zips = {"z%d" % k: ("city%d" % (k % (nzips // 2)), "S%d" % (k % 3)) for k in range(nzips)}
    clean, dirty = [], []
    for _ in range(n):
        z = rng.choice(sorted(zips))
        city, state = zips[z]
        clean.append((z, city, state))
        d = [z, city, state]
        if rng.random() < p:
            d[1] = city + "x"
        if rng.random() < p / 2:
            d[2] = rng.choice(["S0", "S1", "S2"])
        dirty.append(tuple(d))
    return clean, dirty


def brute_noisy(rows, dcs):
    """Oracle: check every ordered pair of rows against every constraint."""
    out = set()
    for dc in dcs:
        attrs = {a for a, _, _ in dc} | {b for _, _, b in dc}
        for i, j in itertools.permutations(range(len(rows)), 2):
            if all({"=": rows[i][a] == rows[j][b], "!=": rows[i][a] != rows[j][b]}[op] for a, op, b in dc):
                out |= {(i, a) for a in attrs} | {(j, a) for a in attrs}
    return out


def test_detection_matches_pairs():
    rng = random.Random(3)
    for _ in range(30):
        _, dirty = synthetic(rng.randint(0, 10**6), n=rng.randint(2, 15), p=0.2)
        assert detect_errors(dirty, DCS) == brute_noisy(dirty, DCS)


def test_small_table():
    rows = [("z1", "Chicago", "IL"), ("z1", "Chicago", "IL"), ("z1", "Chicgo", "IL"), ("z2", "Boston", "MA")]
    noisy = detect_errors(rows, DCS)
    assert noisy == {(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)}
    stats = cooccurrence(rows)
    # Pr[Chicago | z1] = 2/3 and Pr[Chicgo | z1] = 1/3.
    assert prune_domain(rows, (2, 1), 0.5, stats) == ["Chicago", "Chicgo"]
    assert prune_domain(rows, (2, 1), 0.7, stats) == ["Chicgo"]
    assert relaxed_violations(rows, (2, 1), "Chicgo", DCS[0]) == 2
    assert relaxed_violations(rows, (2, 1), "Chicago", DCS[0]) == 0
    assert violates(DCS[0], rows[0], rows[2]) and not violates(DCS[0], rows[0], rows[1])


def test_repairs_on_synthetic_data():
    tp = fp = errors = 0
    for seed in range(8):
        clean, dirty = synthetic(seed)
        repaired, marginals, noisy = holoclean(dirty, DCS, tau=0.3, prior=1.0)
        for i, row in enumerate(dirty):
            for a in range(3):
                if row[a] != clean[i][a]:
                    errors += 1
                if repaired[i][a] != row[a]:
                    if repaired[i][a] == clean[i][a]:
                        tp += 1
                    else:
                        fp += 1
        for c, m in marginals.items():
            assert c in noisy
            assert abs(sum(m.values()) - 1.0) < 1e-9
    # Measured with these seeds: 60 of 60 errors fixed, 12 wrong changes.
    assert (tp, fp, errors) == (60, 12, 60)
    assert tp / (tp + fp) > 0.8 and tp / errors > 0.95


def test_clean_table_is_unchanged():
    clean, _ = synthetic(1)
    repaired, marginals, noisy = holoclean(clean, DCS, tau=0.3)
    assert repaired == clean and not marginals and not noisy


def exact_marginals(rows, dcs, model):
    cells, dom, _, _ = model
    totals = {c: {d: 0.0 for d in dom[c]} for c in cells}
    z = 0.0
    for combo in itertools.product(*[dom[c] for c in cells]):
        x = dict(zip(cells, combo))
        p = math.exp(log_weight(rows, dcs, model, x))
        z += p
        for c in cells:
            totals[c][x[c]] += p
    return {c: {d: v / z for d, v in totals[c].items()} for c in cells}


def test_gibbs_matches_exact_marginals():
    rng = random.Random(11)
    rows = [("z1", "A", "S1"), ("z1", "B", "S1"), ("z1", "A", "S2"), ("z2", "C", "S1")]
    noisy = detect_errors(rows, DCS)
    noisy = {c for c in noisy if c[1] != 0}
    dom = {c: sorted({r[c[1]] for r in rows}) for c in noisy}
    unary = {(c, d): rng.uniform(-1.0, 1.0) for c in noisy for d in dom[c]}
    model = joint_model(rows, DCS, noisy, dom, unary, 1.5)
    assert len(model[0]) == 6
    exact = exact_marginals(rows, DCS, model)
    est = gibbs(rows, DCS, model, sweeps=4000, burn_in=200, rng=random.Random(5))
    for c in exact:
        for d in exact[c]:
            assert abs(exact[c][d] - est[c][d]) < 0.04


def test_near_hard_constraint_traps_the_sampler():
    # Two cells that must agree, with no preference between A and B. The exact
    # marginal is 1/2, but with a weight of 20 one-cell moves almost never leave
    # the first consistent state, so the estimate is 0 or 1.
    rows = [("z1", "A", "S1"), ("z1", "B", "S1")]
    noisy = {(0, 1), (1, 1)}
    dom = {c: ["A", "B"] for c in noisy}
    unary = {(c, d): 0.0 for c in noisy for d in dom[c]}
    model = joint_model(rows, DCS, noisy, dom, unary, 20.0)
    exact = exact_marginals(rows, DCS, model)
    assert abs(exact[(0, 1)]["A"] - 0.5) < 1e-9
    assert log_weight(rows, DCS, model, {(0, 1): "A", (1, 1): "B"}) == -20.0
    est = gibbs(rows, DCS, model, sweeps=2000, burn_in=100, rng=random.Random(1))
    assert est[(0, 1)]["A"] in (0.0, 1.0)
    soft = joint_model(rows, DCS, noisy, dom, unary, 1.0)
    est = gibbs(rows, DCS, soft, sweeps=4000, burn_in=200, rng=random.Random(1))
    assert abs(est[(0, 1)]["A"] - 0.5) < 0.05
