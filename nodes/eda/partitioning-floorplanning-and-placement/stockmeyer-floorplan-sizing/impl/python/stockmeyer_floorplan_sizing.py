# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stockmeyer-floorplan-sizing/. The authors are listed in prov/RH6JHQ.jsonl.

"""Stockmeyer's sizing of a slicing floorplan (1983).

The floorplan is a Polish expression: blocks are ints, "V" puts the first part
to the left of the second (widths add), "H" puts the first part below the
second (heights add). Each block has a list of allowed shapes (w, h), for
example a rectangle and its rotation. The algorithm computes, bottom up, the
list of non-dominated (width, height) pairs of each subtree, and returns a
choice of shapes with the least area of the whole floorplan.
"""

Shape = tuple[int, int]
# An entry of a shape list: (width, height, back pointer). For a leaf the back
# pointer is the index of the shape in the input list; for a node it is the
# pair of indices into the lists of the two children.
Entry = tuple[int, int, object]


def pareto(shapes: list[Shape]) -> list[Entry]:
    """Return the non-dominated shapes, by increasing width and decreasing height."""
    order = sorted(range(len(shapes)), key=lambda k: (shapes[k][0], shapes[k][1]))
    out: list[Entry] = []
    for k in order:
        w, h = shapes[k]
        if out and h >= out[-1][1]:
            continue  # not lower than a narrower (or equal) shape
        if out and w == out[-1][0]:
            out.pop()
        out.append((w, h, k))
    return out


def merge_v(a: list[Entry], b: list[Entry]) -> list[Entry]:
    """Non-dominated shapes of a beside b: widths add, the height is the larger one."""
    i = j = 0  # @line L8
    out: list[Entry] = []
    while True:  # @line L9
        out.append((a[i][0] + b[j][0], max(a[i][1], b[j][1]), (i, j)))  # @line L10
        if a[i][1] > b[j][1]:  # @line L11
            if i == len(a) - 1:
                return out
            i += 1
        elif b[j][1] > a[i][1]:  # @line L12
            if j == len(b) - 1:
                return out
            j += 1
        else:  # @line L13
            if i == len(a) - 1 or j == len(b) - 1:
                return out
            i += 1
            j += 1


def merge_h(a: list[Entry], b: list[Entry]) -> list[Entry]:
    """Non-dominated shapes of a below b: heights add, the width is the larger one.

    This is merge_v with widths and heights exchanged. In exchanged
    coordinates the lists run in the opposite order, so they are reversed.
    """
    ta = [(h, w, k) for (w, h, k) in reversed(a)]
    tb = [(h, w, k) for (w, h, k) in reversed(b)]
    na, nb = len(a), len(b)
    res = merge_v(ta, tb)
    return [(w, h, (na - 1 - i, nb - 1 - j)) for (h, w, (i, j)) in reversed(res)]


def shape_lists(tokens: list, shapes: dict[int, list[Shape]]) -> list:
    """Build the tree of the Polish expression with the shape list of each node.

    A leaf is [block, list]; a node is [op, list, left, right].
    """
    stack: list = []
    for t in tokens:  # @line L1
        if t != "H" and t != "V":  # @line L2
            stack.append([t, pareto(shapes[t])])
        else:  # @line L3
            if len(stack) < 2:
                raise ValueError("not a Polish expression")
            b = stack.pop()
            a = stack.pop()
            merged = merge_v(a[1], b[1]) if t == "V" else merge_h(a[1], b[1])
            stack.append([t, merged, a, b])
    if len(stack) != 1:
        raise ValueError("not a Polish expression")
    return stack[0]


def stockmeyer_sizing(
    tokens: list, shapes: dict[int, list[Shape]]
) -> tuple[int, int, int, dict[int, int], list[Shape]]:
    """Return (area, W, H, choice, front) for a slicing floorplan.

    choice[b] is the index in shapes[b] of the shape given to block b, front is
    the list of non-dominated (W, H) pairs of the whole floorplan, by
    increasing width. Among the shapes of least area, the narrowest is chosen.
    """
    root = shape_lists(tokens, shapes)
    front = root[1]  # @line L4
    best = min(range(len(front)), key=lambda k: (front[k][0] * front[k][1], front[k][0]))  # @line L5
    choice: dict[int, int] = {}
    todo = [(root, best)]  # @line L6
    while todo:
        node, k = todo.pop()
        entry = node[1][k]
        if len(node) == 2:
            choice[node[0]] = entry[2]
        else:
            i, j = entry[2]
            todo.append((node[2], i))
            todo.append((node[3], j))
    w, h = front[best][0], front[best][1]
    return w * h, w, h, choice, [(e[0], e[1]) for e in front]  # @line L7
