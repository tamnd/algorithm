# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/expression-dag/. The authors are listed in prov/46Z0DH.jsonl.

"""A hash-consed expression DAG: every distinct subexpression is stored once.

Nodes are small integers into the arrays of an ExprDAG. A node is a constant
(a Fraction), a symbol (a name), or an operator in + - * ^ with two child
nodes; the second child of ^ is a constant integer k >= 0. Because children
are created before their parents, every child id is smaller than its parent
id, so the arrays are already in topological order.

Cost model: make costs one hash-table lookup, O(1) expected. eval, subs and
diff visit each distinct node reachable from the root once, O(m) node visits
for m such nodes, whatever the size of the unfolded tree. equal is O(1).
"""

from fractions import Fraction
from typing import Dict, List, Optional, Tuple, Union

Number = Union[int, Fraction]
Key = Tuple[str, object, Tuple[int, ...]]


class ExprDAG:
    """A store of hash-consed expression nodes, with one method per operation."""

    def __init__(self) -> None:
        self.op: List[str] = []
        self.val: List[object] = []
        self.kids: List[Tuple[int, ...]] = []
        self.table: Dict[Key, int] = {}

    # construction -----------------------------------------------------------

    def make(self, op: str, val: object, kids: Tuple[int, ...]) -> int:
        """The unique node with this operator, value and children. O(1) expected."""
        key: Key = (op, val, kids)  # @line L1
        found = self.table.get(key)
        if found is not None:  # @line L2
            return found
        i = len(self.op)  # @line L3
        self.op.append(op)
        self.val.append(val)
        self.kids.append(kids)
        self.table[key] = i  # @line L4
        return i  # @line L5

    def const(self, c: Number) -> int:
        return self.make("const", Fraction(c), ())

    def sym(self, name: str) -> int:
        return self.make("sym", name, ())

    def add(self, a: int, b: int) -> int:
        return self.make("+", None, (a, b))

    def sub(self, a: int, b: int) -> int:
        return self.make("-", None, (a, b))

    def mul(self, a: int, b: int) -> int:
        return self.make("*", None, (a, b))

    def power(self, a: int, k: int) -> int:
        if k < 0:
            raise ValueError("exponent must be a nonnegative integer")
        return self.make("^", None, (a, self.const(k)))

    # smart constructors used by diff; they keep the value ---------------------

    def _is_const(self, u: int, c: Optional[int] = None) -> bool:
        return self.op[u] == "const" and (c is None or self.val[u] == c)

    def s_add(self, a: int, b: int) -> int:
        if self._is_const(a) and self._is_const(b):
            return self.const(self.val[a] + self.val[b])  # type: ignore[operator]
        if self._is_const(a, 0):
            return b
        if self._is_const(b, 0):
            return a
        return self.add(a, b)

    def s_sub(self, a: int, b: int) -> int:
        if self._is_const(a) and self._is_const(b):
            return self.const(self.val[a] - self.val[b])  # type: ignore[operator]
        if self._is_const(b, 0):
            return a
        return self.sub(a, b)

    def s_mul(self, a: int, b: int) -> int:
        if self._is_const(a) and self._is_const(b):
            return self.const(self.val[a] * self.val[b])  # type: ignore[operator]
        if self._is_const(a, 0) or self._is_const(b, 0):
            return self.const(0)
        if self._is_const(a, 1):
            return b
        if self._is_const(b, 1):
            return a
        return self.mul(a, b)

    # walks --------------------------------------------------------------------

    def reachable(self, root: int) -> List[int]:
        """Distinct nodes reachable from root, in increasing id order (children first)."""
        seen = {root}
        stack = [root]
        while stack:
            u = stack.pop()
            for k in self.kids[u]:
                if k not in seen:
                    seen.add(k)
                    stack.append(k)
        return sorted(seen)

    def eval(self, root: int, env: Dict[str, Number]) -> Fraction:
        """Value of root when each symbol s is env[s]. O(m) visits, m distinct nodes."""
        v: Dict[int, Fraction] = {}
        for u in self.reachable(root):
            op = self.op[u]
            if op == "const":
                v[u] = self.val[u]  # type: ignore[assignment]
            elif op == "sym":
                v[u] = Fraction(env[self.val[u]])  # type: ignore[index]
            else:
                a, b = v[self.kids[u][0]], v[self.kids[u][1]]
                if op == "+":
                    v[u] = a + b
                elif op == "-":
                    v[u] = a - b
                elif op == "*":
                    v[u] = a * b
                else:
                    v[u] = a ** int(b)
        return v[root]

    def subs(self, root: int, x: str, r: int) -> int:
        """root with the symbol x replaced by the node r. O(m) visits."""
        res: Dict[int, int] = {}
        for u in self.reachable(root):
            if self.op[u] == "sym" and self.val[u] == x:
                res[u] = r
            elif not self.kids[u]:
                res[u] = u
            else:
                res[u] = self.make(self.op[u], None, tuple(res[k] for k in self.kids[u]))
        return res[root]

    def diff(self, root: int, x: str) -> int:
        """Derivative of root with respect to x. O(m) visits and O(m) new nodes."""
        d: Dict[int, int] = {}
        for u in self.reachable(root):
            op = self.op[u]
            if op == "const":
                d[u] = self.const(0)
            elif op == "sym":
                d[u] = self.const(1 if self.val[u] == x else 0)
            else:
                a, b = self.kids[u]
                if op == "+":
                    d[u] = self.s_add(d[a], d[b])
                elif op == "-":
                    d[u] = self.s_sub(d[a], d[b])
                elif op == "*":
                    d[u] = self.s_add(self.s_mul(d[a], b), self.s_mul(a, d[b]))
                else:
                    k = int(self.val[b])  # type: ignore[arg-type]
                    if k == 0:
                        d[u] = self.const(0)
                    else:
                        pk = self.const(1) if k == 1 else (a if k == 2 else self.power(a, k - 1))
                        d[u] = self.s_mul(self.s_mul(self.const(k), pk), d[a])
        return d[root]

    def equal(self, a: int, b: int) -> bool:
        """Syntactic identity of the two expressions: one integer comparison."""
        return a == b

    def dag_size(self, root: int) -> int:
        """Number of distinct nodes reachable from root."""
        return len(self.reachable(root))

    def tree_size(self, root: int) -> int:
        """Number of nodes of the unfolded tree; may be exponential in dag_size."""
        t: Dict[int, int] = {}
        for u in self.reachable(root):
            t[u] = 1 + sum(t[k] for k in self.kids[u])
        return t[root]

    def to_string(self, root: int) -> str:
        """Fully parenthesized infix form of the unfolded tree (** for powers)."""
        s: Dict[int, str] = {}
        for u in self.reachable(root):
            op = self.op[u]
            if op == "const":
                c: Fraction = self.val[u]  # type: ignore[assignment]
                s[u] = "(%d)" % c.numerator if c.denominator == 1 else "Fraction(%d, %d)" % (c.numerator, c.denominator)
            elif op == "sym":
                s[u] = str(self.val[u])
            else:
                a, b = self.kids[u]
                s[u] = "(" + s[a] + " " + ("**" if op == "^" else op) + " " + s[b] + ")"
        return s[root]

    def check_invariant(self) -> None:
        """Arrays agree, the table is a bijection onto the nodes, children precede parents."""
        n = len(self.op)
        assert len(self.val) == n and len(self.kids) == n and len(self.table) == n
        for i in range(n):
            assert self.table[(self.op[i], self.val[i], self.kids[i])] == i
            op = self.op[i]
            if op == "const":
                assert isinstance(self.val[i], Fraction) and self.kids[i] == ()
            elif op == "sym":
                assert isinstance(self.val[i], str) and self.kids[i] == ()
            else:
                assert op in ("+", "-", "*", "^") and len(self.kids[i]) == 2
                assert all(0 <= k < i for k in self.kids[i])
                if op == "^":
                    k = self.kids[i][1]
                    assert self.op[k] == "const" and self.val[k].denominator == 1  # type: ignore[union-attr]
                    assert self.val[k] >= 0  # type: ignore[operator]
