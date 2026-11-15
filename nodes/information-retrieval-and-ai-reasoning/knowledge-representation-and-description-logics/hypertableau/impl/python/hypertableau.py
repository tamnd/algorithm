# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hypertableau/. The authors are listed in prov/974KXE.jsonl.
"""The hypertableau calculus for ALC concept satisfiability with a general TBox.

The TBox and the input concept are first turned into DL-clauses
    U_1 and ... and U_m  ->  V_1 or ... or V_n
over a center variable x and successor variables y_1, ..., y_k. Body atoms are A(x), r(x, y_i)
and A(y_i); head atoms are A(x), A(y_i) and the existential atom (some r.A)(x). An empty head
means a clash. Negative literals go to the body, so labels hold only names and existential atoms.

A clause is a tuple (bx, roles, by, head):
    bx     frozenset of concept names that must hold at x
    roles  tuple of role names; y_i is an r_i-successor of x
    by     tuple of frozensets; by[i] is the set of names that must hold at y_i
    head   tuple of atoms ("x", A), ("y", i, A) or ("some", r, A)
Fresh concept names start with "_Q". The search works on a tree of nodes; node 0 is the root.
Every atom and every edge carries the set of branch points it depends on, so that a clash can
jump back over branch points that did not take part in it (backjumping).
"""

from itertools import product
from typing import Optional, Sequence

from dl import BOTTOM, TOP, GCI, Concept, Interpretation, disj, neg, nnf


class Clausifier:
    """The structural transformation of NNF concepts into DL-clauses."""

    def __init__(self) -> None:
        self.clauses: list[tuple] = []
        self.fresh: dict[Concept, str] = {}

    def name_for(self, c: Concept) -> str:
        """A concept name Q with the clauses of Q subsumed by c. Reused for equal concepts."""
        if c[0] == "atom":
            return c[1]
        if c not in self.fresh:
            q = f"_Q{len(self.fresh) + 1}"
            self.fresh[c] = q
            self.define(q, c)
        return self.fresh[c]

    def define(self, q: str, c: Concept) -> None:
        if c[0] == "and":
            self.define(q, c[1])
            self.define(q, c[2])
        else:
            self.axiom(("or", ("not", ("atom", q)), c))

    def axiom(self, e: Concept) -> None:
        """Add the clauses of top subsumed by e, for e in NNF."""
        if e[0] == "and":
            self.axiom(e[1])
            self.axiom(e[2])
            return
        stack, disjuncts = [e], []
        while stack:
            d = stack.pop()
            if d[0] == "or":
                stack += [d[2], d[1]]
            else:
                disjuncts.append(d)
        bx: set[str] = set()
        roles: list[str] = []
        by: list[frozenset] = []
        head: list[tuple] = []
        for d in disjuncts:
            op = d[0]
            if op == "top" or (op == "all" and d[2] == TOP):
                return  # the clause holds everywhere
            if op == "bottom" or (op == "some" and d[2] == BOTTOM):
                continue
            if op == "atom":
                head.append(("x", d[1]))
            elif op == "not":
                bx.add(d[1][1])
            elif op == "some":
                head.append(("some", d[1], self.name_for(d[2])))
            elif op == "all":
                i = len(roles)
                roles.append(d[1])
                inner = d[2]
                if inner == BOTTOM:
                    by.append(frozenset())
                elif inner[0] == "not":
                    by.append(frozenset({inner[1][1]}))
                else:
                    by.append(frozenset())
                    head.append(("y", i, self.name_for(inner)))
            else:  # a conjunction inside a disjunction gets a fresh name
                head.append(("x", self.name_for(d)))
        self.clauses.append((frozenset(bx), tuple(roles), tuple(by), tuple(dict.fromkeys(head))))


def clausify(c: Concept, tbox: Sequence[GCI] = ()) -> tuple[str, list[tuple]]:
    """The DL-clauses of the TBox and of Q0 subsumed by c, and the name Q0 that the root gets."""
    cl = Clausifier()
    for x, y in tbox:
        cl.axiom(nnf(disj(neg(x), y)))
    root = cl.name_for(nnf(c))
    return root, cl.clauses


class Counter:
    def __init__(self) -> None:
        self.nodes = 0  # nodes made by the existential rule, over all branches
        self.branches = 0  # alternatives tried at nondeterministic Hyp-rule steps
        self.hyp = 0  # Hyp-rule steps


NODEPS: frozenset = frozenset()


class State:
    """One branch: a tree of nodes. labels[x] maps each atom of node x to the branch points it
    depends on; edge[w] is the same for the edge from the parent of w to w. Node ids follow the
    order of creation."""

    def __init__(self, root: str) -> None:
        self.labels: list[dict] = [{root: NODEPS}]
        self.parent: list[Optional[int]] = [None]
        self.role: list[Optional[str]] = [None]
        self.edge: list[frozenset] = [NODEPS]
        self.children: list[list[int]] = [[]]

    def copy(self) -> "State":
        s = State.__new__(State)
        s.labels = [dict(lab) for lab in self.labels]
        s.parent = list(self.parent)
        s.role = list(self.role)
        s.edge = list(self.edge)
        s.children = [list(ch) for ch in self.children]
        return s


def blocking(s: State, mode: str = "equal") -> tuple[list[bool], dict[int, int]]:
    """Which nodes are blocked, and the blocker of each directly blocked node. A node is blocked
    when its parent is blocked, or when an earlier node that is not blocked has the same label
    (mode "equal", anywhere blocking) or a superset of its label (mode "subset", unsound here)."""
    status: list[bool] = []
    blocker: dict[int, int] = {}
    first: dict[frozenset, int] = {}
    open_labels: list[tuple[int, frozenset]] = []
    for w in range(len(s.labels)):
        p = s.parent[w]
        if p is not None and status[p]:
            status.append(True)
            continue
        key = frozenset(s.labels[w])
        if mode == "equal":
            v = first.get(key)
        else:
            v = next((u for u, lab in open_labels if key <= lab), None)
        if v is None:
            first[key] = w
            open_labels.append((w, key))
            status.append(False)
        else:
            blocker[w] = v
            status.append(True)
    return status, blocker


def _holds(s: State, x: int, sigma: tuple, atom: tuple) -> bool:
    if atom[0] == "x":
        return atom[1] in s.labels[x]
    if atom[0] == "y":
        return atom[2] in s.labels[sigma[atom[1]]]
    return atom in s.labels[x]


def _find_hyp(s: State, clauses: Sequence[tuple], deterministic: bool):
    """The first clause instance whose body holds and whose head has no atom that holds, with the
    branch points that its body depends on."""
    for x in range(len(s.labels)):
        lab = s.labels[x]
        for cl in clauses:
            bx, roles, by, head = cl
            if (len(head) <= 1) != deterministic or not bx <= lab.keys():
                continue
            cands = [[w for w in s.children[x] if s.role[w] == r and by[i] <= s.labels[w].keys()] for i, r in enumerate(roles)]
            for sigma in product(*cands):
                if not any(_holds(s, x, sigma, a) for a in head):
                    deps = set().union(*(lab[a] for a in bx))
                    for i, w in enumerate(sigma):
                        deps |= s.edge[w]
                        deps = deps.union(*(s.labels[w][a] for a in by[i]))
                    return x, sigma, head, frozenset(deps)
    return None


def _add(s: State, x: int, sigma: tuple, atom: tuple, deps: frozenset) -> None:
    if atom[0] == "x":
        s.labels[x].setdefault(atom[1], deps)
    elif atom[0] == "y":
        s.labels[sigma[atom[1]]].setdefault(atom[2], deps)
    else:
        s.labels[x].setdefault(atom, deps)


def _exists_rule(s: State, mode: str, cnt: Counter) -> bool:
    """Apply the existential rule once, at the first node that is not blocked and has an
    existential atom without a witness. Return False when there is no such node."""
    status, _ = blocking(s, mode)  # @line L11
    for x in range(len(s.labels)):
        if status[x]:
            continue
        for atom in sorted(a for a in s.labels[x] if isinstance(a, tuple)):
            _, r, a = atom
            if not any(s.role[w] == r and a in s.labels[w] for w in s.children[x]):
                deps = s.labels[x][atom]
                w = len(s.labels)
                s.labels.append({a: deps})
                s.parent.append(x)
                s.role.append(r)
                s.edge.append(deps)
                s.children.append([])
                s.children[x].append(w)
                cnt.nodes += 1
                return True
    return False


def _search(s: State, clauses: Sequence[tuple], mode: str, cnt: Counter, out: list, level: int):
    """Return None when the branch has a clash-free completion (stored in out), and otherwise the
    set of branch points that the clashes depend on."""
    while True:  # @line L2
        app = _find_hyp(s, clauses, True)  # @line L3
        if app is not None:
            cnt.hyp += 1
            x, sigma, head, deps = app
            if not head:  # @line L4
                return deps
            _add(s, x, sigma, head[0], deps)  # @line L5
            continue
        if _exists_rule(s, mode, cnt):  # @line L6
            continue
        app = _find_hyp(s, clauses, False)
        if app is not None:  # @line L7
            cnt.hyp += 1
            x, sigma, head, deps = app
            clash: set = set()
            for atom in head:
                cnt.branches += 1
                s2 = s.copy()
                _add(s2, x, sigma, atom, deps | {level})
                d = _search(s2, clauses, mode, cnt, out, level + 1)  # @line L8
                if d is None:
                    return None
                if level not in d:
                    return d  # backjump: this choice took no part in the clash
                clash |= d - {level}
            return frozenset(clash)  # @line L9
        out.append(s)
        return None  # @line L10


def satisfiable_count(c: Concept, tbox: Sequence[GCI] = (), mode: str = "equal") -> tuple[bool, Counter, Optional[State]]:
    """Decide satisfiability of c with respect to the TBox. Also return the work counter and the
    final state of the open branch, if there is one."""
    root, clauses = clausify(c, tbox)  # @line L1
    cnt = Counter()
    out: list = []
    ok = _search(State(root), clauses, mode, cnt, out, 0) is None
    return ok, cnt, (out[0] if out else None)


def satisfiable(c: Concept, tbox: Sequence[GCI] = ()) -> bool:
    return satisfiable_count(c, tbox)[0]


def subsumes(c: Concept, d: Concept, tbox: Sequence[GCI] = ()) -> bool:
    return not satisfiable(("and", c, neg(d)), tbox)


def model_of(s: State) -> Interpretation:
    """The model of an open branch (equality blocking): the nodes that are not blocked, with each
    edge to a directly blocked node sent to its blocker. The root is element 0."""
    status, blocker = blocking(s, "equal")
    dom = [x for x in range(len(s.labels)) if not status[x]]
    concepts: dict[str, set] = {}
    roles: dict[str, set] = {}
    for x in dom:
        for a in s.labels[x]:
            if isinstance(a, str):
                concepts.setdefault(a, set()).add(x)
        for w in s.children[x]:
            roles.setdefault(s.role[w], set()).add((x, blocker.get(w, w)))
    return Interpretation(dom, concepts, roles)


def model(c: Concept, tbox: Sequence[GCI] = ()) -> Optional[Interpretation]:
    ok, _, s = satisfiable_count(c, tbox)
    return model_of(s) if ok else None
