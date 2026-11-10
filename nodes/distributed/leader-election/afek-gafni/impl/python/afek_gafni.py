# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/afek-gafni/. The authors are listed in prov/51R5KB.jsonl.

"""Synchronous election on a complete network by capture in doubling phases.

This is the simplified synchronous form on the page. Phase i has 4 rounds:
1. every live candidate sends CAP(id) on its next 2^i untried links;
2. a process takes the largest request; if it owns itself it decides at
   once, otherwise it sends Q(id) to its owner;
3. an owner answers every query: YES if it is dead or the id is larger than
   its own (then it dies), NO otherwise;
4. the process sends ACC to the chosen candidate if it was accepted, and REJ
   to every other request.
A candidate stays alive only if all its requests of the phase got ACC. A
candidate that has captured all n - 1 others is the leader and tells everyone.
"""

import math
import random


def afek_gafni_sync(n: int, ids: list[int], initiators: list[int] | None = None,
                    seed: int = 0) -> dict:
    rng = random.Random(seed)
    if initiators is None:
        initiators = list(range(n))
    ports = []
    for v in range(n):
        lst = [w for w in range(n) if w != v]
        rng.shuffle(lst)
        ports.append(lst)
    owner = list(range(n))
    alive = [False] * n
    for c in initiators:
        alive[c] = True
    tried = [0] * n
    captured = [0] * n
    counts = {"CAP": 0, "Q": 0, "ANS": 0, "ACC": 0, "REJ": 0, "LEADER": 0}
    rounds = 0
    survivors: list[int] = []  # number of live candidates after each phase
    leaders: list[int] = []
    if n == 1:
        return {"leaders": [0] if alive[0] else [], "counts": counts, "messages": 0,
                "rounds": 0, "survivors": [], "phases": 0}
    phase = 0
    while not leaders and any(alive):
        # Round 1: requests.  # @line L1
        requests: dict[int, list[int]] = {}
        sent = {}
        for c in range(n):
            if alive[c]:
                k = min(2 ** phase, n - 1 - tried[c])
                targets = ports[c][tried[c]:tried[c] + k]
                tried[c] += k
                sent[c] = targets
                for x in targets:
                    requests.setdefault(x, []).append(c)
                    counts["CAP"] += 1
        # Round 2: each process takes the largest request.  # @line L2
        chosen: dict[int, int] = {}
        decision: dict[int, bool] = {}
        queries: dict[int, list[int]] = {}
        for x, reqs in requests.items():
            c = max(reqs, key=lambda r: ids[r])
            chosen[x] = c
            if owner[x] == x:
                if not alive[x] or ids[c] > ids[x]:
                    alive[x] = False
                    decision[x] = True
                else:
                    decision[x] = False
            else:  # @line L3
                queries.setdefault(owner[x], []).append(x)
                counts["Q"] += 1
        # Round 3: owners answer.  # @line L4
        kill = set()
        for o, xs in queries.items():
            for x in xs:
                c = chosen[x]
                counts["ANS"] += 1
                if not alive[o] or ids[c] > ids[o]:
                    decision[x] = True
                    kill.add(o)
                else:
                    decision[x] = False
        for o in kill:
            alive[o] = False
        # Round 4: answers to the candidates.  # @line L5
        got_rej = set()
        for x, reqs in requests.items():
            for c in reqs:
                if c == chosen[x] and decision[x]:
                    owner[x] = c
                    counts["ACC"] += 1
                    if alive[c]:
                        captured[c] += 1
                else:
                    counts["REJ"] += 1
                    got_rej.add(c)
        rounds += 4
        # End of the phase.  # @line L6
        for c in sent:
            if c in got_rej:
                alive[c] = False
        survivors.append(sum(alive))
        for c in range(n):
            if alive[c] and captured[c] == n - 1:  # @line L7
                leaders.append(c)
                counts["LEADER"] += n - 1
        phase += 1
    if leaders:
        rounds += 1
    return {
        "leaders": leaders,
        "counts": counts,
        "messages": sum(counts.values()),
        "rounds": rounds,
        "survivors": survivors,
        "phases": phase,
    }


def log2_ceil(n: int) -> int:
    return max(0, math.ceil(math.log2(n))) if n > 1 else 0
