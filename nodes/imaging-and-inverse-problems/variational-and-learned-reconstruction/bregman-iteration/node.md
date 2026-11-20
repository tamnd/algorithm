---
tag: 3BKXGP
kind: algorithm
slug: bregman-iteration
name: Bregman iteration
aliases:
- Osher-Burger Bregman iteration
- iterative regularization by Bregman distances
- add-back-the-residual iteration
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: advanced
summary: Repeat a variational reconstruction while adding the residual back to the data, which reduces the contrast loss of total variation regularization.
solves: [image-denoising, sparse-signal-recovery]
model: real-ram
complexity:
  vars: {K: the number of outer iterations, s: the cost of one inner variational solve, m: the number of data values}
  time: {worst: O(K (s + m))}
  space: {extra: O(m)}
properties: {deterministic: true, exact: false, iterative: true, monotone_residual: true, needs_stopping_rule_with_noise: true}
history:
  year: 2005
  people: [Stanley Osher, Martin Burger, Donald Goldfarb, Jinjun Xu, Wotao Yin]
  note: Bregman (1967) introduced the distance and a projection method for convex feasibility. Osher, Burger, Goldfarb, Xu and Yin (2005) turned it into an iterative regularization method for total variation imaging, and Yin, Osher, Goldfarb and Darbon (2008) used it for basis pursuit.
prereqs: [variational-regularization, bregman-divergence, subdifferential, total-variation-denoising]
see_also: [split-bregman-method, bregman-distance-convergence-rates, augmented-lagrangian-method, basis-pursuit, morozov-discrepancy-principle, semi-convergence, landweber-iteration, proximal-point-method]
sources:
  - paper: doi:10.1137/040605412
    title: Stanley Osher, Martin Burger, Donald Goldfarb, Jinjun Xu and Wotao Yin, An iterative regularization method for total variation-based image restoration, Multiscale Modeling and Simulation 4(2), 2005
    locator: pages 460 to 489
  - paper: doi:10.1016/0041-5553(67)90040-7
    title: L. M. Bregman, The relaxation method of finding the common point of convex sets and its application to the solution of problems in convex programming, USSR Computational Mathematics and Mathematical Physics 7(3), 1967
    locator: pages 200 to 217
  - paper: doi:10.1137/070703983
    title: Wotao Yin, Stanley Osher, Donald Goldfarb and Jerome Darbon, Bregman iterative algorithms for l1-minimization with applications to compressed sensing, SIAM Journal on Imaging Sciences 1(1), 2008
    locator: pages 143 to 168
  - paper: doi:10.1088/0266-5611/20/5/005
    title: Martin Burger and Stanley Osher, Convergence rates of convex variational regularization, Inverse Problems 20(5), 2004
    locator: pages 1411 to 1421
  - paper: doi:10.1137/080725891
    title: Tom Goldstein and Stanley Osher, The split Bregman method for L1-regularized problems, SIAM Journal on Imaging Sciences 2(2), 2009
    locator: pages 323 to 343
---

Bregman iteration improves a variational reconstruction by solving it several times. Each time it adds the part of the data that the last reconstruction did not explain back to the data, and solves again. For a regularizer $R$ and data $y = Ax + e$, step $k$ solves $\min_x \tfrac12\|Ax - y^k\|^2 + \lambda R(x)$ and then sets $y^{k+1} = y^k + (y - Ax^{k+1})$. This is the same as replacing $\lambda R(x)$ by its [Bregman divergence](/bregman-divergence/) from the last iterate, which is where the name comes from. For total variation the first step loses contrast, because shrinking a jump lowers the total variation, and the later steps give the contrast back. The residual $\|Ax^k - y\|$ never increases and tends to 0, so with noisy data the iteration must be stopped, for example by the [discrepancy principle](/morozov-discrepancy-principle/). With exact data and $\ell_1$ it ends at a [basis pursuit](/basis-pursuit/) solution.

## In plain words

A cleaning filter for images removes noise but also makes bright objects a little darker and dark objects a little brighter. The method fixes this with a simple loop. Clean the image. Look at what the cleaning removed. Most of that is noise, but some of it is real detail and real contrast. Add the removed part back to the measured image, and clean again. The real detail is now stronger and survives the cleaning, so the new result is closer to the truth. Each round explains more of the measurement. But the noise is also part of the measurement, so if the loop runs too long the noise comes back. The loop must stop when the result explains the measurement about as well as the noise level allows, and not better.

## The problem

The input is a linear forward operator $A$ (given as a routine), data $y \in \mathbb{R}^m$, a convex regularizer $R \ge 0$ with $R(0) = 0$, a weight $\lambda > 0$ and a routine that solves the inner variational problem

$$\operatorname{solve}(d) = \operatorname*{argmin}_x \tfrac12\|Ax - d\|^2 + \lambda R(x)$$

for any data vector $d$. With noisy data $y^\delta$ and a known noise level $\|y^\delta - Ax^\dagger\| \le \delta$, the input also has $\delta$ and a factor $\tau \ge 1$. The output is an approximation of the solution $x^\dagger$ that has small $R$ among the solutions of $Ax = y$. The weight $\lambda$ here is a design choice that sets the speed of the iteration rather than the final smoothing; the stop index plays the role of the regularization parameter.

## The algorithm

```pseudo id=main
BregmanIteration(solve, A, y, K, δ, τ)
L1  y⁰ ← y
L2  for k = 0 to K - 1
L3      x ← solve(yᵏ)                       ▷ argmin ½‖Ax - yᵏ‖² + λR(x)
L4      r ← y - A x                         ▷ what x does not explain
L5      if ‖r‖ ≤ τ δ then return x          ▷ discrepancy stop
L6      yᵏ⁺¹ ← yᵏ + r                       ▷ add the residual back
L7  return x
```

The optimality condition of line L3 at step $k+1$ is $A^\top(y^k - Ax^{k+1}) \in \lambda\,\partial R(x^{k+1})$. Line L6 turns this into $p^{k+1} = A^\top(y^{k+1} - y)/\lambda \in \partial R(x^{k+1})$, a [subgradient](/subdifferential/) of $R$ at the new iterate. With it, line L3 at the next step is the same problem as

$$x^{k+1} = \operatorname*{argmin}_x \tfrac12\|Ax - y\|^2 + \lambda D^{p^k}(x, x^k),\qquad D^{p}(x, z) = R(x) - R(z) - \langle p, x - z\rangle,$$

because $\tfrac12\|Ax - y^k\|^2 = \tfrac12\|Ax - y\|^2 - \lambda\langle p^k, x\rangle$ plus a constant. So each step regularizes by the distance to the last iterate in the geometry of $R$, not by $R$ itself. With exact data, line L6 is also the multiplier update of the [augmented Lagrangian method](/augmented-lagrangian-method/) for $\min R(x)$ subject to $Ax = y$, with multiplier $y^k - y$.

## Example

Take $A = I$, total variation on a signal, $\lambda = 1$ and the clean step $y = (0, 0, 0, 0, 2, 2, 2, 2)$.

Step 1 is [total variation denoising](/total-variation-denoising/) of $y$. Each half moves toward the other by $\lambda$ divided by its length 4, so $x^1 = (0.25, 0.25, 0.25, 0.25, 1.75, 1.75, 1.75, 1.75)$. The jump fell from 2 to 1.5: this is the contrast loss. The residual is $y - x^1 = (-0.25, \dots, 0.25, \dots)$, and line L6 gives $y^1 = (-0.25, -0.25, -0.25, -0.25, 2.25, 2.25, 2.25, 2.25)$, a step with the larger jump 2.5.

Step 2 denoises $y^1$. Again each half moves by $0.25$, so $x^2 = (0, 0, 0, 0, 2, 2, 2, 2) = y$. The contrast is fully restored after one extra step, and the residual is 0.

With $\ell_1$ in place of total variation and $A = I$, line L3 is soft thresholding at $\lambda = 1$. For $y = (3, 0.5, -2)$:

| $k$ | $y^k$ | $x^{k+1}$ | $\|x^{k+1} - y\|$ |
|---|---|---|---|
| 0 | $(3, 0.5, -2)$ | $(2, 0, -1)$ | 1.5 |
| 1 | $(4, 1, -3)$ | $(3, 0, -2)$ | 0.5 |
| 2 | $(4, 1.5, -3)$ | $(3, 0.5, -2)$ | 0 |

The two large entries are exact after step 2. The small entry $0.5$ is below the threshold, but its residual accumulates in $y^k$ and it enters at step 3. If $0.5$ is noise, step 3 lets the noise in, and a discrepancy stop with $\delta = 0.5$ ends the loop after step 2.

## Correctness

The full proofs are in [proofs/correctness.md](proofs/correctness.md). The theorems, for exact inner solves:

- The residual does not increase: $\|Ax^{k+1} - y\| \le \|Ax^k - y\|$ for $k \ge 1$, because $x^k$ is a candidate in the Bregman form of step $k+1$ with distance 0.
- Three-point identity: for every $\tilde x$, $D(\tilde x, x^k) - D(\tilde x, x^{k-1}) + D(x^k, x^{k-1}) = \langle p^k - p^{k-1}, x^k - \tilde x\rangle = \langle y - Ax^k, Ax^k - A\tilde x\rangle/\lambda$. With $2\langle a, b\rangle \le \|a\|^2 + \|b\|^2$ this gives $\lambda\big(D(\tilde x, x^k) - D(\tilde x, x^{k-1})\big) \le \tfrac12\|A\tilde x - y\|^2 - \tfrac12\|Ax^k - y\|^2$.
- Rate: summing over $k$ gives $\tfrac12\|Ax^K - y\|^2 \le \tfrac12\|A\tilde x - y\|^2 + \lambda R(\tilde x)/K$ for every $\tilde x$. With exact data and $\tilde x = x^\dagger$, the squared residual is $O(1/K)$.
- Noise: with $\|Ax^\dagger - y^\delta\| \le \delta$ and $\tilde x = x^\dagger$, the distance $D(x^\dagger, x^k)$ strictly decreases as long as $\|Ax^k - y^\delta\| > \delta$. So the iterates approach the true solution in the Bregman sense until the discrepancy reaches the noise level, which justifies the stop in line L5.
- Exact fit: if $Ax^k = y$ then $x^k$ minimizes $R$ over $\{x : Ax = y\}$, because $p^k = A^\top w$ with $w = (y^k - y)/\lambda$ is a subgradient. For $R = \|\cdot\|_1$ this is basis pursuit, and Yin, Osher, Goldfarb and Darbon (2008) show the exact fit is reached after finitely many steps.

## Complexity

Each outer step costs one inner solve and one product with $A$, plus $O(m)$ for the update, so $K$ steps cost $O(K(s + m))$ time and $O(m)$ extra memory for $y^k$. The inner solve dominates: for total variation it is itself an iterative method, such as [Chambolle's projection algorithm](/chambolle-projection-algorithm/) or the [Chambolle-Pock algorithm](/chambolle-pock-algorithm/). The squared residual is $O(1/K)$ by the rate above. With noise and a discrepancy stop, the number of outer steps depends on $\lambda$: a large $\lambda$ gives many small steps and a fine control of the stop, a small $\lambda$ gives few large steps.

## Properties

- The residual is monotone, and the Bregman distance to the true solution decreases until the noise level is reached. This is the same semi-convergence behavior as [Landweber iteration](/landweber-iteration/): the error first falls and then grows as noise is fitted.
- The method is an iterative regularization: the stop index, not $\lambda$, is the regularization parameter.
- For $R(x) = \tfrac12\|x\|^2$ the Bregman distance is $\tfrac12\|x - x^k\|^2$, and the method is iterated Tikhonov regularization.
- For exact data it is the augmented Lagrangian method (method of multipliers) for $\min R$ subject to $Ax = y$.
- The scale of features enters in order of size: large, high contrast features are recovered in the first steps, small and low contrast ones later. Noise is small scale, so it enters last.
- The iterates are not monotone in $R$ or in the error norm; only the residual and, before the stop, the Bregman distance are.

## Variants and improvements

- [Split Bregman](/split-bregman-method/) applies the same add-back step to the constraint $d = \Phi x$ of a split problem, which gives a fast method for $\ell_1$ and total variation problems. For linear constraints it is [ADMM](/admm/).
- Linearized Bregman: Yin, Osher, Goldfarb and Darbon (2008) replace the inner solve by one gradient step and a shrinkage, which gives a cheap method for basis pursuit. Cai, Osher and Shen (2009) showed that its limit solves $\min \|x\|_1 + \tfrac1{2\mu}\|x\|^2$ subject to $Ax = y$, where $\mu$ is the parameter of the method.
- Inverse scale space: letting $\lambda \to \infty$ with a time scaling gives a continuous flow $\partial_t p = A^\top(y - Ax)$, $p \in \partial R(x)$, studied by Burger, Gilboa, Osher and Xu (2006).
- Inexact inner solves: in practice the inner problem is solved only approximately, often with one sweep, which leads to split Bregman and ADMM.
- Other data terms: the Bregman form with $D^{p^k}$ works for any convex data term, for example the Kullback-Leibler divergence for Poisson data, but then the subgradient no longer has the simple form $A^\top(y^k - y)/\lambda$ and line L6 must be replaced by an explicit update of $p^k$.

## When to use it

Use it when a convex regularizer such as total variation or $\ell_1$ gives the right structure but loses contrast or shrinks large coefficients, and you can solve the variational problem as a black box. It is also a simple way to get the minimal $R$ solution of $Ax = y$ from a solver for the penalized problem. If you only need the penalized solution for one fixed $\lambda$, do not use it; use the inner solver once. With noisy data you need an estimate of the noise level or another stop rule.

## Pitfalls

- Without a stop rule the iteration fits the noise: the residual goes to 0 and the noise enters the reconstruction. With a noise level, stop at the first $k$ with $\|Ax^k - y^\delta\| \le \tau\delta$.
- The add-back must use the original data $y$, not the current $y^k$: line L4 is $y - Ax$. Using $y^k - Ax$ gives a different and divergent method.
- The rate and monotonicity need accurate inner solves. A very rough inner solve breaks the monotone residual, though the loop often still works in practice.
- The weight $\lambda$ changes meaning: here it sets the step size of the iteration. A small $\lambda$ makes each step fit the data almost fully, so the residual can already fall far below the noise level in the first step, and the stop rule then has nothing to choose.
- The subgradient $p^k$ is implicit in $y^k$. If the inner solver works with a different scaling of the data term, for example $\tfrac\mu2\|Ax - d\|^2 + R(x)$, the update must use the same scaling.

## Implementations

## History

Lev Bregman introduced his distance in 1967 together with a method for finding a point in the intersection of convex sets, and it became a standard tool of convex optimization. Osher, Burger, Goldfarb, Xu and Yin (2005) used it to build an iterative regularization method for total variation image restoration. They showed that adding back the residual cures the contrast loss of the Rudin-Osher-Fatemi model and proved the monotone residual and the decrease of the Bregman distance up to the noise level. Burger and Osher (2004) had already given convergence rates in Bregman distances for convex variational regularization. Yin, Osher, Goldfarb and Darbon (2008) applied the iteration to basis pursuit in compressed sensing and introduced linearized Bregman, and Goldstein and Osher (2009) combined it with a splitting to obtain the split Bregman method.

## References
