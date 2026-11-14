# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dominance-frontier-computation/. The authors are listed in prov/VKF111.jsonl.
"""Dominance frontiers of a flow graph.

dominance_frontiers is the bottom-up pass of Cytron, Ferrante, Rosen, Wegman
and Zadeck over the dominator tree (lines L1 to L8 of the page).
dominance_frontiers_walk is the walk of Cooper, Harvey and Kennedy from each
predecessor of a node up to its immediate dominator (lines L9 to L14).

A graph is a dict from node to its list of successors, and a root. Only the
nodes that the root reaches take part. The immediate dominators come from the
iterative algorithm of Cooper, Harvey and Kennedy; idom[root] is None.
"""

import toyir


def program_graph(prog):
    """The successor lists and the entry of a toy IR program."""
    return {label: toyir.succs(prog, label) for label in prog.blocks}, prog.entry


def postorder(succ, root):
    """The nodes that root reaches, in postorder of an iterative DFS."""
    seen = {root}
    out = []
    stack = [(root, iter(succ[root]))]
    while stack:
        v, it = stack[-1]
        w = next(it, None)
        if w is None:
            stack.pop()
            out.append(v)
        elif w not in seen:
            seen.add(w)
            stack.append((w, iter(succ[w])))
    return out


def immediate_dominators(succ, root):
    """Dict from each node that root reaches to its immediate dominator."""
    order = postorder(succ, root)
    po = {v: i for i, v in enumerate(order)}
    pred = {v: [] for v in order}
    for v in order:
        for w in succ[v]:
            pred[w].append(v)
    doms = {root: root}

    def intersect(a, b):
        while a != b:
            while po[a] < po[b]:
                a = doms[a]
            while po[b] < po[a]:
                b = doms[b]
        return a

    changed = True
    while changed:
        changed = False
        for b in reversed(order):
            if b == root:
                continue
            new = None
            for p in pred[b]:
                if p in doms:
                    new = p if new is None else intersect(p, new)
            if doms.get(b) != new:
                doms[b] = new
                changed = True
    idom = dict(doms)
    idom[root] = None
    return idom


def tree_children(idom):
    children = {v: [] for v in idom}
    for v, d in idom.items():
        if d is not None:
            children[d].append(v)
    return children


def _tree_postorder(children, root):
    out = []
    stack = [(root, False)]
    while stack:
        v, done = stack.pop()
        if done:
            out.append(v)
        else:
            stack.append((v, True))
            for c in children[v]:
                stack.append((c, False))
    return out


def dominance_frontiers(succ, root, idom=None):
    """Cytron's bottom-up pass. Returns a dict from node to its frontier."""
    if idom is None:
        idom = immediate_dominators(succ, root)
    children = tree_children(idom)
    df = {}
    for x in _tree_postorder(children, root):  # @line L1
        s = set()  # @line L2
        for y in succ[x]:  # @line L3
            if idom[y] != x:  # @line L4
                s.add(y)
        for z in children[x]:  # @line L5
            for y in df[z]:  # @line L6
                if idom[y] != x:  # @line L7
                    s.add(y)
        df[x] = s
    return df  # @line L8


def dominance_frontiers_walk(succ, root, idom=None):
    """The walk of Cooper, Harvey and Kennedy, with the early stop."""
    if idom is None:
        idom = immediate_dominators(succ, root)
    pred = {v: [] for v in idom}
    for v in idom:
        for w in succ[v]:
            pred[w].append(v)
    df = {v: set() for v in idom}
    for y in idom:  # @line L9
        if len(pred[y]) < 2 and y != root:
            continue
        for p in pred[y]:  # @line L10
            runner = p  # @line L11
            while runner != idom[y] and y not in df[runner]:  # @line L12
                df[runner].add(y)  # @line L13
                runner = idom[runner]  # @line L14
    return df


def iterated_dominance_frontier(df, nodes):
    """DF+ of a set of nodes, by a worklist over the frontiers."""
    result = set()
    seen = set(nodes)
    work = list(nodes)
    while work:
        x = work.pop()
        for y in df[x]:
            if y not in result:
                result.add(y)
                if y not in seen:
                    seen.add(y)
                    work.append(y)
    return result


def program_frontiers(prog):
    """The dominance frontiers of the blocks of a toy IR program."""
    succ, root = program_graph(prog)
    return dominance_frontiers(succ, root)
