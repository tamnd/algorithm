# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bottom-up-enumerative-synthesis/. The authors are listed in prov/Q97T2A.jsonl.
"""Bottom-up enumerative synthesis with observational equivalence.

The grammar has two sorts:
    I ::= x | y | 0 | 1 | I + I | I - I | I * I | ite(B, I, I)
    B ::= I <= I
Programs are trees: "x", "y", "0", "1", (op, p, q) with op in "+", "-", "*",
("<=", p, q) and ("ite", b, p, q). The size of a program is its number of
nodes. An input is a pair (x, y) of ints.

synthesize(examples, max_size) builds programs by size from smaller ones. It
computes the vector of outputs of each new program on the example inputs from
the vectors of its parts. With prune=True it keeps a program only if no kept
program of its sort has the same vector (observational equivalence). It returns
the first program whose vector equals the wanted outputs, which is a program of
least size, together with the number of programs it built.
"""

LEAVES = ("x", "y", "0", "1")
INT_OPS = ("+", "-", "*")


def evaluate(p, inp):
    """The value of program p on the input pair inp."""
    if p == "x":
        return inp[0]
    if p == "y":
        return inp[1]
    if p == "0":
        return 0
    if p == "1":
        return 1
    op = p[0]
    if op == "ite":
        return evaluate(p[2], inp) if evaluate(p[1], inp) else evaluate(p[3], inp)
    a, b = evaluate(p[1], inp), evaluate(p[2], inp)
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "<=":
        return a <= b
    raise ValueError(f"unknown operator {op!r}")


def size(p):
    if isinstance(p, str):
        return 1
    return 1 + sum(size(q) for q in p[1:])


def show(p):
    if isinstance(p, str):
        return p
    if p[0] == "ite":
        return f"ite({show(p[1])}, {show(p[2])}, {show(p[3])})"
    return f"({show(p[1])} {p[0]} {show(p[2])})"


def _leaf_vector(t, inputs):
    return tuple(evaluate(t, i) for i in inputs)


def synthesize(examples, max_size, prune=True):
    """(a smallest program meeting the examples or None, number of programs built)."""
    inputs = [i for i, _ in examples]
    target = tuple(o for _, o in examples)
    ints = {}   # size -> list of (program, vector) of sort I
    bools = {}  # size -> list of (program, vector) of sort B
    seen_int = set()  # @line L1
    seen_bool = set()
    built = 0

    def keep(bank, seen, s, prog, vec):
        nonlocal built
        built += 1
        if prune and vec in seen:  # @line L5
            return False
        seen.add(vec)  # @line L6
        bank.setdefault(s, []).append((prog, vec))
        return True

    for s in range(1, max_size + 1):  # @line L2
        new_ints = []
        if s == 1:
            for t in LEAVES:
                new_ints.append((t, _leaf_vector(t, inputs)))
        else:
            for s1 in range(1, s - 1):  # @line L3
                s2 = s - 1 - s1
                for p, u in ints.get(s1, ()):
                    for q, v in ints.get(s2, ()):
                        for op in INT_OPS:
                            if op == "+":
                                w = tuple(a + b for a, b in zip(u, v))  # @line L4
                            elif op == "-":
                                w = tuple(a - b for a, b in zip(u, v))
                            else:
                                w = tuple(a * b for a, b in zip(u, v))
                            new_ints.append(((op, p, q), w))
                        keep(bools, seen_bool, s, ("<=", p, q), tuple(a <= b for a, b in zip(u, v)))
            for sb in range(3, s - 1):
                for b, bv in bools.get(sb, ()):
                    for s1 in range(1, s - sb - 1):
                        s2 = s - 1 - sb - s1
                        for p, u in ints.get(s1, ()):
                            for q, v in ints.get(s2, ()):
                                w = tuple(x if c else z for c, x, z in zip(bv, u, v))
                                new_ints.append((("ite", b, p, q), w))
        for prog, vec in new_ints:
            if keep(ints, seen_int, s, prog, vec) and vec == target:  # @line L7
                return prog, built
    return None, built  # @line L8
