# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/snlp/. The authors are listed in prov/K3AVD8.jsonl.

"""SNLP, the systematic nonlinear planner of McAllester and Rosenblitt, over
ground STRIPS actions.

It is partial-order planning with one change: a step threatens a causal link
(s, p, w) when it adds or deletes p, not only when it deletes p. Then the
complete plans that the search reaches have pairwise disjoint sets of
linearizations, and no partial plan is reached twice. The search is depth
first with a bound on the number of steps, and snlp() deepens the bound.
"""

from typing import Callable, Dict, FrozenSet, Hashable, Iterable, Iterator, List, NamedTuple, Optional, Sequence, Set, Tuple

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


class PartialPlan:
    """Steps, orderings (as successor sets) and causal links."""

    def __init__(self, init: Iterable[Fact], goal: Iterable[Fact], systematic: bool = True) -> None:
        self.steps: List[Action] = [make_action("START", add=init), make_action("FINISH", pre=goal)]
        self.after: Dict[int, Set[int]] = {START: {FINISH}, FINISH: set()}
        self.links: Set[Link] = set()
        self.systematic = systematic

    def copy(self) -> "PartialPlan":
        other = PartialPlan.__new__(PartialPlan)
        other.steps = list(self.steps)
        other.after = {i: set(s) for i, s in self.after.items()}
        other.links = set(self.links)
        other.systematic = self.systematic
        return other

    def add_step(self, action: Action) -> int:
        i = len(self.steps)
        self.steps.append(action)
        self.after[i] = {FINISH}
        self.after[START].add(i)
        return i

    def precedes(self, i: int, j: int) -> bool:
        seen, stack = {i}, [i]
        while stack:
            for k in self.after[stack.pop()]:
                if k == j:
                    return True
                if k not in seen:
                    seen.add(k)
                    stack.append(k)
        return False

    def add_ordering(self, i: int, j: int) -> bool:
        if i == j or self.precedes(j, i):
            return False
        self.after[i].add(j)
        return True

    def add_link(self, i: int, fact: Fact, j: int) -> bool:
        if not self.add_ordering(i, j):
            return False
        self.links.add(Link(i, fact, j))
        return True

    def touches(self, k: int, fact: Fact) -> bool:
        """SNLP: k threatens a link on fact if it adds or deletes it. POP: if it deletes it."""
        step = self.steps[k]
        return fact in step.delete or (self.systematic and fact in step.add)

    def threats(self) -> List[Tuple[int, Link]]:
        found = []
        for link in sorted(self.links, key=repr):
            for k in range(len(self.steps)):
                if (k != link.producer and k != link.consumer and self.touches(k, link.fact)
                        and not self.precedes(k, link.producer) and not self.precedes(link.consumer, k)):
                    found.append((k, link))
        return found

    def open_conditions(self) -> List[Tuple[Fact, int]]:
        linked = {(link.fact, link.consumer) for link in self.links}
        return [(p, j) for j, step in enumerate(self.steps) for p in sorted(step.pre, key=repr) if (p, j) not in linked]

    def linearizations(self) -> Iterator[Tuple[int, ...]]:
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

    def actions(self, order: Sequence[int]) -> List[Action]:
        return [self.steps[i] for i in order if i not in (START, FINISH)]

    def one_linearization(self) -> List[Action]:
        return self.actions(next(self.linearizations()))

    def labels(self) -> List[Hashable]:
        """The name of each step that does not depend on step numbers: FINISH, START,
        or the action with the sorted (fact, label of consumer) pairs of its links."""
        out_links: Dict[int, List[Tuple[Fact, int]]] = {i: [] for i in range(len(self.steps))}
        for link in self.links:
            out_links[link.producer].append((link.fact, link.consumer))
        memo: Dict[int, Hashable] = {START: ("START",), FINISH: ("FINISH",)}

        def label(i: int) -> Hashable:
            if i not in memo:
                memo[i] = (self.steps[i].name, tuple(sorted((repr(p), label(c)) for p, c in out_links[i])))
            return memo[i]

        return [label(i) for i in range(len(self.steps))]

    def canonical(self) -> Hashable:
        """The plan up to the renaming of its steps."""
        lab = self.labels()
        steps = tuple(sorted(lab, key=repr))
        orders = tuple(sorted(((lab[i], lab[j]) for i, s in self.after.items() for j in s), key=repr))
        links = tuple(sorted(((lab[l.producer], repr(l.fact), lab[l.consumer]) for l in self.links), key=repr))
        return steps, orders, links


def relaxed_reachable(init: State, actions: Sequence[Action]) -> State:
    reached = set(init)
    changed = True
    while changed:
        changed = False
        for a in actions:
            if a.pre <= reached and not a.add <= reached:
                reached |= a.add
                changed = True
    return frozenset(reached)


def useful_actions(init: State, actions: Sequence[Action]) -> List[Action]:
    reach = relaxed_reachable(init, actions)
    return [a for a in actions if a.pre <= reach and not a.add <= a.pre]


Move = Tuple


def resolvers(plan: PartialPlan, flaw: Tuple, actions: Sequence[Action], bound: int,
              cut: Optional[List[bool]] = None) -> List[Move]:
    if flaw[0] == "threat":  # @line L9 (the threat test is PartialPlan.touches)
        _, k, link = flaw
        return [("order", a, b) for a, b in ((k, link.producer), (link.consumer, k))  # @line L10
                if a != b and not plan.precedes(b, a)]
    _, p, j = flaw  # @line L11
    moves: List[Move] = [("link", i, p, j) for i, step in enumerate(plan.steps)  # @line L12
                         if p in step.add and i != j and not plan.precedes(j, i)]
    new = [("new", a, p, j) for a in actions if p in a.add]
    if len(plan.steps) - 2 < bound:
        moves += new  # @line L13
    elif new and cut is not None:
        cut[0] = True  # @line L14
    return moves


def apply(plan: PartialPlan, move: Move) -> PartialPlan:
    child = plan.copy()
    if move[0] == "order":
        child.add_ordering(move[1], move[2])
    elif move[0] == "link":
        child.add_link(move[1], move[2], move[3])
    else:
        child.add_link(child.add_step(move[1]), move[2], move[3])
    return child


def refine(plan: PartialPlan, actions: Sequence[Action], bound: int,
           visit: Optional[Callable[[PartialPlan], None]] = None,
           cut: Optional[List[bool]] = None) -> Iterator[PartialPlan]:
    """FIND-COMPLETION as a generator: every complete plan with at most bound steps."""
    if visit is not None:
        visit(plan)
    flaws = [("threat", k, link) for k, link in plan.threats()] + [("open", p, j) for p, j in plan.open_conditions()]
    best: Optional[List[Move]] = None
    for flaw in flaws:
        moves = resolvers(plan, flaw, actions, bound, cut)
        if best is None or len(moves) < len(best):  # @line L8
            best = moves
            if not best:
                return  # @line L18 (a flaw with no resolver)
    if best is None:
        yield plan  # @line L7
        return
    for move in best:  # @line L15
        yield from refine(apply(plan, move), actions, bound, visit, cut)  # @line L16 @line L17


def complete_plans(init: Iterable[Fact], goal: Iterable[Fact], actions: Sequence[Action], bound: int,
                   systematic: bool = True, visit: Optional[Callable[[PartialPlan], None]] = None) -> List[PartialPlan]:
    """All complete plans of one bounded search."""
    return list(refine(PartialPlan(init, goal, systematic), list(actions), bound, visit))


def snlp(init: Iterable[Fact], goal: Iterable[Fact], actions: Sequence[Action],
         max_steps: Optional[int] = None) -> Optional[PartialPlan]:
    """A complete plan with the fewest steps, or None. Without max_steps the bound
    is 2^|F| - 1, and None means that no plan exists."""
    init, goal = frozenset(init), frozenset(goal)
    useful = useful_actions(init, actions)
    if not goal <= relaxed_reachable(init, useful):
        return None
    if max_steps is None:
        facts = set(init) | set(goal)
        for a in actions:
            facts |= a.pre | a.add | a.delete
        max_steps = 2 ** len(facts) - 1
    for bound in range(max_steps + 1):  # @line L1
        cut = [False]  # @line L2
        for plan in refine(PartialPlan(init, goal), useful, bound, cut=cut):  # @line L3
            return plan  # @line L4
        if not cut[0]:
            return None  # @line L5 (the bound removed nothing, so a larger bound gives the same tree)
    return None  # @line L6


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
