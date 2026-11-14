# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cooper-harvey-kennedy-dominance/. The authors are listed in prov/0T0R8F.jsonl.
"""The iterative dominator algorithm of Cooper, Harvey and Kennedy.

chk(n, edges, root) returns (idom, passes): idom[v] is the immediate
dominator of v, or -1 for the root and for the vertices that the root does
not reach; passes is the number of passes of the main loop, the last of
which changes nothing. cfg_idom(prog) applies it to a toy IR program.
"""

import toyir

UNDEFINED = -1


def _postorder(n, succ, root):
    """Iterative DFS from root; returns the vertices in postorder."""
    seen = [False] * n
    seen[root] = True
    post = []
    stack = [(root, 0)]
    while stack:
        v, i = stack[-1]
        if i < len(succ[v]):
            stack[-1] = (v, i + 1)
            w = succ[v][i]
            if not seen[w]:
                seen[w] = True
                stack.append((w, 0))
        else:
            stack.pop()
            post.append(v)
    return post


def chk(n, edges, root):
    if n < 1 or not 0 <= root < n:
        raise ValueError("a flow graph needs n >= 1 vertices and a root in range")
    succ = [[] for _ in range(n)]
    pred = [[] for _ in range(n)]
    for a, b in edges:
        if not (0 <= a < n and 0 <= b < n):
            raise ValueError("edge endpoint out of range")
        succ[a].append(b)
        pred[b].append(a)

    post = _postorder(n, succ, root)  # @line L1
    po = [-1] * n
    for i, v in enumerate(post):
        po[v] = i
    rpo = post[::-1]

    doms = [UNDEFINED] * n  # @line L2
    doms[root] = root  # @line L3

    def intersect(b1, b2):
        finger1, finger2 = b1, b2  # @line L14
        while finger1 != finger2:  # @line L15
            while po[finger1] < po[finger2]:  # @line L16
                finger1 = doms[finger1]
            while po[finger2] < po[finger1]:  # @line L17
                finger2 = doms[finger2]
        return finger1  # @line L18

    changed = True  # @line L4
    passes = 0
    while changed:  # @line L5
        passes += 1
        changed = False  # @line L6
        for b in rpo[1:]:  # @line L7
            ps = [p for p in pred[b] if doms[p] != UNDEFINED]
            new_idom = ps[0]  # @line L8
            for p in ps[1:]:  # @line L9
                new_idom = intersect(p, new_idom)  # @line L10
            if doms[b] != new_idom:  # @line L11
                doms[b] = new_idom  # @line L12
                changed = True
    idom = [UNDEFINED] * n  # @line L13
    for v in range(n):
        if v != root and doms[v] != UNDEFINED:
            idom[v] = doms[v]
    return idom, passes


def chk_idom(n, edges, root):
    """Immediate dominators only; -1 for the root and unreachable vertices."""
    return chk(n, edges, root)[0]


def cfg_idom(prog):
    """Immediate dominators of the blocks of a toy IR program, as a dict from
    label to label. The entry and the unreachable blocks map to None."""
    labels = list(prog.blocks)
    index = {lab: i for i, lab in enumerate(labels)}
    edges = [(index[a], index[b]) for a, b in toyir.edges(prog)]
    idom = chk_idom(len(labels), edges, 0)
    return {lab: (labels[idom[i]] if idom[i] != UNDEFINED else None) for i, lab in enumerate(labels)}
