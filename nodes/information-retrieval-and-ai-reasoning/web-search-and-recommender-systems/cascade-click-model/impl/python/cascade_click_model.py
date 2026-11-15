# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cascade-click-model/. The authors are listed in prov/F0GVXM.jsonl.
"""The cascade click model (Craswell, Zoeter, Taylor and Ramsey, 2008).

The user examines the results from the top. At each examined result d the
user clicks with probability alpha[d]. After a click the user stops; after
a skip the user examines the next result. A session is recorded as the
rank of its click (0-based) or None when there is no click.
"""

import math


def click_distribution(ranking, alpha):
    """Return ([P(click at rank i) for each i], P(no click))."""
    probs = []
    miss = 1.0
    for d in ranking:
        probs.append(miss * alpha[d])
        miss *= 1.0 - alpha[d]
    return probs, miss


def simulate(rankings, alpha, rng):
    """Draw one session for each ranking, with the random source rng."""
    out = []
    for ranking in rankings:
        click = None
        for i, d in enumerate(ranking):
            if rng.random() < alpha[d]:
                click = i
                break
        out.append(click)
    return out


def examination_counts(rankings, clicks):
    """Return (examined, clicked): per document, the sessions in which it was
    examined (at or above the click, or anywhere in a session without a
    click) and the sessions in which it was clicked."""
    examined, clicked = {}, {}
    for ranking, c in zip(rankings, clicks):
        depth = len(ranking) if c is None else c + 1
        for d in ranking[:depth]:
            examined[d] = examined.get(d, 0) + 1
        if c is not None:
            clicked[ranking[c]] = clicked.get(ranking[c], 0) + 1
    return examined, clicked


def fit(rankings, clicks):
    """Maximum likelihood estimate: alpha[d] = clicks on d / examinations of d."""
    examined, clicked = examination_counts(rankings, clicks)
    return {d: clicked.get(d, 0) / n for d, n in examined.items()}


def log_likelihood(rankings, clicks, alpha):
    """Natural log of the probability of the observed sessions."""
    total = 0.0
    for ranking, c in zip(rankings, clicks):
        probs, miss = click_distribution(ranking, alpha)
        p = miss if c is None else probs[c]
        if p <= 0.0:
            return -math.inf
        total += math.log(p)
    return total
