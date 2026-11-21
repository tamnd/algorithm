# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/security-automaton/. The authors are listed in prov/MN9D48.jsonl.

from collections.abc import Callable, Hashable, Iterable, Sequence

State = Hashable
Event = Hashable
Delta = Callable[[State, Event], Iterable[State]]


def run_monitor(initial: Iterable[State], delta: Delta, events: Sequence[Event]) -> int | None:
    """Simulate a security automaton on a sequence of events.

    The automaton is given by its set of initial states and its transition
    function delta(q, s), which returns the set of next states (empty when the
    automaton has no move). Return the 0-based index of the first event that
    the monitor stops before it runs, or None when the monitor allows every
    event. Precondition: delta returns a finite set. Cost: O(k |Q| d) calls of
    delta and set work for k events, |Q| states and at most d next states per
    move.
    """
    current = set(initial)  # @line L1
    for i, s in enumerate(events):  # @line L2
        nxt: set[State] = set()
        for q in current:  # @line L3
            nxt.update(delta(q, s))
        if not nxt:  # @line L4
            return i
        current = nxt  # @line L5
    return None  # @line L6


def accepts(initial: Iterable[State], delta: Delta, events: Sequence[Event]) -> bool:
    """True when the monitor allows the whole sequence."""
    return run_monitor(initial, delta, events) is None


def table_delta(table: dict[tuple[State, Event], Iterable[State]]) -> Delta:
    """Turn a transition table into a transition function; a missing entry has no move."""

    def delta(q: State, s: Event) -> Iterable[State]:
        return table.get((q, s), ())

    return delta


def no_send_after_read() -> tuple[set[str], Delta]:
    """The automaton of the policy "no send after a file read" over the events read, send and other."""
    table = {
        ("clean", "read"): {"tainted"},
        ("clean", "send"): {"clean"},
        ("clean", "other"): {"clean"},
        ("tainted", "read"): {"tainted"},
        ("tainted", "other"): {"tainted"},
    }
    return {"clean"}, table_delta(table)
