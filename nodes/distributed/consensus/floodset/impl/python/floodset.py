# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/floodset/. The authors are listed in prov/MBNRW2.jsonl.

"""FloodSet consensus in the synchronous model with crash failures.

Lynch, Distributed Algorithms (1996), Section 6.2. There are n processes
0 .. n - 1 on a complete graph with reliable links. The run is in lock-step
rounds: each live process sends, then each live process receives and computes.
A crash plan maps a process to (r, S): the process crashes in round r, and its
round-r message reaches only the processes in S. It sends nothing later and
does not decide. At most f processes crash.

Cost: f + 1 rounds, at most n (n - 1) (f + 1) messages, each a set of at
most |V| values.
"""

from itertools import combinations, product
from typing import Hashable, Iterator

Crash = tuple[int, frozenset[int]]


class FloodSetProcess:
    """The local state of one process: its set W of known values."""

    def __init__(self, pid: int, value: Hashable, rule: str, default: Hashable) -> None:
        self.pid = pid
        self.rule = rule
        self.default = default
        self.w: set[Hashable] = {value}  # @line L1
        self.decision: Hashable | None = None

    def msg(self) -> frozenset[Hashable]:
        """The message of a round: the whole set W."""
        return frozenset(self.w)  # @line L3

    def receive(self, sets: list[frozenset[Hashable]]) -> None:
        """Add the values of each set that arrived in this round."""
        for x in sets:  # @line L4
            self.w |= x  # @line L5

    def decide(self) -> Hashable:
        """The decision rule after the last round."""
        if len(self.w) == 1:  # @line L6
            self.decision = next(iter(self.w))
        elif self.rule == "min":
            self.decision = min(self.w)  # type: ignore[type-var]
        else:
            self.decision = self.default  # @line L7
        return self.decision


def floodset(
    inputs: list[Hashable],
    f: int,
    crashes: dict[int, Crash] | None = None,
    rounds: int | None = None,
    rule: str = "default",
    default: Hashable = 0,
) -> dict:
    """Run FloodSet and return the result of the run.

    rounds defaults to f + 1. rule is "default" (Lynch: decide the one value
    of W, else the default) or "min" (decide min W). The result has the
    decisions of the processes that did not crash, the number of rounds, the
    number of messages and the final sets W.
    """
    n = len(inputs)
    crashes = crashes or {}
    if len(crashes) > f:
        raise ValueError("more than f crashes")
    total = f + 1 if rounds is None else rounds
    procs = [FloodSetProcess(i, inputs[i], rule, default) for i in range(n)]
    live = set(range(n))
    messages = 0
    for r in range(1, total + 1):  # @line L2
        inbox: dict[int, list[frozenset[Hashable]]] = {i: [] for i in range(n)}
        crashed_now = set()
        for i in sorted(live):
            m = procs[i].msg()
            if i in crashes and crashes[i][0] == r:
                targets = [j for j in sorted(crashes[i][1]) if j != i]
                crashed_now.add(i)
            else:
                targets = [j for j in range(n) if j != i]
            for j in targets:
                inbox[j].append(m)
                messages += 1
        live -= crashed_now
        for i in sorted(live):
            procs[i].receive(inbox[i])
    decisions = {i: procs[i].decide() for i in sorted(live)}
    return {
        "decisions": decisions,
        "rounds": total,
        "messages": messages,
        "w": {i: frozenset(procs[i].w) for i in sorted(live)},
    }


def crash_patterns(n: int, f: int, rounds: int) -> Iterator[dict[int, Crash]]:
    """Every crash plan with at most f crashes in rounds 1 .. rounds.

    Each crashing process picks a round and any subset of the other processes
    as the receivers of its last message.
    """
    for k in range(f + 1):
        for who in combinations(range(n), k):
            options = []
            for p in who:
                others = [q for q in range(n) if q != p]
                opts = []
                for r in range(1, rounds + 1):
                    for mask in range(1 << len(others)):
                        s = frozenset(others[b] for b in range(len(others)) if mask >> b & 1)
                        opts.append((r, s))
                options.append(opts)
            for choice in product(*options):
                yield dict(zip(who, choice))


def check_run(inputs: list[Hashable], result: dict) -> list[str]:
    """Return the consensus properties that the run breaks."""
    bad = []
    values = set(result["decisions"].values())
    if len(values) > 1:
        bad.append("agreement")
    if len(set(inputs)) == 1 and values and values != {inputs[0]}:
        bad.append("validity")
    return bad
