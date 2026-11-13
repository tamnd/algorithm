# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/causal-link/. The authors are listed in prov/3AWZJ1.jsonl.

"""Causal links, threats and their resolution, in a partial-order plan over
ground STRIPS actions.

A causal link (i, p, j) records that step i produces the fact p for step j.
A step k threatens the link if k deletes p and some linearization places k
after i and before j. Demotion orders k before i; promotion orders k after j.
In the systematic variant (SNLP) a step that adds p also threatens the link.
"""

from typing import Dict, FrozenSet, Hashable, Iterable, Iterator, List, NamedTuple, Optional, Sequence, Set, Tuple

Fact = Hashable

START, FINISH = 0, 1


class Action(NamedTuple):
    name: str
    pre: FrozenSet[Fact]
    add: FrozenSet[Fact]
    delete: FrozenSet[Fact]


def make_action(name: str, pre: Iterable[Fact] = (), add: Iterable[Fact] = (), delete: Iterable[Fact] = ()) -> Action:
    return Action(name, frozenset(pre), frozenset(add), frozenset(delete))


class Link(NamedTuple):
    producer: int
    fact: Fact
    consumer: int


class Plan:
    def __init__(self, init: Iterable[Fact], goal: Iterable[Fact]) -> None:
        self.steps: List[Action] = [make_action("START", add=init), make_action("FINISH", pre=goal)]
        self.after: Dict[int, Set[int]] = {START: {FINISH}, FINISH: set()}
        self.links: Set[Link] = set()

    def copy(self) -> "Plan":
        other = Plan.__new__(Plan)
        other.steps = list(self.steps)
        other.after = {i: set(s) for i, s in self.after.items()}
        other.links = set(self.links)
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
        if fact not in self.steps[i].add or fact not in self.steps[j].pre:
            raise ValueError("a link needs a producer that adds the fact and a consumer that needs it")
        if not self.add_ordering(i, j):
            return False
        self.links.add(Link(i, fact, j))
        return True

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


def possibly_between(plan: Plan, k: int, link: Link) -> bool:
    """Some linearization puts k after the producer and before the consumer."""
    return k not in (link.producer, link.consumer) and not plan.precedes(k, link.producer) and not plan.precedes(link.consumer, k)


def touches(step: Action, fact: Fact, systematic: bool) -> bool:
    return fact in step.delete or (systematic and fact in step.add)


def threats(plan: Plan, systematic: bool = False) -> List[Tuple[int, Link]]:
    return [(k, link) for link in sorted(plan.links, key=repr) for k, step in enumerate(plan.steps)
            if touches(step, link.fact, systematic) and possibly_between(plan, k, link)]


def resolutions(plan: Plan, k: int, link: Link) -> List[Plan]:
    """Demotion (k before the producer) and promotion (k after the consumer), when consistent."""
    out = []
    for i, j in ((k, link.producer), (link.consumer, k)):
        child = plan.copy()
        if child.add_ordering(i, j):
            out.append(child)
    return out


def protected(plan: Plan, order: Sequence[int], link: Link, systematic: bool = False) -> bool:
    """In this linearization no step between the ends of the link touches its fact."""
    i, j = order.index(link.producer), order.index(link.consumer)
    return not any(touches(plan.steps[k], link.fact, systematic) for k in order[i + 1:j])


def valid(plan: Plan, order: Sequence[int]) -> bool:
    state = frozenset()
    for k in order:
        step = plan.steps[k]
        if not step.pre <= state:
            return False
        state = (state - step.delete) | step.add
    return True
