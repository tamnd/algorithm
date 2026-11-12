# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hicuts/. The authors are listed in prov/RAB6MQ.jsonl.

"""HiCuts: a decision tree for packet classification (Gupta and McKeown, 1999).

A rule is a tuple of d closed ranges (lo, hi). Rule i has priority i: the
first rule in the list that matches a packet wins. Field j has width
widths[j], so its values are 0 .. 2**widths[j] - 1.

Each node v has a box B(v) and the list R(v) of the rules that meet the box,
in priority order. If R(v) has at most binth rules, v is a leaf. Else v cuts
one dimension of its box into np equal pieces. For each dimension, np starts
at 2 and doubles while the space measure

    sm(C) = sum of the rule counts of the children + np

stays at most spfac * |R(v)|. The dimension with the smallest largest child
wins. A cut that gives every child every rule is useless and is skipped; if
all cuts are useless, the node stays a leaf with more than binth rules. The
redundancy rule of the paper is used in its simplest form: in a box, a rule
that covers the whole box hides every later rule, so those are dropped.
"""

from typing import Optional, Sequence

Range = tuple[int, int]
Rule = Sequence[Range]


def matches(rule: Rule, packet: Sequence[int]) -> bool:
    return all(lo <= x <= hi for (lo, hi), x in zip(rule, packet))


def linear_classify(rules: Sequence[Rule], packet: Sequence[int]) -> Optional[int]:
    for i, rule in enumerate(rules):
        if matches(rule, packet):
            return i
    return None


FIVE_TUPLE = (32, 32, 16, 16, 8)


def random_classifier(rng, n: int) -> list[tuple[Range, ...]]:
    """A synthetic five-field classifier with a default rule at the end.

    Addresses are prefixes of length 16, 24 or 32 from a pool of n subnets;
    the source is a wildcard in 30% of the rules. The source port is a
    wildcard or 1024 to 65535, the destination port is a wildcard, a
    well-known port or a range, and the protocol is TCP, UDP or a wildcard.
    No rule repeats. This only imitates the shape of real rule sets.
    """
    nets = [(rng.getrandbits(l), l) for l in rng.choices([16, 24, 24, 32], k=max(50, n))]
    full32, full16 = (0, (1 << 32) - 1), (0, 65535)

    def net():
        p, l = rng.choice(nets)
        return p << (32 - l), ((p + 1) << (32 - l)) - 1

    def dport():
        r = rng.random()
        if r < 0.2:
            return full16
        if r < 0.8:
            v = rng.choice([22, 25, 53, 80, 123, 443, 3306, 8080])
            return v, v
        return rng.choice([(0, 1023), (1024, 65535), (6000, 6063)])

    seen, rules = set(), []
    while len(rules) < n - 1:
        rule = (
            full32 if rng.random() < 0.3 else net(),
            net(),
            full16 if rng.random() < 0.9 else (1024, 65535),
            dport(),
            rng.choice([(6, 6), (6, 6), (17, 17), (0, 255)]),
        )
        if rule not in seen:
            seen.add(rule)
            rules.append(rule)
    rules.append((full32, full32, full16, full16, (0, 255)))  # the default rule
    return rules


class Node:
    __slots__ = ("box", "rules", "dim", "np", "children")

    def __init__(self, box, rules):
        self.box = box  # tuple of (lo, hi) for each field
        self.rules = rules  # rule indices in priority order (kept at leaves)
        self.dim = -1  # -1 marks a leaf
        self.np = 0
        self.children = []

    def is_leaf(self) -> bool:
        return self.dim < 0


class HiCuts:
    def __init__(self, rules: Sequence[Rule], widths: Sequence[int], binth: int = 4, spfac: float = 4.0):
        self.rules = [tuple(r) for r in rules]
        self.widths = tuple(widths)
        self.binth = binth
        self.spfac = spfac
        box = tuple((0, (1 << w) - 1) for w in self.widths)
        self.root = self._build(box, self._colliding(box, range(len(self.rules))))

    # -- building -------------------------------------------------------

    def _colliding(self, box, candidates) -> list[int]:
        """The rules that meet the box, without the redundant ones.

        A rule is redundant in the box if an earlier kept rule contains its
        part inside the box: no packet in the box can reach it.
        """
        out, parts = [], []
        for i in candidates:
            rule = self.rules[i]
            if not all(lo <= bh and bl <= hi for (lo, hi), (bl, bh) in zip(rule, box)):
                continue
            part = tuple((max(lo, bl), min(hi, bh)) for (lo, hi), (bl, bh) in zip(rule, box))
            if any(all(a <= c and d <= b for (a, b), (c, d) in zip(q, part)) for q in parts):
                continue
            out.append(i)
            parts.append(part)
            if part == box:
                break  # rule i matches every packet in the box
        return out

    def _child_counts(self, box, rule_ids, dim, np):
        """Rule counts of the np children of a cut, by a difference array."""
        bl, bh = box[dim]
        size = (bh - bl + 1) // np
        diff = [0] * (np + 1)
        for i in rule_ids:
            lo, hi = self.rules[i][dim]
            a = (max(lo, bl) - bl) // size
            b = (min(hi, bh) - bl) // size
            diff[a] += 1
            diff[b + 1] -= 1
        counts, run = [], 0
        for k in range(np):
            run += diff[k]
            counts.append(run)
        return counts

    def _choose_cut(self, box, rule_ids):
        n = len(rule_ids)
        best = None
        for dim in range(len(box)):
            bl, bh = box[dim]
            if bh == bl:
                continue
            np = 2
            counts = self._child_counts(box, rule_ids, dim, np)
            while 2 * np <= bh - bl + 1:
                c2 = self._child_counts(box, rule_ids, dim, 2 * np)
                if sum(c2) + 2 * np > self.spfac * n:
                    break
                np, counts = 2 * np, c2
            if sum(counts) == n * np:
                continue  # every child gets every rule: the cut is useless
            # Heuristic (d) of the paper: the most distinct range components
            # inside the box; ties go to the smaller largest child.
            distinct = len({(max(lo, bl), min(hi, bh)) for lo, hi in (self.rules[i][dim] for i in rule_ids)})
            key = (-distinct, max(counts), sum(counts) + np, dim)
            if best is None or key < best[0]:
                best = (key, dim, np)
        return best  # None if no cut is useful

    def _build(self, box, rule_ids) -> Node:
        node = Node(box, rule_ids)
        if len(rule_ids) <= self.binth:
            return node
        best = self._choose_cut(box, rule_ids)
        if best is None:
            return node  # no cut separates any rules: stop with a larger leaf
        _, dim, np = best
        node.dim, node.np, node.rules = dim, np, []
        bl, bh = box[dim]
        size = (bh - bl + 1) // np
        prev = None
        for k in range(np):
            cbox = box[:dim] + ((bl + k * size, bl + (k + 1) * size - 1),) + box[dim + 1:]
            crules = self._colliding(cbox, rule_ids)
            if prev is not None and prev.is_leaf() and len(crules) <= self.binth and prev.rules == crules:
                node.children.append(prev)  # share a leaf with the same rules
                continue
            prev = self._build(cbox, crules)
            node.children.append(prev)
        return node

    # -- lookup ---------------------------------------------------------

    def classify(self, packet: Sequence[int]) -> tuple[Optional[int], int]:
        """Return (index of the first matching rule or None, nodes visited)."""
        v = self.root  # @line L1
        visited = 1
        while not v.is_leaf():  # @line L2
            j, np = v.dim, v.np  # @line L3
            bl, bh = v.box[j]
            k = (packet[j] - bl) * np // (bh - bl + 1)  # @line L4
            v = v.children[k]  # @line L5
            visited += 1
        for i in v.rules:  # @line L6
            if matches(self.rules[i], packet):  # @line L7
                return i, visited
        return None, visited  # @line L8

    # -- statistics -----------------------------------------------------

    def stats(self) -> dict:
        """Depth, node counts and stored rule references of the tree."""
        seen = set()
        out = {"nodes": 0, "leaves": 0, "rule_refs": 0, "pointers": 0, "max_depth": 0}
        stack = [(self.root, 0)]
        while stack:
            v, depth = stack.pop()
            if id(v) in seen:
                continue
            seen.add(id(v))
            out["nodes"] += 1
            out["max_depth"] = max(out["max_depth"], depth)
            if v.is_leaf():
                out["leaves"] += 1
                out["rule_refs"] += len(v.rules)
            else:
                out["pointers"] += v.np
                stack.extend((c, depth + 1) for c in v.children)
        return out

    def check(self) -> None:
        """Check the tree invariants; raise AssertionError if one fails."""
        everything = range(len(self.rules))
        stack = [(self.root, self.root.box)]
        while stack:
            v, box = stack.pop()  # box is the region of the slot that points to v
            if v.is_leaf():
                assert v.rules == self._colliding(box, everything)
                if len(v.rules) > self.binth:
                    assert self._choose_cut(box, v.rules) is None
                continue
            assert v.box == box
            bl, bh = box[v.dim]
            size = (bh - bl + 1) // v.np
            assert v.np >= 2 and size * v.np == bh - bl + 1 and len(v.children) == v.np
            for k, c in enumerate(v.children):
                cbox = box[: v.dim] + ((bl + k * size, bl + (k + 1) * size - 1),) + box[v.dim + 1:]
                stack.append((c, cbox))
