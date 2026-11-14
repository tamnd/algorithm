# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/motion-space-assembly-planning/. The authors are listed in prov/TCQ1T4.jsonl.
"""One core step of the motion space approach, for one family of motions.

The framework of Halperin, Latombe and Wilson cuts a space of motions into
cells on which the blocking graph does not change, and reads the removable
subassemblies of each cell from the strongly connected components of its
graph. This module does that step for the motion space of the six axis
translations to infinity, where each of the six directions is its own cell:

    for each direction d, list every nonempty proper subset S of a
    subassembly A that can leave A \\ S by one translation along d.

Motion model: one translation to infinity along +x, -x, +y, -y, +z or -z.
Hand model: two-handed; S moves as one rigid body and A \\ S stays.
"""

from assembly_boxes import AXES6, blocks, members


def blocking_graph(boxes, d, within):
    """Bit j of out[i] is set when part j blocks part i along d, inside within."""
    out = [0] * len(boxes)
    for i in members(within):  # @line L2
        for j in members(within):
            if i != j and blocks(boxes[i], boxes[j], d):
                out[i] |= 1 << j  # @line L3
    return out


def tarjan_sccs(out, within):
    """Strongly connected components of the graph induced on within, as bit
    masks, in completion order: each one after every component it reaches."""
    index, low, on_stack = {}, {}, set()
    stack, comps = [], []
    counter = 0
    for root in members(within):
        if root in index:
            continue
        index[root] = low[root] = counter
        counter += 1
        stack.append(root)
        on_stack.add(root)
        work = [(root, iter(members(out[root] & within)))]
        while work:
            v, it = work[-1]
            pushed = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on_stack.add(w)
                    work.append((w, iter(members(out[w] & within))))
                    pushed = True
                    break
                if w in on_stack:
                    low[v] = min(low[v], index[w])
            if pushed:
                continue
            work.pop()
            if work:
                u = work[-1][0]
                low[u] = min(low[u], low[v])
            if low[v] == index[v]:
                comp = 0
                while True:
                    w = stack.pop()
                    on_stack.discard(w)
                    comp |= 1 << w
                    if w == v:
                        break
                comps.append(comp)
    return comps


def closed_sets(out, within):
    """Every nonempty proper subset of within with no arc to the rest of within."""
    comps = tarjan_sccs(out, within)  # @line L4
    k = len(comps)
    succ = []
    for c in comps:  # @line L5
        m = 0
        for i in members(c):
            m |= out[i]
        succ.append(m & within & ~c)
    result = []

    def extend(t, chosen):  # @line L6
        if t == k:  # @line L7
            if chosen and chosen != within:
                result.append(chosen)
            return
        extend(t + 1, chosen)  # @line L8
        if succ[t] & ~chosen == 0:  # @line L9
            extend(t + 1, chosen | comps[t])

    extend(0, 0)
    return result


def removable_sets(boxes, within, motions=AXES6):
    """A dict from each direction d to the sorted list of the subsets of
    within that can leave the rest of within along d."""
    found = {}
    for d in motions:  # @line L1
        out = blocking_graph(boxes, d, within)
        found[d] = sorted(closed_sets(out, within))
    return found


def separations(boxes, within, motions=AXES6):
    """The splits {S, within \\ S} of within for which one side can leave the
    other along some direction, each as (S1, S2) with S1 holding the lowest
    part of within."""
    low = within & -within
    splits = set()
    for sets in removable_sets(boxes, within, motions).values():
        for s in sets:
            other = within & ~s
            splits.add((s, other) if s & low else (other, s))
    return sorted(splits)
