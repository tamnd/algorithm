# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tombstone/. The authors are listed in prov/MG0079.jsonl.

"""Deletion in a replicated key-value store that syncs by anti-entropy.

Each replica maps key -> (stamp, value). Anti-entropy between two replicas is
one atomic session: for each key, both keep the entry with the larger stamp
(last-writer-wins). Three ways to delete:

- "erase": remove the key. A replica that still has the key gives it back.
- "tombstone": store (stamp, TOMB). A tombstone beats every older write.
- garbage collection of tombstones, either by a grace period (drop a tombstone
  older than `grace` time units) or by a stability condition (drop it once
  this replica knows that every replica holds it).
"""

import random

TOMB = object()


class Replica:
    def __init__(self, rid: int, n: int) -> None:
        self.rid = rid
        self.n = n
        self.data: dict[str, tuple[tuple[int, int], object]] = {}
        self.seen_by: dict[str, set[int]] = {}  # tombstone key -> replicas known to hold it
        self.clock = 0

    def stamp(self, now: int) -> tuple[int, int]:
        self.clock = max(self.clock + 1, now)
        return (self.clock, self.rid)

    def put(self, key: str, value: object, now: int) -> None:
        self.data[key] = (self.stamp(now), value)

    def delete(self, key: str, now: int, mode: str) -> None:
        if mode == "erase":
            self.data.pop(key, None)
        else:
            self.data[key] = (self.stamp(now), TOMB)
            self.seen_by[key] = {self.rid}

    def get(self, key: str) -> object:
        e = self.data.get(key)
        return None if e is None or e[1] is TOMB else e[1]

    def live_keys(self) -> set[str]:
        return {k for k, (_, v) in self.data.items() if v is not TOMB}


def sync(a: Replica, b: Replica, now: int) -> None:
    """One push-pull anti-entropy session: both end with the same entries."""
    for k in set(a.data) | set(b.data):
        ea, eb = a.data.get(k), b.data.get(k)
        best = max((e for e in (ea, eb) if e is not None), key=lambda e: e[0])
        for r, e in ((a, ea), (b, eb)):
            if e != best:
                r.data[k] = best
                r.clock = max(r.clock, best[0][0])
            if best[1] is TOMB:
                r.seen_by.setdefault(k, set()).add(r.rid)
        if best[1] is TOMB:
            s = a.seen_by.get(k, set()) | b.seen_by.get(k, set())
            a.seen_by[k] = set(s)
            b.seen_by[k] = set(s)


def collect(r: Replica, now: int, gc: str, grace: int = 0) -> list[str]:
    """Drop tombstones that the rule allows. Returns the dropped keys."""
    out = []
    for k, (stamp, v) in list(r.data.items()):
        if v is not TOMB:
            continue
        if gc == "grace" and now - stamp[0] > grace:  # the age counts from the deletion time
            out.append(k)
        elif gc == "stable" and len(r.seen_by.get(k, ())) == r.n:
            out.append(k)
    for k in out:
        del r.data[k]
        r.seen_by.pop(k, None)
    return out


def erase_run() -> list[Replica]:
    """Three replicas hold x. Replica 0 erases x; then 0 and 1 sync."""
    reps = [Replica(i, 3) for i in range(3)]
    reps[0].put("x", "v1", 1)
    sync(reps[0], reps[1], 2)
    sync(reps[1], reps[2], 3)
    reps[0].delete("x", 4, "erase")
    sync(reps[0], reps[1], 5)
    return reps


def random_run(seed: int, mode: str, gc: str = "none", grace: int = 0,
               down: tuple[int, int, int] | None = None, rounds: int = 60) -> dict:
    """n replicas; x is written and spread, then deleted at one replica; then
    rounds of anti-entropy between random pairs of live replicas, with tombstone
    collection after each round. down = (replica, from, to) keeps one replica
    out of all sessions in that time interval."""
    rng = random.Random(seed)
    n = rng.randint(3, 6)
    reps = [Replica(i, n) for i in range(n)]
    reps[0].put("x", "v1", 1)
    t = 2
    for i in range(1, n):
        sync(reps[0], reps[i], t)
        t += 1
    reps[rng.randrange(n)].put("y", "keep", t)
    reps[rng.randrange(n)].delete("x", t + 1, mode)
    t += 2
    for _ in range(rounds):
        live = [r for r in reps if not (down and r.rid == down[0] and down[1] <= t < down[2])]
        a, b = rng.sample(live, 2)
        sync(a, b, t)
        if gc != "none":
            for r in live:
                collect(r, t, gc, grace)
        t += 1
    # at the end every pair syncs, so all replicas hold the same entries
    for i in range(n):
        for j in range(i + 1, n):
            sync(reps[i], reps[j], t)
    for i in range(n):
        for j in range(i + 1, n):
            sync(reps[i], reps[j], t)
    return {"reps": reps, "n": n}
