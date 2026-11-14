# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transformation-based-reversible-synthesis/. The authors are listed in prov/WZABZ7.jsonl.

"""Transformation-based synthesis of reversible circuits (Miller, Maslov and
Dueck, DAC 2003).

A reversible function on n lines is a permutation f of 0..2^n - 1, given as
the list [f(0), f(1), ...]. Line t is bit t of the number.

A gate is a pair (controls, target): controls is a bit mask, target is a line
not in it. The gate flips the target bit when every control bit is 1. With no
control it is NOT, with one CNOT, with two Toffoli. A circuit is a list of
gates; the first gate acts first.
"""


def apply_gate(gate, x):
    controls, target = gate
    if x & controls == controls:
        return x ^ (1 << target)
    return x


def run(circuit, x):
    """The output of the circuit on input x."""
    for gate in circuit:
        x = apply_gate(gate, x)
    return x


def table(circuit, n):
    """The truth table [C(0), C(1), ...] of a circuit on n lines."""
    return [run(circuit, x) for x in range(1 << n)]


def row_gates(v, i, n):
    """Gates that map the value v to i and fix every value below i, if v > i.

    First set the bits that i has and v lacks, with the bits of v as controls.
    Then clear the bits that v has and i lacks, with the bits of i as controls.
    """
    gates = []
    for t in range(n):  # @line L5
        if i >> t & 1 and not v >> t & 1:
            gates.append((v, t))
    w = v | i
    for t in range(n):  # @line L6
        if w >> t & 1 and not i >> t & 1:
            gates.append((i, t))
    return gates


def synthesis_steps(f, bidirectional=False):
    """Run the algorithm. Return a list with one (side, gates) per row.

    side is "out" or "in", and gates are the gates found for that row, in the
    order they were applied to the table.
    """
    size = len(f)
    n = size.bit_length() - 1
    if size != 1 << n or sorted(f) != list(range(size)):
        raise ValueError("f must be a permutation of 0..2^n - 1")
    out = list(f)  # @line L1
    inv = [0] * size
    for x, y in enumerate(out):
        inv[y] = x
    steps = []
    for i in range(size):  # @line L2
        if out[i] == i:  # @line L3
            steps.append(("out", []))
            continue
        j = inv[i]
        use_inputs = bidirectional and bin(i ^ j).count("1") < bin(i ^ out[i]).count("1")
        # a is the table to change and b its inverse. A gate G at the outputs
        # makes out <- G o out; a gate at the inputs makes inv <- G o inv.
        a, b = (inv, out) if use_inputs else (out, inv)  # @line L4
        gates = row_gates(a[i], i, n)
        for gate in gates:
            for x in range(size):  # @line L7
                a[x] = apply_gate(gate, a[x])
            for x in range(size):
                b[a[x]] = x
        steps.append(("in" if use_inputs else "out", gates))  # @line L8
    return steps


def synthesize(f, bidirectional=False):
    """Return a circuit of multiple-control Toffoli gates that computes f.

    With bidirectional=False, gates are added only at the outputs (the basic
    algorithm). With bidirectional=True, each row is fixed from the side that
    needs fewer gates.
    """
    at_inputs, at_outputs = [], []
    for side, gates in synthesis_steps(f, bidirectional):
        (at_inputs if side == "in" else at_outputs).extend(gates)
    # The output gates were found from the last gate of the circuit backward.
    return at_inputs + at_outputs[::-1]  # @line L9
