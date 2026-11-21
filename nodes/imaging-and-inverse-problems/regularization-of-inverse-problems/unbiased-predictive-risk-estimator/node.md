---
tag: FEKTYX
kind: algorithm
slug: unbiased-predictive-risk-estimator
name: Unbiased predictive risk estimator
aliases:
- UPRE
- Mallows C_L
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: advanced
summary: Choose the regularization parameter that minimizes an unbiased estimate of the expected predictive error, using a known noise variance.
solves: [regularization-parameter-choice]
model: real-ram
complexity:
  vars: {m: the number of measurements, n: the number of unknowns (n <= m), P: the number of grid points, K: the number of golden-section steps}
  time: {worst: Θ(m n + (P + K) n), average: Θ(m n + (P + K) n), best: Θ(m n + (P + K) n)}
  space: {extra: Θ(P + n)}
properties: {deterministic: true, a_posteriori: true, needs_noise_variance: true, unbiased_risk_estimate: true}
history:
  year: 1973
  people: [Colin L. Mallows]
  note: Mallows (1973) proposed C_L, an unbiased estimate of the prediction error of a linear smoother. Under the name UPRE it is a standard parameter choice rule for inverse problems, as in Vogel (2002).
prereqs: [regularization-parameter-choice, tikhonov-regularization, hat-matrix, stein-unbiased-risk-estimate]
see_also: [generalized-cross-validation, morozov-discrepancy-principle, l-curve-method, lepskii-balancing-principle, akaike-information-criterion, ridge-regression, golden-section-search, spectral-filter-factors]
sources:
  - paper: doi:10.1080/00401706.1973.10489103
    title: C. L. Mallows, Some comments on C_p, Technometrics 15(4), 1973
    locator: pages 661 to 675
  - paper: doi:10.1214/aos/1176345632
    title: Charles M. Stein, Estimation of the mean of a multivariate normal distribution, Annals of Statistics 9(6), 1981
    locator: pages 1135 to 1151
  - book: isbn:9780898715071
    title: Curtis R. Vogel, Computational Methods for Inverse Problems, SIAM, 2002
    locator: chapter 7 (regularization parameter selection methods)
---

The unbiased predictive risk estimator (UPRE) chooses the parameter of a linear regularization method when the noise is white with a known variance $\sigma^2$. The quantity it aims at is the predictive risk $T(\alpha) = \frac1mE\lVert Ax_\alpha - Ax^\dagger\rVert^2$, which depends on the unknown $x^\dagger$. For Tikhonov regularization with influence matrix $H_\alpha = A(A^TA + \alpha I)^{-1}A^T$, the function

$$U(\alpha) = \frac1m\lVert(I - H_\alpha)y\rVert^2 + \frac{2\sigma^2}{m}\mathrm{trace}(H_\alpha) - \sigma^2$$

is computable from the data and satisfies $E\,U(\alpha) = T(\alpha)$ for every $\alpha$. UPRE picks the minimizer of $U$. The residual term alone would always prefer small $\alpha$; the trace term charges $2\sigma^2/m$ for each effective parameter of the fit. Mallows (1973) introduced the estimate as $C_L$ for linear smoothers, and it is the special case of [Stein's unbiased risk estimate](/stein-unbiased-risk-estimate/) for the linear map $y \mapsto H_\alpha y$. The rule is a posteriori in the statistical sense: it needs $\sigma^2$ but not $x^\dagger$.

## In plain words

You want to know how much to smooth, and you know how noisy each measurement is. The best setting is the one whose result predicts the clean data best, but you cannot see the clean data. UPRE estimates that prediction error anyway. It takes the misfit to the noisy data, which is too optimistic because the fit has chased some of the noise, and adds a penalty for each degree of freedom the fit uses. On average the corrected number equals the true prediction error. Then it picks the setting with the smallest corrected number. It works well when the noise level you give it is right, and badly when it is not.

## The problem

The model is $y = Ax^\dagger + e$ with an $m \times n$ matrix $A$ and $e \sim N(0, \sigma^2I_m)$ with a known $\sigma$. The Tikhonov solution for $\alpha > 0$ is $x_\alpha = (A^TA + \alpha I)^{-1}A^Ty$, so $Ax_\alpha = H_\alpha y$. The page [Tikhonov regularization](/tikhonov-regularization/) writes $\lambda$ for this $\alpha$.

With the thin SVD $A = \sum_{i \le r} s_iu_iv_i^T$, $b_i = \langle u_i, y\rangle$, $p^2 = \lVert y\rVert^2 - \sum_i b_i^2$ and the [filter factors](/spectral-filter-factors/) $f_i = s_i^2/(s_i^2 + \alpha)$,

$$U(\alpha) = \frac1m\Big(\sum_i (1 - f_i)^2b_i^2 + p^2\Big) + \frac{2\sigma^2}{m}\sum_i f_i - \sigma^2.$$

The task is to find the $\alpha$ that minimizes $U$ on a search interval, by default $[s_r^2, s_1^2]$.

## The algorithm

The search is the same as for [GCV](/generalized-cross-validation/): a geometric grid in $t = \log\alpha$, then golden-section search between the neighbours of the best grid point.

```pseudo id=main
UPRE-TIKHONOV(U, s, V, y, sigma, P, eps)   ▷ thin SVD of A, s descending, r positive values
L1  b_i ← <u_i, y> for i ≤ r;  p² ← ‖y‖² - Σ b_i²
L2  G(t) := (Σ_i (1 - f_i)² b_i² + p²) / m + 2 sigma² Σ_i f_i / m - sigma²  with f_i = s_i² / (s_i² + e^t)
L3  t_j ← log s_r² + (j / (P - 1)) · (log s_1² - log s_r²) for j = 0, ..., P - 1
L4  j* ← the index of the smallest G(t_j)
L5  [a, c] ← [t_{j*-1}, t_{j*+1}]                 ▷ clipped at the ends of the grid
L6  while c - a > eps
L7      golden-section step on [a, c] that keeps the smaller G inside
L8      remember the best (t, G) seen so far
L9  alpha ← e^t for the best t
L10 return alpha, x = Σ_i s_i b_i / (s_i² + alpha) · v_i, and G at alpha
```

Line L1 projects the data on the left singular vectors. Line L2 is $U(\alpha)$ in SVD form, at a cost of $\Theta(r)$ per value. Lines L3 to L5 locate and bracket the smallest grid value. Lines L6 to L8 are a [golden-section search](/golden-section-search/) for a minimum, and line L8 keeps the best point, so the result is never worse than the best grid point. Line L10 forms the Tikhonov solution.

## Example

Take the same problem as on the GCV page: $A = \mathrm{diag}(s_1, \dots, s_{32})$ with $s_i = 1/i^2$, $x^\dagger_i = 1/i^2$, and $e_i = 10^{-3}g_i$ with $g_i$ from `random.Random(0).gauss(0, 1)`, so $\sigma = 10^{-3}$ and $p = 0$. The table compares $U$ with the true predictive risk $T$.

| $\alpha$ | $U(\alpha)$ | $T(\alpha)$ | $\lVert x_\alpha - x^\dagger\rVert$ | $\mathrm{trace}(H_\alpha)$ |
|---|---|---|---|---|
| $10^{-7}$ | $9.595 \times 10^{-7}$ | $9.585 \times 10^{-7}$ | 3.3560 | 31.32 |
| $10^{-6}$ | $7.951 \times 10^{-7}$ | $7.570 \times 10^{-7}$ | 2.2930 | 27.34 |
| $10^{-5}$ | $6.582 \times 10^{-7}$ | $4.463 \times 10^{-7}$ | 0.8043 | 18.32 |
| $10^{-4}$ | $6.220 \times 10^{-7}$ | $2.471 \times 10^{-7}$ | 0.1711 | 10.51 |
| $3 \times 10^{-4}$ | $5.780 \times 10^{-7}$ | $1.976 \times 10^{-7}$ | 0.0817 | 7.80 |
| $10^{-3}$ | $6.090 \times 10^{-7}$ | $2.615 \times 10^{-7}$ | 0.0583 | 5.74 |
| $3 \times 10^{-3}$ | $1.311 \times 10^{-6}$ | $1.036 \times 10^{-6}$ | 0.0684 | 4.18 |
| $10^{-2}$ | $6.818 \times 10^{-6}$ | $6.737 \times 10^{-6}$ | 0.0981 | 3.01 |
| $10^{-1}$ | $3.071 \times 10^{-4}$ | $3.088 \times 10^{-4}$ | 0.2224 | 1.48 |
| $1$ | $7.936 \times 10^{-3}$ | $7.926 \times 10^{-3}$ | 0.5697 | 0.58 |

For this draw of the noise, $U$ lies above $T$ by about $3.8 \times 10^{-7}$ in the middle of the range. Unbiasedness is a statement about the average over the noise, and one draw scatters around it, but the shape of $U$ near its minimum follows the shape of $T$.

Line L4 picks grid point 27, $\alpha = 5.427 \times 10^{-4}$, and line L5 brackets it by $4.29 \times 10^{-4}$ and $6.86 \times 10^{-4}$. The loop makes 28 steps with $\varepsilon = 10^{-6}$ and returns $\alpha = 5.0416 \times 10^{-4}$ with $U = 5.6956 \times 10^{-7}$. The predictive risk there is $1.983 \times 10^{-7}$, against the smallest possible $1.954 \times 10^{-7}$ at $\alpha \approx 3.98 \times 10^{-4}$. The error in $x$ is $0.06641$, against $0.05817$ at the best $\alpha$ for the error. The two optimal $\alpha$ differ because the predictive risk weights the error by the singular values.

## Correctness

The proof is in `proofs/correctness.md`. Line L2 computes $U$ by the SVD form of $H_\alpha$, the search terminates after $\lceil\log(w/\varepsilon)/\log 1.618\rceil$ golden-section steps for a bracket of width $w$, and the returned value is at most the smallest grid value.

The theorem behind the rule: for every fixed $\alpha$, $E\,U(\alpha) = T(\alpha)$. The proof is two lines. Write $y = g + e$ with $g = Ax^\dagger$. Then $E\lVert(I - H)y\rVert^2 = \lVert(I - H)g\rVert^2 + \sigma^2\mathrm{trace}((I - H)^2)$ and $mT = \lVert(I - H)g\rVert^2 + \sigma^2\mathrm{trace}(H^2)$. The difference is $\sigma^2(m - 2\,\mathrm{trace}(H))$, which is exactly what the last two terms of $U$ remove. The same identity is Stein's lemma for the linear map $y \mapsto H_\alpha y$, whose divergence is $\mathrm{trace}(H_\alpha)$. Only the first two moments of the noise are used, so the identity holds for any noise with mean zero and covariance $\sigma^2I$.

Unbiasedness at each fixed $\alpha$ does not make the minimizer of $U$ the minimizer of $T$. The minimizer depends on the noise, and its risk is a random quantity. Results on asymptotic optimality as $m \to \infty$ (Li 1987, for $C_L$ among others) need further conditions. In the tests, over 20 noise draws on a $64 \times 64$ problem, the risk at the UPRE choice was at most 1.3 times the smallest possible risk in the median and at most 3 times in the worst draw. That is a measurement.

## Complexity

With the thin SVD given, line L1 costs $\Theta(mn)$, each value of $U$ costs $\Theta(r) \subseteq O(n)$, the grid costs $\Theta(Pn)$, the loop $\Theta(Kn)$, and line L10 $\Theta(n^2) \subseteq O(mn)$. The total is $\Theta(mn + (P + K)n)$ with $\Theta(P + n)$ extra space. The SVD itself costs $O(mn^2)$ and dominates. Without an SVD, $\mathrm{trace}(H_\alpha)$ is estimated with random probe vectors, as for GCV.

## Properties

- Needs the noise variance $\sigma^2$ but not $x^\dagger$.
- Unbiased for the predictive risk at every fixed $\alpha$, for any noise with mean zero and covariance $\sigma^2I$.
- Scale free when $\sigma$ is scaled with the data: replacing $A$, $y$ and $\sigma$ by $cA$, $cy$ and $c\sigma$ multiplies the chosen $\alpha$ by $c^2$.
- Monotone in $\sigma$: a larger $\sigma$ puts more weight on the trace, which decreases in $\alpha$, so the minimizer does not move toward smaller $\alpha$.
- The same estimate works for any linear method $x = R_\alpha y$ with fitted data $AR_\alpha y$: replace $H_\alpha$ by $AR_\alpha$.

## Variants and improvements

- **Truncated SVD.** With $k$ terms, $\mathrm{trace}(H_k) = k$ and $U(k) = \frac1m\lVert y - H_ky\rVert^2 + 2\sigma^2k/m - \sigma^2$. This is Mallows' $C_p$ up to scaling, and the implementation includes it.
- **SURE for nonlinear estimators.** For a nonlinear map $y \mapsto g(y)$, such as soft thresholding of wavelet coefficients, replace $\mathrm{trace}(H)$ by the divergence of $g$. See [Stein's unbiased risk estimate](/stein-unbiased-risk-estimate/).
- **Error in x instead of in the data.** The risk $E\lVert x_\alpha - x^\dagger\rVert^2$ has no unbiased estimate in general when $A$ is ill-conditioned. A projected risk, $E\lVert P(x_\alpha - x^\dagger)\rVert^2$ with $P$ the projector on the range of $A^T$, can be estimated, but with a large variance.
- **Colored noise.** With noise covariance $\Sigma$, whiten first: replace $A$ and $y$ by $\Sigma^{-1/2}A$ and $\Sigma^{-1/2}y$, and use $\sigma = 1$.
- **Unknown variance.** Replace $\sigma^2$ by an estimate, for example from the residual of a fit with a small $\alpha$. Then the rule is close to [GCV](/generalized-cross-validation/), which removes $\sigma^2$ from the problem altogether.

## When to use it

Use it when the noise is white or can be whitened and its variance is known well, for example from the physics of a detector. It is then usually more accurate than the [discrepancy principle](/morozov-discrepancy-principle/), which uses only the size of the noise and tends to over-smooth, and more reliable than [GCV](/generalized-cross-validation/) on small problems. If only a deterministic bound $\lVert e\rVert \le \delta$ is known, use the discrepancy principle or the [balancing principle](/lepskii-balancing-principle/) instead, which have proofs in that setting.

## Pitfalls

- A wrong $\sigma$. In the example, $\sigma = 0.5 \times 10^{-3}$ instead of $10^{-3}$ makes line L4 pick the lower end of the interval, $\alpha = 9.5 \times 10^{-7}$, with an error of $2.33$, forty times the best. Overestimating is safer: $\sigma = 2 \times 10^{-3}$ gives $\alpha = 1.31 \times 10^{-3}$ and error $0.0585$. Check where the result lies in the interval.
- Using $\delta^2 = E\lVert e\rVert^2 = m\sigma^2$ in place of $\sigma^2$ in line L2, or the reverse. The formula wants the variance of one component.
- Forgetting the factor 2 on the trace term in line L2. Without it, the estimate is biased and the rule under-smooths.
- Correlated noise used as if it were white. The trace correction is then wrong, and the rule usually under-smooths. Whiten first.
- Minimizing $U$ when it is very flat. The minimum value of $U$ can be negative for one noise draw, which is fine, but a flat $U$ makes the choice sensitive to the noise. Plot it.

## Implementations

## History

Mallows (1973) gave $C_p$ for subset selection in regression and $C_L$ for general linear estimators, both unbiased estimates of the prediction error. Stein (1981) extended the idea to nonlinear, weakly differentiable estimators. Under the name unbiased predictive risk estimator the rule entered the inverse problems literature, where Vogel (2002) treats it next to GCV and the discrepancy principle for Tikhonov and iterative methods. Li (1987) proved asymptotic optimality results for $C_L$ and GCV.

## References
