# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/route-origin-validation/. The authors are listed in prov/BC5B6R.jsonl.

"""Route origin validation of RFC 6811, Section 2, with a binary trie of VRPs.

A VRP (validated ROA payload) is (prefix, max_length, asn). A route is a
prefix and an AS_PATH given as a list of (segment_type, [asn, ...]). The
examples use documentation prefixes and documentation AS numbers only.
"""

from ipaddress import IPv4Network, IPv6Network, ip_network
from typing import Iterable

Network = IPv4Network | IPv6Network
Vrp = tuple[str, int, int]

NOT_FOUND, VALID, INVALID = "NotFound", "Valid", "Invalid"
NONE = None  # the distinguished origin "NONE" of RFC 6811


def origin_asn(as_path: list[tuple[str, list[int]]], own_as: int) -> int | None:
    """The route origin ASN of RFC 6811, Section 2.

    The rightmost AS of the final segment if it is an AS_SEQUENCE; the
    speaker's own AS if the path is empty or the final segment is a
    confederation segment; NONE otherwise (for example an AS_SET). Cost: O(1).
    """
    if not as_path:
        return own_as
    kind, asns = as_path[-1]
    if kind == "AS_SEQUENCE" and asns:
        return asns[-1]
    if kind in ("AS_CONFED_SEQUENCE", "AS_CONFED_SET"):
        return own_as
    return NONE


def bits(net: Network) -> int:
    """The prefix address as an integer of 32 or 128 bits."""
    return int(net.network_address)


class _Node:
    __slots__ = ("child", "vrps")

    def __init__(self) -> None:
        self.child: list["_Node | None"] = [None, None]
        self.vrps: list[tuple[int, int]] = []  # (max_length, asn)


class VrpTrie:
    """A binary trie per address family; each VRP is stored at the node of its prefix."""

    def __init__(self, vrps: Iterable[Vrp] = ()) -> None:
        """Cost: O(total prefix length of the VRPs)."""
        self.roots = {4: _Node(), 6: _Node()}
        for v in vrps:
            self.add(v)

    def add(self, vrp: Vrp) -> None:
        """Precondition: prefix is a valid network and len <= max_length <= width."""
        prefix, max_length, asn = vrp
        net = ip_network(prefix)
        width = net.max_prefixlen
        node = self.roots[net.version]
        a = bits(net)
        for i in range(net.prefixlen):
            b = (a >> (width - 1 - i)) & 1
            if node.child[b] is None:
                node.child[b] = _Node()
            node = node.child[b]
        node.vrps.append((max_length, asn))

    def validate(self, prefix: str, origin: int | None) -> str:
        """The validation state of a route with this prefix and origin ASN.

        Visits only the nodes on the path of the prefix, so the cost is
        O(len + c) for a prefix of length len and c covering VRPs.
        """
        net = ip_network(prefix)
        width, length, a = net.max_prefixlen, net.prefixlen, bits(net)
        state = NOT_FOUND  # @line L1
        node = self.roots[net.version]  # @line L2
        for i in range(length + 1):  # @line L3
            for max_length, asn in node.vrps:  # @line L4
                state = INVALID  # @line L5
                if length <= max_length and origin is not NONE and asn != 0 and asn == origin:  # @line L6
                    return VALID
            if i == length:  # @line L7
                break
            node = node.child[(a >> (width - 1 - i)) & 1]
            if node is None:
                break
        return state  # @line L8


def validate_linear(vrps: Iterable[Vrp], prefix: str, origin: int | None) -> str:
    """The oracle: the definitions of RFC 6811, Section 2, checked VRP by VRP. Cost: O(|vrps|)."""
    route = ip_network(prefix)
    covered = matched = False
    for p, max_length, asn in vrps:
        q = ip_network(p)
        if q.version != route.version or q.prefixlen > route.prefixlen:
            continue
        if route.supernet(new_prefix=q.prefixlen) != q:
            continue
        covered = True
        if route.prefixlen <= max_length and origin is not NONE and asn != 0 and origin == asn:
            matched = True
    if matched:
        return VALID
    return INVALID if covered else NOT_FOUND
