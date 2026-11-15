# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coverage-guided-fuzzing/. The authors are listed in prov/6GRW00.jsonl.
"""Coverage-guided greybox fuzzing in the style of AFL, on the toy IR.

An input is a tuple of integers, one per parameter of the program. The
instrumentation counts how often each edge of the control flow graph is
taken in a run and puts each count in an AFL bucket (1, 2, 3, 4-7, 8-15,
16-31, 32-127, 128+). The coverage of a run is the set of pairs
(edge, bucket). An input that is not a crash is kept in the queue when its
coverage has a pair that no earlier input had. A crash is a trap; it is
kept when its coverage is new among the crashes.

Mutations: a deterministic stage the first time an entry is fuzzed (flip
each of the low 8 bits of each integer, add and subtract 1 to 35, set each
integer to an interesting value) and then a havoc stage of stacked random
mutations. Before each entry the queue is culled: for every edge, the
entry with the shortest run that covers the edge is a candidate, and a
greedy pass picks a favored set that covers every edge. Entries that are
not favored are skipped with probability 0.9.

fuzz(prog, seeds, max_execs, seed) returns a Result. Everything is driven
by random.Random(seed), so a run of the fuzzer can be repeated exactly.
Nothing here claims that the fuzzer finds every path or every crash.
"""

import random

import toyir

INTERESTING = (-128, -1, 0, 1, 16, 32, 64, 100, 127)
ARITH_MAX = 35
HAVOC_RUNS = 32
SKIP_NOT_FAVORED = 0.9


def bucket(n):
    """The AFL hit-count bucket of a count n >= 1."""
    if n <= 3:
        return n
    if n <= 7:
        return 4
    if n <= 15:
        return 8
    if n <= 31:
        return 16
    if n <= 127:
        return 32
    return 128


def execute(prog, args, fuel=10000):
    """Run prog on args with edge counters. Returns (kind, coverage, steps),
    where kind is "ret", "trap" or "fuel" and coverage is a frozenset of
    pairs ((from, to), bucket)."""
    env = dict(zip(prog.params, args))
    counts = {}
    steps = 0
    label = prog.entry

    def val(a):
        if isinstance(a, int):
            return a
        if a not in env:
            raise toyir.UndefinedName(a)
        return env[a]

    def cov():
        return frozenset((e, bucket(n)) for e, n in counts.items())

    while True:
        block = prog.blocks[label]
        for ins in block.instrs:
            if steps >= fuel:
                return "fuel", cov(), steps
            steps += 1
            if ins[0] == "const":
                env[ins[1]] = ins[2]
            elif ins[0] == "copy":
                env[ins[1]] = val(ins[2])
            elif ins[0] == "op":
                try:
                    env[ins[1]] = toyir._binop(ins[2], val(ins[3]), val(ins[4]))
                except toyir._Trap:
                    return "trap", cov(), steps
            else:
                raise ValueError("execute handles const, copy and op only")
        if steps >= fuel:
            return "fuel", cov(), steps
        steps += 1
        t = block.term
        if t[0] == "ret":
            return "ret", cov(), steps
        nxt = t[1] if t[0] == "jump" else (t[2] if val(t[1]) != 0 else t[3])
        e = (label, nxt)
        counts[e] = counts.get(e, 0) + 1
        label = nxt


class Entry:
    __slots__ = ("args", "cov", "steps", "found_at", "det_done")

    def __init__(self, args, cov, steps, found_at):
        self.args = args
        self.cov = cov
        self.steps = steps
        self.found_at = found_at
        self.det_done = False


class Result:
    def __init__(self):
        self.queue = []
        self.crashes = []
        self.virgin = set()
        self.crash_virgin = set()
        self.execs = 0
        self.first_crash = None


def deterministic(args):
    """The deterministic stage: one mutation at a time, in a fixed order."""
    for i in range(len(args)):
        for bit in range(8):
            x = list(args)
            x[i] ^= 1 << bit
            yield tuple(x)
    for i in range(len(args)):
        for d in range(1, ARITH_MAX + 1):
            for s in (d, -d):
                x = list(args)
                x[i] += s
                yield tuple(x)
    for i in range(len(args)):
        for v in INTERESTING:
            if args[i] != v:
                x = list(args)
                x[i] = v
                yield tuple(x)


def havoc(rng, args):
    """A stack of 2 to 8 random mutations."""
    x = list(args)
    k = len(x)
    for _ in range(1 << rng.randint(1, 3)):
        i = rng.randrange(k)
        r = rng.randrange(5)
        if r == 0:
            x[i] ^= 1 << rng.randrange(8)
        elif r == 1:
            x[i] += rng.choice((1, -1)) * rng.randint(1, ARITH_MAX)
        elif r == 2:
            x[i] = rng.choice(INTERESTING)
        elif r == 3:
            x[i] = rng.randint(-128, 127)
        else:
            x[i] = x[rng.randrange(k)]
    return tuple(x)


def edges_of(cov):
    return {e for e, _ in cov}


def cull(queue):
    """The favored entries: for each edge, the entry with the shortest run
    that covers it (the earliest on ties); then a greedy pass over the edges
    in sorted order adds the best entry of each edge not yet covered."""
    best = {}
    for idx, q in enumerate(queue):  # @line L11
        for e in edges_of(q.cov):
            if e not in best or q.steps < queue[best[e]].steps:
                best[e] = idx
    favored = set()  # @line L12
    covered = set()
    for e in sorted(best, key=repr):  # @line L13
        if e not in covered:
            favored.add(best[e])
            covered |= edges_of(queue[best[e]].cov)
    return favored  # @line L14


def fuzz(prog, seeds, max_execs=20000, seed=0, fuel=10000):
    rng = random.Random(seed)
    res = Result()

    def try_input(x):
        """Run x and save it if it is interesting. False when the budget is used."""
        if res.execs >= max_execs:
            return False
        res.execs += 1
        kind, cov, steps = execute(prog, x, fuel)  # @line L7
        if kind == "trap":  # @line L8
            if cov - res.crash_virgin or not res.crashes:
                res.crash_virgin |= cov
                res.crashes.append(x)
                if res.first_crash is None:
                    res.first_crash = res.execs
        elif kind == "ret" and cov - res.virgin:  # @line L9
            res.virgin |= cov  # @line L10
            res.queue.append(Entry(x, cov, steps, res.execs))
        return True

    for s in seeds:  # @line L1
        s = tuple(s)
        res.execs += 1
        kind, cov, steps = execute(prog, s, fuel)
        res.queue.append(Entry(s, cov, steps, res.execs))
        res.virgin |= cov
    if not res.queue:
        raise ValueError("fuzz needs at least one seed")
    while res.execs < max_execs:  # @line L2
        idx = 0
        while idx < len(res.queue):  # @line L3
            q = res.queue[idx]
            favored = cull(res.queue)  # @line L4
            if idx not in favored and rng.random() < SKIP_NOT_FAVORED:  # @line L5
                idx += 1
                continue
            if not q.det_done:  # @line L6
                q.det_done = True
                for x in deterministic(q.args):
                    if not try_input(x):
                        return res
            for _ in range(HAVOC_RUNS):
                if not try_input(havoc(rng, q.args)):
                    return res
            idx += 1
    return res


def random_testing(prog, max_execs=20000, seed=0, lo=-128, hi=127, fuel=10000):
    """Blind random testing with the same budget, for comparison: returns
    the set of edges covered and the number of the first crashing run."""
    rng = random.Random(seed)
    edges = set()
    first_crash = None
    for n in range(1, max_execs + 1):
        x = tuple(rng.randint(lo, hi) for _ in prog.params)
        kind, cov, _ = execute(prog, x, fuel)
        edges |= edges_of(cov)
        if kind == "trap" and first_crash is None:
            first_crash = n
    return edges, first_crash
