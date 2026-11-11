# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/byzantine-broadcast/. The authors are listed in prov/NQ3YET.jsonl.

"""Byzantine broadcast, interactive consistency and consensus, and the
reductions between them, in the synchronous model with signatures.

The base protocol is Dolev-Strong (see the page dolev-strong-algorithm), run
as n parallel instances, one per sender, which gives interactive consistency.
Signatures are unforgeable tokens: (signer, content) pairs in a set, where only
the code of a process, or the adversary for a faulty process, adds pairs.
A signature on an instance covers the sender s of the instance, so a chain
cannot move from one instance to another.
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

    def valid(self, s: int, v: Hashable, chain: Chain) -> bool:
        return bool(chain) and chain[0] == s and all(
            (chain[k], (s, v, chain[:k])) in self.issued for k in range(len(chain))
        )


class Process:
    """A correct process that runs one Dolev-Strong instance per sender."""

    def __init__(self, pid: int, n: int, t: int, sigs: Signatures, value: Hashable) -> None:
        self.pid, self.n, self.t, self.sigs = pid, n, t, sigs
        self.extr: dict[int, list[Hashable]] = {s: [] for s in range(n)}
        self.extr[pid] = [value]
        sigs.sign(pid, (pid, value, ()))
        self.pending: list[tuple[int, Hashable, Chain]] = [(pid, value, ())]

    def send(self) -> list[tuple[int, int, Hashable, Chain]]:
        out = []
        for s, v, chain in self.pending:
            if chain:
                self.sigs.sign(self.pid, (s, v, chain))
            new = chain + (self.pid,)
            out += [(q, s, v, new) for q in range(self.n) if q not in new]
        self.pending = []
        return out

    def receive(self, r: int, s: int, v: Hashable, chain: Chain) -> None:
        if len(chain) != r or len(set(chain)) != r or not self.sigs.valid(s, v, chain):
            return
        if v in self.extr[s]:
            return
        self.extr[s].append(v)
        if r <= self.t and len(self.extr[s]) <= 2:
            self.pending.append((s, v, chain))

    def vector(self) -> list[Hashable]:
        return [e[0] if len(e) == 1 else DEFAULT for e in (self.extr[s] for s in range(self.n))]


class Adversary:
    def __init__(self, n: int, faulty: frozenset[int], sigs: Signatures, rng: random.Random, inputs: dict) -> None:
        self.n, self.faulty, self.sigs, self.rng, self.inputs = n, faulty, sigs, rng, inputs
        self.correct = [q for q in range(n) if q not in faulty]
        self.known: list[tuple[int, Hashable, Chain]] = []

    def sign_as(self, j: int, s: int, v: Hashable, chain: Chain) -> Chain:
        assert j in self.faulty, "no key of a correct process"
        self.sigs.sign(j, (s, v, chain))
        return chain + (j,)

    def extend(self, s: int, v: Hashable, chain: Chain, length: int) -> Optional[Chain]:
        free = [j for j in sorted(self.faulty) if j not in chain]
        self.rng.shuffle(free)
        while len(chain) < length:
            if not free:
                return None
            chain = self.sign_as(free.pop(), s, v, chain)
        return chain


Strategy = Callable[[Adversary, int], list[tuple[int, int, Hashable, Chain]]]


def honest_inputs(adv: Adversary, r: int) -> list:
    """Faulty senders broadcast their own input to all and then stay silent."""
    if r != 1:
        return []
    return [(q, s, adv.inputs[s], adv.sign_as(s, s, adv.inputs[s], ())) for s in adv.faulty for q in adv.correct]


def equivocate(adv: Adversary, r: int) -> list:
    """Each faulty sender signs a different value for each correct process;
    faulty relays pass every chain they know on to all correct processes."""
    out = []
    if r == 1:
        for s in adv.faulty:
            for q in adv.correct:
                v = VALUES[(q + s) % len(VALUES)]
                out.append((q, s, v, adv.sign_as(s, s, v, ())))
                adv.known.append((s, v, (s,)))
        return out
    for s, v, ch in list(adv.known):
        if len(ch) == r - 1:
            new = adv.extend(s, v, ch, r)
            if new:
                out += [(q, s, v, new) for q in adv.correct if q not in new]
    return out


def rand(adv: Adversary, r: int) -> list:
    out = []
    if r == 1:
        for s in adv.faulty:
            for v in VALUES:
                if adv.rng.random() < 0.5:
                    adv.sign_as(s, s, v, ())
                    adv.known.append((s, v, (s,)))
    for s, v, ch in list(adv.known):
        if len(ch) <= r and adv.rng.random() < 0.7:
            new = adv.extend(s, v, ch, r) if len(ch) < r else ch
            if new:
                out += [(q, s, v, new) for q in adv.correct if q not in new and adv.rng.random() < 0.5]
    return out


STRATEGIES: dict[str, Strategy] = {"honest-inputs": honest_inputs, "equivocate": equivocate, "random": rand}


def interactive_consistency(
    n: int, t: int, inputs: dict[int, Hashable], faulty: frozenset[int] = frozenset(),
    strategy: Strategy = honest_inputs, seed: int = 0,
) -> dict:
    """n parallel Dolev-Strong broadcasts in t + 1 rounds. Returns the vector of each correct process."""
    sigs = Signatures()
    procs = {p: Process(p, n, t, sigs, inputs[p]) for p in range(n) if p not in faulty}
    adv = Adversary(n, faulty, sigs, random.Random(seed), inputs) if faulty else None
    messages = 0
    for r in range(1, t + 2):
        batch = []
        for p in sorted(procs):
            for q, s, v, ch in procs[p].send():
                messages += 1
                if q in procs:
                    batch.append((q, s, v, ch))
                elif adv is not None:
                    adv.known.append((s, v, ch))
        if adv is not None:
            batch += [m for m in strategy(adv, r) if m[0] in procs]
        for q, s, v, ch in batch:
            procs[q].receive(r, s, v, ch)
    return {"vectors": {p: pr.vector() for p, pr in procs.items()}, "rounds": t + 1, "messages": messages}


def ic_ok(res: dict, inputs: dict, faulty: frozenset[int]) -> bool:
    """IC agreement (equal vectors) and IC validity (correct entries are the inputs)."""
    vecs = list(res["vectors"].values())
    if any(v != vecs[0] for v in vecs):
        return False
    return all(vec[p] == inputs[p] for vec in vecs for p in res["vectors"])


def broadcast_from_ic(n: int, t: int, sender: int, value: Hashable, faulty=frozenset(), strategy=honest_inputs, seed=0):
    """Broadcast from IC: every process takes the sender's entry of its vector."""
    inputs = {p: (value if p == sender else DEFAULT) for p in range(n)}
    res = interactive_consistency(n, t, inputs, faulty, strategy, seed)
    return {p: vec[sender] for p, vec in res["vectors"].items()}


def majority(vec: list[Hashable]) -> Hashable:
    for v in set(vec):
        if 2 * vec.count(v) > len(vec):
            return v
    return DEFAULT


def consensus_from_ic(n: int, t: int, inputs: dict, faulty=frozenset(), strategy=honest_inputs, seed=0):
    """Consensus from IC: decide the strict majority of the vector, else DEFAULT."""
    res = interactive_consistency(n, t, inputs, faulty, strategy, seed)
    return {p: majority(vec) for p, vec in res["vectors"].items()}


def weak_consensus(n: int, t: int, inputs: dict, faulty=frozenset(), strategy=honest_inputs, seed=0):
    """Consensus with weak validity for any t < n: decide the broadcast of process 0."""
    res = interactive_consistency(n, t, inputs, faulty, strategy, seed)
    return {p: vec[0] for p, vec in res["vectors"].items()}


def broadcast_from_consensus(
    n: int, t: int, value: Hashable, faulty=frozenset(), sent: Optional[dict] = None, strategy=honest_inputs, seed=0
):
    """Broadcast from consensus: in one extra round the sender 0 sends its value
    (a faulty sender sends sent[q] to q); then all run consensus on what they got."""
    got = {q: value for q in range(n)}
    if 0 in faulty and sent is not None:
        got.update(sent)
    return consensus_from_ic(n, t, got, faulty, strategy, seed)


def agreement(dec: dict) -> bool:
    return len(set(dec.values())) <= 1


def strong_validity(dec: dict, inputs: dict, faulty: frozenset[int]) -> bool:
    """If all correct processes have the same input v, every correct decision is v."""
    correct = {inputs[p] for p in inputs if p not in faulty}
    return len(correct) != 1 or set(dec.values()) <= correct


def weak_validity(dec: dict, inputs: dict, faulty: frozenset[int]) -> bool:
    """If no process is faulty and all inputs are v, every decision is v."""
    return bool(faulty) or len(set(inputs.values())) != 1 or set(dec.values()) <= set(inputs.values())
