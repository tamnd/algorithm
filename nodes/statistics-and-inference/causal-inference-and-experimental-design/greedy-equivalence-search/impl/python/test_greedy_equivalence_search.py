# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-equivalence-search/. The authors are listed in prov/08T080.jsonl.

import itertools
import random
from fractions import Fraction

from greedy_equivalence_search import (
    conditional_variance, consistent_extension, cpdag_of_dag, gaussian_bic, ges,
    sample_covariance, sample_sem, sem_covariance,
)

EXAMPLE_NODES = ["A", "B", "C", "D", "E"]
EXAMPLE_WEIGHTS = {("A", "B"): Fraction(4, 5), ("A", "C"): Fraction(7, 10), ("B", "D"): Fraction(3, 5),
                   ("C", "D"): Fraction(3, 5), ("D", "E"): Fraction(9, 10)}
EXAMPLE_DAG = {"A": set(), "B": {"A"}, "C": {"A"}, "D": {"B", "C"}, "E": {"D"}}


# ---------------------------------------------------------------------------
# The large-sample limit of the Gaussian BIC, with exact fractions.
#
# local(v, P) = -(N/2) log Var(v | P) - (|P|/2) log N. For N large enough,
# a difference of two such scores is positive exactly when the ratio of the
# variances is above 1, or equal to 1 with fewer parents. Limit and Delta
# encode this order exactly.


class Delta:
    def __init__(self, ratio, params):
        self.ratio, self.params = ratio, params

    def __gt__(self, other):
        if isinstance(other, int):
            other = Delta(Fraction(1), 0)
        return (self.ratio, self.params) > (other.ratio, other.params)

    def __le__(self, other):
        return not self > other


class Limit:
    def __init__(self, var, k):
        self.var, self.k = var, k

    def __sub__(self, other):
        # (-log var1, -k1) - (-log var2, -k2) = (log(var2 / var1), k2 - k1)
        return Delta(other.var / self.var, other.k - self.k)


def limit_score(cov):
    cache = {}

    def local(v, ps):
        if (v, ps) not in cache:
            cache[(v, ps)] = Limit(conditional_variance(cov, v, sorted(ps)), len(ps))
        return cache[(v, ps)]

    return local


def limit_total(local, nodes, parents):
    prod, k = Fraction(1), 0
    for v in nodes:
        s = local(v, frozenset(parents[v]))
        prod *= s.var
        k += s.k
    return -prod, -k  # larger is better


# ---------------------------------------------------------------------------
# Helpers


def all_dags(nodes):
    pairs = list(itertools.combinations(nodes, 2))
    for choice in itertools.product((0, 1, 2), repeat=len(pairs)):
        parents = {v: set() for v in nodes}
        for (u, v), c in zip(pairs, choice):
            if c == 1:
                parents[v].add(u)
            elif c == 2:
                parents[u].add(v)
        if topological_order(nodes, parents) is not None:
            yield parents


def topological_order(nodes, parents):
    order, left = [], set(nodes)
    while left:
        free = [v for v in sorted(left) if not (parents[v] & left)]
        if not free:
            return None
        order.append(free[0])
        left.discard(free[0])
    return order


def random_weights(rng, parents):
    w = {}
    for v in sorted(parents):  # sorted: set order of strings varies between runs
        for p in sorted(parents[v]):
            # Many distinct values, so that exact cancellations of paths
            # (unfaithful models) are unlikely.
            w[(p, v)] = Fraction(rng.randint(300, 1000), 1000) * rng.choice((1, -1))
    return w


def dsep(parents, a, b, s):
    keep, stack = {a, b} | s, [a, b, *s]
    while stack:
        v = stack.pop()
        for p in parents[v]:
            if p not in keep:
                keep.add(p)
                stack.append(p)
    nb = {v: set() for v in keep}
    for v in keep:
        for p in parents[v]:
            nb[v].add(p)
            nb[p].add(v)
        for p, q in itertools.combinations(parents[v], 2):
            nb[p].add(q)
            nb[q].add(p)
    seen, stack = {a}, [a]
    while stack:
        v = stack.pop()
        if v == b:
            return False
        for w in nb[v]:
            if w not in seen and w not in s:
                seen.add(w)
                stack.append(w)
    return True


def key(g):
    arrows, lines = g.edges()
    return tuple(arrows), tuple(lines)


def class_key(nodes, parents):
    return key(cpdag_of_dag(nodes, parents))


# ---------------------------------------------------------------------------
# Tests


def test_worked_example():
    res = ges(EXAMPLE_NODES, gaussian_bic(sem_covariance(EXAMPLE_NODES, EXAMPLE_WEIGHTS), 1000))
    kinds = [(k, x, y, sorted(t)) for k, x, y, t, _ in res.steps]
    assert kinds == [("insert", "D", "E", []), ("insert", "B", "D", []), ("insert", "D", "C", []),
                     ("insert", "A", "B", []), ("insert", "C", "A", ["B"]), ("insert", "B", "C", []),
                     ("delete", "B", "C", ["D"])]
    assert key(res.cpdag) == class_key(EXAMPLE_NODES, EXAMPLE_DAG)
    assert res.evaluations == 150


def test_local_optimum_at_smaller_sample_size():
    # With the same exact covariance but N = 500, the forward phase stops with
    # the collider at A, and the true class has a higher score.
    cov = sem_covariance(EXAMPLE_NODES, EXAMPLE_WEIGHTS)
    local = gaussian_bic(cov, 500)
    res = ges(EXAMPLE_NODES, local)
    assert res.cpdag.edges() == ([("B", "A"), ("C", "A")], [("B", "D"), ("C", "D"), ("D", "E")])
    ext = consistent_extension(res.cpdag)
    got = sum(local(v, frozenset(ext[v])) for v in EXAMPLE_NODES)
    true = sum(local(v, frozenset(EXAMPLE_DAG[v])) for v in EXAMPLE_NODES)
    assert true > got + 1.9
    prod = Fraction(1)
    for v in EXAMPLE_NODES:
        prod *= conditional_variance(cov, v, sorted(ext[v]))
    assert prod == Fraction(3086174, 3061875)  # the true class has product 1


def test_cpdag_and_extension_round_trip():
    nodes = list("ABCD")
    for parents in all_dags(nodes):
        g = cpdag_of_dag(nodes, parents)
        ext = consistent_extension(g)
        assert ext is not None and class_key(nodes, ext) == key(g)


def test_score_equivalence_exact():
    # Equivalent DAGs have the same product of conditional variances, exactly.
    rng = random.Random(3)
    nodes = list("ABCD")
    full = {v: set(nodes[:i]) for i, v in enumerate(nodes)}
    cov = sem_covariance(nodes, random_weights(rng, full))
    products = {}
    for parents in all_dags(nodes):
        prod = Fraction(1)
        for v in nodes:
            prod *= conditional_variance(cov, v, sorted(parents[v]))
        products.setdefault(class_key(nodes, parents), set()).add(prod)
    assert len(products) == 185
    assert all(len(p) == 1 for p in products.values())


def test_local_consistency_of_limit_score():
    rng = random.Random(11)
    nodes = list("ABCD")
    for parents in itertools.islice(all_dags(nodes), 0, 543, 5):
        cov = sem_covariance(topological_order(nodes, parents), random_weights(rng, parents))
        local = limit_score(cov)
        for x, y in itertools.permutations(nodes, 2):
            rest = [v for v in nodes if v not in (x, y)]
            for k in range(len(rest) + 1):
                for p in itertools.combinations(rest, k):
                    delta = local(y, frozenset(p) | {x}) - local(y, frozenset(p))
                    assert (delta > 0) == (not dsep(parents, x, y, set(p)))


def check_all_dags(nodes, seed):
    rng = random.Random(seed)
    dags = list(all_dags(nodes))
    for truth in dags:
        cov = sem_covariance(topological_order(nodes, truth), random_weights(rng, truth))
        local = limit_score(cov)
        res = ges(nodes, local)
        best = max(dags, key=lambda d: limit_total(local, nodes, d))
        assert key(res.cpdag) == class_key(nodes, best)
        assert key(res.cpdag) == class_key(nodes, truth)
    return len(dags)


def test_every_dag_on_three_nodes_against_exhaustive_search():
    assert check_all_dags(list("ABC"), 1) == 25


def test_every_dag_on_four_nodes_against_exhaustive_search():
    assert check_all_dags(list("ABCD"), 2) == 543


def test_float_bic_at_large_n_on_four_nodes():
    # With the float BIC at N = 10^6, GES still finds the best class over all
    # 543 DAGs. It can differ from the truth when a partial correlation is so
    # small that the penalty wins; that is a property of the score.
    rng = random.Random(4)
    nodes = list("ABCD")
    dags = list(all_dags(nodes))
    agree_truth = 0
    for truth in dags:
        cov = sem_covariance(topological_order(nodes, truth), random_weights(rng, truth))
        local = gaussian_bic(cov, 10 ** 6)
        res = ges(nodes, local)
        best = max(dags, key=lambda d: sum(local(v, frozenset(d[v])) for v in nodes))
        assert key(res.cpdag) == class_key(nodes, best)
        agree_truth += key(res.cpdag) == class_key(nodes, truth)
    assert agree_truth == 537  # measured: 6 of the 543 models lose one weak edge


def test_random_dags_on_six_nodes():
    rng = random.Random(6)
    nodes = list("ABCDEF")
    for _ in range(30):
        order = nodes[:]
        rng.shuffle(order)
        parents = {v: set() for v in nodes}
        for i, j in itertools.combinations(range(6), 2):
            if rng.random() < 0.4:
                parents[order[j]].add(order[i])
        cov = sem_covariance(order, random_weights(rng, parents))
        res = ges(nodes, limit_score(cov))
        assert key(res.cpdag) == class_key(nodes, parents)


def test_empty_graph_best_case():
    nodes = list("ABCDE")
    cov = {u: {v: Fraction(int(u == v)) for v in nodes} for u in nodes}
    res = ges(nodes, gaussian_bic(cov, 1000))
    assert res.steps == [] and res.evaluations == 5 * 4


def test_finite_samples_success_rate():
    # Measured, not proved: 50 data sets of size 2000 from the example model.
    ok = 0
    truth = class_key(EXAMPLE_NODES, EXAMPLE_DAG)
    for seed in range(50):
        rng = random.Random(seed)
        rows = sample_sem(EXAMPLE_NODES, EXAMPLE_WEIGHTS, 2000, rng)
        res = ges(EXAMPLE_NODES, gaussian_bic(sample_covariance(rows, EXAMPLE_NODES), 2000))
        ok += key(res.cpdag) == truth
    assert ok == 40
