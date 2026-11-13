# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hierarchical-task-network/. The authors are listed in prov/8H40VK.jsonl.

"""The HTN model over ground tasks, with two constructions that compare it with
STRIPS: any STRIPS task as a tail-recursive HTN, and an HTN whose solutions are
the strings a^n b^n, which no STRIPS task has as its set of plans.

The solutions of an HTN problem are the primitive plans that come from the
initial task network by decomposition and that are executable from the
initial state. A depth bound D forbids the decomposition of a node of depth D or
more; the tasks of the initial network have depth 0.
"""

from collections import deque
from typing import Dict, FrozenSet, Iterable, Iterator, List, NamedTuple, Optional, Sequence, Set, Tuple

Fact = str


class Operator(NamedTuple):
    name: str
    pre: FrozenSet[Fact]
    add: FrozenSet[Fact]
    delete: FrozenSet[Fact]


class Method(NamedTuple):
    name: str
    task: str
    pre: FrozenSet[Fact]
    subtasks: Tuple[str, ...]
    order: FrozenSet[Tuple[int, int]]


def operator(name: str, pre: Iterable[Fact] = (), add: Iterable[Fact] = (), delete: Iterable[Fact] = ()) -> Operator:
    return Operator(name, frozenset(pre), frozenset(add), frozenset(delete) - frozenset(add))


def method(name: str, task: str, pre: Iterable[Fact], subtasks: Sequence[str]) -> Method:
    """A method whose subtasks are totally ordered."""
    return Method(name, task, frozenset(pre), tuple(subtasks), frozenset((i, i + 1) for i in range(len(subtasks) - 1)))


class Domain:
    def __init__(self, operators: Iterable[Operator], methods: Iterable[Method]) -> None:
        self.operators: Dict[str, Operator] = {o.name: o for o in operators}
        self.methods: Dict[str, List[Method]] = {}
        for m in methods:
            self.methods.setdefault(m.task, []).append(m)


class TaskNetwork(NamedTuple):
    nodes: Dict[int, Tuple[str, int]]
    order: FrozenSet[Tuple[int, int]]

    @staticmethod
    def of(tasks: Sequence[str]) -> "TaskNetwork":
        return TaskNetwork({i: (t, 0) for i, t in enumerate(tasks)}, frozenset((i, i + 1) for i in range(len(tasks) - 1)))


def minimal(net: TaskNetwork) -> List[int]:
    later = {v for _, v in net.order}
    return sorted(n for n in net.nodes if n not in later)


def replace(net: TaskNetwork, n: int, m: Optional[Method]) -> TaskNetwork:
    """Remove node n (m is None) or decompose it by m; new nodes inherit its orderings."""
    task, depth = net.nodes[n]
    subtasks = m.subtasks if m else ()
    start = max(net.nodes) + 1
    ids = list(range(start, start + len(subtasks)))
    before = {u for u, v in net.order if v == n}
    after = {v for u, v in net.order if u == n}
    nodes = {k: x for k, x in net.nodes.items() if k != n}
    nodes.update({i: (t, depth + 1) for i, t in zip(ids, subtasks)})
    order = {(u, v) for u, v in net.order if n not in (u, v)}
    order |= {(u, i) for u in before for i in ids} | {(i, v) for i in ids for v in after}
    if m:
        order |= {(ids[i], ids[j]) for i, j in m.order}
    if not ids:
        order |= {(u, v) for u in before for v in after}
    return TaskNetwork(nodes, frozenset(order))


def solutions(state: FrozenSet[Fact], net: TaskNetwork, domain: Domain, depth: int) -> Iterator[Tuple[str, ...]]:
    """Every solution within the depth bound, found by forward decomposition."""
    if not net.nodes:
        yield ()
        return
    for n in minimal(net):
        task, d = net.nodes[n]
        if task in domain.operators:
            op = domain.operators[task]
            if op.pre <= state:
                for rest in solutions((state - op.delete) | op.add, replace(net, n, None), domain, depth):
                    yield (task,) + rest
        elif d < depth:
            for m in domain.methods.get(task, []):
                if m.pre <= state:
                    yield from solutions(state, replace(net, n, m), domain, depth)


def solution_set(init: Iterable[Fact], tasks: Sequence[str], domain: Domain, depth: int) -> Set[Tuple[str, ...]]:
    return set(solutions(frozenset(init), TaskNetwork.of(tasks), domain, depth))


def anbn_domain() -> Domain:
    """S -> a S b | a b, with primitive a and b that need and change nothing."""
    return Domain([operator("a"), operator("b")],
                  [method("wrap", "S", [], ["a", "S", "b"]), method("base", "S", [], ["a", "b"])])


def strips_as_htn(operators: Sequence[Operator], goal: Iterable[Fact]) -> Domain:
    """The task 'solve' stops when the goal holds, or does one action and solves again.
    Its solutions are the STRIPS plans; with depth bound D, those of length below D."""
    methods = [method("stop", "solve", goal, [])]
    methods += [method(f"use-{o.name}", "solve", [], [o.name, "solve"]) for o in operators]
    return Domain(operators, methods)


# Labeled STRIPS tasks: every action carries a letter, and a word is accepted if
# some executable sequence of actions with those letters reaches the goal.

class Labeled(NamedTuple):
    label: str
    op: Operator


def accepts(init: Iterable[Fact], goal: Iterable[Fact], actions: Sequence[Labeled], word: str) -> bool:
    states = {frozenset(init)}
    goal = frozenset(goal)
    for letter in word:
        states = {(s - a.op.delete) | a.op.add for s in states for a in actions if a.label == letter and a.op.pre <= s}
        if not states:
            return False
    return any(goal <= s for s in states)


def reachable_states(init: Iterable[Fact], actions: Sequence[Labeled]) -> Set[FrozenSet[Fact]]:
    start = frozenset(init)
    seen = {start}
    queue = deque([start])
    while queue:
        s = queue.popleft()
        for a in actions:
            if a.op.pre <= s:
                t = (s - a.op.delete) | a.op.add
                if t not in seen:
                    seen.add(t)
                    queue.append(t)
    return seen
