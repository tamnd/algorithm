# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/resource-allocation-graph/. The authors are listed in prov/SGGS8W.jsonl.
import random
from itertools import permutations

import pytest
from resource_allocation_graph import RAG, has_cycle


def random_rag(rng: random.Random, n: int, units: list[int]) -> RAG:
    g = RAG(n, units)
    for _ in range(3 * n):
        p, r = rng.randrange(n), rng.randrange(len(units))
        if any(g.req[p]) or g.held[p][r] + 1 > units[r]:
            continue  # p is blocked, or it cannot ask for more of r
        g.request(p, r)
        if rng.random() < 0.6:
            g.grant(p)  # take the unit now if it is free; else p stays blocked
    return g


def removable_by_some_order(g: RAG) -> set[int]:
    """Brute force: the largest set that some order of reductions removes."""
    best: set[int] = set()
    for order in permutations(range(g.n)):
        work, done = list(g.avail), set()
        for p in order:
            if all(g.req[p][r] <= work[r] for r in range(g.m)):
                done.add(p)
                work = [work[r] + g.held[p][r] for r in range(g.m)]
        if len(done) > len(best):
            best = done
    return best


def test_example_of_the_page():
    g = RAG(3, [1, 2])  # A has 1 unit, B has 2 units
    g.request(0, 0); assert g.grant(0)      # p holds A
    g.request(1, 1); assert g.grant(1)      # q holds one B
    g.request(2, 1); assert g.grant(2)      # s holds one B
    g.request(1, 0); assert not g.grant(1)  # q waits for A
    g.request(0, 1); assert not g.grant(0)  # p waits for a B
    assert g.wait_for_graph() == {0: {1, 2}, 1: {0}, 2: set()}
    assert has_cycle(g.wait_for_graph())
    assert g.reduce() == []  # s can finish, then p, then q: no deadlock
    g.request(2, 0)          # s now waits for A as well
    assert g.reduce() == [0, 1, 2]


def test_avail_invariant_under_random_operations():
    rng = random.Random(1)
    for _ in range(300):
        units = [rng.randint(1, 3) for _ in range(3)]
        g = random_rag(rng, 4, units)
        for r in range(3):
            assert g.avail[r] + sum(g.held[p][r] for p in range(4)) == units[r]
            assert all(g.held[p][r] + g.req[p][r] <= units[r] for p in range(4))


def test_reduction_matches_brute_force_over_all_orders():
    rng = random.Random(2)
    for _ in range(400):
        g = random_rag(rng, 4, [rng.randint(1, 3) for _ in range(3)])
        left = g.reduce()
        assert set(range(4)) - set(left) == removable_by_some_order(g)


def test_single_unit_cycle_iff_irreducible():
    rng = random.Random(3)
    seen = set()
    for _ in range(600):
        g = random_rag(rng, 4, [1, 1, 1, 1])
        dead = bool(g.reduce())
        assert dead == has_cycle(g.wait_for_graph())
        seen.add(dead)
    assert seen == {True, False}


def test_release_and_bad_calls():
    g = RAG(1, [2])
    g.request(0, 0, 2)
    assert g.grant(0) and g.avail == [0]
    g.release(0, 0)
    assert g.avail == [1]
    with pytest.raises(ValueError):
        g.release(0, 0, 2)
    with pytest.raises(ValueError):
        g.request(0, 0, 2)


def claims_safe_by_brute_force(g: RAG) -> bool:
    """Some order lets each process get all its claims, one process at a time."""
    for order in permutations(range(g.n)):
        work = list(g.avail)
        ok = True
        for p in order:
            if any(work[r] < 1 for r in g.claim[p] if g.held[p][r] == 0):
                ok = False
                break
            work = [work[r] + g.held[p][r] for r in range(g.m)]
        if ok:
            return True
    return False


def test_textbook_claim_example():
    g = RAG(2, [1, 1])
    for p in (0, 1):
        g.add_claim(p, 0)
        g.add_claim(p, 1)
    g.request(0, 0)
    assert g.safe_grant(0, 0)           # p1 gets R1
    g.request(1, 1)
    assert not g.safe_grant(1, 1)       # R2 to p2 would close p1 -> R2 -> p2 -> R1 -> p1
    assert g.req[1][1] == 1 and g.avail == [0, 1]


def test_safe_grant_keeps_every_state_safe():
    rng = random.Random(4)
    refused = 0
    for _ in range(300):
        n, m = 3, 3
        g = RAG(n, [1] * m)
        for p in range(n):
            for r in rng.sample(range(m), 2):
                g.add_claim(p, r)
        for _ in range(8):
            p = rng.randrange(n)
            free = [r for r in g.claim[p] if g.held[p][r] == 0 and g.req[p][r] == 0 and g.avail[r] == 1]
            if free:
                r = rng.choice(free)
                g.request(p, r)
                if not g.safe_grant(p, r):
                    refused += 1
                    assert not claims_safe_by_brute_force_after(g, p, r)
                    g.req[p][r] -= 1
            assert claims_safe_by_brute_force(g)
    assert refused > 0


def claims_safe_by_brute_force_after(g: RAG, p: int, r: int) -> bool:
    g.req[p][r] -= 1; g.held[p][r] += 1; g.avail[r] -= 1
    ok = claims_safe_by_brute_force(g)
    g.req[p][r] += 1; g.held[p][r] -= 1; g.avail[r] += 1
    return ok
