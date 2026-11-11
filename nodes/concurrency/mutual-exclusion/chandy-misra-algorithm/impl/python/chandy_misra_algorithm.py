# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chandy-misra-algorithm/. The authors are listed in prov/0J7AS3.jsonl.

"""The Chandy and Misra (1984) hygienic solution of the dining philosophers, in procsim.

The conflict graph is any undirected graph on the philosophers p0, ..., p(n-1).
Each edge e = {u, v} carries one fork and one request token. A fork is clean
or dirty. Messages travel on the edges: one network process per edge (a
daemon) delivers the fork and the token, in any order and after any delay.
Each philosopher runs one enabled rule per step:

  L2 hungry   a thinking philosopher that wants another meal becomes hungry
  L3 request  hungry, holds the token for e but not the fork: send the token
  L4 release  holds the fork and the token for e, the fork is dirty, and it is
              not eating: clean the fork and send it
  L6 eat      hungry, holds every fork, and each fork it holds is clean or its
              token is not here: eat; all its forks become dirty
  L7 finish   an eating philosopher goes back to thinking

Precondition: the graph is simple and the philosophers are numbered; the start
puts each fork, dirty, at the lower numbered end and the token at the other
end, so that the precedence graph is acyclic. Cost: per meal, at most two
messages per edge at the philosopher; each rule check is O(d) for degree d.
"""

from typing import Callable, Iterator, Optional

from procsim import Sim


def _edge(a: int, b: int) -> str:
    return f"{min(a, b)}-{max(a, b)}"


def _here(s: Sim, kind: str, e: str, u: str) -> bool:
    """The fork or token of e is at u and not on its way."""
    return s.v[kind][e] == u and not s.v[kind + "_moving"][e]


def _rule(s: Sim, u: str) -> Optional[Callable[[Sim], None]]:
    """The first enabled rule of u, as a function that fires it, or None."""
    v = s.v
    st = v["state"][u]
    nb = v["nbrs"][u]
    if st == "eating":
        def finish(s: Sim) -> None:
            v["state"][u] = "thinking"  # @line L7
        return finish
    for e, w in nb:
        if _here(s, "fork", e, u) and v["dirty"][e] and _here(s, "token", e, u):  # @line L4
            def release(s: Sim, e: str = e, w: str = w) -> None:
                v["dirty"][e] = False
                v["fork"][e], v["fork_moving"][e] = w, True
            return release
    if st == "hungry":
        for e, w in nb:
            if _here(s, "token", e, u) and v["fork"][e] != u:  # @line L3
                def request(s: Sim, e: str = e, w: str = w) -> None:
                    v["token"][e], v["token_moving"][e] = w, True
                return request
        if all(_here(s, "fork", e, u) and (not v["dirty"][e] or not _here(s, "token", e, u))
               for e, _ in nb):  # @line L6
            def eat(s: Sim) -> None:
                v["state"][u] = "eating"
                v["meals"][u] += 1
                for e, _ in nb:
                    v["dirty"][e] = True
                s.emit("eat", u)
            return eat
    if st == "thinking" and v["meals"][u] < v["rounds"]:
        def hungry(s: Sim) -> None:
            v["state"][u] = "hungry"  # @line L2
        return hungry
    return None


def philosopher(sim: Sim, me: str) -> Iterator[tuple]:
    while True:
        yield ("when", lambda s: _rule(s, me) is not None, lambda s: _rule(s, me)(s))


def network(sim: Sim, me: str, e: str) -> Iterator[tuple]:
    """Delivers the fork or the token of edge e; a fork arrives clean."""
    def moving(s: Sim) -> bool:
        return s.v["fork_moving"][e] or s.v["token_moving"][e]

    def deliver(s: Sim) -> None:
        kind = "fork" if s.v["fork_moving"][e] else "token"
        s.v[kind + "_moving"][e] = False  # @line L5

    while True:
        yield ("when", moving, deliver)


def build(n: int, edges: list[tuple[int, int]], rounds: int = 1) -> Sim:
    s = Sim()
    v = s.v
    v["rounds"] = rounds
    v["state"] = {f"p{i}": "thinking" for i in range(n)}
    v["meals"] = {f"p{i}": 0 for i in range(n)}
    v["nbrs"] = {f"p{i}": [] for i in range(n)}
    for kind in ("fork", "fork_moving", "token", "token_moving", "dirty"):
        v[kind] = {}
    for a, b in edges:
        assert a != b
        lo, hi = min(a, b), max(a, b)
        e = _edge(a, b)
        v["fork"][e], v["dirty"][e], v["token"][e] = f"p{lo}", True, f"p{hi}"  # @line L1
        v["fork_moving"][e] = v["token_moving"][e] = False
        v["nbrs"][f"p{lo}"].append((e, f"p{hi}"))
        v["nbrs"][f"p{hi}"].append((e, f"p{lo}"))
    for i in range(n):
        s.spawn(f"p{i}", philosopher)
    for e in sorted(v["fork"]):
        s.spawn(f"net{e}", network, e, daemon=True)
    return s


def all_meals_eaten(s: Sim) -> bool:
    return all(m == s.v["rounds"] for m in s.v["meals"].values())


def precedence(s: Sim) -> dict[str, set[str]]:
    """u -> w when u has precedence over w: u holds the shared fork clean, or w holds
    it dirty. A fork on its way counts as held, clean, by the receiver."""
    g: dict[str, set[str]] = {u: set() for u in s.v["state"]}
    for e, holder in s.v["fork"].items():
        a, b = (f"p{x}" for x in e.split("-"))
        other = b if holder == a else a
        if s.v["dirty"][e]:
            g[other].add(holder)
        else:
            g[holder].add(other)
    return g
