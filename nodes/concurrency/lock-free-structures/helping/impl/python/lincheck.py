# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/helping/. The authors are listed in prov/4QNG5W.jsonl.
"""A brute force checker for linearizability and sequential consistency.

A history is a list of events. An event is ("inv", pid, name, arg) or
("res", pid, value). Each process has at most one pending operation.

The search is the one of Wing and Gong (1993): pick an operation that may
come next, apply it to the sequential specification, and check its result.
Under linearizability, an operation may come next only if no operation that
is still to be placed responded before it was invoked (real-time order).
Under sequential consistency, only the order of each process counts.
A memo of (placed set, state) pairs cuts the search, as in Lowe (2017).
A pending operation may be placed with any result, or left out.
"""

INF = float("inf")


class Op:
    __slots__ = ("pid", "name", "arg", "res", "inv", "ret", "pending", "idx")

    def __init__(self, pid, name, arg, inv, idx):
        self.pid, self.name, self.arg, self.inv, self.idx = pid, name, arg, inv, idx
        self.res, self.ret, self.pending = None, INF, True

    def __repr__(self):
        r = "pending" if self.pending else repr(self.res)
        return f"p{self.pid}.{self.name}({self.arg!r})->{r}"


def operations(history):
    """Turn a list of events into a list of operations with time stamps."""
    ops, open_ = [], {}
    for t, e in enumerate(history):
        if e[0] == "inv":
            if e[1] in open_:
                raise ValueError(f"process {e[1]} invokes twice without a response")
            o = Op(e[1], e[2], e[3] if len(e) > 3 else None, t, len(ops))
            ops.append(o)
            open_[e[1]] = o
        elif e[0] == "res":
            o = open_.pop(e[1])
            o.res, o.ret, o.pending = e[2], t, False
        elif e[0] != "lp":
            raise ValueError(f"bad event {e!r}")
    return ops


def _search(ops, spec, must_precede):
    n = len(ops)
    before = [0] * n
    for a in ops:
        for b in ops:
            if a is not b and must_precede(a, b):
                before[b.idx] |= 1 << a.idx
    complete = 0
    for o in ops:
        if not o.pending:
            complete |= 1 << o.idx
    seen = set()
    stack = [(0, spec.init, ())]
    while stack:
        mask, state, order = stack.pop()
        if mask & complete == complete:
            return [ops[i] for i in order]
        if (mask, state) in seen:
            continue
        seen.add((mask, state))
        for o in ops:
            bit = 1 << o.idx
            if mask & bit or before[o.idx] & ~mask:
                continue
            state2, r = spec.apply(state, o.name, o.arg, o.pid)
            if o.pending or r == o.res:
                stack.append((mask | bit, state2, order + (o.idx,)))
    return None


def linearize(history, spec):
    """A legal sequential order that respects real time, or None."""
    ops = operations(history)
    return _search(ops, spec, lambda a, b: a.ret < b.inv)


def sequential_order(history, spec):
    """A legal sequential order that respects each process order, or None."""
    ops = operations(history)
    return _search(ops, spec, lambda a, b: a.pid == b.pid and a.ret < b.inv)


def is_linearizable(history, spec):
    return linearize(history, spec) is not None


def is_sequentially_consistent(history, spec):
    return sequential_order(history, spec) is not None


def project(history, obj):
    """The events of one object, for names of the form (obj, method)."""
    out, open_ = [], {}
    for e in history:
        if e[0] == "lp":
            continue
        if e[0] == "inv":
            open_[e[1]] = e[2][0] == obj
            if open_[e[1]]:
                out.append(e)
        elif open_.pop(e[1]):
            out.append(e)
    return out


# ------------------------------------------------------------ specifications
# A specification has a hashable initial state `init` and a function
# apply(state, name, arg, pid) -> (new state, result).


class Register:
    def __init__(self, init=0):
        self.init = init

    def apply(self, s, name, arg, pid):
        if name == "read":
            return s, s
        if name == "write":
            return arg, None
        raise ValueError(name)


class Queue:
    """A FIFO queue. deq on an empty queue returns None."""

    def __init__(self, init=()):
        self.init = tuple(init)

    def apply(self, s, name, arg, pid):
        if name == "enq":
            return s + (arg,), None
        if name == "deq":
            return (s[1:], s[0]) if s else (s, None)
        raise ValueError(name)


class Stack:
    """A LIFO stack. pop on an empty stack returns None."""

    def __init__(self, init=()):
        self.init = tuple(init)

    def apply(self, s, name, arg, pid):
        if name == "push":
            return s + (arg,), None
        if name == "pop":
            return (s[:-1], s[-1]) if s else (s, None)
        raise ValueError(name)


class Counter:
    """A counter with fetch-and-add and read."""

    init = 0

    def apply(self, s, name, arg, pid):
        if name == "faa":
            return s + arg, s
        if name == "read":
            return s, s
        raise ValueError(name)


class Objects:
    """Several objects side by side. An operation name is (object, method)."""

    def __init__(self, specs):
        self.names = sorted(specs)
        self.specs = specs
        self.init = tuple(specs[k].init for k in self.names)

    def apply(self, s, name, arg, pid):
        obj, method = name
        i = self.names.index(obj)
        s2, r = self.specs[obj].apply(s[i], method, arg, pid)
        return s[:i] + (s2,) + s[i + 1:], r
