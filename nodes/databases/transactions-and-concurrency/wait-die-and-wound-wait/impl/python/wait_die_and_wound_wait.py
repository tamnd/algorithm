# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wait-die-and-wound-wait/. The authors are listed in prov/8VMTDE.jsonl.

"""Wait-die and wound-wait (Rosenkrantz, Stearns and Lewis 1978), as a simulator.

Transactions lock items in S or X mode and hold every lock until they end
(rigorous two-phase locking). Each transaction has a timestamp, its start
time; a smaller timestamp is older. Here the timestamp of transaction t is t.
When a request conflicts with the locks of a set H of other transactions:

  wait-die:   the requester waits if it is older than every holder in H;
              otherwise it dies (aborts).
  wound-wait: the requester wounds (aborts) every younger holder in H, and
              waits for the older holders that are left, if any.

An aborted transaction is undone with before images and restarts with its
old timestamp. The rules are checked again each time the scheduler looks
at a waiting transaction, since the holders of an item can change.
"""

import random

Program = list[tuple[str, str]]


def write_value(t: int, k: int, seen: tuple) -> tuple:
    """The value that action number k of T_t writes after reading seen."""
    return ("f", t, k, seen)


def run_serial(programs: dict[int, Program], order: list[int], initial: dict) -> tuple[dict, dict]:
    """Run the programs one after the other. Return (final state, reads)."""
    db = dict(initial)
    reads: dict[int, list] = {}
    for t in order:
        seen: list = []
        for k, (op, x) in enumerate(programs[t]):
            if op == "r":
                seen.append(db[x])
            else:
                db[x] = write_value(t, k, tuple(seen))
        reads[t] = seen
    return db, reads


def run_locking(
    programs: dict[int, Program],
    policy: str,
    initial: dict,
    rng: random.Random | None = None,
    script: list[int] | None = None,
    max_steps: int = 200000,
) -> dict:
    """Run the programs under rigorous 2PL with the given policy.

    policy is "wait-die" or "wound-wait". With script, transactions step in
    that order (a waiting one keeps its turn), then the smallest runnable one
    steps; with rng, a random runnable one steps.

    Returns a dict with:
      schedule:     executed actions (op, txn, item), with "c" and "a" entries
      commit_order: the transactions in commit order
      reads:        the values that each committed attempt read
      final:        the final database state
      waits:        the wait-for graph after each decision, as sets of edges
      aborts:       the number of aborts of each transaction
    """
    assert policy in ("wait-die", "wound-wait")
    db = dict(initial)
    held: dict[str, dict[int, str]] = {x: {} for x in initial}
    pc = {t: 0 for t in programs}
    seen: dict[int, list] = {t: [] for t in programs}
    undo: dict[int, list] = {t: [] for t in programs}
    done: list[int] = []
    reads: dict[int, list] = {}
    schedule: list = []
    waits: list[frozenset] = []
    aborts = {t: 0 for t in programs}
    queue = list(script or [])

    def blockers(t: int) -> set[int]:
        if t in done or pc[t] == len(programs[t]):
            return set()
        op, x = programs[t][pc[t]]
        m = "X" if op == "w" else "S"
        if held[x].get(t) in ("X", m):
            return set()
        return {u for u, um in held[x].items() if u != t and (m == "X" or um == "X")}

    def abort(t: int) -> None:
        for x, before in reversed(undo[t]):  # @line L8
            db[x] = before
        for x in held:
            held[x].pop(t, None)
        schedule.append(("a", t, None))
        pc[t] = 0
        seen[t] = []
        undo[t] = []
        aborts[t] += 1

    def resolve() -> None:
        """Apply the policy to every waiting transaction, oldest first.

        A transaction that died before its first action has nothing to undo;
        it stays unstarted (a delayed restart) and does not wait for anyone.
        """
        dead = set()
        for t in sorted(programs):
            h = blockers(t)
            if not h:  # @line L1
                continue
            if policy == "wait-die":
                if any(u < t for u in h):  # @line L3
                    dead.add(t)  # T_t is younger than a holder: it dies
                    if pc[t] > 0:
                        abort(t)
                # else: T_t is older than every holder and waits  # @line L2
            else:
                for u in sorted(h):
                    if u > t:  # @line L4
                        abort(u)  # T_t wounds the younger holder
                # the holders left are older, and T_t waits for them  # @line L5
        edges = frozenset((t, u) for t in programs if t not in dead for u in blockers(t))
        waits.append(edges)

    def step(t: int) -> None:
        if pc[t] == len(programs[t]):
            schedule.append(("c", t, None))
            for x in held:  # @line L7
                held[x].pop(t, None)
            done.append(t)
            reads[t] = seen[t]
            return
        op, x = programs[t][pc[t]]
        m = "X" if op == "w" else "S"
        if held[x].get(t) not in ("X", m):
            held[x][t] = m  # @line L6
        if op == "r":
            seen[t].append(db[x])
        else:
            undo[t].append((x, db[x]))
            db[x] = write_value(t, pc[t], tuple(seen[t]))
        schedule.append((op, t, x))
        pc[t] += 1

    for _ in range(max_steps):
        live = [t for t in programs if t not in done]
        if not live:
            break
        resolve()
        runnable = [t for t in live if not blockers(t)]
        while queue and queue[0] in done:
            queue.pop(0)
        if queue and queue[0] in runnable:
            step(queue.pop(0))
        elif queue:
            step(min(runnable))
        else:
            step(min(runnable) if rng is None else rng.choice(runnable))
    else:
        raise RuntimeError("step limit reached")
    return {
        "schedule": schedule,
        "commit_order": done,
        "reads": reads,
        "final": db,
        "waits": waits,
        "aborts": aborts,
    }
