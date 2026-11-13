# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/strips-plan-existence-pspace-complete/. The authors are listed in prov/NF2ETY.jsonl.

"""Executable parts of the proof that STRIPS plan existence is PSPACE-complete.

tm_to_strips is the hardness reduction: a Turing machine that uses at most p
tape cells becomes a STRIPS task whose states are the machine's configurations.
savitch_reach is the membership argument: a midpoint recursion that decides
plan existence while it stores only O(|F|) states at a time.
hanoi_task gives a family whose shortest plans are exponentially long.
"""

from collections import deque
from itertools import product
from typing import Dict, FrozenSet, Hashable, Iterable, List, NamedTuple, Optional, Sequence, Tuple

Fact = Hashable
State = FrozenSet[Fact]


class Action(NamedTuple):
    name: str
    pre: FrozenSet[Fact]
    add: FrozenSet[Fact]
    delete: FrozenSet[Fact]


def make_action(name: str, pre: Iterable[Fact] = (), add: Iterable[Fact] = (), delete: Iterable[Fact] = ()) -> Action:
    return Action(name, frozenset(pre), frozenset(add), frozenset(delete))


def successor(s: State, a: Action) -> State:
    return (s - a.delete) | a.add


def bfs_distance(init: Iterable[Fact], goal: Iterable[Fact], actions: Sequence[Action]) -> Optional[int]:
    init = frozenset(init)
    goal = frozenset(goal)
    dist = {init: 0}
    queue = deque([init])
    while queue:
        s = queue.popleft()
        if goal <= s:
            return dist[s]
        for a in actions:
            if a.pre <= s:
                t = successor(s, a)
                if t not in dist:
                    dist[t] = dist[s] + 1
                    queue.append(t)
    return None


def reachable_states(init: Iterable[Fact], actions: Sequence[Action]) -> List[State]:
    init = frozenset(init)
    seen = {init}
    queue = deque([init])
    while queue:
        s = queue.popleft()
        for a in actions:
            if a.pre <= s:
                t = successor(s, a)
                if t not in seen:
                    seen.add(t)
                    queue.append(t)
    return list(seen)


# ---------------------------------------------------------------- hardness

# A machine is (states, alphabet, delta, start, accept, blank). delta maps
# (q, x) to a list of moves (q2, y, d) with d in {-1, 0, +1}; a deterministic
# machine has at most one move per pair. The head starts on cell 0. A move that
# would leave cells 0..p-1 is not available, so the machine halts there.

def tm_to_strips(machine, word: Sequence, p: int):
    """Facts head(i, q), sym(i, x) and accept. One action per cell and move.
    Every action has two positive preconditions; a write that keeps the symbol
    changes only the head fact."""
    states, alphabet, delta, start, accept, blank = machine
    acts = []
    for i in range(p):
        for (q, x), moves in delta.items():
            for (q2, y, d) in moves:
                j = i + d
                if not 0 <= j < p:
                    continue
                pre = [("head", i, q), ("sym", i, x)]
                add = [("head", j, q2)]
                delete = [("head", i, q)]
                if y != x:
                    add.append(("sym", i, y))
                    delete.append(("sym", i, x))
                if (j, q2) == (i, q):            # the head fact is both deleted and added: keep it
                    add.remove(("head", j, q2))
                    delete.remove(("head", i, q))
                acts.append(make_action(f"step({i},{q},{x})->({q2},{y},{d})", pre, add, delete))
        acts.append(make_action(f"accept({i})", [("head", i, accept)], [("accept",)], []))
    tape = list(word) + [blank] * (p - len(word))
    init = {("head", 0, start)} | {("sym", i, tape[i]) for i in range(p)}
    return frozenset(init), frozenset([("accept",)]), acts


def run_dtm(machine, word: Sequence, p: int) -> bool:
    """Direct simulation of a deterministic machine on p cells. A repeated
    configuration means the machine loops and never accepts."""
    states, alphabet, delta, start, accept, blank = machine
    tape = list(word) + [blank] * (p - len(word))
    q, i = start, 0
    seen = set()
    while True:
        if q == accept:
            return True
        conf = (q, i, tuple(tape))
        if conf in seen:
            return False
        seen.add(conf)
        moves = [m for m in delta.get((q, tape[i]), []) if 0 <= i + m[2] < p]
        if not moves:
            return False
        q2, y, d = moves[0]
        tape[i] = y
        q, i = q2, i + d


def ntm_accepts(machine, word: Sequence, p: int) -> bool:
    """Search over configurations of a nondeterministic machine on p cells."""
    states, alphabet, delta, start, accept, blank = machine
    tape = tuple(list(word) + [blank] * (p - len(word)))
    start_conf = (start, 0, tape)
    seen = {start_conf}
    queue = deque([start_conf])
    while queue:
        q, i, t = queue.popleft()
        if q == accept:
            return True
        for (q2, y, d) in delta.get((q, t[i]), []):
            if 0 <= i + d < p:
                c = (q2, i + d, t[:i] + (y,) + t[i + 1:])
                if c not in seen:
                    seen.add(c)
                    queue.append(c)
    return False


def decode(state: State, p: int):
    """The configuration a state encodes, or None if it encodes none."""
    heads = [f for f in state if f[0] == "head"]
    syms = sorted(f for f in state if f[0] == "sym")
    if len(heads) != 1 or [f[1] for f in syms] != list(range(p)):
        return None
    _, i, q = heads[0]
    return q, i, tuple(f[2] for f in syms)


# ---------------------------------------------------------------- membership

def all_states(facts: Sequence[Fact]) -> List[State]:
    return [frozenset(f for f, bit in zip(facts, bits) if bit) for bits in product((0, 1), repeat=len(facts))]


def savitch_reach(s: State, t: State, i: int, actions: Sequence[Action], universe: List[State]) -> bool:
    """True if t is reachable from s in at most 2^i steps. The recursion depth is
    i and each level stores one midpoint, so the space is O(i * |F|)."""
    if s == t:
        return True
    if i == 0:
        return any(a.pre <= s and successor(s, a) == t for a in actions)
    return any(savitch_reach(s, m, i - 1, actions, universe) and savitch_reach(m, t, i - 1, actions, universe)
               for m in universe)


def plan_exists_savitch(facts: Sequence[Fact], init: State, goal: State, actions: Sequence[Action]) -> bool:
    """A plan exists iff some goal state is reachable in at most 2^|F| - 1 steps."""
    universe = all_states(facts)
    return any(goal <= t and savitch_reach(init, t, len(facts), actions, universe) for t in universe)


# ---------------------------------------------------------------- long plans

def hanoi_task(n: int):
    """Tower of Hanoi with n disks: disk d may sit on a larger disk or a peg.
    It has O(n^2) facts and its shortest plan has 2^n - 1 actions."""
    disks = list(range(1, n + 1))
    places = disks + ["P1", "P2", "P3"]
    acts = []
    for d in disks:
        for x in places:
            for y in places:
                if x == y or d == x or d == y:
                    continue
                if (isinstance(x, int) and x <= d) or (isinstance(y, int) and y <= d):
                    continue
                acts.append(make_action(f"move({d},{x},{y})", [("on", d, x), ("clear", d), ("clear", y)],
                                        [("on", d, y), ("clear", x)], [("on", d, x), ("clear", y)]))
    init = {("on", n, "P1"), ("clear", 1), ("clear", "P2"), ("clear", "P3")}
    goal = {("on", n, "P3")}
    for d in range(1, n):
        init.add(("on", d, d + 1))
        goal.add(("on", d, d + 1))
    return frozenset(init), frozenset(goal), acts
