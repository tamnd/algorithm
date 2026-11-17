---
title: Each accepted Newton step lowers the NDT cost, and the cost converges
proves: [correctness]
status: full
---

We use the notation of the page and of the reference code. The current scan has $m$ points $x_1, \ldots, x_m$. A pose $p = (t_x, t_y, \phi)$ maps $x$ to $x'(p) = R(\phi) x + t$. There are four grids. In grid $g$, the point $x'$ falls into one cell $c_g(x')$. If that cell holds a distribution with mean $q$ and inverse covariance $A$, the pair adds the term $-\exp(-s)$ with $s = \frac{1}{2} u^\top A u$ and $u = x' - q$; else it adds nothing. The cost $f(p)$ is the sum of all these terms. Line L3 computes $f$, a vector $g$ and a matrix $H$. Line L4 adds $\lambda I$ to $H$ until a Cholesky factorization succeeds, and solves $(H + \lambda I)\,\Delta p = -g$. Line L5 tries the steps $\Delta p, \Delta p / 2, \Delta p / 4, \ldots$, at most 20 of them, and line L6 accepts the first one that gives a smaller $f$.

## Lemma 1: the cost is bounded

$-4m \le f(p) \le 0$ for every pose $p$.

*Proof.* Each matrix $A$ is positive definite: it is $U \operatorname{diag}(1/\ell_1, 1/\ell_2) U^\top$ with $\ell_1 > 0$ and $\ell_2 \ge 0.001\,\ell_1 > 0$. So $s \ge 0$ and each term $-\exp(-s)$ lies in $[-1, 0)$. Each of the $m$ points adds at most one term for each of the 4 grids. $\square$

## Lemma 2: the history strictly decreases and converges

The values $f_0, f_1, \ldots$ in the history of the reference code satisfy $f_{j+1} < f_j$, and the sequence has a limit.

*Proof.* Line L5 sets `accepted` only when the trial value is below the current value $f$, and line L6 appends exactly that value. So every new entry is smaller than the one before. By Lemma 1 the entries are bounded below by $-4m$. A decreasing sequence that is bounded below converges. $\square$

The reference code also stops after `max_iter` steps, or when the decrease is below the relative tolerance (line L7), so it always ends.

## Lemma 3: g and H are the exact derivatives where the cells do not change

Let $p$ be a pose at which no point $x'(p)$ lies on a cell boundary of any grid. Then $f$ is smooth near $p$, and $g = \nabla f(p)$ and $H = \nabla^2 f(p)$.

*Proof.* The cell boundaries are lines, and $x'(p)$ depends continuously on $p$. So in a small neighbourhood of $p$ every point stays in the same cell of every grid, and $f$ is a fixed sum of smooth functions there. Take one term, with $u = x'(p) - q$ and $A$ fixed. Let $J_i = \partial x' / \partial p_i$: $J_1 = (1, 0)$, $J_2 = (0, 1)$ and $J_3 = (-x_1 \sin\phi - x_2 \cos\phi,\; x_1 \cos\phi - x_2 \sin\phi)$. Since $A$ is symmetric, $\partial s / \partial p_i = u^\top A J_i$, so

$$\frac{\partial}{\partial p_i}\bigl(-e^{-s}\bigr) = e^{-s}\, u^\top A J_i .$$

Differentiate again with respect to $p_k$:

$$\frac{\partial^2}{\partial p_i \partial p_k}\bigl(-e^{-s}\bigr) = e^{-s} \Bigl( -(u^\top A J_i)(u^\top A J_k) + J_i^\top A J_k + u^\top A \frac{\partial J_i}{\partial p_k} \Bigr).$$

$J_1$ and $J_2$ are constant, and $J_3$ depends on $\phi$ only, so $\partial J_i / \partial p_k = 0$ unless $i = k = 3$, where it is $h = (-x_1 \cos\phi + x_2 \sin\phi,\; -x_1 \sin\phi - x_2 \cos\phi)$. These are the expressions that the function `score` adds up, term by term, for $g$ and the upper triangle of $H$; it copies the upper triangle to the lower one, which is correct because $H$ is symmetric. $\square$

## Lemma 4: the step is a descent direction

If $g \ne 0$, the step $\Delta p$ of line L4 satisfies $g^\top \Delta p < 0$. Line L4 ends after a finite number of tries.

*Proof.* The Cholesky factorization of a symmetric matrix succeeds exactly when the matrix is positive definite. $H + \lambda I$ is positive definite once $\lambda$ exceeds minus the smallest eigenvalue of $H$, and $\lambda$ grows at least geometrically after the first try, so the loop ends. Then $\Delta p = -(H + \lambda I)^{-1} g$, and $g^\top \Delta p = -g^\top (H + \lambda I)^{-1} g < 0$, because the inverse of a positive definite matrix is positive definite. $\square$

## Theorem

Let $p$ be a pose as in Lemma 3 with $g \ne 0$. Then there is a $\tau > 0$ such that $f(p + t\,\Delta p) < f(p)$ for every $0 < t < \tau$. So if $\tau > 2^{-19}$, line L5 accepts a step, and the reference code makes progress. In every case, the pose that the code returns has a cost no higher than the start pose, and the costs of the accepted poses strictly decrease.

*Proof.* By Lemma 3, $f$ is differentiable at $p$ with gradient $g$, so $f(p + t \Delta p) = f(p) + t\, g^\top \Delta p + o(t)$. By Lemma 4 the linear term is negative, so it dominates for small $t$, which gives $\tau$. Line L5 tries $t = 1, 1/2, \ldots, 2^{-19}$, and one of these lies below $\tau$ if $\tau > 2^{-19}$. The last claims are Lemma 2. $\square$

## What this does not prove

- **No global optimum.** $f$ has many local minima, one for nearly every way to put the walls of the scan onto walls of the map. The code finds a pose where no further step is accepted, which is near a local minimum. From a start pose far from the truth, this local minimum can be wrong. The tests show that a grid of side 1.0 recovers a turn of 8 degrees but fails for some scans with a turn of 12 degrees.
- **Jumps at cell boundaries.** When a point crosses a cell boundary, its term changes to the term of another cell, so $f$ jumps. At a pose on a boundary, Lemma 3 does not hold, and the step may not be a descent direction. The four shifted grids make the jumps smaller, because a point that crosses one boundary line keeps the terms of the two grids that do not have that line, but they do not remove them. The code is still safe, because it accepts only steps that lower $f$.
- **No rate.** The proof does not show that the limit of the history is a stationary point, or how fast the pose converges. The plain Newton rate holds near a minimum only if the cells stay the same and $H$ is positive definite there.
