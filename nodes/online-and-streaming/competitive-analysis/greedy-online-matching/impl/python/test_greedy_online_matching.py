# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-online-matching/. The authors are listed in prov/39VNTT.jsonl.

import random
from collections.abc import Hashable, Sequence

from greedy_online_matching import (
    GreedyOnlineMatching,
    adversary_half,
    first,
    greedy_online_matching,
    matching_size,
)


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


def check_valid(offline, arrivals, match) -> None:
    used = [u for u in match if u is not None]
    assert len(used) == len(set(used))
    for t, u in enumerate(match):
        if u is not None:
            assert u in arrivals[t] and u in offline
        else:
            # greedy: no free neighbour at time t
            taken = {x for x in match[:t] if x is not None}
            assert all(x in taken for x in arrivals[t])


def random_instance(rng: random.Random):
    k = rng.randint(1, 7)
    n = rng.randint(1, 7)
    p = rng.choice([0.2, 0.4, 0.7])
    arrivals = [[u for u in range(k) if rng.random() < p] for _ in range(n)]
    return list(range(k)), arrivals


def test_example_from_page() -> None:
    arrivals = [["a", "b"], ["a"], ["b", "c"], ["c", "d"]]
    match = greedy_online_matching("abcd", arrivals)
    assert match == ["a", None, "b", "c"]
    assert matching_size(match) == 3
    assert max_matching(arrivals) == 4


def test_half_on_random_instances() -> None:
    rng = random.Random(1)
    rules = [first, lambda c: c[-1], lambda c: max(c)]
    for _ in range(1500):
        offline, arrivals = random_instance(rng)
        opt = max_matching(arrivals)
        for rule in rules:
            match = greedy_online_matching(offline, arrivals, rule)
            check_valid(offline, arrivals, match)
            assert 2 * matching_size(match) >= opt


def test_half_with_random_choices() -> None:
    rng = random.Random(2)
    for _ in range(800):
        offline, arrivals = random_instance(rng)
        opt = max_matching(arrivals)
        match = greedy_online_matching(offline, arrivals, rng.choice)
        check_valid(offline, arrivals, match)
        assert 2 * matching_size(match) >= opt


def test_adversary_forces_half() -> None:
    for rule in [first, lambda c: c[-1], lambda c: min(c)]:
        for k in range(1, 8):
            arrivals, match = adversary_half(rule, k)
            assert max_matching(arrivals) == 2 * k
            assert matching_size(match) == k


def test_upper_triangular_example() -> None:
    arrivals = [["u1", "u2", "u3"], ["u1", "u2"], ["u1"]]
    match = greedy_online_matching(["u1", "u2", "u3"], arrivals)
    assert match == ["u1", "u2", None]
    assert max_matching(arrivals) == 3


def test_bad_choose_is_rejected() -> None:
    g = GreedyOnlineMatching([0, 1], choose=lambda c: 5)
    try:
        g.arrive([0])
    except ValueError:
        return
    raise AssertionError("expected ValueError")


if __name__ == "__main__":
    for name, f in list(globals().items()):
        if name.startswith("test_"):
            f()
    print("ok")
