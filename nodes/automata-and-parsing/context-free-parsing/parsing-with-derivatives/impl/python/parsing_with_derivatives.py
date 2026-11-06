# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parsing-with-derivatives/. The authors are listed in prov/FA07T5.jsonl.
"""Recognition of context-free languages by Brzozowski derivatives (Might, Darais
and Spiewak 2011), with memoized, lazily tied derivatives and a linear-time
nullability fixed point, as analyzed by Adams, Hollenbeck and Might (2016).

A language is a node of a possibly cyclic graph: EMPTY (no strings), EPS (only
the empty string), a token, a union a | b, or a concatenation a . b. A grammar
is a list of productions (A, rhs); the nonterminals are the left sides, and
every other symbol in a right side is a token.
"""


class Node:
    __slots__ = ("kind", "a", "b", "tok", "nullable")

    def __init__(self, kind, a=None, b=None, tok=None):
        self.kind = kind  # "empty", "eps", "tok", "alt" or "cat"
        self.a, self.b, self.tok = a, b, tok
        self.nullable = None  # None until decided

    def __repr__(self):
        return f"<{self.kind}>"


EMPTY = Node("empty")
EMPTY.nullable = False
EPS = Node("eps")
EPS.nullable = True


def from_grammar(prods, start):
    """The language node of start: each nonterminal becomes a union of its
    productions, and each production a right-nested concatenation."""
    nts = {a for a, _ in prods} | {start}
    top = {a: Node("alt") for a in nts}
    toks = {}

    def sym(x):
        if x in nts:
            return top[x]
        if x not in toks:
            toks[x] = Node("tok", tok=x)
        return toks[x]

    for a in nts:
        alts = [rhs for b, rhs in prods if b == a]
        seqs = []
        for rhs in alts:
            node = EPS
            if rhs:
                node = sym(rhs[-1])
                for x in reversed(rhs[:-1]):
                    node = Node("cat", sym(x), node)
            seqs.append(node)
        # top[a] = seq1 | (seq2 | (... | EMPTY))
        rest = EMPTY
        for node in reversed(seqs[1:]):
            rest = Node("alt", node, rest)
        top[a].a = seqs[0] if seqs else EMPTY
        top[a].b = rest
    return top[start]


def nullable(root):
    """Least fixed point of: EPS is nullable, a | b if a or b is, a . b if both are.
    Decides every undecided node reachable from root, in time linear in their number."""
    if root.nullable is not None:
        return root.nullable
    found, todo = [root], [root]  # @line L11
    seen = {id(root)}
    users = {}
    while todo:
        x = todo.pop()
        for y in (x.a, x.b) if x.kind in ("alt", "cat") else ():
            users.setdefault(id(y), []).append(x)
            if y.nullable is None and id(y) not in seen:
                seen.add(id(y))
                found.append(y)
                todo.append(y)
    # need[x] = number of children still to be proven nullable before x is
    need = {}
    for x in found:
        if x.kind == "eps":
            need[id(x)] = 0
        elif x.kind == "alt":
            need[id(x)] = 0 if (x.a.nullable or x.b.nullable) else 1
        elif x.kind == "cat":
            need[id(x)] = (x.a.nullable is not True) + (x.b.nullable is not True)
            if x.a.nullable is False or x.b.nullable is False:
                need[id(x)] = 3  # can never become nullable
        else:
            need[id(x)] = 3
    # decide only after all counts are taken, so that no child is counted twice
    queue = [x for x in found if need[id(x)] == 0]
    for x in queue:
        x.nullable = True  # @line L12
    while queue:
        y = queue.pop()
        for x in users.get(id(y), ()):
            if x.nullable is None and id(x) in need:
                need[id(x)] -= 1
                if need[id(x)] == 0:
                    x.nullable = True
                    queue.append(x)
    for x in found:
        if x.nullable is None:
            x.nullable = False  # @line L13
    return root.nullable


def compact(x):
    """A node with the same language as x, skipping trivial nodes: a union with
    EMPTY on one side, a concatenation with EMPTY on one side (which is EMPTY),
    and a concatenation EPS . y, which is y. A cycle of such skips denotes the
    empty language (it is the least fixed point of x = x)."""
    seen = set()
    while id(x) not in seen:
        seen.add(id(x))
        if x.kind == "alt":
            if x.a is EMPTY:
                x = x.b
            elif x.b is EMPTY:
                x = x.a
            else:
                return x
        elif x.kind == "cat":
            if x.a is EMPTY or x.b is EMPTY:
                return EMPTY
            if x.a is EPS:
                x = x.b
            else:
                return x
        else:
            return x
    return EMPTY


class Deriver:
    """Memoized derivatives. memo[(id(node), token)] is the derivative node; the
    nodes are kept alive in keep so that ids are not reused."""

    def __init__(self):
        self.memo = {}
        self.keep = []
        self.created = 0

    def derive(self, root, c):
        stack = []
        result = self._get(root, c, stack)
        while stack:
            x, u = stack.pop()
            if x.kind == "alt":  # @line L7
                u.a = self._get(x.a, c, stack)
                u.b = self._get(x.b, c, stack)
            elif u.kind == "cat":  # @line L8
                u.a = self._get(x.a, c, stack)
                u.b = x.b
            else:  # @line L9
                u.a.a = self._get(x.a, c, stack)
                u.a.b = x.b
                u.b = self._get(x.b, c, stack)
        return result

    def _get(self, x, c, stack):
        """The node for D_c(x): a constant for a leaf, otherwise a memoized node
        whose children are filled in later from the stack."""
        x = compact(x)  # @line L3
        if x.kind in ("empty", "eps"):  # @line L4
            return EMPTY
        if x.kind == "tok":  # @line L5
            return EPS if x.tok == c else EMPTY
        key = (id(x), c)
        u = self.memo.get(key)  # @line L6
        if u is not None:
            return u
        if x.kind == "alt":
            u = Node("alt")
            self.created += 1
        elif not nullable(x.a):
            u = Node("cat")
            self.created += 1
        else:
            u = Node("alt", Node("cat"))
            self.created += 2
        self.memo[key] = u
        self.keep.append(x)
        stack.append((x, u))
        return u  # @line L10


def recognize(prods, start, tokens, stats=None):
    """True when the token sequence is in L(G). If stats is a dict, the number of
    derivative nodes created is stored under "nodes"."""
    lang = from_grammar(prods, start)
    d = Deriver()
    for c in tokens:  # @line L1
        lang = d.derive(lang, c)
    if stats is not None:
        stats["nodes"] = d.created
    return nullable(lang)  # @line L2


def recognize_naive(lang, tokens, limit=10**6):
    """The derivative without memoization, for acyclic languages only (no recursion);
    counts the nodes built, to show the duplication that memoization removes."""
    built = [0]

    def nul(x):
        if x.kind == "eps":
            return True
        if x.kind == "alt":
            return nul(x.a) or nul(x.b)
        if x.kind == "cat":
            return nul(x.a) and nul(x.b)
        return False

    def der(x, c):
        if built[0] > limit:
            raise OverflowError
        if x.kind in ("empty", "eps"):
            return EMPTY
        if x.kind == "tok":
            return EPS if x.tok == c else EMPTY
        built[0] += 1
        if x.kind == "alt":
            return Node("alt", der(x.a, c), der(x.b, c))
        left = Node("cat", der(x.a, c), x.b)
        if nul(x.a):
            built[0] += 1
            return Node("alt", left, der(x.b, c))
        return left

    for c in tokens:
        lang = der(lang, c)
    return nul(lang), built[0]
