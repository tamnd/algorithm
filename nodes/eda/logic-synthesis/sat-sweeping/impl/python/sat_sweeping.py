# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sat-sweeping/. The authors are listed in prov/D7SVKR.jsonl.

"""SAT sweeping: build a functionally reduced AIG (a FRAIG).

An AIG has node 0 (the constant 0), inputs 1..n and AND nodes after
them. A literal is 2 v + c: node v, complemented when c = 1. The input
AIG is given as `n` and a list `ands` of fanin literal pairs; node
n + 1 + i has the fanins ands[i]. Outputs are literals.

The sweep copies the AIG in topological order into a new AIG. Each new
AND node gets a simulation signature over a set of input patterns. Two
nodes whose signatures are equal, or equal after complement, are
candidates. A candidate pair is checked with SAT on the miter of the two
cones. When the miter is unsatisfiable the new node is replaced by the
old one (with the phase); when it is satisfiable the counterexample is
added to the patterns, which splits the pair. At the end no two nodes of
the result compute the same function or its complement.
"""

import random
from typing import List, Optional, Sequence, Tuple


# ---------------------------------------------------------------- SAT
def dpll(clauses: Sequence[Sequence[int]], n_vars: int) -> Optional[List[int]]:
    """A small DPLL solver. Return a model as a list of 0/1 for vars 1..n, or None."""
    assign: dict = {}

    def value(lit):
        v = assign.get(abs(lit))
        return None if v is None else (v if lit > 0 else 1 - v)

    def propagate(trail):
        changed = True
        while changed:
            changed = False
            for cl in clauses:
                free, sat = None, False
                n_free = 0
                for lit in cl:
                    val = value(lit)
                    if val == 1:
                        sat = True
                        break
                    if val is None:
                        n_free += 1
                        free = lit
                if sat:
                    continue
                if n_free == 0:
                    return False
                if n_free == 1:
                    assign[abs(free)] = 1 if free > 0 else 0
                    trail.append(abs(free))
                    changed = True
        return True

    def solve():
        trail: list = []
        if not propagate(trail):
            for v in trail:
                del assign[v]
            return False
        var = next((v for v in range(1, n_vars + 1) if v not in assign), None)
        if var is None:
            return True
        for b in (1, 0):
            assign[var] = b
            if solve():
                return True
            del assign[var]
        for v in trail:
            del assign[v]
        return False

    if not solve():
        return None
    return [assign.get(v, 0) for v in range(1, n_vars + 1)]


# ---------------------------------------------------------------- AIG
class Aig:
    def __init__(self, n: int) -> None:
        self.n = n
        self.fanins: List[Tuple[int, int]] = [(0, 0)] * (n + 1)  # const and inputs
        self.table: dict = {}

    def is_and(self, v: int) -> bool:
        return v > self.n

    def add_and(self, a: int, b: int) -> int:
        """AND with constant rules and structural hashing; returns a literal."""
        if a > b:
            a, b = b, a
        if a == 0 or a == (b ^ 1):
            return 0
        if a == 1 or a == b:
            return b
        if (a, b) in self.table:
            return self.table[(a, b)]
        self.fanins.append((a, b))
        lit = 2 * (len(self.fanins) - 1)
        self.table[(a, b)] = lit
        return lit


def simulate(aig: Aig, patterns: Sequence[int], width: int) -> list:
    """Bit-parallel simulation: sig[v] holds the value of node v in each pattern."""
    mask = (1 << width) - 1
    sig = [0] + list(patterns)
    for v in range(aig.n + 1, len(aig.fanins)):
        a, b = aig.fanins[v]
        x = sig[a >> 1] ^ (mask if a & 1 else 0)
        y = sig[b >> 1] ^ (mask if b & 1 else 0)
        sig.append(x & y)
    return sig


def miter_cnf(aig: Aig, p: int, q: int):
    """CNF that is satisfiable iff literals p and q differ on some input."""
    seen, stack = set(), [p >> 1, q >> 1]
    while stack:
        v = stack.pop()
        if v not in seen:
            seen.add(v)
            if aig.is_and(v):
                stack.extend(lit >> 1 for lit in aig.fanins[v])
    var = {v: i + 1 for i, v in enumerate(sorted(seen))}

    def lit(x):
        return -var[x >> 1] if x & 1 else var[x >> 1]

    clauses = []
    if 0 in var:
        clauses.append([-var[0]])
    for v in sorted(seen):
        if aig.is_and(v):  # Tseitin: v <-> a and b
            a, b = aig.fanins[v]
            clauses += [[-var[v], lit(a)], [-var[v], lit(b)], [var[v], -lit(a), -lit(b)]]
    clauses += [[lit(p), lit(q)], [-lit(p), -lit(q)]]  # p != q
    return clauses, var


def sat_sweep(n: int, ands: Sequence[Tuple[int, int]], outputs: Sequence[int],
              n_patterns: int = 16, seed: int = 1):
    """Return (fraig, output literals, stats). stats counts SAT calls by result."""
    for i, (a, b) in enumerate(ands):
        if max(a, b) >> 1 >= n + 1 + i:
            raise ValueError("fanins must come before the node")
    rng = random.Random(seed)
    width = n_patterns
    pats = [rng.getrandbits(width) for _ in range(n)]  # @line L1: pats[i] belongs to input i + 1
    new = Aig(n)
    old_to_new = list(range(0, 2 * (n + 1), 2))  # node v of the input -> literal
    stats = {"sat": 0, "unsat": 0}

    def key_of(s):  # the phase is fixed by pattern 0: the key has bit 0 clear
        return s ^ ((1 << width) - 1) if s & 1 else s

    dead: set = set()

    def classes(sig, skip):
        return {key_of(sig[u]): u for u in range(len(new.fanins)) if u not in dead and u != skip}

    sig = simulate(new, pats, width)
    reps = classes(sig, None)
    for a, b in ands:  # @line L2
        fa = old_to_new[a >> 1] ^ (a & 1)
        fb = old_to_new[b >> 1] ^ (b & 1)
        size = len(new.fanins)
        lit = new.add_and(fa, fb)  # @line L3
        if len(new.fanins) == size:  # @line L4: a constant rule or the hash table answered
            old_to_new.append(lit)
            continue
        w = lit >> 1
        sig = simulate(new, pats, width)
        while True:  # @line L5
            r = reps.get(key_of(sig[w]))  # @line L6
            if r is None:  # @line L7: no candidate, w is a new class
                reps[key_of(sig[w])] = w
                old_to_new.append(lit)
                break
            phase = (sig[w] ^ sig[r]) & 1
            clauses, var = miter_cnf(new, 2 * w, 2 * r + phase)
            model = dpll(clauses, len(var))  # @line L8
            if model is None:  # @line L9: proved equal, use r and drop w
                stats["unsat"] += 1
                dead.add(w)
                new.table[new.fanins[w]] = 2 * r + phase
                old_to_new.append(2 * r + phase)
                break
            stats["sat"] += 1  # @line L10: the counterexample becomes a new pattern
            for i_in in range(1, n + 1):
                bit = model[var[i_in] - 1] if i_in in var else 0
                pats[i_in - 1] |= bit << width
            width += 1
            sig = simulate(new, pats, width)
            reps = classes(sig, w)
    outs = [old_to_new[o >> 1] ^ (o & 1) for o in outputs]
    res, res_outs = compact(new, outs)  # @line L11
    return res, res_outs, stats


def compact(aig: Aig, outs: Sequence[int]):
    """Copy the cones of the outputs into a fresh AIG; return (aig, outputs)."""
    res = Aig(aig.n)
    m = {v: 2 * v for v in range(aig.n + 1)}

    def copy(v):
        if v not in m:
            a, b = aig.fanins[v]
            m[v] = res.add_and(copy(a >> 1) ^ (a & 1), copy(b >> 1) ^ (b & 1))
        return m[v]

    return res, [copy(o >> 1) ^ (o & 1) for o in outs]
