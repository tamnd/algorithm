# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/needham-schroeder/. The authors are listed in prov/0T48C0.jsonl.
"""A bounded Dolev-Yao model checker for the Needham-Schroeder public-key
protocol (NSPK) and Lowe's fix (NSL).

NSPK (Needham and Schroeder 1978), with {m}pk(X) the encryption of m for X:
    1. A -> B : {Na, A}pk(B)
    2. B -> A : {Na, Nb}pk(A)          NSL: {Na, Nb, B}pk(A)
    3. A -> B : {Nb}pk(B)

The model:
* Agents A and B are honest. I is the intruder, a registered agent whose
  private key the intruder holds. The intruder is the network: it reads every
  message, and it sends any message that it can derive (Dolev and Yao 1983).
* Encryption is perfect: {m}pk(X) opens only with the private key of X.
* Messages are typed: an honest agent accepts only a message of the expected
  form, with a nonce where a nonce belongs and an agent name where a name
  belongs. All nonces the intruder makes are one atom Ni.
* A scenario is a finite list of sessions. The search explores every
  interleaving and every typed message that the intruder can derive.

The goals checked are agreement (when an honest agent finishes a run with an
honest partner, the partner ran the protocol with it on the same nonces) and
the secrecy of the nonces of such runs.

This is a teaching tool, not a protocol verifier. Use Tamarin, ProVerif or
Scyther for real analysis.
"""

from itertools import combinations_with_replacement
from typing import Dict, FrozenSet, List, NamedTuple, Optional, Tuple, Union

Term = Union[str, tuple]  # an atom is a str; ("tup", t1, ..., tn); ("enc", X, body)

AGENTS = ("A", "B", "I")
HONEST = ("A", "B")
INTRUDER = "I"
INTRUDER_NONCE = "Ni"


def tup(*parts: Term) -> tuple:
    return ("tup",) + parts


def enc(agent: str, body: Term) -> tuple:
    return ("enc", agent, body)


def show(t: Term) -> str:
    if isinstance(t, str):
        return t
    if t[0] == "tup":
        return ", ".join(show(p) for p in t[1:])
    return "{" + show(t[2]) + "}pk(" + t[1] + ")"


# ---------------------------------------------------------------- intruder deduction


def close(known: FrozenSet[Term]) -> FrozenSet[Term]:
    """Analysis: add every part of a pair and every body of {m}pk(I), until nothing is new."""
    out = set(known)
    work = list(known)
    while work:  # @line L12
        t = work.pop()
        parts: Tuple[Term, ...] = ()
        if isinstance(t, tuple) and t[0] == "tup":
            parts = t[1:]
        elif isinstance(t, tuple) and t[0] == "enc" and t[1] == INTRUDER:
            parts = (t[2],)
        for p in parts:
            if p not in out:
                out.add(p)
                work.append(p)
    return frozenset(out)


def derive(known: FrozenSet[Term], t: Term) -> bool:
    """Synthesis over an analysed set: known terms, pairs of derivable parts, and
    encryption of a derivable body with any public key (all public keys are public)."""
    if t in known:  # @line L13
        return True
    if isinstance(t, tuple) and t[0] == "tup":
        return all(derive(known, p) for p in t[1:])
    if isinstance(t, tuple) and t[0] == "enc":
        return derive(known, t[2])
    return False


# ---------------------------------------------------------------- protocol roles


class Session(NamedTuple):
    role: str  # "init" or "resp"
    agent: str
    partner: Optional[str]  # fixed for the initiator; learned from message 1 by the responder
    nonce: str  # the fresh nonce of this session
    step: int  # 0, 1 or 2 (2 = finished)
    peer_nonce: Optional[str]  # the other party's nonce, once received


def msg1(a: str, x: str, na: str) -> tuple:
    return enc(x, tup(na, a))


def msg2(proto: str, b: str, y: str, na: str, nb: str) -> tuple:
    return enc(y, tup(na, nb, b) if proto == "nsl" else tup(na, nb))


def msg3(x: str, nb: str) -> tuple:
    return enc(x, nb)


def make_sessions(scenario: List[tuple]) -> Tuple[Session, ...]:
    out = []
    for i, s in enumerate(scenario):
        if s[0] == "init":
            out.append(Session("init", s[1], s[2], "N%d" % (i + 1), 0, None))
        else:
            out.append(Session("resp", s[1], None, "N%d" % (i + 1), 0, None))
    return tuple(out)


def initial_knowledge(sessions: Tuple[Session, ...]) -> FrozenSet[Term]:
    return close(frozenset(AGENTS + (INTRUDER_NONCE,)))


# ---------------------------------------------------------------- goals


def violated(sessions: Tuple[Session, ...], known: FrozenSet[Term]) -> Tuple[str, ...]:
    """Return the goals that fail in this state (empty when all hold)."""
    out = []
    for s in sessions:
        if s.step != 2 or s.partner not in HONEST:
            continue
        if s.nonce in known or s.peer_nonce in known:
            out.append("secrecy: %s's run with %s leaks a nonce" % (s.agent, s.partner))
        if s.role == "resp":
            ok = any(t.role == "init" and t.agent == s.partner and t.partner == s.agent and t.nonce == s.peer_nonce and t.step == 2 and t.peer_nonce == s.nonce for t in sessions)
        else:
            ok = any(t.role == "resp" and t.agent == s.partner and t.partner == s.agent and t.nonce == s.peer_nonce and t.peer_nonce == s.nonce and t.step >= 1 for t in sessions)
        if not ok:
            out.append("agreement: %s finished a run with %s, but %s ran no matching run with %s" % (s.agent, s.partner, s.partner, s.agent))
    return tuple(out)


# ---------------------------------------------------------------- the search


class Result(NamedTuple):
    attack: Optional[List[str]]
    goals: Tuple[str, ...]
    states: int


def check(proto: str, scenario: List[tuple]) -> Result:
    """Depth-first search over all interleavings and all derivable typed inputs."""
    assert proto in ("nspk", "nsl")
    start = make_sessions(scenario)
    nonces = tuple(s.nonce for s in start) + (INTRUDER_NONCE,)
    stack: List[Tuple[Tuple[Session, ...], FrozenSet[Term], Tuple[str, ...]]] = [(start, initial_knowledge(start), ())]  # @line L1
    seen = set()
    while stack:  # @line L2
        sessions, known, trace = stack.pop()  # @line L3
        if (sessions, known) in seen:  # @line L4
            continue
        seen.add((sessions, known))
        goals = violated(sessions, known)
        if goals:  # @line L5
            return Result(list(trace), goals, len(seen))
        for i, s in enumerate(sessions):
            def advance(new: Session) -> Tuple[Session, ...]:
                return sessions[:i] + (new,) + sessions[i + 1:]

            if s.role == "init" and s.step == 0:  # @line L6
                m = msg1(s.agent, s.partner, s.nonce)
                stack.append((advance(s._replace(step=1)), close(known | {m}), trace + ("%s sends %s" % (s.agent, show(m)),)))  # @line L7
            elif s.role == "init" and s.step == 1:  # @line L8
                for z in nonces:  # @line L9
                    expect = msg2(proto, s.partner, s.agent, s.nonce, z)
                    if derive(known, expect):  # @line L10
                        m = msg3(s.partner, z)
                        ev = ("%s receives %s" % (s.agent, show(expect)), "%s sends %s" % (s.agent, show(m)))
                        stack.append((advance(s._replace(step=2, peer_nonce=z)), close(known | {m}), trace + ev))
            elif s.role == "resp" and s.step == 0:
                for w in nonces:
                    for y in AGENTS:
                        if y == s.agent:
                            continue
                        expect = msg1(y, s.agent, w)
                        if derive(known, expect):
                            m = msg2(proto, s.agent, y, w, s.nonce)
                            ev = ("%s receives %s" % (s.agent, show(expect)), "%s sends %s" % (s.agent, show(m)))
                            stack.append((advance(s._replace(step=1, partner=y, peer_nonce=w)), close(known | {m}), trace + ev))
            elif s.role == "resp" and s.step == 1:
                expect = msg3(s.agent, s.nonce)
                if derive(known, expect):
                    ev = ("%s receives %s" % (s.agent, show(expect)),)
                    stack.append((advance(s._replace(step=2)), known, trace + ev))
    return Result(None, (), len(seen))  # @line L11


SESSION_KINDS = [("init", "A", "B"), ("init", "A", "I"), ("init", "B", "A"), ("init", "B", "I"), ("resp", "A"), ("resp", "B")]


def check_all(proto: str, max_sessions: int) -> Dict[tuple, Result]:
    """Run check on every multiset of at most max_sessions sessions."""
    out = {}
    for k in range(1, max_sessions + 1):
        for scen in combinations_with_replacement(SESSION_KINDS, k):
            out[scen] = check(proto, list(scen))
    return out
