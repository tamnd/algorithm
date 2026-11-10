# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nakamoto-consensus/. The authors are listed in prov/XQ55B7.jsonl.

import math
from fractions import Fraction as F

from nakamoto_consensus import (Block, attacker_success, attacker_success_exact, better, catch_up,
                                chain_of, common_prefix, min_z, ruin_finite, selfish_revenue,
                                simulate, simulate_race, simulate_selfish)

# The tables of Section 11 of the white paper
PAPER_Q01 = [1.0000000, 0.2045873, 0.0509779, 0.0131722, 0.0034552, 0.0009137,
             0.0002428, 0.0000647, 0.0000173, 0.0000046, 0.0000012]
PAPER_Q03 = {5: 0.1773523, 10: 0.0416605, 15: 0.0101008, 20: 0.0024804, 25: 0.0006132,
             30: 0.0001522, 35: 0.0000379, 40: 0.0000095, 45: 0.0000024, 50: 0.0000006}
PAPER_MIN_Z = {0.10: 5, 0.15: 8, 0.20: 11, 0.25: 15, 0.30: 24, 0.35: 41, 0.40: 89, 0.45: 340}


def test_white_paper_tables() -> None:
    for z, want in enumerate(PAPER_Q01):
        assert round(attacker_success(0.1, z), 7) == want
    for z, want in PAPER_Q03.items():
        assert round(attacker_success(0.3, z), 7) == want
    for q, z in PAPER_MIN_Z.items():
        assert min_z(q) == z


def test_gamblers_ruin() -> None:
    for q in (F(1, 10), F(3, 10), F(1, 2), F(3, 5)):
        p, n = 1 - q, 12
        a = [ruin_finite(q, z, n) for z in range(n + 1)]
        assert a[0] == 1 and a[n] == 0
        for z in range(1, n):
            assert a[z] == p * a[z + 1] + q * a[z - 1]  # first-step equation, exactly
    # as the far barrier moves away the finite answer tends to (q/p)^z
    q = F(3, 10)
    gaps = [catch_up(q, 4) - ruin_finite(q, 4, n) for n in (10, 20, 40)]
    assert all(g > 0 for g in gaps) and gaps[0] > gaps[1] > gaps[2]
    assert gaps[2] < F(1, 10 ** 12)
    assert catch_up(F(1, 2), 7) == 1 and catch_up(F(3, 5), 7) == 1


def test_race_simulation_matches_formulas() -> None:
    for q, z, seed in ((0.3, 5, 1), (0.1, 2, 3), (0.2, 3, 5)):
        n = 12000
        for poisson, formula in ((True, attacker_success), (False, attacker_success_exact)):
            est = simulate_race(q, z, n, seed + poisson, poisson)
            want = formula(q, z)
            sigma = math.sqrt(want * (1 - want) / n)
            assert abs(est - want) < 4 * sigma + 1e-3


def test_exact_and_poisson_differ_a_little() -> None:
    # z = 1, q = 0.1: 0.9 * (1/9) + 0.1 = 0.2 exactly, against 0.2045873 in the paper's table
    assert abs(attacker_success_exact(0.1, 1) - 0.2) < 1e-12
    for q in (0.1, 0.3):
        for z in (1, 3, 6):
            a, b = attacker_success(q, z), attacker_success_exact(q, z)
            assert a != b and b / a < 3 and a / b < 3


def test_most_work_not_most_blocks() -> None:
    g = Block(0, None, 0, -1)
    long = g
    for i in range(5):
        long = Block(1 + i, long, 10, 0)  # five easy blocks, work 50
    short = g
    for i in range(2):
        short = Block(10 + i, short, 40, 1)  # two hard blocks, work 80
    assert better(short, long) and not better(long, short)
    assert chain_of(short) == [0, 10, 11]


def test_common_prefix_and_forks() -> None:
    forks = 0
    for seed in range(30):
        tips, blocks = simulate(miners=8, p=0.01, delay=3, rounds=1500, seed=seed)
        assert common_prefix(tips, 6)
        main = set(chain_of(max(tips, key=lambda b: b.work)))
        forks += len(blocks) - len(main)
    assert forks > 0  # with delay, some blocks are orphaned


def test_long_delay_breaks_agreement_on_recent_blocks() -> None:
    # with delay far above the block interval, the tips disagree deeply
    bad = sum(not common_prefix(simulate(8, 0.2, 10, 200, s)[0], 2) for s in range(10))
    assert bad > 5


def test_selfish_mining() -> None:
    for alpha, gamma in ((0.25, 0.0), (0.3, 0.5), (0.34, 0.0), (0.4, 0.0)):
        est = simulate_selfish(alpha, gamma, 150000, seed=7)
        assert abs(est - selfish_revenue(alpha, gamma)) < 0.01
    # threshold (1 - gamma) / (3 - 2 gamma): 1/3 for gamma = 0, 1/4 for gamma = 1/2
    for gamma, th in ((0.0, 1 / 3), (0.5, 1 / 4)):
        assert selfish_revenue(th - 0.01, gamma) < th - 0.01
        assert selfish_revenue(th + 0.01, gamma) > th + 0.01
        assert abs(selfish_revenue(th, gamma) - th) < 1e-12
