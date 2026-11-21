---
tag: 6BGG92
kind: algorithm
slug: morozov-discrepancy-principle
name: Morozov discrepancy principle
aliases:
- discrepancy principle
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: core
summary: Choose the regularization parameter so that the residual norm equals tau times the known noise level, for a fixed tau a little above 1.
solves: [regularization-parameter-choice]
model: real-ram
complexity:
  vars: {m: the number of measurements, n: the number of unknowns (n <= m), K: "the number of root-finding steps once the thin SVD of A is known"}
  time: {worst: Θ(m n + K n), average: Θ(m n + K n), best: Θ(m n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, iterative: true, a_posteriori: true, needs_noise_level: true, convergent_regularization: true}
history:
  year: 1966
  people: [Vladimir A. Morozov]
  note: Morozov (1966) proposed to fit the data only up to the noise level. Phillips (1962) had used the same idea without a proof. The theory for Tikhonov and iterative methods is in Engl, Hanke and Neubauer (1996).
prereqs: [regularization-parameter-choice, tikhonov-regularization, singular-value-decomposition]
see_also: [l-curve-method, generalized-cross-validation, lepskii-balancing-principle, unbiased-predictive-risk-estimator, bakushinskii-veto, landweber-iteration, truncated-svd, newton-bisection-hybrid]
sources:
  - paper: "V. A. Morozov, On the solution of functional equations by the method of regularization, Soviet Math. Dokl. 7 (1966)"
    title: V. A. Morozov, On the solution of functional equations by the method of regularization, Soviet Mathematics Doklady 7, 1966
    locator: pages 414 to 417
  - book: isbn:9780792341574
    title: Heinz W. Engl, Martin Hanke and Andreas Neubauer, Regularization of Inverse Problems, Kluwer, 1996
    locator: chapter 4 (a posteriori parameter choice and the discrepancy principle) and chapter 5 (Tikhonov regularization); the discrete rule for iterative methods in chapters 6 and 7
  - book: isbn:9780898716962
    title: Per Christian Hansen, Discrete Inverse Problems, Insight and Algorithms, SIAM, 2010
    locator: chapter 5 (choosing the regularization parameter)
---

The discrepancy principle chooses the parameter of a regularization method from the noise level. If the data $y^\delta$ differ from the exact data by at most $\delta$ in norm, there is no reason to fit them more closely than $\delta$. So the rule takes the parameter $\alpha$ at which the residual $\lVert Ax_\alpha - y^\delta\rVert$ equals $\tau\delta$, for a fixed safety factor $\tau \ge 1$, often $\tau$ between $1.01$ and $1.5$. V. A. Morozov stated and analyzed it in 1966. It is an a posteriori rule: it uses both $\delta$ and $y^\delta$. For [Tikhonov regularization](/tikhonov-regularization/) it is a proved rule. The chosen solution converges to the true solution as $\delta \to 0$, and under the source condition $x^\dagger = A^\ast w$ the error is $O(\delta^{1/2})$. It needs a reliable $\delta$. With a wrong $\delta$ it over-smooths or under-smooths in proportion, and without any $\delta$ the [Bakushinskii veto](/bakushinskii-veto/) says that no rule can be convergent in the worst case. For iterative methods such as [Landweber](/landweber-iteration/) the same principle is a stopping rule: stop at the first $k$ with residual at most $\tau\delta$.

## In plain words

Your measurements contain noise, and you know roughly how big the noise is. A smoothing method has a knob. Turn it down and the result follows the data more closely, noise included. Turn it up and the result becomes smoother and follows the data less. The rule says: do not follow the data more closely than the noise allows. Turn the knob until the gap between the data and what the result predicts is as large as the noise, and stop there. Anything closer means that you are fitting the noise. Anything looser throws away real information. The rule is simple and has a proof behind it, but it only works if your estimate of the noise size is good.

## The problem

The model is $y^\delta = Ax^\dagger + e$ with $\lVert e\rVert \le \delta$ and a known $\delta$. Here $A$ is an $m \times n$ matrix and $x^\dagger$ is the minimum norm solution of $Ax = y$ for the exact data $y = Ax^\dagger$. The Tikhonov solution for $\alpha > 0$ is

$$x_\alpha = \arg\min_x \lVert Ax - y^\delta\rVert^2 + \alpha\lVert x\rVert^2 = (A^TA + \alpha I)^{-1}A^Ty^\delta.$$

The page [Tikhonov regularization](/tikhonov-regularization/) writes $\lambda$ for this $\alpha$. The task is to find $\alpha$ with

$$\lVert Ax_\alpha - y^\delta\rVert = \tau\delta.$$

With the thin SVD $A = \sum_i s_iu_iv_i^T$ and $b_i = \langle u_i, y^\delta\rangle$, the squared residual is $\rho(\alpha) = \sum_i (\alpha/(s_i^2 + \alpha))^2 b_i^2 + p^2$. Here $p$ is the norm of the part of $y^\delta$ outside the range of $A$. The function $\rho$ is continuous and increasing, from $p^2$ at $\alpha \to 0$ to $\lVert y^\delta\rVert^2$ at $\alpha \to \infty$. So a root exists and is unique when $p < \tau\delta < \lVert y^\delta\rVert$.

## The algorithm

The search works in $t = \log\alpha$, where the residual changes on a scale that does not depend on the size of $\alpha$. It is a safeguarded Newton method: a Newton step from the better end of a bracket, replaced by a bisection step on every second pass or when it leaves the bracket.

```pseudo id=main
DISCREPANCY-TIKHONOV(U, s, V, y, delta, tau, eps)     ▷ thin SVD of A, s descending, r positive values
L1  b_i ← <u_i, y> for i ≤ r;  p² ← ‖y‖² - Σ b_i²       ▷ p: norm of y outside the range
L2  if p ≥ tau·delta then return FAIL                   ▷ no alpha reaches the target
L3  if ‖y‖ ≤ tau·delta then return (∞, 0)               ▷ x = 0 already fits the data
L4  F(t) := Σ_i (e^t / (s_i² + e^t))² b_i² + p² - tau² delta²   ▷ increasing in t
L5  hi ← log(s_1² q / (1 - q)) with q = (1 + tau·delta/‖y‖) / 2
L6  lo ← log(s_r² · sqrt((tau² delta² - p²) / 2) / ‖y‖)
L7  for k = 0, 1, 2, ...
L8      c ← the end of [lo, hi] with the smaller |F|
L9      if hi - lo ≤ eps or |F(c)| ≤ eps · F'(c) then exit the loop
L10     t ← c - F(c) / F'(c); if k is odd or t ∉ (lo, hi) then t ← (lo + hi) / 2
L11     if F(t) > 0 then hi ← t else lo ← t
L12 alpha ← e^c
L13 return alpha, x = Σ_i s_i b_i / (s_i² + alpha) · v_i
```

Line L1 projects the data on the left singular vectors. Lines L2 and L3 handle the two cases where the equation has no root: the target is below the smallest reachable residual, or above the largest. Line L4 defines the function whose root is wanted. Its derivative is $F'(t) = 2\sum_i \alpha^2 s_i^2 b_i^2/(s_i^2 + \alpha)^3$ with $\alpha = e^t$, so each evaluation costs $\Theta(r)$. Lines L5 and L6 give a bracket from two simple bounds, proved in `proofs/correctness.md`. At $\alpha_{hi}$ the largest filter factor is so small that the residual exceeds $q\lVert y\rVert > \tau\delta$. At $\alpha_{lo}$ even the smallest singular value is so much larger than $\alpha$ that the residual is below $\tau\delta$. Lines L8 to L11 shrink the bracket. Line L10 takes the Newton point, but uses the midpoint on every second pass, and when the Newton point is not strictly inside the bracket. Line L13 forms the Tikhonov solution from the SVD.

## Example

Take $A = \mathrm{diag}(1, 0.1, 0.01)$, so $U = V = I$, the true solution $x^\dagger = (1, 1, 0.5)$, and the noise $e = (0, 0.03, 0.04)$ with $\lVert e\rVert = \delta = 0.05$. The data are $y^\delta = (1, 0.13, 0.045)$. With $\tau = 1.2$ the target residual is $0.06$. Line L1 gives $b = y^\delta$ and $p = 0$, and $\lVert y^\delta\rVert = 1.009418$. Line L5 gives $q = 0.529720$ and $\alpha_{hi} = 1.126$, with residual $0.5470$. Line L6 gives $\alpha_{lo} = 4.203 \times 10^{-6}$, with residual $0.001816$. With $\varepsilon = 10^{-10}$ the loop runs as follows:

| pass | step | $t$ | $\alpha$ | residual | lo | hi |
|---|---|---|---|---|---|---|
| 1 | bisection (Newton point outside) | -6.1303 | 0.002176 | 0.04894 | -6.1303 | 0.1190 |
| 2 | bisection | -3.0057 | 0.04951 | 0.12625 | -6.1303 | -3.0057 |
| 3 | Newton | -4.9923 | 0.006790 | 0.06911 | -6.1303 | -4.9923 |
| 4 | bisection | -5.5613 | 0.003844 | 0.05693 | -5.5613 | -4.9923 |
| 5 | Newton | -5.3827 | 0.004596 | 0.06030 | -5.5613 | -5.3827 |
| 6 | bisection | -5.4720 | 0.004203 | 0.05856 | -5.4720 | -5.3827 |
| 7 | Newton | -5.3975 | 0.004528 | 0.06000 | -5.4720 | -5.3975 |
| 8 | bisection | -5.4348 | 0.004362 | 0.05927 | -5.4348 | -5.3975 |
| 9 | Newton | -5.3977 | 0.004527 | 0.06000 | -5.4348 | -5.3977 |
| 10 | bisection | -5.4162 | 0.004444 | 0.05963 | -5.4162 | -5.3977 |
| 11 | Newton | -5.3977 | 0.004527 | 0.06000 | -5.4162 | -5.3977 |

After pass 11 the test of line L9 holds, and the rule returns $\alpha = 0.0045272$ and $x_\alpha = (0.99549, 0.89487, 0.09725)$, with error $\lVert x_\alpha - x^\dagger\rVert = 0.4163$. On a fine grid of $\alpha$ the smallest error is $0.1990$, at $\alpha \approx 8.9 \times 10^{-4}$. With $\tau = 1$ the rule gives $\alpha = 0.0023897$ and error $0.3230$. The third component is the hard one: $s_3x^\dagger_3 = 0.005$ is far below the noise $0.04$ in that component, and every reasonable rule damps it.

## Correctness

The proof is in `proofs/correctness.md`. It has two parts.

The first part is about the algorithm. The residual is continuous and strictly increasing in $\alpha$, so the equation has exactly one root when $p < \tau\delta < \lVert y^\delta\rVert$. Lines L5 and L6 give $F(\mathrm{lo}) < 0 < F(\mathrm{hi})$, and line L11 keeps the signs, so the root stays in the bracket. On exit, $|\lVert Ax_\alpha - y^\delta\rVert^2 - \tau^2\delta^2| \le \frac{8}{27}\lVert y^\delta\rVert^2\varepsilon$, because $0 \le F' \le \frac{8}{27}\lVert y^\delta\rVert^2$. Under the noise model, $p = \lVert P^\perp e\rVert \le \delta$, so line L2 never fails when $\tau > 1$.

The second part is the theorem that makes the rule a regularization method. Let $\tau \ge 1$ and let $\alpha$ solve the discrepancy equation. Then $\lVert x_\alpha\rVert \le \lVert x^\dagger\rVert$ and $\lVert Ax_\alpha - y\rVert \le (1 + \tau)\delta$. From these two bounds and a weak compactness argument, $x_\alpha \to x^\dagger$ as $\delta \to 0$. If $x^\dagger = A^\ast w$, then

$$\lVert x_\alpha - x^\dagger\rVert \le \sqrt{2(1 + \tau)\lVert w\rVert\delta}.$$

This holds in any Hilbert space, not only for matrices. EHN show more generally that Tikhonov with the discrepancy principle is order optimal under $x^\dagger = (A^\ast A)^\nu w$ for $0 < \nu \le 1/2$, and that the rate $O(\delta^{1/2})$ is the best this combination can give, however smooth $x^\dagger$ is (EHN chapters 4 and 5).

## Complexity

In the real-RAM model with the thin SVD given, line L1 costs $\Theta(mn)$, each pass of the loop costs $\Theta(n)$ for one evaluation of $F$ and $F'$, and line L13 costs $\Theta(n^2)$, which is at most $\Theta(mn)$. The total is $\Theta(mn + Kn)$, with $\Theta(n)$ extra space. The bracket has width $W = \log(\alpha_{hi}/\alpha_{lo})$, which grows like $\log(s_1^2/s_r^2)$ plus the logarithm of the signal-to-noise ratio, and the loop makes at most $K \le 2\lceil\log_2(W/\varepsilon)\rceil$ passes, because the width halves at least once in every two passes. In the example, $W = 12.5$ and $\varepsilon = 10^{-10}$ give the bound $74$, and the loop needed $11$. The SVD itself costs $O(mn^2)$ by a standard dense method and dominates.

Without an SVD, each evaluation of the residual needs a new Tikhonov solve, for example by [CGLS](/cgls/) with the shift $\alpha$. Then a root finder that needs few evaluations, such as the [secant method](/secant-method/) in $\log\alpha$, matters more than the cost of each step.

## Properties

- A posteriori: it needs $\delta$ and $y^\delta$, not $x^\dagger$.
- Convergent for Tikhonov with $\tau \ge 1$ when the root exists; the existence argument needs $\tau > 1$ unless $y^\delta$ has no part outside the range.
- Order optimal for Tikhonov only up to $\nu = 1/2$. The a priori choice $\alpha \sim \delta^{2/(2\nu+1)}$ reaches $O(\delta^{2/3})$ at $\nu = 1$, the discrepancy principle does not.
- Scale free: replacing $A$, $y^\delta$ and $\delta$ by $cA$, $cy^\delta$ and $c\delta$ multiplies the chosen $\alpha$ by $c^2$ and gives the same $x$.
- The chosen $\alpha$ grows with $\tau\delta$, because the residual is increasing in $\alpha$. So a loose upper bound $\delta$ gives a too large $\alpha$ and an over-smoothed solution.

## Variants and improvements

- **Discrete rule for iterative methods.** For [Landweber](/landweber-iteration/), [CGLS](/cgls/) or [truncated SVD](/truncated-svd/), stop at the first index $k$ with $\lVert Ax_k - y^\delta\rVert \le \tau\delta$. For Landweber this gives order optimal rates for all $\nu > 0$ when $\tau$ is large enough (EHN chapter 6 states the condition on $\tau$). For CG it is the standard stopping rule (EHN chapter 7).
- **Statistical noise.** If $e \sim N(0, \sigma^2 I_m)$, then $E\lVert e\rVert^2 = m\sigma^2$, and the rule is often used with $\delta = \sqrt m\,\sigma$. A variant targets $\lVert Ax_\alpha - y\rVert^2 = \sigma^2\,\mathrm{trace}(I - H_\alpha)$, which accounts for the degrees of freedom used by the fit.
- **Modified discrepancy principles.** Engl (1987) and Gfrerer (1987) compare a smoothed residual with the noise level, for example $\alpha^3\langle (AA^\ast + \alpha I)^{-3}y^\delta, y^\delta\rangle = c\,\delta^2$, and so make Tikhonov order optimal up to $\nu = 1$. EHN treat these rules next to the plain principle.
- **Other root finders.** Newton in $\alpha$ itself, the secant method in $\log\alpha$, or [Brent's method](/brent-method/). As a function of $\beta = 1/\alpha$ the squared residual is a sum of terms $b_i^2/(1 + \beta s_i^2)^2$ plus a constant, so it is convex and decreasing, and Newton in $\beta$ converges monotonically from any $\beta$ below the root.
- **Nonlinear problems.** The same equation is used for nonlinear Tikhonov and as the stopping rule of the iteratively regularized Gauss-Newton method.

## When to use it

Use it when the noise level is known or can be estimated well: from the physics of the detector, from repeated measurements, or from the high frequency part of the data. It is the default a posteriori rule in the theory of regularization, and the natural stopping rule for iterative methods. When only the noise variance of white noise is known, [UPRE](/unbiased-predictive-risk-estimator/) uses the same information in a statistically sharper way. When $\delta$ is unknown, use a heuristic rule such as [GCV](/generalized-cross-validation/), the [L-curve](/l-curve-method/) or the [quasi-optimality criterion](/quasi-optimality-criterion/), and accept that it can fail. The [balancing principle](/lepskii-balancing-principle/) also uses $\delta$ and adapts to the smoothness of $x^\dagger$ without the saturation at $\nu = 1/2$.

## Pitfalls

- A wrong $\delta$ is the main failure. If $\delta$ is too small, line L2 can fail, or the root moves toward zero and the noise blows up. If it is too large, line L3 returns $x = 0$ or the solution is over-smoothed.
- With $\tau = 1$ and $p = \delta$ exactly, line L2 fails although the noise model holds. Use $\tau > 1$.
- Searching in $\alpha$ instead of $\log\alpha$ (lines L5 to L11) makes the bracket span many orders of magnitude, and plain bisection in $\alpha$ wastes most steps near the large end.
- An unsafeguarded Newton step in line L10 can jump far outside the bracket when started far from the root, as pass 1 of the example shows. Keep the bracket.
- The test $|F(c)| \le \varepsilon F'(c)$ in line L9 compares squared residuals. If $\lVert y\rVert$ is huge compared with $\tau\delta$, scale the data first, or the absolute tolerance hides a large relative error in the residual.
- In the discrete rule for iterative methods, comparing the residual with $\delta$ instead of $\tau\delta$ with $\tau > 1$ can make the iteration run far too long when the residual stalls just above $\delta$.

## Implementations

## History

D. L. Phillips (1962) chose the smoothing parameter of his method by matching the residual to the expected error, without a proof. V. A. Morozov (1966) made the rule precise and proved that it gives a convergent method for Tikhonov regularization. Later work found the rates, the saturation at $O(\delta^{1/2})$ and the modified rules of Engl (1987) and Gfrerer (1987), and Engl, Hanke and Neubauer (1996) put the discrepancy principle, its discrete form for iterative methods and its variants into one framework.

## References
