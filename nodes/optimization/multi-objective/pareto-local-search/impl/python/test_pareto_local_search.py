# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pareto-local-search/. The authors are listed in prov/X6FC7X.jsonl.

import itertools
import random

from pareto_local_search import dominates, pareto_local_search, weakly_dominates


def flips(x):
    return [x[:i] + (1 - x[i],) + x[i + 1 :] for i in range(len(x))]


def knap(a, b):
    """Minimize (the value of the items left out, the weight of the items taken)."""
    return lambda x: (sum(u * (1 - v) for u, v in zip(a, x)), sum(u * v for u, v in zip(b, x)))


def front(images):
    return {y for y in images if not any(dominates(z, y) for z in images)}


def test_example() -> None:
    f = knap((4, 1, 3), (2, 5, 3))
    trace = []
    out = pareto_local_search((0, 1, 0), f, flips, lambda x, a: trace.append((x, [y for _, y in a])))
    assert trace == [
        ((0, 1, 0), [(7, 5), (3, 7), (8, 0)]),
        ((1, 1, 0), [(3, 7), (8, 0), (4, 2), (0, 10)]),
        ((0, 0, 0), [(3, 7), (8, 0), (4, 2), (0, 10)]),
        ((1, 0, 0), [(8, 0), (4, 2), (0, 10), (1, 5)]),
        ((1, 1, 1), [(8, 0), (4, 2), (0, 10), (1, 5)]),
        ((1, 0, 1), [(8, 0), (4, 2), (0, 10), (1, 5)]),
    ]
    space = list(itertools.product((0, 1), repeat=3))
    assert {y for _, y in out} == front({f(x) for x in space})


def test_local_trap() -> None:
    # path a - b - c with f(a) = (1, 1), f(b) = (2, 2), f(c) = (0, 0)
    img = {"a": (1, 1), "b": (2, 2), "c": (0, 0)}
    nb = {"a": ["b"], "b": ["a", "c"], "c": ["b"]}
    out = pareto_local_search("a", img.__getitem__, nb.__getitem__)
    assert out == [("a", (1, 1))]


def random_instance(rng, n, p):
    rows = [[rng.randint(0, 9) for _ in range(n)] for _ in range(p)]
    return lambda x: tuple(sum(r[i] * (1 - x[i]) if k % 2 == 0 else r[i] * x[i] for i in range(n)) for k, r in enumerate(rows))


def test_invariants_and_archive_is_front_of_seen() -> None:
    rng = random.Random(7)
    for _ in range(60):
        n, p = rng.randint(2, 7), rng.randint(2, 3)
        f = random_instance(rng, n, p)
        start = tuple(rng.randint(0, 1) for _ in range(n))
        seen = {f(start)}
        visits = []

        def nb(x):
            ys = flips(x)
            seen.update(f(y) for y in ys)
            return ys

        def hook(x, archive):
            visits.append(x)
            imgs = [y for _, y in archive]
            assert len(set(imgs)) == len(imgs)
            assert set(imgs) == front(seen)

        out = pareto_local_search(start, f, nb, hook)
        imgs = [y for _, y in out]
        assert len(visits) == len(set(visits)) <= len(seen)
        assert not any(dominates(u, v) for u in imgs for v in imgs)
        # Pareto local optimum set: every neighbour of a member is weakly dominated by the archive
        for x, _ in out:
            for z in flips(x):
                assert any(weakly_dominates(y, f(z)) for y in imgs)


def test_complete_neighbourhood_gives_the_front() -> None:
    rng = random.Random(11)
    for _ in range(40):
        n, p = rng.randint(1, 6), rng.randint(2, 3)
        f = random_instance(rng, n, p)
        space = list(itertools.product((0, 1), repeat=n))
        out = pareto_local_search(rng.choice(space), f, lambda x: space)
        assert sorted(y for _, y in out) == sorted(front({f(x) for x in space}))


def test_connected_efficient_set_gives_the_front() -> None:
    rng = random.Random(5)
    used = 0
    for _ in range(300):
        n, p = rng.randint(2, 6), 2
        f = random_instance(rng, n, p)
        space = list(itertools.product((0, 1), repeat=n))
        pf = front({f(x) for x in space})
        eff = [x for x in space if f(x) in pf]
        if len({f(x) for x in eff}) != len(eff):
            continue
        reach, todo = {eff[0]}, [eff[0]]
        while todo:
            for z in flips(todo.pop()):
                if z in eff and z not in reach:
                    reach.add(z)
                    todo.append(z)
        if len(reach) != len(eff):
            continue
        used += 1
        out = pareto_local_search(rng.choice(eff), f, flips)
        assert {y for _, y in out} == pf
    assert used >= 20
