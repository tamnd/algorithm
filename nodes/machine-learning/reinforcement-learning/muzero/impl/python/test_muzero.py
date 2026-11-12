# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/muzero/. The authors are listed in prov/RGAS70.jsonl.

import random

from muzero import TableModel, search


def optimal_q(T, g, n, k):
    """Independent oracle: Q* of a deterministic MDP by value iteration."""
    V = [0.0] * n
    for _ in range(3000):
        V = [max(T[(s, a)][0] + g * V[T[(s, a)][1]] for a in range(k)) for s in range(n)]
    return [[T[(s, a)][0] + g * V[T[(s, a)][1]] for a in range(k)] for s in range(n)], V


def trap():
    """State 0: action 0 pays 1 now and leads to a dead end; action 1 pays 0 now and then 2 at every step."""
    T = {(0, 0): (1.0, 1), (0, 1): (0.0, 2), (1, 0): (0.0, 1), (1, 1): (0.0, 1), (2, 0): (2.0, 2), (2, 1): (0.0, 1)}
    return T, 3, 2


def test_trap_exact_model_zero_values():
    T, n, k = trap()
    Q, _ = optimal_q(T, 0.9, n, k)
    assert abs(Q[0][1] - 18) < 1e-9 and Q[0][0] == 1.0  # 0.9 * 2 / (1 - 0.9) = 18 against 1
    m = TableModel(T, {s: [0.5, 0.5] for s in range(n)}, {s: 0.0 for s in range(n)})
    visits, a, _ = search(m, 0, 0.9, 10)
    assert a == 0 and visits == [9, 1]  # too few simulations to see past the first reward
    for sims, want in ((50, [13, 37]), (200, [13, 187]), (800, [21, 779])):
        visits, a, _ = search(m, 0, 0.9, sims)
        assert a == 1 and visits == want


def test_trap_misleading_prior_is_overcome():
    T, n, k = trap()
    m = TableModel(T, {s: [0.9, 0.1] for s in range(n)}, {s: 0.0 for s in range(n)})
    visits, a, _ = search(m, 0, 0.9, 200)
    assert a == 0 and visits == [199, 1]
    visits, a, _ = search(m, 0, 0.9, 400)
    assert a == 0 and visits == [285, 115]
    visits, a, root = search(m, 0, 0.9, 800)
    assert a == 1 and visits == [285, 515]
    child = root.children[1]
    assert 16 < child.reward + 0.9 * child.value() < 18  # approaches Q*(0, 1) = 18 from below


def random_case(rng):
    """A small deterministic MDP whose best root action is better than the others by at least 1."""
    while True:
        n, k = rng.randint(2, 5), rng.randint(2, 3)
        T = {(s, a): (float(rng.randint(0, 4)), rng.randrange(n)) for s in range(n) for a in range(k)}
        g = rng.choice([0.5, 0.8])
        Q, V = optimal_q(T, g, n, k)
        q = sorted(Q[0])
        if q[-1] - q[-2] >= 1.0:
            return T, n, k, g, Q, V


def check_tree(node, root=True):
    """Every expanded node: N = sum of the children's N, plus 1 for the simulation that expanded it."""
    child_sum = sum(c.N for c in node.children.values())
    if node.children:
        assert node.N == child_sum + (0 if root else 1)
    for c in node.children.values():
        if c.N:
            check_tree(c, False)


def test_exact_model_finds_optimal_action_on_500_random_mdps():
    rng = random.Random(7)
    for _ in range(500):
        T, n, k, g, Q, V = random_case(rng)
        m = TableModel(T, {s: [1 / k] * k for s in range(n)}, {s: V[s] for s in range(n)})
        visits, a, root = search(m, 0, g, 100)
        assert Q[0][a] == max(Q[0])
        assert sum(visits) == 100 and root.N == 100
        check_tree(root)
        for b, c in root.children.items():
            if c.N:
                assert c.reward + g * c.value() <= Q[0][b] + 1e-9  # no overestimate with an exact model
        _, _, one = search(m, 0, g, k)
        for b, c in one.children.items():
            if c.N == 1:
                assert abs(c.reward + g * c.value() - Q[0][b]) < 1e-9  # exact after the first visit


def test_more_simulations_overcome_random_priors():
    rng = random.Random(8)
    hits = {25: 0, 400: 0}
    for _ in range(100):
        T, n, k, g, Q, V = random_case(rng)
        pri = {}
        for s in range(n):
            w = [rng.random() for _ in range(k)]
            pri[s] = [x / sum(w) for x in w]
        m = TableModel(T, pri, {s: V[s] for s in range(n)})
        for sims in hits:
            _, a, _ = search(m, 0, g, sims)
            hits[sims] += Q[0][a] == max(Q[0])
    assert hits[400] > hits[25] and hits[400] >= 95


def test_representation_and_edges():
    T = {("x", 0): (1.0, "x")}
    m = TableModel(T, {"x": [1.0]}, {"x": 0.0}, represent={"obs": "x"})
    visits, a, root = search(m, "obs", 0.5, 5)
    assert visits == [5] and a == 0 and root.state == "x"
    visits, a, _ = search(m, "obs", 0.5, 0)
    assert visits == [0] and a == 0
