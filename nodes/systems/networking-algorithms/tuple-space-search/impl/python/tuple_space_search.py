# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tuple-space-search/. The authors are listed in prov/DFBVFN.jsonl.

"""Tuple space search for packet classification (Srinivasan, Suri and Varghese, 1999).

A rule has one prefix (p, l) for each field: p is the top l bits of the
field, and l = 0 is a wildcard. The tuple of a rule is its vector of prefix
lengths (l_1, ..., l_d). All rules with the same tuple go into one hash
table, keyed by their vector of prefix values. A lookup probes each table
once with the packet bits cut to that tuple, and keeps the best rule found.

A smaller priority value wins; ties go to the smaller rule id. Three lookups
are given: the basic one, one that visits the tuples in order of their best
priority and stops early (as in the Open vSwitch classifier), and pruned
tuple space search, which first finds for each field the tuples that can
match and probes only the tuples that every field allows.
"""

import bisect
from typing import Optional, Sequence

Prefix = tuple[int, int]  # (value, length)


def key_of(packet: Sequence[int], lengths: Sequence[int], widths: Sequence[int]) -> tuple[int, ...]:
    """The top lengths[i] bits of each field of the packet."""
    return tuple(x >> (w - l) for x, l, w in zip(packet, lengths, widths))


def rule_matches(prefixes: Sequence[Prefix], packet: Sequence[int], widths: Sequence[int]) -> bool:
    return all(x >> (w - l) == p for (p, l), x, w in zip(prefixes, packet, widths))


class TupleSpace:
    def __init__(self, widths: Sequence[int]):
        self.widths = tuple(widths)
        # tuple of lengths -> {tuple of values -> sorted list of (priority, rule id)}
        self.tables: dict[tuple[int, ...], dict[tuple[int, ...], list]] = {}
        self.rules: dict[int, tuple[tuple[Prefix, ...], int]] = {}
        # for pruning: field i -> {(value, length) -> {tuple: count of rules}}
        self.field_index = [dict() for _ in self.widths]

    def __len__(self) -> int:
        return len(self.rules)

    def tuples(self) -> list[tuple[int, ...]]:
        return list(self.tables)

    def insert(self, rule_id: int, prefixes: Sequence[Prefix], priority: int) -> None:
        if rule_id in self.rules:
            raise KeyError(f"rule {rule_id} is already present")
        prefixes = tuple(prefixes)
        for (p, l), w in zip(prefixes, self.widths):
            if not (0 <= l <= w and 0 <= p < (1 << l)):
                raise ValueError("bad prefix")
        t = tuple(l for _, l in prefixes)
        key = tuple(p for p, _ in prefixes)
        bucket = self.tables.setdefault(t, {}).setdefault(key, [])
        bisect.insort(bucket, (priority, rule_id))
        self.rules[rule_id] = (prefixes, priority)
        for i, pl in enumerate(prefixes):
            counts = self.field_index[i].setdefault(pl, {})
            counts[t] = counts.get(t, 0) + 1

    def delete(self, rule_id: int) -> bool:
        if rule_id not in self.rules:
            return False
        prefixes, priority = self.rules.pop(rule_id)
        t = tuple(l for _, l in prefixes)
        key = tuple(p for p, _ in prefixes)
        table = self.tables[t]
        bucket = table[key]
        bucket.remove((priority, rule_id))
        if not bucket:
            del table[key]
            if not table:
                del self.tables[t]  # an empty tuple costs a probe, so drop it
        for i, pl in enumerate(prefixes):
            counts = self.field_index[i][pl]
            counts[t] -= 1
            if counts[t] == 0:
                del counts[t]
                if not counts:
                    del self.field_index[i][pl]
        return True

    # -- lookups ----------------------------------------------------------

    def lookup(self, packet: Sequence[int]) -> tuple[Optional[int], int]:
        """Basic tuple space search: (best rule id or None, hash probes)."""
        best = None  # @line L1
        probes = 0
        for t, table in self.tables.items():  # @line L2
            key = key_of(packet, t, self.widths)  # @line L3
            bucket = table.get(key)  # @line L4
            probes += 1
            if bucket is not None and (best is None or bucket[0] < best):  # @line L5
                best = bucket[0]
        return (best[1] if best else None), probes  # @line L6

    def lookup_sorted(self, packet: Sequence[int]) -> tuple[Optional[int], int]:
        """Visit tuples by their best priority and stop when no tuple can win."""
        order = sorted(self.tables.items(), key=lambda item: min(b[0] for b in item[1].values()))
        best, probes = None, 0
        for t, table in order:
            top = min(b[0] for b in table.values())
            if best is not None and best <= top:
                break  # every rule of this and later tuples is worse than best
            bucket = table.get(key_of(packet, t, self.widths))
            probes += 1
            if bucket is not None and (best is None or bucket[0] < best):
                best = bucket[0]
        return (best[1] if best else None), probes

    def candidate_tuples(self, packet: Sequence[int]) -> set:
        """Pruning: the tuples that each field allows, intersected."""
        allowed = None
        for i, (x, w) in enumerate(zip(packet, self.widths)):
            here = set()
            index = self.field_index[i]
            for l in range(w + 1):  # every prefix of x_i that some rule uses
                counts = index.get((x >> (w - l), l))
                if counts:
                    here.update(counts)
            allowed = here if allowed is None else allowed & here
            if not allowed:
                break
        return allowed or set()

    def lookup_pruned(self, packet: Sequence[int]) -> tuple[Optional[int], int]:
        best, probes = None, 0
        for t in self.candidate_tuples(packet):
            bucket = self.tables[t].get(key_of(packet, t, self.widths))
            probes += 1
            if bucket is not None and (best is None or bucket[0] < best):
                best = bucket[0]
        return (best[1] if best else None), probes


def linear_classify(rules, packet, widths) -> Optional[int]:
    """Reference: rules is a list of (rule id, prefixes, priority)."""
    best = None
    for rid, prefixes, priority in rules:
        if rule_matches(prefixes, packet, widths) and (best is None or (priority, rid) < best):
            best = (priority, rid)
    return best[1] if best else None


def range_to_prefixes(lo: int, hi: int, w: int) -> list[Prefix]:
    """The fewest prefixes whose union is [lo, hi] (greedy aligned blocks)."""
    out = []
    while lo <= hi:
        size = lo & -lo if lo else 1 << w
        while size > hi - lo + 1:
            size >>= 1
        k = size.bit_length() - 1
        out.append((lo >> k, w - k))
        lo += size
    return out


FIVE_TUPLE = (32, 32, 16, 16, 8)


def random_prefix_classifier(rng, n: int) -> list[tuple[int, tuple[Prefix, ...], int]]:
    """A synthetic five-field prefix classifier: (rule id, prefixes, priority).

    Addresses are prefixes of length 8, 16, 24 or 32 from a pool of subnets,
    or wildcards. Ports are exact, wildcards, or the range 1024 to 65535
    expanded into its 6 prefixes. The protocol is exact or a wildcard. The
    priority is the position in the list; a last rule matches everything.
    """
    nets = [(rng.getrandbits(l), l) for l in rng.choices([8, 16, 24, 24, 32], k=max(50, n))]
    out = []
    while len(out) < n - 1:
        src = rng.choice(nets) if rng.random() < 0.7 else (0, 0)
        dst = rng.choice(nets) if rng.random() < 0.95 else (0, 0)
        sports = [(0, 0)] if rng.random() < 0.9 else range_to_prefixes(1024, 65535, 16)
        r = rng.random()
        if r < 0.2:
            dports = [(0, 0)]
        elif r < 0.9:
            dports = [(rng.choice([22, 25, 53, 80, 123, 443, 3306, 8080]), 16)]
        else:
            dports = range_to_prefixes(1024, 65535, 16)
        proto = rng.choice([(6, 8), (6, 8), (17, 8), (0, 0)])
        prio = len(out)
        for sp in sports:
            for dp in dports:
                if len(out) < n - 1:
                    out.append((len(out), (src, dst, sp, dp, proto), prio))
    out.append((n - 1, ((0, 0),) * 5, n - 1))
    return out
