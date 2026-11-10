# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/consensus-round-lower-bound/. The authors are listed in prov/72GMWX.jsonl.

"""The chain of executions behind the f + 1 round lower bound.

Model: n processes, synchronous lock-step rounds, crash failures, a complete
network. A protocol that runs R rounds is given in full-information form: in
each round each live process sends its whole view, and after round R each
live process decides by a rule decide(p, view). Every deterministic R-round
protocol is a full-information protocol with some rule, so this loses nothing.

An execution is (inputs, crashes). crashes maps a process to (r, S): it
crashes in round r, its round-r message reaches only S, and it sends nothing
later and does not decide.

build_chain(n, R) returns a list of executions from all inputs 0 to all
inputs 1, with no failures at both ends, such that:
  * each execution has at most one crash in each round, so at most R crashes;
  * in each adjacent pair, some process that is live in both has the same
    final view in both, and so decides the same value in both.
If R <= f, every execution of the chain is allowed, and the chain shows that
any R-round rule breaks agreement or validity in one of them. Code can only
check this for small cases; the proof on the page covers all cases.
"""

from typing import Callable, Hashable

Crash = tuple[int, frozenset[int]]
Execution = tuple[tuple[int, ...], tuple[tuple[int, Crash], ...]]


def make(inputs: tuple[int, ...], crashes: dict[int, Crash]) -> Execution:
    """A hashable execution."""
    return (tuple(inputs), tuple(sorted(crashes.items())))


def crash_map(e: Execution) -> dict[int, Crash]:
    return dict(e[1])


def final_views(e: Execution, rounds: int) -> dict[int, Hashable]:
    """The view after the last round of each process that does not crash."""
    inputs, crashes = e[0], crash_map(e)
    n = len(inputs)
    view: list[Hashable] = [(v,) for v in inputs]
    for r in range(1, rounds + 1):
        inbox: list[list[Hashable]] = [[None] * n for _ in range(n)]
        for p in range(n):
            if p in crashes and crashes[p][0] < r:
                continue
            targets = crashes[p][1] if p in crashes and crashes[p][0] == r else range(n)
            for q in targets:
                if q != p:
                    inbox[q][p] = view[p]
        view = [(view[q], tuple(inbox[q])) for q in range(n)]
    return {p: view[p] for p in range(n) if p not in crashes}


def _set_crash(e: Execution, p: int, c: Crash | None) -> Execution:
    crashes = crash_map(e)
    if c is None:
        crashes.pop(p, None)
    else:
        crashes[p] = c
    return make(e[0], crashes)


def _silence(e: Execution, p: int, k: int, rounds: int) -> list[Execution]:
    """Executions from e (p live) to e with p crashed in round k, sending nothing."""
    n = len(e[0])
    path = [e]
    for r in range(rounds, k - 1, -1):
        cur = _set_crash(path[-1], p, (r, frozenset(q for q in range(n) if q != p)))
        path.append(cur)  # the same views as the previous execution
        for q in range(n):
            if q != p:
                path.extend(_remove(path[-1], p, q, r, rounds)[1:])
    return path


def _remove(e: Execution, p: int, q: int, r: int, rounds: int) -> list[Execution]:
    """Executions from e to e without the round-r message from p to q."""
    crashes = crash_map(e)
    rr, s = crashes[p]
    assert rr == r and q in s
    target = _set_crash(e, p, (r, s - {q}))
    if r == rounds or (q in crashes and crashes[q][0] <= r):
        return [e, target]
    # Silence q from round r + 1 on, drop the message, then bring q back.
    there = _silence(e, q, r + 1, rounds)
    back = _silence(target, q, r + 1, rounds)
    dropped = _set_crash(there[-1], p, (r, s - {q}))
    assert dropped == back[-1]
    return there + list(reversed(back))


def build_chain(n: int, rounds: int) -> list[Execution]:
    """The chain from all 0 to all 1 for R = rounds, as described above."""
    inputs = [0] * n
    chain = [make(tuple(inputs), {})]
    for i in range(n):
        start = chain[-1]
        there = _silence(start, i, 1, rounds)
        inputs[i] = 1
        back = _silence(make(tuple(inputs), {}), i, 1, rounds)
        assert back[-1][1] == there[-1][1]
        chain.extend(there[1:])
        chain.extend(reversed(back))
    return chain


def max_crashes(chain: list[Execution]) -> int:
    return max(len(e[1]) for e in chain)


def one_crash_per_round(e: Execution) -> bool:
    rounds = [c[0] for _, c in e[1]]
    return len(rounds) == len(set(rounds))


def witness(a: Execution, b: Execution, rounds: int) -> int | None:
    """A process live in both executions with the same final view, if any."""
    va, vb = final_views(a, rounds), final_views(b, rounds)
    for p in sorted(set(va) & set(vb)):
        if va[p] == vb[p]:
            return p
    return None


Rule = Callable[[int, Hashable], int]


def find_violation(chain: list[Execution], rounds: int, rule: Rule) -> tuple[str, Execution] | None:
    """Walk the chain and return the first execution that breaks agreement or validity."""
    for e in chain:
        dec = {rule(p, v) for p, v in final_views(e, rounds).items()}
        if len(dec) > 1:
            return ("agreement", e)
        if len(set(e[0])) == 1 and dec and dec != {e[0][0]}:
            return ("validity", e)
    return None


def inputs_seen(view: Hashable) -> set[int]:
    """All input values that appear in a full-information view."""
    out: set[int] = set()
    stack = [view]
    while stack:
        v = stack.pop()
        if v is None:
            continue
        if isinstance(v, tuple) and len(v) == 1 and isinstance(v[0], int):
            out.add(v[0])
        elif isinstance(v, tuple):
            stack.extend(v)
    return out


def floodset_rule(p: int, view: Hashable) -> int:
    """FloodSet with the minimum rule, read off the full-information view."""
    return min(inputs_seen(view))
