# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sticky-sessions/. The authors are listed in prov/GNHJ0X.jsonl.

"""Sticky sessions: cookie affinity and source-IP affinity.

Model: a pool of servers that changes only when a server leaves or joins.
A request carries a session id, a client address and maybe an affinity
cookie. The cookie balancer sends a request to the server that its cookie
names while that server is in the pool; otherwise it picks a server for the
session with a fallback policy (fewest bound sessions, lowest name on a tie)
and sets a new cookie. The source-IP balancers map a hash of the address to
a server, either by `hash mod n` over the list of live servers or with a
consistent-hash ring.
"""

import bisect
import hashlib


def h64(text: str) -> int:
    """A stable 64-bit hash (the first 8 bytes of SHA-256)."""
    return int.from_bytes(hashlib.sha256(text.encode()).digest()[:8], "big")


class CookieBalancer:
    def __init__(self, servers: list[str]) -> None:
        self.pool = sorted(servers)
        self.bound: dict[str, set[str]] = {s: set() for s in self.pool}  # server -> sessions
        self.rebinds = 0  # sessions that had a cookie for a server that left

    def route(self, session: str, cookie: str | None) -> tuple[str, str | None]:
        """Return (server, cookie to set or None)."""
        if cookie is not None and cookie in self.bound:  # @line L1
            return cookie, None  # @line L2
        if cookie is not None:
            self.rebinds += 1
        s = min(self.pool, key=lambda x: (len(self.bound[x]), x))  # @line L3
        self.bound[s].add(session)  # @line L4
        return s, s  # @line L5

    def end_session(self, session: str, server: str) -> None:
        if server in self.bound:
            self.bound[server].discard(session)

    def remove(self, server: str) -> set[str]:
        """The server leaves; return the sessions that lose their server."""
        self.pool.remove(server)
        return self.bound.pop(server)

    def add(self, server: str) -> None:
        self.pool = sorted(self.pool + [server])
        self.bound[server] = set()


def mod_server(key: int, live: list[str]) -> str:
    """Source-IP hash over the list of live servers: live[h mod n]."""
    return live[key % len(live)]  # @line L8


class Ring:
    """A consistent-hash ring with `vnodes` points per server."""

    def __init__(self, servers: list[str], vnodes: int = 100) -> None:
        self.vnodes = vnodes
        self.points: list[tuple[int, str]] = []
        for s in servers:
            self.add(s)

    def add(self, server: str) -> None:
        for i in range(self.vnodes):
            bisect.insort(self.points, (h64(f"{server}#{i}"), server))

    def remove(self, server: str) -> None:
        self.points = [p for p in self.points if p[1] != server]

    def lookup(self, key: int) -> str:
        i = bisect.bisect_left(self.points, (key, ""))
        return self.points[i % len(self.points)][1]  # @line L7


def ip_key(address: str, prefix_octets: int | None = None) -> int:
    """The hash key of a client address. With prefix_octets=3 only the first
    three octets of an IPv4 address count, as in the nginx ip_hash method."""
    if prefix_octets is not None:
        address = ".".join(address.split(".")[:prefix_octets])
    return h64(address)  # @line L6


def moved_by_mod_removal(n: int, removed: int) -> int:
    """How many of the n(n-1) keys 0 .. n(n-1)-1 change server when server
    `removed` leaves a list of n servers that is indexed by key mod size."""
    live = list(range(n))
    rest = [x for x in live if x != removed]
    return sum(1 for k in range(n * (n - 1)) if live[k % n] != rest[k % (n - 1)])


def load_per_server(assign: dict[str, str], weight: dict[str, int]) -> dict[str, int]:
    """Requests per server when client c sends weight[c] requests to assign[c]."""
    out: dict[str, int] = {}
    for c, s in assign.items():
        out[s] = out.get(s, 0) + weight[c]
    return out
