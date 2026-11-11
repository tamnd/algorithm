# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/replicated-log/. The authors are listed in prov/BQWX41.jsonl.

"""The replicated log as a data structure, at one replica.

Slots are numbered 1, 2, 3, ... . Each slot holds an entry (term, command) or
nothing. The replica keeps two indexes:

- commit_index: every slot up to it holds a committed (chosen) entry;
- last_applied: the state machine has applied every slot up to it.

The invariant is last_applied <= commit_index, and the slots up to
commit_index never change. Two ways to fill the log are shown:

- Multi-Paxos style: a slot can be chosen out of order, which leaves gaps;
  the commit index is the end of the longest chosen prefix, and a new leader
  fills gaps with NOOP;
- Raft style: the follower side of AppendEntries (Ongaro and Ousterhout 2014,
  Figure 2), which keeps the Log Matching Property.

A snapshot replaces the prefix up to an index by the state after it.
"""

from typing import Callable

NOOP = ("noop",)
Entry = tuple  # (term, command)


class Log:
    def __init__(self, s0: object, apply: Callable[[object, tuple], object]) -> None:
        self.entries: dict[int, Entry] = {}
        self.chosen: set[int] = set()
        self.commit_index = 0
        self.last_applied = 0
        self.apply_fn = apply
        self.state = s0
        self.snap_index = 0  # the slots up to snap_index are in the snapshot
        self.snap_term = 0

    # ------------------------------------------------------------ common
    def last_index(self) -> int:
        return max(self.entries, default=self.snap_index)

    def term_at(self, i: int) -> int | None:
        if i == self.snap_index:
            return self.snap_term
        e = self.entries.get(i)
        return None if e is None else e[0]

    def apply_committed(self) -> list[int]:
        """Apply the committed slots in order. Returns the slots applied."""
        done = []
        while self.last_applied < self.commit_index:
            i = self.last_applied + 1
            cmd = self.entries[i][1]
            if cmd != NOOP:
                self.state = self.apply_fn(self.state, cmd)
            self.last_applied = i
            done.append(i)
        return done

    # ------------------------------------------------------------ Multi-Paxos style
    def choose(self, slot: int, term: int, cmd: tuple) -> None:
        """Slot `slot` is chosen with this command. A chosen slot never changes."""
        old = self.entries.get(slot)
        if slot in self.chosen:
            assert old == (term, cmd) or old[1] == cmd, "a chosen slot cannot change"
            return
        self.entries[slot] = (term, cmd)
        self.chosen.add(slot)
        while self.commit_index + 1 in self.chosen:
            self.commit_index += 1

    def gaps(self) -> list[int]:
        top = max(self.chosen, default=0)
        return [i for i in range(self.commit_index + 1, top) if i not in self.chosen]

    def fill_gaps(self, term: int) -> list[int]:
        """What a new leader does when phase 1 shows no value in a slot: propose NOOP."""
        g = self.gaps()
        for i in g:
            self.choose(i, term, NOOP)
        return g

    # ------------------------------------------------------------ Raft style
    def append_entries(self, prev_index: int, prev_term: int, new: list[Entry],
                       leader_commit: int) -> bool:
        """The receiver rules of AppendEntries. Returns False on a log mismatch."""
        if prev_index > self.last_index() or self.term_at(prev_index) != prev_term:
            return False
        for k, e in enumerate(new):
            i = prev_index + 1 + k
            if i <= self.snap_index:
                continue
            if i in self.entries and self.entries[i][0] != e[0]:
                assert i > self.commit_index, "a committed entry cannot be removed"
                for j in [j for j in self.entries if j >= i]:
                    del self.entries[j]
            if i not in self.entries:
                self.entries[i] = e
        if leader_commit > self.commit_index:
            self.commit_index = min(leader_commit, prev_index + len(new))
        return True

    # ------------------------------------------------------------ compaction
    def snapshot(self) -> tuple[int, int, object]:
        """Drop the applied prefix; keep (last included index, its term, state)."""
        i = self.last_applied
        if i > self.snap_index:
            self.snap_term = self.term_at(i)
            for j in [j for j in self.entries if j <= i]:
                del self.entries[j]
            self.snap_index = i
        return self.snap_index, self.snap_term, self.state

    def install_snapshot(self, index: int, term: int, state: object) -> None:
        """Replace the prefix up to index by a snapshot from the leader."""
        if index <= self.snap_index:
            return
        if self.term_at(index) == term:
            keep = {j: e for j, e in self.entries.items() if j > index}
        else:
            keep = {}
        self.entries = keep
        self.snap_index, self.snap_term, self.state = index, term, state
        self.commit_index = max(self.commit_index, index)
        self.last_applied = index
