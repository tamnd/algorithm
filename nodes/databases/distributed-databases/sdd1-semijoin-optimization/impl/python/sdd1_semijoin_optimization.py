# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sdd1-semijoin-optimization/. The authors are listed in prov/ER70WT.jsonl.

"""Algorithm OPT of SDD-1: a greedy choice of semijoins before the relations move to one site.

The query is the natural join of some relations, each stored at one site, after
local selections. Attributes with the same name are joined, and each attribute
name has one domain with a size c(X) and a width w(X).

The database profile holds c(R) for each relation and c(R.A), the number of
distinct values of R.A. The estimates follow Bernstein et al. (1981):

* R[A] is a random subset of its domain. Each set of values is described by its
  lineage, a set of selection edges with labels in (0, 1]; its selectivity is the
  product of the labels, and its estimated size is the selectivity times c(X).
  At the start R[A] has one edge with label c(R.A) / c(X).
* The semijoin R_i <A] R_j maps R_i[A] to R_i[A] & R_j[A]; the new lineage is the
  union of the two lineages. The new c(R_i) is c(R_i.A)new * c(R_i) / c(R_i.A)old,
  since the tuples are spread evenly over the values. For every other attribute
  A' of R_i, c(R_i.A') becomes the piecewise form of Yao's function of the new
  c(R_i) and the old c(R_i.A'), and R_i[A'] gets an edge with the ratio new/old.
* The cost of R_i <A] R_j is c(R_j.A) * w(A), or 0 at the same site. The benefit
  is (c(R_i) before - c(R_i) after) * width(R_i).

OPT appends the most profitable nonlocal semijoin while one has benefit > cost
(each semijoin at most once: in a cyclic query the estimates can otherwise shrink
forever through Yao's function, so the loop would not end),
chooses the assembly site with the largest estimated data, and then prunes
semijoins that reduce a relation at the assembly site when the program costs
less without them. The cost counts transmitted data only; local work and the
number of messages are free.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from fractions import Fraction
from collections.abc import Callable, Mapping, Sequence


def yao_approx(n, b):
    """The piecewise approximation of Yao's function: the expected number of distinct
    values left when n of the tuples are kept, for b distinct values before."""
    if n < Fraction(b) / 2:
        return Fraction(n)
    if n < 2 * b:
        return Fraction(n + b) / 3
    return Fraction(b)


# ---------------------------------------------------------------- the profile and its estimates


@dataclass
class Profile:
    domains: dict            # attribute -> (c(X), w(X)); c(X) may be None for an attribute no clause uses
    sites: dict              # relation -> site
    card: dict               # relation -> c(R)
    distinct: dict           # relation -> {attribute: c(R.A)} for the attributes with a known count
    schema: dict             # relation -> all attributes of the query in R (they make up its width)

    def width(self, r: str) -> int:
        return sum(self.domains[a][1] for a in self.schema[r])


@dataclass
class Estimate:
    """The changing estimates while a program is replayed."""
    profile: Profile
    card: dict = field(default_factory=dict)
    distinct: dict = field(default_factory=dict)
    lineage: dict = field(default_factory=dict)   # (relation, attribute) -> frozenset of edge ids
    labels: list = field(default_factory=list)    # edge id -> label

    @classmethod
    def start(cls, p: Profile) -> "Estimate":
        e = cls(p)
        for r in p.card:
            e.card[r] = Fraction(p.card[r])
            e.distinct[r] = {}
            for a, c in p.distinct[r].items():
                e.distinct[r][a] = Fraction(c)
                e.lineage[r, a] = frozenset([e._edge(Fraction(c, p.domains[a][0]))])
        return e

    def _edge(self, label: Fraction) -> int:
        self.labels.append(Fraction(label))
        return len(self.labels) - 1

    def selectivity(self, lin: frozenset) -> Fraction:
        out = Fraction(1)
        for k in lin:
            out *= self.labels[k]
        return out

    def _shrink_others(self, r: str, a: str, old_card: Fraction) -> None:
        for b in self.distinct[r]:
            if b == a:
                continue
            old = self.distinct[r][b]
            new = yao_approx(self.card[r], old)
            if old and new < old:
                self.lineage[r, b] = self.lineage[r, b] | {self._edge(new / old)}
            self.distinct[r][b] = new

    def select(self, r: str, a: str, factor) -> None:
        """A local selection on r.A that keeps the fraction factor of the values of r.A."""
        factor = Fraction(factor)
        old_card, old = self.card[r], self.distinct[r][a]
        self.lineage[r, a] = self.lineage[r, a] | {self._edge(factor)}
        self.distinct[r][a] = old * factor
        self.card[r] = old_card * factor
        self._shrink_others(r, a, old_card)

    def effect(self, i: str, j: str, a: str) -> tuple[Fraction, Fraction, frozenset]:
        """(new c(R_i), new c(R_i.A), new lineage) of R_i <A] R_j, without applying it."""
        lin = self.lineage[i, a] | self.lineage[j, a]
        new_a = self.selectivity(lin) * self.profile.domains[a][0]
        old_a = self.distinct[i][a]
        new_card = new_a * self.card[i] / old_a if old_a else Fraction(0)
        return new_card, new_a, lin

    def cost(self, i: str, j: str, a: str) -> Fraction:
        if self.profile.sites[i] == self.profile.sites[j]:
            return Fraction(0)
        return self.distinct[j][a] * self.profile.domains[a][1]

    def benefit(self, i: str, j: str, a: str) -> Fraction:
        new_card, _, _ = self.effect(i, j, a)
        return (self.card[i] - new_card) * self.profile.width(i)

    def semijoin(self, i: str, j: str, a: str) -> None:
        new_card, new_a, lin = self.effect(i, j, a)
        old_card = self.card[i]
        self.lineage[i, a] = lin
        self.distinct[i][a] = new_a
        self.card[i] = new_card
        self._shrink_others(i, a, old_card)

    def size(self, r: str) -> Fraction:
        return self.card[r] * self.profile.width(r)


def candidates(p: Profile) -> list[tuple[str, str, str]]:
    """Every nonlocal semijoin R_i <A] R_j of the query: i != j at different sites, A common."""
    out = []
    for i in sorted(p.card):
        for j in sorted(p.card):
            if i != j and p.sites[i] != p.sites[j]:
                for a in sorted(set(p.distinct[i]) & set(p.distinct[j])):
                    out.append((i, j, a))
    return out


def choose_site(est: Estimate) -> object:
    """The site with the largest estimated data of the query (the first one on a tie)."""
    size: Counter = Counter()
    for r in sorted(est.card):
        size[est.profile.sites[r]] += est.size(r)
    return max(sorted(size, key=repr), key=lambda s: size[s])


def replay(p: Profile, program: Sequence[tuple], assembly=None) -> tuple[Fraction, Fraction, object, Estimate]:
    """Replay a program through the estimates. Return (cost of the semijoins, cost of moving
    the reduced relations to the assembly site, the assembly site, the final estimates)."""
    est = Estimate.start(p)
    sj_cost = Fraction(0)
    for op in program:
        if op[0] == "select":
            est.select(op[1], op[2], op[3])
        else:
            _, i, j, a = op
            sj_cost += est.cost(i, j, a)
            est.semijoin(i, j, a)
    site = choose_site(est) if assembly is None else assembly
    move = sum((est.size(r) for r in sorted(p.card) if p.sites[r] != site), Fraction(0))
    return sj_cost, move, site, est


@dataclass
class Plan:
    program: list                 # local selections, then semijoins ("semijoin", i, j, A)
    assembly: object
    cost: Fraction                # estimated cost after pruning
    cost_before_pruning: Fraction
    trace: list                   # per step: (chosen semijoin, cost, benefit)
    pruned: list


def opt(p: Profile, selections: Sequence[tuple] = (), prune: bool = True, max_steps: int = 1000) -> Plan:
    """Algorithm OPT. selections are (relation, attribute, factor) local selections."""
    est = Estimate.start(p)
    program = []
    for r, a, f in selections:  # @line L1
        est.select(r, a, f)
        program.append(("select", r, a, Fraction(f)))  # @line L2
    cands = candidates(p)
    used = set()
    trace = []
    for _ in range(max_steps):
        best = None
        for sj in cands:  # @line L3
            if sj in used:
                continue
            profit = est.benefit(*sj) - est.cost(*sj)
            if profit > 0 and (best is None or profit > best[0]):
                best = (profit, sj)  # @line L4
        if best is None:
            break
        sj = best[1]
        used.add(sj)
        trace.append((sj, est.cost(*sj), est.benefit(*sj)))
        program.append(("semijoin",) + sj)  # @line L5
        est.semijoin(*sj)
    site = choose_site(est)  # @line L6
    sj_cost, move, _, _ = replay(p, program, site)
    before = sj_cost + move
    pruned = []
    if prune:
        k = 0
        while k < len(program):  # @line L7
            op = program[k]
            if op[0] == "semijoin" and p.sites[op[1]] == site:
                without = program[:k] + program[k + 1:]
                c, m, _, _ = replay(p, without, site)
                if c + m < sj_cost + move:
                    pruned.append(op)
                    program, sj_cost, move = without, c, m
                    continue
            k += 1
    return Plan(program, site, sj_cost + move, before, trace, pruned)  # @line L8


# ---------------------------------------------------------------- execution on data


@dataclass
class Table:
    schema: tuple
    rows: Counter                  # tuple -> count (bag semantics)

    def col(self, a: str) -> int:
        return self.schema.index(a)


def _cols(t: Table, a) -> list[int]:
    return [t.col(x) for x in ((a,) if isinstance(a, str) else a)]


def semijoin_values(t: Table, a) -> set:
    """The distinct non-null values of t.A (A is one attribute or a tuple of them), which
    is what a semijoin ships."""
    ks = _cols(t, a)
    vals = {tuple(row[k] for k in ks) for row in t.rows}
    return {v for v in vals if None not in v}


def reduce_by(t: Table, a, values: set) -> Table:
    ks = _cols(t, a)
    return Table(t.schema, Counter({row: c for row, c in t.rows.items() if tuple(row[k] for k in ks) in values}))


def _width(widths: Mapping[str, int], a) -> int:
    return sum(widths[x] for x in ((a,) if isinstance(a, str) else a))


def hash_join(r: Table, s: Table) -> Table:
    common = [a for a in r.schema if a in s.schema]
    rest = [a for a in s.schema if a not in common]
    rk = [r.col(a) for a in common]
    sk = [s.col(a) for a in common]
    sr = [s.col(a) for a in rest]
    table: dict = {}
    for row, c in s.rows.items():
        key = tuple(row[k] for k in sk)
        if None not in key:
            table.setdefault(key, []).append((row, c))
    out: Counter = Counter()
    for row, c in r.rows.items():
        key = tuple(row[k] for k in rk)
        for srow, d in table.get(key, ()):
            out[row + tuple(srow[k] for k in sr)] += c * d
    return Table(r.schema + tuple(rest), out)


@dataclass
class Run:
    result: Table
    semijoin_bytes: int
    move_bytes: int
    reduced: dict


def execute(tables: Mapping[str, Table], sites: Mapping[str, object], widths: Mapping[str, int],
            program: Sequence[tuple], assembly, predicates: Mapping[str, Callable] | None = None) -> Run:
    """Run a program on data. A ("select", R, ...) step applies predicates[R]. A semijoin
    ships the distinct values of R_j.A (if the sites differ) and keeps the rows of R_i
    whose A is among them. Then all relations move to the assembly site and are joined."""
    cur = dict(tables)
    sj_bytes = 0
    for op in program:
        if op[0] == "select":
            r = op[1]
            pred = (predicates or {}).get(r)
            if pred is not None:
                t = cur[r]
                cur[r] = Table(t.schema, Counter({row: c for row, c in t.rows.items()
                                                   if pred(dict(zip(t.schema, row))) is True}))
        else:
            _, i, j, a = op
            vals = semijoin_values(cur[j], a)
            if sites[i] != sites[j]:
                sj_bytes += len(vals) * _width(widths, a)
            cur[i] = reduce_by(cur[i], a, vals)
    move = 0
    for r in sorted(cur):
        if sites[r] != assembly:
            move += sum(cur[r].rows.values()) * sum(widths[a] for a in cur[r].schema)
    names = sorted(cur)
    result = cur[names[0]]
    for r in names[1:]:
        result = hash_join(result, cur[r])
    return Run(result, sj_bytes, move, cur)


def full_reducer(parent: Mapping[str, str | None], schemas: Mapping[str, Sequence[str]]) -> list[tuple]:
    """The semijoin program of Bernstein and Chiu for a tree query given as a rooted join
    tree (parent[root] is None): semijoins from the leaves up, then from the root down.
    Each semijoin uses all the attributes that the two relations have in common."""
    children: dict = {r: [] for r in parent}
    root = None
    for r in sorted(parent):
        if parent[r] is None:
            root = r
        else:
            children[parent[r]].append(r)
    order = []

    def walk(r):
        order.append(r)
        for c in children[r]:
            walk(c)

    walk(root)
    common = lambda r: tuple(sorted(set(schemas[r]) & set(schemas[parent[r]])))
    up = [("semijoin", parent[r], r, common(r)) for r in reversed(order) if parent[r] is not None]
    down = [("semijoin", r, parent[r], common(r)) for r in order if parent[r] is not None]
    return up + down
