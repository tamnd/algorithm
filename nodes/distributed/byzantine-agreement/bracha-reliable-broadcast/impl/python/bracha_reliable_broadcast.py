# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bracha-reliable-broadcast/. The authors are listed in prov/9Y7P6X.jsonl.

"""Bracha's reliable broadcast (1987) for n > 3t, in an asynchronous network.

A sender s broadcasts initial(m). A process echoes the first initial from s;
it sends ready(v) after echo(v) from more than (n + t)/2 senders or ready(v)
from t + 1 senders; it delivers v after ready(v) from 2t + 1 senders.

The network is a pool of messages in transit. A seeded scheduler picks the
next message to deliver, so a run is an asynchronous run with an arbitrary
(here random or adversarial) order. Each run goes on until no message is left,
which models eventual delivery. Byzantine processes inject the messages that
a seeded strategy chooses, and they can react to every message they receive.
"""

import random
from typing import Callable

Msg = tuple  # (src, dst, kind, value)
# strategy(event, faulty_process, info, rng) -> list of messages to inject.
# event is "start" (once per faulty process) or "recv" (info is the message).
Strategy = Callable[[str, int, dict, random.Random], list]


def run(n: int, t: int, sender: int, value: str, faulty: set[int], strategy: Strategy, scheduler: str = "random", seed: int = 0) -> dict:
    assert len(faulty) <= t
    rng = random.Random(seed)
    honest = [p for p in range(n) if p not in faulty]
    st = {p: {"echoed": False, "ready": None, "delivered": [], "echo": {}, "readys": {}} for p in honest}
    pending: list[Msg] = []
    stats = {"messages": 0, "steps": 0}
    log = []
    ctx = {"n": n, "t": t, "sender": sender, "honest": honest, "faulty": faulty}

    def bcast(src: int, kind: str, v: str) -> None:
        for d in range(n):
            pending.append((src, d, kind, v))
        stats["messages"] += n

    if sender not in faulty:
        bcast(sender, "initial", value)  # @line L1
    for f in sorted(faulty):
        pending.extend(strategy("start", f, ctx, rng))

    while pending:
        i = choose(pending, scheduler, faulty, honest, rng)
        src, dst, kind, v = pending.pop(i)
        stats["steps"] += 1
        if dst in faulty:
            pending.extend(strategy("recv", dst, {**ctx, "msg": (src, dst, kind, v)}, rng))
            continue
        s = st[dst]
        if kind == "initial" and src == sender and not s["echoed"]:
            s["echoed"] = True
            bcast(dst, "echo", v)  # @line L2
            log.append((dst, "echo", v))
        elif kind == "echo":
            s["echo"].setdefault(v, set()).add(src)
        elif kind == "ready":
            s["readys"].setdefault(v, set()).add(src)
        if s["ready"] is None:
            for w in sorted(set(s["echo"]) | set(s["readys"])):
                if 2 * len(s["echo"].get(w, ())) > n + t:
                    s["ready"] = w
                    bcast(dst, "ready", w)  # @line L3
                    log.append((dst, "ready", w))
                    break
                if len(s["readys"].get(w, ())) >= t + 1:
                    s["ready"] = w
                    bcast(dst, "ready", w)  # @line L4
                    log.append((dst, "ready", w))
                    break
        for w, senders in s["readys"].items():
            if len(senders) >= 2 * t + 1 and not s["delivered"]:
                s["delivered"].append(w)  # @line L5
                log.append((dst, "deliver", w))
    return {"delivered": {p: list(st[p]["delivered"]) for p in honest}, "messages": stats["messages"], "steps": stats["steps"], "log": log}


def choose(pending: list, scheduler: str, faulty: set[int], honest: list[int], rng: random.Random) -> int:
    """Pick the index of the next message to deliver."""
    if scheduler == "fifo":
        return 0
    if scheduler == "random":
        return rng.randrange(len(pending))
    # "adversarial": messages from faulty processes first, then messages to
    # processes other than the victim (the first honest process); the victim
    # gets its messages last. Ties are broken at random.
    victim = honest[0] if honest else -1
    best = min((0 if m[0] in faulty else 1, 1 if m[1] == victim else 0) for m in pending)
    idx = [k for k, m in enumerate(pending) if (0 if m[0] in faulty else 1, 1 if m[1] == victim else 0) == best]
    return rng.choice(idx)


def check(n: int, sender: int, value: str, faulty: set[int], res: dict) -> list[str]:
    """Validity, no duplication, integrity, consistency and totality."""
    bad = []
    d = res["delivered"]
    if any(len(v) > 1 for v in d.values()):
        bad.append("no duplication")
    got = {v[0] for v in d.values() if v}
    if sender not in faulty:
        if any(v != [value] for v in d.values()):
            bad.append("validity")
        if got - {value}:
            bad.append("integrity")
    if len(got) > 1:
        bad.append("consistency")
    if any(d.values()) and not all(d.values()):
        bad.append("totality")
    return bad


# ---- Byzantine strategies --------------------------------------------------

def to_all(f: int, n: int, kind: str, v: str) -> list:
    return [(f, d, kind, v) for d in range(n)]


def silent(event, f, ctx, rng):
    return []


def split(event, f, ctx, rng):
    """The attack of the consistency proof: the honest processes are cut into
    two halves A and B; every faulty process sends initial, echo and ready
    for "a" to A and for "b" to B, once at the start."""
    if event != "start":
        return []
    h = ctx["honest"]
    a_side = set(h[: (len(h) + 1) // 2])
    out = []
    for d in range(ctx["n"]):
        v = "a" if d in a_side or d in ctx["faulty"] else "b"
        if f == ctx["sender"]:
            out.append((f, d, "initial", v))
        out.append((f, d, "echo", v))
        out.append((f, d, "ready", v))
    return out


def equivocate(event, f, ctx, rng):
    """Send each kind of message with a random value to each receiver, at
    the start; as sender, also a random initial to each receiver."""
    if event != "start":
        return []
    out = []
    for d in range(ctx["n"]):
        if f == ctx["sender"]:
            out.append((f, d, "initial", rng.choice("ab")))
        out.append((f, d, "echo", rng.choice("ab")))
        out.append((f, d, "ready", rng.choice("ab")))
    return out


def follow_opposite(event, f, ctx, rng):
    """React to what it receives: when it gets echo(v) or ready(v), send the
    other value to one random receiver; as sender, start with a split."""
    if event == "start":
        if f != ctx["sender"]:
            return []
        return [(f, d, "initial", "a" if d % 2 == 0 else "b") for d in range(ctx["n"])]
    _, _, kind, v = ctx["msg"]
    if kind in ("echo", "ready") and rng.random() < 0.5:
        w = "b" if v == "a" else "a"
        return [(f, rng.randrange(ctx["n"]), kind, w)]
    return []


def starve_one(event, f, ctx, rng):
    """Try to break totality: as sender, give initial("a") only to the
    first honest process; send echo and ready for "a" to that process only."""
    if event != "start":
        return []
    p = ctx["honest"][0]
    out = [(f, p, "echo", "a"), (f, p, "ready", "a")]
    if f == ctx["sender"]:
        out.append((f, p, "initial", "a"))
    return out


STRATEGIES = {"silent": silent, "split": split, "equivocate": equivocate, "follow-opposite": follow_opposite, "starve-one": starve_one}


if __name__ == "__main__":
    res = run(4, 1, 0, "a", {0}, split, "fifo")
    print(res["delivered"], res["messages"])
    for e in res["log"]:
        print(e)
