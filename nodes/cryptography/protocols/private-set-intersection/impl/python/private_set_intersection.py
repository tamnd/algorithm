# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/private-set-intersection/. The authors are listed in prov/P1QYT2.jsonl.
"""Private set intersection for semi-honest parties, two ways.

1. Diffie-Hellman PSI (Meadows 1986; Huberman, Franklin and Hogg 1999).
   Items are hashed into a group of prime order q, and each party raises
   them to its secret exponent. H(x)^(ab) = H(y)^(ab) exactly when x = y
   (up to hash collisions), so the client matches the doubly blinded values.

2. OPRF PSI with cuckoo hashing, in the layout of Kolesnikov, Kumaresan,
   Rosulek and Trieu (2016): the receiver puts each item in one of 3 bins,
   the sender puts each item in all 3 of its bins, and there is one OPRF
   key per bin. The OPRF here is the Diffie-Hellman OPRF H(x)^k with
   blinding, not the OT-based OPRF of KKRT, so this is a simpler variant
   that keeps the hashing structure but not the speed.

The group is the subgroup of squares modulo a safe prime p = 2q + 1. Hashing
to the group is SHA-256 mod p, squared. These are small local copies of a
DH group and a hash to it; the 64-bit group is far too small to be secure.

For study only. The code is not constant time and uses Python's random
module. Use a maintained library (for example the PSI code in libOTe or
Microsoft's APSI) for real data.
"""

import hashlib
import random
from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass(frozen=True)
class Group:
    p: int      # safe prime p = 2q + 1
    q: int      # prime order of the subgroup of squares

    def contains(self, h: int) -> bool:
        return 0 < h < self.p and pow(h, self.q, self.p) == 1


SMALL_GROUP = Group(1019, 509)
TOY_GROUP = Group(9223372036854778487, 4611686018427389243)


def hash_to_group(x: str, group: Group, domain: bytes = b"psi") -> int:
    """H(x): SHA-256 of the item, reduced mod p and squared into the subgroup."""
    ctr = 0
    while True:
        d = hashlib.sha256(domain + ctr.to_bytes(4, "big") + x.encode()).digest()
        h = pow(int.from_bytes(d, "big") % group.p, 2, group.p)
        if h not in (0, 1):
            return h
        ctr += 1


def random_exponent(group: Group, rng: random.Random) -> int:
    return rng.randrange(1, group.q)


@dataclass
class DHRun:
    intersection: set[str]
    to_server: list[int]                 # H(x)^a, shuffled
    to_client_xs: list[int]              # H(x)^(ab), in the client's order
    to_client_ys: list[int]              # H(y)^b, shuffled
    elements_sent: int
    client_key: int                      # a, known to the client only
    server_key: int                      # b, known to the server only


def dh_psi(xs: Iterable[str], ys: Iterable[str], group: Group, rng: random.Random) -> DHRun:
    """The client holds xs and learns xs & ys; the server holds ys and learns |xs|."""
    xs, ys = list(dict.fromkeys(xs)), list(dict.fromkeys(ys))
    a = random_exponent(group, rng)                                  # client key
    b = random_exponent(group, rng)
    order = list(range(len(xs)))
    rng.shuffle(order)
    to_server = [pow(hash_to_group(xs[i], group), a, group.p) for i in order]   # client to server
    back = [pow(v, b, group.p) for v in to_server]                   # server to client, same order
    to_client_ys = [pow(hash_to_group(y, group), b, group.p) for y in ys]   # server to client
    rng.shuffle(to_client_ys)
    theirs = {pow(v, a, group.p) for v in to_client_ys}             # H(y)^(ba)
    mine = {back[pos]: xs[i] for pos, i in enumerate(order)}
    inter = {x for v, x in mine.items() if v in theirs}              # match
    return DHRun(inter, to_server, back, to_client_ys,
                 len(to_server) + len(back) + len(to_client_ys), a, b)


def naive_hash_psi_leak(ys: Iterable[str], domain: Iterable[str]) -> set[str]:
    """The broken protocol: the server sends SHA-256(y) for its items. A
    client that can list the domain hashes every candidate and learns the
    whole server set, not only the intersection."""
    sent = {hashlib.sha256(y.encode()).digest() for y in ys}
    return {z for z in domain if hashlib.sha256(z.encode()).digest() in sent}


# ---------------------------------------------------------------- cuckoo hashing


def bin_of(x: str, i: int, nbins: int, seed: int) -> int:
    d = hashlib.sha256(seed.to_bytes(8, "big") + bytes([i]) + x.encode()).digest()
    return int.from_bytes(d[:8], "big") % nbins


def cuckoo_insert(items: list[str], nbins: int, seed: int, rng: random.Random,
                  max_kicks: int = 500) -> Optional[list[Optional[tuple[str, int]]]]:
    """Cuckoo hashing with 3 hash functions and no stash. Returns the table,
    where slot b holds (item, i) with bin_of(item, i) = b, or None if an
    insertion fails."""
    table: list[Optional[tuple[str, int]]] = [None] * nbins
    for x in items:
        cur, i = x, rng.randrange(3)
        for _ in range(max_kicks):
            placed = False
            for j in range(3):
                b = bin_of(cur, j, nbins, seed)
                if table[b] is None:
                    table[b] = (cur, j)
                    placed = True
                    break
            if placed:
                break
            b = bin_of(cur, i, nbins, seed)
            evicted = table[b]
            table[b] = (cur, i)
            assert evicted is not None
            cur = evicted[0]
            i = (evicted[1] + 1 + rng.randrange(2)) % 3     # move it to another of its bins
        else:
            return None
    return table


# ---------------------------------------------------------------- OPRF PSI


@dataclass
class OPRFRun:
    intersection: set[str]
    nbins: int
    oprf_calls: int                      # blinded evaluations, one per bin
    sender_values: int                   # 3 per sender item
    seed: int


def oprf_psi(xs: Iterable[str], ys: Iterable[str], group: Group, rng: random.Random,
             expansion: float = 1.5) -> OPRFRun:
    """Receiver holds xs and learns xs & ys; sender holds ys.

    Bin b has an OPRF key k_b, and F_b(x) = H(x)^(k_b). The receiver gets
    F_b on the item in bin b (a dummy for an empty bin) by a blinded
    evaluation: it sends H(x)^r, the sender returns H(x)^(r k_b), and the
    receiver removes r. The sender sends, for each y and each i in 0..2, a
    short hash of F_b(y) with b = bin_of(y, i), tagged by i."""
    xs, ys = list(dict.fromkeys(xs)), list(dict.fromkeys(ys))
    nbins = max(4, int(expansion * len(xs)) + 1)
    while True:
        seed = rng.getrandbits(32)
        table = cuckoo_insert(xs, nbins, seed, rng)
        if table is not None:
            break
    keys = [random_exponent(group, rng) for _ in range(nbins)]

    def short(v: int, i: int) -> bytes:
        return hashlib.sha256(bytes([i]) + v.to_bytes(16, "big")).digest()[:12]

    mine: dict[bytes, str] = {}
    calls = 0
    for b, slot in enumerate(table):
        item = slot[0] if slot else "\x00dummy%d" % rng.getrandbits(64)
        r = random_exponent(group, rng)
        blinded = pow(hash_to_group(item, group), r, group.p)        # receiver to sender
        answer = pow(blinded, keys[b], group.p)                      # sender to receiver
        value = pow(answer, pow(r, -1, group.q), group.p)            # H(item)^(k_b)
        calls += 1
        if slot:
            mine[short(value, slot[1])] = slot[0]
    sent = set()
    for y in ys:
        for i in range(3):
            b = bin_of(y, i, nbins, seed)
            sent.add(short(pow(hash_to_group(y, group), keys[b], group.p), i))
    inter = {x for tag, x in mine.items() if tag in sent}
    return OPRFRun(inter, nbins, calls, 3 * len(ys), seed)
