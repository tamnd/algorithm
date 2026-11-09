# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karp-miller-tree/. The authors are listed in prov/V1GHKA.jsonl.

import random
from collections import deque

from karp_miller_tree import OMEGA, coverable, karp_miller_tree, unbounded_places

# The worked example: places (p, q, r).
EXAMPLE = [
    ((1, 0, 0), (1, 1, 0)),  # t1: p stays, one token more in q
    ((1, 0, 0), (0, 0, 1)),  # t2: move the token from p to r
    ((0, 1, 1), (1, 0, 0)),  # t3: r and one token of q give p
]


def fire_all(net, m):
    for pre, post in net:
        if all(a <= b for a, b in zip(pre, m)):
            yield tuple(b - a + c for a, b, c in zip(pre, m, post))


def reachable_bfs(net, m0, cap):
    """All reachable markings, or None if there are more than cap of them."""
    seen, queue = {tuple(m0)}, deque([tuple(m0)])
    while queue:
        m = queue.popleft()
        for m2 in fire_all(net, m):
            if m2 not in seen:
                seen.add(m2)
                if len(seen) > cap:
                    return None
                queue.append(m2)
    return seen


def backward_coverable(net, m0, target) -> bool:
    """The backward algorithm: a finite basis of the markings that can cover target."""
    basis = [tuple(target)]
    frontier = list(basis)
    while frontier:
        new = []
        for b in frontier:
            for pre, post in net:
                m = tuple(pr + max(0, bb - po) for pr, bb, po in zip(pre, b, post))
                if not any(all(x <= y for x, y in zip(c, m)) for c in basis):
                    basis = [c for c in basis if not all(x <= y for x, y in zip(m, c))]
                    basis.append(m)
                    new.append(m)
        frontier = [m for m in new if m in basis]
    return any(all(x <= y for x, y in zip(c, m0)) for c in basis)


def random_net(rng, places, transitions, conserving):
    net = []
    for _ in range(transitions):
        pre = [rng.randint(0, 1) for _ in range(places)]
        if sum(pre) == 0:
            pre[rng.randrange(places)] = 1
        if conserving:
            post = [0] * places
            for _ in range(sum(pre)):
                post[rng.randrange(places)] += 1
        else:
            post = [rng.randint(0, 2) for _ in range(places)]
        net.append((tuple(pre), tuple(post)))
    return net


def test_example() -> None:
    labels = {lab for lab, _, _ in karp_miller_tree(EXAMPLE, (1, 0, 0))}
    assert labels == {(1, 0, 0), (1, OMEGA, 0), (0, 0, 1), (0, OMEGA, 1)}
    assert len(karp_miller_tree(EXAMPLE, (1, 0, 0))) == 6
    assert coverable(EXAMPLE, (1, 0, 0), (0, 5, 1))
    assert not coverable(EXAMPLE, (1, 0, 0), (1, 0, 1))
    assert unbounded_places(EXAMPLE, (1, 0, 0)) == {1}


def test_edges() -> None:
    assert karp_miller_tree([], (2, 0)) == [((2, 0), -1, -1)]
    assert coverable([], (2, 0), (1, 0)) and not coverable([], (2, 0), (0, 1))
    # a transition with an empty preset: every place it feeds is unbounded
    net = [((0, 0), (0, 1))]
    assert unbounded_places(net, (0, 0)) == {1}
    assert coverable(net, (0, 0), (0, 1000))
    # a dead net
    assert unbounded_places([((1, 0), (0, 1))], (0, 0)) == set()


def test_bounded_nets_against_bfs() -> None:
    rng = random.Random(11)
    for _ in range(300):
        places = rng.randint(1, 4)
        net = random_net(rng, places, rng.randint(1, 4), conserving=True)
        m0 = tuple(rng.randint(0, 2) for _ in range(places))
        reach = reachable_bfs(net, m0, 10_000)
        labels = {lab for lab, _, _ in karp_miller_tree(net, m0)}
        assert labels == reach
        for _ in range(5):
            target = tuple(rng.randint(0, 3) for _ in range(places))
            want = any(all(a <= b for a, b in zip(target, m)) for m in reach)
            assert coverable(net, m0, target) == want


def test_unbounded_nets_terminate_and_agree() -> None:
    rng = random.Random(12)
    for _ in range(300):
        places = rng.randint(1, 4)
        net = random_net(rng, places, rng.randint(1, 4), conserving=False)
        m0 = tuple(rng.randint(0, 2) for _ in range(places))
        tree = karp_miller_tree(net, m0)
        assert tree  # it terminates
        for _ in range(5):
            target = tuple(rng.randint(0, 4) for _ in range(places))
            assert coverable(net, m0, target) == backward_coverable(net, m0, target)
        if not unbounded_places(net, m0):
            reach = reachable_bfs(net, m0, 10_000)
            assert reach == {lab for lab, _, _ in tree}
        else:
            assert reachable_bfs(net, m0, 2_000) is None
