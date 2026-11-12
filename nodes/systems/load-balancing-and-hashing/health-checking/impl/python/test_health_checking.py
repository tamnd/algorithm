# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/health-checking/. The authors are listed in prov/K5FA12.jsonl.

import itertools
import random

from health_checking import (OutlierDetector, RiseFallChecker, detection_delay,
                             detection_delay_formula, routable, state_by_runs)


def run(results, rise, fall, healthy=False):
    c = RiseFallChecker(rise, fall, healthy)
    for r in results:
        c.observe(r)
    return c


def test_state_machine_matches_run_reference_exhaustively():
    for n in range(0, 11):
        for bits in itertools.product([False, True], repeat=n):
            for rise in (1, 2, 3):
                for fall in (1, 2, 3):
                    for start in (False, True):
                        got = run(bits, rise, fall, start).healthy
                        assert got == state_by_runs(list(bits), rise, fall, start)


def test_haproxy_defaults_trace():
    # rise 2, fall 3, starting healthy.
    c = RiseFallChecker(rise=2, fall=3, healthy=True)
    seq = [True, False, False, True, False, False, False, True, False, True, True]
    states = [c.observe(r) for r in seq]
    assert states == [True, True, True, True, True, True, False, False, False, False, True]
    assert c.transitions == 2


def test_flapping_is_suppressed():
    # Two failures then one success, repeated: never three failures in a row.
    seq = [False, False, True] * 50
    assert run(seq, rise=2, fall=3, healthy=True).transitions == 0
    # With no hysteresis the same backend changes state on almost every probe.
    assert run(seq, rise=1, fall=1, healthy=True).transitions == 100


def test_flapping_random_backend():
    rng = random.Random(7)
    seq = [rng.random() >= 0.3 for _ in range(10_000)]
    plain = run(seq, 1, 1, True).transitions
    hyst = run(seq, 2, 3, True).transitions
    assert plain > 4000
    assert hyst < plain // 5


def test_detection_delay_exact():
    for interval in (1, 2, 5, 10):
        for timeout in (0, 1, 3):
            for fall in (1, 2, 3, 5):
                delays = []
                for t in range(1, 4 * interval + 1):
                    d = detection_delay(t, interval, timeout, fall)
                    assert d == detection_delay_formula(t, interval, timeout, fall)
                    delays.append(d)
                assert min(delays) == (fall - 1) * interval + timeout
                assert max(delays) == fall * interval + timeout - 1


def test_haproxy_default_numbers():
    # inter 2000 ms, fall 3, timeout 0: between 4000 and 5999 ms.
    ds = [detection_delay(t, 2000, 0, 3) for t in range(1, 2001)]
    assert (min(ds), max(ds)) == (4000, 5999)


def test_outlier_ejection_after_five_consecutive():
    od = OutlierDetector(10)
    for _ in range(4):
        od.on_response(0, 503, now=0)
    od.on_response(0, 200, now=0)
    for _ in range(4):
        od.on_response(0, 503, now=1)
    assert not od.ejected(0)
    od.on_response(0, 500, now=1)
    assert od.ejected(0)
    assert od.log == [(1, 0, 30)]


def test_ejection_time_grows_and_is_capped():
    od = OutlierDetector(10, base_ejection_time=30, max_ejection_time=100)
    now, times = 0, []
    for _ in range(5):
        for _ in range(5):
            od.on_response(3, 503, now)
        times.append(od.log[-1][2])
        now += od.log[-1][2]
        od.sweep(now)
        assert not od.ejected(3)
    assert times == [30, 60, 90, 100, 100]


def test_multiplier_decays_while_healthy():
    od = OutlierDetector(10)
    for _ in range(5):
        od.on_response(2, 503, 0)
    od.sweep(30)  # back in service, multiplier 1
    od.sweep(40)  # healthy sweep: multiplier 0
    for _ in range(5):
        od.on_response(2, 503, 41)
    assert od.log[-1] == (41, 2, 30)


def test_max_ejection_percent():
    od = OutlierDetector(20, max_ejection_percent=10)
    for h in range(5):
        for _ in range(5):
            od.on_response(h, 503, 0)
    assert od.ejected_count() == 2
    small = OutlierDetector(5, max_ejection_percent=10)
    for _ in range(5):
        small.on_response(0, 503, 0)
    assert small.ejected_count() == 0


def test_panic_threshold():
    assert routable([True, True, False, False]) == [0, 1]
    assert routable([True, False, False, False]) == [0, 1, 2, 3]
    assert routable([False] * 6) == list(range(6))
    assert routable([False] * 6, panic_percent=0) == []
