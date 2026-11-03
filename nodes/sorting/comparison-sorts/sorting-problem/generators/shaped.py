"""Lists with an order that is a known hard case for some sorts (spec 09.4).

The shape is sorted, reversed, nearly (sorted with a few swaps), organ (up, then down) or equal (one value).
"""


def generate(rng, n, T="int", shape="sorted"):
    if T == "string":
        xs = sorted("".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(rng.randint(0, 6))) for _ in range(n))
    else:
        xs = sorted(rng.randint(-(10**6), 10**6) for _ in range(n))
    if shape == "reversed":
        xs.reverse()
    elif shape == "nearly":
        for _ in range(max(1, n // 20)):
            if n > 1:
                i, j = rng.randrange(n), rng.randrange(n)
                xs[i], xs[j] = xs[j], xs[i]
    elif shape == "organ":
        xs = xs[0::2] + xs[1::2][::-1]
    elif shape == "equal":
        xs = [xs[0]] * n if n else []
    return {"xs": xs}
