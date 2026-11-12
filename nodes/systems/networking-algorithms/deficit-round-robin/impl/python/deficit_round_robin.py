# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deficit-round-robin/. The authors are listed in prov/4F8MEF.jsonl.

"""Deficit round robin (Shreedhar and Varghese, SIGCOMM 1995).

Each flow has a FIFO queue, a quantum Q_i in bytes and a deficit counter
DC_i. The flows with packets are kept in a round-robin ActiveList. When a
flow gets its turn, Q_i is added to DC_i, and the flow sends head packets
while the head fits in DC_i. A flow whose queue empties leaves the list and
its counter is reset to 0.

next_packet() returns one packet at a time, so the scheduler keeps the state
of the turn in progress between calls.
"""

from collections import deque


class DRR:
    def __init__(self, quantum: dict) -> None:
        self.quantum = dict(quantum)  # flow -> Q_i in bytes
        self.queues: dict = {f: deque() for f in quantum}  # flow -> (size, pid)
        self.dc: dict = {f: 0 for f in quantum}  # deficit counters
        self.active: deque = deque()  # the ActiveList
        self.in_list: set = set()
        self.turn_started = False  # has the head flow got its quantum?
        self.turns = 0  # number of turns given, for the cost analysis
        self.empty_turns = 0  # turns in which the flow sent nothing
        self._sent_this_turn = 0

    def enqueue(self, flow, size: int, pid) -> None:
        self.queues[flow].append((size, pid))  # @line L1
        if flow not in self.in_list:  # @line L2
            self.active.append(flow)
            self.in_list.add(flow)
            self.dc[flow] = 0

    def _end_turn(self) -> None:
        if self._sent_this_turn == 0:
            self.empty_turns += 1
        self.turn_started = False

    def next_packet(self):
        """Return (flow, size, pid) of the next packet to send, or None."""
        while self.active:  # @line L3
            i = self.active[0]  # @line L4
            if not self.turn_started:  # @line L5
                self.dc[i] += self.quantum[i]
                self.turn_started = True
                self.turns += 1
                self._sent_this_turn = 0
            q = self.queues[i]
            if q and q[0][0] <= self.dc[i]:  # @line L6
                size, pid = q.popleft()  # @line L7
                self.dc[i] -= size
                self._sent_this_turn += 1
                if not q:  # @line L8
                    self.dc[i] = 0
                    self.active.popleft()
                    self.in_list.discard(i)
                    self._end_turn()
                return i, size, pid  # @line L9
            self.active.rotate(-1)  # @line L10
            self._end_turn()
        return None  # @line L11


def packet_round_robin(queues: dict):
    """Plain round robin over packets, for comparison: one packet per flow
    per turn, whatever its size. queues: flow -> list of sizes. Yields
    (flow, size)."""
    qs = {f: deque(v) for f, v in queues.items()}
    order = deque(f for f in qs if qs[f])
    while order:
        f = order.popleft()
        yield f, qs[f].popleft()
        if qs[f]:
            order.append(f)
