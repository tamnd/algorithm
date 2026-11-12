# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bgp/. The authors are listed in prov/BXJ1W1.jsonl.

import itertools
import random

from bgp import (CUSTOMER, EGP, IGP, INCOMPLETE, PEER, PROVIDER, ASNetwork,
                 Route, decide, random_hierarchy)


def test_loop_and_next_hop_excluded():
    a = Route((2, 7, 9))
    b = Route((3, 9), next_hop_ok=False)
    c = Route((4, 1, 9))
    assert decide([a, b, c], 7) is c
    assert decide([b], 7) is None
    assert decide([], 7) is None


def test_each_step_in_order():
    # local preference beats a shorter AS path
    a = Route((2, 5, 6, 9), local_pref=200)
    b = Route((3, 9), local_pref=100)
    assert decide([a, b], 1) is a
    # then the shorter AS path
    c = Route((3, 8, 9), local_pref=200)
    assert decide([a, c], 1) is c
    # then the lowest ORIGIN
    d = Route((4, 9), origin=EGP)
    e = Route((5, 9), origin=INCOMPLETE)
    f = Route((6, 9), origin=IGP)
    assert decide([d, e, f], 1) is f
    # then eBGP over iBGP, then interior cost, then BGP id, then address
    g = Route((4, 9), ebgp=False, igp_cost=0, bgp_id=1)
    h = Route((5, 9), ebgp=True, igp_cost=50, bgp_id=9)
    assert decide([g, h], 1) is h
    i = Route((6, 9), igp_cost=10, bgp_id=9)
    assert decide([h, i], 1) is i
    j = Route((7, 9), igp_cost=10, bgp_id=3)
    assert decide([i, j], 1) is j
    k = Route((7, 9), igp_cost=10, bgp_id=3, peer_addr=1)
    m = Route((7, 9), igp_cost=10, bgp_id=3, peer_addr=0)
    assert decide([k, m], 1) is m


def test_med_only_within_one_neighbour_as():
    # two routes from AS 2 and one from AS 3; MED compares only within AS 2
    a = Route((2, 9), med=10, igp_cost=5, bgp_id=1)
    b = Route((2, 9), med=20, igp_cost=1, bgp_id=2)
    c = Route((3, 9), med=0, igp_cost=3, bgp_id=3)
    # b loses to a on MED; then a (cost 5) loses to c (cost 3)
    assert decide([a, b, c], 1) is c
    # without c, a wins although b has the lower interior cost
    assert decide([a, b], 1) is a
    # the result does not depend on the order of the candidates
    for perm in itertools.permutations([a, b, c]):
        assert decide(list(perm), 1) is c
    # a missing MED counts as the lowest value
    d = Route((2, 9), med=None, igp_cost=9, bgp_id=4)
    assert decide([a, d], 1) is d


def relation(rel, a, b):
    return rel[a][b]


def valley_free(rel, path):
    """up* (peer)? down*, read from the source toward the origin."""
    phase = 0                     # 0: going up, 1: after the peer link, 2: going down
    for a, b in zip(path, path[1:]):
        r = rel[a][b]             # what b is to a
        if r == PROVIDER:
            if phase > 0:
                return False
        elif r == PEER:
            if phase > 0:
                return False
            phase = 1
        else:
            phase = 2
    return True


def check_stable(net):
    rel = net.rel
    for a in rel:
        if a == net.o:
            continue
        cands = []
        for b in rel[a]:
            p = net.exports(b, a)
            if p is not None:
                cands.append(Route(p, local_pref={CUSTOMER: 300, PEER: 200,
                                                  PROVIDER: 100}[rel[a][b]],
                                   neighbor_as=b, bgp_id=b, peer_addr=b))
        want = decide(cands, a)
        got = net.best[a]
        assert (want is None) == (got is None)
        if want is not None:
            assert want.as_path == got.as_path


def test_gao_rexford_converges_valley_free():
    for seed in range(12):
        rng = random.Random(seed)
        rel = random_hierarchy(rng, rng.randint(4, 25))
        for origin in rng.sample(sorted(rel), 3):
            net = ASNetwork(rel, origin, rng=random.Random(seed * 7 + origin))
            assert net.run()
            check_stable(net)
            for a in rel:
                p = net.path(a)
                # the tier-1 mesh and the provider chains give full reach
                assert p is not None and p[-1] == origin
                assert len(set(p)) == len(p)
                assert all(b in rel[x] for x, b in zip(p, p[1:]))
                assert valley_free(rel, p)
                # forwarding is consistent: the next AS uses the suffix
                if len(p) > 1:
                    assert net.path(p[1]) == p[1:]


def test_customer_routes_win():
    for seed in range(8):
        rng = random.Random(100 + seed)
        rel = random_hierarchy(rng, 20)
        origin = rng.randrange(20)
        net = ASNetwork(rel, origin, rng=random.Random(seed))
        net.run()
        # an AS that is a provider-chain ancestor of the origin uses a
        # customer route
        up = {origin}
        changed = True
        while changed:
            changed = False
            for a in rel:
                if a not in up and any(rel[a][c] == CUSTOMER and c in up for c in rel[a]):
                    up.add(a)
                    changed = True
        for a in up - {origin}:
            assert rel[a][net.path(a)[1]] == CUSTOMER
        for a in set(rel) - up:
            assert rel[a][net.path(a)[1]] != CUSTOMER


def test_same_result_for_any_timing():
    rng = random.Random(42)
    rel = random_hierarchy(rng, 18)
    results = set()
    for seed in range(10):
        net = ASNetwork(rel, 17, rng=random.Random(seed))
        net.run()
        results.add(tuple(net.path(a) for a in sorted(rel)))
    assert len(results) == 1
