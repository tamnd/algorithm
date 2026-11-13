# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forward-state-space-search/. The authors are listed in prov/3SHV74.jsonl.

"""Forward state-space search (progression) for propositional STRIPS tasks.

A state is a frozenset of facts. An action applies in s when pre <= s, and the
next state is (s minus del) union add. The STRIPS core below is copied from the
strips page, not imported.
"""

import heapq
from collections import deque
from typing import Dict, FrozenSet, Hashable, Iterable, List, NamedTuple, Optional, Sequence, Tuple

Fact = Hashable
State = FrozenSet[Fact]


class Action(NamedTuple):
    name: str
    pre: FrozenSet[Fact]
    add: FrozenSet[Fact]
    delete: FrozenSet[Fact]
    cost: int = 1


def make_action(name: str, pre: Iterable[Fact] = (), add: Iterable[Fact] = (), delete: Iterable[Fact] = (), cost: int = 1) -> Action:
    return Action(name, frozenset(pre), frozenset(add), frozenset(delete), cost)


def successor(state: State, action: Action) -> State:
    return (state - action.delete) | action.add


def run_plan(state: State, plan: Sequence[Action]) -> Optional[State]:
    """Apply the plan from state. Return the final state, or None if an action is not applicable."""
    for a in plan:
        if not a.pre <= state:
            return None
        state = (state - a.delete) | a.add
    return state


def is_plan(init: Iterable[Fact], goal: Iterable[Fact], plan: Sequence[Action]) -> bool:
    final = run_plan(frozenset(init), plan)
    return final is not None and frozenset(goal) <= final


class Stats(NamedTuple):
    expanded: int
    generated: int
    reached: int


def _extract(parent: Dict[State, Optional[Tuple[State, Action]]], s: State) -> List[Action]:
    plan = []  # @line L13
    while parent[s] is not None:  # @line L14
        s, a = parent[s]  # @line L15
        plan.append(a)  # @line L16 (appended here, reversed below)
    plan.reverse()
    return plan  # @line L17


def forward_search(init: Iterable[Fact], goal: Iterable[Fact], actions: Sequence[Action],
                   strategy: str = "bfs") -> Tuple[Optional[List[Action]], Stats]:
    """Progression search from init until a state contains the goal.

    strategy "bfs" returns a plan with the fewest actions, "ucs" a plan of least
    total cost (costs must be nonnegative), and "dfs" some plan. All three keep a
    reached set, so each state is expanded at most once and the search stops on
    every finite task. Returns (plan or None, Stats).
    """
    init = frozenset(init)
    goal = frozenset(goal)
    parent: Dict[State, Optional[Tuple[State, Action]]] = {init: None}  # @line L1
    expanded = generated = 0
    if strategy == "ucs":
        best = {init: 0}
        tie = 0
        heap = [(0, tie, init)]
        done = set()
        while heap:
            g, _, s = heapq.heappop(heap)
            if s in done:
                continue
            done.add(s)
            if goal <= s:
                return _extract(parent, s), Stats(expanded, generated, len(best))
            expanded += 1
            for a in actions:
                if a.pre <= s:
                    t = (s - a.delete) | a.add
                    generated += 1
                    ng = g + a.cost
                    if t not in best or ng < best[t]:
                        best[t] = ng
                        parent[t] = (s, a)
                        tie += 1
                        heapq.heappush(heap, (ng, tie, t))
        return None, Stats(expanded, generated, len(best))
    if strategy not in ("bfs", "dfs"):
        raise ValueError("strategy must be bfs, dfs or ucs")
    frontier = deque([init])  # @line L2
    pop = frontier.popleft if strategy == "bfs" else frontier.pop
    while frontier:  # @line L3
        s = pop()  # @line L4
        if goal <= s:  # @line L5
            return _extract(parent, s), Stats(expanded, generated, len(parent))
        expanded += 1
        for a in actions:  # @line L6
            if a.pre <= s:  # @line L7
                t = (s - a.delete) | a.add  # @line L8
                generated += 1
                if t not in parent:  # @line L9
                    parent[t] = (s, a)  # @line L10
                    frontier.append(t)  # @line L11
    return None, Stats(expanded, generated, len(parent))  # @line L12


def reachable(init: Iterable[Fact], actions: Sequence[Action]) -> Dict[State, int]:
    """Reference: breadth first search over all reachable states, state -> fewest actions."""
    init = frozenset(init)
    dist = {init: 0}
    queue = deque([init])
    while queue:
        s = queue.popleft()
        for a in actions:
            if a.pre <= s:
                t = (s - a.delete) | a.add
                if t not in dist:
                    dist[t] = dist[s] + 1
                    queue.append(t)
    return dist


# Small tasks used on the page and in the tests.

def delivery_task():
    """One truck, one package, places A and B. The package must go from A to B."""
    acts = [
        make_action("drive(A,B)", ["tA"], ["tB"], ["tA"]),
        make_action("drive(B,A)", ["tB"], ["tA"], ["tB"]),
        make_action("load(A)", ["tA", "pA"], ["pT"], ["pA"]),
        make_action("load(B)", ["tB", "pB"], ["pT"], ["pB"]),
        make_action("unload(A)", ["tA", "pT"], ["pA"], ["pT"]),
        make_action("unload(B)", ["tB", "pT"], ["pB"], ["pT"]),
    ]
    return frozenset(["tA", "pA"]), frozenset(["pB"]), acts


def blocks_world_actions(blocks: Sequence[str]) -> List[Action]:
    """Blocks world with a hand: pickup, putdown, stack and unstack."""
    acts = []
    for x in blocks:
        acts.append(make_action(f"pickup({x})", [("clear", x), ("ontable", x), ("handempty",)], [("holding", x)], [("clear", x), ("ontable", x), ("handempty",)]))
        acts.append(make_action(f"putdown({x})", [("holding", x)], [("ontable", x), ("clear", x), ("handempty",)], [("holding", x)]))
        for y in blocks:
            if x != y:
                acts.append(make_action(f"stack({x},{y})", [("holding", x), ("clear", y)], [("on", x, y), ("clear", x), ("handempty",)], [("holding", x), ("clear", y)]))
                acts.append(make_action(f"unstack({x},{y})", [("on", x, y), ("clear", x), ("handempty",)], [("holding", x), ("clear", y)], [("on", x, y), ("clear", x), ("handempty",)]))
    return acts


def blocks_world_state(stacks: Sequence[Sequence[str]]) -> State:
    """Facts of an arrangement with an empty hand; each stack is listed from the bottom up."""
    facts = {("handempty",)}
    for st in stacks:
        if st:
            facts.add(("ontable", st[0]))
            for below, above in zip(st, st[1:]):
                facts.add(("on", above, below))
            facts.add(("clear", st[-1]))
    return frozenset(facts)
