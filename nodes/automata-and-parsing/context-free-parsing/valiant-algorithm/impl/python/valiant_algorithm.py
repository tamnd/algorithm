# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/valiant-algorithm/. The authors are listed in prov/44TRAH.jsonl.
"""Valiant's algorithm: context-free recognition by Boolean matrix multiplication.

A grammar is a list of productions (A, rhs), where rhs is a tuple of symbols.
The nonterminals are the left sides and the start symbol; every other symbol
is a terminal. VALIANT needs Chomsky normal form: A -> B C with B and C
nonterminals, A -> a with a terminal, and S -> () only for a start symbol S
that is on no right side. to_cnf converts any grammar.

The table T is kept as one Boolean matrix per nonterminal A: rows[A][i] is an
int whose bit j is set when A derives w[i:j]. Positions are 0..n, padded to
N, a power of two. The recursion follows Okhotin's formulation; its depth is
log2 N, and every product goes through one pluggable function bmm.
"""


def bmm_rows(x, y):
    """Boolean product of x (r rows, each an int over k columns) and y (k rows,
    each an int over c columns): row i of the result is the OR of the rows
    y[t] for the set bits t of x[i]."""
    out = []
    for row in x:
        acc, t = 0, 0
        while row:
            if row & 1:
                acc |= y[t]
            row >>= 1
            t += 1
        out.append(acc)
    return out


def is_cnf(prods, start):
    nts = {a for a, _ in prods} | {start}
    for a, rhs in prods:
        if len(rhs) == 2 and rhs[0] in nts and rhs[1] in nts:
            if start in rhs and (start, ()) in prods:
                return False
        elif len(rhs) == 1 and rhs[0] not in nts:
            pass
        elif len(rhs) == 0 and a == start:
            pass
        else:
            return False
    if (start, ()) in prods and any(start in rhs for _, rhs in prods):
        return False
    return True


class Valiant:
    """Fills the recognition table of w for a grammar in CNF."""

    def __init__(self, prods, start, w, bmm=None):
        prods = [(a, tuple(r)) for a, r in prods]
        if not is_cnf(prods, start):
            raise ValueError("the grammar is not in Chomsky normal form")
        self.start, self.w, self.n = start, list(w), len(w)
        self.bmm = bmm or bmm_rows
        self.calls = 0  # number of calls of bmm
        self.cells = 0  # number of cells finished at line L9
        self.products = {}  # block size -> number of block products (lines L13 to L15)
        self.nts = sorted({a for a, _ in prods} | {start})
        self.pairs = sorted({rhs for _, rhs in prods if len(rhs) == 2})
        self.lhs = {bc: sorted({a for a, r in prods if r == bc}) for bc in self.pairs}
        self.by_term = {}
        for a, rhs in prods:
            if len(rhs) == 1:
                self.by_term.setdefault(rhs[0], set()).add(a)
        self.accepts_empty = (start, ()) in prods
        size = 1
        while size < self.n + 1:
            size *= 2
        self.N = size
        self.rows = {a: [0] * size for a in self.nts}  # T, one matrix per nonterminal
        self.prod = {bc: [0] * size for bc in self.pairs}  # P, one matrix per pair (B, C)
        for i, c in enumerate(self.w):  # @line L1
            for a in self.by_term.get(c, ()):
                self.rows[a][i] |= 1 << (i + 1)
        self.compute(0, size)  # @line L2

    def compute(self, l, m):
        """Fill T for all cells l <= i < j < m."""
        if m - l >= 2:  # @line L5
            h = (l + m) // 2
            self.compute(l, h)  # @line L6
            self.compute(h, m)
            self.complete(l, h, h, m)  # @line L7

    def _block(self, mat, r0, r1, c0, c1):
        mask = (1 << (c1 - c0)) - 1
        return [(mat[i] >> c0) & mask for i in range(r0, r1)]

    def _add_product(self, r0, r1, k0, k1, c0, c1):
        """P[r0:r1, c0:c1] |= T[r0:r1, k0:k1] x T[k0:k1, c0:c1], for every pair (B, C)."""
        self.products[r1 - r0] = self.products.get(r1 - r0, 0) + 1
        for b, c in self.pairs:
            x = self._block(self.rows[b], r0, r1, k0, k1)
            if not any(x):
                continue
            y = self._block(self.rows[c], k0, k1, c0, c1)
            if not any(y):
                continue
            self.calls += 1
            z = self.bmm(x, y)
            target = self.prod[(b, c)]
            for t, row in enumerate(z):
                target[r0 + t] |= row << c0

    def complete(self, l, m, l2, m2):
        """Fill T for rows l..m-1 and columns l2..m2-1, where m <= l2. Needs: T is
        done inside [l, m) and inside [l2, m2), and P holds every split k in [m, l2)."""
        if m - l == 1:  # @line L8
            i, j = l, l2
            if j > i + 1:  # @line L9
                bit = 1 << j
                for bc in self.pairs:
                    if self.prod[bc][i] & bit:
                        for a in self.lhs[bc]:
                            self.rows[a][i] |= bit
                self.cells += 1
            return  # @line L10
        a = (l + m) // 2  # @line L11
        b = (l2 + m2) // 2
        self.complete(a, m, l2, b)  # @line L12
        self._add_product(l, a, a, m, l2, b)  # @line L13
        self.complete(l, a, l2, b)
        self._add_product(a, m, l2, b, b, m2)  # @line L14
        self.complete(a, m, b, m2)
        self._add_product(l, a, a, m, b, m2)  # @line L15
        self._add_product(l, a, l2, b, b, m2)
        self.complete(l, a, b, m2)  # @line L16

    def derives(self, a, i, j):
        """True when nonterminal a derives w[i:j], for 0 <= i < j <= n."""
        return bool((self.rows[a][i] >> j) & 1)

    def table(self):
        """The set of (A, i, j) with i < j and A =>* w[i:j]."""
        out = set()
        for a in self.nts:
            for i in range(self.n):
                row = self.rows[a][i]
                for j in range(i + 1, self.n + 1):
                    if (row >> j) & 1:
                        out.add((a, i, j))
        return out

    def accepts(self):
        if self.n == 0:  # @line L3
            return self.accepts_empty
        return self.derives(self.start, 0, self.n)  # @line L4


def recognize(prods, start, w, bmm=None):
    """True when w is in L(G), for G in Chomsky normal form."""
    return Valiant(prods, start, w, bmm).accepts()


def to_cnf(prods, start):
    """An equivalent grammar in Chomsky normal form, and its start symbol."""
    prods = [(a, tuple(r)) for a, r in prods]
    nts = {a for a, _ in prods} | {start}
    used = set(nts) | {x for _, r in prods for x in r}
    count = [0]

    def fresh(base):
        while True:
            count[0] += 1
            name = "<%s%d>" % (base, count[0])
            if name not in used:
                used.add(name)
                return name

    s0 = fresh("S")
    rules = [(s0, (start,))] + prods
    nts.add(s0)
    # TERM: terminals inside long right sides get their own nonterminal
    term = {}
    step = []
    for a, rhs in rules:
        if len(rhs) >= 2:
            new = []
            for x in rhs:
                if x not in nts:
                    if x not in term:
                        term[x] = fresh("T")
                    x = term[x]
                new.append(x)
            rhs = tuple(new)
        step.append((a, rhs))
    for x, t in term.items():
        step.append((t, (x,)))
        nts.add(t)
    # BIN: right sides of length at most 2
    rules = []
    for a, rhs in step:
        while len(rhs) > 2:
            t = fresh("B")
            nts.add(t)
            rules.append((a, (rhs[0], t)))
            a, rhs = t, rhs[1:]
        rules.append((a, rhs))
    # DEL: remove empty right sides, keeping S0 -> () when S0 is nullable
    nullable = set()
    changed = True
    while changed:
        changed = False
        for a, rhs in rules:
            if a not in nullable and all(x in nullable for x in rhs):
                nullable.add(a)
                changed = True
    step = set()
    for a, rhs in rules:
        if len(rhs) == 2:
            step.add((a, rhs))
            if rhs[1] in nullable:
                step.add((a, rhs[:1]))
            if rhs[0] in nullable:
                step.add((a, rhs[1:]))
        elif len(rhs) == 1:
            step.add((a, rhs))
    # UNIT: replace A -> B by A -> beta for every non-unit B -> beta
    unit = {a: {a} for a in nts}
    changed = True
    while changed:
        changed = False
        for a, rhs in step:
            if len(rhs) == 1 and rhs[0] in nts:
                for x in list(unit):
                    if a in unit[x] and rhs[0] not in unit[x]:
                        unit[x].add(rhs[0])
                        changed = True
    out = set()
    for x in nts:
        for a, rhs in step:
            if a in unit[x] and not (len(rhs) == 1 and rhs[0] in nts):
                out.add((x, rhs))
    # keep only productions whose nonterminals derive some nonempty string, so
    # that every nonterminal on a right side has a production
    gen = set()
    changed = True
    while changed:
        changed = False
        for a, rhs in out:
            if a not in gen and all(x in gen or x not in nts for x in rhs):
                gen.add(a)
                changed = True
    out = {(a, rhs) for a, rhs in out if all(x in gen or x not in nts for x in rhs)}
    if s0 in nullable:
        out.add((s0, ()))
    return sorted(out), s0
