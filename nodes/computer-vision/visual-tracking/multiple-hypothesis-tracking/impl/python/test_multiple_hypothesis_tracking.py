# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiple-hypothesis-tracking/. The authors are listed in prov/XRTTYC.jsonl.

import itertools
import math
import random

from multiple_hypothesis_tracking import INF, MHT, hungarian, murty_k_best


def all_assignments(cost):
    r = len(cost)
    c = len(cost[0]) if r else 0
    out = []
    for cols in itertools.permutations(range(c), r):
        s = sum(cost[i][j] for i, j in enumerate(cols))
        if s < INF:
            out.append((s, list(cols)))
    out.sort(key=lambda t: t[0])
    return out


def test_hungarian_and_murty_against_brute_force():
    rng = random.Random(1968)
    for _ in range(150):
        r = rng.randint(1, 4)
        c = rng.randint(r, 6)
        cost = [[INF if rng.random() < 0.3 else rng.randint(0, 30) for _ in range(c)] for _ in range(r)]
        every = all_assignments(cost)
        k = rng.randint(1, 12)
        got = murty_k_best(cost, k)
        assert len(got) == min(k, len(every))
        # the costs are the k smallest, in order; the assignments are valid and distinct
        assert [g[0] for g in got] == [e[0] for e in every[: len(got)]]
        seen = set()
        for total, sol in got:
            assert len(set(sol)) == r
            assert sum(cost[i][j] for i, j in enumerate(sol)) == total
            seen.add(tuple(sol))
        assert len(seen) == len(got)
        if every:
            assert hungarian(cost)[0] == every[0][0]
        else:
            assert hungarian(cost) is None


def reid_log_weight(mht, pred, zs, owner):
    """Reid's formula, written directly: owner[j] is a track index, 'NT' or 'FT'."""
    n = len(pred)
    lw = 0.0
    detected = 0
    for j, o in enumerate(owner):
        if o == "NT":
            lw += math.log(mht.beta_nt)
        elif o == "FT":
            lw += math.log(mht.beta_ft)
        else:
            _, _, _, _, z_hat, s, s_inv, det, _ = pred[o]
            nu = [zs[j][0] - z_hat[0], zs[j][1] - z_hat[1]]
            d2 = sum(nu[a] * s_inv[a][b] * nu[b] for a in range(2) for b in range(2))
            if d2 > mht.gamma:
                return None
            lw += math.log(mht.p_d) - 0.5 * d2 - 0.5 * math.log((2 * math.pi) ** 2 * det)
            detected += 1
    return lw + (n - detected) * math.log(1.0 - mht.p_d)


def two_track_mht():
    mht = MHT(p_d=0.8, beta_nt=0.002, beta_ft=0.02, gamma=9.21)
    mht.add_track([[0.0], [0.0], [1.0], [0.0]], [[0.3, 0, 0, 0], [0, 0.3, 0, 0], [0, 0, 0.1, 0], [0, 0, 0, 0.1]])
    mht.add_track([[0.0], [2.0], [1.0], [0.0]], [[0.3, 0, 0, 0], [0, 0.3, 0, 0], [0, 0, 0.1, 0], [0, 0, 0, 0.1]])
    return mht


def test_children_follow_reid_formula():
    mht = two_track_mht()
    zs = [(1.2, 0.3), (1.0, 1.4), (0.8, 2.2)]
    w, tracks = mht.hyps[0]
    children = mht.children_of(w, tracks, zs, 10 ** 6)
    pred = children[0][1]
    brute = []
    for owner in itertools.product([0, 1, "NT", "FT"], repeat=len(zs)):
        used = [o for o in owner if o in (0, 1)]
        if len(used) != len(set(used)):
            continue
        lw = reid_log_weight(mht, pred, zs, owner)
        if lw is not None:
            brute.append(lw)
    brute.sort(reverse=True)
    got = [c[0] for c in children]
    assert len(got) == len(brute)
    assert all(abs(a - b) < 1e-9 for a, b in zip(got, brute))
    # the best child gives z1 to track 0 and z3 to track 1, and calls z2 a false alarm
    best = children[0][2]
    assert best[0] == 0 and best[2] == 1 and best[1] == 2 + 3 + 1


def test_global_top_m_is_exact():
    rng = random.Random(42)
    for _ in range(20):
        mht = two_track_mht()
        mht.m_best = 4
        mht.step([(1.0 + rng.gauss(0, 0.5), rng.gauss(0, 0.5)), (1.0 + rng.gauss(0, 0.5), 2.0 + rng.gauss(0, 0.5))])
        zs = [(2.0 + rng.gauss(0, 0.7), rng.gauss(0, 0.7)) for _ in range(2)] + [(2.0, 2.0 + rng.gauss(0, 0.5))]
        every = []
        for w, tracks in mht.hyps:
            every.extend(c[0] for c in mht.children_of(w, tracks, zs, 10 ** 6))
        every.sort(reverse=True)
        kept = []
        for w, tracks in mht.hyps:
            kept.extend(c[0] for c in mht.children_of(w, tracks, zs, mht.m_best))
        kept.sort(reverse=True)
        assert all(abs(a - b) < 1e-9 for a, b in zip(kept[: mht.m_best], every[: mht.m_best]))


def test_weights_are_normalized():
    mht = two_track_mht()
    mht.step([(1.1, 0.1), (0.9, 2.1), (5.0, 5.0)])
    assert abs(sum(math.exp(w) for w, _ in mht.hyps) - 1.0) < 1e-12
    assert len(mht.hyps) == mht.m_best


def test_no_measurements():
    mht = two_track_mht()
    est = mht.step([])
    assert sorted(est) == [0, 1]
    assert len(mht.hyps) == 1


def poisson(rng, mean):
    limit, k, prod = math.exp(-mean), 0, rng.random()
    while prod > limit:
        k += 1
        prod *= rng.random()
    return k


def run_scene(m_best, seed):
    rng = random.Random(seed)
    starts = [(0.0, 0.0, 1.0, 0.25), (0.0, 5.0, 1.0, -0.25)]  # the paths cross at frame 10
    mht = MHT(p_d=0.85, beta_nt=0.001, beta_ft=0.01, m_best=m_best)
    for x0, y0, vx, vy in starts:
        mht.add_track([[x0], [y0], [vx], [vy]], [[0.25, 0, 0, 0], [0, 0.25, 0, 0], [0, 0, 0.01, 0], [0, 0, 0, 0.01]])
    errs = []
    for t in range(1, 21):
        truth = [(x0 + vx * t, y0 + vy * t) for x0, y0, vx, vy in starts]
        zs = [(a + rng.gauss(0, 0.5), b + rng.gauss(0, 0.5)) for a, b in truth if rng.random() < 0.85]
        for _ in range(poisson(rng, 1.0)):
            zs.append((truth[0][0] + rng.uniform(-5, 5), 2.5 + rng.uniform(-5, 5)))
        rng.shuffle(zs)
        est = mht.step(zs)
        for tid, (a, b) in enumerate(truth):
            if tid in est:
                errs.append(math.hypot(est[tid][0] - a, est[tid][1] - b))
            else:
                errs.append(INF)
    return errs


def test_two_crossing_targets_in_clutter():
    errs = run_scene(5, 1979)
    assert max(errs) < 2.0
    assert sum(errs) / len(errs) < 0.6
