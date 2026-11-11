# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scamp/. The authors are listed in prov/7YXJZ9.jsonl.

import math
import random
import statistics

from scamp import Scamp, harmonic, predicted_mean_view


def check_views(s: Scamp) -> None:
    for v in s.alive:
        assert v not in s.view[v]
        for w in s.view[v]:
            assert v in s.inview[w]


def test_one_join_adds_d_plus_c_plus_one_arcs():
    s = Scamp(2, 1)
    s.grow(60)
    for _ in range(50):
        m = sum(len(s.view[k]) for k in s.alive)
        contact = s.rng.choice(sorted(s.alive))
        d = len(s.view[contact])
        drops = s.dropped
        s.join(contact)
        assert sum(len(s.view[k]) for k in s.alive) - m == 1 + d + 2 - (s.dropped - drops)
    check_views(s)


def test_mean_view_is_c_plus_one_times_log_n():
    for c in (1, 2):
        got, want = [], []
        for seed in range(4):
            s = Scamp(c, seed)
            s.grow(50)
            a0 = s.mean_view()
            s.grow(600)
            got.append(s.mean_view())
            want.append(predicted_mean_view(600, c, 50, a0))
        assert abs(statistics.mean(got) / statistics.mean(want) - 1) < 0.05
        # the growth from 50 to 600 nodes is (c + 1) ln(600 / 50) up to O(1/n)
        assert abs((c + 1) * (harmonic(600) - harmonic(50)) - (c + 1) * math.log(12)) < 0.05 * (c + 1)


def test_flooding_reaches_everyone():
    s = Scamp(1, 3)
    s.grow(500)
    check_views(s)
    for src in (0, 100, 499):
        assert s.reach(src) == 500


def test_unsubscription_keeps_the_log_law_and_connectivity():
    s = Scamp(1, 4)
    s.grow(800)
    before = s.mean_view()
    rng = random.Random(9)
    for k in rng.sample(range(800), 240):
        s.unsubscribe(k)
    check_views(s)
    assert s.dead_arcs() == 0
    expect = before - 2 * (harmonic(800) - harmonic(560))
    assert abs(s.mean_view() / expect - 1) < 0.1
    live = sorted(s.alive)
    assert s.reach(live[0]) == len(live)


def test_lease_removes_crashed_nodes():
    s = Scamp(1, 5)
    s.grow(600)
    rng = random.Random(2)
    for k in rng.sample(range(600), 180):
        s.crash(k)
    assert s.dead_arcs() > 0
    for t in range(10):
        s.lease_round(10, t)
    assert s.dead_arcs() == 0
    check_views(s)
    live = sorted(s.alive)
    assert s.reach(live[0]) == len(live)


def test_indirection_spreads_the_contact():
    s = Scamp(1, 6, indirection=5)
    s.grow(300)
    assert s.reach(0) == 300
    assert s.mean_view() > 0.8 * predicted_mean_view(300, 1)
