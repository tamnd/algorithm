# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hyperparameter-tuning/. The authors are listed in prov/47B9Z8.jsonl.

"""Grid search, random search, successive halving and Hyperband.

A configuration is any value; evaluate(config, budget) trains with the given
resource (epochs, samples, ...) and returns a validation loss, lower is
better. Hyperband follows Algorithm 1 of Li, Jamieson, DeSalvo, Rostamizadeh
and Talwalkar (2018): s_max = floor(log_eta R), B = (s_max + 1) R, and bracket
s starts n = ceil(B / R * eta^s / (s + 1)) configurations with resource
r = R eta^-s. Round i of successive halving evaluates n_i = floor(n eta^-i)
configurations with r_i = r eta^i and keeps the best floor(n_i / eta).
Resources are Fractions, so the budget arithmetic is exact.
"""

import itertools
from fractions import Fraction
from typing import Callable, Dict, List, Sequence, Tuple


def grid_search(space: Dict[str, Sequence], evaluate: Callable[[dict], float]) -> Tuple[dict, float]:
    """Evaluate every point of the Cartesian product of the value lists; return the best."""
    keys = sorted(space)
    best = None
    for values in itertools.product(*(space[k] for k in keys)):
        config = dict(zip(keys, values))
        loss = evaluate(config)
        if best is None or loss < best[1]:
            best = (config, loss)
    return best


def random_search(sample: Callable, evaluate: Callable, trials: int, rng) -> Tuple[object, float]:
    """Evaluate `trials` configurations drawn independently by sample(rng); return the best."""
    best = None
    for _ in range(trials):
        config = sample(rng)
        loss = evaluate(config)
        if best is None or loss < best[1]:
            best = (config, loss)
    return best


def prob_hit_top_fraction(q: Fraction, trials: int) -> Fraction:
    """P(at least one of `trials` independent draws lands in a region of probability q) = 1 - (1 - q)^T."""
    return 1 - (1 - Fraction(q)) ** trials


def max_bracket(r_max: int, eta: int) -> int:
    """s_max = floor(log_eta R), by integer arithmetic."""
    s, p = 0, 1
    while p * eta <= r_max:
        p *= eta
        s += 1
    return s


def successive_halving_schedule(n: int, r: Fraction, eta: int, s: int) -> List[Tuple[int, Fraction]]:
    """The rounds (n_i, r_i) = (floor(n / eta^i), r eta^i) for i = 0..s."""
    return [(n // eta ** i, Fraction(r) * eta ** i) for i in range(s + 1)]


def hyperband_schedule(r_max: int, eta: int) -> List[Tuple[int, List[Tuple[int, Fraction]]]]:
    """The brackets of Hyperband, from s = s_max down to 0, each with its successive halving rounds."""
    s_max = max_bracket(r_max, eta)
    out = []
    for s in range(s_max, -1, -1):
        n = -((-(s_max + 1) * eta ** s) // (s + 1))  # ceil((s_max + 1) eta^s / (s + 1)) = ceil(B/R eta^s/(s+1))
        r = Fraction(r_max, eta ** s)
        out.append((s, successive_halving_schedule(n, r, eta, s)))
    return out


def bracket_budget(rounds: Sequence[Tuple[int, Fraction]]) -> Fraction:
    """The total resource of one bracket: sum of n_i r_i."""
    return sum((Fraction(n) * r for n, r in rounds), Fraction(0))


def successive_halving(configs: Sequence, evaluate: Callable, rounds: Sequence[Tuple[int, Fraction]],
                       eta: int) -> Tuple[object, float, Fraction]:
    """Run successive halving on the given configurations with the given rounds.

    Returns the best configuration of the last round, its loss, and the total
    resource spent (each evaluation is charged its full r_i).
    """
    alive = list(configs)
    spent = Fraction(0)
    best = None
    for i, (n_i, r_i) in enumerate(rounds):
        assert len(alive) == n_i
        scored = sorted(((evaluate(c, r_i), k, c) for k, c in enumerate(alive)), key=lambda t: (t[0], t[1]))
        spent += n_i * r_i
        best = (scored[0][2], scored[0][0])
        alive = [c for _, _, c in scored[: n_i // eta]]
    return best[0], best[1], spent


def hyperband(sample: Callable, evaluate: Callable, r_max: int, eta: int, rng) -> Tuple[object, float, Fraction]:
    """Hyperband: run every bracket of the schedule on freshly sampled configurations; return the best."""
    best, spent = None, Fraction(0)
    for _, rounds in hyperband_schedule(r_max, eta):
        configs = [sample(rng) for _ in range(rounds[0][0])]
        c, loss, used = successive_halving(configs, evaluate, rounds, eta)
        spent += used
        if best is None or loss < best[1]:
            best = (c, loss)
    return best[0], best[1], spent
