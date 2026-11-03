"""Random lists for the sorting problem (spec 09.4).

The parameter k sets the range of the items. A small k gives many repeated items. With k = 0 the items use the full range of a 64-bit integer.
"""

import itertools

LETTERS = "abcdefghijklmnopqrstuvwxyz"


def item(rng, T, k):
    if T == "string":
        alphabet = LETTERS[: max(1, min(k, 26))] if k else LETTERS
        return "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 6)))
    if k == 0:
        return rng.randint(-(2**63), 2**63 - 1)
    return rng.randint(-k, k)


def generate(rng, n, T="int", k=1000):
    return {"xs": [item(rng, T, k) for _ in range(n)]}


def exhaustive(n, T="int", k=1000):
    """Each list of length n over three values, which covers each order and each pattern of repeated items."""
    values = ["", "a", "b"] if T == "string" else [-1, 0, 1]
    for p in itertools.product(values, repeat=n):
        yield {"xs": list(p)}
