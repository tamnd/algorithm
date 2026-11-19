# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mention-pair-model/. The authors are listed in prov/XJ8G58.jsonl.

import random

from mention_pair_model import (DisjointSet, best_first, closest_first, clusters_from_antecedents,
                                components, log_loss, log_loss_grad, ng_cardie_instances,
                                non_transitive_triples, soon_instances, train)

# The example of the page: Mary(0) met John(1). He(2) gave her(3) a book(4). Mary(5) thanked ...
CHAIN = [0, 1, 1, 0, 2, 0]
PRON = [False, False, True, True, False, False]
P = {(0, 1): 0.1, (0, 2): 0.2, (1, 2): 0.9, (0, 3): 0.8, (1, 3): 0.3, (2, 3): 0.52,
     (0, 4): 0.05, (1, 4): 0.05, (2, 4): 0.05, (3, 4): 0.05,
     (0, 5): 0.95, (1, 5): 0.1, (2, 5): 0.1, (3, 5): 0.4, (4, 5): 0.05}


def prob(i, j):
    return P[(i, j)]


def test_soon_instances():
    assert soon_instances(CHAIN) == [(1, 2, 1), (0, 3, 1), (1, 3, 0), (2, 3, 0), (3, 5, 1), (4, 5, 0)]


def test_ng_cardie_instances():
    got = ng_cardie_instances(CHAIN, PRON)
    assert got == [(1, 2, 1), (0, 3, 1), (1, 3, 0), (2, 3, 0), (0, 5, 1), (1, 5, 0), (2, 5, 0), (4, 5, 0)]


def test_closest_and_best_first():
    cf = closest_first(6, prob)
    bf = best_first(6, prob)
    assert cf == [None, None, 1, 2, None, 0]
    assert bf == [None, None, 1, 0, None, 0]
    assert clusters_from_antecedents(cf) == [[0, 5], [1, 2, 3], [4]]
    assert clusters_from_antecedents(bf) == [[0, 3, 5], [1, 2], [4]]


def test_pairwise_decisions_are_not_transitive():
    assert (0, 2, 3) in non_transitive_triples(6, prob)
    assert sorted(non_transitive_triples(6, prob)) == [(0, 2, 3), (0, 3, 5), (1, 2, 3)]
    # Linking all pairs above 0.5 and closing transitively merges two gold entities.
    links = [k for k, v in P.items() if v > 0.5]
    assert components(6, links) == [[0, 1, 2, 3, 5], [4]]


def brute_closest(n, prob):
    out = [None] * n
    for j in range(n):
        cands = [i for i in range(j) if prob(i, j) > 0.5]
        out[j] = max(cands) if cands else None
    return out


def brute_best(n, prob):
    out = [None] * n
    for j in range(n):
        cands = [i for i in range(j) if prob(i, j) > 0.5]
        if cands:
            top = max(prob(i, j) for i in cands)
            out[j] = max(i for i in cands if prob(i, j) == top)
    return out


def test_linkers_against_definitions():
    rng = random.Random(5)
    for _ in range(200):
        n = rng.randint(1, 9)
        table = {(i, j): rng.choice([0.1, 0.3, 0.5, 0.6, 0.7, 0.9]) for j in range(n) for i in range(j)}
        f = lambda i, j: table[(i, j)]
        assert closest_first(n, f) == brute_closest(n, f)
        assert best_first(n, f) == brute_best(n, f)


def bfs_components(n, links):
    adj = {k: set() for k in range(n)}
    for a, b in links:
        adj[a].add(b)
        adj[b].add(a)
    seen, out = set(), []
    for s in range(n):
        if s in seen:
            continue
        comp, stack = [], [s]
        seen.add(s)
        while stack:
            x = stack.pop()
            comp.append(x)
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        out.append(sorted(comp))
    return sorted(out)


def test_union_find_against_search():
    rng = random.Random(6)
    for _ in range(200):
        n = rng.randint(1, 12)
        links = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 10))]
        assert components(n, links) == bfs_components(n, links)
    ds = DisjointSet(3)
    ds.union(0, 1)
    assert ds.find(0) == ds.find(1) != ds.find(2)


def synthetic_docs(rng, count):
    """Documents of mentions (entity, gender, is_pronoun, sentence); entities have a name and a gender."""
    docs = []
    for _ in range(count):
        ents = [(e, rng.choice("mfn")) for e in range(3)]
        ms = []
        for s in range(4):
            for _ in range(rng.randint(1, 2)):
                e, g = rng.choice(ents)
                ms.append((e, g, rng.random() < 0.4, s))
        docs.append(ms)
    return docs


def features(a, b):
    """Bias, same name (both not pronouns and same entity name), anaphor is a pronoun,
    gender agreement, and the sentence distance (scaled)."""
    same_name = 1.0 if (not a[2] and not b[2] and a[0] == b[0]) else 0.0
    return [1.0, same_name, 1.0 if b[2] else 0.0, 1.0 if a[1] == b[1] else 0.0, (b[3] - a[3]) / 3.0]


def instances(docs):
    data = []
    for ms in docs:
        for i, j, y in soon_instances([m[0] for m in ms]):
            data.append((features(ms[i], ms[j]), y))
    return data


def test_gradient_finite_differences():
    rng = random.Random(8)
    data = instances(synthetic_docs(rng, 5))
    h = 1e-6
    for _ in range(5):
        w = [rng.uniform(-1, 1) for _ in range(5)]
        g = log_loss_grad(w, data, 0.01)
        for k in range(5):
            up, dn = list(w), list(w)
            up[k] += h
            dn[k] -= h
            num = (log_loss(up, data, 0.01) - log_loss(dn, data, 0.01)) / (2 * h)
            assert abs(num - g[k]) < 1e-5


def test_training_learns_string_match_and_agreement():
    rng = random.Random(9)
    data = instances(synthetic_docs(rng, 60))
    w = train(data, 5, steps=400)
    assert log_loss(w, data, 0.01) < log_loss([0.0] * 5, data, 0.01)
    assert w[1] > 0 and w[3] > 0  # same name and gender agreement push toward coreference
