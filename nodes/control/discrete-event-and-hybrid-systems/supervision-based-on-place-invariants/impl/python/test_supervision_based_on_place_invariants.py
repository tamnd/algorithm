# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/supervision-based-on-place-invariants/. The authors are listed in prov/131GMK.jsonl.

import itertools
import random

import pytest

from supervision_based_on_place_invariants import (
    closed_loop,
    enabled,
    fire,
    incidence,
    is_admissible,
    monitor_places,
    reachable_markings,
)

# Two cyclic processes p1 -> t1 -> p2 -> t2 -> p1 and p3 -> t3 -> p4 -> t4 -> p3.
# p2 and p4 are the critical sections. The constraint mu(p2) + mu(p4) <= 1 is
# mutual exclusion.
PRE = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
]
POST = [
    [0, 1, 0, 0],
    [1, 0, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0],
]
MU0 = [1, 0, 1, 0]
L_MUTEX = [[0, 1, 0, 1]]
B_MUTEX = [1]


def lin(L, mu):
    return [sum(a * x for a, x in zip(row, mu)) for row in L]


def legal(L, b):
    return lambda mu: all(v <= bj for v, bj in zip(lin(L, mu), b))


def random_conservative_net(rng, n, q):
    """Each transition moves k tokens, so the total number of tokens is constant."""
    pre = [[0] * q for _ in range(n)]
    post = [[0] * q for _ in range(n)]
    for t in range(q):
        k = rng.randint(1, 2)
        for _ in range(k):
            pre[rng.randrange(n)][t] += 1
            post[rng.randrange(n)][t] += 1
    return pre, post


def random_case(rng):
    n = rng.randint(2, 5)
    q = rng.randint(2, 5)
    pre, post = random_conservative_net(rng, n, q)
    mu0 = [0] * n
    for _ in range(rng.randint(1, 4)):
        mu0[rng.randrange(n)] += 1
    c = rng.randint(1, 2)
    L = [[rng.randint(-1, 2) for _ in range(n)] for _ in range(c)]
    b = [v + rng.randint(0, 2) for v in lin(L, mu0)]
    return pre, post, mu0, L, b


def test_incidence_of_the_example():
    assert incidence(PRE, POST) == [
        [-1, 1, 0, 0],
        [1, -1, 0, 0],
        [0, 0, -1, 1],
        [0, 0, 1, -1],
    ]


def test_mutual_exclusion_monitor_is_a_semaphore():
    pre_c, post_c, muc0 = monitor_places(PRE, POST, MU0, L_MUTEX, B_MUTEX)
    # D_c = -L D = [-1, 1, -1, 1]: the monitor feeds t1 and t3, and t2 and t4 give the token back.
    assert pre_c == [[1, 0, 1, 0]]
    assert post_c == [[0, 1, 0, 1]]
    assert muc0 == [1]


def test_example_reachability_counts():
    plant = reachable_markings(PRE, POST, MU0)
    assert plant == {(1, 0, 1, 0), (0, 1, 1, 0), (1, 0, 0, 1), (0, 1, 0, 1)}
    pre2, post2, mu2 = closed_loop(PRE, POST, MU0, L_MUTEX, B_MUTEX)
    cl = reachable_markings(pre2, post2, mu2)
    assert cl == {(1, 0, 1, 0, 1), (0, 1, 1, 0, 0), (1, 0, 0, 1, 0)}


def test_infeasible_initial_marking_is_rejected():
    with pytest.raises(ValueError):
        monitor_places(PRE, POST, [0, 1, 0, 1], L_MUTEX, B_MUTEX)


def test_bad_input_is_rejected():
    with pytest.raises(ValueError):
        incidence([[1, -1]], [[0, 0]])
    with pytest.raises(ValueError):
        monitor_places(PRE, POST, MU0, [[1, 1]], [1])


def test_random_nets_match_restricted_reachability_graph():
    rng = random.Random(20240611)
    checked = 0
    for _ in range(300):
        pre, post, mu0, L, b = random_case(rng)
        n = len(pre)
        pre2, post2, mu2 = closed_loop(pre, post, mu0, L, b)
        cl = reachable_markings(pre2, post2, mu2)
        projected = {m[:n] for m in cl}
        target = reachable_markings(pre, post, mu0, allowed=legal(L, b))
        assert projected == target
        for m in cl:
            mu, muc = m[:n], m[n:]
            # the place invariant L mu + mu_c = b holds on every reachable marking
            assert [v + w for v, w in zip(lin(L, mu), muc)] == list(b)
            assert all(w >= 0 for w in muc)
        checked += len(cl)
    assert checked > 500


def test_maximal_permissiveness_on_every_legal_marking():
    rng = random.Random(7)
    for _ in range(200):
        pre, post, mu0, L, b = random_case(rng)
        n, q = len(pre), len(pre[0])
        pre2, post2, mu2 = closed_loop(pre, post, mu0, L, b)
        ok = legal(L, b)
        for m in reachable_markings(pre2, post2, mu2):
            mu = m[:n]
            for t in range(q):
                plant_allows = enabled(pre, mu, t) and ok(fire(pre, post, mu, t))
                assert enabled(pre2, m, t) == plant_allows


def test_all_firing_sequences_up_to_length_8():
    rng = random.Random(99)
    for _ in range(25):
        pre, post, mu0, L, b = random_case(rng)
        n, q = len(pre), len(pre[0])
        if q > 3:
            pre = [row[:3] for row in pre]
            post = [row[:3] for row in post]
            q = 3
        pre2, post2, mu2 = closed_loop(pre, post, mu0, L, b)
        ok = legal(L, b)
        for length in range(9):
            for seq in itertools.product(range(q), repeat=length):
                mu, m = tuple(mu0), tuple(mu2)
                plant_ok, cl_ok = True, True
                for t in seq:
                    if plant_ok and enabled(pre, mu, t):
                        mu = fire(pre, post, mu, t)
                        plant_ok = ok(mu)
                    else:
                        plant_ok = False
                    if cl_ok and enabled(pre2, m, t):
                        m = fire(pre2, post2, m, t)
                    else:
                        cl_ok = False
                assert plant_ok == cl_ok
                if cl_ok:
                    assert m[:n] == mu


def test_admissibility_with_uncontrollable_transitions():
    # t2 and t4 leave the critical sections. They only lower L mu, so they may be uncontrollable.
    assert is_admissible(PRE, POST, L_MUTEX, uncontrollable=[1, 3])
    pre_c, _, _ = monitor_places(PRE, POST, MU0, L_MUTEX, B_MUTEX)
    assert pre_c[0][1] == 0 and pre_c[0][3] == 0
    # t1 enters a critical section. If it is uncontrollable the monitor cannot block it.
    assert not is_admissible(PRE, POST, L_MUTEX, uncontrollable=[0])
    # t2 changes L mu, so it must be observed.
    assert not is_admissible(PRE, POST, L_MUTEX, unobservable=[1])


def test_admissible_monitor_never_blocks_uncontrollable_transitions():
    rng = random.Random(4242)
    found = 0
    for _ in range(400):
        pre, post, mu0, L, b = random_case(rng)
        q = len(pre[0])
        unc = [t for t in range(q) if rng.random() < 0.5]
        if not is_admissible(pre, post, L, uncontrollable=unc):
            continue
        found += 1
        pre_c, _, _ = monitor_places(pre, post, mu0, L, b)
        for t in unc:
            assert all(row[t] == 0 for row in pre_c)
    assert found > 20


def test_bounded_buffer_capacity():
    # producer t0 puts an item in the buffer p0, consumer t1 takes it; p1 and p2 are idle places.
    pre = [[0, 1], [1, 0], [0, 0]]
    post = [[1, 0], [1, 0], [0, 0]]
    mu0 = [0, 1, 0]
    # the plant buffer is unbounded; the monitor keeps mu(p0) <= 3
    pre2, post2, mu2 = closed_loop(pre, post, mu0, [[1, 0, 0]], [3])
    cl = reachable_markings(pre2, post2, mu2)
    assert {m[0] for m in cl} == {0, 1, 2, 3}
    assert all(m[0] + m[3] == 3 for m in cl)
    with pytest.raises(RuntimeError):
        reachable_markings(pre, post, mu0, limit=50)
