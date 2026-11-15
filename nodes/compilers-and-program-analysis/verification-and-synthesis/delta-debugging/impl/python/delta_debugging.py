# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delta-debugging/. The authors are listed in prov/25NQX4.jsonl.
"""The minimizing delta debugging algorithm ddmin of Zeller and Hildebrandt.

test(c) gets a list, a sub-list of the input in the original order, and
returns FAIL, PASS or UNRESOLVED. ddmin(items, test) assumes that
test(items) is FAIL and that the test of the empty list is PASS. It returns
a failing sub-list that is 1-minimal: removing any one element of it does
not give FAIL. It is not always a failing sub-list of the smallest size.

When the granularity is 2, the two complements are the two subsets, so they
are not tested again. Apart from that, the order of the tests is the one of
the paper: all subsets, then all complements.
"""

FAIL = "FAIL"
PASS = "PASS"
UNRESOLVED = "UNRESOLVED"


def split(c, n):
    """Split the list c into n contiguous parts whose sizes differ by at most 1."""
    parts = []
    start = 0
    for i in range(n):
        end = start + (len(c) - start) // (n - i)
        parts.append(c[start:end])
        start = end
    return parts


def ddmin(items, test):
    """Return (result, number of calls of test)."""
    calls = 0

    def run(c):
        nonlocal calls
        calls += 1
        out = test(c)
        if out not in (FAIL, PASS, UNRESOLVED):
            raise ValueError("test must return FAIL, PASS or UNRESOLVED")
        return out

    c = list(items)
    n = 2  # @line L1
    while len(c) >= 2:  # @line L2
        parts = split(c, n)  # @line L3
        reduced = False
        for d in parts:  # @line L4
            if run(d) == FAIL:
                c, n = d, 2  # @line L5
                reduced = True
                break
        if not reduced and n > 2:  # @line L6
            for i in range(n):
                comp = [x for j, p in enumerate(parts) if j != i for x in p]
                if run(comp) == FAIL:
                    c, n = comp, max(n - 1, 2)  # @line L7
                    reduced = True
                    break
        if reduced:
            continue
        if n < len(c):  # @line L8
            n = min(2 * n, len(c))  # @line L9
        else:  # @line L10
            break  # @line L11
    return c, calls  # @line L12


def is_one_minimal(c, test):
    """True when no sub-list of c with one element removed fails."""
    return all(test(c[:i] + c[i + 1:]) != FAIL for i in range(len(c)))


# ------------------------------------------------- a use on toy IR programs


def program_test(instrs, ret, oracle):
    """A test on lists of toy IR instructions of one block that ends with
    "ret ret". A list that reads a name before it is defined is UNRESOLVED,
    as an invalid program is in a real reducer. oracle(outcome) says whether
    the outcome of toyir.run shows the failure."""
    import toyir

    def test(sub):
        defined = set()
        for ins in sub:
            if any(a not in defined for a in toyir.uses(ins)):
                return UNRESOLVED
            defined.add(toyir.defs(ins))
        if isinstance(ret, str) and ret not in defined:
            return UNRESOLVED
        prog = toyir.Program([], {"entry": toyir.Block(list(sub), ("ret", ret))})
        return FAIL if oracle(toyir.run(prog, [])) else PASS

    return test
