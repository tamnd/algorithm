# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/leiden-algorithm/. The authors are listed in prov/K4ZNR0.jsonl.

import random
from collections import deque
from fractions import Fraction
from itertools import combinations

from leiden_algorithm import leiden_algorithm


def modularity(n, edges, groups):
    """Weighted modularity from the definition, over ordered pairs of vertices."""
    a = [[Fraction(0)] * n for _ in range(n)]
    for u, v, w in edges:
        if u == v:
            a[u][u] += 2 * w
        else:
            a[u][v] += w
            a[v][u] += w
    k = [sum(row) for row in a]
    two_w = sum(k)
    label = {}
    for i, g in enumerate(groups):
        for v in g:
            label[v] = i
    q = Fraction(0)
    for i in range(n):
        for j in range(n):
            if label[i] == label[j]:
                q += a[i][j] - k[i] * k[j] / two_w
    return q / two_w


def is_connected(group, edges):
    inside = set(group)
    seen = {group[0]}
    stack = [group[0]]
    while stack:
        x = stack.pop()
        for u, v, _ in edges:
            for a, b in ((u, v), (v, u)):
                if a == x and b in inside and b not in seen:
                    seen.add(b)
                    stack.append(b)
    return len(seen) == len(inside)


def reference(n, edges):
    """The same rules on blocks of original vertices, each score computed from the definition."""
    if sum(w for _, _, w in edges) == 0:
        return [[v] for v in range(n)]
    linked = set()
    weight = {}
    deg = [0] * n
    for u, v, w in edges:
        linked.add((u, v))
        linked.add((v, u))
        deg[u] += w
        deg[v] += w
        if u != v:
            weight[(u, v)] = weight.get((u, v), 0) + w
            weight[(v, u)] = weight.get((v, u), 0) + w
    two_w = sum(deg)

    def touch(x, y):
        return any((a, b) in linked for a in x for b in y)

    def between(x, y):
        return sum(weight.get((a, b), 0) for a in x for b in y)

    def vol(x):
        return sum(deg[a] for a in x)

    def groups_of(blocks, comm):
        out = {}
        for b, c in enumerate(comm):
            out.setdefault(c, []).extend(blocks[b])
        return list(out.values())

    def move_fast(blocks, comm):
        k = len(blocks)

        def choice(b):
            old = comm[b]
            alone = sum(1 for c in comm if c == old) == 1

            def score(target):
                trial = comm[:]
                trial[b] = target
                return modularity(n, edges, groups_of(blocks, trial))

            near = sorted({comm[c] for c in range(k) if c != b and touch(blocks[b], blocks[c])})
            best, best_q = old, score(old)
            for c in near:
                if c != old and score(c) > best_q:
                    best, best_q = c, score(c)
            if not alone:
                free = min(c for c in range(k) if c not in comm)
                if score(free) > best_q:
                    best = free
            return best

        queue = deque(range(k))
        while True:
            while queue:
                b = queue.popleft()
                best = choice(b)
                moved = best != comm[b]
                comm[b] = best
                if moved:
                    for c in range(k):
                        if c != b and touch(blocks[b], blocks[c]) and comm[c] != best and c not in queue:
                            queue.append(c)
            pending = [b for b in range(k) if choice(b) != comm[b]]
            if not pending:
                return comm
            queue.extend(pending)

    def refine(blocks, comm):
        k = len(blocks)
        label = list(range(k))
        firsts = []
        for c in comm:
            if c not in firsts:
                firsts.append(c)
        for c in firsts:
            mem = [b for b in range(k) if comm[b] == c]
            whole = sum((blocks[b] for b in mem), [])
            good = []
            for b in mem:
                rest = [x for x in whole if x not in blocks[b]]
                if between(blocks[b], rest) * two_w >= vol(blocks[b]) * vol(rest):
                    good.append(b)
            for b in good:
                if sum(1 for x in label if x == label[b]) != 1:
                    continue
                best, best_q = None, None
                for s in sorted(set(label[x] for x in mem if x != b)):
                    part = sum((blocks[x] for x in mem if label[x] == s), [])
                    rest = [x for x in whole if x not in part]
                    if not touch(blocks[b], part):
                        continue
                    if between(part, rest) * two_w < vol(part) * vol(rest):
                        continue
                    trial = label[:]
                    trial[b] = s
                    q = modularity(n, edges, groups_of(blocks, trial))
                    if best is None or q > best_q:
                        best, best_q = s, q
                if best is not None and best_q >= modularity(n, edges, groups_of(blocks, label)):
                    label[b] = best
        return label

    result = [[v] for v in range(n)]
    while True:
        previous = result
        blocks = [[v] for v in range(n)]
        comm = [0] * n
        for i, g in enumerate(result):
            for v in g:
                comm[v] = i
        while True:
            comm = move_fast(blocks, comm)
            if len(set(comm)) == len(blocks):
                break
            label = refine(blocks, comm)
            order = []
            for x in label:
                if x not in order:
                    order.append(x)
            coarse = []
            new_blocks, new_comm = [], []
            for x in order:
                mem = [b for b in range(len(blocks)) if label[b] == x]
                new_blocks.append(sum((blocks[b] for b in mem), []))
                if comm[mem[0]] not in coarse:
                    coarse.append(comm[mem[0]])
                new_comm.append(coarse.index(comm[mem[0]]))
            for b in range(len(blocks)):
                if comm[b] not in coarse:
                    coarse.append(comm[b])
            blocks, comm = new_blocks, new_comm
        result = sorted(sorted(g) for g in groups_of(blocks, comm))
        if result == previous:
            return result


def all_partitions(items):
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for p in all_partitions(rest):
        for i in range(len(p)):
            yield p[:i] + [[first] + p[i]] + p[i + 1 :]
        yield [[first]] + p


def random_weighted(rng, n, p):
    edges = [(u, v, rng.choice([1, 1, 1, 2, 3])) for u, v in combinations(range(n), 2) if rng.random() < p]
    if n and rng.random() < 0.2:
        v = rng.randrange(n)
        edges.append((v, v, rng.choice([1, 2])))
    return edges


def test_example():
    edges = [(u, v, 1) for u, v in [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6)]]
    comms = leiden_algorithm(7, edges)
    assert comms == [[0, 1, 2, 3], [4, 5, 6]]
    assert modularity(7, edges, comms) == Fraction(59, 162)


def test_edge_cases():
    assert leiden_algorithm(0, []) == []
    assert leiden_algorithm(3, []) == [[0], [1], [2]]
    assert leiden_algorithm(2, [(0, 1, 1)]) == [[0, 1]]
    assert leiden_algorithm(4, [(0, 1, 1), (2, 3, 1)]) == [[0, 1], [2, 3]]
    assert leiden_algorithm(3, [(1, 1, 2)]) == [[0], [1], [2]]
    assert leiden_algorithm(5, [(0, 1, 1), (0, 1, 2), (3, 4, 1)]) == [[0, 1], [2], [3, 4]]


def test_random_against_reference():
    rng = random.Random(20190326)
    for _ in range(300):
        n = rng.randint(0, 8)
        edges = random_weighted(rng, n, rng.choice([0.2, 0.4, 0.6]))
        assert leiden_algorithm(n, edges) == reference(n, edges)


def test_connected_and_locally_optimal():
    rng = random.Random(5233)
    for _ in range(400):
        n = rng.randint(1, 12)
        edges = random_weighted(rng, n, rng.choice([0.15, 0.3, 0.5]))
        comms = leiden_algorithm(n, edges)
        assert sorted(v for c in comms for v in c) == list(range(n))
        for c in comms:
            assert is_connected(c, edges)
        if not edges:
            continue
        q = modularity(n, edges, comms)
        assert q >= modularity(n, edges, [[v] for v in range(n)])
        where = {v: i for i, c in enumerate(comms) for v in c}
        for v in range(n):
            options = {where[u] for u, w, _ in edges if w == v and u != v}
            options |= {where[w] for u, w, _ in edges if u == v and w != v}
            options.add(len(comms))
            for t in options:
                if t == where[v]:
                    continue
                trial = [[x for x in c if x != v] for c in comms] + [[]]
                trial[t].append(v)
                assert modularity(n, edges, [c for c in trial if c]) <= q


def test_never_above_optimum():
    rng = random.Random(2019)
    for _ in range(120):
        n = rng.randint(1, 7)
        edges = random_weighted(rng, n, 0.45)
        if not edges:
            continue
        q = modularity(n, edges, leiden_algorithm(n, edges))
        assert q <= max(modularity(n, edges, p) for p in all_partitions(list(range(n))))


if __name__ == "__main__":
    test_example()
    test_edge_cases()
    test_random_against_reference()
    test_connected_and_locally_optimal()
    test_never_above_optimum()
    print("ok")
