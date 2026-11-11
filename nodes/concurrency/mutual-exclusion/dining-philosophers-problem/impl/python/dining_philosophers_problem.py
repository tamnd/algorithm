# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dining-philosophers-problem/. The authors are listed in prov/611KPX.jsonl.

"""Solutions of the dining philosophers problem, as procsim models.

Philosopher i (0 <= i < n) sits between fork i (its left) and fork (i + 1) mod n
(its right). Each fork is a mutex. A philosopher thinks, takes both forks, eats,
and puts the forks down, `rounds` times.

  "naive"       left then right; can deadlock
  "ordered"     lower numbered fork first (a lock order)
  "asymmetric"  even philosophers left first, odd ones right first
  "waiter"      a counting semaphore lets at most n - 1 philosophers sit down
  "dijkstra"    no forks: states thinking, hungry, eating, one mutex and one
                semaphore per philosopher (Dijkstra 1971)
  "polite"      left, then trylock right, else put the left down and retry;
                deterministic and symmetric, so a lock-step schedule starves all
  "free"        Lehmann and Rabin's free philosophers: pick a random first fork,
                wait for it, trylock the other, else put the first down and retry

Precondition: n >= 2 (n >= 3 for a real ring), rounds >= 1.
Cost: an exhaustive search at n = 3 with one round visits a few thousand states.
"""

import random
from typing import Iterator

from procsim import Sim

POLICIES = ("naive", "ordered", "asymmetric", "waiter", "dijkstra", "polite", "free")


def _fork(i: int) -> str:
    return f"fork{i}"


def _start_eating(i: int):
    def f(s: Sim) -> None:
        s.v["eating"][i] = True
        s.v["meals"][i] += 1
        s.emit("eat", i)
    return f


def _stop_eating(i: int):
    def f(s: Sim) -> None:
        s.v["eating"][i] = False
    return f


def _first_and_second(i: int, n: int, policy: str) -> tuple[int, int]:
    left, right = i, (i + 1) % n
    if policy == "ordered":
        return min(left, right), max(left, right)
    if policy == "asymmetric" and i % 2 == 1:
        return right, left
    return left, right


def fork_philosopher(sim: Sim, me: str, i: int, n: int, rounds: int, policy: str) -> Iterator[tuple]:
    """naive, ordered, asymmetric and waiter: take two forks with lock."""
    a, b = _first_and_second(i, n, policy)
    for _ in range(rounds):
        yield ("tick",)  # think
        if policy == "waiter":
            yield ("P", "seats")
        yield ("lock", _fork(a))
        yield ("lock", _fork(b))
        yield ("atomic", _start_eating(i))
        yield ("atomic", _stop_eating(i))
        yield ("unlock", _fork(b))
        yield ("unlock", _fork(a))
        if policy == "waiter":
            yield ("V", "seats")


def retry_philosopher(sim: Sim, me: str, i: int, n: int, rounds: int, policy: str,
                      seed: int = 0) -> Iterator[tuple]:
    """polite (always left first) and free (a random first fork, Lehmann and Rabin)."""
    rng = random.Random(seed)
    left, right = i, (i + 1) % n
    for _ in range(rounds):
        yield ("tick",)  # think
        while True:
            a, b = left, right
            if policy == "free" and rng.random() < 0.5:
                a, b = right, left
            yield ("lock", _fork(a))  # wait until the chosen fork is free, and take it
            ok = yield ("trylock", _fork(b))
            if ok:
                break
            yield ("unlock", _fork(a))
        yield ("atomic", _start_eating(i))
        yield ("atomic", _stop_eating(i))
        yield ("unlock", _fork(b))
        yield ("unlock", _fork(a))


def _test(s: Sim, k: int) -> None:
    """Dijkstra's test: let a hungry philosopher eat if neither neighbour eats."""
    n, st = s.v["n"], s.v["state"]
    if st[k] == "hungry" and st[(k - 1) % n] != "eating" and st[(k + 1) % n] != "eating":
        st[k] = "eating"
        s.sems[f"s{k}"].count += 1  # V(s[k]) on a weak semaphore


def dijkstra_philosopher(sim: Sim, me: str, i: int, n: int, rounds: int) -> Iterator[tuple]:
    def hungry(s: Sim) -> None:
        s.v["state"][i] = "hungry"
        _test(s, i)

    def done(s: Sim) -> None:
        s.v["state"][i] = "thinking"
        _test(s, (i - 1) % n)
        _test(s, (i + 1) % n)

    for _ in range(rounds):
        yield ("tick",)  # think
        yield ("P", "mutex")
        yield ("atomic", hungry)
        yield ("V", "mutex")
        yield ("P", f"s{i}")
        yield ("atomic", _start_eating(i))
        yield ("atomic", _stop_eating(i))
        yield ("P", "mutex")
        yield ("atomic", done)
        yield ("V", "mutex")


def build(n: int, policy: str, rounds: int = 1, seed: int = 0) -> Sim:
    assert policy in POLICIES and n >= 2 and rounds >= 1
    s = Sim()
    s.v["n"] = n
    s.v["eating"] = [False] * n
    s.v["meals"] = [0] * n
    for k in range(n):
        s.mutex(_fork(k))
    if policy == "waiter":
        s.semaphore("seats", n - 1)
    if policy == "dijkstra":
        s.v["state"] = ["thinking"] * n
        s.semaphore("mutex", 1)
        for k in range(n):
            s.semaphore(f"s{k}", 0)
    for k in range(n):
        name = f"p{k}"
        if policy == "dijkstra":
            s.spawn(name, dijkstra_philosopher, k, n, rounds)
        elif policy in ("polite", "free"):
            s.spawn(name, retry_philosopher, k, n, rounds, policy, seed * 1000 + k)
        else:
            s.spawn(name, fork_philosopher, k, n, rounds, policy)
    return s


def neighbours_never_eat_together(s: Sim):
    """The safety property: no two neighbours eat at the same time."""
    n, e = s.v["n"], s.v["eating"]
    for k in range(n):
        if e[k] and e[(k + 1) % n]:
            return f"p{k} and p{(k + 1) % n} eat together"
    return None
