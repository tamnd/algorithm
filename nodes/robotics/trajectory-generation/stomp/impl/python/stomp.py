# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stomp/. The authors are listed in prov/2F4S7V.jsonl.
"""STOMP: stochastic trajectory optimization for motion planning.

A point robot moves in the plane from q_0 to q_(n+1) through n free
waypoints theta_1, ..., theta_n. A is the n x n second-difference matrix
(1, -2, 1) and R = A^T A. The total cost of a trajectory is

    Q(theta) = sum_t q(theta_t) + (w / 2) sum_t |acc_t|^2,

where q is a state cost (any function, no gradient needed) and acc_t is the
second difference at waypoint t, using the fixed ends.

Each iteration samples K noise trajectories eps_k ~ N(0, sigma^2 R^-1) for
each coordinate, evaluates the state cost of theta + eps_k at every
waypoint, turns the costs at each waypoint into weights
P = exp(-S / lam) / sum exp(-S / lam), averages the noise with these
weights, smooths the average with M (R^-1 with each column scaled so that
its largest entry is 1/n), and adds it to theta. The best trajectory seen,
by Q, is returned.

A is symmetric and tridiagonal, so eps = sigma A^-1 z with z ~ N(0, I) has
the covariance sigma^2 (A^T A)^-1 = sigma^2 R^-1 and costs O(n) to sample.
"""

import math
import random


def straight_line(q0, q1, n):
    return [[q0[d] + (q1[d] - q0[d]) * t / (n + 1) for d in range(2)] for t in range(1, n + 1)]


def solve_second_difference(rhs):
    """Solve A x = rhs, A = tridiag(1, -2, 1) of size n (Thomas algorithm)."""
    n = len(rhs)
    c = [0.0] * n
    d = [0.0] * n
    beta = -2.0
    c[0] = 1.0 / beta
    d[0] = rhs[0] / beta
    for i in range(1, n):
        beta = -2.0 - c[i - 1]
        c[i] = 1.0 / beta
        d[i] = (rhs[i] - d[i - 1]) / beta
    x = [0.0] * n
    x[n - 1] = d[n - 1]
    for i in range(n - 2, -1, -1):
        x[i] = d[i] - c[i] * x[i + 1]
    return x


def r_inverse(n):
    """R^-1 = A^-1 A^-1 as a dense n x n list of rows (A is symmetric)."""
    cols = []
    for j in range(n):
        e = [0.0] * n
        e[j] = 1.0
        cols.append(solve_second_difference(solve_second_difference(e)))
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def smoothing_matrix(n):
    """M: R^-1 with each column scaled so that its largest entry is 1/n."""
    rinv = r_inverse(n)
    m = [[0.0] * n for _ in range(n)]
    for j in range(n):
        top = max(rinv[i][j] for i in range(n))
        for i in range(n):
            m[i][j] = rinv[i][j] / (top * n)
    return m


def sample_noise(rng, n, sigma):
    """One noise trajectory for both coordinates, each ~ N(0, sigma^2 R^-1)."""
    cols = [solve_second_difference([sigma * rng.gauss(0.0, 1.0) for _ in range(n)]) for _ in range(2)]
    return [[cols[0][t], cols[1][t]] for t in range(n)]


def weights(costs, lam):
    """exp(-S / lam), normalized; shifting by the minimum avoids overflow."""
    lo = min(costs)
    e = [math.exp(-(s - lo) / lam) for s in costs]
    tot = sum(e)
    return [v / tot for v in e]


def control_cost(theta, q0, q1, w):
    pts = [list(q0)] + [list(p) for p in theta] + [list(q1)]
    s = 0.0
    for t in range(1, len(pts) - 1):
        for d in range(2):
            a = pts[t - 1][d] - 2.0 * pts[t][d] + pts[t + 1][d]
            s += 0.5 * w * a * a
    return s


def total_cost(theta, q0, q1, state_cost, w):
    return sum(state_cost(p) for p in theta) + control_cost(theta, q0, q1, w)


def stomp(q0, q1, n, state_cost, k=20, lam=0.1, sigma=0.05, w=100.0, iters=100, seed=0, theta0=None):
    """Run STOMP. Returns (best theta, best Q, history of Q of the iterates)."""
    rng = random.Random(seed)
    m = smoothing_matrix(n)
    theta = straight_line(q0, q1, n) if theta0 is None else [list(p) for p in theta0]
    best, best_q = theta, total_cost(theta, q0, q1, state_cost, w)
    hist = [best_q]
    for _ in range(iters):  # @line L1
        noise, costs = [], []
        for _ in range(k):  # @line L2
            eps = sample_noise(rng, n, sigma)  # @line L3
            noise.append(eps)
            costs.append([state_cost([theta[t][0] + eps[t][0], theta[t][1] + eps[t][1]]) for t in range(n)])  # @line L4
        avg = [[0.0, 0.0] for _ in range(n)]
        for t in range(n):  # @line L5
            p = weights([costs[j][t] for j in range(k)], lam)  # @line L6
            for d in range(2):
                avg[t][d] = sum(p[j] * noise[j][t][d] for j in range(k))  # @line L7
        theta = [[theta[i][d] + sum(m[i][j] * avg[j][d] for j in range(n)) for d in range(2)] for i in range(n)]  # @line L8
        qv = total_cost(theta, q0, q1, state_cost, w)
        hist.append(qv)
        if qv < best_q:  # @line L9
            best, best_q = theta, qv
    return best, best_q, hist  # @line L10


def disc_hinge(discs, margin):
    """State cost: sum over discs of max(0, margin + r - |p - o|), no gradient used."""
    def cost(p):
        return sum(max(0.0, margin + r - math.hypot(p[0] - ox, p[1] - oy)) for ox, oy, r in discs)
    return cost


def min_clearance(theta, discs):
    return min(math.hypot(p[0] - ox, p[1] - oy) - r for p in theta for ox, oy, r in discs)
