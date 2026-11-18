# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/higher-order-ivm/. The authors are listed in prov/0ABZ30.jsonl.

"""Higher-order incremental view maintenance by the viewlet transform.

The query is a sum over a natural join of distinct relations (no self-join):

    Q[F] = SUM over the join of R_1, ..., R_k of the product of the values x_v, v in VALS,

grouped by the variables F. Relations have integer weights (a weight w > 0 is
w copies, w < 0 is a deletion). With VALS empty, Q is COUNT(*).

For each set S of atoms other than the set of all atoms, the program keeps a
map M_S, the delta of Q with respect to the atoms of S. With rem the atoms not
in S and Vars(X) the variables of the atoms in X:

    K_S = Vars(rem) & (Vars(S) | F)          the key of M_S
    Z_S = Vars(rem) - K_S                    the variables summed out
    M_S(y) = SUM over z of PROD_{i in rem} R_i(y, z) * PROD_{v in VALS & Z_S} z_v

M_{} is Q (without the value factors of F), and M_{all atoms}() = 1. An update
of tuple t with weight w to atom j changes only the maps with j not in S, and

    M_S(y) += w * PROD_{v in VALS & Z_S & V_j} t_v * M_{S + j}(y'),

where y' runs over the entries of M_{S + j} that agree with t, and y is y' with t,
cut to K_S. No join is evaluated: every update is lookups, products and sums.
"""

from collections import Counter
from collections.abc import Mapping, Sequence


class HigherOrderIVM:
    def __init__(self, atoms: Mapping[str, Sequence[str]], vals: Sequence[str] = (),
                 group: Sequence[str] = ()) -> None:
        self.names = list(atoms)
        self.vars = {n: tuple(atoms[n]) for n in self.names}
        for n, vs in self.vars.items():
            if len(set(vs)) != len(vs):
                raise ValueError("atom %r repeats a variable" % n)
        allv = set().union(*map(set, self.vars.values()))
        if not set(vals) <= allv or not set(group) <= allv:
            raise ValueError("unknown variable in vals or group")
        self.vals = frozenset(vals)
        self.group = tuple(group)
        self.full = frozenset(self.names)
        self.key: dict = {}
        self.zvars: dict = {}
        self.maps: dict = {}
        k = len(self.names)
        for mask in range(1 << k):  # @line L1
            s = frozenset(self.names[i] for i in range(k) if mask >> i & 1)
            rem = self.full - s
            vrem = set().union(*(set(self.vars[n]) for n in rem)) if rem else set()
            vs = set().union(*(set(self.vars[n]) for n in s)) if s else set()
            key = tuple(sorted(vrem & (vs | set(self.group))))
            self.key[s] = key
            self.zvars[s] = vrem - set(key)
            self.maps[s] = Counter({(): 1}) if s == self.full else Counter()
        self.work = 0

    def update(self, name: str, t: Sequence, w: int = 1) -> None:
        """Apply weight w of tuple t to relation name."""
        vj = self.vars[name]
        if len(t) != len(vj):
            raise ValueError("tuple %r does not fit %r" % (t, vj))
        bind = dict(zip(vj, t))
        # The child S + j does not contain j, so the order of the maps does not matter.
        for s in self.maps:  # @line L2
            if name in s:
                continue
            child = s | {name}  # @line L3
            ckey = self.key[child]
            factor = w
            for v in self.vals & self.zvars[s] & set(vj):
                factor *= bind[v]
            out = self.maps[s]
            for yc, c in list(self.maps[child].items()):  # @line L4
                self.work += 1
                env = dict(zip(ckey, yc))
                if any(env[v] != bind[v] for v in ckey if v in bind):
                    continue
                env.update(bind)
                y = tuple(env[v] for v in self.key[s])  # @line L5
                out[y] += factor * c  # @line L6
                if out[y] == 0:
                    del out[y]  # @line L7

    def result(self) -> dict:
        """Q as a dict from group values (in the order of group) to the sum; zero groups are absent."""
        top = self.maps[frozenset()]
        pos = [self.key[frozenset()].index(v) for v in self.group]
        res = {}
        for y, c in top.items():  # @line L8
            g = tuple(y[i] for i in pos)
            for v, x in zip(self.key[frozenset()], y):
                if v in self.vals:
                    c *= x
            if c:
                res[g] = c
        return res


def brute_force(atoms: Mapping[str, Sequence[str]], rels: Mapping[str, Mapping], vals=(), group=()) -> dict:
    """Q by enumeration of the join of the weighted relations, for tests."""
    names = list(atoms)
    envs = [({}, 1)]
    for n in names:
        nxt = []
        for env, wt in envs:
            for t, w in rels.get(n, {}).items():
                if any(env.get(v, x) != x for v, x in zip(atoms[n], t)):
                    continue
                e = dict(env)
                e.update(zip(atoms[n], t))
                nxt.append((e, wt * w))
        envs = nxt
    res: Counter = Counter()
    for env, wt in envs:
        for v in vals:
            wt *= env[v]
        res[tuple(env[v] for v in group)] += wt
    return {g: c for g, c in res.items() if c}


def map_definition(ivm: HigherOrderIVM, rels: Mapping[str, Mapping], s: frozenset) -> dict:
    """M_S by its definition, for tests: the sum over the atoms not in S, grouped by K_S."""
    rem = [n for n in ivm.names if n not in s]
    sub = {n: ivm.vars[n] for n in rem}
    vals = tuple(sorted(ivm.vals & ivm.zvars[s]))
    if not rem:
        return {(): 1}
    return brute_force(sub, rels, vals, ivm.key[s])
