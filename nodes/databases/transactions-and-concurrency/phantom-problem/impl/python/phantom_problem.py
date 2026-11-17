# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phantom-problem/. The authors are listed in prov/J2PGNY.jsonl.

"""The phantom problem, shown with two lock schemes on a sorted index.

A table is a set of integer keys kept in a sorted index. A transaction runs
range scans ("scan", lo, hi) and inserts ("ins", k). All locks are held until
commit (rigorous two-phase locking).

  "tuple":    a scan takes S locks on the keys it finds; an insert takes an
              X lock on the new key. A key that does not exist yet cannot be
              locked, so a concurrent insert into a scanned range succeeds and
              a repeated scan sees a phantom.
  "next-key": a scan also locks the first key after its range (or the end of
              the index), and an insert also takes an X lock on the key just
              above the new key. Each gap between keys is protected by the key
              that ends it, so an insert into a scanned range must wait.

Deadlocks are found in the wait-for graph; the youngest transaction on a
cycle aborts, its inserts are removed, and it restarts.
"""

import bisect
import random

END = float("inf")  # the lock name of the end of the index


def run_index(
    programs: dict[int, list],
    initial: list[int],
    scheme: str,
    rng: random.Random | None = None,
    script: list[int] | None = None,
    max_steps: int = 100000,
) -> dict:
    """Run the programs. Return the scan results, schedule and commit order."""
    assert scheme in ("tuple", "next-key")
    keys = sorted(initial)
    held: dict[float, dict[int, str]] = {}
    pc = {t: 0 for t in programs}
    results: dict[int, list] = {t: [] for t in programs}
    inserted: dict[int, list] = {t: [] for t in programs}
    done: list[int] = []
    schedule: list = []
    queue = list(script or [])

    def next_key(k: float) -> float:
        i = bisect.bisect_right(keys, k)
        return keys[i] if i < len(keys) else END

    def wanted(t: int) -> list[tuple[float, str]]:
        """The locks that the next action of t needs."""
        act = programs[t][pc[t]]
        if act[0] == "scan":
            _, lo, hi = act
            found = keys[bisect.bisect_left(keys, lo) : bisect.bisect_right(keys, hi)]
            need = [(k, "S") for k in found]
            if scheme == "next-key":
                need.append((next_key(hi), "S"))  # the gap after the range
            return need
        k = act[1]
        need = [(k, "X")]
        if scheme == "next-key":
            need.append((next_key(k), "X"))  # the gap that k falls into
        return need

    def blockers(t: int) -> set[int]:
        if t in done or pc[t] == len(programs[t]):
            return set()
        out = set()
        for k, m in wanted(t):
            for u, um in held.get(k, {}).items():
                if u != t and (m == "X" or um == "X"):
                    out.add(u)
        return out

    def release(t: int) -> None:
        for h in held.values():
            h.pop(t, None)

    def on_cycles() -> list[int]:
        live = [t for t in programs if t not in done]
        edges = {t: blockers(t) for t in live}
        found = []
        for t in live:
            reach, stack = set(), list(edges[t])
            while stack:
                v = stack.pop()
                if v not in reach:
                    reach.add(v)
                    stack.extend(edges[v])
            if t in reach:
                found.append(t)
        return found

    def step(t: int) -> None:
        if pc[t] == len(programs[t]):
            release(t)
            done.append(t)
            schedule.append(("c", t))
            return
        for k, m in wanted(t):
            if held.setdefault(k, {}).get(t) != "X":
                held[k][t] = m
        act = programs[t][pc[t]]
        if act[0] == "scan":
            _, lo, hi = act
            found = keys[bisect.bisect_left(keys, lo) : bisect.bisect_right(keys, hi)]
            results[t].append(list(found))
            schedule.append(("scan", t, lo, hi, tuple(found)))
        else:
            k = act[1]
            if k not in keys:
                bisect.insort(keys, k)
                inserted[t].append(k)
            schedule.append(("ins", t, k))
        pc[t] += 1

    for _ in range(max_steps):
        live = [t for t in programs if t not in done]
        if not live:
            break
        cyc = on_cycles()
        if cyc:
            v = max(cyc)
            for k in inserted[v]:
                keys.remove(k)
            inserted[v] = []
            results[v] = []
            release(v)
            pc[v] = 0
            schedule.append(("a", v))
            continue
        runnable = [t for t in live if not blockers(t)]
        while queue and queue[0] in done:
            queue.pop(0)
        if queue and queue[0] in runnable:
            step(queue.pop(0))
        else:
            step(min(runnable) if rng is None or queue else rng.choice(runnable))
    else:
        raise RuntimeError("step limit reached")
    return {"results": results, "schedule": schedule, "commit_order": done, "keys": keys}


def run_serial(programs: dict[int, list], initial: list[int], order: list[int]) -> dict[int, list]:
    """The scan results when the transactions run one after the other."""
    keys = set(initial)
    results: dict[int, list] = {}
    for t in order:
        results[t] = []
        for act in programs[t]:
            if act[0] == "scan":
                results[t].append(sorted(k for k in keys if act[1] <= k <= act[2]))
            else:
                keys.add(act[1])
    return results


def has_phantom(results: dict[int, list], programs: dict[int, list]) -> bool:
    """Did some transaction get two different answers for the same range?

    Keys that the transaction inserted itself do not count.
    """
    for t, prog in programs.items():
        own: set = set()
        seen: dict[tuple, set] = {}
        answers = iter(results[t])
        for a in prog:
            if a[0] == "ins":
                own.add(a[1])
                continue
            r = set(next(answers)) - own
            if a in seen and seen[a] != r:
                return True
            seen[a] = r
    return False
