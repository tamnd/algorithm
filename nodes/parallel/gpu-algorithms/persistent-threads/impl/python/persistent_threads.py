# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/persistent-threads/. The authors are listed in prov/NMFBCT.jsonl.
"""Models of persistent-threads GPU programs.

persistent_queue simulates p persistent workers (for example warps) that take
batches of tasks from a global counter with an atomic add, as in Aila and
Laine (2009).  static_blocks gives each worker a fixed contiguous share.
grid_barrier_run shows why a grid-wide barrier needs every block to be
resident at once.  Times are exact Fractions.  No CUDA code is run.
"""
import heapq
from fractions import Fraction as F


class Deadlock(Exception):
    pass


def persistent_queue(costs, p, batch=1, fetch_cost=0):
    """Greedy dynamic fetching. Returns (makespan, atomics, owner list)."""
    n = len(costs)
    nxt = 0                                    # the global work counter
    atomics = 0
    owner = [None] * n
    heap = [(F(0), w) for w in range(p)]       # (time the worker is free, worker id)
    heapq.heapify(heap)
    finish = F(0)
    while heap:                                            # @line L1: each worker loops until no work is left
        t, w = heapq.heappop(heap)
        base = nxt                                         # @line L2: base <- ATOMIC-ADD(next, g)
        nxt += batch
        atomics += 1
        t += F(fetch_cost)
        if base >= n:                                      # @line L3: no work left, the worker exits
            finish = max(finish, t)
            continue
        for i in range(base, min(n, base + batch)):        # @line L4: process the batch
            owner[i] = w
            t += F(costs[i])
        heapq.heappush(heap, (t, w))                       # @line L5: loop back for more work
    return finish, atomics, owner


def static_blocks(costs, p):
    """Each worker gets a contiguous share of ceil(n/p) tasks; no queue."""
    n = len(costs)
    share = -(-n // p) if n else 0
    loads = [sum((F(c) for c in costs[w * share:(w + 1) * share]), F(0)) for w in range(p)]
    return max(loads) if loads else F(0)


def graham_bound(costs, p, batch=1, fetch_cost=0):
    """Total work (with fetches) over p, plus the largest batch: a bound on the makespan."""
    n = len(costs)
    batches = [costs[i:i + batch] for i in range(0, n, batch)]
    jobs = [F(fetch_cost) + sum((F(c) for c in b), F(0)) for b in batches]
    total = sum(jobs, F(0)) + p * F(fetch_cost)          # every worker also makes one failed fetch
    return total / p + (max(jobs) if jobs else 0) + F(fetch_cost)


def rounds_time(r, round_work, launch, barrier, persistent):
    """r dependent rounds: one launch per round, or one launch and a grid barrier per round."""
    if persistent:
        return F(launch) + r * (F(round_work) + F(barrier))
    return r * (F(launch) + F(round_work))


def grid_barrier_run(blocks, resident):
    """Blocks run to a grid barrier and then finish. At most `resident` blocks are on the GPU.

    The block scheduler starts a waiting block only when a resident block finishes.
    Returns the order in which blocks finish, or raises Deadlock.
    """
    waiting = list(range(blocks))
    on_gpu = []
    arrived = set()
    done = []
    while waiting or on_gpu:
        while waiting and len(on_gpu) < resident:
            on_gpu.append(waiting.pop(0))
        for b in on_gpu:
            arrived.add(b)                                  # each resident block reaches the barrier
        if len(arrived) < blocks:
            raise Deadlock("%d blocks wait at the barrier for %d that cannot start"
                           % (len(arrived), blocks - len(arrived)))
        done.extend(on_gpu)                                 # all arrived: everyone passes and ends
        on_gpu = []
    return done


def max_persistent_blocks(sms, blocks_per_sm):
    """The grid size of a persistent kernel: every block can be resident at once."""
    return sms * blocks_per_sm
