---
title: The Epanechnikov mean shift step raises the weighted density, the tracker never accepts a lower coefficient, and both loops stop
proves: [correctness]
status: full
---

Notation as on the page. The window at $y$ has half axes $h = (h_u, h_v)$, and for a point $x$ we write $|x|_h^2 = (x_u / h_u)^2 + (x_v / h_v)^2$ and $r_i(y) = |x_i - y|_h^2$. The Epanechnikov profile is $k(r) = \max(1 - r, 0)$.

## Claim 1: one weighted step raises the weighted density

Let $x_1, \ldots, x_n$ be points with weights $w_i \ge 0$, and let

$$
f(y) = \sum_{i=1}^n w_i\, k(r_i(y)).
$$

Let $S = \{ i : r_i(y_0) \le 1 \}$ and $W = \sum_{i \in S} w_i$. If $W > 0$, the step is $y_1 = \sum_{i \in S} w_i x_i / W$. Then

$$
f(y_1) - f(y_0) \ge W\, |y_1 - y_0|_h^2 .
$$

*Proof.* $k$ is the maximum of the two affine functions $1 - r$ and $0$, so it is convex. For $i \in S$, the number $-1$ is a subgradient of $k$ at $r_i(y_0)$: if $r_i(y_0) < 1$ it is the derivative, and at $r_i(y_0) = 1$ the subgradients are the interval $[-1, 0]$. So $k(r) \ge k(r_i(y_0)) - (r - r_i(y_0))$ for every $r$. For $i \notin S$, $k(r_i(y_0)) = 0 \le k(r)$ for every $r$. Summing with the weights,

$$
f(y_1) - f(y_0) \ge \sum_{i \in S} w_i \big( r_i(y_0) - r_i(y_1) \big).
$$

The map $y \mapsto |x - y|_h^2$ is the squared norm of the inner product $\langle a, b \rangle_h = a_u b_u / h_u^2 + a_v b_v / h_v^2$. Expanding $|x_i - y_0|_h^2 = |x_i - y_1|_h^2 + 2 \langle x_i - y_1, y_1 - y_0 \rangle_h + |y_1 - y_0|_h^2$ and summing over $S$ with weights, the middle term is $2 \langle \sum_{i \in S} w_i (x_i - y_1), y_1 - y_0 \rangle_h = 0$ by the definition of $y_1$. So the right side equals $W |y_1 - y_0|_h^2$. $\square$

## Claim 2: with fixed weights, the iteration stops at a fixed point after finitely many steps

Repeat the step of Claim 1 from $y_0$ with the same points and weights, and stop when $W = 0$ or $y_{j+1} = y_j$.

*Proof.* Every $y_j$ with $j \ge 1$ is the weighted mean of a nonempty subset of the $n$ points, so it lies in a finite set of at most $2^n$ points. While the iteration runs, $y_{j+1} \ne y_j$ and $W > 0$, so Claim 1 gives $f(y_{j+1}) > f(y_j)$. The values of $f$ strictly increase, so no point of the finite set occurs twice, and the iteration stops after at most $2^n + 1$ steps. At the stop, $y_{j+1} = y_j$: the point is the weighted mean of the points in its own window. $\square$

This is the reason the Epanechnikov profile is used: the step is a weighted mean, and the convergence argument needs only convexity and the finite set. For profiles with unbounded support the argument does not apply, and the convergence of the sequence of points (not only of the density values) needs more care: Li, Hu and Wu (2007) pointed out a gap in the convergence proof of Comaniciu and Meer (2002).

## Claim 3: the tracker step increases a surrogate of the coefficient

In the tracker the weights are $w_i = \sqrt{q_{b(x_i)} / p_{b(x_i)}(y_0)}$, and $p_u(y) = C(y) \sum_i k(r_i(y)) [b(x_i) = u]$ with $C(y) = 1 / \sum_i k(r_i(y))$. For every bin with $p_u(y_0) > 0$, the concavity of the square root gives

$$
\sqrt{p_u(y)} \le \sqrt{p_u(y_0)} + \frac{p_u(y) - p_u(y_0)}{2 \sqrt{p_u(y_0)}} .
$$

Multiplying by $\sqrt{q_u}$ and summing gives $\rho(y) \le \frac12 \rho(y_0) + \frac12 \sum_u p_u(y) \sqrt{q_u / p_u(y_0)}$ over the bins with $p_u(y_0) > 0$ (a bin with $p_u(y_0) = 0$ and $p_u(y) > 0$ adds a term that the bound does not cover). If $C(y) = C(y_0) = C$, the last sum is $C\, f(y)$ with the weights $w_i$, and both sides are equal at $y = y_0$. So line L4 maximizes, by Claim 1, a function that agrees with $\rho$ to first order at $y_0$. This is a statement about the surrogate only. $C(y)$ changes with $y$ on a pixel grid, new bins can enter the window, and $\rho(y_1) < \rho(y_0)$ is possible. The tracker does not rely on the surrogate for correctness; Claim 4 does not use it.

## Claim 4: the accepted coefficients never decrease, and the procedure stops

*Proof.* A location is accepted only at line L10 or returned at line L9, and both are reached only when the test of line L8 failed, that is, when $\rho_1 \ge \rho_0$. The returned value at line L8 is the last accepted location. So the sequence of coefficients of accepted locations is nondecreasing, and the returned coefficient is at least the coefficient at the start. The inner loop of lines L6 and L7 runs at most $j_{\max}$ times, and the outer loop at most $k_{\max}$ times, so the procedure stops after at most $k_{\max} (j_{\max} + 1)$ histogram evaluations after the first. $\square$

## What is not claimed

Nothing here says that the returned location is the true target position, or even a local maximum of $\rho$. The coefficient is a heuristic score of similarity; a background patch with the same colors can score as high as the target, and the search sees only locations whose window overlaps the region where the iterations go. The halving rule of lines L6 and L7 is from Comaniciu, Ramesh and Meer; the cap $j_{\max}$ is added here so that the procedure provably stops.
