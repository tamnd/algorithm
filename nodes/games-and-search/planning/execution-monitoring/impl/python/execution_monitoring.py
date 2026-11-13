# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/execution-monitoring/. The authors are listed in prov/SF0N1W.jsonl.

"""Execution monitoring of a STRIPS plan with the kernels of a triangle table.

An action is a tuple (name, pre, add, delete) of frozensets of facts. A state is a
frozenset of facts. The k-th kernel is the set of facts that must hold before step k
so that the rest of the plan, steps k to n - 1, can run and reach the goal. It is the
regression of the goal through the rest of the plan, or None if no state works.
"""

from typing import Callable, FrozenSet, List, Optional, Sequence, Tuple

Fact = str
State = FrozenSet[Fact]
Action = Tuple[str, FrozenSet[Fact], FrozenSet[Fact], FrozenSet[Fact]]


def act(name: str, pre, add, delete) -> Action:
    return (name, frozenset(pre), frozenset(add), frozenset(delete))


def applicable(s: State, a: Action) -> bool:
    return a[1] <= s


def apply(s: State, a: Action) -> State:
    return (s - a[3]) | a[2]


def regress(cond: Optional[State], a: Action) -> Optional[State]:
    """The weakest condition before a that gives cond after a, or None if none exists."""
    if cond is None:
        return None
    _, pre, add, delete = a
    rest = cond - add
    if rest & delete:
        return None
    return pre | rest


def kernels(plan: Sequence[Action], goal) -> List[Optional[State]]:
    """K[n] = goal, K[k] = regress(K[k + 1], plan[k])."""
    ks: List[Optional[State]] = [None] * (len(plan) + 1)
    ks[len(plan)] = frozenset(goal)
    for k in range(len(plan) - 1, -1, -1):
        ks[k] = regress(ks[k + 1], plan[k])
    return ks


def triangle_table(init: State, plan: Sequence[Action], goal):
    """The marked entries of the triangle table of Fikes, Hart and Nilsson.

    Row i (0 <= i <= n) holds the needs of step i (the goal for i = n). Column j holds the facts
    that come from step j - 1 (column 0 is the initial state). Entry (i, j) is the set of facts
    that row i needs, that column j supplies, and that no step from j to i - 1 adds again.
    The k-th kernel is the union of the entries in rows k to n and columns 0 to k."""
    n = len(plan)
    need = [plan[i][1] for i in range(n)] + [frozenset(goal)]
    table = {}
    for i in range(n + 1):
        for j in range(i + 1):
            later_adds = frozenset().union(*[plan[t][2] for t in range(j, i)])
            source = init if j == 0 else plan[j - 1][2]
            table[i, j] = (need[i] & source) - later_adds
    return table


def table_kernel(table, n: int, k: int) -> State:
    return frozenset().union(*[table[i, j] for i in range(k, n + 1) for j in range(k + 1)])


def choose_step(s: State, ks: Sequence[Optional[State]]) -> Optional[int]:
    """PLANEX: the largest k whose kernel holds in s, or None if no kernel holds."""
    for k in range(len(ks) - 1, -1, -1):
        if ks[k] is not None and ks[k] <= s:
            return k
    return None


def execute(init: State, plan: Sequence[Action], goal, world: Callable, limit: int = 100):
    """Run the plan under the kernel monitor.

    world(t, s, a) is the state after the agent does a in s at time t; it may differ from apply(s, a).
    Returns ("goal", trace) or ("replan", trace), where trace lists the steps that were run."""
    ks = kernels(plan, goal)
    s, trace = frozenset(init), []
    for t in range(limit):
        k = choose_step(s, ks)
        if k is None:
            return "replan", trace
        if k == len(plan):
            return "goal", trace
        trace.append(k)
        s = world(t, s, plan[k])
    return "limit", trace


def execute_naive(init: State, plan: Sequence[Action], goal, world: Callable):
    """Check only the precondition of the next step, and the goal at the end."""
    s, trace = frozenset(init), []
    for t, a in enumerate(plan):
        if not applicable(s, a):
            return "replan", trace
        trace.append(t)
        s = world(t, s, a)
    return ("goal" if frozenset(goal) <= s else "replan"), trace


def blocks_world(blocks: Sequence[str]):
    """The four STRIPS actions of the blocks world with one hand."""
    acts = []
    for x in blocks:
        acts.append(act(f"pickup {x}", {f"clear {x}", f"table {x}", "hand empty"}, {f"holding {x}"},
                        {f"clear {x}", f"table {x}", "hand empty"}))
        acts.append(act(f"putdown {x}", {f"holding {x}"}, {f"table {x}", f"clear {x}", "hand empty"},
                        {f"holding {x}"}))
        for y in blocks:
            if x != y:
                acts.append(act(f"stack {x} {y}", {f"holding {x}", f"clear {y}"},
                                {f"on {x} {y}", f"clear {x}", "hand empty"}, {f"holding {x}", f"clear {y}"}))
                acts.append(act(f"unstack {x} {y}", {f"on {x} {y}", f"clear {x}", "hand empty"},
                                {f"holding {x}", f"clear {y}"}, {f"on {x} {y}", f"clear {x}", "hand empty"}))
    return {a[0]: a for a in acts}
