# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/htn-decomposition/. The authors are listed in prov/NW29JR.jsonl.

"""Forward HTN decomposition in the style of SHOP (total order) and SHOP2
(partial order), over ground tasks and STRIPS operators.

A task is a string. It is primitive if the domain has an operator with that
name, and compound otherwise. A method for a compound task has a precondition,
a list of subtasks and ordering constraints between the subtasks (pairs of
indices). The planner works forward from the initial state: it always takes a
task with no predecessor, so it knows the current state when it applies an
operator or tests a method precondition.

Every node of a task network carries a depth: the tasks of the initial network
have depth 0, and the subtasks of a node of depth d have depth d + 1. A depth
bound D forbids the decomposition of a node of depth D or more, so the search
is finite.
"""

from itertools import count
from typing import Dict, FrozenSet, Iterable, Iterator, List, NamedTuple, Optional, Sequence, Tuple

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


def chain(k: int) -> FrozenSet[Tuple[int, int]]:
    return frozenset((i, i + 1) for i in range(k - 1))


def method(name: str, task: str, pre: Iterable[Fact], subtasks: Sequence[str],
           order: Optional[Iterable[Tuple[int, int]]] = None) -> Method:
    """A method; without an explicit order the subtasks are totally ordered."""
    order = chain(len(subtasks)) if order is None else frozenset(order)
    return Method(name, task, frozenset(pre), tuple(subtasks), order)


class Domain:
    def __init__(self, operators: Iterable[Operator], methods: Iterable[Method]) -> None:
        self.operators: Dict[str, Operator] = {o.name: o for o in operators}
        self.methods: Dict[str, List[Method]] = {}
        for m in methods:
            self.methods.setdefault(m.task, []).append(m)

    def is_primitive(self, task: str) -> bool:
        return task in self.operators


class TaskNetwork:
    """Nodes map to (task, depth); order is a set of pairs (u, v), meaning u before v."""

    def __init__(self, nodes: Dict[int, Tuple[str, int]], order: Iterable[Tuple[int, int]]) -> None:
        self.nodes = dict(nodes)
        self.order = set(order)

    @staticmethod
    def of(tasks: Sequence[str], order: Optional[Iterable[Tuple[int, int]]] = None) -> "TaskNetwork":
        order = chain(len(tasks)) if order is None else order
        return TaskNetwork({i: (t, 0) for i, t in enumerate(tasks)}, order)

    def minimal(self) -> List[int]:
        later = {v for _, v in self.order}
        return sorted(n for n in self.nodes if n not in later)

    def remove(self, n: int) -> "TaskNetwork":
        before = {u for u, v in self.order if v == n}
        after = {v for u, v in self.order if u == n}
        nodes = {k: x for k, x in self.nodes.items() if k != n}
        order = {(u, v) for u, v in self.order if n not in (u, v)} | {(u, v) for u in before for v in after}
        return TaskNetwork(nodes, order)

    def decompose(self, n: int, m: Method) -> "TaskNetwork":
        """Replace node n by the subtasks of m; they inherit every ordering of n."""
        task, depth = self.nodes[n]
        start = max(self.nodes) + 1
        ids = list(range(start, start + len(m.subtasks)))
        before = {u for u, v in self.order if v == n}
        after = {v for u, v in self.order if u == n}
        nodes = {k: x for k, x in self.nodes.items() if k != n}
        nodes.update({i: (t, depth + 1) for i, t in zip(ids, m.subtasks)})
        order = {(u, v) for u, v in self.order if n not in (u, v)}
        order |= {(u, i) for u in before for i in ids} | {(i, v) for i in ids for v in after}
        order |= {(ids[i], ids[j]) for i, j in m.order}
        if not ids:
            order |= {(u, v) for u in before for v in after}
        return TaskNetwork(nodes, order)


def apply(state: FrozenSet[Fact], op: Operator) -> FrozenSet[Fact]:
    return (state - op.delete) | op.add


def decompositions(state: FrozenSet[Fact], network: TaskNetwork, domain: Domain, depth: int) -> Iterator[Tuple[str, ...]]:
    """Every primitive plan the partial-order planner can reach, in search order.
    The same plan can appear more than once, through different choices of the next task."""
    if not network.nodes:  # @line L1
        yield ()
        return
    for n in network.minimal():  # @line L2
        task, d = network.nodes[n]
        if domain.is_primitive(task):  # @line L3
            op = domain.operators[task]
            if op.pre <= state:  # @line L4
                for rest in decompositions(apply(state, op), network.remove(n), domain, depth):  # @line L5
                    yield (task,) + rest  # @line L6
        elif d < depth:  # @line L7
            for m in domain.methods.get(task, []):
                if m.pre <= state:  # @line L8
                    yield from decompositions(state, network.decompose(n, m), domain, depth)  # @line L9 @line L10
    # @line L11 (every choice failed)


def shop(state: FrozenSet[Fact], tasks: Sequence[Tuple[str, int]], domain: Domain, depth: int) -> Iterator[Tuple[str, ...]]:
    """Total-order forward decomposition: the task list is processed from the left.
    Each entry is (task, depth); methods must order their subtasks totally."""
    if not tasks:
        yield ()
        return
    (task, d), rest = tasks[0], list(tasks[1:])
    if domain.is_primitive(task):
        op = domain.operators[task]
        if op.pre <= state:
            for tail in shop(apply(state, op), rest, domain, depth):
                yield (task,) + tail
    elif d < depth:
        for m in domain.methods.get(task, []):
            if m.pre <= state:
                if m.order != chain(len(m.subtasks)):
                    raise ValueError(f"method {m.name} is not totally ordered")
                yield from shop(state, [(t, d + 1) for t in m.subtasks] + rest, domain, depth)


def find_plan(init: Iterable[Fact], network: TaskNetwork, domain: Domain, depth: int) -> Optional[Tuple[str, ...]]:
    """The first plan in backtracking order, or None if no plan exists within the depth bound."""
    return next(decompositions(frozenset(init), network, domain, depth), None)


def all_plans(init: Iterable[Fact], network: TaskNetwork, domain: Domain, depth: int) -> set:
    return set(decompositions(frozenset(init), network, domain, depth))


def run_plan(init: Iterable[Fact], plan: Sequence[str], domain: Domain) -> Optional[FrozenSet[Fact]]:
    state = frozenset(init)
    for task in plan:
        op = domain.operators[task]
        if not op.pre <= state:
            return None
        state = apply(state, op)
    return state


def travel_domain() -> Tuple[FrozenSet[Fact], Domain]:
    """Go from home to the park. The bus method passes its own precondition but
    fails in its subtasks, so the planner backtracks to the taxi method."""
    ops = [
        operator("walk", ["at-home"], ["at-park"], ["at-home"]),
        operator("go-to-stop", ["at-home"], ["at-stop"], ["at-home"]),
        operator("buy-ticket", ["at-stop", "have-coin"], ["have-ticket"], ["have-coin"]),
        operator("ride-bus", ["at-stop", "have-ticket"], ["at-park"], ["at-stop", "have-ticket"]),
        operator("call-taxi", [], ["taxi-at-home"]),
        operator("ride-taxi", ["at-home", "taxi-at-home"], ["at-park", "owe-driver"], ["at-home", "taxi-at-home"]),
        operator("pay-driver", ["owe-driver", "have-cash"], [], ["owe-driver", "have-cash"]),
    ]
    methods = [
        method("by-foot", "travel", ["park-is-near"], ["walk"]),
        method("by-bus", "travel", [], ["go-to-stop", "buy-ticket", "ride-bus"]),
        method("by-taxi", "travel", ["have-cash"], ["call-taxi", "ride-taxi", "pay-driver"]),
    ]
    return frozenset({"at-home", "have-cash"}), Domain(ops, methods)
