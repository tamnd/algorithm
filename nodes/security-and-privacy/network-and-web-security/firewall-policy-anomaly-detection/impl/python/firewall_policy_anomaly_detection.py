# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/firewall-policy-anomaly-detection/. The authors are listed in prov/MRZ666.jsonl.

"""Anomalies between pairs of rules in an ordered firewall policy.

A rule matches a box: one closed integer interval for each header field, for
example protocol, source address, source port, destination address and
destination port. The first rule that matches a packet decides it. For an
earlier rule Rx and a later rule Ry, the classes follow Al-Shaer and Hamed
(2004):

* shadowing: Ry is inside Rx and the actions differ, so Ry never acts;
* redundancy-later: Ry is inside Rx with the same action, so Ry can go;
* generalization: Rx is strictly inside Ry and the actions differ;
* redundancy-earlier: Rx is strictly inside Ry with the same action, and no
  rule between them meets Rx with another action, so Rx can go;
* correlation: the boxes overlap, neither contains the other, and the actions
  differ.

The code only reads rule lists. It does not touch any network.
"""

import ipaddress
from typing import NamedTuple, Optional

Box = tuple  # ((lo, hi), ...) with lo <= hi in each field

DISJOINT, EQUAL, SUBSET, SUPERSET, CORRELATED = "disjoint", "equal", "subset", "superset", "correlated"


class Rule(NamedTuple):
    box: Box
    action: str


class Anomaly(NamedTuple):
    kind: str
    x: int  # 1-based index of the earlier rule
    y: int  # 1-based index of the later rule
    removable: Optional[int]  # the rule that can be removed, if any


def relation(a: Box, b: Box) -> str:
    """How box a relates to box b. SUBSET means a is strictly inside b.

    Cost: O(d) for d fields. A box is a product of intervals, so a is inside b
    exactly when each interval of a is inside the one of b.
    """
    a_in_b = b_in_a = True
    for (alo, ahi), (blo, bhi) in zip(a, b, strict=True):
        if ahi < blo or bhi < alo:
            return DISJOINT
        a_in_b = a_in_b and blo <= alo and ahi <= bhi
        b_in_a = b_in_a and alo <= blo and bhi <= ahi
    if a_in_b and b_in_a:
        return EQUAL
    if a_in_b:
        return SUBSET
    if b_in_a:
        return SUPERSET
    return CORRELATED


def anomalies(rules: list[Rule]) -> list[Anomaly]:
    """ANOMALIES of the page. Cost: O(m^2 d) for m rules of d fields."""
    out: list[Anomaly] = []  # @line L1
    for x in range(len(rules)):  # @line L2
        blocked = False  # @line L3
        for y in range(x + 1, len(rules)):  # @line L4
            rel = relation(rules[x].box, rules[y].box)  # @line L5
            same = rules[x].action == rules[y].action
            if rel != DISJOINT:  # @line L6
                if rel in (EQUAL, SUPERSET):  # @line L7
                    kind = "redundancy-later" if same else "shadowing"
                    out.append(Anomaly(kind, x + 1, y + 1, y + 1 if same else None))
                elif rel == SUBSET and not same:  # @line L8
                    out.append(Anomaly("generalization", x + 1, y + 1, None))
                elif rel == SUBSET and not blocked:  # @line L9
                    out.append(Anomaly("redundancy-earlier", x + 1, y + 1, x + 1))
                elif rel == CORRELATED and not same:  # @line L10
                    out.append(Anomaly("correlation", x + 1, y + 1, None))
                if not same:  # @line L11
                    blocked = True
    return out  # @line L12


def decide(rules: list[Rule], packet: tuple, default: str = "deny") -> str:
    """The action of the first rule that matches, or the default."""
    for r in rules:
        if all(lo <= v <= hi for (lo, hi), v in zip(r.box, packet, strict=True)):
            return r.action
    return default


def subtract(a: Box, b: Box) -> list[Box]:
    """Disjoint boxes whose union is a minus b. At most 2d of them."""
    if relation(a, b) == DISJOINT:
        return [a]
    out = []
    cur = list(a)
    for i, ((lo, hi), (blo, bhi)) in enumerate(zip(a, b, strict=True)):
        if lo < blo:
            out.append(tuple(cur[:i] + [(lo, blo - 1)] + cur[i + 1 :]))
        if bhi < hi:
            out.append(tuple(cur[:i] + [(bhi + 1, hi)] + cur[i + 1 :]))
        cur[i] = (max(lo, blo), min(hi, bhi))
    return out


def is_dead(rules: list[Rule], y: int) -> bool:
    """True when the earlier rules together cover rule y (1-based), so it never
    decides a packet. This catches shadowing by a union of rules, which the
    pairwise test misses. The number of pieces can grow fast with the rules."""
    pieces = [rules[y - 1].box]
    for r in rules[: y - 1]:
        pieces = [p for piece in pieces for p in subtract(piece, r.box)]
        if not pieces:
            return True
    return False


ANY_PORT = (0, 65535)
ANY_PROTOCOL = (0, 255)
PROTOCOL = {"tcp": (6, 6), "udp": (17, 17), "any": ANY_PROTOCOL}


def prefix(s: str) -> tuple[int, int]:
    """The address interval of an IPv4 or IPv6 prefix such as 192.0.2.0/24."""
    net = ipaddress.ip_network(s, strict=True)
    return int(net.network_address), int(net.broadcast_address)


def port(s: str) -> tuple[int, int]:
    if s == "any":
        return ANY_PORT
    lo, _, hi = s.partition("-")
    return int(lo), int(hi or lo)


def rule(protocol: str, src: str, sport: str, dst: str, dport: str, action: str) -> Rule:
    """A rule from text fields, in the order of the page."""
    return Rule((PROTOCOL[protocol], prefix(src), port(sport), prefix(dst), port(dport)), action)
