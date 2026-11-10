# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/balance-algorithm/. The authors are listed in prov/QHSMWD.jsonl.

import itertools
import random
from collections.abc import Hashable, Sequence

from balance_algorithm import Balance, balance, balance_ratio, bjn_adwords, msvv, size


def max_b_matching(arrivals: Sequence[Sequence[Hashable]], b: int) -> int:
    """Maximum b-matching: copy each offline vertex b times, then Kuhn."""
    owner: dict = {}

    def augment(v: int, seen: set) -> bool:
        for u in arrivals[v]:
            for j in range(b):
                key = (u, j)
                if key in seen:
                    continue
                seen.add(key)
                if key not in owner or augment(owner[key], seen):
                    owner[key] = v
                    return True
        return False

    return sum(1 for v in range(len(arrivals)) if augment(v, set()))


def adwords_opt(budgets, bids) -> float:
    """Best offline revenue by trying every assignment (small inputs)."""
    choices = [[None] + list(q) for q in bids]
    best = 0.0
    for pick in itertools.product(*choices):
        spent = dict.fromkeys(budgets, 0.0)
        for q, i in zip(bids, pick):
            if i is not None:
                spent[i] += q[i]
        best = max(best, sum(min(spent[i], budgets[i]) for i in budgets))
    return best


def block_adversary(n: int, b: int) -> tuple[int, int]:
    """Rounds of b arrivals on a shrinking set; the adversary drops the least loaded vertex."""
    alg = Balance(range(n), b)
    alive = list(range(n))
    for _ in range(n):
        for _ in range(b):
            alg.arrive(list(alive))
        w = min(alive, key=lambda x: (alg.load[x], x))
        alive.remove(w)
    return size(alg.match), n * b


def test_ratio_values() -> None:
    assert balance_ratio(1) == 0.5
    assert abs(balance_ratio(2) - 5 / 9) < 1e-12
    assert abs(balance_ratio(3) - 37 / 64) < 1e-12


def test_example_from_page() -> None:
    arr = [["u1", "u2", "u3"]] * 2 + [["u1", "u2"]] * 2 + [["u2"]] * 2
    alg = balance(["u1", "u2", "u3"], 2, arr)
    assert alg.match == ["u1", "u2", "u1", "u2", None, None]
    assert max_b_matching(arr, 2) == 6
    assert all(abs(a - w) < 1e-12 for a, w in zip(alg.beta, [1, 1, 0.6, 0.6, 0, 0]))
    alpha = alg.alpha()
    assert abs(2 * sum(alpha.values()) + sum(alg.beta) - 7.2) < 1e-9


def test_ratio_and_dual_on_random_instances() -> None:
    rng = random.Random(5)
    for _ in range(1200):
        k = rng.randint(1, 4)
        b = rng.randint(1, 3)
        n = rng.randint(1, 9)
        arr = [[u for u in range(k) if rng.random() < 0.5] for _ in range(n)]
        alg = balance(range(k), b, arr)
        m = size(alg.match)
        assert all(alg.load[u] <= b for u in alg.load)
        opt = max_b_matching(arr, b)
        c = balance_ratio(b)
        assert m >= c * opt - 1e-9
        alpha = alg.alpha()
        dual = b * sum(alpha.values()) + sum(alg.beta)
        assert abs(dual - m / c) < 1e-9
        for t, nb in enumerate(arr):
            for u in nb:
                assert alpha[u] + alg.beta[t] >= 1 - 1e-9


def test_block_adversary_is_nearly_tight() -> None:
    for b in (1, 2, 3, 5):
        got, opt = block_adversary(200, b)
        c = balance_ratio(b)
        assert got >= c * opt
        assert got / opt - c < 0.005


def test_msvv_is_balance_for_unit_bids() -> None:
    rng = random.Random(8)
    for _ in range(300):
        k = rng.randint(1, 4)
        b = rng.randint(1, 3)
        arr = [[u for u in range(k) if rng.random() < 0.6] for _ in range(rng.randint(1, 9))]
        bids = [{u: 1.0 for u in nb} for nb in arr]
        assign, rev = msvv({u: float(b) for u in range(k)}, bids)
        alg = balance(range(k), b, arr)
        assert assign == alg.match
        assert rev == size(alg.match)


def test_bjn_bound_and_dual() -> None:
    rng = random.Random(9)
    for _ in range(300):
        adv = list(range(rng.randint(1, 3)))
        budgets = {i: float(rng.randint(4, 10)) for i in adv}
        bids = []
        for _ in range(rng.randint(1, 6)):
            q = {i: float(rng.randint(1, 3)) for i in adv if rng.random() < 0.7}
            bids.append(q)
        assign, rev, x, z, c = bjn_adwords(budgets, bids)
        R = max((q[i] / budgets[i] for q in bids for i in q), default=1.0)
        opt = adwords_opt(budgets, bids)
        dual = sum(budgets[i] * x[i] for i in adv) + sum(z)
        for t, q in enumerate(bids):
            for i, bid in q.items():
                assert bid * x[i] + z[t] >= bid - 1e-9
        assert dual >= opt - 1e-9
        assert rev >= (1 - 1 / c) * (1 - R) * opt - 1e-9
        fake = sum(q[i] for q, i in zip(bids, assign) if i is not None)
        assert abs(dual - c / (c - 1) * fake) < 1e-9
        m_rev = msvv(budgets, bids)[1]
        assert m_rev <= opt + 1e-9


if __name__ == "__main__":
    for name, f in list(globals().items()):
        if name.startswith("test_"):
            f()
    print("ok")
