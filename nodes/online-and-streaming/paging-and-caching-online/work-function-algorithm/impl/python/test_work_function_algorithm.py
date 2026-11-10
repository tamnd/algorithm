# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/work-function-algorithm/. The authors are listed in prov/CQEK7R.jsonl.

import random

from work_function_algorithm import config_distance, work_function_algorithm


def random_metric(rng, n, top=9):
    """Shortest path distances of a random complete graph with integer weights, so a metric."""
    d = [[0 if i == j else rng.randint(1, top) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i):
            d[i][j] = d[j][i]
    for m in range(n):
        for i in range(n):
            for j in range(n):
                d[i][j] = min(d[i][j], d[i][m] + d[m][j])
    return d


def line_metric(points):
    return [[abs(a - b) for b in points] for a in points]


def brute_opt(d, start, requests):
    """Offline optimum by a dynamic program over lazy configurations."""
    layer = {frozenset(start): 0}
    for r in requests:
        nxt = {}
        for conf, c in layer.items():
            if r in conf:
                options = [(conf, c)]
            else:
                options = [((conf - {x}) | {r}, c + d[x][r]) for x in conf]
            for new, cost in options:
                if new not in nxt or cost < nxt[new]:
                    nxt[new] = cost
        layer = nxt
    return min(layer.values())


def cases(seed, count, max_n=6, max_k=3, max_m=10):
    rng = random.Random(seed)
    for _ in range(count):
        n = rng.randint(2, max_n)
        k = rng.randint(1, min(max_k, n - 1))
        d = random_metric(rng, n)
        start = rng.sample(range(n), k)
        requests = [rng.randrange(n) for _ in range(rng.randint(0, max_m))]
        yield d, start, requests


def test_line_example() -> None:
    # Points 0, 10 and 11 of the line; servers at 0 and 10; requests 11, 10, 11, 10, ...
    d = line_metric([0, 10, 11])
    requests = [2, 1] * 13
    cost, configs, works = work_function_algorithm(d, [0, 1], requests)
    assert min(works[-1].values()) == brute_opt(d, [0, 1], requests) == 11
    assert cost == 29
    assert configs[19] == frozenset({0, 2})
    assert configs[20] == configs[-1] == frozenset({1, 2})
    assert [works[19][frozenset(x)] for x in ({0, 1}, {0, 2}, {1, 2})] == [20, 19, 11]


def test_offline_optimum_is_min_of_work_function() -> None:
    for d, start, requests in cases(1, 150):
        _, _, works = work_function_algorithm(d, start, requests)
        assert min(works[-1].values()) == brute_opt(d, start, requests)


def test_one_server_is_optimal() -> None:
    for d, start, requests in cases(2, 100, max_k=1):
        cost, _, _ = work_function_algorithm(d, start[:1], requests)
        assert cost == brute_opt(d, start[:1], requests)


def test_identity_and_extended_cost() -> None:
    for d, start, requests in cases(3, 150):
        cost, configs, works = work_function_algorithm(d, start, requests)
        total_ext = 0
        for t in range(1, len(works)):
            before, after = configs[t - 1], configs[t]
            # The WFA move lands where w_t(C_{t-1}) = w_t(C_t) + D(C_{t-1}, C_t).
            assert works[t][before] == works[t][after] + config_distance(d, before, after)
            # w_t is at least w_{t-1}, and Lipschitz in the configuration.
            assert all(works[t][x] >= works[t - 1][x] for x in works[t])
            total_ext += max(works[t][x] - works[t - 1][x] for x in works[t])
        opt = min(works[-1].values())
        assert cost + opt <= total_ext


def test_k_plus_one_points() -> None:
    rng = random.Random(4)
    for _ in range(150):
        k = rng.randint(1, 4)
        d = random_metric(rng, k + 1)
        diam = max(max(row) for row in d)
        start = rng.sample(range(k + 1), k)
        requests = [rng.randrange(k + 1) for _ in range(rng.randint(0, 14))]
        cost, _, _ = work_function_algorithm(d, start, requests)
        assert cost <= k * brute_opt(d, start, requests) + k * diam


def test_two_k_minus_one_bound_with_slack() -> None:
    for d, start, requests in cases(5, 150, max_m=14):
        k = len(start)
        diam = max(max(row) for row in d)
        cost, _, _ = work_function_algorithm(d, start, requests)
        assert cost <= (2 * k - 1) * brute_opt(d, start, requests) + k * k * diam


def test_adversary_on_k_plus_one_points_gives_ratio_near_k() -> None:
    d = line_metric([0, 1, 3])
    start, requests = [0, 1], []
    conf = frozenset(start)
    for _ in range(30):
        r = next(p for p in range(3) if p not in conf)
        requests.append(r)
        _, configs, _ = work_function_algorithm(d, start, requests)
        conf = configs[-1]
    cost, _, _ = work_function_algorithm(d, start, requests)
    opt = brute_opt(d, start, requests)
    assert cost <= 2 * opt + 2 * 3
    assert cost >= 2 * opt - 2 * 3
