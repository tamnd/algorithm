# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crew-pram/. The authors are listed in prov/RA6DW1.jsonl.
"""The CREW PRAM: a step simulator with the concurrent-read exclusive-write check,
merging by ranking, and the one-step broadcast.

A step maps a processor number to (reads, compute). The read addresses may
depend on the processor's local registers, which the driver keeps; they are
known before the step. compute takes the tuple of values read and returns a
list of (address, value) writes. Reads see the old memory; writes go to a new
memory. A cell that was never written holds None.
"""


class AccessError(Exception):
    pass


def run_step(mem, step, exclusive_read=False):
    """Run one CREW step (or one EREW step if exclusive_read). Return (new memory, readers, writers)."""
    readers, writers, new = {}, {}, dict(mem)
    pending = []
    for pid in sorted(step):
        reads, compute = step[pid]
        for a in reads:
            readers.setdefault(a, set()).add(pid)
        for a, v in compute(tuple(mem.get(a) for a in reads)):
            writers.setdefault(a, []).append(pid)
            pending.append((a, v))
    for a, ps in writers.items():
        if len(ps) > 1:
            raise AccessError(f"concurrent write of cell {a!r} by {ps}")
    if exclusive_read:
        for a, ps in readers.items():
            if len(ps) > 1:
                raise AccessError(f"concurrent read of cell {a!r} by {sorted(ps)}")
    for a, v in pending:
        new[a] = v
    return new, readers, writers


class Crew:
    """A CREW PRAM that records the readers of each cell in each step."""

    def __init__(self, mem, exclusive_read=False):
        self.mem = dict(mem)
        self.exclusive_read = exclusive_read
        self.trace = []
        self.work = 0

    def step(self, step):
        self.mem, readers, writers = run_step(self.mem, step, self.exclusive_read)
        self.trace.append((readers, writers))
        self.work += len(step)

    @property
    def time(self):
        return len(self.trace)

    def max_readers(self):
        return max((len(s) for readers, _ in self.trace for s in readers.values()), default=0)


def search_steps(n):
    """The number of lock-step rounds of a binary search over n + 1 positions."""
    return (n).bit_length()  # equals ceil(lg(n + 1))


def merge_by_ranking(a, b, exclusive_read=False):
    """Merge sorted lists a and b on a CREW PRAM with len(a) + len(b) processors.

    Processor ("a", i) finds the number of b-items smaller than a[i]; processor
    ("b", j) finds the number of a-items at most b[j]. Each does a binary search
    in lock step, one probe per step, and then writes its item to position
    i + rank or j + rank of the output C. Ties put the a-item first, so all
    positions are distinct and the writes are exclusive.

    Return (merged list, machine).
    """
    m, n = len(a), len(b)
    mem = {("A", i): x for i, x in enumerate(a)}
    mem.update({("B", j): y for j, y in enumerate(b)})
    pram = Crew(mem, exclusive_read)
    procs = [("a", i) for i in range(m)] + [("b", j) for j in range(n)]
    if not procs:
        return [], pram
    # local registers of each processor: its item and its search interval [lo, hi)
    item, lo, hi = {}, {}, {}

    def load(pid):
        src = ("A", pid[1]) if pid[0] == "a" else ("B", pid[1])

        def compute(v, pid=pid):
            item[pid] = v[0]
            return []
        return (src,), compute

    pram.step({pid: load(pid) for pid in procs})
    for pid in procs:
        lo[pid], hi[pid] = 0, (n if pid[0] == "a" else m)

    def probe(pid):
        mid = (lo[pid] + hi[pid]) // 2
        other = ("B", mid) if pid[0] == "a" else ("A", mid)

        def compute(v, pid=pid, mid=mid):
            x = v[0]
            go_right = x < item[pid] if pid[0] == "a" else x <= item[pid]
            if go_right:
                lo[pid] = mid + 1
            else:
                hi[pid] = mid
            return []
        return (other,), compute

    for _ in range(search_steps(max(m, n))):
        pram.step({pid: probe(pid) for pid in procs if lo[pid] < hi[pid]})

    def write(pid):
        return (), lambda v, pid=pid: [(("C", pid[1] + lo[pid]), item[pid])]

    pram.step({pid: write(pid) for pid in procs})
    return [pram.mem[("C", k)] for k in range(m + n)], pram


def broadcast(p, value, exclusive_read=False):
    """All p processors read cell "x" in one step and write their own cell B[i]."""
    pram = Crew({"x": value}, exclusive_read)
    pram.step({i: (("x",), lambda v, i=i: [(("B", i), v[0])]) for i in range(p)})
    return [pram.mem[("B", i)] for i in range(p)], pram


def tree_or(bits):
    """The OR of n bits by a balanced tree in ceil(lg n) steps; it is EREW, so also CREW."""
    n = len(bits)
    pram = Crew({("A", i): x for i, x in enumerate(bits)})
    d = 1
    while d < n:
        pram.step({i: ((("A", i), ("A", i + d)), lambda v, i=i: [(("A", i), v[0] | v[1])])
                   for i in range(0, n - d, 2 * d)})
        d *= 2
    return (pram.mem[("A", 0)] if n else 0), pram
