# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-graph-dynamics/. The authors are listed in prov/AN42TN.jsonl.

import math
import random

from distributed_graph_dynamics import (
    fewest_tokens_path,
    from_list,
    is_t_interval_connected,
    knowers_first_path,
    phased_dissemination,
    pipelined_dissemination,
    random_tree,
    t_interval_sequence,
)


def gossip_inputs(n, rng):
    toks = rng.sample(range(1, 10 * n), n)
    return [{x} for x in toks], sorted(toks)


def test_generator_is_t_interval_connected():
    for seed in range(30):
        n = 2 + seed % 9
        t = 1 + seed % 4
        graphs = t_interval_sequence(n, t, 6 * t, seed)
        assert is_t_interval_connected(n, graphs, t)


def test_checker_rejects_changing_trees():
    rng = random.Random(5)
    graphs = [random_tree(8, rng) for _ in range(10)]
    assert is_t_interval_connected(8, graphs, 1)
    assert not is_t_interval_connected(8, graphs, 2)
    assert not is_t_interval_connected(4, [{(0, 1), (2, 3)}], 1)


def test_one_token_takes_exactly_n_minus_1_rounds_against_the_path_adversary():
    for n in range(2, 16):
        inputs = [set() for _ in range(n)]
        inputs[n // 2] = {7}
        res = phased_dissemination(n, inputs, 1, knowers_first_path(7))
        assert res["first_full"] == n - 1  # one new node per round, never more
        assert all(a == {7} for a in res["knows"])


def test_phase_j_finishes_the_j_smallest_tokens():
    for seed in range(40):
        rng = random.Random(seed)
        n = 2 + seed % 8
        inputs, toks = gossip_inputs(n, rng)
        kinds = [fewest_tokens_path(), knowers_first_path(toks[-1]), from_list(t_interval_sequence(n, 1, n * n, seed))]
        adv = kinds[seed % 3]
        for j in range(1, n + 1):
            res = phased_dissemination(n, inputs, j, adv)
            assert all(set(toks[:j]) <= a for a in res["knows"])
            assert all(d == set(toks[:j]) for d in res["done"])
            assert res["rounds"] == j * (n - 1)
        assert res["first_full"] is not None and res["first_full"] <= n * (n - 1)


def test_k_tokens_from_several_holders():
    for seed in range(30):
        rng = random.Random(100 + seed)
        n = 3 + seed % 7
        k = 1 + seed % 5
        toks = rng.sample(range(1, 100), k)
        inputs = [set() for _ in range(n)]
        for x in toks:
            for v in rng.sample(range(n), rng.randint(1, n)):
                inputs[v].add(x)
        res = phased_dissemination(n, inputs, k, fewest_tokens_path())
        assert all(a == set(toks) for a in res["knows"])
        assert res["first_full"] <= k * (n - 1)


def test_pipelined_t_smallest_tokens_on_2t_interval_graphs():
    for seed in range(30):
        rng = random.Random(200 + seed)
        n = 4 + seed % 9
        t = 1 + seed % 3
        inputs, toks = gossip_inputs(n, rng)
        phases = math.ceil(n / t)
        graphs = t_interval_sequence(n, 2 * t, phases * 2 * t, seed, p=0.05)
        assert is_t_interval_connected(n, graphs, 2 * t)
        res = pipelined_dissemination(n, inputs, t, phases, from_list(graphs))
        assert all(set(toks[:t]) <= a for a in res["knows"])
        assert res["rounds"] == phases * 2 * t
