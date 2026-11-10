# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-generals-problem/. The authors are listed in prov/6MJM6Y.jsonl.

"""Brute force checks for the two generals (coordinated attack) problem.

Two processes, A = 0 and B = 1, each with an input bit (1 means "attack").
They run a fixed number of synchronous rounds. A schedule lists, for each
round, which processes send in it. Any message can be lost. After the last
round each process decides a bit. The conditions, as in Lynch, Section 5.1:

  agreement   both decide the same value, in every run;
  validity    if both inputs are 0, both decide 0; if both inputs are 1 and
              no message is lost, both decide 1;
  termination both decide after the last round (built in).

A protocol decides by a rule on the local view of a process. The full
information protocol sends the whole view in each message, so each other
protocol's decision is a function of the full information view. So if no
rule on full information views works, no protocol with that schedule works.
The search uses a union-find over views: in each run, the views of A and B
must get the same value.
"""

from itertools import product
from typing import Hashable, Iterator, Optional

Schedule = list[list[int]]
Run = tuple[tuple[int, int], frozenset[int]]  # inputs, lost message slots


def alternating(k: int) -> Schedule:
    """k rounds; A sends in odd rounds and B in even rounds."""
    return [[i % 2] for i in range(k)]


def simultaneous(r: int) -> Schedule:
    """r rounds; both send in each round."""
    return [[0, 1] for _ in range(r)]


def slots(schedule: Schedule) -> list[tuple[int, int]]:
    """(round, sender) for each message slot, in order."""
    return [(r, s) for r, senders in enumerate(schedule) for s in senders]


def full_info_views(schedule: Schedule, inputs: tuple[int, int], lost: frozenset[int]) -> tuple[Hashable, Hashable]:
    view: list[Hashable] = [(inputs[0],), (inputs[1],)]
    i = 0
    for senders in schedule:
        inbox: list[Hashable] = [None, None]
        for s in senders:
            if i not in lost:
                inbox[1 - s] = view[s]
            i += 1
        view = [(view[0], inbox[0]), (view[1], inbox[1])]
    return view[0], view[1]


def all_runs(schedule: Schedule) -> Iterator[Run]:
    m = len(slots(schedule))
    for inputs in product([0, 1], repeat=2):
        for mask in range(1 << m):
            yield (inputs, frozenset(i for i in range(m) if mask >> i & 1))  # type: ignore[misc]


def forced(run: Run, strong: bool = True) -> Optional[int]:
    """The value that validity forces in this run, if any."""
    inputs, lost = run
    if inputs == (0, 0):
        return 0
    if strong and inputs == (1, 1) and not lost:
        return 1
    return None


class _UF:
    def __init__(self) -> None:
        self.parent: dict[Hashable, Hashable] = {}

    def find(self, x: Hashable) -> Hashable:
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: Hashable, b: Hashable) -> None:
        self.parent[self.find(a)] = self.find(b)


def rule_exists(view_pairs: list[tuple[Hashable, Hashable, Optional[int]]]) -> Optional[dict]:
    """Given (view of A, view of B, forced value) for each run, return a
    decision rule (a dict from (process, view) to a bit) that meets agreement
    and validity in all runs, or None if there is none."""
    uf = _UF()
    for va, vb, _ in view_pairs:
        uf.union((0, va), (1, vb))
    need: dict[Hashable, int] = {}
    for va, vb, v in view_pairs:
        if v is None:
            continue
        root = uf.find((0, va))
        if need.setdefault(root, v) != v:
            return None
    rule = {}
    for va, vb, _ in view_pairs:
        for node in ((0, va), (1, vb)):
            rule[node] = need.get(uf.find(node), 0)
    return rule


def solvable(schedule: Schedule, strong: bool = True) -> bool:
    pairs = [(*full_info_views(schedule, *run), forced(run, strong)) for run in all_runs(schedule)]
    return rule_exists(pairs) is not None


def one_bit_protocols(k: int) -> Iterator[list[dict]]:
    """All alternating protocols with k one-bit messages. Message i is a
    function of the sender's history: its input and the bits it got so far
    (None for a lost message)."""
    tables_per_slot = []
    for i in range(k):
        got = len([j for j in range(i) if j % 2 != i % 2])
        hist = list(product([0, 1], *([[0, 1, None]] * got)))
        tables_per_slot.append([dict(zip(hist, bits)) for bits in product([0, 1], repeat=len(hist))])
    yield from (list(t) for t in product(*tables_per_slot))


def one_bit_histories(tables: list[dict], inputs: tuple[int, int], lost: frozenset[int]) -> tuple[tuple, tuple]:
    hist: list[tuple] = [(inputs[0],), (inputs[1],)]
    for i, table in enumerate(tables):
        s = i % 2
        bit = table[hist[s]]
        hist[1 - s] = hist[1 - s] + (None if i in lost else bit,)
    return hist[0], hist[1]


def one_bit_solvable(tables: list[dict], strong: bool = True) -> bool:
    schedule = alternating(len(tables))
    pairs = [(*one_bit_histories(tables, *run), forced(run, strong)) for run in all_runs(schedule)]
    return rule_exists(pairs) is not None


def last_message_chain(schedule: Schedule) -> list[Run]:
    """The chain of the impossibility proof. Start with inputs (1, 1) and no
    loss. Lose the last delivered message, then the one before it, and so on.
    With all messages lost, set the input of A to 0, then the input of B."""
    m = len(slots(schedule))
    chain: list[Run] = [((1, 1), frozenset())]
    for i in range(m - 1, -1, -1):
        chain.append(((1, 1), frozenset(range(i, m))))
    everything = frozenset(range(m))
    chain.append(((0, 1), everything))
    chain.append(((0, 0), everything))
    return chain


def same_view_witness(schedule: Schedule, a: Run, b: Run) -> Optional[int]:
    """A process with the same full information view in both runs, if any."""
    va, vb = full_info_views(schedule, *a), full_info_views(schedule, *b)
    for p in (0, 1):
        if va[p] == vb[p]:
            return p
    return None
