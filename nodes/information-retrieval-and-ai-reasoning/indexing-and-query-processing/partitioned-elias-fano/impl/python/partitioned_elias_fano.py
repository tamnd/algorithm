# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partitioned-elias-fano/. The authors are listed in prov/PX2K2C.jsonl.

import bisect

RUN, BITMAP, EF = "run", "bitmap", "ef"


def low_width(b: int, u: int) -> int:
    """The Elias-Fano low width floor(log2(u / b)) for 1 <= b <= u, in integers."""
    return (u // b).bit_length() - 1


def ef_bits(b: int, u: int) -> int:
    """Bits of the Elias-Fano code of b distinct values in [0, u): b*l low bits plus b + floor((u-1)/2^l) + 1 high bits."""
    lw = low_width(b, u)
    return b * lw + b + ((u - 1) >> lw) + 1


def chunk_bits(b: int, u: int) -> int:
    """Payload bits of a chunk of b distinct values whose largest value is u - 1."""
    if b == u:
        return 0
    return min(u, ef_bits(b, u))


def chunk_universe(x: list[int], i: int, j: int) -> tuple[int, int, int]:
    """For the chunk x[i..j-1], return (base, U, b): values are coded as x - base in [0, U)."""
    base = 0 if i == 0 else x[i - 1] + 1
    return base, x[j - 1] - base + 1, j - i


def partition_cost(x: list[int], cuts: list[int], fixed: int) -> int:
    """Total bits of a partition given by cuts = [0, ..., n]: fixed bits per chunk plus the payloads."""
    total = 0
    for i, j in zip(cuts, cuts[1:]):
        _, u, b = chunk_universe(x, i, j)
        total += fixed + chunk_bits(b, u)
    return total


def optimal_partition(x: list[int], fixed: int) -> tuple[int, list[int]]:
    """The exact optimal partition by dynamic programming over prefixes. Cost O(n^2) time, O(n) space."""
    n = len(x)
    c = [0] + [0] * n  # @line L1
    back = [0] * (n + 1)
    for j in range(1, n + 1):  # @line L2
        best = None  # @line L3
        for i in range(j):  # @line L4
            _, u, b = chunk_universe(x, i, j)
            v = c[i] + fixed + chunk_bits(b, u)
            if best is None or v < best:  # @line L5
                best, back[j] = v, i
        c[j] = best if best is not None else 0
    cuts = [n]  # @line L6
    while cuts[-1] > 0:
        cuts.append(back[cuts[-1]])
    cuts.reverse()
    return c[n], cuts


def uniform_partition(n: int, size: int) -> list[int]:
    """Cuts for chunks of a fixed size, the last one possibly shorter."""
    return list(range(0, n, size)) + [n]


def ef_encode(vals: list[int], u: int) -> str:
    """Elias-Fano bit string of distinct increasing vals in [0, u): the low parts, then the high part H."""
    b = len(vals)
    lw = low_width(b, u)
    low = "".join(format(v & ((1 << lw) - 1), f"0{lw}b") if lw else "" for v in vals)
    high = ["0"] * (b + ((u - 1) >> lw) + 1)
    for k, v in enumerate(vals):
        high[(v >> lw) + k] = "1"
    return low + "".join(high)


def ef_access(payload: str, b: int, u: int, k: int) -> int:
    """Element k of an Elias-Fano chunk. Cost O(size of H) here; a select structure makes it O(1)."""
    lw = low_width(b, u)
    low = int(payload[k * lw:(k + 1) * lw], 2) if lw else 0
    high = payload[b * lw:]
    pos = -1
    for _ in range(k + 1):
        pos = high.index("1", pos + 1)
    return ((pos - k) << lw) | low


class PartitionedEliasFano:
    """A strictly increasing list of nonnegative integers, cut into chunks.

    Each chunk is coded relative to the last value of the chunk before it, as
    a run (no bits), a bitmap, or Elias-Fano, whichever is smallest. The upper
    level keeps, for each chunk, its first index and its last value; its size is
    modelled as fixed bits per chunk.
    """

    def __init__(self, x: list[int], fixed: int | None = None, chunk_size: int | None = None) -> None:
        for a, b in zip(x, x[1:]):
            if not a < b:
                raise ValueError("the list must be strictly increasing")
        if x and x[0] < 0:
            raise ValueError("values must be nonnegative")
        self.n = len(x)
        u = x[-1] + 1 if x else 1
        self.fixed = fixed if fixed is not None else 2 * u.bit_length() + self.n.bit_length()
        if not x:
            cuts = [0]
        elif chunk_size is None:
            _, cuts = optimal_partition(x, self.fixed)
        else:
            cuts = uniform_partition(self.n, chunk_size)
        self.cuts = cuts
        self.starts: list[int] = []
        self.lasts: list[int] = []
        self.chunks: list[tuple[str, int, int, int, str]] = []  # (kind, base, U, b, payload)
        for i, j in zip(cuts, cuts[1:]):  # @line L7
            base, u_j, b = chunk_universe(x, i, j)  # @line L8
            vals = [v - base for v in x[i:j]]
            if b == u_j:  # @line L9
                kind, payload = RUN, ""
            elif u_j <= ef_bits(b, u_j):  # @line L10
                bits = ["0"] * u_j
                for v in vals:
                    bits[v] = "1"
                kind, payload = BITMAP, "".join(bits)
            else:
                kind, payload = EF, ef_encode(vals, u_j)  # @line L11
            self.starts.append(i)  # @line L12
            self.lasts.append(x[j - 1])
            self.chunks.append((kind, base, u_j, b, payload))

    def __len__(self) -> int:
        return self.n

    def bits(self) -> int:
        """Total size in the cost model: fixed bits per chunk plus all payload bits."""
        return sum(self.fixed + len(c[4]) for c in self.chunks)

    def _element(self, j: int, k: int) -> int:
        kind, base, u, b, payload = self.chunks[j]
        if kind == RUN:
            return base + k
        if kind == BITMAP:
            pos = -1
            for _ in range(k + 1):
                pos = payload.index("1", pos + 1)
            return base + pos
        return base + ef_access(payload, b, u, k)

    def access(self, q: int) -> int:
        """The value at index q, 0 <= q < n."""
        if not 0 <= q < self.n:
            raise IndexError("index out of range")
        j = bisect.bisect_right(self.starts, q) - 1  # @line L13
        return self._element(j, q - self.starts[j])  # @line L14

    def next_geq(self, y: int) -> int:
        """The least index q with value >= y, or n if there is none."""
        j = bisect.bisect_left(self.lasts, y)  # @line L15
        if j == len(self.lasts):
            return self.n
        b = self.chunks[j][3]
        for k in range(b):  # @line L16
            if self._element(j, k) >= y:
                return self.starts[j] + k
        return self.n

    def decode(self) -> list[int]:
        """All values in order."""
        return [self._element(j, k) for j in range(len(self.chunks)) for k in range(self.chunks[j][3])]
