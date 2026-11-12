# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weak-learnability-equivalence/. The authors are listed in prov/XAZCTX.jsonl.
"""Weak to strong learning by AdaBoost, with decision stumps as the weak learner.

Every round records the weighted error eps_t of the stump, its edge gamma_t = 1/2 - eps_t, the
normalizer Z_t = 2 sqrt(eps_t (1 - eps_t)), and the training error of the weighted vote. The theorem
says: training error <= prod Z_t <= exp(-2 sum gamma_t^2).
"""

import math
import random

Point = tuple[float, ...]
Stump = tuple[int, float, int]  # (feature, threshold, sign): predict sign if x[feature] > threshold, else -sign


def stump_predict(s: Stump, x: Point) -> int:
    f, thr, sgn = s
    return sgn if x[f] > thr else -sgn


def best_stump(xs: list[Point], ys: list[int], w: list[float]) -> tuple[Stump, float]:
    """The stump with the smallest weighted error, by trying every threshold between sorted values."""
    best: tuple[Stump, float] = ((0, -math.inf, 1), math.inf)
    total = sum(w)
    for f in range(len(xs[0])):
        order = sorted(range(len(xs)), key=lambda i: xs[i][f])
        # Threshold below every point: sign +1 predicts +1 everywhere.
        err_plus = sum(w[i] for i in order if ys[i] != 1)
        cands = [(err_plus, -math.inf)]
        for pos, i in enumerate(order):
            # Move point i to the "<= threshold" side, where sign +1 predicts -1.
            err_plus += w[i] if ys[i] == 1 else -w[i]
            nxt = xs[order[pos + 1]][f] if pos + 1 < len(order) else math.inf
            if nxt > xs[i][f]:
                thr = (xs[i][f] + nxt) / 2 if nxt < math.inf else math.inf
                cands.append((err_plus, thr))
        for e, thr in cands:
            for sgn, err in ((1, e), (-1, total - e)):
                if err < best[1] - 1e-15:
                    best = ((f, thr, sgn), err)
    return best[0], best[1] / total


def adaboost(xs: list[Point], ys: list[int], rounds: int) -> tuple[list[tuple[float, Stump]], list[dict]]:
    """Run AdaBoost. Returns the weighted vote [(alpha_t, h_t)] and one record per round."""
    n = len(xs)
    d = [1.0 / n] * n
    vote: list[tuple[float, Stump]] = []
    log: list[dict] = []
    margins = [0.0] * n
    prod_z = 1.0
    sum_g2 = 0.0
    for t in range(rounds):
        h, eps = best_stump(xs, ys, d)
        if eps <= 0.0:  # a perfect stump: the vote of it alone has zero training error
            vote.append((1.0, h))
            margins = [m + ys[i] * stump_predict(h, xs[i]) for i, m in enumerate(margins)]
            log.append({"t": t + 1, "eps": 0.0, "gamma": 0.5, "z": 0.0, "prod_z": 0.0,
                        "exp_bound": math.exp(-2 * (sum_g2 + 0.25)), "train_error": 0.0, "mass_on_wrong": 0.0})
            break
        alpha = 0.5 * math.log((1 - eps) / eps)
        z = 2 * math.sqrt(eps * (1 - eps))
        new = [d[i] * math.exp(-alpha * ys[i] * stump_predict(h, xs[i])) for i in range(n)]
        z_direct = sum(new)
        d = [v / z_direct for v in new]
        vote.append((alpha, h))
        margins = [m + alpha * ys[i] * stump_predict(h, xs[i]) for i, m in enumerate(margins)]
        prod_z *= z
        gamma = 0.5 - eps
        sum_g2 += gamma * gamma
        log.append({
            "t": t + 1, "eps": eps, "gamma": gamma, "z": z, "z_direct": z_direct, "prod_z": prod_z,
            "exp_bound": math.exp(-2 * sum_g2),
            "train_error": sum(1 for m in margins if m <= 0) / n,
            "mass_on_wrong": sum(d[i] for i in range(n) if stump_predict(h, xs[i]) != ys[i]),
        })
    return vote, log


def predict(vote: list[tuple[float, Stump]], x: Point) -> int:
    s = sum(a * stump_predict(h, x) for a, h in vote)
    return 1 if s > 0 else -1


def circle_data(n: int, rng: random.Random, radius2: float = 0.5) -> tuple[list[Point], list[int]]:
    xs = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
    ys = [1 if x * x + y * y < radius2 else -1 for x, y in xs]
    return xs, ys


if __name__ == "__main__":
    xs, ys = circle_data(200, random.Random(1))
    tx, ty = circle_data(5000, random.Random(2))
    vote, log = adaboost(xs, ys, 400)
    scores = [0.0] * len(tx)
    first_zero = min((r["t"] for r in log if r["train_error"] == 0), default=None)
    for r, (a, h) in zip(log, vote):
        scores = [s + a * stump_predict(h, x) for s, x in zip(scores, tx)]
        if r["t"] in (1, 2, 3, 5, 10, 20, 50, 100, 200, 400) or r["t"] == first_zero:
            test = sum((1 if s > 0 else -1) != y for s, y in zip(scores, ty)) / len(tx)
            print(r["t"], round(r["eps"], 4), round(r["train_error"], 4), round(r["prod_z"], 4),
                  round(r["exp_bound"], 4), round(test, 4))
