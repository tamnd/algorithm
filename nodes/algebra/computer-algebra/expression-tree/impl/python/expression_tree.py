# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/expression-tree/. The authors are listed in prov/5TDXMG.jsonl.

"""Expression trees over Fraction constants, symbols and the operators
+, -, * and ^ (a power with a constant nonnegative integer exponent).

Nodes are immutable, so a subtree may be shared by several parents; every
operation treats the structure as a tree all the same. All walks use an
explicit stack, so deep trees do not hit the recursion limit.

Cost model: eval, subs, diff, size, equal and to_string each visit every
node once, so they take O(n) node visits for a tree of n nodes; eval also
performs O(n) arithmetic operations on Fractions, plus O(log k) of them for
each power with exponent k.
"""

from fractions import Fraction
from typing import Dict, List, Optional, Tuple, Union

Number = Union[int, Fraction]
BINARY = ("+", "-", "*", "^")


class Expr:
    """One node: op is 'const', 'sym' or one of + - * ^."""

    __slots__ = ("op", "val", "kids")

    def __init__(self, op: str, val: object = None, kids: Tuple["Expr", ...] = ()) -> None:
        self.op = op
        self.val = val
        self.kids = kids

    def __repr__(self) -> str:
        return to_string(self)

    # One method per operation of the data structure; each delegates to the
    # module-level function of the same name.
    def eval(self, env: Dict[str, Number]) -> Fraction:
        return eval_expr(self, env)

    def subs(self, x: str, r: "Expr") -> "Expr":
        return subs(self, x, r)

    def diff(self, x: str) -> "Expr":
        return diff(self, x)

    def size(self) -> int:
        return size(self)

    def height(self) -> int:
        return height(self)

    def equal(self, other: "Expr") -> bool:
        return equal(self, other)

    def to_string(self) -> str:
        return to_string(self)

    def check_invariant(self) -> None:
        check_invariant(self)


def const(c: Number) -> Expr:
    return Expr("const", Fraction(c))


def sym(name: str) -> Expr:
    return Expr("sym", name)


def add(a: Expr, b: Expr) -> Expr:
    return Expr("+", None, (a, b))


def sub(a: Expr, b: Expr) -> Expr:
    return Expr("-", None, (a, b))


def mul(a: Expr, b: Expr) -> Expr:
    return Expr("*", None, (a, b))


def power(a: Expr, k: int) -> Expr:
    if k < 0:
        raise ValueError("exponent must be a nonnegative integer")
    return Expr("^", None, (a, const(k)))


def _apply(op: str, a: Fraction, b: Fraction) -> Fraction:
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    return a ** int(b)


def eval_expr(e: Expr, env: Dict[str, Number]) -> Fraction:
    """Value of e when each symbol s takes the value env[s].

    Precondition: every symbol of e is a key of env. Cost: O(n) node visits.
    """
    stack: List[Tuple[Expr, bool]] = [(e, False)]  # @line L1
    vals: List[Fraction] = []
    while stack:  # @line L2
        u, done = stack.pop()  # @line L3
        if u.op == "const":  # @line L4
            vals.append(u.val)  # type: ignore[arg-type]
        elif u.op == "sym":  # @line L5
            vals.append(Fraction(env[u.val]))  # type: ignore[index]
        elif not done:  # @line L6
            stack.append((u, True))
            for k in reversed(u.kids):
                stack.append((k, False))
        else:  # @line L7
            b = vals.pop()
            a = vals.pop()
            vals.append(_apply(u.op, a, b))
    return vals[0]  # @line L8


def _postorder(e: Expr) -> List[Expr]:
    """Nodes of e in postorder (children before parents), iteratively."""
    out: List[Expr] = []
    stack: List[Tuple[Expr, bool]] = [(e, False)]
    while stack:
        u, done = stack.pop()
        if done or not u.kids:
            out.append(u)
        else:
            stack.append((u, True))
            for k in reversed(u.kids):
                stack.append((k, False))
    return out


def subs(e: Expr, x: str, r: Expr) -> Expr:
    """e with every occurrence of the symbol x replaced by r. Cost O(n)."""
    res: Dict[int, Expr] = {}
    for u in _postorder(e):
        if u.op == "sym" and u.val == x:
            res[id(u)] = r
        elif not u.kids:
            res[id(u)] = u
        else:
            res[id(u)] = Expr(u.op, None, tuple(res[id(k)] for k in u.kids))
    return res[id(e)]


def _is_const(u: Expr, c: Optional[int] = None) -> bool:
    return u.op == "const" and (c is None or u.val == c)


def s_add(a: Expr, b: Expr) -> Expr:
    """Smart constructor: folds constants and drops a zero summand."""
    if _is_const(a) and _is_const(b):
        return const(a.val + b.val)  # type: ignore[operator]
    if _is_const(a, 0):
        return b
    if _is_const(b, 0):
        return a
    return add(a, b)


def s_sub(a: Expr, b: Expr) -> Expr:
    if _is_const(a) and _is_const(b):
        return const(a.val - b.val)  # type: ignore[operator]
    if _is_const(b, 0):
        return a
    return sub(a, b)


def s_mul(a: Expr, b: Expr) -> Expr:
    """Smart constructor: folds constants, 0 * u = 0 and 1 * u = u."""
    if _is_const(a) and _is_const(b):
        return const(a.val * b.val)  # type: ignore[operator]
    if _is_const(a, 0) or _is_const(b, 0):
        return const(0)
    if _is_const(a, 1):
        return b
    if _is_const(b, 1):
        return a
    return mul(a, b)


def diff(e: Expr, x: str) -> Expr:
    """Derivative of e with respect to x, by the sum, product and power rules.

    The result shares subtrees of e. Cost: O(n) node visits and O(n) new nodes.
    """
    d: Dict[int, Expr] = {}
    for u in _postorder(e):
        if u.op == "const":
            d[id(u)] = const(0)
        elif u.op == "sym":
            d[id(u)] = const(1 if u.val == x else 0)
        else:
            a, b = u.kids
            da, db = d[id(a)], d[id(b)]
            if u.op == "+":
                d[id(u)] = s_add(da, db)
            elif u.op == "-":
                d[id(u)] = s_sub(da, db)
            elif u.op == "*":
                d[id(u)] = s_add(s_mul(da, b), s_mul(a, db))
            else:
                k = int(b.val)  # type: ignore[arg-type]
                if k == 0:
                    d[id(u)] = const(0)
                else:
                    pk = const(1) if k == 1 else (a if k == 2 else power(a, k - 1))
                    d[id(u)] = s_mul(s_mul(const(k), pk), da)
    return d[id(e)]


def size(e: Expr) -> int:
    """Number of nodes, counting a shared subtree once per occurrence."""
    return len(_postorder(e))


def height(e: Expr) -> int:
    """Number of edges on a longest root-to-leaf path."""
    h: Dict[int, int] = {}
    for u in _postorder(e):
        h[id(u)] = 1 + max(h[id(k)] for k in u.kids) if u.kids else 0
    return h[id(e)]


def equal(a: Expr, b: Expr) -> bool:
    """Syntactic identity: same operators, constants and symbols in the same shape."""
    stack: List[Tuple[Expr, Expr]] = [(a, b)]
    while stack:
        u, v = stack.pop()
        if u is v:
            continue
        if u.op != v.op or u.val != v.val or len(u.kids) != len(v.kids):
            return False
        stack.extend(zip(u.kids, v.kids))
    return True


def to_string(e: Expr) -> str:
    """Fully parenthesized infix form; ^ is written **, so Python can parse it."""
    s: Dict[int, str] = {}
    for u in _postorder(e):
        if u.op == "const":
            c = u.val
            s[id(u)] = "Fraction(%d, %d)" % (c.numerator, c.denominator) if c.denominator != 1 else "(%d)" % c.numerator  # type: ignore[union-attr]
        elif u.op == "sym":
            s[id(u)] = str(u.val)
        else:
            a, b = u.kids
            o = "**" if u.op == "^" else u.op
            s[id(u)] = "(" + s[id(a)] + " " + o + " " + s[id(b)] + ")"
    return s[id(e)]


def check_invariant(e: Expr) -> None:
    """Every node has a valid operator and arity, and the structure is acyclic."""
    on_path: set = set()
    stack: List[Tuple[Expr, bool]] = [(e, False)]
    while stack:
        u, done = stack.pop()
        if done:
            on_path.discard(id(u))
            continue
        assert id(u) not in on_path, "cycle"
        if u.op == "const":
            assert isinstance(u.val, Fraction) and u.kids == ()
        elif u.op == "sym":
            assert isinstance(u.val, str) and u.kids == ()
        else:
            assert u.op in BINARY and len(u.kids) == 2
            if u.op == "^":
                k = u.kids[1]
                assert k.op == "const" and k.val.denominator == 1 and k.val >= 0  # type: ignore[union-attr]
            on_path.add(id(u))
            stack.append((u, True))
            for k in u.kids:
                stack.append((k, False))
