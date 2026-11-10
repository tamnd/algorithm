# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bsp-model/. The authors are listed in prov/C7AB2T.jsonl.
"""A BSP machine simulator that counts w, h and the supersteps, and three BSP
algorithms on it: broadcast (direct, tree and two-phase), prefix sums, and
sorting by regular sampling.

A superstep is a function step(pid, state, inbox) -> (work, outbox). It may
read and change only its own state and read only its own inbox, which holds
the (sender, word) pairs sent to it in the previous superstep, in the order
of the senders. The outbox is a list of (dest, word). The simulator runs the
p calls one after the other, but no call can see the effect of another call,
so the order does not matter: this is the parallel step. Then it delivers
all messages at once, which is the barrier. A message to oneself is
delivered but not counted in h, because it does not use the network.
"""

from dataclasses import dataclass, field


@dataclass
class Superstep:
    w: int  # the largest local work of one processor
    h: int  # the largest number of words that one processor sends or receives
    sent: list = field(default_factory=list)
    received: list = field(default_factory=list)


class BSP:
    def __init__(self, p):
        if p < 1:
            raise ValueError("p must be at least 1")
        self.p = p
        self.state = [dict() for _ in range(p)]
        self.inbox = [[] for _ in range(p)]
        self.log = []

    def superstep(self, step):
        p = self.p
        results = [step(i, self.state[i], self.inbox[i]) for i in range(p)]
        sent, received = [0] * p, [0] * p
        new_inbox = [[] for _ in range(p)]
        work = []
        for i, (wk, out) in enumerate(results):
            work.append(wk)
            for dest, word in out:
                if not 0 <= dest < p:
                    raise ValueError("bad destination %r" % (dest,))
                new_inbox[dest].append((i, word))
                if dest != i:
                    sent[i] += 1
                    received[dest] += 1
        self.inbox = new_inbox  # the barrier: all messages appear at once
        s = Superstep(max(work), max(max(sent), max(received)), sent, received)
        self.log.append(s)
        return s

    def totals(self):
        """(W, H, S): the sums of w and h over the supersteps, and their number."""
        return sum(s.w for s in self.log), sum(s.h for s in self.log), len(self.log)

    def cost(self, g, L):
        return sum(s.w + g * s.h + L for s in self.log)


def ceil_log2(x):
    return (x - 1).bit_length() if x > 1 else 0


# ---------------------------------------------------------------- broadcast


def broadcast_direct(p, x, root=0):
    """One superstep: the root sends x to each other processor. h = p - 1."""
    m = BSP(p)
    m.state[root]["x"] = x

    def send(i, st, inbox):
        if i == root:
            return 0, [(j, st["x"]) for j in range(p) if j != root]
        return 0, []

    m.superstep(send)
    out = [m.state[i].get("x", m.inbox[i][0][1] if m.inbox[i] else None) for i in range(p)]
    return out, m


def broadcast_tree(p, x, root=0):
    """Doubling: in superstep t each holder of rank r < 2^t sends to rank r + 2^t.
    ceil(lg p) supersteps, each with h = 1."""
    m = BSP(p)
    m.state[root]["x"] = x
    for t in range(ceil_log2(p)):
        def step(i, st, inbox, t=t):
            if inbox:
                st["x"] = inbox[0][1]
            r = (i - root) % p
            if r < (1 << t) and r + (1 << t) < p:
                return 0, [((root + r + (1 << t)) % p, st["x"])]
            return 0, []
        m.superstep(step)
    out = []
    for i in range(p):
        st = m.state[i]
        out.append(st["x"] if "x" in st else m.inbox[i][0][1])
    return out, m


def broadcast_two_phase(p, data, root=0):
    """Broadcast a list of n words in two supersteps. The root scatters piece j
    (of about n/p words) to processor j, then each processor sends its piece
    to all others. Each superstep has h <= (p - 1) * ceil(n / p)."""
    n = len(data)
    m = BSP(p)
    m.state[root]["data"] = list(data)
    bounds = [(j * n) // p for j in range(p + 1)]

    def scatter(i, st, inbox):
        if i != root:
            return 0, []
        out = []
        for j in range(p):
            for k in range(bounds[j], bounds[j + 1]):
                out.append(((root + j) % p, (k, st["data"][k])))
        return 0, out

    def allgather(i, st, inbox):
        st["piece"] = [word for _, word in inbox]
        return 0, [(j, word) for word in st["piece"] for j in range(p) if j != i]

    m.superstep(scatter)
    m.superstep(allgather)
    out = []
    for i in range(p):
        got = dict(m.state[i]["piece"])
        got.update(word for _, word in m.inbox[i])
        out.append([got[k] for k in range(n)])
    return out, m


# ---------------------------------------------------------------- prefix sums


def prefix_sums(blocks):
    """Inclusive prefix sums of the concatenation of blocks, block i on
    processor i. Two supersteps: local prefix sums and an exchange of the block
    totals (h = p - 1), then the offset is added."""
    p = len(blocks)
    m = BSP(p)
    for i in range(p):
        m.state[i]["a"] = list(blocks[i])

    def local(i, st, inbox):
        a = st["a"]
        for k in range(1, len(a)):
            a[k] = a[k - 1] + a[k]
        total = a[-1] if a else 0
        return len(a), [(j, total) for j in range(i + 1, p)]

    def offset(i, st, inbox):
        off = 0
        for _, t in inbox:
            off += t
        st["a"] = [v + off for v in st["a"]]
        return len(inbox) + len(st["a"]), []

    m.superstep(local)
    m.superstep(offset)
    return [m.state[i]["a"] for i in range(p)], m


# ---------------------------------------------------------------- sorting


def merge(a, b, counter):
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        counter[0] += 1
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out


def merge_runs(runs, counter):
    """Merge sorted runs pairwise, in ceil(lg k) rounds of at most r comparisons."""
    runs = [r for r in runs] or [[]]
    while len(runs) > 1:
        nxt = [merge(runs[k], runs[k + 1], counter) for k in range(0, len(runs) - 1, 2)]
        if len(runs) % 2:
            nxt.append(runs[-1])
        runs = nxt
    return runs[0]


def merge_sort(a, counter):
    return merge_runs([[x] for x in a], counter)


def sort_regular_sampling(blocks):
    """Sort by regular sampling on p processors. Each block has m >= p items.
    Keys are made distinct by tagging them with (processor, index).
    Superstep 1: local sort, p regular samples to processor 0.
    Superstep 2: processor 0 sorts the p^2 samples and sends p - 1 splitters.
    Superstep 3: each processor splits its run and sends bucket j to j.
    Superstep 4: each processor merges the runs it received.
    Returns (the sorted blocks, the machine)."""
    p = len(blocks)
    sizes = {len(b) for b in blocks}
    if len(sizes) != 1 or sizes.pop() < p:
        raise ValueError("each block must have the same size m >= p")
    m_items = len(blocks[0])
    mach = BSP(p)
    for i in range(p):
        mach.state[i]["a"] = [(x, i, k) for k, x in enumerate(blocks[i])]

    def s1(i, st, inbox):
        c = [0]
        st["a"] = merge_sort(st["a"], c)
        pos = [-(-(k + 1) * m_items // p) - 1 for k in range(p)]
        return c[0], [(0, st["a"][t]) for t in pos]

    def s2(i, st, inbox):
        if i != 0:
            return 0, []
        c = [0]
        samples = merge_runs([[s] for _, s in inbox], c)
        st["splitters"] = [samples[j * p - 1] for j in range(1, p)]
        return c[0], [(j, s) for j in range(p) for s in st["splitters"]]

    def s3(i, st, inbox):
        spl = [s for _, s in inbox]
        buckets, j, c = [[] for _ in range(p)], 0, 0
        for x in st["a"]:
            while j < p - 1:
                c += 1
                if x <= spl[j]:
                    break
                j += 1
            buckets[j].append(x)
        return c, [(dest, x) for dest in range(p) for x in buckets[dest]]

    def s4(i, st, inbox):
        runs = {}
        for sender, x in inbox:
            runs.setdefault(sender, []).append(x)
        c = [0]
        st["out"] = merge_runs([runs[s] for s in sorted(runs)], c)
        st["received"] = len(inbox)
        return c[0], []

    for step in (s1, s2, s3, s4):
        mach.superstep(step)
    return [[x for x, _, _ in mach.state[i]["out"]] for i in range(p)], mach
