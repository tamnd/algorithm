---
tag: 7S65BE
kind: algorithm
slug: generalized-cross-validation
name: Generalized cross-validation
aliases:
- GCV
- GCV criterion
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: core
summary: "Choose the parameter that minimizes V, which is (1/m) times the squared residual norm divided by the square of (1/m) trace(I minus the influence matrix). It needs no noise level."
solves: [regularization-parameter-choice]
model: real-ram
complexity:
  vars: {m: the number of measurements, n: the number of unknowns (n <= m), P: the number of grid points, K: the number of golden-section steps}
  time: {worst: Θ(m n + (P + K) n), average: Θ(m n + (P + K) n), best: Θ(m n + (P + K) n)}
  space: {extra: Θ(P + n)}
properties: {deterministic: true, heuristic: true, needs_noise_level: false, rotation_invariant: true, convergent_regularization: false}
history:
  year: 1979
  people: [Peter Craven, Grace Wahba, Gene H. Golub, Michael Heath]
  note: Craven and Wahba proposed GCV for smoothing splines, and Golub, Heath and Wahba studied it for ridge regression. Both papers appeared in 1979.
prereqs: [regularization-parameter-choice, tikhonov-regularization, hat-matrix, cross-validation, singular-value-decomposition]
see_also: [unbiased-predictive-risk-estimator, stein-unbiased-risk-estimate, l-curve-method, quasi-optimality-criterion, morozov-discrepancy-principle, ridge-regression, golden-section-search, bakushinskii-veto]
sources:
  - paper: doi:10.1007/BF01404567
    title: Peter Craven and Grace Wahba, Smoothing noisy data with spline functions, Numerische Mathematik 31(4), 1979
    locator: pages 377 to 403
  - paper: doi:10.1080/00401706.1979.10489751
    title: Gene H. Golub, Michael Heath and Grace Wahba, Generalized cross-validation as a method for choosing a good ridge parameter, Technometrics 21(2), 1979
    locator: pages 215 to 223
  - book: isbn:9780898715071
    title: Curtis R. Vogel, Computational Methods for Inverse Problems, SIAM, 2002
    locator: chapter 7 (regularization parameter selection methods)
  - book: isbn:9780898716962
    title: Per Christian Hansen, Discrete Inverse Problems, Insight and Algorithms, SIAM, 2010
    locator: chapter 5 (choosing the regularization parameter)
---

Generalized cross-validation (GCV) chooses the parameter of a linear regularization method from the data alone. For Tikhonov regularization the fitted data are $Ax_\alpha = H_\alpha y$ with the influence matrix $H_\alpha = A(A^TA + \alpha I)^{-1}A^T$. GCV minimizes

$$V(\alpha) = \frac{\frac1m\lVert(I - H_\alpha)y\rVert^2}{\big[\frac1m\,\mathrm{trace}(I - H_\alpha)\big]^2},$$

the mean squared residual divided by the square of the mean of the diagonal of $I - H_\alpha$. The idea comes from leave-one-out [cross-validation](/cross-validation/): predict each measurement from the others and pick the $\alpha$ with the smallest prediction error. GCV is the version of this that does not change when the data space is rotated. Craven and Wahba (1979) introduced it for smoothing splines and Golub, Heath and Wahba (1979) for ridge regression. It needs neither the noise level $\delta$ nor the variance $\sigma^2$, so it is a heuristic rule in the sense of the [Bakushinskii veto](/bakushinskii-veto/). For white noise, Golub, Heath and Wahba proved that $E\,V(\alpha) - \sigma^2$ is close to the predictive risk when the effective number of parameters is a small part of $m$, which explains why it works well on large problems.

## In plain words

You want to know how much to smooth, but you do not know how noisy the data are. Cross-validation answers this by testing: hide one measurement, fit the rest, and see how well the fit predicts the hidden value. Repeat for every measurement and add up the misses. Too little smoothing fits the noise and predicts badly. Too much smoothing misses real structure and also predicts badly. GCV is a fast shortcut for this test. It divides the misfit by a factor that grows when the fit uses many degrees of freedom. Then it picks the knob setting with the smallest value. It needs no noise estimate, but on small or square problems it can pick far too little smoothing.

## The problem

The model is $y = Ax^\dagger + e$ with an $m \times n$ matrix $A$, $m \ge n$, and noise $e$. GCV is designed for white noise, $e \sim N(0, \sigma^2I_m)$ with unknown $\sigma$, but the algorithm does not use $\sigma$. The Tikhonov solution for $\alpha > 0$ is $x_\alpha = (A^TA + \alpha I)^{-1}A^Ty$. The page [Tikhonov regularization](/tikhonov-regularization/) writes $\lambda$ for this $\alpha$, and the page [hat matrix](/hat-matrix/) treats $H_\alpha$ in least squares, where $\alpha = 0$.

With the thin SVD $A = \sum_{i \le r} s_iu_iv_i^T$, $b_i = \langle u_i, y\rangle$, $p^2 = \lVert y\rVert^2 - \sum_i b_i^2$ and the [filter factors](/spectral-filter-factors/) $f_i = s_i^2/(s_i^2 + \alpha)$,

$$\lVert(I - H_\alpha)y\rVert^2 = \sum_i (1 - f_i)^2b_i^2 + p^2, \qquad \mathrm{trace}(I - H_\alpha) = m - \sum_i f_i.$$

The sum $\mathrm{trace}(H_\alpha) = \sum_i f_i$ is the effective number of parameters of the fit. The task is to find the $\alpha$ that minimizes $V$ on a search interval, by default $[s_r^2, s_1^2]$.

## The algorithm

The search works in $t = \log\alpha$. A coarse geometric grid finds the region of the smallest $V$, and golden-section search refines the minimum between the two grid neighbours.

```pseudo id=main
GCV-TIKHONOV(U, s, V, y, P, eps)       ▷ thin SVD of A, s descending, r positive values
L1  b_i ← <u_i, y> for i ≤ r;  p² ← ‖y‖² - Σ b_i²
L2  G(t) := m (Σ_i (1 - f_i)² b_i² + p²) / (m - Σ_i f_i)² with f_i = s_i² / (s_i² + e^t)
L3  t_j ← log s_r² + (j / (P - 1)) · (log s_1² - log s_r²) for j = 0, ..., P - 1
L4  j* ← the index of the smallest G(t_j)
L5  [a, c] ← [t_{j*-1}, t_{j*+1}]                 ▷ clipped at the ends of the grid
L6  while c - a > eps
L7      golden-section step on [a, c] that keeps the smaller G inside
L8      remember the best (t, G) seen so far
L9  alpha ← e^t for the best t
L10 return alpha, x = Σ_i s_i b_i / (s_i² + alpha) · v_i, and G at alpha
```

Line L1 projects the data on the left singular vectors. Line L2 is $V(\alpha)$ written with the SVD; the factors $1/m$ cancel into one factor $m$. Each value costs $\Theta(r)$. Lines L3 and L4 locate the smallest value on a grid, and line L5 brackets it. Lines L6 to L8 are a [golden-section search](/golden-section-search/) for a minimum, with one evaluation per step. Line L8 keeps the best point, so the result is never worse than the best grid point. Line L10 forms the Tikhonov solution.

## Example

Take $A = \mathrm{diag}(s_1, \dots, s_{32})$ with $s_i = 1/i^2$, so $U = V = I$, the true solution $x^\dagger_i = 1/i^2$, and white noise $e_i = 10^{-3}g_i$ with $g_i$ drawn by `random.Random(0).gauss(0, 1)`. Then $\lVert e\rVert = 0.006508$ and $p = 0$. The table shows $V$, the predictive risk $T(\alpha) = \frac1mE\lVert Ax_\alpha - Ax^\dagger\rVert^2$, the error for this draw of the noise, and $\mathrm{trace}(H_\alpha)$.

| $\alpha$ | $V(\alpha)$ | $T(\alpha)$ | $\lVert x_\alpha - x^\dagger\rVert$ | $\mathrm{trace}(H_\alpha)$ |
|---|---|---|---|---|
| $10^{-7}$ | $4.883 \times 10^{-6}$ | $9.585 \times 10^{-7}$ | 3.3560 | 31.32 |
| $10^{-6}$ | $4.068 \times 10^{-6}$ | $7.570 \times 10^{-7}$ | 2.2930 | 27.34 |
| $10^{-5}$ | $2.808 \times 10^{-6}$ | $4.463 \times 10^{-7}$ | 0.8043 | 18.32 |
| $10^{-4}$ | $2.140 \times 10^{-6}$ | $2.471 \times 10^{-7}$ | 0.1711 | 10.51 |
| $3 \times 10^{-4}$ | $1.907 \times 10^{-6}$ | $1.976 \times 10^{-7}$ | 0.0817 | 7.80 |
| $10^{-3}$ | $1.856 \times 10^{-6}$ | $2.615 \times 10^{-7}$ | 0.0583 | 5.74 |
| $3 \times 10^{-3}$ | $2.712 \times 10^{-6}$ | $1.036 \times 10^{-6}$ | 0.0684 | 4.18 |
| $10^{-2}$ | $9.297 \times 10^{-6}$ | $6.737 \times 10^{-6}$ | 0.0981 | 3.01 |
| $10^{-1}$ | $3.386 \times 10^{-4}$ | $3.088 \times 10^{-4}$ | 0.2224 | 1.48 |
| $1$ | $8.231 \times 10^{-3}$ | $7.926 \times 10^{-3}$ | 0.5697 | 0.58 |

Line L3 uses $[s_{32}^2, s_1^2] = [9.54 \times 10^{-7}, 1]$ with $P = 60$, a step of $0.235$ in $\log\alpha$. Line L4 picks grid point 28, $\alpha = 6.865 \times 10^{-4}$ with $V = 1.8346 \times 10^{-6}$, and line L5 brackets it by $5.43 \times 10^{-4}$ and $8.68 \times 10^{-4}$. With $\varepsilon = 10^{-6}$ the loop makes 28 steps and returns $\alpha = 7.0867 \times 10^{-4}$ with $V = 1.83444 \times 10^{-6}$. The error is $0.06056$, against $0.05817$ for the best $\alpha$ on a fine grid, at $1.10 \times 10^{-3}$. The predictive risk at the GCV choice is $2.162 \times 10^{-7}$, against the smallest possible $1.954 \times 10^{-7}$. At this $\alpha$ the value $V = 1.83 \times 10^{-6}$ is not close to $\sigma^2 + T = 1.22 \times 10^{-6}$: here $\mathrm{trace}(H_\alpha)/m \approx 0.2$ is not small, and the theorem in Correctness gives only a loose bound. The minimizer is still good.

With the noise from seed 2 instead of seed 0, the same code returns the lower end $\alpha = s_{32}^2$, with an error 25 times the best. See Pitfalls.

## Correctness

The proof is in `proofs/correctness.md`. It has three parts.

The first part shows that line L2 computes $V(\alpha)$: in the SVD basis $H_\alpha$ is diagonal with entries $f_i$ on the range of $A$ and $0$ on its orthogonal complement. The second part shows that the loop terminates after $\lceil\log(w/\varepsilon)/\log 1.618\rceil$ steps, where $w$ is the width of the bracket, and returns a value of $V$ at most the smallest grid value.

The third part is the theorem behind the rule, by Golub, Heath and Wahba (1979, Theorem 1). Let $e \sim N(0, \sigma^2I)$, let $T(\alpha) = \frac1mE\lVert H_\alpha y - Ax^\dagger\rVert^2$ be the predictive risk, and let $\mu_1 = \frac1m\mathrm{trace}(H_\alpha)$ and $\mu_2 = \frac1m\mathrm{trace}(H_\alpha^2)$. Then

$$\frac{|E\,V(\alpha) - \sigma^2 - T(\alpha)|}{T(\alpha)} \le \frac{2\mu_1 + \mu_1^2/\mu_2}{(1 - \mu_1)^2}.$$

So when the fit uses few effective parameters compared with $m$, the expected GCV function is the predictive risk plus a constant, and its minimizer is close to the minimizer of the risk. This is a statement about expectations. It does not bound the error of the minimizer of $V$ for one draw of the noise, and it is about the predictive risk $\lVert A(x_\alpha - x^\dagger)\rVert$, not about the error $\lVert x_\alpha - x^\dagger\rVert$. Results by Li (1987) show asymptotic optimality of the GCV choice for the predictive risk as $m \to \infty$ under conditions. In the deterministic setting with $\lVert e\rVert \le \delta$, GCV is not a convergent rule.

## Complexity

With the thin SVD given, line L1 costs $\Theta(mn)$, each value of $G$ costs $\Theta(r) \subseteq O(n)$, the grid costs $\Theta(Pn)$, the loop $\Theta(Kn)$, and line L10 $\Theta(n^2) \subseteq O(mn)$. The total is $\Theta(mn + (P + K)n)$ with $\Theta(P + n)$ extra space, and $K = \lceil\log(w/\varepsilon)/\log 1.618\rceil$ with $w = 2\log(s_1^2/s_r^2)/(P - 1)$. The SVD costs $O(mn^2)$ and dominates. For large problems without an SVD the trace is the hard part: it is estimated with random vectors $z$ through $E\,z^TH_\alpha z = \mathrm{trace}(H_\alpha)$ (Hutchinson, Girard), or from the Lanczos bidiagonalization of a Krylov method.

## Properties

- Heuristic: it uses only $A$ and $y$, not $\delta$ or $\sigma$.
- Rotation invariant: replacing $A$ and $y$ by $QA$ and $Qy$ for an orthogonal $Q$ leaves $V$ unchanged. Ordinary leave-one-out cross-validation does not have this property.
- Scale free: replacing $A$ and $y$ by $cA$ and $cy$ multiplies the chosen $\alpha$ by $c^2$.
- Targets the predictive risk $\frac1m\lVert A(x_\alpha - x^\dagger)\rVert^2$, which weights the error by the singular values. The error in $x$ can prefer a somewhat larger $\alpha$.
- With $\mathrm{trace}(I - H_\alpha) \to 0$ as $\alpha \to 0$ for a square invertible $A$, $V$ has a finite limit at $0$ that can be below the interior minimum.

## Variants and improvements

- **Truncated SVD.** For [truncated SVD](/truncated-svd/) with $k$ terms the filter factors are $1$ and $0$, so $\mathrm{trace}(I - H_k) = m - k$ and $G(k) = m\lVert y - H_ky\rVert^2/(m - k)^2$, minimized over $k < m$. The implementation includes this rule.
- **Ordinary cross-validation.** Leave-one-out minimizes $\frac1m\sum_k ((y - H_\alpha y)_k/(1 - (H_\alpha)_{kk}))^2$. GCV replaces each $1 - (H_\alpha)_{kk}$ by their mean.
- **Weighted GCV.** Chung, Nagy and O'Leary (2008) multiply the trace term by a weight $\omega$ to make GCV choose larger $\alpha$ in hybrid Krylov methods, where plain GCV often under-regularizes.
- **Randomized trace.** For large sparse problems, estimate $\mathrm{trace}(H_\alpha)$ with a few random vectors.
- **Known variance.** If $\sigma^2$ is known, [UPRE](/unbiased-predictive-risk-estimator/) estimates the same risk without bias, and the [discrepancy principle](/morozov-discrepancy-principle/) gives a convergent rule.

## When to use it

Use it for white noise of unknown variance, when $m$ is large compared with the effective number of parameters, for example in image deblurring, spline smoothing or [ridge regression](/ridge-regression/). It is often the most accurate of the rules that need no noise level. On small or square problems, or with correlated noise, also compute the [L-curve](/l-curve-method/) or the [quasi-optimality criterion](/quasi-optimality-criterion/), and look at a plot of $V$: a very flat minimum or a minimum at the lower end of the interval is a warning.

## Pitfalls

- The minimum at the lower end. For a square invertible $A$ the residual and $\mathrm{trace}(I - H_\alpha)$ both go to zero as $\alpha \to 0$, and $V$ tends to a finite value that can be the smallest one. In the example with seed 2, line L4 picks the first grid point. Check whether the result sits at the end of the interval of line L3.
- Correlated noise. The theory assumes white noise. With correlated noise GCV often under-smooths, sometimes badly. Whiten the data first if the covariance is known.
- A flat $V$. Near its minimum, $V$ can be very flat, so a small change of the data moves $\alpha$ by a large factor. The variance of the GCV choice is known to be large on small problems.
- Dropping the square in the denominator of line L2, or dropping the factor $m$, changes the minimizer. The two factors $1/m$ in the definition do not cancel out of the ratio; they leave the factor $m$.
- Using $\mathrm{trace}(H_\alpha)$ instead of $\mathrm{trace}(I - H_\alpha)$, or forgetting the $m - r$ part of the trace when $m > n$. The trace of $I - H_\alpha$ is $m - \sum_i f_i$, not $r - \sum_i f_i$.
- Using $p^2$ from rounding. If $A$ is square, $p^2$ should be $0$ but can come out slightly negative or positive; line L1 clamps it at $0$.

## Implementations

## History

Wahba (1977) used cross-validation to choose the parameter in the regularized solution of linear operator equations. Craven and Wahba (1979) defined generalized cross-validation for smoothing splines and studied how well it estimates the predictive risk for large $m$. Golub, Heath and Wahba (1979) studied it for ridge regression and gave the bound on the expected GCV function. Li (1986, 1987) proved asymptotic optimality under general conditions. Wahba's 1990 monograph on spline models made it standard in statistics, and Vogel (2002) and Hansen (2010) describe its use for inverse problems.

## References
