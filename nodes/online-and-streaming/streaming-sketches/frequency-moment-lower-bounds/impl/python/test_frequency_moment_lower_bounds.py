# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frequency-moment-lower-bounds/. The authors are listed in prov/7C0H0K.jsonl.

import math
import random
from itertools import product

from frequency_moment_lower_bounds import (
    decide_from_estimate,
    disj_via_f_inf,
    message_bits,
    moment,
    players_for,
    promise_instance,
)


def test_moments_of_a_small_stream() -> None:
    s = list("abacab")
    assert [moment(s, p) for p in (0, 1, 2, 3)] == [3, 6, 14, 36]
    assert moment(s, math.inf) == 3


def test_f_inf_decides_disjointness_on_all_small_inputs() -> None:
    n = 5
    subsets = [{j for j in range(n) if mask >> j & 1} for mask in range(1 << n)]
    for a, b in product(subsets, repeat=2):
        assert disj_via_f_inf(a, b) == bool(a & b)


def test_promise_disjointness_gap_for_f_k() -> None:
    rng = random.Random(1)
    eps = 1 / 3
    for k in (2.5, 3, 4, 6):
        for n in (20, 50, 200):
            t = players_for(n, k)
            assert t**k > 2 * n and (t - 1) ** k <= 2 * n or t == 2
            for _ in range(20):
                sizes = [rng.randrange(0, (n - 1) // t + 1) for _ in range(t)]
                no = promise_instance(n, t, None, sizes)
                yes = promise_instance(n, t, rng.randrange(n), sizes)
                f_no = moment([x for s in no for x in s], k)
                f_yes = moment([x for s in yes for x in s], k)
                assert f_no <= n and f_yes >= t**k
                # Every allowed estimate leads to the right answer.
                for a in (1 - eps, 1, 1 + eps):
                    assert not decide_from_estimate(a * f_no, n, eps)
                    assert decide_from_estimate(a * f_yes, n, eps)


def test_message_count_of_the_simulation() -> None:
    assert message_bits(10, 2, 1) == 10
    assert message_bits(10, 2, 3) == 50
    assert message_bits(7, 5, 2) == 7 * (2 * 4 + 1)
