# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/security-automaton/. The authors are listed in prov/MN9D48.jsonl.

import itertools
import random

from security_automaton import accepts, no_send_after_read, run_monitor, table_delta


def violates_no_send_after_read(trace) -> int | None:
    """Index of the first send that comes after a read, read straight from the policy."""
    seen_read = False
    for i, e in enumerate(trace):
        if e == "send" and seen_read:
            return i
        if e == "read":
            seen_read = True
    return None


def test_page_example() -> None:
    q0, delta = no_send_after_read()
    assert run_monitor(q0, delta, ["other", "send", "read", "other", "send", "send"]) == 4
    assert run_monitor(q0, delta, ["send", "send", "other"]) is None
    assert run_monitor(q0, delta, ["read", "read"]) is None


def test_edges() -> None:
    q0, delta = no_send_after_read()
    assert run_monitor(q0, delta, []) is None
    # No initial state: the empty trace is allowed, the first event is stopped.
    assert run_monitor(set(), delta, []) is None
    assert run_monitor(set(), delta, ["other"]) == 0
    # An unknown event has no move.
    assert run_monitor(q0, delta, ["exec"]) == 0


def test_against_policy_predicate() -> None:
    q0, delta = no_send_after_read()
    for k in range(8):
        for trace in itertools.product(["read", "send", "other"], repeat=k):
            assert run_monitor(q0, delta, trace) == violates_no_send_after_read(trace)


def path_exists(initial, table, trace) -> bool:
    """Oracle: is there a sequence of states that follows the transitions along the trace?"""
    states = sorted({q for (q, _) in table} | {r for v in table.values() for r in v} | set(initial))
    for path in itertools.product(states, repeat=len(trace) + 1):
        if path[0] not in initial:
            continue
        if all(path[i + 1] in table.get((path[i], trace[i]), ()) for i in range(len(trace))):
            return True
    return False


def test_nondeterministic_against_paths() -> None:
    rng = random.Random(2000)
    alphabet = ["a", "b", "c"]
    for _ in range(500):
        n = rng.randint(1, 3)
        states = list(range(n))
        table = {}
        for q in states:
            for s in alphabet:
                nxt = {r for r in states if rng.random() < 0.4}
                if nxt:
                    table[(q, s)] = nxt
        initial = {q for q in states if rng.random() < 0.6} or {0}
        delta = table_delta(table)
        trace = [rng.choice(alphabet) for _ in range(rng.randint(0, 5))]
        stop = run_monitor(initial, delta, trace)
        # The monitor allows exactly the prefixes that have a path.
        for k in range(len(trace) + 1):
            allowed = stop is None or k <= stop
            assert path_exists(initial, table, trace[:k]) == allowed
        assert accepts(initial, delta, trace) == path_exists(initial, table, trace)


def test_allowed_set_is_prefix_closed() -> None:
    rng = random.Random(7)
    q0, delta = no_send_after_read()
    for _ in range(500):
        trace = [rng.choice(["read", "send", "other"]) for _ in range(rng.randint(0, 9))]
        if accepts(q0, delta, trace):
            assert all(accepts(q0, delta, trace[:k]) for k in range(len(trace)))
        else:
            stop = run_monitor(q0, delta, trace)
            # Every extension of a stopped prefix is stopped at the same event.
            ext = trace + [rng.choice(["read", "send", "other"]) for _ in range(3)]
            assert run_monitor(q0, delta, ext) == stop
