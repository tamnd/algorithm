# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fault-tolerance-by-recomputation/. The authors are listed in prov/M9PXF3.jsonl.
"""A MapReduce master that survives worker failures by running tasks again,
as in Dean and Ghemawat (2004), Section 3.3, in discrete time steps.

A task runs on one worker for 1 to 3 steps (chosen by the rng). Map output
stays on the local disk of the worker, so it is lost when that worker fails.
Reduce output goes to the global file system, and a reduce task commits it
with one atomic rename, so it survives. A reduce task starts only when all
map outputs exist, and it reads all its input when it starts.
When a worker fails, the master sets back to idle:
  every map or reduce task that is in progress on that worker, and
  every completed map task whose output was on that worker,
but not completed reduce tasks.
The job is word count, with R reduce tasks.
"""


def part(word, R):
    return sum(map(ord, word)) % R  # a fixed hash, the same in every run


def word_count_map(split):
    return [(w, 1) for w in split.split()]


def reduce_task(splits, t, R):
    groups = {}
    for s in splits:
        for k, v in word_count_map(s):
            if part(k, R) == t:
                groups.setdefault(k, []).append(v)
    return {k: sum(vs) for k, vs in groups.items()}


def run_job(splits, R, workers, fail_at, rng):
    """fail_at maps a time step to the workers that fail at the start of
    that step; they never come back. Returns (output dict, stats)."""
    M = len(splits)
    alive = set(range(workers))
    state = {("m", t): "idle" for t in range(M)}
    state.update({("r", t): "idle" for t in range(R)})
    where = {}                      # task -> worker
    ends = {}                       # running task -> the step at whose end it finishes
    gfs = {}                        # reduce task -> committed output
    stats = {"map_runs": 0, "reduce_runs": 0, "lost_map_outputs": 0,
             "killed_running": 0, "steps": 0}
    step = 0
    while len(gfs) < R:
        step += 1
        if step > 100000:
            raise RuntimeError("no progress")
        for w in sorted(fail_at.get(step, ())):
            if w not in alive:
                continue
            alive.discard(w)
            for task in sorted(state):
                if where.get(task) != w:
                    continue
                if state[task] == "running":
                    stats["killed_running"] += 1
                    state[task] = "idle"
                    del ends[task], where[task]
                elif state[task] == "done" and task[0] == "m":
                    stats["lost_map_outputs"] += 1
                    state[task] = "idle"
                    del where[task]
        if not alive:
            raise RuntimeError("all workers failed")
        # Give idle tasks to free workers: maps first, reduces when all maps are done.
        free = sorted(alive - {where[t] for t in ends})
        rng.shuffle(free)
        maps_done = all(state[("m", t)] == "done" for t in range(M))
        for task in sorted(state):
            if not free:
                break
            if state[task] == "idle" and (task[0] == "m" or maps_done):
                state[task], where[task] = "running", free.pop()
                ends[task] = step + rng.randint(1, 3) - 1
        # Tasks that end in this step.
        for task in sorted(t for t, e in ends.items() if e == step):
            del ends[task]
            state[task] = "done"
            if task[0] == "m":
                stats["map_runs"] += 1
            else:
                stats["reduce_runs"] += 1
                if task[1] not in gfs:      # the atomic rename: the first commit wins
                    gfs[task[1]] = reduce_task(splits, task[1], R)
                del where[task]
    stats["steps"] = step
    # A map output lost after all reduce tasks have read it need not be made
    # again: the job can end while such a map task is still idle or running.
    stats["maps_not_done_at_end"] = sum(state[("m", t)] != "done" for t in range(M))
    out = {}
    for t in range(R):
        out.update(gfs[t])
    return out, stats
