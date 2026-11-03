# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sorting-problem/. The brute force oracle (spec 09.5). Rule S07 checks that it agrees with reference.py.


def sort(xs):
    """Sort xs in place. It moves the smallest item that is left to the output until no item is left, so it does not share code with the built-in sort."""
    out = []
    while xs:
        m = 0
        for i in range(1, len(xs)):
            if xs[i] < xs[m]:
                m = i
        out.append(xs.pop(m))
    xs.extend(out)
