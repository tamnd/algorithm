# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/carry-lookahead-adder/. The authors are listed in prov/ZGRFB8.jsonl.

"""A gate-level model of the hierarchical carry-lookahead adder.

A wire is a pair (bit, arrival time). Every AND, OR and XOR gate has delay
1, whatever its fan-in. The lookahead units have r children each, so the
largest fan-in is r + 1. The function returns the sum bits, the carry out,
the gate counts and the depth of the circuit, so that tests can check both
the values and the cost claims of the page.
"""

from dataclasses import dataclass, field

Wire = tuple[int, int]


@dataclass
class Counts:
    """Gates used by the circuit, and the largest fan-in seen."""

    and_gates: int = 0
    or_gates: int = 0
    xor_gates: int = 0
    max_fan_in: int = 0
    levels: int = 0


@dataclass
class Node:
    """A node of the lookahead tree: its (G, P) pair and its children."""

    g: Wire
    p: Wire | None
    children: list["Node"] = field(default_factory=list)
    leaf: int = -1
    carry_in: Wire | None = None


def _and(ws: list[Wire], k: Counts) -> Wire:
    if len(ws) == 1:
        return ws[0]
    k.and_gates += 1
    k.max_fan_in = max(k.max_fan_in, len(ws))
    return (int(all(w[0] for w in ws)), max(w[1] for w in ws) + 1)


def _or(ws: list[Wire], k: Counts) -> Wire:
    if len(ws) == 1:
        return ws[0]
    k.or_gates += 1
    k.max_fan_in = max(k.max_fan_in, len(ws))
    return (int(any(w[0] for w in ws)), max(w[1] for w in ws) + 1)


def _xor(x: Wire, y: Wire, k: Counts) -> Wire:
    k.xor_gates += 1
    return (x[0] ^ y[0], max(x[1], y[1]) + 1)


def _lookahead(ch: list[Node], c: Wire | None, k: Counts) -> Wire:
    """g[m-1] or p[m-1] g[m-2] or ... or p[m-1] ... p[0] c, for m = len(ch)."""
    m = len(ch)
    terms = [ch[m - 1].g]
    for j in range(m - 2, -1, -1):
        terms.append(_and([ch[t].p for t in range(m - 1, j, -1)] + [ch[j].g], k))
    if c is not None:
        terms.append(_and([ch[t].p for t in range(m - 1, -1, -1)] + [c], k))
    return _or(terms, k)


def cla_add(a: list[int], b: list[int], c0: int = 0, r: int = 4):
    """Add two n-bit numbers given low bit first.

    Returns (sum bits, carry out, counts, depth).
    """
    n = len(a)
    assert n == len(b) and n >= 1 and r >= 2
    k = Counts()
    ins_a = [(x, 0) for x in a]
    ins_b = [(y, 0) for y in b]
    cin: Wire = (c0, 0)
    level = []
    for i in range(n):
        g = _and([ins_a[i], ins_b[i]], k)  # @line L1
        p = _xor(ins_a[i], ins_b[i], k)  # @line L1
        level.append(Node(g, p, leaf=i))  # @line L2
    h = 0  # @line L2
    while True:  # @line L3
        h += 1  # @line L4
        groups = [level[j:j + r] for j in range(0, len(level), r)]  # @line L4
        root = len(groups) == 1
        nxt = []
        for ch in groups:  # @line L5
            if root:
                nxt.append(Node((0, 0), None, ch))
            else:
                big_g = _lookahead(ch, None, k)  # @line L5
                big_p = _and([w.p for w in ch], k)  # @line L5
                nxt.append(Node(big_g, big_p, ch))
        level = nxt
        if root:  # @line L6
            break
    k.levels = h
    top = level[0]
    top.carry_in = cin  # @line L7
    stack = [top]
    carries: list[Wire] = [cin] * n
    while stack:  # @line L8
        node = stack.pop()
        if node.leaf >= 0:
            carries[node.leaf] = node.carry_in
            continue
        ch = node.children
        ch[0].carry_in = node.carry_in  # @line L9
        for t in range(1, len(ch)):
            ch[t].carry_in = _lookahead(ch[:t], node.carry_in, k)  # @line L9
        stack.extend(ch)
    cout = _lookahead(top.children, cin, k)  # @line L10
    leaves = _leaves(top)
    s = [_xor(leaves[i].p, carries[i], k) for i in range(n)]  # @line L11
    depth = max([w[1] for w in s] + [cout[1]])
    return [w[0] for w in s], cout[0], k, depth  # @line L12


def _leaves(top: Node) -> list[Node]:
    out, stack = [], [top]
    while stack:
        node = stack.pop()
        if node.leaf >= 0:
            out.append(node)
        else:
            stack.extend(node.children)
    out.sort(key=lambda x: x.leaf)
    return out


def to_bits(x: int, n: int) -> list[int]:
    return [(x >> i) & 1 for i in range(n)]


def from_bits(bits: list[int]) -> int:
    return sum(bit << i for i, bit in enumerate(bits))


def add(x: int, y: int, n: int, c0: int = 0, r: int = 4) -> int:
    """x + y + c0 for 0 <= x, y < 2^n, through the circuit."""
    s, cout, _, _ = cla_add(to_bits(x, n), to_bits(y, n), c0, r)
    return from_bits(s) + (cout << n)
