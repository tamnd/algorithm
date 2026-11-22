# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/route-origin-validation/. The authors are listed in prov/BC5B6R.jsonl.

import random
from ipaddress import ip_address, ip_network

from route_origin_validation import (
    INVALID,
    NONE,
    NOT_FOUND,
    VALID,
    VrpTrie,
    origin_asn,
    validate_linear,
)

EXAMPLE_VRPS = [
    ("192.0.2.0/24", 24, 64496),
    ("198.51.100.0/24", 25, 64497),
    ("203.0.113.0/24", 24, 0),
    ("2001:db8:1000::/36", 48, 64498),
]

EXAMPLE_ROUTES = [
    ("192.0.2.0/24", [("AS_SEQUENCE", [64500, 64496])], VALID),
    ("192.0.2.0/25", [("AS_SEQUENCE", [64500, 64496])], INVALID),
    ("192.0.2.0/24", [("AS_SEQUENCE", [64500, 64511])], INVALID),
    ("198.51.100.128/25", [("AS_SEQUENCE", [64497])], VALID),
    ("203.0.113.0/24", [("AS_SEQUENCE", [64501])], INVALID),
    ("2001:db8:1000::/48", [("AS_SEQUENCE", [64500, 64498])], VALID),
    ("2001:db8:1000::/48", [("AS_SEQUENCE", [64500]), ("AS_SET", [64498, 64499])], INVALID),
    ("2001:db8::/32", [("AS_SEQUENCE", [64499])], NOT_FOUND),
]

OWN_AS = 64510


def test_example() -> None:
    trie = VrpTrie(EXAMPLE_VRPS)
    for prefix, path, want in EXAMPLE_ROUTES:
        origin = origin_asn(path, OWN_AS)
        assert trie.validate(prefix, origin) == want, prefix
        assert validate_linear(EXAMPLE_VRPS, prefix, origin) == want


def test_origin_asn() -> None:
    assert origin_asn([], OWN_AS) == OWN_AS
    assert origin_asn([("AS_SEQUENCE", [64496, 64497])], OWN_AS) == 64497
    assert origin_asn([("AS_SEQUENCE", [64496]), ("AS_SET", [64497])], OWN_AS) is NONE
    assert origin_asn([("AS_CONFED_SEQUENCE", [64505])], OWN_AS) == OWN_AS
    assert origin_asn([("AS_CONFED_SET", [64505])], OWN_AS) == OWN_AS


def test_edges() -> None:
    empty = VrpTrie()
    assert empty.validate("192.0.2.0/24", 64496) == NOT_FOUND
    # NONE never matches, even a VRP that would cover and fit.
    assert VrpTrie(EXAMPLE_VRPS).validate("192.0.2.0/24", NONE) == INVALID
    # A VRP for ASN 0 never matches, even a route with origin 0.
    assert VrpTrie([("203.0.113.0/24", 24, 0)]).validate("203.0.113.0/24", 0) == INVALID
    # One matching VRP is enough, even when others cover with other ASNs.
    both = VrpTrie([("192.0.2.0/24", 24, 64511), ("192.0.2.0/23", 24, 64496)])
    assert both.validate("192.0.2.0/24", 64496) == VALID
    # Host routes, and families kept apart.
    assert VrpTrie([("192.0.2.0/24", 32, 64496)]).validate("192.0.2.1/32", 64496) == VALID
    t = VrpTrie([("192.0.2.0/24", 24, 64496)])
    assert t.validate("192.0.2.1/32", 64496) == INVALID
    assert t.validate("2001:db8::/32", 64496) == NOT_FOUND
    # A more specific VRP does not cover a less specific route.
    assert VrpTrie([("192.0.2.128/25", 25, 64496)]).validate("192.0.2.0/24", 64511) == NOT_FOUND


BASES = [ip_network("192.0.2.0/24"), ip_network("198.51.100.0/24"), ip_network("2001:db8::/32")]


def random_prefix(rng: random.Random, base, extra: int) -> str:
    length = base.prefixlen + rng.randrange(0, extra + 1)
    width = base.max_prefixlen
    host = rng.getrandbits(extra) << (width - base.prefixlen - extra) if extra else 0
    addr = int(base.network_address) | host
    net = ip_network((ip_address(addr), length), strict=False)
    return str(net)


def test_random_against_oracle() -> None:
    """The trie agrees with the linear scan of the definitions on random VRP sets and routes."""
    rng = random.Random(6811)
    asns = list(range(64496, 64500)) + [0]
    counts = {VALID: 0, INVALID: 0, NOT_FOUND: 0}
    for _ in range(300):
        extra = rng.randrange(0, 5)
        vrps = []
        for _ in range(rng.randrange(0, 8)):
            base = rng.choice(BASES)
            p = random_prefix(rng, base, extra)
            plen = ip_network(p).prefixlen
            max_length = rng.randrange(plen, min(plen + 4, ip_network(p).max_prefixlen) + 1)
            vrps.append((p, max_length, rng.choice(asns)))
        trie = VrpTrie(vrps)
        for _ in range(5):
            route = random_prefix(rng, rng.choice(BASES), extra + 1)
            origin = rng.choice(asns + [NONE])
            got = trie.validate(route, origin)
            assert got == validate_linear(vrps, route, origin)
            counts[got] += 1
    assert min(counts.values()) > 50
