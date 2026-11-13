# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/belief-space/. The authors are listed in prov/N0RMN6.jsonl.

"""Beliefs and their updates, in the two forms that planners use.

A set belief is a frozenset of the states that are possible. Its update uses a
nondeterministic model: succ(s, a) is the set of possible next states, and
obs(s) is the set of observations that the sensor can give in the state s.

A probabilistic belief is a dict from states to probabilities, with no zero
entries. Its update uses P(s, a), a dict of next states to probabilities, and
O(o, s), the probability of the observation o in the state s. Use Fraction
values to get exact results.
"""

from collections import deque
from fractions import Fraction
from typing import Callable, Dict, FrozenSet, Hashable, Iterable, List, Optional, Set, Tuple

State = Hashable
SetBelief = FrozenSet[State]
ProbBelief = Dict[State, Fraction]


# ---- set beliefs ----

def progress(b: SetBelief, a, succ: Callable) -> SetBelief:
    """The states that are possible after the action a."""
    return frozenset(t for s in b for t in succ(s, a))


def filter_obs(b: SetBelief, o, obs: Callable) -> SetBelief:
    """The states of b in which the sensor can give the observation o."""
    return frozenset(s for s in b if o in obs(s))


def update_set(b: SetBelief, a, o, succ: Callable, obs: Callable) -> SetBelief:
    return filter_obs(progress(b, a, succ), o, obs)


def applicable(b: SetBelief, a, succ: Callable) -> bool:
    """An action is safe in a belief if it has a successor in every state of the belief."""
    return all(len(succ(s, a)) > 0 for s in b)


def reachable_set_beliefs(b0: SetBelief, actions: Iterable, succ: Callable, obs: Callable, observations: Iterable) -> Set[SetBelief]:
    """All nonempty set beliefs that some sequence of actions and observations gives from b0."""
    actions, observations = list(actions), list(observations)
    seen = {b0}
    queue = deque([b0])
    while queue:
        b = queue.popleft()
        for a in actions:
            if not applicable(b, a, succ):
                continue
            nb = progress(b, a, succ)
            for o in observations:
                c = filter_obs(nb, o, obs)
                if c and c not in seen:
                    seen.add(c)
                    queue.append(c)
    return seen


# ---- probabilistic beliefs ----

def predict(b: ProbBelief, a, P: Callable) -> ProbBelief:
    """The distribution of the next state: the sum over s of P(s' | s, a) b(s)."""
    out: Dict[State, Fraction] = {}
    for s, p in b.items():
        for t, q in P(s, a).items():
            out[t] = out.get(t, 0) + p * q
    return {t: p for t, p in out.items() if p != 0}


def obs_prob(b: ProbBelief, a, o, P: Callable, O: Callable):
    """Pr(o | b, a)."""
    return sum(O(o, t) * p for t, p in predict(b, a, P).items())


def update(b: ProbBelief, a, o, P: Callable, O: Callable) -> ProbBelief:
    """Bayes rule: b'(s') is proportional to O(o | s') times the predicted probability of s'."""
    pred = predict(b, a, P)
    joint = {t: O(o, t) * p for t, p in pred.items()}
    z = sum(joint.values())
    if z == 0:
        raise ValueError("the observation has probability 0 in this belief")
    return {t: p / z for t, p in joint.items() if p != 0}


def condition(b: ProbBelief, o, O: Callable) -> ProbBelief:
    """Bayes rule for an observation with no action, as for the first observation."""
    joint = {s: O(o, s) * p for s, p in b.items()}
    z = sum(joint.values())
    if z == 0:
        raise ValueError("the observation has probability 0 in this belief")
    return {s: p / z for s, p in joint.items() if p != 0}


def support(b: ProbBelief) -> SetBelief:
    return frozenset(s for s, p in b.items() if p > 0)


def as_vector(b: ProbBelief, states: List[State]) -> Tuple[Fraction, ...]:
    """The belief as a point of the simplex over the given order of states."""
    return tuple(Fraction(b.get(s, 0)) for s in states)


def track(b: ProbBelief, steps: Iterable[Tuple[Optional[object], object]], P: Callable, O: Callable) -> List[ProbBelief]:
    """Apply a sequence of (action, observation) pairs; an action of None means no move."""
    out = [b]
    for a, o in steps:
        b = condition(b, o, O) if a is None else update(b, a, o, P, O)
        out.append(b)
    return out
