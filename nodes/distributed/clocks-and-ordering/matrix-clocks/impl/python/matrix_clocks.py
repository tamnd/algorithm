# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/matrix-clocks/. The authors are listed in prov/J3RKBA.jsonl.

"""Matrix clocks (Wuu and Bernstein 1984; Sarin and Lynch 1987).

Process i keeps an n x n matrix M. Row i is the vector clock of i. Row j is
what i knows of the vector clock of j. The model is the asynchronous
message-passing model with n processes 0 .. n - 1 and channels that need
not be FIFO. Executions use the format

    (p, "local", None), (p, "send", (q, mid)), (p, "recv", mid)

Each event costs O(n^2) time, each process stores n^2 integers, and each
message carries n^2 integers.
"""

import random

Matrix = tuple[tuple[int, ...], ...]


class MatrixClock:
    """The matrix clock of process i among n processes."""

    def __init__(self, n: int, i: int) -> None:
        """Precondition: 0 <= i < n."""
        self.n = n
        self.i = i
        self.m = [[0] * n for _ in range(n)]  # @line L1

    def snapshot(self) -> Matrix:
        """An immutable copy of the matrix. O(n^2)."""
        return tuple(tuple(row) for row in self.m)

    def tick(self) -> Matrix:
        """A local event. Return the timestamp of the event."""
        self.m[self.i][self.i] += 1  # @line L2
        return self.snapshot()  # @line L3

    def send(self) -> Matrix:
        """A send event. Return the matrix to attach to the message."""
        return self.tick()  # @line L4

    def receive(self, w: Matrix, j: int) -> Matrix:
        """A receive event of a message with matrix w sent by process j. O(n^2)."""
        for k in range(self.n):  # @line L5
            for col in range(self.n):
                self.m[k][col] = max(self.m[k][col], w[k][col])  # @line L6
        for col in range(self.n):
            self.m[self.i][col] = max(self.m[self.i][col], w[j][col])  # @line L7
        return self.tick()  # @line L8

    def known_by_all(self, k: int) -> int:
        """A count t such that, as far as i knows, every process knows the first t events of k. O(n)."""
        return min(self.m[row][k] for row in range(self.n))  # @line L9


def timestamp_execution(n: int, execution: list[tuple]) -> list[Matrix]:
    """Run one matrix clock per process. Return M(e) for each event, in order."""
    clocks = [MatrixClock(n, p) for p in range(n)]
    msg: dict[int, tuple[Matrix, int]] = {}
    out: list[Matrix] = []
    for p, kind, x in execution:
        if kind == "local":
            out.append(clocks[p].tick())
        elif kind == "send":
            t = clocks[p].send()
            msg[x[1]] = (t, p)
            out.append(t)
        elif kind == "recv":
            w, j = msg[x]
            out.append(clocks[p].receive(w, j))
        else:
            raise ValueError(f"unknown step kind {kind!r}")
    return out


def random_execution(n: int, steps: int, rng: random.Random, p_send: float = 0.4, p_recv: float = 0.4) -> list[tuple]:
    """A seeded random execution. In-transit messages are received in a random order."""
    in_transit: list[tuple[int, int]] = []
    out: list[tuple] = []
    mid = 0
    for _ in range(steps):
        r = rng.random()
        if r < p_recv and in_transit:
            m, q = in_transit.pop(rng.randrange(len(in_transit)))
            out.append((q, "recv", m))
        elif r < p_recv + p_send and n > 1:
            p = rng.randrange(n)
            q = rng.randrange(n - 1)
            q += q >= p
            out.append((p, "send", (q, mid)))
            in_transit.append((mid, q))
            mid += 1
        else:
            out.append((rng.randrange(n), "local", None))
    return out
