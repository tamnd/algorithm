# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lalr-lookahead-computation/. The authors are listed in prov/VAAJVS.jsonl.

"""LALR(1) lookahead sets by the relations of DeRemer and Pennello.

lalr_lookaheads(productions) builds the LR(0) automaton of the grammar
augmented with S' -> S, and computes for every completed item of every state
the set of LALR(1) lookaheads, through the relations "reads", "includes" and
"lookback" and two runs of the Digraph algorithm.

A production is (lhs, rhs) with rhs a tuple of symbols. The left sides are the
nonterminals; every other symbol is a terminal. The first production's left
side is the start symbol. Production i of the input is production i + 1 of the
augmented grammar; production 0 is S' -> S. The grammar should be reduced:
every nonterminal reachable from the start symbol and deriving some terminal
string.
"""

from collections.abc import Hashable, Iterable, Mapping, Sequence
from dataclasses import dataclass

END = "$"

Transition = tuple[int, str]  # (state p, nonterminal A): the transition of p on A


@dataclass
class Lookaheads:
    productions: list[tuple[str, tuple[str, ...]]]  # the augmented grammar
    kernels: list[frozenset[tuple[int, int]]]  # state -> kernel items (production, dot)
    goto: dict[tuple[int, str], int]
    transitions: list[Transition]  # the nonterminal transitions, the set X
    dr: dict[Transition, frozenset[str]]
    reads: dict[Transition, list[Transition]]
    read: dict[Transition, frozenset[str]]
    includes: dict[Transition, list[Transition]]
    follow: dict[Transition, frozenset[str]]
    la: dict[tuple[int, int], frozenset[str]]  # (state, production) -> lookaheads of the completed item


def digraph(nodes: Iterable[Hashable], rel: Mapping[Hashable, Sequence[Hashable]],
            base: Mapping[Hashable, Iterable]) -> dict:
    """F(x) = base(x) united with F(y) for every y reachable from x by rel.

    The Digraph algorithm of DeRemer and Pennello: a depth-first search that
    finds the strongly connected components of rel, as Tarjan's algorithm does,
    and gives every node of a component the same set. Iterative, so long chains
    do not exhaust the call stack.
    """
    nodes = list(nodes)
    infinity = len(nodes) + 1
    n = {x: 0 for x in nodes}
    f: dict = {}
    stack: list = []
    for start in nodes:
        if n[start]:  # @line L8
            continue
        stack.append(start)  # @line L9
        n[start] = len(stack)
        f[start] = set(base[start])
        frames = [(start, len(stack), 0)]  # (x, d, index of the next successor)
        while frames:
            x, d, i = frames[-1]
            succ = rel[x]
            if i < len(succ):
                frames[-1] = (x, d, i + 1)
                y = succ[i]
                if n[y] == 0:  # @line L10
                    stack.append(y)
                    n[y] = len(stack)
                    f[y] = set(base[y])
                    frames.append((y, len(stack), 0))
                    continue
                n[x] = min(n[x], n[y])  # @line L11
                f[x] |= f[y]
                continue
            frames.pop()
            if n[x] == d:  # @line L12
                while True:
                    top = stack.pop()
                    n[top] = infinity
                    f[top] = f[x]
                    if top == x:
                        break
            if frames:  # back in the caller: line L11 for the edge parent -> x
                parent = frames[-1][0]
                n[parent] = min(n[parent], n[x])
                f[parent] |= f[x]
    return {x: frozenset(s) for x, s in f.items()}


def lr0_automaton(prods: Sequence[tuple[str, tuple[str, ...]]], nts: set[str]):
    """Kernels in breadth-first order and the GOTO function of the LR(0) automaton."""
    order: list[str] = []
    for _, rhs in prods:
        for x in rhs:
            if x not in order:
                order.append(x)
    rank = {x: i for i, x in enumerate(order)}
    by_lhs: dict[str, list[int]] = {}
    for i, (a, _) in enumerate(prods):
        by_lhs.setdefault(a, []).append(i)

    def closure(kernel: frozenset) -> list[tuple[int, int]]:
        out = set(kernel)
        todo = list(kernel)
        while todo:
            p, d = todo.pop()
            rhs = prods[p][1]
            if d < len(rhs) and rhs[d] in nts:
                for q in by_lhs[rhs[d]]:
                    if (q, 0) not in out:
                        out.add((q, 0))
                        todo.append((q, 0))
        return sorted(out)

    kernels = [frozenset({(0, 0)})]
    number = {kernels[0]: 0}
    goto: dict[tuple[int, str], int] = {}
    q = 0
    while q < len(kernels):
        buckets: dict[str, list[tuple[int, int]]] = {}
        for p, d in closure(kernels[q]):
            if d < len(prods[p][1]):
                buckets.setdefault(prods[p][1][d], []).append((p, d + 1))
        for x in sorted(buckets, key=rank.__getitem__):
            nxt = frozenset(buckets[x])
            if nxt not in number:
                number[nxt] = len(kernels)
                kernels.append(nxt)
            goto[(q, x)] = number[nxt]
        q += 1
    return kernels, goto


def nullable_symbols(prods: Sequence[tuple[str, tuple[str, ...]]]) -> set[str]:
    """The nonterminals that derive the empty string, in time linear in the grammar size."""
    nts = {a for a, _ in prods}
    missing = [sum(1 for x in rhs if x in nts) if all(x in nts for x in rhs) else -1 for _, rhs in prods]
    uses: dict[str, list[int]] = {}
    for i, (_, rhs) in enumerate(prods):
        if missing[i] > 0:
            for x in rhs:
                uses.setdefault(x, []).append(i)
    nullable: set[str] = set()
    todo = [a for i, (a, _) in enumerate(prods) if missing[i] == 0]
    while todo:
        a = todo.pop()
        if a in nullable:
            continue
        nullable.add(a)
        for i in uses.get(a, []):
            missing[i] -= 1
            if missing[i] == 0:
                todo.append(prods[i][0])
    return nullable


def lalr_lookaheads(productions: Sequence[tuple[str, Sequence[str]]]) -> Lookaheads:
    """The LALR(1) lookahead set of every completed item of the LR(0) automaton."""
    user = [(a, tuple(rhs)) for a, rhs in productions]
    names = []
    for a, _ in user:
        if a not in names:
            names.append(a)
    start = names[0]
    aug = start + "'"
    symbols = set(names) | {x for _, rhs in user for x in rhs}
    while aug in symbols:
        aug += "'"
    prods = [(aug, (start,))] + user
    nts = set(names) | {aug}
    nullable = nullable_symbols(prods)

    kernels, goto = lr0_automaton(prods, nts)  # @line L1
    transitions = [(p, x) for (p, x) in goto if x in nts]

    dr: dict[Transition, frozenset[str]] = {}
    reads: dict[Transition, list[Transition]] = {}
    out_edges: dict[int, list[str]] = {}
    for (p, x) in goto:
        out_edges.setdefault(p, []).append(x)
    for (p, a) in transitions:
        r = goto[(p, a)]
        terms = {t for t in out_edges.get(r, []) if t not in nts}  # @line L2
        if (0, 1) in kernels[r]:  # r holds S' -> S., so the end marker can follow
            terms.add(END)
        dr[(p, a)] = frozenset(terms)
        reads[(p, a)] = [(r, c) for c in out_edges.get(r, []) if c in nts and c in nullable]  # @line L3

    read = digraph(transitions, reads, dr)  # @line L4

    by_lhs: dict[str, list[int]] = {}
    for i, (a, _) in enumerate(prods):
        by_lhs.setdefault(a, []).append(i)
    includes: dict[Transition, list[Transition]] = {t: [] for t in transitions}
    for (pp, b) in transitions:
        for i in by_lhs[b]:
            rhs = prods[i][1]
            suffix_nullable = [True] * (len(rhs) + 1)  # suffix_nullable[j]: rhs[j:] is nullable
            for j in range(len(rhs) - 1, -1, -1):
                suffix_nullable[j] = suffix_nullable[j + 1] and rhs[j] in nullable
            s = pp
            for j, x in enumerate(rhs):
                if x in nts and suffix_nullable[j + 1]:
                    includes[(s, x)].append((pp, b))  # @line L5
                s = goto[(s, x)]

    follow = digraph(transitions, includes, read)  # @line L6

    la: dict[tuple[int, int], set[str]] = {}
    for (p, a) in transitions:
        for i in by_lhs[a]:
            q = p
            for x in prods[i][1]:
                q = goto[(q, x)]
            la.setdefault((q, i), set()).update(follow[(p, a)])  # @line L7

    return Lookaheads(
        productions=prods, kernels=kernels, goto=goto, transitions=transitions, dr=dr, reads=reads,
        read=read, includes=includes, follow=follow, la={k: frozenset(v) for k, v in la.items()})
