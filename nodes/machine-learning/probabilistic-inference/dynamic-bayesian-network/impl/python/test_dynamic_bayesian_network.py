# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-bayesian-network/. The authors are listed in prov/YPNGR6.jsonl.

import math
import random
from fractions import Fraction as F
from itertools import product

import pytest

from dynamic_bayesian_network import DBN, flat_hmm, frontier_filter, frontier_step, log_likelihood, sample


def rand_p(rng: random.Random, exact: bool):
    k = rng.randint(1, 9)
    return F(k, 10) if exact else k / 10 + rng.uniform(-0.04, 0.04)


def rand_dbn(rng: random.Random, K: int, M: int, exact: bool = True, coupled: bool = True) -> DBN:
    parents = []
    for k in range(K):
        if coupled:
            ps = tuple(i for i in range(K) if i == k or rng.random() < 0.5)
        else:
            ps = (k,)
        parents.append(ps)
    cpt = [{u: rand_p(rng, exact) for u in product((0, 1), repeat=len(ps))} for ps in parents]
    emit = []
    for _ in range(K):
        rows = []
        for _ in range(2):
            w = [rng.randint(1, 5) for _ in range(M)]
            rows.append([F(x, sum(w)) if exact else x / sum(w) for x in w])
        emit.append(rows)
    return DBN([rand_p(rng, exact) for _ in range(K)], parents, cpt, emit)


def joint(dbn: DBN, xs, ys):
    w = F(1)
    for t, (x, y) in enumerate(zip(xs, ys)):
        for k in range(dbn.K):
            p1 = dbn.prior[k] if t == 0 else dbn.cpt[k][tuple(xs[t - 1][i] for i in dbn.parents[k])]
            w *= (p1 if x[k] else 1 - p1) * dbn.emit[k][x[k]][y[k]]
    return w


def brute_filter(dbn: DBN, ys):
    """P(y_1..y_t) and P(X_t | y_1..y_t) for each t, by listing every trajectory of the unrolled net."""
    out = []
    states = list(product((0, 1), repeat=dbn.K))
    for t in range(1, len(ys) + 1):
        marg = {s: F(0) for s in states}
        for xs in product(states, repeat=t):
            marg[xs[-1]] += joint(dbn, xs, ys[:t])
        total = sum(marg.values())
        out.append((total, {s: v / total for s, v in marg.items()}))
    return out


def test_frontier_matches_enumeration_of_trajectories() -> None:
    rng = random.Random(1989)
    for _ in range(40):
        K, T = rng.randint(1, 3), rng.randint(1, 3)
        dbn = rand_dbn(rng, K, 2)
        ys = [tuple(rng.randrange(2) for _ in range(K)) for _ in range(T)]
        order = list(range(K))
        rng.shuffle(order)
        beliefs, norms, _ = frontier_filter(dbn, ys, order)
        ref = brute_filter(dbn, ys)
        p = F(1)
        for t in range(T):
            p *= norms[t]
            assert p == ref[t][0]  # P(y_1..y_t)
            assert beliefs[t] == ref[t][1]  # P(X_t | y_1..y_t)


def flat_forward(dbn: DBN, ys):
    """Scaled forward algorithm on the flat HMM over 2^K product states."""
    states, pi, A, b = flat_hmm(dbn)
    n = len(states)
    row = [pi[s] * b(s, ys[0]) for s in range(n)]
    ll, rows = 0.0, []
    for t in range(len(ys)):
        if t:
            row = [b(j, ys[t]) * sum(row[i] * A[i][j] for i in range(n)) for j in range(n)]
        c = sum(row)
        ll += math.log(c)
        row = [x / c for x in row]
        rows.append(dict(zip(states, row)))
    return ll, rows


def test_matches_the_flat_hmm_on_product_states() -> None:
    rng = random.Random(2002)
    for K in (2, 3):
        dbn = rand_dbn(rng, K, 3, exact=False)
        _, ys = sample(dbn, 200, rng)
        beliefs, norms, _ = frontier_filter(dbn, ys)
        ll, rows = flat_forward(dbn, ys)
        assert ll < -100  # the product of the norms would be tiny; the log stays exact enough
        assert math.isclose(log_likelihood(norms), ll, rel_tol=1e-9)
        for got, want in zip(beliefs, rows):
            assert all(abs(got[s] - want[s]) < 1e-9 for s in want)


def is_product(belief: dict, K: int) -> bool:
    margs = [sum(v for s, v in belief.items() if s[k] == 1) for k in range(K)]
    for s, v in belief.items():
        w = F(1)
        for k in range(K):
            w *= margs[k] if s[k] else 1 - margs[k]
        if w != v:
            return False
    return True


def test_uncoupled_chains_stay_factored() -> None:
    rng = random.Random(5)
    dbn = rand_dbn(rng, 3, 2, coupled=False)
    ys = [tuple(rng.randrange(2) for _ in range(3)) for _ in range(6)]
    beliefs, _, largest = frontier_filter(dbn, ys)
    assert all(is_product(b, 3) for b in beliefs)
    assert largest == 3 + 1


def test_a_cross_link_entangles_the_belief() -> None:
    # the example on the page: X^0 stays with probability 0.9, X^1_t copies X^0_(t-1)
    # with probability 0.9, and the observations carry no information
    half, stay = F(1, 2), F(9, 10)
    dbn = DBN([half, half], [(0,), (0,)],
              [{(0,): 1 - stay, (1,): stay}, {(0,): 1 - stay, (1,): stay}],
              [[[F(1)], [F(1)]], [[F(1)], [F(1)]]])
    beliefs, norms, _ = frontier_filter(dbn, [(0, 0), (0, 0)])
    assert norms == [1, 1]
    assert is_product(beliefs[0], 2)
    b = beliefs[1]
    assert b == {(0, 0): F(41, 100), (0, 1): F(9, 100), (1, 0): F(9, 100), (1, 1): F(41, 100)}
    assert not is_product(b, 2)  # each marginal is 1/2, but P(1, 1) = 0.41, not 0.25


def test_frontier_size() -> None:
    rng = random.Random(3)
    K = 3
    ys = [(0, 1, 0)] * 3
    full = rand_dbn(rng, K, 2)
    full = DBN(full.prior, [tuple(range(K))] * K,
               [{u: F(1, 3) + F(sum(u), 9) for u in product((0, 1), repeat=K)} for _ in range(K)], full.emit)
    assert frontier_filter(full, ys)[2] == 2 * K  # every old node waits for every new node
    chain = DBN(full.prior, [(0,), (0, 1), (1, 2)],
                [{u: F(1, 4) + F(sum(u), 8) for u in product((0, 1), repeat=n)} for n in (1, 2, 2)], full.emit)
    # the order of addition changes the frontier but not the answer: adding X^2 first frees
    # the old X^2 at once, while adding X^0 first keeps the old X^0 until X^1 is in
    b1, n1, f1 = frontier_filter(chain, ys, [2, 1, 0])
    b2, n2, f2 = frontier_filter(chain, ys)
    assert (b1, n1) == (b2, n2)
    assert (f1, f2) == (K + 1, K + 2)


def test_errors() -> None:
    with pytest.raises(ValueError):
        DBN([0.5], [(0,)], [{(0,): 0.5}], [[[1.0], [1.0]]])  # CPT misses the assignment (1,)
    with pytest.raises(ValueError):
        DBN([0.5], [(1,)], [{(0,): 0.5, (1,): 0.5}], [[[1.0], [1.0]]])
    dbn = DBN([F(1)], [(0,)], [{(0,): F(0), (1,): F(1)}], [[[F(1), F(0)], [F(1), F(0)]]])
    with pytest.raises(ValueError):
        frontier_step(dbn, None, (1,))
    with pytest.raises(ValueError):
        frontier_filter(dbn, [])
