# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/observability-based-coverage/. The authors are listed in prov/XHG8NR.jsonl.
"""Observability tags on a gate-level circuit, after Devadas, Ghosh and Keutzer (1996).

A circuit has named primary inputs, gates in topological order and named
primary outputs. Every line (a primary input or a gate output) is a tag site.
A tag on line t stands for an error that flips the value of t. For one input
vector, tag_sets() computes for every line the set of sites whose tag reaches
it by the rule of the page: a tag passes a gate input when every other input
of the gate has a non-controlling value and does not depend on the tagged site.
The rule is sound (a tag at a line means that flipping the site flips the
line) and not complete. observable_sites() is the exact brute force.
"""

from fractions import Fraction

GATE_TYPES = ("AND", "OR", "NAND", "NOR", "XOR", "XNOR", "NOT", "BUF")
# The controlling input value of each gate type; None means no controlling value.
CONTROLLING = {"AND": 0, "NAND": 0, "OR": 1, "NOR": 1,
               "XOR": None, "XNOR": None, "NOT": None, "BUF": None}


class Circuit:
    """A combinational circuit. gates is a list of (name, type, [input names])."""

    def __init__(self, inputs, gates, outputs):
        self.inputs = list(inputs)
        self.gates = [(name, kind, list(ins)) for name, kind, ins in gates]
        self.outputs = list(outputs)
        seen = set(self.inputs)
        for name, kind, ins in self.gates:
            if kind not in GATE_TYPES:
                raise ValueError("unknown gate type " + kind)
            if kind in ("NOT", "BUF") and len(ins) != 1:
                raise ValueError(name + " needs one input")
            if kind not in ("NOT", "BUF") and len(ins) < 2:
                raise ValueError(name + " needs two or more inputs")
            for x in ins:
                if x not in seen:
                    raise ValueError("gates are not in topological order at " + name)
            if name in seen:
                raise ValueError("line defined twice: " + name)
            seen.add(name)
        for o in self.outputs:
            if o not in seen:
                raise ValueError("unknown output " + o)

    def lines(self):
        return self.inputs + [name for name, _, _ in self.gates]


def gate_value(kind, values):
    if kind == "AND":
        return int(all(values))
    if kind == "OR":
        return int(any(values))
    if kind == "NAND":
        return 1 - int(all(values))
    if kind == "NOR":
        return 1 - int(any(values))
    if kind == "XOR":
        return sum(values) % 2
    if kind == "XNOR":
        return 1 - sum(values) % 2
    if kind == "NOT":
        return 1 - values[0]
    return values[0]  # BUF


def simulate(circuit, vector, flip=None):
    """Values of all lines for vector (a dict input -> 0 or 1).

    If flip names a line, that line takes the complement of its computed value,
    and every gate that reads it sees the complement.
    """
    val = {}
    for x in circuit.inputs:
        val[x] = vector[x]
        if x == flip:
            val[x] = 1 - val[x]
    for name, kind, ins in circuit.gates:
        val[name] = gate_value(kind, [val[x] for x in ins])
        if name == flip:
            val[name] = 1 - val[name]
    return val


def fanin_cones(circuit):
    """Fin(l): the set of lines on which line l depends, l included."""
    fin = {x: {x} for x in circuit.inputs}
    for name, _, ins in circuit.gates:
        cone = {name}
        for x in ins:
            cone |= fin[x]
        fin[name] = cone  # @line L1
    return fin


def tag_sets(circuit, vector, fin=None):
    """Return (values, tags): tags[l] is the set of sites whose tag reaches line l."""
    if fin is None:
        fin = fanin_cones(circuit)
    val = simulate(circuit, vector)  # @line L4
    tag = {x: {x} for x in circuit.inputs}  # @line L5
    for name, kind, ins in circuit.gates:  # @line L6
        ctrl = CONTROLLING[kind]
        out = {name}  # @line L7
        k = len(ins)
        # prefix and suffix unions of the cones, so each pin costs O(1) unions
        prefix = [set()]
        for x in ins:
            prefix.append(prefix[-1] | fin[x])
        suffix = [set()]
        for x in reversed(ins):
            suffix.append(suffix[-1] | fin[x])
        suffix.reverse()
        bad = [ctrl is not None and val[x] == ctrl for x in ins]
        n_bad = sum(bad)
        for j, x in enumerate(ins):  # @line L8
            others_bad = n_bad - (1 if bad[j] else 0)
            if others_bad == 0:  # @line L9
                blocked = prefix[j] | suffix[j + 1]
                out |= tag[x] - blocked  # @line L10
        tag[name] = out
    return val, tag


def tagged_sites(circuit, vector, fin=None):
    """Sites whose tag reaches some primary output for this vector."""
    _, tag = tag_sets(circuit, vector, fin)
    reached = set()
    for o in circuit.outputs:
        reached |= tag[o]  # @line L11
    return reached


def observable_sites(circuit, vector):
    """Brute force: sites whose flip changes some primary output for this vector."""
    good = simulate(circuit, vector)
    result = set()
    for t in circuit.lines():
        bad = simulate(circuit, vector, flip=t)
        if any(bad[o] != good[o] for o in circuit.outputs):
            result.add(t)
    return result


def tag_coverage(circuit, vectors, sites=None):
    """Observability-based coverage of a vector set: (covered sites, ratio as a Fraction)."""
    if sites is None:
        sites = circuit.lines()
    sites = list(sites)
    fin = fanin_cones(circuit)
    covered = set()  # @line L2
    for v in vectors:  # @line L3
        covered |= tagged_sites(circuit, v, fin)
    covered &= set(sites)
    return covered, Fraction(len(covered), len(sites))  # @line L12


def exact_coverage(circuit, vectors, sites=None):
    """The same ratio with the brute-force observable sets."""
    if sites is None:
        sites = circuit.lines()
    sites = list(sites)
    covered = set()
    for v in vectors:
        covered |= observable_sites(circuit, v)
    covered &= set(sites)
    return covered, Fraction(len(covered), len(sites))


def example_circuit():
    """The circuit of the page: x reconverges at the OR gate y."""
    return Circuit(
        inputs=["x", "b", "c", "d"],
        gates=[("p", "AND", ["x", "b"]),
               ("q", "AND", ["x", "c"]),
               ("y", "OR", ["p", "q"]),
               ("z", "AND", ["q", "d"])],
        outputs=["y", "z"])


if __name__ == "__main__":
    c = example_circuit()
    vectors = [dict(x=0, b=1, c=1, d=0), dict(x=1, b=0, c=1, d=1)]
    for v in vectors:
        val, tag = tag_sets(c, v)
        print(v, {l: sorted(tag[l]) for l in c.lines()})
        print("  tagged", sorted(tagged_sites(c, v)), "exact", sorted(observable_sites(c, v)))
    print(tag_coverage(c, vectors), exact_coverage(c, vectors))
