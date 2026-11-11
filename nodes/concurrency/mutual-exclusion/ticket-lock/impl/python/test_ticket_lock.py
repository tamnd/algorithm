# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ticket-lock/. The authors are listed in prov/B01V2J.jsonl.

from interleave import explore, max_passage_rmr, no_progress, run, starvation
from ticket_lock import INIT, client


def test_mutual_exclusion_and_fifo_two_processes() -> None:
    g = explore([client(0, rounds=2)] * 2, INIT, cache=True)
    assert g.violation is None and not g.stuck
    assert [max_passage_rmr(g, p, "cc") for p in range(2)] == [4, 4]


def test_mutual_exclusion_and_fifo_three_processes() -> None:
    g = explore([client(0, rounds=1)] * 3, INIT, cache=True)
    assert g.violation is None and not g.stuck
    assert [max_passage_rmr(g, p, "cc") for p in range(3)] == [5, 5, 5]


def test_dsm_waiting_is_remote_and_unbounded() -> None:
    home = {"next": 0, "serving": 0}
    g = explore([client(0, rounds=1)] * 2, INIT, home=home)
    assert max_passage_rmr(g, 1, "dsm") == float("inf")


def test_proportional_backoff_keeps_safety() -> None:
    g = explore([client(1, rounds=1)] * 3, INIT)
    assert g.violation is None and not g.stuck


def test_starvation_free_with_wrapping_counters() -> None:
    g = explore([client(0, rounds=None, wrap=3)] * 2, INIT)
    assert g.violation is None
    assert no_progress(g) == []
    assert starvation(g, 0) == [] and starvation(g, 1) == []


def test_wrapping_too_soon_breaks_mutual_exclusion() -> None:
    g = explore([client(0, rounds=None, wrap=2)] * 3, INIT, stop=True)
    assert g.violation is not None
    # tickets 0, 1, 0: the third process enters while the first is inside
    order = [0, 0, 0, 1, 1, 2, 2, 2]
    m = run([client(0, rounds=1, wrap=2)] * 3, INIT, policy=lambda t, e, r: order[t] if t < len(order) else None)
    assert m.violations and m.violations[0][0] == "mutual exclusion"


def take_tickets_then_round_robin(n):
    # each process runs its 'try' step and its fetch-and-add first, then all run in turn
    def policy(t, enabled, rng):
        if t < 2 * n:
            return t // 2
        return enabled[t % len(enabled)]
    return policy


def test_last_in_line_pays_n_plus_two() -> None:
    for n in range(2, 9):
        m = run([client(0, rounds=1)] * n, INIT, policy=take_tickets_then_round_robin(n))
        assert m.entries == list(range(n))
        assert [cc for cc, _ in m.passages[n - 1]] == [n + 2]
        assert all(cc <= n + 2 for p in range(n) for cc, _ in m.passages[p])


def test_random_runs_fifo_and_bound() -> None:
    for seed in range(60):
        n = 2 + seed % 7
        m = run([client(seed % 2, rounds=3)] * n, INIT, seed=seed)
        assert m.violations == []
        assert len(m.entries) == 3 * n
        assert all(cc <= n + 2 for p in range(n) for cc, _ in m.passages[p])
