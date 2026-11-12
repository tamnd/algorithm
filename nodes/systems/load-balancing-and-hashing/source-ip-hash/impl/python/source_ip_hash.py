# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/source-ip-hash/. The authors are listed in prov/39Q693.jsonl.

"""Source IP hash in the form of the nginx ip_hash module.

The key is the first three bytes of an IPv4 address, or all sixteen bytes of
an IPv6 address. The hash is h <- (113 h + b) mod 6271 over the key bytes,
starting from 89. The server is the one whose weight range contains h mod W,
where W is the total weight. If that server is down, the loop hashes the key
again from the current h, up to 21 picks, and then gives up.
"""

import ipaddress
from collections.abc import Sequence

START = 89
MULT = 113
MOD = 6271
MAX_TRIES = 20


def key_bytes(ip: str) -> bytes:
    addr = ipaddress.ip_address(ip)
    if addr.version == 4:
        return addr.packed[:3]
    return addr.packed


def step(h: int, key: bytes) -> int:
    for b in key:
        h = (h * MULT + b) % MOD
    return h


class SourceIpHash:
    def __init__(self, servers: Sequence[str], weights: Sequence[int] | None = None) -> None:
        if not servers:
            raise ValueError("need at least one server")
        self.servers = list(servers)
        self.weights = list(weights) if weights is not None else [1] * len(self.servers)
        if len(self.weights) != len(self.servers) or min(self.weights) < 1:
            raise ValueError("weights must be positive integers, one per server")
        self.total = sum(self.weights)

    def pick(self, ip: str, down: frozenset[str] | set[str] = frozenset()) -> str | None:
        """Return the server for ip, or None when nginx would fall back to round robin."""
        a = key_bytes(ip)  # @line L1
        h, tries = START, 0  # @line L2
        while True:  # @line L3
            for b in a:  # @line L4
                h = (h * MULT + b) % MOD
            r = h % self.total  # @line L5
            i = 0  # @line L6
            while r >= self.weights[i]:  # @line L7
                r -= self.weights[i]
                i += 1
            if self.servers[i] not in down:  # @line L8
                return self.servers[i]
            tries += 1  # @line L9
            if tries > MAX_TRIES:  # @line L10
                return None


def mod_n_pick(ip: str, servers: Sequence[str]) -> str:
    """The plain form: the same hash, modulo the number of servers that are up."""
    return servers[step(START, key_bytes(ip)) % len(servers)]
