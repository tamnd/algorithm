# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/load-linked-store-conditional/. The authors are listed in prov/5J33C1.jsonl.
"""LL/SC built from CAS with an unbounded tag, and its sequential specification.

The shared word X holds a pair (value, tag). LL reads the pair and keeps it
as the link. SC(v) is CAS(X, link, (v, tag + 1)). Each successful SC raises
the tag, and a tag never comes back, so X equals the link exactly when no SC
has succeeded since the LL. This is the simple form of the idea. The tag
here is a Python integer with no bound; the constructions of Moir (1997)
and of Jayanti and Petrovic (2003) work with words of fixed size.

The variant value_only() keeps only the value in X, with no tag. It is
plain CAS, and it shows the ABA problem.
"""


class LLSC:
    """Sequential specification. State: (value, frozenset of linked pids)."""

    def __init__(self, init):
        self.init = (init, frozenset())

    def apply(self, s, name, arg, pid):
        val, links = s
        if name == "ll":
            return (val, links | {pid}), val
        if name == "sc":
            if pid in links:
                return (arg, frozenset()), True
            return s, False
        if name == "vl":
            return s, pid in links
        raise ValueError(name)


def ll(tagged):
    yield ("inv", "ll", None)
    w = yield ("read", "X")                   # the linearization point
    yield ("res", w[0] if tagged else w)
    return w


def sc(link, v, tagged):
    yield ("inv", "sc", v)
    if link is None:                          # no LL before: fail with no step
        yield ("res", False)
        return False
    new = (v, link[1] + 1) if tagged else v
    ok = yield ("cas", "X", link, new)        # the linearization point
    yield ("res", ok)
    return ok


def vl(link):
    yield ("inv", "vl", None)
    w = yield ("read", "X")
    ok = link is not None and w == link
    yield ("res", ok)
    return ok


def program(ops, tagged=True):
    """Run ("ll",), ("sc", v) and ("vl",) in order. The link is a local."""
    link = None
    for op in ops:
        if op[0] == "ll":
            link = yield from ll(tagged)
        elif op[0] == "sc":
            yield from sc(link, op[1], tagged)
        else:
            yield from vl(link)


def setup_for(programs, init="A", tagged=True):
    def setup():
        x = (init, 0) if tagged else init
        return {"X": x}, [program(ops, tagged) for ops in programs]

    return setup
