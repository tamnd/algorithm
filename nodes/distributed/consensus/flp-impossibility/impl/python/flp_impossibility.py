# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flp-impossibility/. The authors are listed in prov/1ADEFK.jsonl.

"""A small explorer for the FLP setting.

The model is the asynchronous message system of Fischer, Lynch and Paterson,
made finite: n processes, binary inputs, one broadcast of the input by each
process, and any order of events. An event is one of:

  ("send", p)          p puts the next message of its broadcast on the network;
  ("recv", m)          the message m = (dest, src, value) reaches dest;
  ("crash", p)         p stops for ever (at most one crash in a run).

Each send of a broadcast is its own event, so a crash can fall between two
sends of one broadcast. A protocol is a rule decide(p, own, got, n) that maps
the input of p and the values that p has received to a decision or None.

The explorer searches every schedule. It can find a run that breaks agreement,
or a run with one crash that stops with a correct process undecided. Code can
only do this for one protocol and a small n. It cannot prove the FLP theorem,
which is about every protocol; the proof on the page does that.
"""

from collections import deque
from typing import Callable, Optional

Rule = Callable[[int, int, dict[int, int], int], Optional[int]]
# A process state is (input, sends left, received values, decision).
State = tuple[int, tuple[int, ...], tuple[tuple[int, int], ...], Optional[int]]
Config = tuple[tuple[State, ...], tuple[tuple[int, int, int], ...], frozenset[int]]
Event = tuple


def majority_of_some(p: int, own: int, got: dict[int, int], n: int) -> Optional[int]:
    """Protocol A: wait for n - 1 values (own included), decide the majority, ties to 0."""
    vals = [own, *got.values()]
    if len(vals) < n - 1:
        return None
    return 1 if 2 * sum(vals) > len(vals) else 0


def majority_of_all(p: int, own: int, got: dict[int, int], n: int) -> Optional[int]:
    """Protocol B: wait for all n values, decide the majority, ties to 0."""
    vals = [own, *got.values()]
    if len(vals) < n:
        return None
    return 1 if 2 * sum(vals) > len(vals) else 0


def follow_p0(p: int, own: int, got: dict[int, int], n: int) -> Optional[int]:
    """Protocol C: p0 decides its own input, the others wait for the value of p0."""
    if p == 0:
        return own
    return got.get(0)


def initial(inputs: tuple[int, ...]) -> Config:
    n = len(inputs)
    states = tuple((v, tuple(q for q in range(n) if q != p), (), None) for p, v in enumerate(inputs))
    return (states, (), frozenset())


def _with_state(states: tuple[State, ...], p: int, s: State) -> tuple[State, ...]:
    return states[:p] + (s,) + states[p + 1 :]


def _decide(rule: Rule, p: int, s: State, n: int) -> State:
    v, out, got, d = s
    if d is None:
        d = rule(p, v, dict(got), n)
    return (v, out, got, d)


def events(c: Config, max_crashes: int = 1) -> list[Event]:
    states, net, crashed = c
    ev: list[Event] = []
    for p, s in enumerate(states):
        if p not in crashed and s[1]:
            ev.append(("send", p))
    for m in sorted(set(net)):
        if m[0] not in crashed:
            ev.append(("recv", m))
    if len(crashed) < max_crashes:
        ev.extend(("crash", p) for p in range(len(states)) if p not in crashed)
    return ev


def step(c: Config, e: Event, rule: Rule) -> Config:
    states, net, crashed = c
    n = len(states)
    if e[0] == "crash":
        return (states, net, crashed | {e[1]})
    if e[0] == "send":
        p = e[1]
        v, out, got, d = states[p]
        msg = (out[0], p, v)
        s = _decide(rule, p, (v, out[1:], got, d), n)
        return (_with_state(states, p, s), tuple(sorted(net + (msg,))), crashed)
    dest, src, val = e[1]
    lst = list(net)
    lst.remove(e[1])
    v, out, got, d = states[dest]
    s = _decide(rule, dest, (v, out, tuple(sorted(got + ((src, val),))), d), n)
    return (_with_state(states, dest, s), tuple(lst), crashed)


def decisions(c: Config) -> set[int]:
    """The values decided by any process, also by one that crashed later."""
    return {s[3] for s in c[0] if s[3] is not None}


def blocked(c: Config) -> bool:
    """No send or delivery is left for a live process, and a live process is undecided."""
    states, net, crashed = c
    live = [p for p in range(len(states)) if p not in crashed]
    if any(states[p][1] for p in live) or any(m[0] not in crashed for m in net):
        return False
    return any(states[p][3] is None for p in live)


def search(inputs: tuple[int, ...], rule: Rule, max_crashes: int = 1) -> Optional[tuple[str, list[Event]]]:
    """Breadth-first search over all schedules from one initial configuration.

    Returns ("agreement", events) for a shortest run where two processes decide
    differently, else ("blocked", events) for a shortest run that ends with no
    work left and a correct process undecided, else None.
    """
    start = initial(inputs)
    parent: dict[Config, tuple[Optional[Config], Optional[Event]]] = {start: (None, None)}
    queue = deque([start])
    found_block: Optional[Config] = None
    while queue:
        c = queue.popleft()
        if len(decisions(c)) > 1:
            return ("agreement", _path(parent, c))
        if found_block is None and blocked(c):
            found_block = c
        for e in events(c, max_crashes):
            d = step(c, e, rule)
            if d not in parent:
                parent[d] = (c, e)
                queue.append(d)
    if found_block is not None:
        return ("blocked", _path(parent, found_block))
    return None


def _path(parent: dict, c: Config) -> list[Event]:
    out = []
    while parent[c][0] is not None:
        c, e = parent[c]
        out.append(e)
    return out[::-1]


def replay(inputs: tuple[int, ...], rule: Rule, evs: list[Event], max_crashes: int = 1) -> Config:
    c = initial(inputs)
    for e in evs:
        assert e in events(c, max_crashes), e
        c = step(c, e, rule)
    return c


def reachable(inputs: tuple[int, ...], rule: Rule, max_crashes: int = 1) -> set[Config]:
    seen = {initial(inputs)}
    stack = [initial(inputs)]
    while stack:
        c = stack.pop()
        for e in events(c, max_crashes):
            d = step(c, e, rule)
            if d not in seen:
                seen.add(d)
                stack.append(d)
    return seen


def valence(c: Config, rule: Rule, silent: Optional[int] = None) -> set[int]:
    """The decision values reachable from c with no crash. If silent is set,
    that process takes no step, as if it had crashed or were very slow."""
    seen = {c}
    stack = [c]
    vals: set[int] = set()
    while stack:
        x = stack.pop()
        vals |= decisions(x)
        for e in events(x, 0):
            if silent is not None and (e == ("send", silent) or (e[0] == "recv" and e[1][0] == silent)):
                continue
            y = step(x, e, rule)
            if y not in seen:
                seen.add(y)
                stack.append(y)
    return vals


def lemma2(n: int, rule: Rule) -> tuple[str, int]:
    """The dichotomy behind Lemma 2 of FLP on the chain I_0, ..., I_n, where I_j
    gives input 1 to p_0, ..., p_{j-1}. Returns ("bivalent", j) if I_j is
    bivalent. Otherwise it finds j with I_{j-1} 0-valent and I_j 1-valent, and
    returns ("silent-run-undecided", p) where p = p_{j-1} is the one process
    whose input differs: no run in which p takes no step decides anything."""
    chain = [initial(tuple(1 if i < j else 0 for i in range(n))) for j in range(n + 1)]
    vals = [valence(c, rule) for c in chain]
    for j, v in enumerate(vals):
        if v == {0, 1}:
            return ("bivalent", j)
    for j in range(1, n + 1):
        if vals[j - 1] != vals[j]:
            p = j - 1
            silent0 = valence(chain[j - 1], rule, silent=p)
            silent1 = valence(chain[j], rule, silent=p)
            # The two silent runs are the same for every process but p.
            assert silent0 == silent1
            assert not silent0, "a deciding silent run would make one end bivalent"
            return ("silent-run-undecided", p)
    raise AssertionError("validity fails: I_0 and I_n have the same valence")
