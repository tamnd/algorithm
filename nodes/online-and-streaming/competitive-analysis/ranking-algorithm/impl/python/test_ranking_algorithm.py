# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ranking-algorithm/. The authors are listed in prov/NV7H45.jsonl.

import math
import random
from collections.abc import Hashable, Sequence
from fractions import Fraction

from ranking_algorithm import F, Ranking, expected_size, g, ranking, ranking_dual, ranking_with_order, size

C = 1 - 1 / math.e


def max_matching(arrivals: Sequence[Sequence[Hashable]]) -> int:
    """Maximum bipartite matching by augmenting paths (Kuhn), small inputs."""
    owner: dict[Hashable, int] = {}

    def augment(v: int, seen: set) -> bool:
        for u in arrivals[v]:
            if u in seen:
                continue
            seen.add(u)
            if u not in owner or augment(owner[u], seen):
                owner[u] = v
                return True
        return False

    return sum(1 for v in range(len(arrivals)) if augment(v, set()))


def upper_triangular(n: int) -> list[list[int]]:
    return [list(range(j, n)) for j in range(n)]


def test_example_from_page() -> None:
    arr = [["u1", "u2", "u3"], ["u2", "u3"], ["u3"]]
    assert ranking_with_order(["u1", "u2", "u3"], arr) == ["u1", "u2", "u3"]
    assert ranking_with_order(["u2", "u3", "u1"], arr) == ["u2", "u3", None]
    assert expected_size(["u1", "u2", "u3"], arr) == Fraction(13, 6)


def test_upper_triangular_exact() -> None:
    want = [Fraction(1), Fraction(3, 2), Fraction(13, 6), Fraction(67, 24),
            Fraction(137, 40), Fraction(2921, 720), Fraction(23633, 5040)]
    for n in range(1, 8):
        e = expected_size(list(range(n)), upper_triangular(n))
        assert e == want[n - 1]
        assert e >= C * n
        assert e <= (n + 1) * C + 2


def test_ratio_on_random_instances() -> None:
    rng = random.Random(7)
    for _ in range(250):
        k = rng.randint(1, 5)
        n = rng.randint(1, 6)
        p = rng.choice([0.3, 0.5, 0.8])
        arr = [[u for u in range(k) if rng.random() < p] for _ in range(n)]
        e = expected_size(list(range(k)), arr)
        assert e >= C * max_matching(arr)


def test_kvv_family() -> None:
    want = {1: Fraction(3, 2), 2: Fraction(35, 12), 3: Fraction(517, 120)}
    for k, w in want.items():
        arr = [[i] + list(range(k, 2 * k)) for i in range(k)] + [[i] for i in range(k, 2 * k)]
        assert max_matching(arr) == 2 * k
        assert expected_size(list(range(2 * k)), arr) == w


def run_free_sets(y: dict, arrivals: Sequence[Sequence[Hashable]]) -> list[set]:
    r = Ranking(y)
    out = [set(r.free)]
    for nb in arrivals:
        r.arrive(nb)
        out.append(set(r.free))
    return out


def test_primal_dual_lemmas() -> None:
    rng = random.Random(11)
    for _ in range(400):
        k = rng.randint(1, 6)
        n = rng.randint(1, 6)
        arr = [[u for u in range(k) if rng.random() < 0.5] for _ in range(n)]
        y = {u: rng.random() for u in range(k)}
        match, alpha, beta = ranking_dual(y, arr)
        assert abs(sum(alpha.values()) + sum(beta) - size(match) / F) < 1e-9
        full_free = run_free_sets(y, arr)
        for u in range(k):
            y_wo = {x: y[x] for x in y if x != u}
            arr_wo = [[x for x in nb if x != u] for nb in arr]
            match_wo = ranking_with_order(sorted(y_wo, key=y_wo.get), arr_wo)
            # the free sets differ by at most one vertex: F' = F or F' = F + {z}
            for a, b in zip(full_free, run_free_sets(y_wo, arr_wo)):
                assert b <= a and len(a - b) <= 1
            for t, nb in enumerate(arr):
                if u not in nb:
                    continue
                yc = 1.0 if match_wo[t] is None else y[match_wo[t]]
                if y[u] < yc:
                    assert u in match
                assert beta[t] >= (1 - g(yc)) / F - 1e-12


def test_random_runs_are_matchings() -> None:
    rng = random.Random(3)
    for _ in range(300):
        k = rng.randint(1, 8)
        arr = [[u for u in range(k) if rng.random() < 0.4] for _ in range(rng.randint(1, 8))]
        m = ranking(range(k), arr, rng)
        used = [u for u in m if u is not None]
        assert len(used) == len(set(used))
        assert all(u is None or u in arr[t] for t, u in enumerate(m))
        assert 2 * size(m) >= max_matching(arr)


if __name__ == "__main__":
    for name, f in list(globals().items()):
        if name.startswith("test_"):
            f()
    print("ok")
