# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partial-order-plan/. The authors are listed in prov/QH51FZ.jsonl.

"""A partial-order plan over ground STRIPS actions.

The plan holds a list of steps, a set of ordering constraints (i, j), read
"step i comes before step j", and a set of causal links (i, p, j), read "step
i produces the fact p for step j". Step 0 is START, whose add list is the
initial state, and step 1 is FINISH, whose precondition is the goal. Every
other step is ordered after START and before FINISH.
"""

from typing import Dict, FrozenSet, Hashable, Iterable, Iterator, List, NamedTuple, Optional, Sequence, Set, Tuple

Fact = Hashable
State = FrozenSet[Fact]

START, FINISH = 0, 1


class Action(NamedTuple):
    name: str
    pre: FrozenSet[Fact]
    add: FrozenSet[Fact]
    delete: FrozenSet[Fact]


def make_action(name: str, pre: Iterable[Fact] = (), add: Iterable[Fact] = (), delete: Iterable[Fact] = ()) -> Action:
    return Action(name, frozenset(pre), frozenset(add), frozenset(delete))


def successor(state: State, action: Action) -> State:
    return (state - action.delete) | action.add


def run_plan(state: State, plan: Sequence[Action]) -> Optional[State]:
    for action in plan:
        if not action.pre <= state:
            return None
        state = successor(state, action)
    return state


def is_plan(init: State, goal: FrozenSet[Fact], plan: Sequence[Action]) -> bool:
    end = run_plan(frozenset(init), plan)
    return end is not None and frozenset(goal) <= end


class Link(NamedTuple):
    producer: int
    fact: Fact
    consumer: int


class PartialOrderPlan:
    """Steps, ordering constraints and causal links. The orderings may be
    cyclic after add_ordering_unchecked; is_consistent tells."""

    def __init__(self, init: Iterable[Fact], goal: Iterable[Fact]) -> None:
        self.steps: List[Action] = [make_action("START", add=init), make_action("FINISH", pre=goal)]
        self.after: Dict[int, Set[int]] = {START: {FINISH}, FINISH: set()}
        self.links: Set[Link] = set()

    def copy(self) -> "PartialOrderPlan":
        other = PartialOrderPlan.__new__(PartialOrderPlan)
        other.steps = list(self.steps)
        other.after = {i: set(s) for i, s in self.after.items()}
        other.links = set(self.links)
        return other

    @property
    def orderings(self) -> Set[Tuple[int, int]]:
        return {(i, j) for i, s in self.after.items() for j in s}

    def add_step(self, action: Action) -> int:
        i = len(self.steps)  # @line L1
        self.steps.append(action)
        self.after[i] = {FINISH}
        self.after[START].add(i)
        return i

    def precedes(self, i: int, j: int) -> bool:
        """True when a chain of orderings leads from i to j (i != j)."""
        seen, stack = {i}, [i]  # @line L2
        while stack:  # @line L3
            for k in self.after[stack.pop()]:  # @line L4
                if k == j:  # @line L5
                    return True
                if k not in seen:  # @line L6
                    seen.add(k)
                    stack.append(k)
        return False  # @line L7

    def can_order(self, i: int, j: int) -> bool:
        """Adding i < j to a consistent plan keeps it consistent."""
        return i != j and not self.precedes(j, i)

    def add_ordering(self, i: int, j: int) -> bool:
        if not self.can_order(i, j):  # @line L8
            return False
        self.after[i].add(j)  # @line L9
        return True

    def add_ordering_unchecked(self, i: int, j: int) -> None:
        self.after[i].add(j)

    def add_link(self, i: int, fact: Fact, j: int) -> bool:
        if fact not in self.steps[i].add or fact not in self.steps[j].pre:  # @line L10
            raise ValueError("a link needs a producer that adds the fact and a consumer that needs it")
        if not self.add_ordering(i, j):  # @line L11
            return False
        self.links.add(Link(i, fact, j))  # @line L12
        return True

    def is_consistent(self) -> bool:
        """Kahn's algorithm: the orderings are consistent iff they are acyclic."""
        indegree = {i: 0 for i in self.after}
        for s in self.after.values():
            for j in s:
                indegree[j] += 1
        ready = [i for i, d in indegree.items() if d == 0]
        done = 0
        while ready:
            i = ready.pop()
            done += 1
            for j in self.after[i]:
                indegree[j] -= 1
                if indegree[j] == 0:
                    ready.append(j)
        return done == len(self.after)

    def linearizations(self) -> Iterator[Tuple[int, ...]]:
        """Every total order of the steps that respects the orderings."""
        indegree = {i: 0 for i in self.after}
        for s in self.after.values():
            for j in s:
                indegree[j] += 1
        order: List[int] = []

        def extend() -> Iterator[Tuple[int, ...]]:
            if len(order) == len(indegree):
                yield tuple(order)
                return
            for i in sorted(indegree):
                if indegree[i] == 0:
                    indegree[i] = -1
                    for j in self.after[i]:
                        indegree[j] -= 1
                    order.append(i)
                    yield from extend()
                    order.pop()
                    for j in self.after[i]:
                        indegree[j] += 1
                    indegree[i] = 0

        yield from extend()

    def possibly_between(self, k: int, i: int, j: int) -> bool:
        """Some linearization places k after i and before j (given i < j)."""
        return k != i and k != j and not self.precedes(k, i) and not self.precedes(j, k)

    def threats(self) -> List[Tuple[int, Link]]:
        """Pairs (k, link) where step k deletes the fact of the link and may fall between its ends."""
        found = []
        for link in sorted(self.links, key=repr):  # @line L13
            for k, step in enumerate(self.steps):
                if link.fact in step.delete and self.possibly_between(k, link.producer, link.consumer):  # @line L14
                    found.append((k, link))
        return found

    def open_conditions(self) -> List[Tuple[Fact, int]]:
        """Pairs (p, j) where p is a precondition of step j with no link."""
        linked = {(link.fact, link.consumer) for link in self.links}
        return [(p, j) for j, step in enumerate(self.steps) for p in sorted(step.pre, key=repr)  # @line L15
                if (p, j) not in linked]  # @line L16

    def is_solution(self) -> bool:
        return self.is_consistent() and not self.open_conditions() and not self.threats()  # @line L17

    def actions(self, order: Sequence[int]) -> List[Action]:
        return [self.steps[i] for i in order if i not in (START, FINISH)]

    def every_linearization_valid(self) -> bool:
        init = self.steps[START].add
        goal = self.steps[FINISH].pre
        orders = list(self.linearizations())
        return bool(orders) and all(is_plan(init, goal, self.actions(order)) for order in orders)


def move_actions(blocks: Sequence[str]) -> List[Action]:
    """The blocks world with one move operator and no hand."""
    acts = []
    for b in blocks:
        for x in blocks:
            if x == b:
                continue
            acts.append(make_action(f"move({b},{x},table)", [("on", b, x), ("clear", b)], [("ontable", b), ("clear", x)], [("on", b, x)]))
            acts.append(make_action(f"move({b},table,{x})", [("ontable", b), ("clear", b), ("clear", x)], [("on", b, x)], [("ontable", b), ("clear", x)]))
            for y in blocks:
                if y != b and y != x:
                    acts.append(make_action(f"move({b},{x},{y})", [("on", b, x), ("clear", b), ("clear", y)], [("on", b, y), ("clear", x)], [("on", b, x), ("clear", y)]))
    return acts


SUSSMAN_INIT = frozenset({("on", "c", "a"), ("ontable", "a"), ("ontable", "b"), ("clear", "c"), ("clear", "b")})
SUSSMAN_GOAL = frozenset({("on", "a", "b"), ("on", "b", "c")})


def sussman_plan(resolve: bool = True) -> PartialOrderPlan:
    """The partial-order plan for the Sussman anomaly. With resolve=False the
    two orderings that remove its threats are left out."""
    acts = {a.name: a for a in move_actions("abc")}
    plan = PartialOrderPlan(SUSSMAN_INIT, SUSSMAN_GOAL)
    c_off = plan.add_step(acts["move(c,a,table)"])
    b_on = plan.add_step(acts["move(b,table,c)"])
    a_on = plan.add_step(acts["move(a,table,b)"])
    plan.add_link(a_on, ("on", "a", "b"), FINISH)
    plan.add_link(b_on, ("on", "b", "c"), FINISH)
    plan.add_link(START, ("on", "c", "a"), c_off)
    plan.add_link(START, ("clear", "c"), c_off)
    plan.add_link(START, ("ontable", "b"), b_on)
    plan.add_link(START, ("clear", "b"), b_on)
    plan.add_link(START, ("clear", "c"), b_on)
    plan.add_link(START, ("ontable", "a"), a_on)
    plan.add_link(c_off, ("clear", "a"), a_on)
    plan.add_link(START, ("clear", "b"), a_on)
    if resolve:
        plan.add_ordering(c_off, b_on)
        plan.add_ordering(b_on, a_on)
    return plan
