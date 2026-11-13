# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tweak/. The authors are listed in prov/SW1BEM.jsonl.

"""Chapman's TWEAK: a partial-order planner with variables, built on the modal
truth criterion (MTC) for necessary truth.

A term is a constant or a variable; a variable is a string that starts with
"?". A proposition is a tuple (predicate, term, ...). A step asserts its add
list and denies its delete list. The plan holds the steps, ordering
constraints, codesignation constraints (a union-find over terms in which two
different constants never meet) and noncodesignation constraints.

The truth that the MTC decides is truth under projection: the effects of the
steps are applied in order, whether or not their preconditions hold. Chapman's
representation has infinitely many constants, so two variables are always
free to differ unless a constraint says otherwise.
"""

from collections import deque
from itertools import product
from typing import Dict, FrozenSet, Hashable, Iterable, Iterator, List, NamedTuple, Optional, Sequence, Set, Tuple

Term = str
Prop = Tuple[str, ...]

START, FINISH = 0, 1


def is_var(t: Term) -> bool:
    return t.startswith("?")


class Bindings:
    """Codesignation as a union-find; noncodesignation as pairs of terms."""

    def __init__(self) -> None:
        self.parent: Dict[Term, Term] = {}
        self.neq: Set[FrozenSet[Term]] = set()

    def copy(self) -> "Bindings":
        b = Bindings()
        b.parent = dict(self.parent)
        b.neq = set(self.neq)
        return b

    def find(self, t: Term) -> Term:
        while self.parent.get(t, t) != t:
            t = self.parent[t]
        return t

    def same(self, a: Term, b: Term) -> bool:
        return self.find(a) == self.find(b)

    def value(self, t: Term) -> Optional[Term]:
        """The constant that t is bound to, if any. A constant is the root of its class."""
        r = self.find(t)
        return None if is_var(r) else r

    def unify(self, a: Term, b: Term) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return True
        if not is_var(ra) and not is_var(rb):
            return False
        if not is_var(ra):
            ra, rb = rb, ra
        self.parent[ra] = rb          # a constant stays the root
        return all(not self.same(*pair) for pair in map(tuple, self.neq))

    def separate(self, a: Term, b: Term) -> bool:
        if self.same(a, b):
            return False
        self.neq.add(frozenset((a, b)))
        return True

    def unify_props(self, p: Prop, q: Prop) -> bool:
        if p[0] != q[0] or len(p) != len(q):
            return False
        return all(self.unify(x, y) for x, y in zip(p[1:], q[1:]))

    def necessarily_equal(self, p: Prop, q: Prop) -> bool:
        return p[0] == q[0] and len(p) == len(q) and all(self.same(x, y) for x, y in zip(p[1:], q[1:]))

    def possibly_equal(self, p: Prop, q: Prop) -> bool:
        return self.copy().unify_props(p, q)

    def with_equal(self, p: Prop, q: Prop) -> Optional["Bindings"]:
        b = self.copy()
        return b if b.unify_props(p, q) else None


class Step(NamedTuple):
    name: Tuple[str, ...]
    pre: Tuple[Prop, ...]
    add: Tuple[Prop, ...]
    delete: Tuple[Prop, ...]


class Schema(NamedTuple):
    """An operator with parameters; neq lists pairs of terms that must differ."""
    name: str
    params: Tuple[Term, ...]
    pre: Tuple[Prop, ...]
    add: Tuple[Prop, ...]
    delete: Tuple[Prop, ...]
    neq: Tuple[Tuple[Term, Term], ...] = ()


class Plan:
    def __init__(self, init: Iterable[Prop], goal: Iterable[Prop]) -> None:
        self.steps: List[Step] = [Step(("START",), (), tuple(init), ()), Step(("FINISH",), tuple(goal), (), ())]
        self.after: Dict[int, Set[int]] = {START: {FINISH}, FINISH: set()}
        self.b = Bindings()

    def copy(self) -> "Plan":
        other = Plan.__new__(Plan)
        other.steps = list(self.steps)
        other.after = {i: set(s) for i, s in self.after.items()}
        other.b = self.b.copy()
        return other

    def add_step(self, step: Step) -> int:
        i = len(self.steps)
        self.steps.append(step)
        self.after[i] = {FINISH}
        self.after[START].add(i)
        return i

    def instantiate(self, schema: Schema) -> Optional[int]:
        """Add a step of the schema with fresh variables, or None if its constraints fail."""
        k = len(self.steps)
        ren = {v: f"{v}_{k}" for v in schema.params}
        sub = lambda props: tuple((p[0],) + tuple(ren.get(t, t) for t in p[1:]) for p in props)
        step = Step((schema.name,) + tuple(ren[v] for v in schema.params), sub(schema.pre), sub(schema.add), sub(schema.delete))
        for x, y in schema.neq:
            if not self.b.separate(ren.get(x, x), ren.get(y, y)):
                return None
        return self.add_step(step)

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

    def possibly_before(self, c: int, s: int) -> bool:
        return c != s and not self.precedes(s, c)

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


def white_knight(plan: Plan, c: int, s: int, p: Prop, q: Prop) -> bool:
    """A step W necessarily between c and s asserts some r with r = p whenever p = q."""
    b2 = plan.b.with_equal(p, q)
    if b2 is None:
        return True
    return any(plan.precedes(c, w) and plan.precedes(w, s) and any(b2.necessarily_equal(r, p) for r in plan.steps[w].add)
               for w in range(len(plan.steps)))


def necessarily_true(plan: Plan, s: int, p: Prop) -> bool:
    """Chapman's modal truth criterion for necessary truth of p just before step s."""
    if not any(plan.precedes(t, s) and any(plan.b.necessarily_equal(q, p) for q in plan.steps[t].add)
               for t in range(len(plan.steps))):
        return False
    for c in range(len(plan.steps)):
        if not plan.possibly_before(c, s):
            continue
        for q in plan.steps[c].delete:
            if plan.b.possibly_equal(q, p) and not white_knight(plan, c, s, p, q):
                return False
    return True


# The brute force reference for the criterion.

def completions(plan: Plan, extra: Iterable[Prop] = ()) -> Iterator[Tuple[Tuple[int, ...], Dict[Term, Term]]]:
    """Every linearization with every binding of the variables that meets the constraints.
    The values are the constants of the plan plus one fresh constant per variable, which
    covers every pattern of equalities that an infinite set of constants allows."""
    terms = set()
    for st in plan.steps:
        for p in st.pre + st.add + st.delete:
            terms |= set(p[1:])
    for p in extra:
        terms |= set(p[1:])
    terms |= {t for pair in plan.b.neq for t in pair} | set(plan.b.parent) | set(plan.b.parent.values())
    variables = sorted(t for t in terms if is_var(t))
    constants = sorted(t for t in terms if not is_var(t)) + [f"#{i}" for i in range(len(variables))]
    orders = list(plan.linearizations())
    for values in product(constants, repeat=len(variables)):
        env = dict(zip(variables, values))
        val = lambda t: env.get(t, t)
        if any(val(t) != val(plan.b.find(t)) for t in terms):
            continue
        if any(val(x) == val(y) for x, y in map(tuple, plan.b.neq)):
            continue
        for order in orders:
            yield order, env


def ground(p: Prop, env: Dict[Term, Term]) -> Prop:
    return (p[0],) + tuple(env.get(t, t) for t in p[1:])


def projected_state(plan: Plan, order: Sequence[int], s: int, env: Dict[Term, Term]) -> Set[Prop]:
    state: Set[Prop] = set()
    for i in order:
        if i == s:
            break
        st = plan.steps[i]
        state -= {ground(q, env) for q in st.delete}
        state |= {ground(q, env) for q in st.add}
    return state


def brute_necessarily_true(plan: Plan, s: int, p: Prop) -> bool:
    return all(ground(p, env) in projected_state(plan, order, s, env) for order, env in completions(plan, [p]))


# The planner.

def establishers(plan: Plan, s: int, p: Prop, schemas: Sequence[Schema], bound: int, cut: Optional[List[bool]]) -> List[Tuple[Plan, int, Prop]]:
    out = []
    for t in range(len(plan.steps)):
        if t != s and not plan.precedes(s, t):
            for q in plan.steps[t].add:
                child = plan.copy()
                if child.add_ordering(t, s) and child.b.unify_props(q, p):
                    out.append((child, t, q))  # @line L9
    if len(plan.steps) - 2 < bound:
        for schema in schemas:  # @line L10
            for q in schema.add:
                if q[0] != p[0] or len(q) != len(p):
                    continue
                child = plan.copy()
                t = child.instantiate(schema)
                if t is None:
                    continue
                q2 = child.steps[t].add[schema.add.index(q)]
                if child.add_ordering(t, s) and child.b.unify_props(q2, p):
                    out.append((child, t, q2))
    elif cut is not None and any(q[0] == p[0] for schema in schemas for q in schema.add):
        cut[0] = True  # @line L11
    return out


def declobber(plan: Plan, t: int, s: int, p: Prop) -> Iterator[Plan]:
    """Make every possible clobberer between t and s harmless: demotion before t,
    promotion after s, separation of one argument, or an existing white knight."""
    for c in range(len(plan.steps)):
        if c in (t, s) or not plan.possibly_before(c, s) or plan.precedes(c, t):
            continue
        for q in plan.steps[c].delete:
            if not plan.b.possibly_equal(q, p) or white_knight(plan, c, s, p, q):
                continue
            options = []  # @line L18 (c is a clobberer with no white knight)
            child = plan.copy()
            if child.add_ordering(c, t):
                options.append(child)
            child = plan.copy()
            if child.add_ordering(s, c):
                options.append(child)
            for x, y in zip(q[1:], p[1:]):
                child = plan.copy()
                if child.b.separate(x, y):
                    options.append(child)
            for w in range(len(plan.steps)):
                if w in (c, s):
                    continue
                for r in plan.steps[w].add:
                    child = plan.copy()
                    if child.add_ordering(c, w) and child.add_ordering(w, s) and child.b.unify_props(r, p):
                        options.append(child)  # @line L19
            for child in options:
                yield from declobber(child, t, s, p)  # @line L20
            return
    yield plan  # @line L17


def first_goal(plan: Plan) -> Optional[Tuple[int, Prop]]:
    for s in range(len(plan.steps)):
        for p in plan.steps[s].pre:
            if not necessarily_true(plan, s, p):
                return s, p
    return None


def refine(plan: Plan, schemas: Sequence[Schema], bound: int, cut: Optional[List[bool]] = None) -> Iterator[Plan]:
    goal = first_goal(plan)
    if goal is None:
        yield plan  # @line L7
        return
    s, p = goal  # @line L8
    for child, t, _ in establishers(plan, s, p, schemas, bound, cut):  # @line L12
        for done in declobber(child, t, s, p):  # @line L13
            yield from refine(done, schemas, bound, cut)  # @line L14 @line L15
    # @line L16 (every choice failed)


def tweak(init: Iterable[Prop], goal: Iterable[Prop], schemas: Sequence[Schema], max_steps: int) -> Optional[Plan]:
    """A plan with the fewest steps whose every completion is a solution, or None."""
    for bound in range(max_steps + 1):  # @line L1
        cut = [False]  # @line L2
        for plan in refine(Plan(init, goal), schemas, bound, cut):  # @line L3
            return plan  # @line L4
        if not cut[0]:
            return None  # @line L5 (the bound removed nothing, so a larger bound gives the same tree)
    return None  # @line L6


def solution(plan: Plan) -> List[Tuple[str, ...]]:
    """One completion: the first linearization, with each variable replaced by its constant."""
    order = next(plan.linearizations())
    out = []
    for i in order:
        if i in (START, FINISH):
            continue
        name = plan.steps[i].name
        out.append((name[0],) + tuple(plan.b.value(t) or t for t in name[1:]))
    return out


# Ground semantics for checking plans.

def ground_actions(schemas: Sequence[Schema], constants: Sequence[Term]) -> List[Tuple[Tuple[str, ...], FrozenSet[Prop], FrozenSet[Prop], FrozenSet[Prop]]]:
    out = []
    for schema in schemas:
        for values in product(constants, repeat=len(schema.params)):
            env = dict(zip(schema.params, values))
            if any(env.get(x, x) == env.get(y, y) for x, y in schema.neq):
                continue
            g = lambda props: frozenset(ground(p, env) for p in props)
            out.append(((schema.name,) + values, g(schema.pre), g(schema.add), g(schema.delete)))
    return out


def run(init: Iterable[Prop], actions, names: Sequence[Tuple[str, ...]]) -> Optional[FrozenSet[Prop]]:
    table = {a[0]: a for a in actions}
    state = frozenset(init)
    for n in names:
        _, pre, add, dele = table[n]
        if not pre <= state:
            return None
        state = (state - dele) | add
    return state


def bfs_length(init: Iterable[Prop], goal: Iterable[Prop], actions) -> Optional[int]:
    start, goal = frozenset(init), frozenset(goal)
    dist = {start: 0}
    queue = deque([start])
    while queue:
        s = queue.popleft()
        if goal <= s:
            return dist[s]
        for _, pre, add, dele in actions:
            if pre <= s:
                t = (s - dele) | add
                if t not in dist:
                    dist[t] = dist[s] + 1
                    queue.append(t)
    return None


def blocks_schemas() -> List[Schema]:
    """The lifted blocks world with one move operator and a table that is always clear."""
    return [
        Schema("move-to-table", ("?b", "?x"), (("on", "?b", "?x"), ("clear", "?b"), ("block", "?x")),
               (("ontable", "?b"), ("clear", "?x")), (("on", "?b", "?x"),), (("?b", "?x"),)),
        Schema("move-from-table", ("?b", "?y"), (("ontable", "?b"), ("clear", "?b"), ("clear", "?y")),
               (("on", "?b", "?y"),), (("ontable", "?b"), ("clear", "?y")), (("?b", "?y"),)),
        Schema("move", ("?b", "?x", "?y"), (("on", "?b", "?x"), ("clear", "?b"), ("clear", "?y"), ("block", "?x")),
               (("on", "?b", "?y"), ("clear", "?x")), (("on", "?b", "?x"), ("clear", "?y")),
               (("?b", "?x"), ("?b", "?y"), ("?x", "?y"))),
    ]


SUSSMAN_INIT = (("on", "c", "a"), ("ontable", "a"), ("ontable", "b"), ("clear", "c"), ("clear", "b"),
                ("block", "a"), ("block", "b"), ("block", "c"))
SUSSMAN_GOAL = (("on", "a", "b"), ("on", "b", "c"))
