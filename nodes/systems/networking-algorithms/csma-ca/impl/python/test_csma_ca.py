# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/csma-ca/. The authors are listed in prov/HMFCEA.jsonl.

import random

from csma_ca import (
    bianchi_fixed_point,
    bianchi_tau,
    bianchi_throughput,
    dcf_network,
    saturated_dcf,
    sim_throughput,
)


def test_tau_formula_matches_the_closed_form_away_from_one_half():
    w, m = 32, 5
    for p in (0.0, 0.1, 0.3, 0.45, 0.55, 0.9):
        closed = 2 * (1 - 2 * p) / ((1 - 2 * p) * (w + 1) + p * w * (1 - (2 * p) ** m))
        assert abs(bianchi_tau(p, w, m) - closed) < 1e-12
    assert bianchi_tau(0, w, m) == 2 / (w + 1)


def test_fixed_point_solves_both_equations():
    for n in (2, 5, 10, 20, 50):
        tau, p = bianchi_fixed_point(n)
        assert abs(bianchi_tau(p, 32, 5) - tau) < 1e-12
        assert abs(1 - (1 - tau) ** (n - 1) - p) < 1e-9


def test_model_trends():
    ps = [bianchi_fixed_point(n)[1] for n in (2, 5, 10, 20, 50)]
    assert ps == sorted(ps)
    ss = [bianchi_throughput(n) for n in (2, 5, 10, 20, 50)]
    assert ss == sorted(ss, reverse=True)


def test_slot_level_simulation_agrees_with_bianchi():
    for n in (5, 10, 20):
        tau, p = bianchi_fixed_point(n)
        idle, succ, coll, sends, collided, wins = saturated_dcf(n, 150000, random.Random(n))
        steps = idle + succ + coll
        assert abs(sends / (n * steps) - tau) / tau < 0.03
        assert abs(collided / sends - p) / p < 0.03
        assert abs(sim_throughput(idle, succ, coll) - bianchi_throughput(n)) < 0.01
        assert min(wins) > 0.8 * max(wins)


HIDDEN = [{1}, {0, 2}, {1}]  # A - B - C: A and C do not hear each other
EXPOSED = [{1}, {0, 2}, {1, 3}, {2}]  # A - B - C - D: B sends to A, C sends to D
CLIQUE = [{1, 2, 3}, {0, 2, 3}, {0, 1, 3}, {0, 1, 2}]


def lost_fraction(stats):
    lost = sum(s["lost"] for s in stats.values())
    sent = lost + sum(s["delivered"] for s in stats.values())
    return lost / sent


def test_hidden_terminals_collide_and_rts_cts_helps():
    for seed in (3, 4):
        plain = dcf_network(HIDDEN, {0: 1, 2: 1}, 30000, random.Random(seed))
        guarded = dcf_network(HIDDEN, {0: 1, 2: 1}, 30000, random.Random(seed), rts=True)
        assert lost_fraction(plain) > 0.15
        assert lost_fraction(guarded) < 0.06
        assert all(s["dropped"] == 0 for s in guarded.values())


def test_rts_cts_in_a_clique_never_loses_data():
    plain = dcf_network(CLIQUE, {0: 3, 1: 3, 2: 3}, 30000, random.Random(5))
    guarded = dcf_network(CLIQUE, {0: 3, 1: 3, 2: 3}, 30000, random.Random(5), rts=True)
    assert lost_fraction(plain) > 0.05
    assert lost_fraction(guarded) == 0


def test_exposed_terminals_share_the_air_without_need():
    single = dcf_network([{1}, {0}], {0: 1}, 30000, random.Random(6))[0]["delivered"]
    stats = dcf_network(EXPOSED, {1: 0, 2: 3}, 30000, random.Random(6))
    assert lost_fraction(stats) == 0
    both = sum(s["delivered"] for s in stats.values())
    assert both < 1.5 * single  # two links that could run in parallel get far less than 2x


def test_every_acked_frame_was_delivered():
    for topo, flows in ((HIDDEN, {0: 1, 2: 1}), (CLIQUE, {0: 3, 1: 3, 2: 3})):
        for rts in (False, True):
            stats = dcf_network(topo, flows, 10000, random.Random(7), rts=rts)
            for s in stats.values():
                assert s["acked"] == s["delivered"]
