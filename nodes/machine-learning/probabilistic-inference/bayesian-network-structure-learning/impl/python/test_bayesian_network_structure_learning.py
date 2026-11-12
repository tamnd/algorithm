# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayesian-network-structure-learning/. The authors are listed in prov/RJFQX2.jsonl.

import itertools
import math
import random
from collections import defaultdict

from bayesian_network_structure_learning import bdeu, bic, local_scores, network_score, silander_myllymaki


def all_dags(n):
    """Every DAG on n nodes as a list of parent masks."""
    pairs = list(itertools.combinations(range(n), 2))
    for choice in itertools.product(range(3), repeat=len(pairs)):
        par = [0] * n
        for (a, b), c in zip(pairs, choice):
            if c == 1:
                par[b] |= 1 << a
            elif c == 2:
                par[a] |= 1 << b
        done, left = 0, (1 << n) - 1
        progress = True
        while left and progress:
            progress = False
            for v in range(n):
                if left >> v & 1 and par[v] & ~done == 0:
                    done |= 1 << v
                    left &= ~(1 << v)
                    progress = True
        if not left:
            yield par


def robinson(n):
    a = [1]
    for m in range(1, n + 1):
        a.append(sum((-1) ** (k + 1) * math.comb(m, k) * 2 ** (k * (m - k)) * a[m - k] for k in range(1, m + 1)))
    return a[n]


def sample(n, rng, s, arity):
    order = list(range(n))
    rng.shuffle(order)
    par = {v: [u for u in order[:i] if rng.random() < 0.5][:2] for i, v in enumerate(order)}
    table = {}
    data = []
    for _ in range(s):
        x = [0] * n
        for v in order:
            key = (v, tuple(x[u] for u in par[v]))
            if key not in table:
                w = [rng.random() ** 2 for _ in range(arity[v])]
                table[key] = [t / sum(w) for t in w]
            x[v] = rng.choices(range(arity[v]), table[key])[0]
        data.append(tuple(x))
    return data


def pattern(n, par):
    """The skeleton and the v-structures of a DAG."""
    skel = {frozenset((u, v)) for v in range(n) for u in range(n) if par[v] >> u & 1}
    vs = set()
    for v in range(n):
        ps = [u for u in range(n) if par[v] >> u & 1]
        for a, b in itertools.combinations(ps, 2):
            if frozenset((a, b)) not in skel:
                vs.add((frozenset((a, b)), v))
    return frozenset(skel), frozenset(vs)


def test_dag_counts():
    for n in range(1, 5):
        assert sum(1 for _ in all_dags(n)) == robinson(n)
    assert [robinson(n) for n in range(1, 6)] == [1, 3, 25, 543, 29281]


def test_markov_equivalence_class_counts():
    assert len({pattern(3, p) for p in all_dags(3)}) == 11
    assert len({pattern(4, p) for p in all_dags(4)}) == 185


def test_dp_equals_brute_force_on_four_nodes():
    rng = random.Random(2006)
    dags = list(all_dags(4))
    for trial in range(12):
        arity = [rng.choice((2, 3)) for _ in range(4)]
        data = sample(4, rng, rng.randint(15, 60), arity)
        for score in (bic, bdeu):
            ls = local_scores(data, arity, 4, score)
            best, parents = silander_myllymaki(4, ls)
            brute = max(network_score(ls, p) for p in dags)
            assert abs(best - brute) < 1e-9
            assert abs(network_score(ls, parents) - best) < 1e-9
            assert any(parents == p for p in dags)  # the output is acyclic


def test_dp_equals_brute_force_on_five_nodes():
    rng = random.Random(1996)
    dags = list(all_dags(5))
    assert len(dags) == 29281
    for trial in range(2):
        arity = [2] * 5
        data = sample(5, rng, 80, arity)
        ls = local_scores(data, arity, 5, bdeu)
        best, parents = silander_myllymaki(5, ls)
        assert abs(best - max(network_score(ls, p) for p in dags)) < 1e-9


def test_bic_and_bdeu_are_score_equivalent():
    rng = random.Random(1995)
    arity = [2, 3, 2, 2]
    data = sample(4, rng, 50, arity)
    for score in (bic, bdeu):
        ls = local_scores(data, arity, 4, score)
        groups = defaultdict(set)
        for p in all_dags(4):
            groups[pattern(4, p)].add(round(network_score(ls, p), 8))
        assert all(len(g) == 1 for g in groups.values())


def test_learns_a_v_structure_from_many_samples():
    rng = random.Random(7)
    data = []
    for _ in range(3000):
        a, b = rng.randrange(2), rng.randrange(2)
        c = (a ^ b) if rng.random() < 0.9 else 1 - (a ^ b)
        data.append((a, b, c))
    ls = local_scores(data, [2, 2, 2], 3, bic)
    _, parents = silander_myllymaki(3, ls)
    assert parents == [0, 0, 0b011]
