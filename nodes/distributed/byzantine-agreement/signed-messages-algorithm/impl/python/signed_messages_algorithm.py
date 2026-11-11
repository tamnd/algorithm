# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/signed-messages-algorithm/. The authors are listed in prov/XR29FE.jsonl.

"""The signed messages algorithm SM(m) of Lamport, Shostak and Pease (1982).

Synchronous model, n generals 0 .. n - 1 on a complete graph, general 0 is the
commander. Signatures are modelled as unforgeable tokens: the signature of
general j on the content x exists only if j's code (or the adversary, when j is
a traitor) called sign(j, x). This is assumption A4 without real cryptography.

A message is (v, chain): the value v and the signers in order, commander
first. Signer k signs (v, chain[:k]), so each signature covers the ones before
it. A message with k lieutenant signatures arrives in round k + 1, so SM(m)
ends after round m + 1. The adversary is rushing and controls all traitors
together: in round r it sees the messages that loyal generals send to traitors
in round r before it picks the messages of the traitors.
"""

import random
from typing import Callable, Hashable, Optional

RETREAT = 0
VALUES = (0, 1, 2)
Chain = tuple[int, ...]
Msg = tuple[Hashable, Chain]


class Signatures:
    """The set of signatures made so far, as (signer, content) tokens."""

    def __init__(self) -> None:
        self.issued: set[tuple[int, tuple]] = set()

    def sign(self, signer: int, content: tuple) -> None:
        self.issued.add((signer, content))

    def valid(self, v: Hashable, chain: Chain) -> bool:
        return all((chain[k], (v, chain[:k])) in self.issued for k in range(len(chain)))


def choice(vs: set[Hashable]) -> Hashable:
    """LSP's choice: the single order of a one-element set, else RETREAT."""
    return next(iter(vs)) if len(vs) == 1 else RETREAT


class SignedGeneral:
    def __init__(self, pid: int, n: int, m: int, sigs: Signatures, value: Hashable = None) -> None:
        self.pid, self.n, self.m, self.sigs, self.value = pid, n, m, sigs, value
        self.V: set[Hashable] = set()
        self.relay: list[Msg] = []
        self.rejected = 0

    def send(self, r: int) -> list[tuple[int, Hashable, Chain]]:
        out = []
        if self.pid == 0:
            if r == 1:
                self.sigs.sign(0, (self.value, ()))  # @line L1
                out = [(q, self.value, (0,)) for q in range(1, self.n)]
            return out
        for v, chain in self.relay:  # @line L3
            self.sigs.sign(self.pid, (v, chain))  # @line L9
            new = chain + (self.pid,)
            out += [(q, v, new) for q in range(1, self.n) if q not in new]  # @line L10
        self.relay = []
        return out

    def receive(self, r: int, v: Hashable, chain: Chain) -> None:
        if self.pid == 0:
            return
        if len(chain) != r or chain[0] != 0 or len(set(chain)) != r or self.pid in chain:  # @line L5
            return
        if not self.sigs.valid(v, chain):  # @line L6
            self.rejected += 1
            return
        if v in self.V:
            return
        self.V.add(v)  # @line L7
        if r - 1 < self.m:  # @line L8
            self.relay.append((v, chain))

    def decide(self) -> Hashable:
        return choice(self.V)  # @line L11


class Adversary:
    """All traitors together. known holds every valid message a traitor has seen."""

    def __init__(self, n: int, traitors: frozenset[int], sigs: Signatures, rng: random.Random) -> None:
        self.n, self.traitors, self.sigs, self.rng = n, traitors, sigs, rng
        self.known: list[Msg] = []
        self.loyal = [q for q in range(1, n) if q not in traitors]

    def sign_as(self, j: int, content: tuple) -> None:
        if j not in self.traitors:
            raise PermissionError("the adversary has no key of a loyal general")
        self.sigs.sign(j, content)

    def extend(self, v: Hashable, chain: Chain, length: int) -> Optional[Chain]:
        """Add traitor signatures to reach the given length, or None if too few traitors."""
        free = [j for j in sorted(self.traitors) if j not in chain and j != 0]
        self.rng.shuffle(free)
        while len(chain) < length:
            if not free:
                return None
            j = free.pop()
            self.sign_as(j, (v, chain))
            chain = chain + (j,)
        return chain

    def commander_sign(self, v: Hashable) -> Msg:
        self.sign_as(0, (v, ()))
        return v, (0,)

    def sender_of(self, chain: Chain) -> int:
        return chain[-1] if chain[-1] in self.traitors else min(self.traitors)


Strategy = Callable[[Adversary, int], list[tuple[int, int, Hashable, Chain]]]


def silent(adv: Adversary, r: int) -> list:
    return []


def equivocate(adv: Adversary, r: int) -> list:
    """A traitorous commander sends a different value to each loyal lieutenant;
    traitor lieutenants relay each known message to every other lieutenant."""
    out = []
    if r == 1 and 0 in adv.traitors:
        for q in adv.loyal:
            v, ch = adv.commander_sign(VALUES[q % len(VALUES)])
            out.append((0, q, v, ch))
        return out
    for v, ch in list(adv.known):
        if len(ch) == r - 1:
            new = adv.extend(v, ch, r)
            if new:
                out += [(new[-1], q, v, new) for q in adv.loyal if q not in new]
    return out


def late(adv: Adversary, r: int) -> list:
    """The attack of the proof: the commander sends 1 to all, and passes a second
    signed value along a chain of all traitors, shown to one loyal general last."""
    if 0 not in adv.traitors:
        return []
    out = []
    k = len(adv.traitors)
    if r == 1:
        out = [(0, q, *adv.commander_sign(1)) for q in adv.loyal]
        adv.secret = adv.commander_sign(2)
    if r == k and adv.loyal:
        v, ch = adv.secret
        new = adv.extend(v, ch, k)
        out.append((new[-1], adv.loyal[0], v, new))
    return out


def rand(adv: Adversary, r: int) -> list:
    """Random subsets of extended known messages; a traitor commander signs random values."""
    out = []
    if r == 1 and 0 in adv.traitors:
        for v in VALUES:
            if adv.rng.random() < 0.6:
                msg = adv.commander_sign(v)
                adv.known.append(msg)
    for v, ch in list(adv.known):
        if len(ch) <= r and adv.rng.random() < 0.7:
            new = adv.extend(v, ch, r) if len(ch) < r else ch
            if new is None:
                continue
            for q in adv.loyal:
                if q not in new and adv.rng.random() < 0.5:
                    out.append((adv.sender_of(new), q, v, new))
    return out


def forge(adv: Adversary, r: int) -> list:
    """Random, plus messages that claim signatures of loyal generals; these must fail."""
    out = rand(adv, r)
    for q in adv.loyal:
        fake: Chain = tuple([0] + [p for p in adv.loyal if p != q][: r - 1])
        if len(fake) == r:
            out.append((min(adv.traitors), q, VALUES[-1], fake))
    return out


STRATEGIES: dict[str, Strategy] = {
    "silent": silent,
    "equivocate": equivocate,
    "late": late,
    "random": rand,
    "forge": forge,
}


def sm(
    n: int,
    m: int,
    value: Hashable,
    traitors: frozenset[int] = frozenset(),
    strategy: Strategy = silent,
    seed: int = 0,
    rounds: Optional[int] = None,
) -> dict:
    """Run SM(m). Traitors follow the strategy; with no traitors every general is loyal."""
    sigs = Signatures()
    rng = random.Random(seed)
    gens = {p: SignedGeneral(p, n, m, sigs, value if p == 0 else None) for p in range(n) if p not in traitors}
    adv = Adversary(n, traitors, sigs, rng) if traitors else None
    total = m + 1 if rounds is None else rounds
    loyal_msgs = loyal_sigs = traitor_msgs = 0
    for r in range(1, total + 1):  # @line L2
        batch = []
        for p in sorted(gens):
            for q, v, ch in gens[p].send(r):
                loyal_msgs += 1
                loyal_sigs += len(ch)
                if q in gens:
                    batch.append((q, v, ch))
                elif adv is not None and sigs.valid(v, ch):
                    adv.known.append((v, ch))  # rushing: seen before the traitors move
        if adv is not None:
            for _, q, v, ch in strategy(adv, r):
                traitor_msgs += 1
                if q in gens:
                    batch.append((q, v, ch))
        for q, v, ch in batch:
            gens[q].receive(r, v, ch)  # @line L4
    decisions = {p: g.decide() for p, g in gens.items() if p != 0}
    return {
        "decisions": decisions,
        "rounds": total,
        "loyal_messages": loyal_msgs,
        "loyal_signatures": loyal_sigs,
        "traitor_messages": traitor_msgs,
        "rejected": sum(g.rejected for g in gens.values()),
        "sets": {p: frozenset(g.V) for p, g in gens.items() if p != 0},
    }


def agreement_and_validity(res: dict, value: Hashable, commander_loyal: bool) -> bool:
    d = set(res["decisions"].values())
    if len(d) > 1:
        return False
    return not commander_loyal or d <= {value}
