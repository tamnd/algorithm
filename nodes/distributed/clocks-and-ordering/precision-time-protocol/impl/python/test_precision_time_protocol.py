# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/precision-time-protocol/. The authors are listed in prov/QV4H8D.jsonl.

import random

from precision_time_protocol import AnnounceData, Path, best_master, boundary_chain, exchange, ptp_compute


def test_page_example() -> None:
    # Times in microseconds. The slave is 40 us ahead; 3 us one way, 5 us back.
    t1, t2, t3, t4 = 1000.0, 1043.0, 1100.0, 1065.0
    off, mpd = ptp_compute(t1, t2, t3, t4)
    assert off == 39.0 and mpd == 4.0
    assert abs(off - 40.0) == abs(3.0 - 5.0) / 2


def test_symmetric_path_is_exact() -> None:
    rng = random.Random(1)
    for _ in range(500):
        o = rng.uniform(-1e-3, 1e-3)
        d = rng.uniform(1e-7, 1e-5)
        r = exchange(o, Path([d], [d]), rng, use_tc=False, start=rng.uniform(0, 10))
        assert abs(r["offset"] - o) < 1e-12 and abs(r["mpd"] - d) < 1e-12


def test_asymmetric_error_and_bound() -> None:
    rng = random.Random(2)
    for _ in range(2000):
        o = rng.uniform(-1e-3, 1e-3)
        a, b = rng.uniform(0, 1e-5), rng.uniform(0, 1e-5)
        r = exchange(o, Path([a], [b]), rng, use_tc=False)
        assert abs((r["offset"] - o) - (a - b) / 2) < 1e-12
        assert abs(r["mpd"] - (a + b) / 2) < 1e-12
        assert abs(r["offset"] - o) <= r["mpd"] + 1e-12


def test_transparent_clocks_remove_queueing() -> None:
    rng = random.Random(3)
    worst_plain = worst_tc = 0.0
    for _ in range(500):
        o = rng.uniform(-1e-3, 1e-3)
        p = Path([2e-6, 3e-6, 1e-6], [2e-6, 3e-6, 1e-6], res_lo=0.0, res_hi=5e-5)
        plain = exchange(o, p, rng, use_tc=False)
        tc = exchange(o, p, rng, use_tc=True)
        assert abs(tc["offset"] - o) < 1e-12  # symmetric links: exact after correction
        assert abs(plain["offset"] - o - (plain["res"][0] - plain["res"][1]) / 2) < 1e-12
        worst_plain = max(worst_plain, abs(plain["offset"] - o))
        worst_tc = max(worst_tc, abs(tc["offset"] - o))
    assert worst_plain > 1e-5 and worst_tc < 1e-12


def test_boundary_chain_adds_hop_asymmetries() -> None:
    rng = random.Random(4)
    paths = [Path([1e-6], [1.4e-6]), Path([2e-6], [1e-6]), Path([1e-6], [1e-6])]
    err = boundary_chain([0.0, 5e-4, -3e-4, 7e-4], paths, rng)
    want = [0.0, -(1e-6 - 1.4e-6) / 2]
    want.append(want[1] - (2e-6 - 1e-6) / 2)
    want.append(want[2])
    assert all(abs(x - y) < 1e-15 for x, y in zip(err, want))


def test_bmca_order_of_fields() -> None:
    gps = AnnounceData(128, 6, 0x21, 0x4E5D, 128, "00:1b:19:ff:fe:00:00:01")
    free = AnnounceData(128, 248, 0xFE, 0xFFFF, 1, "00:1b:19:ff:fe:00:00:02")
    forced = AnnounceData(100, 248, 0xFE, 0xFFFF, 128, "00:1b:19:ff:fe:00:00:03")
    twin = AnnounceData(128, 6, 0x21, 0x4E5D, 128, "00:1b:19:ff:fe:00:00:00")
    assert best_master([free, gps]) == gps  # clockClass beats priority2
    assert best_master([free, gps, forced]) == forced  # priority1 comes first
    assert best_master([gps, twin]) == twin  # the identity breaks the last tie
