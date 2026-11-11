# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dolev-strong-algorithm/. The authors are listed in prov/EHN65V.jsonl.

"""The Dolev-Strong authenticated broadcast algorithm (1983).

Synchronous model with lock-step rounds 1 .. t + 1, processes 0 .. n - 1 on a
complete graph, process 0 is the sender, at most t processes are Byzantine and
the adversary is static and rushing. Signatures are unforgeable tokens: the
signature of j on x exists only if j's code, or the adversary when j is
faulty, called sign(j, x).

A message is (v, chain), where chain lists the signers in order with the
sender first, and signer k signs (v, chain[:k]). A process accepts v in round r
only if the chain holds r distinct valid signatures and starts with the sender.
It adds v to its extracted set EXTR, and relays only the first two values it
extracts, so a correct process sends at most 2(n - 2) relay messages.
"""

import random
from typing import Callable, Hashable, Optional

DEFAULT = 0
VALUES = (0, 1, 2)
Chain = tuple[int, ...]


class Signatures:
    def __init__(self) -> None:
        self.issued: set[tuple[int, tuple]] = set()

    def sign(self, signer: int, content: tuple) -> None:
        self.issued.add((signer, content))

    def valid(self, v: Hashable, chain: Chain) -> bool:
        return all((chain[k], (v, chain[:k])) in self.issued for k in range(len(chain)))


class Process:
    def __init__(self, pid: int, n: int, t: int, sigs: Signatures, value: Hashable = None) -> None:
        self.pid, self.n, self.t, self.sigs = pid, n, t, sigs
        self.extr: list[Hashable] = []
        self.pending: list[tuple[Hashable, Chain]] = []
        if pid == 0:
            self.extr = [value]
            sigs.sign(0, (value, ()))
            self.pending = [(value, ())]  # @line L1

    def send(self, r: int) -> list[tuple[int, Hashable, Chain]]:
        out = []
        for v, chain in self.pending:
            if chain:
                self.sigs.sign(self.pid, (v, chain))  # @line L8
            new = chain + (self.pid,)
            out += [(q, v, new) for q in range(self.n) if q not in new]  # @line L9
        self.pending = []
        return out

    def receive(self, r: int, v: Hashable, chain: Chain) -> None:
        if len(chain) != r or chain[0] != 0 or len(set(chain)) != r:  # @line L4
            return
        if not self.sigs.valid(v, chain) or v in self.extr:  # @line L5
            return
        self.extr.append(v)  # @line L6
        if r <= self.t and len(self.extr) <= 2:  # @line L7
            self.pending.append((v, chain))

    def decide(self) -> Hashable:
        return self.extr[0] if len(self.extr) == 1 else DEFAULT  # @line L10


class Adversary:
    def __init__(self, n: int, faulty: frozenset[int], sigs: Signatures, rng: random.Random) -> None:
        self.n, self.faulty, self.sigs, self.rng = n, faulty, sigs, rng
        self.known: list[tuple[Hashable, Chain]] = []
        self.correct = [q for q in range(n) if q not in faulty]
        self.secret: Optional[tuple[Hashable, Chain]] = None

    def sign_as(self, j: int, content: tuple) -> None:
        if j not in self.faulty:
            raise PermissionError("the adversary has no key of a correct process")
        self.sigs.sign(j, content)

    def extend(self, v: Hashable, chain: Chain, length: int) -> Optional[Chain]:
        free = [j for j in sorted(self.faulty) if j not in chain and j != 0]
        self.rng.shuffle(free)
        while len(chain) < length:
            if not free:
                return None
            j = free.pop()
            self.sign_as(j, (v, chain))
            chain = chain + (j,)
        return chain

    def sender_sign(self, v: Hashable) -> tuple[Hashable, Chain]:
        self.sign_as(0, (v, ()))
        return v, (0,)


Strategy = Callable[[Adversary, int], list[tuple[int, Hashable, Chain]]]


def silent(adv: Adversary, r: int) -> list:
    return []


def equivocate(adv: Adversary, r: int) -> list:
    """A faulty sender signs a different value for each correct process; faulty
    relays pass every known chain on to all correct processes."""
    out = []
    if r == 1 and 0 in adv.faulty:
        return [(q, *adv.sender_sign(VALUES[q % len(VALUES)])) for q in adv.correct]
    for v, ch in list(adv.known):
        if len(ch) == r - 1:
            new = adv.extend(v, ch, r)
            if new:
                out += [(q, v, new) for q in adv.correct if q not in new]
    return out


def late(adv: Adversary, r: int) -> list:
    """The attack behind the t + 1 rounds: the sender gives 1 to all correct
    processes, and a second value travels through the t faulty processes and
    reaches one correct process in round t."""
    if 0 not in adv.faulty:
        return []
    out = []
    k = len(adv.faulty)
    if r == 1:
        out = [(q, *adv.sender_sign(1)) for q in adv.correct]
        adv.secret = adv.sender_sign(2)
    if r == k and adv.secret is not None:
        v, ch = adv.secret
        new = adv.extend(v, ch, k)
        out.append((adv.correct[0], v, new))
    return out


def rand(adv: Adversary, r: int) -> list:
    out = []
    if r == 1 and 0 in adv.faulty:
        for v in VALUES:
            if adv.rng.random() < 0.6:
                adv.known.append(adv.sender_sign(v))
    for v, ch in list(adv.known):
        if len(ch) <= r and adv.rng.random() < 0.7:
            new = adv.extend(v, ch, r) if len(ch) < r else ch
            if new is None:
                continue
            out += [(q, v, new) for q in adv.correct if q not in new and adv.rng.random() < 0.5]
    return out


def forge(adv: Adversary, r: int) -> list:
    """Random, plus chains that claim signatures of correct processes."""
    out = rand(adv, r)
    for q in adv.correct:
        fake = tuple([0] + [p for p in adv.correct if p not in (0, q)][: r - 1])
        if len(fake) == r:
            out.append((q, VALUES[-1], fake))
    return out


STRATEGIES: dict[str, Strategy] = {
    "silent": silent,
    "equivocate": equivocate,
    "late": late,
    "random": rand,
    "forge": forge,
}


def dolev_strong(
    n: int,
    t: int,
    value: Hashable,
    faulty: frozenset[int] = frozenset(),
    strategy: Strategy = silent,
    seed: int = 0,
    rounds: Optional[int] = None,
) -> dict:
    """Run the protocol for t + 1 rounds (or the given number) and return the
    decisions of the correct processes and the costs."""
    sigs = Signatures()
    procs = {p: Process(p, n, t, sigs, value if p == 0 else None) for p in range(n) if p not in faulty}
    adv = Adversary(n, faulty, sigs, random.Random(seed)) if faulty else None
    total = t + 1 if rounds is None else rounds
    msgs = sig_count = max_sigs = 0
    for r in range(1, total + 1):  # @line L2
        batch = []
        for p in sorted(procs):
            for q, v, ch in procs[p].send(r):
                msgs += 1
                sig_count += len(ch)
                max_sigs = max(max_sigs, len(ch))
                if q in procs:
                    batch.append((q, v, ch))
                elif adv is not None:
                    adv.known.append((v, ch))
        if adv is not None:
            batch += [(q, v, ch) for q, v, ch in strategy(adv, r) if q in procs]
        for q, v, ch in batch:
            procs[q].receive(r, v, ch)  # @line L3
    return {
        "decisions": {p: pr.decide() for p, pr in procs.items()},
        "extracted": {p: list(pr.extr) for p, pr in procs.items()},
        "rounds": total,
        "correct_messages": msgs,
        "correct_signatures": sig_count,
        "max_signatures": max_sigs,
    }


def agreement_and_validity(res: dict, value: Hashable, sender_correct: bool) -> bool:
    d = set(res["decisions"].values())
    return len(d) <= 1 and (not sender_correct or d <= {value})


def message_bound(n: int) -> int:
    """At most n - 1 sends by the sender and 2(n - 2) relays by each other correct process."""
    return (n - 1) + 2 * (n - 1) * (n - 2)
