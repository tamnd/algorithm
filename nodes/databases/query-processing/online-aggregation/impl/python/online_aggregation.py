# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/online-aggregation/. The authors are listed in prov/NT88SJ.jsonl.

"""Online aggregation of SELECT g, SUM(x), COUNT(*), AVG(x) FROM T GROUP BY g.

The table is read in a random order (or in the given order when rng is None).
After i of the N tuples, for each group seen so far:

    SUM estimate    N / i * s_g          (s_g: sum of x in the group so far)
    COUNT estimate  N / i * c_g          (c_g: tuples of the group so far)
    AVG estimate    s_g / c_g

The SUM and COUNT estimates are unbiased. The AVG estimate is unbiased given
c_g >= 1, because the tuples of a group seen so far are then a uniform random
subset of the group. Two half widths are given for AVG: a large-sample one,
z * sqrt((1 - i/N) * var_g / c_g), and a conservative one from Hoeffding's
inequality for values in [lo, hi], (hi - lo) * sqrt(ln(2 / delta) / (2 c_g)),
which also holds for sampling without replacement. When i = N every estimate
is the exact answer.
"""

import math
import random
from collections.abc import Callable, Sequence
from fractions import Fraction


def online_aggregate(rows: Sequence[tuple], group: Callable, value: Callable, every: int = 1,
                     rng: random.Random | None = None, z: float = 1.96,
                     bounds: tuple | None = None, delta: float = 0.05) -> list:
    """Read rows one at a time and return a snapshot after every `every` tuples and at the end.

    A snapshot is (i, {g: estimates}); the estimates of a group are a dict with
    count, sum, avg (Fractions), half_clt and half_hoeffding (floats, the
    latter only when bounds = (lo, hi) is given).
    """
    order = list(rows)
    big_n = len(order)
    if rng is not None:
        rng.shuffle(order)  # @line L1
    cnt: dict = {}
    tot: dict = {}
    sq: dict = {}
    snaps = []
    for i, t in enumerate(order, start=1):  # @line L2
        g, x = group(t), value(t)
        cnt[g] = cnt.get(g, 0) + 1
        tot[g] = tot.get(g, 0) + x
        sq[g] = sq.get(g, 0) + x * x  # @line L3
        if i % every and i != big_n:
            continue
        est = {}
        for h in sorted(cnt, key=repr):
            c, s = cnt[h], tot[h]
            avg = Fraction(s, c)
            var = float((sq[h] - c * avg * avg) / (c - 1)) if c > 1 else 0.0
            e = {"count": Fraction(big_n * c, i), "sum": Fraction(big_n * s, i), "avg": avg,
                 "half_clt": z * math.sqrt(max(0.0, (1 - i / big_n) * var / c))}
            if bounds is not None:
                lo, hi = bounds
                e["half_hoeffding"] = 0.0 if i == big_n else (hi - lo) * math.sqrt(math.log(2 / delta) / (2 * c))
            est[h] = e  # @line L4
        snaps.append((i, est))
    return snaps  # @line L5
