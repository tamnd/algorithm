# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/readers-writer-lock/. The authors are listed in prov/ZZ28W3.jsonl.

from interleave import explore, no_progress, starvation
from readers_writer_lock import POLICIES, WP_INIT, system, wp_read_acquire, wp_upgrade


def graph(policy, roles, rounds):
    procs, init = system(policy, roles, rounds)
    # readers may share the critical section, so the explorer allows all; the tests check writers
    return explore(procs, init, cs_limit=len(roles))


def check_exclusion(g, roles):
    shared = False
    for sec in g.section:
        inside = [p for p, s in enumerate(sec) if s == "cs"]
        if any(roles[p] == "w" for p in inside):
            assert len(inside) == 1
        shared |= len(inside) >= 2
    return shared


def test_writers_exclude_everyone_and_readers_share() -> None:
    for policy in POLICIES:
        for roles in ("rrw", "rww"):
            g = graph(policy, roles, 1)
            assert g.violation is None and not g.stuck
            check_exclusion(g, roles)
        assert check_exclusion(graph(policy, "rrw", 1), "rrw")


def test_reader_preference_starves_the_writer() -> None:
    g = graph("reader preference", "rrw", None)
    assert no_progress(g) == []
    comps = starvation(g, 2)
    assert comps
    # in the starving cycle the two readers take turns, and one of them is always inside
    for comp, inner in comps:
        assert {e[0] for _, e in inner if e[5]} <= {0, 1}
    # with a weak semaphore 'wrt', the first reader can also lose to a writer forever
    assert starvation(g, 0) != []


def test_writer_preference_starves_a_reader() -> None:
    g = graph("writer preference", "rww", None)
    assert no_progress(g) == []
    assert starvation(g, 0) != []


def test_fair_lock_starves_nobody() -> None:
    for roles in ("rrw", "rww"):
        g = graph("fair", roles, None)
        check_exclusion(g, roles)
        assert no_progress(g) == []
        assert all(starvation(g, p) == [] for p in range(3))


def test_two_readers_that_upgrade_deadlock() -> None:
    def upgrader(pid):
        yield ("mark", "try")
        yield from wp_read_acquire()
        yield from wp_upgrade()
        yield ("mark", "cs")
    g = explore([upgrader, upgrader], WP_INIT, cs_limit=2)
    assert g.stuck  # both hold a read lock and wait for the other to leave
    assert g.violation is None
