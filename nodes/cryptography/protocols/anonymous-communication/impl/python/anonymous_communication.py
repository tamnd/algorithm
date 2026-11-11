# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/anonymous-communication/. The authors are listed in prov/5V20J4.jsonl.
"""A toy onion routing network, and a timing correlation attack on it.

* Each relay has a long-term X25519 key. A client builds a circuit through
  three relays (guard, middle, exit) one hop at a time. It sends CREATE to
  the guard, then asks the last relay of the circuit so far to EXTEND it by
  one hop. For each hop the client sends a fresh ephemeral public key, and
  both ends derive the hop keys from the X25519 shared secret with HKDF.
  This one-way handshake is a simplification of the ntor handshake of Tor:
  the relay sends no ephemeral key, so a later theft of the relay key
  exposes old circuits.
* Each cell on a circuit is wrapped in one AEAD layer per hop. A relay
  removes its layer and learns only the next step: forward the rest, extend
  the circuit, or deliver data to a destination. On the way back, each relay
  adds a layer and the client removes them all. Here a layer adds a tag, so
  a cell becomes shorter at each hop; Tor uses cells of a fixed size.
* A Network delivers cells with random link delays in an event simulation.
  Each directed link is first in, first out. The network keeps a log of the
  time, the ends and the bytes of each cell, from which an adversary takes
  only the part it can see.
* A relay can hold each cell for a random time before it sends it on
  (hold_mean > 0), which is what a mix does. With hold_mean = 0 the network
  is low latency, like Tor.

The AEAD is a study construction (encrypt-then-MAC with an HMAC-SHA256 key
stream) and X25519 is a local copy of RFC 7748. For study only: the code is
not constant time and has no link encryption, no padding and no defense
against the attacks in the tests. Use Tor (or Arti, its Rust version) for
real anonymity.
"""

import hashlib
import heapq
import hmac
import random
import secrets
from typing import Dict, List, NamedTuple, Optional, Set, Tuple

# ---------------------------------------------------------------- X25519 (RFC 7748 Section 5)

PRIME = 2**255 - 19
BASE_U = (9).to_bytes(32, "little")


def x25519(k: bytes, u: bytes) -> bytes:
    b = bytearray(k)
    b[0] &= 248
    b[31] &= 127
    b[31] |= 64
    kk = int.from_bytes(b, "little")
    x1 = int.from_bytes(u, "little") % (2**255) % PRIME
    x2, z2, x3, z3, swap = 1, 0, x1, 1, 0
    for t in range(254, -1, -1):
        kt = (kk >> t) & 1
        swap ^= kt
        if swap:
            x2, x3, z2, z3 = x3, x2, z3, z2
        swap = kt
        a, b_ = (x2 + z2) % PRIME, (x2 - z2) % PRIME
        aa, bb = a * a % PRIME, b_ * b_ % PRIME
        e = (aa - bb) % PRIME
        c, d = (x3 + z3) % PRIME, (x3 - z3) % PRIME
        da, cb = d * a % PRIME, c * b_ % PRIME
        x3 = (da + cb) ** 2 % PRIME
        z3 = x1 * (da - cb) ** 2 % PRIME
        x2 = aa * bb % PRIME
        z2 = e * (aa + 121665 * e) % PRIME
    if swap:
        x2, z2 = x3, z3
    return (x2 * pow(z2, PRIME - 2, PRIME) % PRIME).to_bytes(32, "little")


# ---------------------------------------------------------------- HKDF and the study AEAD


def _prf(key: bytes, data: bytes) -> bytes:
    return hmac.new(key, data, hashlib.sha256).digest()


def hkdf(ikm: bytes, info: bytes, length: int) -> bytes:
    prk = _prf(bytes(32), ikm)
    out, block, i = b"", b"", 1
    while len(out) < length:
        block = _prf(prk, block + info + bytes([i]))
        out, i = out + block, i + 1
    return out[:length]


def hop_keys(shared: bytes, eph_pub: bytes, relay_pub: bytes) -> Tuple[bytes, bytes]:
    """A forward key and a backward key for one hop."""
    okm = hkdf(shared, b"toy onion hop" + eph_pub + relay_pub, 64)
    return okm[:32], okm[32:]


class AuthError(ValueError):
    pass


TAG = 16


def _stream(key: bytes, nonce: bytes, n: int) -> bytes:
    return b"".join(_prf(key, nonce + i.to_bytes(4, "big")) for i in range(n // 32 + 1))[:n]


def seal(key: bytes, counter: int, pt: bytes) -> bytes:
    nonce = counter.to_bytes(8, "big")
    ke, km = _prf(key, b"enc"), _prf(key, b"mac")
    ct = bytes(a ^ b for a, b in zip(pt, _stream(ke, nonce, len(pt))))
    return ct + _prf(km, nonce + ct)[:TAG]


def open_layer(key: bytes, counter: int, ct: bytes) -> bytes:
    nonce = counter.to_bytes(8, "big")
    ke, km = _prf(key, b"enc"), _prf(key, b"mac")
    body, tag = ct[:-TAG], ct[-TAG:]
    if not hmac.compare_digest(tag, _prf(km, nonce + body)[:TAG]):
        raise AuthError("bad tag")
    return bytes(a ^ b for a, b in zip(body, _stream(ke, nonce, len(body))))


# ---------------------------------------------------------------- cells

CREATE, RELAY, STREAM = "create", "relay", "stream"
EXTEND, DATA = 1, 2


class Cell(NamedTuple):
    circ_id: int  # chosen per link, so it differs at each hop
    kind: str
    payload: bytes


def put_name(name: str) -> bytes:
    raw = name.encode()
    return bytes([len(raw)]) + raw


def get_name(b: bytes) -> Tuple[str, bytes]:
    return b[1 : 1 + b[0]].decode(), b[1 + b[0] :]


# ---------------------------------------------------------------- the network


class LinkEvent(NamedTuple):
    depart: float
    arrive: float
    src: str
    dst: str
    payload: bytes


class Network:
    def __init__(self, rng: random.Random, latency: Tuple[float, float] = (0.005, 0.03)) -> None:
        self.rng, self.latency = rng, latency
        self.nodes: Dict[str, object] = {}
        self.queue: List[tuple] = []
        self.seq = 0
        self.last: Dict[Tuple[str, str], float] = {}
        self.log: List[LinkEvent] = []

    def add(self, *nodes) -> None:
        for n in nodes:
            self.nodes[n.name] = n

    def send(self, src: str, dst: str, cell: Cell, depart: float) -> None:
        lo, hi = self.latency
        arrive = max(depart + self.rng.uniform(lo, hi), self.last.get((src, dst), 0.0) + 1e-6)
        self.last[(src, dst)] = arrive  # first in, first out on each link
        self.log.append(LinkEvent(depart, arrive, src, dst, cell.payload))
        heapq.heappush(self.queue, (arrive, self.seq, src, dst, cell))
        self.seq += 1

    def run(self) -> None:
        while self.queue:
            t, _, src, dst, cell = heapq.heappop(self.queue)
            self.nodes[dst].receive(self, t, src, cell)


# ---------------------------------------------------------------- relays


class Hop:
    """The state of one circuit at one relay."""

    def __init__(self, prev: str, prev_id: int, kf: bytes, kb: bytes) -> None:
        self.prev, self.prev_id, self.kf, self.kb = prev, prev_id, kf, kb
        self.next: Optional[str] = None
        self.next_id = 0
        self.nf = self.nb = 0
        self.seen: Set[str] = {prev}  # every node this relay exchanges a cell with on this circuit


class Relay:
    def __init__(self, name: str, hold_mean: float = 0.0) -> None:
        self.name, self.hold_mean = name, hold_mean
        self.private = secrets.token_bytes(32)
        self.public = x25519(self.private, BASE_U)
        self.by_prev: Dict[Tuple[str, int], Hop] = {}
        self.by_next: Dict[Tuple[str, int], Hop] = {}
        self.streams: Dict[str, Hop] = {}
        self.hops: List[Hop] = []

    def _send(self, net: Network, now: float, hop: Hop, dst: str, cell: Cell) -> None:
        hold = net.rng.expovariate(1 / self.hold_mean) if self.hold_mean else 0.0
        hop.seen.add(dst)
        net.send(self.name, dst, cell, now + hold)

    def receive(self, net: Network, now: float, src: str, cell: Cell) -> None:
        if cell.kind == CREATE:
            kf, kb = hop_keys(x25519(self.private, cell.payload), cell.payload, self.public)
            hop = Hop(src, cell.circ_id, kf, kb)
            self.by_prev[(src, cell.circ_id)] = hop
            self.hops.append(hop)
            return
        if cell.kind == STREAM:  # a reply from a destination
            hop = self.streams[src]
            hop.seen.add(src)
            self._send(net, now, hop, hop.prev, Cell(hop.prev_id, RELAY, seal(hop.kb, hop.nb, cell.payload)))
            hop.nb += 1
            return
        hop = self.by_prev.get((src, cell.circ_id))
        if hop is not None:  # forward direction: remove one layer
            body = open_layer(hop.kf, hop.nf, cell.payload)
            hop.nf += 1
            if hop.next is not None:
                self._send(net, now, hop, hop.next, Cell(hop.next_id, RELAY, body))
                return
            cmd, (name, rest) = body[0], get_name(body[1:])
            if cmd == EXTEND:
                hop.next, hop.next_id = name, secrets.randbits(32)
                self.by_next[(name, hop.next_id)] = hop
                self._send(net, now, hop, name, Cell(hop.next_id, CREATE, rest))
            elif cmd == DATA:  # this relay is the exit
                self.streams[name] = hop
                self._send(net, now, hop, name, Cell(0, STREAM, rest))
            return
        hop = self.by_next[(src, cell.circ_id)]  # backward direction: add one layer
        hop.seen.add(src)
        self._send(net, now, hop, hop.prev, Cell(hop.prev_id, RELAY, seal(hop.kb, hop.nb, cell.payload)))
        hop.nb += 1


# ---------------------------------------------------------------- clients and destinations


class Circuit:
    def __init__(self, path: List[str], circ_id: int) -> None:
        self.path, self.circ_id = path, circ_id
        self.keys: List[Tuple[bytes, bytes]] = []
        self.nf: List[int] = []
        self.nb: List[int] = []


class Client:
    def __init__(self, name: str) -> None:
        self.name = name
        self.circuits: Dict[int, Circuit] = {}
        self.replies: List[Tuple[float, bytes]] = []

    def _wrap(self, circ: Circuit, body: bytes) -> bytes:
        """One layer per hop built so far; the layer of the last hop is the inner one."""
        for i in reversed(range(len(circ.keys))):
            body = seal(circ.keys[i][0], circ.nf[i], body)
            circ.nf[i] += 1
        return body

    def build(self, net: Network, relays: List[Relay], t: float) -> Circuit:
        circ = Circuit([r.name for r in relays], secrets.randbits(32))
        self.circuits[circ.circ_id] = circ
        for k, relay in enumerate(relays):
            e = secrets.token_bytes(32)
            epub = x25519(e, BASE_U)
            keys = hop_keys(x25519(e, relay.public), epub, relay.public)
            if k == 0:
                cell = Cell(circ.circ_id, CREATE, epub)
            else:
                cell = Cell(circ.circ_id, RELAY, self._wrap(circ, bytes([EXTEND]) + put_name(relay.name) + epub))
            net.send(self.name, relays[0].name, cell, t)
            circ.keys.append(keys)
            circ.nf.append(0)
            circ.nb.append(0)
        return circ

    def send(self, net: Network, circ: Circuit, dest: str, data: bytes, t: float) -> None:
        body = self._wrap(circ, bytes([DATA]) + put_name(dest) + data)
        net.send(self.name, circ.path[0], Cell(circ.circ_id, RELAY, body), t)

    def receive(self, net: Network, now: float, src: str, cell: Cell) -> None:
        circ = self.circuits[cell.circ_id]
        body = cell.payload
        for i in range(len(circ.keys)):  # the guard's layer is the outer one
            body = open_layer(circ.keys[i][1], circ.nb[i], body)
            circ.nb[i] += 1
        self.replies.append((now, body))


class Destination:
    def __init__(self, name: str, echo: bool = False) -> None:
        self.name, self.echo = name, echo
        self.received: List[Tuple[float, str, bytes]] = []

    def receive(self, net: Network, now: float, src: str, cell: Cell) -> None:
        self.received.append((now, src, cell.payload))
        if self.echo:
            net.send(self.name, src, Cell(0, STREAM, b"re: " + cell.payload), now)


# ---------------------------------------------------------------- the timing correlation attack


def correlate(entry: Dict[str, List[float]], exits: Dict[str, List[float]], window: float, rng: random.Random) -> Dict[str, str]:
    """For each destination, guess the client whose cells entered the network
    shortly before the cells that reached it. The attacker sees only the times
    on the client to guard links and on the exit to destination links."""
    guess = {}
    for site, xs in exits.items():

        def score(c: str) -> Tuple[int, float]:
            hits = sum(any(0 < x - e <= window for e in entry[c]) for x in xs)
            return hits, rng.random()  # break ties at random

        guess[site] = max(entry, key=score)
    return guess


def timing_experiment(n_clients: int = 16, n_relays: int = 8, msgs: int = 10, rate: float = 3.0, hold_mean: float = 0.0, window: float = 0.15, seed: int = 1) -> float:
    """Each client sends msgs cells, at Poisson times with the given rate, over
    its own three-hop circuit to its own destination. Returns the fraction of
    destinations whose client the attack finds."""
    rng = random.Random(seed)
    net = Network(rng)
    relays = [Relay(f"R{i}", hold_mean) for i in range(n_relays)]
    clients = [Client(f"client{i}") for i in range(n_clients)]
    sites = [Destination(f"site{i}") for i in range(n_clients)]
    net.add(*relays, *clients, *sites)
    talks_to = dict(zip((c.name for c in clients), (sites[j].name for j in rng.sample(range(n_clients), n_clients))))
    for c in clients:
        circ = c.build(net, rng.sample(relays, 3), 0.0)
        t = 1.0
        for k in range(msgs):
            t += rng.expovariate(rate)
            c.send(net, circ, talks_to[c.name], b"cell %d" % k, t)
    net.run()
    entry = {c.name: [e.depart for e in net.log if e.src == c.name and e.depart >= 1.0] for c in clients}
    exits = {s.name: [e.arrive for e in net.log if e.dst == s.name] for s in sites}
    guess = correlate(entry, exits, window, rng)
    return sum(guess[talks_to[c.name]] == c.name for c in clients) / n_clients
