"""Random sorted lists and a key for the search problem (spec 09.4).

The parameter k sets the range of the items. A small k gives many repeated items. The key is an item of the list about half of the time, and else a random value, which can be below, above or between the items.
"""

import itertools

LETTERS = "abcdefghijklmnopqrstuvwxyz"


def item(rng, T, k):
    if T == "string":
        return "".join(rng.choice(LETTERS[: max(1, min(k, 26))]) for _ in range(rng.randint(0, 4)))
    return rng.randint(-k, k)


def generate(rng, n, T="int", k=1000):
    a = sorted(item(rng, T, k) for _ in range(n))
    if a and rng.random() < 0.5:
        x = rng.choice(a)
    else:
        x = item(rng, T, k + 2)
    return {"a": a, "x": x}


def exhaustive(n, T="int", k=1000):
    """Each sorted list of length n over three values, with each key from below the smallest to above the largest."""
    values = ["a", "b", "c"] if T == "string" else [0, 1, 2]
    keys = ["", "a", "ab", "b", "bc", "c", "d"] if T == "string" else [-1, 0, 1, 2, 3]
    for a in itertools.combinations_with_replacement(values, n):
        for x in keys:
            yield {"a": list(a), "x": x}
