# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/read-modify-write/. The authors are listed in prov/Q90K2C.jsonl.
"""General read-modify-write, and two-process consensus from any nontrivial one.

RMW(a, f) replaces the word a by f(old) and returns old, in one atomic step.
The explorer in explorer.py has a fixed set of steps, so this module adds
the step ("rmw", a, f) with a subclass of its Memory.
"""

from explorer import Memory


class RMWMemory(Memory):
    def apply(self, pid, op):
        if op[0] == "rmw":
            old = self.get(op[1])
            self.put(op[1], op[2](old))
            return old
        return super().apply(pid, op)


# Some functions, each with the name of the primitive it gives.
def inc(x):
    return x + 1          # fetch-and-increment


def set_one(x):
    return 1              # test-and-set


def put_seven(x):
    return 7              # swap(7)


def double(x):
    return 2 * x          # fetch-and-multiply by 2


def or_two(x):
    return x | 2          # fetch-and-or 2


def identity(x):
    return x              # a plain read: the trivial RMW


def cas_fn(expected, new):
    """The function of CAS(expected, new)."""

    def f(x):
        return new if x == expected else x

    f.__qualname__ = f"cas({expected},{new})"
    return f


def nontrivial_point(f, domain):
    """A value v with f(v) != v, or None if f is the identity on the domain."""
    for v in domain:
        if f(v) != v:
            return v
    return None


def consensus2(pid, value, f, v0):
    """Herlihy's protocol: the register starts at v0, where f(v0) != v0."""
    yield ("write", ("prop", pid), value)
    r = yield ("rmw", "r", f)
    if r == v0:
        return value
    other = yield ("read", ("prop", 1 - pid))
    return other


def setup_for(f, v0, values):
    def setup():
        return RMWMemory({"r": v0}), [consensus2(p, v, f, v0) for p, v in enumerate(values)]

    return setup


def classify(fs, domain):
    """Is the set of functions commuting, overwriting, or neither, on the domain?

    For each pair f, g: they commute if f(g(x)) = g(f(x)) for all x, and f
    overwrites g if f(g(x)) = f(x) for all x. Herlihy calls a set interfering
    if each pair commutes or one overwrites the other. Such a set has
    consensus number exactly 2 (if some function is nontrivial).
    """
    commute = overwrite = True
    interfering = True
    for f in fs:
        for g in fs:
            c = all(f(g(x)) == g(f(x)) for x in domain)
            fo = all(f(g(x)) == f(x) for x in domain)
            go = all(g(f(x)) == g(x) for x in domain)
            commute &= c
            overwrite &= fo or go
            interfering &= c or fo or go
    return {"commute": commute, "overwrite": overwrite, "interfering": interfering}
