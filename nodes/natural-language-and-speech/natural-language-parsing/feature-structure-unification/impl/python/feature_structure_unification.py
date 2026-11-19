# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/feature-structure-unification/. The authors are listed in prov/W1EW4J.jsonl.

"""Destructive unification of feature structures with union-find.

A feature structure is a rooted directed graph. Each node is either an atom
(a string such as "sg"), or a complex node with a table of features, or an
empty node with no atom and no feature (the variable []). Two paths that lead
to the same node are reentrant. Cycles are allowed: unify does no occurs
check, so it unifies rational (cyclic) structures as Huet's algorithm does for
terms.

unify(a, b) merges the two graphs in place and returns the root of the result,
or None if the structures clash. On a clash the input graphs are left in a
partly merged state; use unify_copy to keep the inputs.

build(spec) makes a structure from nested Python values: a dict is a complex
node, a str is an atom, None is the empty node. A reentrant node is written
("#1", spec) at its first use and "#1" at every other use.
"""


class Node:
    __slots__ = ("parent", "rank", "atom", "arcs")

    def __init__(self, atom=None, arcs=None):
        self.parent = self
        self.rank = 0
        self.atom = atom
        self.arcs = {} if arcs is None else arcs


def find(x):
    """Return the root of the class of x, with path compression."""
    root = x
    while root.parent is not root:
        root = root.parent
    while x.parent is not root:
        x.parent, x = root, x.parent
    return root


def _clash(x, y):
    if x.atom is not None and y.atom is not None:
        return x.atom != y.atom
    if x.atom is not None and y.arcs:
        return True
    if y.atom is not None and x.arcs:
        return True
    return False


def unify(a, b):
    """Unify the structures rooted at a and b in place.

    Return the root of the unified structure, or None on a clash.
    """
    stack = [(a, b)]  # @line L1
    while stack:  # @line L2
        x, y = stack.pop()  # @line L3
        x, y = find(x), find(y)
        if x is y:  # @line L4
            continue
        if _clash(x, y):  # @line L5
            return None
        if x.rank < y.rank:  # @line L6
            x, y = y, x
        y.parent = x
        if x.rank == y.rank:
            x.rank += 1
        if x.atom is None:  # @line L7
            x.atom = y.atom
        big, small = x.arcs, y.arcs  # @line L8
        if len(big) < len(small):
            big, small = small, big
        for f, v in small.items():  # @line L9
            if f in big:  # @line L10
                stack.append((big[f], v))
            else:  # @line L11
                big[f] = v
        x.arcs = big  # @line L12
        y.arcs = {}
        y.atom = None
    return find(a)  # @line L13


def build(spec, tags=None):
    """Build a structure from nested dicts, strings, None and reentrancy tags."""
    if tags is None:
        tags = {}
    if isinstance(spec, tuple):
        tag, inner = spec
        if tag not in tags:
            tags[tag] = Node()
        node = unify(tags[tag], build(inner, tags))
        if node is None:
            raise ValueError("tag " + tag + " has clashing values")
        return node
    if isinstance(spec, str) and spec.startswith("#"):
        if spec not in tags:
            tags[spec] = Node()
        return tags[spec]
    if spec is None:
        return Node()
    if isinstance(spec, str):
        return Node(atom=spec)
    node = Node()
    for f in sorted(spec):
        node.arcs[f] = build(spec[f], tags)
    return node


def nodes_of(root):
    """List the class roots reachable from root, in a fixed order."""
    root = find(root)
    seen = {id(root): root}
    order = [root]
    i = 0
    while i < len(order):
        x = order[i]
        i += 1
        for f in sorted(x.arcs):
            y = find(x.arcs[f])
            if id(y) not in seen:
                seen[id(y)] = y
                order.append(y)
    return order


def copy(root):
    """Return a fresh copy of the structure rooted at root."""
    order = nodes_of(root)
    new = {id(x): Node(atom=x.atom) for x in order}
    for x in order:
        new[id(x)].arcs = {f: new[id(find(v))] for f, v in x.arcs.items()}
    return new[id(order[0])]


def unify_copy(a, b):
    """Unify copies of a and b; the inputs are not changed."""
    return unify(copy(a), copy(b))


def canonical(root):
    """A canonical form: two structures are equal as graphs iff the forms are equal.

    Nodes are numbered in breadth-first order with features in sorted order.
    Because each node has at most one arc per feature, this numbering is the
    same for isomorphic rooted graphs.
    """
    order = nodes_of(root)
    num = {id(x): i for i, x in enumerate(order)}
    return tuple(
        (x.atom, tuple((f, num[id(find(x.arcs[f]))]) for f in sorted(x.arcs)))
        for x in order
    )


def subsumes(general, specific):
    """Return True if general subsumes specific (general is at most as informative).

    Look for a map h from the nodes of general to the nodes of specific with
    h(root) = root, h(x.f) = h(x).f for every arc, and every atom kept. The map
    is forced by the paths, so a breadth-first walk decides it.
    """
    g0, s0 = find(general), find(specific)
    h = {id(g0): s0}
    queue = [g0]
    while queue:
        x = queue.pop()
        y = h[id(x)]
        if x.atom is not None and x.atom != y.atom:
            return False
        for f, v in x.arcs.items():
            if f not in y.arcs:
                return False
            v, w = find(v), find(y.arcs[f])
            if id(v) in h:
                if h[id(v)] is not w:
                    return False
            else:
                h[id(v)] = w
                queue.append(v)
    return True


def get_path(root, path):
    """Follow a path of features from root; return the node or None."""
    x = find(root)
    for f in path:
        if f not in x.arcs:
            return None
        x = find(x.arcs[f])
    return x


def to_spec(root):
    """Inverse of build, with tags "#1", "#2", ... on nodes reached twice."""
    order = nodes_of(root)
    indeg = {id(x): 0 for x in order}
    for x in order:
        for v in x.arcs.values():
            indeg[id(find(v))] += 1
    indeg[id(order[0])] += 1
    tag_of = {}
    for x in order:
        if indeg[id(x)] > 1:
            tag_of[id(x)] = "#" + str(len(tag_of) + 1)
    done = set()

    def walk(x):
        x = find(x)
        if id(x) in tag_of and id(x) in done:
            return tag_of[id(x)]
        done.add(id(x))
        if x.atom is not None:
            body = x.atom
        elif x.arcs:
            body = {f: walk(x.arcs[f]) for f in sorted(x.arcs)}
        else:
            body = None
        if id(x) in tag_of:
            return (tag_of[id(x)], body)
        return body

    return walk(order[0])
