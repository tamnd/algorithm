# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deadlock-prevention/. The authors are listed in prov/KAC40H.jsonl.

"""Three ways to break a Coffman condition, on one workload, in procsim.

The workload: three processes and three locks a, b, c. Process p needs
{a, b}, q needs {b, c}, and s needs {c, a}, each taking its first lock
before its second. Taken naively this can close the cycle p -> q -> s -> p.
Each build function returns a fresh Sim. Precondition: none. Cost: each
exhaustive search here visits at most a few hundred states.
"""

from typing import Callable, Iterator

from procsim import Sim

NEEDS = {"p": ("a", "b"), "q": ("b", "c"), "s": ("c", "a")}
RANK = {"a": 0, "b": 1, "c": 2}


def naive(sim: Sim, me: str, first: str, second: str) -> Iterator[tuple]:
    """Hold the first lock while waiting for the second: all four conditions can hold."""
    yield ("lock", first)
    yield ("lock", second)
    sim.emit("cs", me)
    yield ("unlock", second)
    yield ("unlock", first)


def one_shot(sim: Sim, me: str, first: str, second: str) -> Iterator[tuple]:
    """Breaks hold and wait: take both locks in one step, or wait holding none."""
    yield ("lock_all", [first, second])
    sim.emit("cs", me)
    yield ("unlock", second)
    yield ("unlock", first)


def release_and_retry(sim: Sim, me: str, first: str, second: str) -> Iterator[tuple]:
    """Breaks no preemption, in its voluntary form: if the second lock is busy, give up the first."""
    while True:
        yield ("lock", first)
        ok = yield ("trylock", second)
        if ok:
            break
        yield ("unlock", first)  # back off; a real program would wait a random time here
    sim.emit("cs", me)
    yield ("unlock", second)
    yield ("unlock", first)


def ordered(sim: Sim, me: str, first: str, second: str) -> Iterator[tuple]:
    """Breaks circular wait: take the locks in increasing rank."""
    lo, hi = sorted((first, second), key=RANK.__getitem__)
    yield ("lock", lo)
    yield ("lock", hi)
    sim.emit("cs", me)
    yield ("unlock", hi)
    yield ("unlock", lo)


def build(proc: Callable[..., Iterator[tuple]]) -> Sim:
    s = Sim()
    for m in "abc":
        s.mutex(m)
    for name, (x, y) in NEEDS.items():
        s.spawn(name, proc, x, y)
    return s


def has_cycle(g: dict[str, set[str]]) -> bool:
    """Depth-first search for a cycle in a small graph. Cost: O(V + E)."""
    state: dict[str, int] = {}

    def visit(v: str) -> bool:
        state[v] = 1
        for w in g.get(v, ()):
            if state.get(w) == 1 or (w not in state and visit(w)):
                return True
        state[v] = 2
        return False

    return any(v not in state and visit(v) for v in list(g))
