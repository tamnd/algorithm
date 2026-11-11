# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cigarette-smokers-problem/. The authors are listed in prov/JBBYWT.jsonl.

"""The cigarette smokers problem, as procsim models.

The agent is fixed (Patil): three agent processes share agentSem = 1, and
each one loops "P(agentSem); V(x); V(y)" for its own pair of the semaphores
tobacco, paper and match. Each agent also records which pair it offered, in
a step that does not synchronize, so that the tests can check that the right
smoker smoked.

Smoker solutions:
  naive    the smoker who has matches does P(tobacco); P(paper), and so on.
           Two smokers can each take one ingredient of the same offer, and
           then everyone waits.
  pushers  three pusher processes, one per ingredient, with a mutex and the
           flags isTobacco, isPaper, isMatch; the pusher that sees the second
           ingredient of an offer wakes the smoker who needs that pair
           (Downey's solution, with conditionals).
  indexed  no conditionals: each pusher adds the weight of its ingredient
           (tobacco 1, paper 2, match 4) to a shared sum t under a mutex and
           does V(S[t]); the smoker who needs a pair waits on S[sum of the
           pair]. This is in the style of Parnas (1975), who used arrays of
           semaphores and arithmetic in place of conditionals; it is not his
           exact program.
  simultaneous  each smoker does one P on its two semaphores at once (a
           primitive that Dijkstra's P and V do not have).

To make the model finite, the smoker who smokes the last of `rounds`
cigarettes does not give agentSem back, so a run that does not deadlock ends
with every process blocked and `smoked == rounds`.

Precondition: rounds >= 1. Cost: O(1) semaphore operations per cigarette.
"""

from typing import Iterator

from procsim import Sim

INGREDIENTS = ("tobacco", "paper", "match")
WEIGHT = {"tobacco": 1, "paper": 2, "match": 4}
# each smoker has one ingredient and needs the other two
NEEDS = {have: tuple(x for x in INGREDIENTS if x != have) for have in INGREDIENTS}


def _offered(pair: tuple):
    def f(s: Sim) -> None:
        s.v["offered"][pair] += 1
    return f


def agent(sim: Sim, me: str, pair: tuple) -> Iterator[tuple]:
    """Patil's agent: it may not be changed."""
    while True:
        yield ("P", "agentSem")
        yield ("atomic", _offered(pair))  # instrumentation only
        yield ("V", pair[0])
        yield ("V", pair[1])


def _smoke(have: str):
    def f(s: Sim) -> int:
        s.v["smoked_by"][have] += 1
        s.v["smoked"] += 1
        return s.v["smoked"]
    return f


def _finish(sim: Sim, have: str) -> Iterator[tuple]:
    n = yield ("atomic", _smoke(have))
    if n < sim.v["rounds"]:  # the stop rule of the model, not part of the protocol
        yield ("V", "agentSem")


def naive_smoker(sim: Sim, me: str, have: str) -> Iterator[tuple]:
    a, b = NEEDS[have]
    while True:
        yield ("P", a)
        yield ("P", b)
        yield from _finish(sim, have)


def _both(a: str, b: str):
    def ready(s: Sim) -> bool:
        return s.sems[a].count > 0 and s.sems[b].count > 0

    def take(s: Sim) -> None:
        s.sems[a].count -= 1
        s.sems[b].count -= 1
    return ready, take


def simultaneous_smoker(sim: Sim, me: str, have: str) -> Iterator[tuple]:
    """A P on two semaphores at once: wait until both are positive, then take both in one step."""
    ready, take = _both(*NEEDS[have])
    while True:
        yield ("when", ready, take)
        yield from _finish(sim, have)


def _flag(name: str, value: bool):
    def f(s: Sim) -> None:
        s.v[name] = value
    return f


def _get(name: str):
    def f(s: Sim):
        return s.v[name]
    return f


def pusher(sim: Sim, me: str, ingredient: str) -> Iterator[tuple]:
    """Wake the smoker who needs this ingredient and one seen before, or note it."""
    others = [x for x in INGREDIENTS if x != ingredient]
    while True:
        yield ("P", ingredient)
        yield ("P", "mutex")
        for other in others:
            if (yield ("atomic", _get("is_" + other))):
                yield ("atomic", _flag("is_" + other, False))
                (have,) = [x for x in INGREDIENTS if x not in (ingredient, other)]
                yield ("V", "smoker_" + have)
                break
        else:
            yield ("atomic", _flag("is_" + ingredient, True))
        yield ("V", "mutex")


def pusher_smoker(sim: Sim, me: str, have: str) -> Iterator[tuple]:
    while True:
        yield ("P", "smoker_" + have)
        yield from _finish(sim, have)


def _add_weight(w: int):
    def f(s: Sim) -> int:
        s.v["t"] += w
        return s.v["t"]
    return f


def _reset(s: Sim) -> None:
    s.v["t"] = 0


def indexed_pusher(sim: Sim, me: str, ingredient: str) -> Iterator[tuple]:
    """No conditional: the sum t names the semaphore to signal."""
    while True:
        yield ("P", ingredient)
        yield ("P", "mutex")
        t = yield ("atomic", _add_weight(WEIGHT[ingredient]))
        yield ("V", f"S{t}")
        yield ("V", "mutex")


def indexed_smoker(sim: Sim, me: str, have: str) -> Iterator[tuple]:
    a, b = NEEDS[have]
    while True:
        yield ("P", f"S{WEIGHT[a] + WEIGHT[b]}")
        yield ("atomic", _reset)
        yield from _finish(sim, have)


def build(kind: str, rounds: int) -> Sim:
    s = Sim()
    s.v.update(rounds=rounds, smoked=0, t=0, smoked_by={x: 0 for x in INGREDIENTS},
               offered={NEEDS[x]: 0 for x in INGREDIENTS})
    s.semaphore("agentSem", 1)
    for x in INGREDIENTS:
        s.semaphore(x, 0)
    for have in INGREDIENTS:
        s.spawn(f"agent_{have}", agent, NEEDS[have], daemon=True)
    if kind in ("naive", "simultaneous"):
        smoker = naive_smoker if kind == "naive" else simultaneous_smoker
        for have in INGREDIENTS:
            s.spawn(f"smoker_{have}", smoker, have, daemon=True)
    elif kind == "pushers":
        s.semaphore("mutex", 1)
        for x in INGREDIENTS:
            s.v["is_" + x] = False
            s.semaphore("smoker_" + x, 0)
            s.spawn(f"pusher_{x}", pusher, x, daemon=True)
        for have in INGREDIENTS:
            s.spawn(f"smoker_{have}", pusher_smoker, have, daemon=True)
    elif kind == "indexed":
        s.semaphore("mutex", 1)
        for t in range(1, 8):
            s.semaphore(f"S{t}", 0)
        for x in INGREDIENTS:
            s.spawn(f"pusher_{x}", indexed_pusher, x, daemon=True)
        for have in INGREDIENTS:
            s.spawn(f"smoker_{have}", indexed_smoker, have, daemon=True)
    else:
        raise ValueError(kind)
    return s


def all_smoked(s: Sim) -> bool:
    """The goal: `rounds` cigarettes, each by the smoker the agent's offer was for."""
    return s.v["smoked"] == s.v["rounds"] and all(
        s.v["smoked_by"][have] == s.v["offered"][NEEDS[have]] for have in INGREDIENTS)


def right_smoker(s: Sim):
    """Safety: no smoker has smoked more often than its pair was offered."""
    for have in INGREDIENTS:
        if s.v["smoked_by"][have] > s.v["offered"][NEEDS[have]]:
            return f"the smoker with {have} smoked without its offer"
    return None
