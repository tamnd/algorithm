# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lai-yang-snapshot/. The authors are listed in prov/HRAZCB.jsonl.

import random

from lai_yang_snapshot import Bank, uniform_delay


def test_non_fifo_snapshots_are_consistent_and_conserve_money() -> None:
    overtakes = 0
    for seed in range(60):
        rng = random.Random(seed)
        n = rng.randrange(2, 6)
        balances = [rng.randrange(0, 200) for _ in range(n)]
        bank = Bank(balances, delay=uniform_delay(0.1, 6.0), seed=seed)
        bank.run(initiator=rng.randrange(n), t_init=rng.uniform(0, 10), ticks=8, horizon=12.0)
        assert all(pr.red for pr in bank.p)
        assert bank.is_consistent()
        assert {ch: set(m) for ch, m in bank.channel_states().items()} == bank.in_transit()
        assert bank.recorded_total() == sum(balances)
        assert sum(pr.balance for pr in bank.p) == sum(balances)
        overtakes += bool(bank.channel_states())
    assert overtakes > 0  # some runs record money in a channel


def test_page_example() -> None:
    def delay(src, dst, msg, rng):
        return 4.0 if msg[2] else 1.0

    bank = Bank([100, 50], delay=delay, seed=0)
    bank.run(initiator=0, t_init=2.0, script=[(1.0, 1, 0, 30)])
    assert [pr.saved for pr in bank.p] == [100, 20]
    assert bank.channel_states() == {(1, 0): {0: 30}}
    assert bank.recorded_total() == 150


def test_red_message_overtaking_is_harmless() -> None:
    # The run that breaks Chandy and Lamport: the 10 overtakes the slow message
    # that tells p1 to record. It is red, so p1 records before it takes the 10.
    def delay(src, dst, msg, rng):
        return 1.0 if msg[2] else 5.0

    bank = Bank([100, 100], delay=delay, seed=0)
    bank.run(initiator=0, t_init=0.0, script=[(0.5, 0, 1, 10)])
    assert [pr.saved for pr in bank.p] == [100, 100]
    assert bank.is_consistent() and bank.recorded_total() == 200
