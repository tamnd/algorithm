# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-coverage/. The authors are listed in prov/M90XJV.jsonl.

import itertools
import random

from double_coverage import double_coverage


def opt_trajectory(start, requests):
    """Optimal offline k-server cost on the line, with the configurations of one optimal schedule.

    Brute force: a dynamic program over all lazy configurations. A lazy schedule moves
    one server to the request only when no server is there; lazy schedules are optimal.
    """
    layer = {tuple(sorted(start)): (0, None)}
    layers = [layer]
    for r in requests:
        nxt = {}
        for conf, (c, _) in layer.items():
            if r in conf:
                cand = [(conf, c)]
            else:
                cand = []
                for j, x in enumerate(conf):
                    new = tuple(sorted(conf[:j] + (r,) + conf[j + 1:]))
                    cand.append((new, c + abs(x - r)))
            for new, cost in cand:
                if new not in nxt or cost < nxt[new][0]:
                    nxt[new] = (cost, conf)
        layer = nxt
        layers.append(layer)
    best = min(layer, key=lambda conf: layer[conf][0])
    total = layer[best][0]
    path = [best]
    for t in range(len(requests), 0, -1):
        path.append(layers[t][path[-1]][1])
    path.reverse()
    return total, path


def matching(a, b):
    """Minimum cost perfect matching between two point lists, by trying all bijections."""
    return min(sum(abs(x - y) for x, y in zip(a, p)) for p in itertools.permutations(b))


def spread(a):
    return sum(abs(x - y) for x, y in itertools.combinations(a, 2))


def test_example() -> None:
    cost, pos = double_coverage([0, 10, 20], [12, 4, 13, 19, 6, 20, 30])
    assert cost == 43
    assert pos == [6, 11, 30]


def test_one_server_is_optimal() -> None:
    rng = random.Random(11)
    for _ in range(200):
        reqs = [rng.randint(0, 20) for _ in range(rng.randint(0, 12))]
        start = rng.randint(0, 20)
        cost, _ = double_coverage([start], reqs)
        assert cost == opt_trajectory([start], reqs)[0]


def test_edges() -> None:
    assert double_coverage([3, 7], []) == (0, [3, 7])
    assert double_coverage([3, 7], [3, 7, 3]) == (0, [3, 7])
    assert double_coverage([7, 3], [5]) == (4, [5, 5])
    assert double_coverage([0, 10], [-5, 15]) == (10, [-5, 15])


def test_k_competitive_with_potential() -> None:
    rng = random.Random(2024)
    for _ in range(400):
        k = rng.randint(1, 3)
        start = rng.sample(range(0, 13), k)
        reqs = [rng.randint(0, 12) for _ in range(rng.randint(1, 9))]
        opt, path = opt_trajectory(start, reqs)
        dc_total, _ = double_coverage(start, reqs)
        assert dc_total <= k * opt + spread(start)
        # The potential k*M + (sum of pairwise distances) pays for each step.
        s = sorted(start)
        phi = k * matching(s, list(path[0])) + spread(s)
        assert phi == spread(start)
        for t, r in enumerate(reqs):
            opt_step = matching(list(path[t]), list(path[t + 1]))
            step, s = double_coverage(s, [r])
            new_phi = k * matching(s, list(path[t + 1])) + spread(s)
            assert step + new_phi - phi <= k * opt_step
            phi = new_phi


def test_adversary_on_k_plus_one_points() -> None:
    # Always request the one point of {0, ..., k} that DC leaves uncovered.
    for k in (2, 3):
        s = list(range(k))
        reqs = []
        for _ in range(12):
            free = [p for p in range(k + 1) if p not in s]
            r = free[0]
            reqs.append(r)
            _, s = double_coverage(s, [r])
            assert all(x in range(k + 1) for x in s)
        dc_total, _ = double_coverage(list(range(k)), reqs)
        opt, _ = opt_trajectory(list(range(k)), reqs)
        assert dc_total <= k * opt + spread(list(range(k)))
        assert dc_total == k * opt
