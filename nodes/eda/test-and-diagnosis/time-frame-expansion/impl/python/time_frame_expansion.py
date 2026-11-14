# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/time-frame-expansion/. The authors are listed in prov/3RBAMV.jsonl.
"""Time-frame expansion: test generation for a sequential circuit from reset.

A synchronous sequential circuit is a combinational core (a td2net Circuit) and
m flip-flops. The core's inputs are the primary inputs followed by the m
present-state lines, and its outputs are the primary outputs followed by the m
next-state lines. Every clock cycle the flip-flops load the next state. The
circuit starts in a known reset state, the same in the good and the faulty
machine. A single stuck-at fault sits on a line of the core, so it is present in
every clock cycle.

unroll(seq, k) builds the iterative logic array: k copies of the core, where the
present-state inputs of copy t + 1 read the next-state outputs of copy t and the
present-state inputs of copy 1 are the reset values. find_test_sequence searches the
array for k = 1, 2, ... frames with a complete branch-and-bound over the primary
inputs (in the style of PODEM, without backtrace), so it finds a shortest test
sequence when one of at most k_max vectors exists. The brute forces in the tests
are shortest_test_length (breadth-first search over pairs of good and faulty
states) and plain enumeration of input sequences.
"""

from __future__ import annotations

from collections import deque
from itertools import product
from typing import Optional, Sequence

from td2net import X, Circuit, Fault, eval_gate


class SequentialCircuit:
    """A combinational core with n_pi primary inputs, n_ff flip-flops and n_po primary outputs."""

    def __init__(self, core: Circuit, n_pi: int, n_ff: int, reset: Optional[Sequence[int]] = None) -> None:
        if len(core.pi) != n_pi + n_ff or len(core.po) < n_ff:
            raise ValueError("the core needs n_pi + n_ff inputs and at least n_ff outputs")
        self.core = core
        self.n_pi = n_pi
        self.n_ff = n_ff
        self.n_po = len(core.po) - n_ff
        self.reset = tuple(reset) if reset is not None else (0,) * n_ff
        if len(self.reset) != n_ff:
            raise ValueError("the reset state needs one value per flip-flop")

    def step(self, state: Sequence[int], vector: Sequence[int], fault: Optional[Fault] = None):
        """One clock cycle: (primary outputs, next state)."""
        out = self.core.outputs(tuple(vector) + tuple(state), fault)
        return out[: self.n_po], out[self.n_po :]

    def run(self, vectors: Sequence[Sequence[int]], fault: Optional[Fault] = None) -> list[tuple[int, ...]]:
        """The primary outputs of each clock cycle, starting from reset."""
        state = self.reset
        outs = []
        for v in vectors:
            o, state = self.step(state, v, fault)
            outs.append(o)
        return outs

    def detects(self, vectors: Sequence[Sequence[int]], fault: Fault) -> bool:
        """True if some output of some cycle differs between the good and the faulty machine."""
        return self.run(vectors) != self.run(vectors, fault)


class IterativeLogicArray:
    """k copies of the core as one combinational circuit.

    Line (t, j) is line j of the core in frame t (t = 0 .. k-1). A present-state
    stem of frame t > 0 reads the next-state line of frame t - 1, and a
    present-state stem of frame 0 is the reset value. The array's inputs are
    the primary inputs of every frame and its outputs are the primary outputs of
    every frame.
    """

    def __init__(self, seq: SequentialCircuit, k: int) -> None:
        core = seq.core
        self.seq = seq
        self.k = k
        n = core.n_lines
        self.n_core = n
        state_line = core.pi[seq.n_pi :]
        next_line = core.po[seq.n_po :]
        # L2: one copy of the core for each frame
        self.source: list[Optional[int]] = [None] * (k * n)
        self.reset_value: dict[int, int] = {}
        self.inputs: list[int] = []
        for t in range(k):
            for p in core.pi[: seq.n_pi]:
                self.inputs.append(t * n + p)
            for i, s in enumerate(state_line):
                if t == 0:
                    # L4: the present state of frame 1 is the reset state
                    self.reset_value[s] = seq.reset[i]
                else:
                    # L3: next state of frame t - 1 feeds the present state of frame t
                    self.source[t * n + s] = (t - 1) * n + next_line[i]
        self.outputs = [t * n + o for t in range(k) for o in core.po[: seq.n_po]]

    def simulate(self, pi_values: Sequence[int], fault: Optional[Fault] = None) -> list[int]:
        """Three-valued values of all k * L lines; the fault is in every frame."""
        core = self.seq.core
        n = self.n_core
        vals = [X] * (self.k * n)
        free = iter(pi_values)
        for t in range(self.k):
            base = t * n
            for j in range(n):
                line = base + j
                kind = core.kind[j]
                if kind == "pi":
                    src = self.source[line]
                    if src is not None:
                        v = vals[src]
                    elif t == 0 and j in self.reset_value:
                        v = self.reset_value[j]
                    else:
                        v = next(free)
                else:
                    v = eval_gate(core.op[j], [vals[base + q] for q in core.fanin[j]])
                # L5: the fault is present in every copy
                if fault is not None and fault[0] == j:
                    v = fault[1]
                vals[line] = v
        return vals

    def frame_vectors(self, pi_values: Sequence[int]) -> list[tuple[int, ...]]:
        p = self.seq.n_pi
        return [tuple(pi_values[t * p : (t + 1) * p]) for t in range(self.k)]


def unroll(seq: SequentialCircuit, k: int) -> IterativeLogicArray:
    return IterativeLogicArray(seq, k)


def combinational_test(ila: IterativeLogicArray, fault: Fault) -> Optional[list[int]]:
    """Complete search over the array's inputs: a fully specified test, or None.

    Decisions set the primary inputs frame by frame. After each decision the good
    and the faulty array are simulated with X on the open inputs. A branch
    succeeds when some output has known, different values, and fails when every
    output is known and equal in both arrays.
    """
    n_in = len(ila.inputs)
    values = [X] * n_in

    def outcome() -> Optional[bool]:
        good = ila.simulate(values)
        bad = ila.simulate(values, fault)
        open_output = False
        for o in ila.outputs:
            g, b = good[o], bad[o]
            if g != X and b != X:
                if g != b:
                    return True
            else:
                open_output = True
        return None if open_output else False

    def search(i: int) -> bool:
        r = outcome()
        if r is not None:
            return r
        if i == n_in:
            return False
        for v in (0, 1):
            values[i] = v
            if search(i + 1):
                return True
        values[i] = X
        return False

    if not search(0):
        return None
    return [0 if v == X else v for v in values]


def find_test_sequence(seq: SequentialCircuit, fault: Fault, k_max: int) -> Optional[list[tuple[int, ...]]]:
    """A shortest test sequence of at most k_max vectors from reset, or None.

    unroll makes the k copies (L2), links the frames (L3) and fixes the reset
    state (L4); simulate puts the fault in every copy (L5).
    """
    for k in range(1, k_max + 1):  # @line L1
        # @line L2
        # @line L3
        # @line L4
        ila = unroll(seq, k)
        # @line L5
        t = combinational_test(ila, fault)  # @line L6
        if t is not None:
            return ila.frame_vectors(t)  # @line L7
    return None  # @line L8


def shortest_test_length(seq: SequentialCircuit, fault: Fault) -> Optional[int]:
    """Brute force: breadth-first search over pairs (good state, faulty state) from reset.

    Returns the length of a shortest detecting sequence, or None if the fault
    cannot be detected from reset by any sequence.
    """
    vectors = list(product((0, 1), repeat=seq.n_pi))
    start = (seq.reset, seq.reset)
    depth = {start: 0}
    queue = deque([start])
    while queue:
        pair = queue.popleft()
        g, b = pair
        for v in vectors:
            og, ng = seq.step(g, v)
            ob, nb = seq.step(b, v, fault)
            if og != ob:
                return depth[pair] + 1
            nxt = (ng, nb)
            if nxt not in depth:
                depth[nxt] = depth[pair] + 1
                queue.append(nxt)
    return None


def reachable_pairs(seq: SequentialCircuit, fault: Fault) -> int:
    """The number of (good state, faulty state) pairs reachable from reset."""
    vectors = list(product((0, 1), repeat=seq.n_pi))
    start = (seq.reset, seq.reset)
    seen = {start}
    stack = [start]
    while stack:
        g, b = stack.pop()
        for v in vectors:
            nxt = (seq.step(g, v)[1], seq.step(b, v, fault)[1])
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return len(seen)


def counter_with_enable(m: int) -> SequentialCircuit:
    """An m-bit counter that counts up when e = 1, with the output z = q_{m-1} ... q_0."""
    inputs = ["e"] + [f"q{i}" for i in range(m)]
    gates: list[tuple[str, str, list[str]]] = []
    carry = "e"
    for i in range(m):
        gates.append((f"d{i}", "XOR", [f"q{i}", carry]))
        if i + 1 < m:
            gates.append((f"c{i + 1}", "AND", [carry, f"q{i}"]))
            carry = f"c{i + 1}"
    if m == 1:
        gates.append(("z", "BUF", ["q0"]))
    else:
        gates.append(("z", "AND", [f"q{i}" for i in range(m)]))
    core = Circuit(inputs, gates, ["z"] + [f"d{i}" for i in range(m)])
    return SequentialCircuit(core, 1, m)
