# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/failover/. The authors are listed in prov/D00TZM.jsonl.

import random
from fractions import Fraction

from failover import (LeaseService, Storage, leases_disjoint, random_cluster, run_failover,
                      takeover_time_formula, tokens_monotone, vrrp_master_down_interval)


def test_lease_service_one_holder():
    s = LeaseService(10)
    assert s.acquire(0, 0) == (1, 10)
    assert s.acquire(1, 5) is None
    assert s.acquire(0, 6) == (1, 16)  # renewal keeps the token
    assert s.acquire(1, 15) is None
    assert s.acquire(1, 16) == (2, 26)  # expired: new holder, new token
    assert s.acquire(0, 17) is None
    assert leases_disjoint(s)


def test_storage_fencing():
    st = Storage()
    assert st.write(0, 33, 0)
    assert st.write(1, 34, 1)
    assert not st.write(0, 33, 2)
    assert st.write(1, 34, 3)


def test_worked_example_crash():
    r = run_failover(lease=10, renew=3, poll=2, promote=2, fail_time=7)
    assert (r.last_old_write, r.acquire_time, r.first_new_write) == (6, 16, 18)
    assert [g[:3] for g in r.service.grants] == [(0, 0, 1), (16, 1, 2)]


def test_takeover_time_formula_and_bounds():
    for lease in (5, 10, 13):
        for renew in (1, 2, 4):
            for poll in (1, 2, 3):
                for promote in (1, 3):
                    gaps = []
                    for c in range(1, 40):
                        r = run_failover(lease, renew, poll, promote, fail_time=c)
                        assert r.acquire_time == takeover_time_formula(lease, renew, poll, c)
                        assert r.first_new_write == r.acquire_time + promote
                        assert r.last_old_write == c - 1
                        gaps.append(r.first_new_write - c)
                    assert min(gaps) >= lease - renew + promote
                    assert max(gaps) <= lease + poll - 2 + promote


def test_paused_primary_is_fenced():
    r = run_failover(lease=10, renew=3, poll=2, promote=2, fail_time=7, pause=20)
    assert r.acquire_time == 16
    assert r.stale_rejected
    assert r.storage.rejected == [(27, 0, 1)]
    assert tokens_monotone(r.storage)
    # After the new primary's first write, no write of the old primary is accepted.
    assert all(a[1] == 1 for a in r.storage.accepted if a[0] >= r.first_new_write)


def test_paused_primary_without_fencing_overwrites():
    r = run_failover(lease=10, renew=3, poll=2, promote=2, fail_time=7, pause=20, fencing=False)
    assert (27, 0, 1) in r.storage.accepted
    assert not tokens_monotone(r.storage)


def test_short_pause_needs_no_failover():
    r = run_failover(lease=10, renew=3, poll=2, promote=2, fail_time=7, pause=2, horizon=60)
    assert r.acquire_time is None
    assert r.storage.rejected == []


def test_random_clusters():
    bad_plain = 0
    for seed in range(300):
        st, svc = random_cluster(random.Random(seed), fencing=True)
        assert tokens_monotone(st)
        assert leases_disjoint(svc)
        st2, _ = random_cluster(random.Random(seed), fencing=False)
        bad_plain += not tokens_monotone(st2)
    assert bad_plain == 267


def test_vrrp_master_down_interval():
    assert vrrp_master_down_interval(100, 100) == Fraction(5775, 16)  # 360.9375 cs
    assert vrrp_master_down_interval(100, 254) == Fraction(9625, 32)  # 300.78125 cs
    # A higher priority backup declares the master down sooner.
    assert vrrp_master_down_interval(100, 200) < vrrp_master_down_interval(100, 100)
