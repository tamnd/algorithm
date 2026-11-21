---
tag: W03DNM
kind: algorithm
slug: l-curve-method
name: L-curve method
aliases:
- L-curve criterion
- L-curve corner rule
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: core
summary: Plot the log solution norm against the log residual norm over the parameter and choose the parameter at the corner of maximum curvature.
solves: [regularization-parameter-choice]
model: real-ram
complexity:
  vars: {m: the number of measurements, n: the number of unknowns (n <= m), P: the number of grid points, K: the number of golden-section steps}
  time: {worst: Θ(m n + (P + K) n), average: Θ(m n + (P + K) n), best: Θ(m n + (P + K) n)}
  space: {extra: Θ(P + n)}
properties: {deterministic: true, heuristic: true, needs_noise_level: false, convergent_regularization: false}
history:
  year: 1992
  people: [Per Christian Hansen, Dianne P. O'Leary, Charles L. Lawson, Richard J. Hanson]
  note: Lawson and Hanson (1974) already plotted the solution norm against the residual norm. Hansen (1992) analyzed the log-log curve, and Hansen and O'Leary (1993) proposed the corner of maximum curvature as the rule.
prereqs: [regularization-parameter-choice, tikhonov-regularization, singular-value-decomposition]
see_also: [generalized-cross-validation, morozov-discrepancy-principle, quasi-optimality-criterion, bakushinskii-veto, golden-section-search, spectral-filter-factors, hybrid-krylov-regularization, truncated-svd]
sources:
  - paper: doi:10.1137/1034115
    title: Per Christian Hansen, Analysis of discrete ill-posed problems by means of the L-curve, SIAM Review 34(4), 1992
    locator: pages 561 to 580
  - paper: doi:10.1137/0914086
    title: Per Christian Hansen and Dianne P. O'Leary, The use of the L-curve in the regularization of discrete ill-posed problems, SIAM Journal on Scientific Computing 14(6), 1993
    locator: pages 1487 to 1503
  - paper: doi:10.1007/BF01731984
    title: Martin Hanke, Limitations of the L-curve method in ill-posed problems, BIT 36(2), 1996
    locator: pages 287 to 301
  - paper: doi:10.1088/0266-5611/12/4/013
    title: Curtis R. Vogel, Non-convergence of the L-curve regularization parameter selection method, Inverse Problems 12(4), 1996
    locator: pages 535 to 547
  - book: isbn:9780898716962
    title: Per Christian Hansen, Discrete Inverse Problems, Insight and Algorithms, SIAM, 2010
    locator: chapter 5 (choosing the regularization parameter)
---

The L-curve method chooses the parameter of Tikhonov regularization from the data alone. For each $\alpha > 0$ it takes the point $(\log\lVert Ax_\alpha - y\rVert, \log\lVert x_\alpha\rVert)$. As $\alpha$ runs from large to small, the residual falls and the solution norm grows, and for many discrete ill-posed problems the curve has the shape of the letter L. On the flat part, the solution is over-smoothed: a smaller $\alpha$ buys a much smaller residual at little cost in norm. On the steep part, the solution fits noise: a smaller $\alpha$ makes the norm explode for almost no gain in residual. The rule takes the corner between the two, defined as the point of largest curvature. Hansen and O'Leary proposed it in 1993, after Hansen's 1992 analysis of the curve. It needs neither the noise level nor the noise variance, so it is a heuristic rule. By the [Bakushinskii veto](/bakushinskii-veto/) no such rule can converge for every problem, and Hanke and Vogel gave explicit examples where the L-curve choice does not converge. In practice it is robust to correlated noise and easy to inspect by eye.

## In plain words

A smoothing method has a knob. For each setting you can measure two numbers: how far the result is from the data, and how wild the result is. Draw these two numbers against each other on log scales, one point per setting. For many problems you get an L. Along one arm, turning the knob makes the result much closer to the data and only a little wilder. Along the other arm, it makes the result much wilder and only a little closer. The best compromise sits at the bend. The method finds the bend as the point where the curve turns most sharply. It does not need to know how much noise there is, which is its strength, and it can be fooled, which is its weakness.

## The problem

The model is $y = Ax^\dagger + e$ with an $m \times n$ matrix $A$ and unknown noise $e$. The Tikhonov solution for $\alpha > 0$ is

$$x_\alpha = \arg\min_x \lVert Ax - y\rVert^2 + \alpha\lVert x\rVert^2 = (A^TA + \alpha I)^{-1}A^Ty.$$

The page [Tikhonov regularization](/tikhonov-regularization/) writes $\lambda$ for this $\alpha$. With the thin SVD $A = \sum_{i \le r} s_iu_iv_i^T$, $b_i = \langle u_i, y\rangle$ and $p^2 = \lVert y\rVert^2 - \sum_i b_i^2$, write

$$\eta(\alpha) = \lVert x_\alpha\rVert^2 = \sum_i \frac{s_i^2b_i^2}{(s_i^2 + \alpha)^2}, \qquad \rho(\alpha) = \lVert Ax_\alpha - y\rVert^2 = \sum_i \frac{\alpha^2b_i^2}{(s_i^2 + \alpha)^2} + p^2.$$

The L-curve is the plane curve $\alpha \mapsto (\tfrac12\log\rho, \tfrac12\log\eta)$. Its signed curvature is

$$\kappa(\alpha) = -\frac{2\eta\rho\,(\alpha\eta'\rho + \alpha^2\eta'\eta + \eta\rho)}{\eta'\,(\alpha^2\eta^2 + \rho^2)^{3/2}}, \qquad \eta'(\alpha) = -2\sum_i \frac{s_i^2b_i^2}{(s_i^2 + \alpha)^3}.$$

It is positive where the curve turns like the corner of an L. The task is to find the $\alpha$ that maximizes $\kappa$ on a search interval, by default $[s_r^2, s_1^2]$.

## The algorithm

The search works in $t = \log\alpha$. A coarse geometric grid finds the region of the largest curvature, and golden-section search refines the maximum between the two grid neighbours.

```pseudo id=main
L-CURVE-CORNER(U, s, V, y, P, eps)        ▷ thin SVD of A, s descending, r positive values
L1  b_i ← <u_i, y> for i ≤ r;  p² ← ‖y‖² - Σ b_i²
L2  t_j ← log s_r² + (j / (P - 1)) · (log s_1² - log s_r²) for j = 0, ..., P - 1
L3  k_j ← κ(e^{t_j}) for every j                     ▷ η, ρ, η' from b, p² in Θ(r)
L4  j* ← the index of the largest k_j
L5  [a, c] ← [t_{j*-1}, t_{j*+1}]                     ▷ clipped at the ends of the grid
L6  while c - a > eps
L7      golden-section step on [a, c] that keeps the larger κ inside
L8      remember the best (t, κ) seen so far
L9  alpha ← e^t for the best t
L10 return alpha, x = Σ_i s_i b_i / (s_i² + alpha) · v_i, and its curvature
```

Line L1 projects the data on the left singular vectors. After that, every value of $\eta$, $\rho$ and $\eta'$ costs $\Theta(r)$, so line L3 is cheap even with a fine grid. Line L4 picks the grid point of largest curvature, and line L5 brackets it by its neighbours. Lines L6 to L8 are a [golden-section search](/golden-section-search/) for a maximum: each step evaluates $\kappa$ once and shrinks the bracket by the factor $0.618$. Line L8 keeps the best point, so the result is never worse than the best grid point. Line L10 forms the Tikhonov solution from the SVD.

## Example

Take the test problem deriv2 with $n = m = 24$: $A$ is the discretized Green's function of $-u''$ on $[0, 1]$ with zero boundary values, at the midpoints $t_i = (i - \frac12)/24$, with entries $h\,t_i(t_j - 1)$ for $t_i < t_j$ and $h = 1/24$. The true solution has two bumps, $x^\dagger_j = e^{-80(t_j - 0.3)^2} + 0.6\,e^{-80(t_j - 0.7)^2}$, and $\lVert x^\dagger\rVert = 2.1402$. The noise is Gaussian from `random.Random(0)`, scaled so that $\lVert e\rVert = 0.1\lVert Ax^\dagger\rVert = 0.01754$. The singular values run from $s_1 = 0.101466$ to $s_{24} = 4.34 \times 10^{-4}$, and $p = 0$ because $A$ is square and invertible.

| $\alpha$ | $\lVert Ax_\alpha - y\rVert$ | $\lVert x_\alpha\rVert$ | $\kappa$ | $\lVert x_\alpha - x^\dagger\rVert$ |
|---|---|---|---|---|
| $10^{-7}$ | 0.00404 | 21.3866 | -0.3935 | 21.2693 |
| $10^{-6}$ | 0.01186 | 7.4657 | -0.3572 | 7.1273 |
| $10^{-5}$ | 0.01590 | 2.4850 | 0.2798 | 1.3985 |
| $3.16 \times 10^{-5}$ | 0.01694 | 2.0287 | 2.1954 | 0.8312 |
| $10^{-4}$ | 0.01799 | 1.8573 | 4.4166 | 0.9049 |
| $3.16 \times 10^{-4}$ | 0.02001 | 1.7423 | 1.4294 | 1.0462 |
| $10^{-3}$ | 0.02638 | 1.5990 | 0.0332 | 1.1602 |
| $10^{-2}$ | 0.08996 | 0.8802 | -0.6814 | 1.5090 |
| $10^{-1}$ | 0.16138 | 0.1619 | -0.1089 | 2.0110 |

Read the table from the bottom up. From $\alpha = 0.1$ to $10^{-3}$ the residual falls by a factor of 6 and the norm grows by a factor of 10. From $10^{-5}$ to $10^{-7}$ the residual falls by a factor of 4 and the norm grows by a factor of 9. In between, from $10^{-3}$ to $10^{-5}$, the residual barely moves and the norm grows slowly: that is the corner. The curvature is negative on both arms, where the log-log curve bends the other way.

Line L2 uses the default interval $[s_{24}^2, s_1^2] = [1.88 \times 10^{-7}, 0.0103]$ with $P = 60$ points, so neighbouring grid points are $0.1849$ apart in $\log\alpha$. Line L4 picks grid point 33, $\alpha = 8.4117 \times 10^{-5}$ with $\kappa = 4.4985$, and line L5 brackets it by $6.99 \times 10^{-5}$ and $1.012 \times 10^{-4}$. With $\varepsilon = 10^{-6}$ the golden-section loop makes 27 steps and returns $\alpha = 8.5477 \times 10^{-5}$ with $\kappa = 4.4994$, residual $0.01782$ and $\lVert x_\alpha\rVert = 1.8749$. The error is $\lVert x_\alpha - x^\dagger\rVert = 0.8850$. On a fine grid the smallest error is $0.8215$, at $\alpha \approx 3.98 \times 10^{-5}$, so the corner costs 8 percent here. For comparison, the [discrepancy principle](/morozov-discrepancy-principle/) with the true $\delta$ and $\tau = 1$ gives $\alpha = 6.42 \times 10^{-5}$ and error $0.8517$. The residual at the corner, $0.01782$, is close to $\delta$, which is what the rule hopes for when it has no $\delta$.

## Correctness

The proof is in `proofs/correctness.md`. It shows three things. First, $\eta$ is strictly decreasing and $\rho$ is strictly increasing in $\alpha$ when some $s_ib_i \ne 0$, and $\rho' = -\alpha\eta'$, so the L-curve is a graph that runs from upper left to lower right. Second, the closed form of $\kappa$ above is the signed curvature of the curve $(\frac12\log\rho, \frac12\log\eta)$: the second derivative $\eta''$ cancels out of the numerator once $\rho' = -\alpha\eta'$ and $\rho'' = -\eta' - \alpha\eta''$ are substituted. The curvature of a plane curve does not depend on the parameter, so computing it in $\alpha$ or in $t = \log\alpha$ gives the same value. Third, the search terminates after $\lceil\log(w/\varepsilon)/\log(1/0.618)\rceil$ golden-section steps, where $w$ is the width of the initial bracket, and returns a point whose curvature is at least the largest curvature on the grid. If $\kappa$ is unimodal on the bracket, the result is within $\varepsilon$ of the local maximum in $\log\alpha$.

None of this says that the corner gives a good $\alpha$. That claim is a heuristic. For a solution that satisfies the discrete Picard condition and noise that is not too small, Hansen (1992) explains why the curve has a corner near the $\alpha$ where the noise starts to dominate the solution. There is no theorem that it converges, and there are proofs that it does not in some settings (see Pitfalls).

## Complexity

With the thin SVD given, line L1 costs $\Theta(mn)$. Each curvature value costs $\Theta(r) \subseteq O(n)$, so line L3 costs $\Theta(Pn)$ and the loop costs $\Theta(Kn)$ for $K$ golden-section steps. Line L10 costs $\Theta(n^2) \subseteq O(mn)$. The total is $\Theta(mn + (P + K)n)$ with $\Theta(P + n)$ extra space. The bracket has width $w = 2\log(s_1^2/s_r^2)/(P - 1)$, and $K = \lceil\log(w/\varepsilon)/\log 1.618\rceil$. In the example $w = 0.370$, $\varepsilon = 10^{-6}$ and $K = 27$. The SVD itself costs $O(mn^2)$ by a standard dense method and dominates. Without an SVD, each point of the curve needs one Tikhonov solve and $\eta'$ needs one more solve, so large problems use a few points of the curve and a Krylov method, as in [hybrid Krylov regularization](/hybrid-krylov-regularization/).

## Properties

- Heuristic: it uses only $A$ and $y$, not $\delta$ or $\sigma$.
- Not convergent in general. By the [Bakushinskii veto](/bakushinskii-veto/), a rule that ignores the noise level cannot converge for every $x^\dagger$ and every noise sequence.
- Scale free: replacing $A$ and $y$ by $cA$ and $cy$ multiplies the chosen $\alpha$ by $c^2$ and leaves $x_\alpha$ and $\kappa$ unchanged, because a scaling of $\rho$ and $\eta$ is a shift of the log-log curve.
- The curvature is a property of the curve and not of the parameter. The same corner is found in $\alpha$, $\log\alpha$ or $\sqrt\alpha$.
- The corner need not exist. On mildly ill-posed problems the curve can be convex the wrong way everywhere, and then line L4 returns the least negative curvature, which is not a corner (see Pitfalls).

## Variants and improvements

- **Discrete L-curve.** For [truncated SVD](/truncated-svd/), CGLS or other methods with a discrete parameter the curve is a set of points. Hansen, Jensen and Rodriguez (2007) choose the corner by an adaptive pruning of the points. A simpler choice is the point of largest angle change.
- **Triangle and maximum distance rules.** Pick the point farthest from the line through the two ends of the curve. This needs no derivatives.
- **Krylov approximations.** Calvetti, Golub and Reichel (1999) bound the curve with Gauss quadrature from Lanczos bidiagonalization, the L-ribbon, so the corner can be found without the SVD.
- **General form.** With a penalty $\alpha\lVert Lx\rVert^2$ the vertical axis becomes $\log\lVert Lx_\alpha\rVert$. The same formulas hold with the generalized SVD of $(A, L)$.
- **Other heuristic rules.** [GCV](/generalized-cross-validation/) and the [quasi-optimality criterion](/quasi-optimality-criterion/) also work without $\delta$. They fail in different situations, so computing two of them is a cheap check.

## When to use it

Use it when the noise level is unknown, the problem is severely ill-posed and the noise is not tiny, and you want a picture that a person can check. It is a good first rule in exploratory work because the plot shows at once whether the problem has a clear corner. If $\delta$ is known, use the [discrepancy principle](/morozov-discrepancy-principle/) or the [balancing principle](/lepskii-balancing-principle/), which have proofs. If the noise is white with known variance, use [UPRE](/unbiased-predictive-risk-estimator/). For large white-noise problems, [GCV](/generalized-cross-validation/) is often more accurate.

## Pitfalls

- A curve with no corner. For a mildly ill-posed problem, such as a $16 \times 16$ integration matrix with $1$ percent noise, the curvature is negative on the whole interval. Line L4 still returns a point. Check that the returned $\kappa$ is positive and look at the plot.
- Smooth solutions and small noise. Hanke (1996) showed in a model problem that the L-curve choice does not converge in the right way when the true solution is very smooth. Vogel (1996) showed that the chosen parameter does not converge as the discretization is refined in a statistical setting. Treat the rule as a heuristic, not as a regularization method.
- A grid that is too coarse in line L2. The peak of $\kappa$ can be narrow, and a coarse grid can miss it and lock line L5 onto a second, smaller local maximum. With $P = 60$ on $[s_r^2, s_1^2]$ this rarely happens, but more points cost little.
- A search interval that is too narrow or too wide. Below $s_r^2$ the curve is nearly a straight line and can have spurious bends caused by rounding. Above $s_1^2$ the curvature is near zero. The default $[s_r^2, s_1^2]$ in line L2 avoids both.
- Using the plain norms instead of their logarithms. The corner is a feature of the log-log plot. In linear scales the curvature formula and the maximum are different.
- Computing the curvature with finite differences of the plotted points instead of the closed form in line L3. The second differences lose many digits when the points are close, and $\eta'$ is available exactly.

## Implementations

## History

Lawson and Hanson (1974) plotted the solution norm against the residual norm to choose a truncation level. Hansen (1992) studied the curve in log-log scale for discrete ill-posed problems and explained its L shape from the SVD and the Picard condition. Hansen and O'Leary (1993) turned the picture into a rule, the corner of maximum curvature, and gave the curvature formula in terms of $\eta$, $\rho$ and $\eta'$. Hanke (1996) and Vogel (1996) showed limits of the rule: it is not convergent in general. It remains one of the most used heuristic rules, mainly because the plot is easy to read.

## References
