# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stride-scheduling/. The authors are listed in prov/RJMX01.jsonl.

import heapq
from fractions import Fraction
from typing import Union

Num = Union[int, Fraction]


def _div(a: int, b: int) -> Num:
    """a / b as an int when exact, else as a Fraction."""
    return a // b if a % b == 0 else Fraction(a, b)


class Stride:
    """Stride scheduling of Waldspurger and Weihl (MIT/LCS/TM-528, 1995).

    Client c with t_c tickets has stride stride1 / t_c. Each quantum goes to
    the client with the smallest pass (ties to the client that joined first),
    and its pass grows by its stride. Arithmetic is exact: a stride is an int
    when t_c divides stride1, else a Fraction.

    The dynamic part follows the paper's global pass: it grows by
    stride1 / T per quantum, where T is the total of the tickets. A client
    joins with pass = global pass + remain, and leaving saves
    remain = pass - global pass.
    """

    def __init__(self, stride1: int) -> None:
        if stride1 < 1:
            raise ValueError("stride1 must be positive")
        self.stride1 = stride1
        self.tickets: dict[str, int] = {}
        self.stride: dict[str, Num] = {}
        self.pass_: dict[str, Num] = {}
        self.seq: dict[str, int] = {}
        self._next_seq = 0
        self.heap: list[tuple[Num, int, str]] = []
        self.global_pass: Num = 0

    def join(self, name: str, tickets: int, remain: Num = 0) -> None:
        if name in self.tickets or tickets < 1:
            raise ValueError("new client with at least one ticket")
        self.tickets[name] = tickets
        self.stride[name] = _div(self.stride1, tickets)  # @line L1
        self.pass_[name] = self.global_pass + remain
        self.seq[name] = self._next_seq
        self._next_seq += 1
        heapq.heappush(self.heap, (self.pass_[name], self.seq[name], name))  # @line L2

    def leave(self, name: str) -> Num:
        """Remove a client and return its remain, for a later join."""
        remain = self.pass_[name] - self.global_pass
        for d in (self.tickets, self.stride, self.pass_, self.seq):
            del d[name]
        self.heap = [e for e in self.heap if e[2] != name]
        heapq.heapify(self.heap)
        return remain

    def set_tickets(self, name: str, tickets: int) -> None:
        """Change the tickets of a client; its remain scales with its stride."""
        old = self.stride[name]
        remain = self.leave(name)
        new = _div(self.stride1, tickets)
        self.join(name, tickets, remain * Fraction(new) / Fraction(old))

    def schedule(self) -> str:
        """Choose the client for the next quantum and charge it."""
        if not self.heap:
            raise ValueError("no clients")
        _, s, c = heapq.heappop(self.heap)  # @line L4
        self.pass_[c] += self.stride[c]  # @line L6
        heapq.heappush(self.heap, (self.pass_[c], s, c))  # @line L7
        self.global_pass += _div(self.stride1, sum(self.tickets.values()))
        return c


def stride_schedule(tickets: dict[str, int], n: int, stride1: int = 0) -> list[str]:
    """Run n quanta for a fixed set of clients, all with pass 0 at the start.
    stride1 = 0 means the least common multiple of the tickets, so that all
    strides are integers. Return the client of each quantum."""
    if stride1 == 0:
        stride1 = 1
        for t in tickets.values():
            stride1 = stride1 * t // _gcd(stride1, t)
    st = Stride(stride1)
    for c, t in tickets.items():
        st.join(c, t)
    out = []
    for _ in range(n):  # @line L3
        out.append(st.schedule())  # @line L5
    return out


def _gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a
