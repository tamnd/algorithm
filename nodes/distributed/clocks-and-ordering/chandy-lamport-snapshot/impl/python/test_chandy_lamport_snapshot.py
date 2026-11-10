# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chandy-lamport-snapshot/. The authors are listed in prov/32HBY1.jsonl.

import random

from chandy_lamport_snapshot import Bank, uniform_delay


def test_fifo_snapshots_are_consistent_and_conserve_money() -> None:
    for seed in range(60):
        rng = random.Random(seed)
        n = rng.randrange(2, 6)
        balances = [rng.randrange(0, 200) for _ in range(n)]
        bank = Bank(balances, fifo=True, delay=uniform_delay(0.1, 3.0), seed=seed)
        bank.run(initiator=rng.randrange(n), t_init=rng.uniform(0, 10), ticks=8, horizon=12.0)
        assert all(pr.recorded for pr in bank.p)
        assert bank.is_consistent()
        assert bank.recorded_channels() == bank.in_transit()
        assert bank.recorded_total() == sum(balances)
        assert bank.markers == n * (n - 1)  # one marker per channel
        assert sum(pr.balance for pr in bank.p) == sum(balances)


def test_page_example() -> None:
    # p0 starts the snapshot at time 2. p1 sent 30 to p0 at time 1; it is
    # still in the channel when p0 records, so the channel state holds it.
    def delay(src, dst, msg, rng):
        return 4.0 if msg[0] == "app" else 1.0

    bank = Bank([100, 50], fifo=True, delay=delay, seed=0)
    bank.run(initiator=0, t_init=2.0, script=[(1.0, 1, 0, 30)])
    assert [pr.saved for pr in bank.p] == [100, 20]
    assert bank.recorded_channels() == {(1, 0): {0}}
    assert bank.recorded_total() == 150


def test_non_fifo_breaks_chandy_lamport() -> None:
    # p0 records, sends the marker, then sends 10. The 10 overtakes the marker.
    def delay(src, dst, msg, rng):
        return 5.0 if msg[0] == "marker" else 1.0

    bank = Bank([100, 100], fifo=False, delay=delay, seed=0)
    bank.run(initiator=0, t_init=0.0, script=[(0.5, 0, 1, 10)])
    assert [pr.saved for pr in bank.p] == [100, 110]
    assert not bank.is_consistent()
    assert bank.recorded_total() == 210  # 10 counted twice
    # The same run on a FIFO channel keeps the 10 behind the marker.
    good = Bank([100, 100], fifo=True, delay=delay, seed=0)
    good.run(initiator=0, t_init=0.0, script=[(0.5, 0, 1, 10)])
    assert good.is_consistent() and good.recorded_total() == 200
