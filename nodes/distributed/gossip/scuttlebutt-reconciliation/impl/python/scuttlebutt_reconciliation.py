# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scuttlebutt-reconciliation/. The authors are listed in prov/75N9PB.jsonl.

"""Scuttlebutt reconciliation (van Renesse, Dumitriu, Gough and Thomas, LADIS 2008).

Every participant p keeps a table mu_p(r)(k) = (value, version) for every
participant r and key k. Only r writes mu(r), and each write gets a version
larger than every version r has used before. A digest lists, for every r, the
largest version known for r. A gossip partner sends back the deltas
(r, k, v, n) with n larger than that maximum, at most mtu of them, and for
each r it sends a prefix of its deltas in version order. That keeps the
invariant C(p, q): for every key k of p, q has p's current mapping or p's
current version of k is larger than everything q has seen from p.

Precise reconciliation compares the full tables and is kept as a baseline.
The simulator is deterministic, seeded and runs exchanges one at a time.
"""

import random

Delta = tuple[int, str, str, int]  # (participant, key, value, version)


class Participant:
    """Message types: DIGEST(maxima) and DELTAS(list of deltas)."""

    def __init__(self, ident: int, n: int) -> None:
        self.id = ident
        self.state: list[dict[str, tuple[str, int]]] = [{} for _ in range(n)]
        self.maxv = [0] * n

    def update(self, key: str, value: str, version: int) -> None:
        assert version > self.maxv[self.id]
        self.state[self.id][key] = (value, version)  # @line L1
        self.maxv[self.id] = version

    def digest(self) -> tuple[int, ...]:
        return tuple(self.maxv)  # @line L3

    def available(self, digest: tuple[int, ...]) -> dict[int, list[Delta]]:
        """For each participant, the deltas newer than the peer's maximum, in version order."""
        out: dict[int, list[Delta]] = {}
        for r, table in enumerate(self.state):
            if self.maxv[r] > digest[r]:
                out[r] = sorted(((r, k, v, n) for k, (v, n) in table.items() if n > digest[r]), key=lambda d: d[3])  # @line L4
        return out

    def select(self, digest: tuple[int, ...], mtu: int, ordering: str, rng: random.Random) -> list[Delta]:
        avail = self.available(digest)
        if ordering == "scuttle-depth":
            parts = sorted(avail, key=lambda r: (-len(avail[r]), rng.random()))  # @line L5
            order = [d for r in parts for d in avail[r]]
        elif ordering == "scuttle-breadth":
            rank = {r: rng.random() for r in avail}
            order = sorted((d for r in avail for d in avail[r]),
                           key=lambda d: (avail[d[0]].index(d), rank[d[0]]))
        else:
            raise ValueError(ordering)
        return order[:mtu]  # @line L6

    def apply(self, deltas: list[Delta]) -> None:
        for r, k, v, n in deltas:
            if n > self.state[r].get(k, ("", 0))[1]:  # @line L7
                self.state[r][k] = (v, n)
            if n > self.maxv[r]:  # @line L8
                self.maxv[r] = n


def exchange(p: Participant, q: Participant, mtu: int, ordering: str, rng: random.Random) -> tuple[int, int]:
    """Push-pull: p sends its digest, q answers with its digest and deltas for p,
    p answers with deltas for q. Return the sizes of the two delta sets."""
    if ordering.startswith("precise"):
        return precise_exchange(p, q, mtu, ordering == "precise-newest")
    to_p = q.select(p.digest(), mtu, ordering, rng)
    to_q = p.select(q.digest(), mtu, ordering, rng)
    p.apply(to_p)
    q.apply(to_q)
    return len(to_p), len(to_q)


def precise_exchange(p: Participant, q: Participant, mtu: int, newest: bool) -> tuple[int, int]:
    def newer(a: Participant, b: Participant) -> list[Delta]:
        out = [(r, k, v, n) for r, table in enumerate(a.state) for k, (v, n) in table.items()
               if n > b.state[r].get(k, ("", 0))[1]]
        out.sort(key=lambda d: d[3], reverse=newest)
        return out[:mtu]

    to_p, to_q = newer(q, p), newer(p, q)
    for target, deltas in ((p, to_p), (q, to_q)):
        for r, k, v, n in deltas:
            if n > target.state[r].get(k, ("", 0))[1]:
                target.state[r][k] = (v, n)
    return len(to_p), len(to_q)


def invariant_holds(p: Participant, q: Participant) -> bool:
    """C(p, q): every key of p is current at q, or newer than all q has seen from p."""
    for k, (v, n) in p.state[p.id].items():
        if q.state[p.id].get(k) != (v, n) and not n > q.maxv[p.id]:
            return False
    return True


def stale_mappings(parts: list[Participant]) -> int:
    """The number of (p, r, k) where p's copy of r's key k is not r's current mapping."""
    return sum(p.state[r.id].get(k) != m for p in parts for r in parts for k, m in r.state[r.id].items())


def simulate(n: int, keys: int, rng: random.Random, mtu: int, ordering: str, updates_per_round: int,
             update_rounds: int, total_rounds: int) -> tuple[list[int], int]:
    """Each round, random participants write random keys, then every participant
    gossips with one random peer. Return (stale mappings after each round,
    the largest delta set sent)."""
    parts = [Participant(i, n) for i in range(n)]
    version, biggest, stale = 0, 0, []
    for rnd in range(total_rounds):
        if rnd < update_rounds:
            for _ in range(updates_per_round):
                version += 1
                w = parts[rng.randrange(n)]
                w.update(f"k{rng.randrange(keys)}", f"v{version}", version)
        for p in parts:
            u = rng.randrange(n - 1)  # @line L2
            q = parts[u + 1 if u >= p.id else u]
            a, b = exchange(p, q, mtu, ordering, rng)
            biggest = max(biggest, a, b)
        stale.append(stale_mappings(parts))
    return stale, biggest


# Flow control (Section 4).

def share_rates(rho_p: float, rho_q: float, tau_p: float, tau_q: float) -> tuple[float, float]:
    """Split the joint maximum rate tau_p + tau_q between two gossip partners
    according to their desired rates rho. The sum is conserved."""
    total = tau_p + tau_q
    if rho_p + rho_q <= total:
        spare = (total - rho_p - rho_q) / 2
        return rho_p + spare, rho_q + spare
    avg = total / 2
    if rho_p >= avg and rho_q >= avg:
        return avg, avg
    if rho_p < avg:
        return rho_p, total - rho_p
    return total - rho_q, rho_q


class Aimd:
    """Additive increase, multiplicative decrease of the local maximum rate."""

    def __init__(self, tau: float, mtu: int, phi1: int = 3, phi2: int = 3, alpha: float = 0.75,
                 beta: float = 0.2) -> None:
        self.tau, self.mtu = tau, mtu
        self.phi1, self.phi2, self.alpha, self.beta = phi1, phi2, alpha, beta
        self.over = self.under = 0

    def observe(self, sizes: tuple[int, int]) -> float:
        """Record the two delta set sizes (before truncation) of one exchange."""
        if max(sizes) > self.mtu:
            self.over, self.under = self.over + 1, 0
            if self.over >= self.phi1:
                self.tau, self.over = self.alpha * self.tau, 0
        elif max(sizes) < self.mtu:
            self.under, self.over = self.under + 1, 0
            if self.under >= self.phi2:
                self.tau, self.under = min(self.tau + self.beta, self.mtu), 0
        else:  # exactly full: neither rule of Section 4.2 applies, both streaks end
            self.over = self.under = 0
        return self.tau
