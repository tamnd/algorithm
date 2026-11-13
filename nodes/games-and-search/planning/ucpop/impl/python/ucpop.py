# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ucpop/. The authors are listed in prov/9M4E8C.jsonl.

"""UCPOP over ground actions with conditional effects and negative literals.

A literal is a pair (fact, sign). An action has a precondition, a set of
literals, and a list of effects. An effect has a condition, a set of
literals, an add list and a delete list. In a state s the action applies when
its precondition holds, and every effect whose condition holds in s fires:
the next state is s minus the union of the fired delete lists, plus the union
of the fired add lists. No action may add and delete the same fact.

The initial state is complete (the closed world assumption): START makes
(f, True) for f in the initial state and (f, False) for every other fact.

The planner keeps goals (literal, step) and causal links. A threat to a
link is resolved by demotion, promotion or confrontation; confrontation adds
the negation of one literal of the threatening effect's condition as a new
goal of the threatening step.
"""

from collections import deque
from itertools import product
from typing import Callable, Dict, FrozenSet, Hashable, Iterable, Iterator, List, NamedTuple, Optional, Sequence, Set, Tuple

Fact = Hashable
Literal = Tuple[Fact, bool]
State = FrozenSet[Fact]

START, FINISH = 0, 1


class Effect(NamedTuple):
    cond: FrozenSet[Literal]
    add: FrozenSet[Fact]
    delete: FrozenSet[Fact]


class Action(NamedTuple):
    name: str
    pre: FrozenSet[Literal]
    effects: Tuple[Effect, ...]


def negate(lit: Literal) -> Literal:
    return (lit[0], not lit[1])


def effect(cond: Iterable[Literal] = (), add: Iterable[Fact] = (), delete: Iterable[Fact] = ()) -> Effect:
    return Effect(frozenset(cond), frozenset(add), frozenset(delete))


def compatible(literals: Iterable[Literal]) -> bool:
    lits = set(literals)
    return not any(negate(l) in lits for l in lits)


def make_action(name: str, pre: Iterable[Literal] = (), effects: Iterable[Effect] = ()) -> Action:
    """Two effects that can fire together may not add and delete the same fact."""
    pre, effects = frozenset(pre), tuple(effects)
    for e1 in effects:
        for e2 in effects:
            if e1.add & e2.delete and compatible(pre | e1.cond | e2.cond):
                raise ValueError("two effects that can fire together add and delete the same fact")
    return Action(name, pre, effects)


def holds(state: State, literals: Iterable[Literal]) -> bool:
    return all((f in state) == sign for f, sign in literals)


def successor(state: State, action: Action) -> State:
    fired = [e for e in action.effects if holds(state, e.cond)]
    dels = set().union(*(e.delete for e in fired)) if fired else set()
    adds = set().union(*(e.add for e in fired)) if fired else set()
    return frozenset((state - dels) | adds)


def run_plan(state: State, plan: Sequence[Action]) -> Optional[State]:
    for action in plan:
        if not holds(state, action.pre):
            return None
        state = successor(state, action)
    return state


def is_plan(init: Iterable[Fact], goal: Iterable[Literal], plan: Sequence[Action]) -> bool:
    end = run_plan(frozenset(init), plan)
    return end is not None and holds(end, goal)


class Link(NamedTuple):
    producer: int
    effect: int
    lit: Literal
    consumer: int


class PartialPlan:
    def __init__(self, init: Iterable[Fact], goal: Iterable[Literal]) -> None:
        self.init = frozenset(init)
        self.steps: List[Action] = [make_action("START"), make_action("FINISH", goal)]
        self.after: Dict[int, Set[int]] = {START: {FINISH}, FINISH: set()}
        self.goals: Set[Tuple[Literal, int]] = {(lit, FINISH) for lit in goal}
        self.links: Set[Link] = set()

    def copy(self) -> "PartialPlan":
        other = PartialPlan.__new__(PartialPlan)
        other.init = self.init
        other.steps = list(self.steps)
        other.after = {i: set(s) for i, s in self.after.items()}
        other.goals = set(self.goals)
        other.links = set(self.links)
        return other

    def add_step(self, action: Action) -> int:
        i = len(self.steps)
        self.steps.append(action)
        self.after[i] = {FINISH}
        self.after[START].add(i)
        self.goals |= {(lit, i) for lit in action.pre}
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

    def makes(self, i: int, e: int, lit: Literal) -> bool:
        """Effect e of step i makes the literal true. START makes the initial state, closed world."""
        fact, sign = lit
        if i == START:
            return (fact in self.init) == sign
        eff = self.steps[i].effects[e]
        return fact in (eff.add if sign else eff.delete)

    def effect_ids(self, i: int) -> range:
        return range(1) if i == START else range(len(self.steps[i].effects))

    def cond(self, i: int, e: int) -> FrozenSet[Literal]:
        return frozenset() if i == START else self.steps[i].effects[e].cond

    def add_link(self, i: int, e: int, lit: Literal, j: int) -> bool:
        if not self.add_ordering(i, j):
            return False
        self.links.add(Link(i, e, lit, j))
        self.goals |= {(c, i) for c in self.cond(i, e)}
        return True

    def threats(self) -> List[Tuple[int, int, Link]]:
        """(k, e, link): effect e of step k makes the link's literal false, k may fall
        between the link's ends, and no goal of k yet blocks the condition of e."""
        found = []
        for link in sorted(self.links, key=repr):
            bad = negate(link.lit)
            for k in range(2, len(self.steps)):
                if k in (link.producer, link.consumer):
                    continue
                if self.precedes(k, link.producer) or self.precedes(link.consumer, k):
                    continue
                for e in self.effect_ids(k):
                    if self.makes(k, e, bad) and not any((negate(c), k) in self.goals for c in self.cond(k, e)):
                        found.append((k, e, link))
        return found

    def open_goals(self) -> List[Tuple[Literal, int]]:
        linked = {(link.lit, link.consumer) for link in self.links}
        return sorted((g for g in self.goals if g not in linked), key=repr)

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


Move = Tuple


def resolvers(plan: PartialPlan, flaw: Tuple, actions: Sequence[Action], bound: int,
              cut: Optional[List[bool]]) -> List[Move]:
    if flaw[0] == "threat":  # @line L9
        _, k, e, link = flaw
        moves: List[Move] = [("order", a, b) for a, b in ((k, link.producer), (link.consumer, k))  # @line L10
                             if a != b and not plan.precedes(b, a)]
        moves += [("goal", negate(c), k) for c in sorted(plan.cond(k, e), key=repr)]  # @line L11 (confrontation)
        return moves
    _, lit, j = flaw  # @line L12
    moves = [("link", i, e, lit, j) for i in range(len(plan.steps)) if i != j and not plan.precedes(j, i)  # @line L13
             for e in plan.effect_ids(i) if plan.makes(i, e, lit)]
    new = [("new", a, e, lit, j) for a in actions for e, eff in enumerate(a.effects)
           if lit[0] in (eff.add if lit[1] else eff.delete)]
    if len(plan.steps) - 2 < bound:
        moves += new  # @line L14
    elif new and cut is not None:
        cut[0] = True  # @line L15
    return moves


def apply(plan: PartialPlan, move: Move) -> PartialPlan:
    child = plan.copy()
    if move[0] == "order":
        child.add_ordering(move[1], move[2])
    elif move[0] == "goal":
        child.goals.add((move[1], move[2]))
    elif move[0] == "link":
        child.add_link(move[1], move[2], move[3], move[4])
    else:
        child.add_link(child.add_step(move[1]), move[2], move[3], move[4])
    return child


def refine(plan: PartialPlan, actions: Sequence[Action], bound: int,
           cut: Optional[List[bool]] = None) -> Iterator[PartialPlan]:
    """Every complete plan with at most bound steps; the flaw with the fewest resolvers first."""
    flaws = [("threat", k, e, link) for k, e, link in plan.threats()] + [("open", lit, j) for lit, j in plan.open_goals()]
    best: Optional[List[Move]] = None
    for flaw in flaws:
        moves = resolvers(plan, flaw, actions, bound, cut)
        if best is None or len(moves) < len(best):  # @line L8
            best = moves
            if not best:
                return  # @line L19 (a flaw with no resolver)
    if best is None:
        yield plan  # @line L7
        return
    for move in best:  # @line L16
        yield from refine(apply(plan, move), actions, bound, cut)  # @line L17 @line L18


def facts_of(init: Iterable[Fact], goal: Iterable[Literal], actions: Sequence[Action]) -> Set[Fact]:
    facts = set(init) | {f for f, _ in goal}
    for a in actions:
        facts |= {f for f, _ in a.pre}
        for e in a.effects:
            facts |= {f for f, _ in e.cond} | e.add | e.delete
    return facts


def ucpop(init: Iterable[Fact], goal: Iterable[Literal], actions: Sequence[Action],
          max_steps: Optional[int] = None) -> Optional[PartialPlan]:
    """A complete plan with the fewest steps, or None. Without max_steps the bound
    is 2^|F| - 1, and None means that no plan exists."""
    init, goal = frozenset(init), frozenset(goal)
    if not compatible(goal):
        return None                  # a goal that asks for f and not f
    if max_steps is None:
        max_steps = 2 ** len(facts_of(init, goal, actions)) - 1
    usable = [a for a in actions if compatible(a.pre)]
    for bound in range(max_steps + 1):  # @line L1
        cut = [False]  # @line L2
        for plan in refine(PartialPlan(init, goal), usable, bound, cut):  # @line L3
            return plan  # @line L4
        if not cut[0]:
            return None  # @line L5 (the bound removed nothing, so a larger bound gives the same tree)
    return None  # @line L6


class StripsAction(NamedTuple):
    name: str
    pre: FrozenSet[Literal]
    add: FrozenSet[Fact]
    delete: FrozenSet[Fact]


def compile_to_strips(actions: Sequence[Action]) -> List[StripsAction]:
    """One STRIPS action, with negative preconditions, for each way the effects can fire.
    An effect that does not fire needs one literal of its condition to be false; each
    literal gives its own case."""
    out = []
    for a in actions:
        options = []
        for e in a.effects:
            cases = [(True, e.cond)] + [(False, frozenset([negate(c)])) for c in sorted(e.cond, key=repr)]
            options.append(cases)
        for choice in product(*options):
            pre = set(a.pre)
            add, dele = set(), set()
            for (fires, extra), e in zip(choice, a.effects):
                pre |= extra
                if fires:
                    add |= e.add
                    dele |= e.delete
            if any((f, not s) in pre for f, s in pre):
                continue
            out.append(StripsAction(a.name, frozenset(pre), frozenset(add), frozenset(dele - add)))
    return out


def bfs_length(init: Iterable[Fact], goal: Iterable[Literal], actions: Sequence[StripsAction]) -> Optional[int]:
    """Breadth-first search on a STRIPS task with negative preconditions."""
    start = frozenset(init)
    dist = {start: 0}
    queue = deque([start])
    while queue:
        s = queue.popleft()
        if holds(s, goal):
            return dist[s]
        for a in actions:
            if holds(s, a.pre):
                t = (s - a.delete) | a.add
                if t not in dist:
                    dist[t] = dist[s] + 1
                    queue.append(t)
    return None


def briefcase() -> Tuple[State, FrozenSet[Literal], List[Action]]:
    """Pednault's briefcase: the paycheck must stay at home, the dictionary must go to the office."""
    objects, places = ("P", "D"), ("home", "office")
    acts = []
    for l1 in places:
        for l2 in places:
            if l1 != l2:
                effs = [effect([], [("at", "B", l2)], [("at", "B", l1)])]
                effs += [effect([(("in", x), True)], [("at", x, l2)], [("at", x, l1)]) for x in objects]
                acts.append(make_action(f"move-b({l1},{l2})", [(("at", "B", l1), True)], effs))
    for x in objects:
        acts.append(make_action(f"take-out({x})", [(("in", x), True)], [effect([], [], [("in", x)])]))
        for l in places:
            acts.append(make_action(f"put-in({x},{l})", [(("at", x, l), True), (("at", "B", l), True), (("in", x), False)],
                                    [effect([], [("in", x)], [])]))
    init = frozenset({("at", "B", "home"), ("at", "P", "home"), ("at", "D", "home"), ("in", "P")})
    goal = frozenset({(("at", "B", "office"), True), (("at", "D", "office"), True), (("at", "P", "home"), True)})
    return init, goal, acts
