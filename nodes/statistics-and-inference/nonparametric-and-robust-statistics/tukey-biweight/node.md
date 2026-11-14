---
tag: 9NDW0S
kind: algorithm
slug: tukey-biweight
name: Tukey's biweight
aliases:
- Tukey bisquare
- bisquare estimator
area: statistics-and-inference/nonparametric-and-robust-statistics
level: core
summary: A redescending M-estimator whose psi function goes to zero beyond a threshold, so gross outliers get no weight. Fitted by iteratively reweighted least squares.
model: real-ram
complexity:
  vars: {n: the sample size, t: the number of reweighting steps}
  time: {worst: Θ(n log n + n t), average: Θ(n log n + n t), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, randomized: false, exact_in_exact_arithmetic: false, in_place: false, online: false}
history:
  year: 1974
  people: [Albert E. Beaton, John W. Tukey]
  note: Beaton and Tukey introduced the biweight in 1974 to fit polynomials to band-spectroscopic data with outliers. Holland and Welsch studied its reweighting algorithm in 1977.
prereqs: [huber-m-estimator, m-estimator, median-absolute-deviation, influence-function]
see_also: [mm-estimator, iteratively-reweighted-least-squares, breakdown-point, trimmed-mean, least-trimmed-squares, robust-model-fitting, ransac, median]
sources:
  - paper: doi:10.1080/00401706.1974.10489171
    title: Albert E. Beaton and John W. Tukey, The fitting of power series, meaning polynomials, illustrated on band-spectroscopic data, Technometrics 16(2), 1974
    locator: pp. 147 to 185 (the biweight weight function and its use in reweighted fits)
  - paper: doi:10.1080/03610927708827533
    title: Paul W. Holland and Roy E. Welsch, Robust regression using iteratively reweighted least-squares, Communications in Statistics, Theory and Methods 6(9), 1977
    locator: pp. 813 to 827 (iteratively reweighted least squares with the bisquare and other weight functions)
  - book: isbn:9781119214687
    title: Ricardo A. Maronna, R. Douglas Martin, Victor J. Yohai and Matías Salibián-Barrera, Robust Statistics, Theory and Methods (with R), second edition, Wiley, 2019
    locator: Chapter 2 (redescending M-estimators of location, the bisquare, the choice of c and the reweighting algorithm)
  - book: isbn:9780471829218
    title: Frank R. Hampel, Elvezio M. Ronchetti, Peter J. Rousseeuw and Werner A. Stahel, Robust Statistics, The Approach Based on Influence Functions, Wiley, 1986
    locator: Chapter 2 (redescending estimators and the rejection point)
---

Tukey's biweight is the [M-estimator](/m-estimator/) of location with the loss $\rho_c(u) = \frac{c^2}{6}\bigl[1 - (1 - (u/c)^2)^3\bigr]$ for $|u| \le c$ and $\rho_c(u) = c^2/6$ beyond. Its derivative $\psi_c(u) = u(1 - (u/c)^2)^2$ rises, falls back, and is exactly 0 for $|u| \ge c$. So a point farther than $c\hat\sigma$ from the estimate has no influence at all. The loss is not convex, so the estimate is computed by iteratively reweighted means from a robust start, the [median](/median/), with the scale fixed at the normalized [MAD](/median-absolute-deviation/). Each step does not increase the objective. With $c = 4.685$ the efficiency at the normal is 95%.

## In plain words

Each point gets a weight between 0 and 1. A point near the current center gets a weight close to 1. A point farther away gets a smaller weight, and a point beyond a cutoff gets weight 0. The new center is the weighted average of the points. Then the weights are computed again for the new center, and so on until the center stops moving. A point far from the bulk of the data is not only weakened, it is ignored. The cutoff is a number of typical spreads, measured with a robust spread.

## The problem

The input is a sample $x_1, \ldots, x_n$, a constant $c > \Phi^{-1}(3/4) \approx 0.6745$ (the default is $c = 4.685$) and a tolerance. The scale is $\hat\sigma = \mathrm{MAD}/\Phi^{-1}(3/4)$. The target is a local minimizer of
$$Q(\theta) = \sum_{i=1}^n \rho_c\!\left(\frac{x_i - \theta}{\hat\sigma}\right),$$
that is a root of $\sum_i \psi_c((x_i - \theta)/\hat\sigma) = 0$, reached from the median. The output is the point where the iteration stops. $Q$ can have several local minima, and the method does not promise the global one.

## The algorithm

The weight function is $w_c(u) = \psi_c(u)/u = (1 - (u/c)^2)^2$ for $|u| < c$ and 0 otherwise.

```pseudo id=main
BIWEIGHT(x, c, tol)                       ▷ x[1 .. n]
L1  θ ← median(x); σ ← MAD(x)/Φ⁻¹(3/4); if σ = 0 then return θ
L2  repeat
L3      r_i ← (x_i − θ)/σ for each i
L4      w_i ← (1 − (r_i/c)²)² if |r_i| < c, else 0
L5      θ' ← Σ w_i x_i / Σ w_i
L6      if |θ' − θ| ≤ tol · σ then return θ'
L7      θ ← θ'
```

A fixed point of lines L3 to L5 satisfies $\sum_i w_i (x_i - \theta) = 0$, which is $\hat\sigma \sum_i \psi_c(r_i) = 0$. So the method stops near a root of the estimating equation.

## Example

Take $x = (2, 4, 5, 6, 7, 30)$ and $c = 4.685$. The median is $5.5$. The absolute deviations are $(3.5, 1.5, 0.5, 0.5, 1.5, 24.5)$, so the MAD is $1.5$ and $\hat\sigma = 1.5/0.6745 = 2.2239$. Then $c\hat\sigma = 10.42$, and the point 30 is beyond the cutoff from the start.

| step | $\theta$ | weights of $(2, 4, 5, 6, 7, 30)$ | $Q(\theta)$ | $\sum \psi_c$ |
|---|---|---|---|---|
| 0 | 5.5 | 0.787, 0.959, 0.995, 0.995, 0.959, 0 | 5.2582 | $-1.2387$ |
| 1 | 4.9134 | 0.850, 0.985, 1.000, 0.978, 0.921, 0 | 5.0762 | $-0.1361$ |
| 2 | 4.8494 | | 5.0741 | |
| 3 | 4.8425 | | 5.0740 | |

The iteration stops after 13 steps at $\hat\theta = 4.8416$, with $|\sum \psi_c| < 10^{-12}$. It is the mean of the first five points weighted almost equally. The value 30 has no effect: moving it to $10^9$ gives the same result. The mean is 9 and the median is $5.5$.

## Correctness

Two facts make the iteration safe, and `proofs/correctness.md` proves both. First, $\rho_c(u) = g(u^2)$ with $g$ concave and nondecreasing on $[0, \infty)$, and $w_c(u) = 2g'(u^2)$. A concave function lies below its tangent, so $Q$ lies below a weighted sum of squares that touches it at the current $\theta$. Line L5 minimizes that sum of squares. So $Q(\theta') \le Q(\theta)$, with equality only when $\theta' = \theta$. Second, the sum of the weights in line L5 is never 0. At the median, at least half of the points are within one MAD, that is within $\Phi^{-1}(3/4)\,\hat\sigma < c\hat\sigma$, so $Q$ at the start is less than $nc^2/6$. If all weights were 0 at a later step, $Q$ would be $nc^2/6$ there, against the descent. The proof also shows that every limit point of the iterates is a root of the estimating equation.

## Complexity

- **Time.** The median and the MAD take $\Theta(n \log n)$ by sorting, or expected $\Theta(n)$ with [quickselect](/quickselect/). Each step takes $\Theta(n)$. So the total is $\Theta(n \log n + nt)$ for $t$ steps.
- **Steps.** The convergence is linear in general. The rate depends on the data: when almost all points have weight near 1, it is fast, and in the example the step length drops by about a factor 9 each step. No bound on $t$ in terms of $n$ alone holds.
- **Space.** $\Theta(n)$ for the weights.

## Properties

The page proves the descent, the positive weights, and the bounded estimate for far outliers. The efficiency and the influence function are computed. The rest is cited.

- **Influence function.** At the normal law with the scale fixed, $\mathrm{IF}(x) = \sigma\psi_c((x - \mu)/\sigma)/\mathrm E\psi_c'(Z)$. It is 0 for $|x - \mu| \ge c\sigma$: the rejection point is $c\sigma$. The largest value of $\psi_c$ is at $u = c/\sqrt5$, and with $c = 4.685$ the standardized gross-error sensitivity is $1.770$, against $1.637$ for the [Huber estimator](/huber-m-estimator/) at 95% efficiency.
- **Efficiency at the normal.** The asymptotic variance is $\mathrm E\psi_c(Z)^2/(\mathrm E\psi_c'(Z))^2$ with $\psi_c'(u) = (1 - (u/c)^2)(1 - 5(u/c)^2)$ inside. A numerical integration gives 1.0526 for $c = 4.685$, an efficiency of 0.950.
- **Far outliers are ignored (proved).** Let $c_1$ and $c_2$ be the least and the greatest clean point, and let $m < n/2$ points be replaced by values farther than $c\hat\sigma$ from $[c_1, c_2]$. The median $\theta_0$ is in $[c_1, c_2]$, because more than half the points are clean. If $\theta_t \in [c_1, c_2]$, every replaced point has weight 0, so $\theta_{t+1}$ is a weighted mean of clean points and is in $[c_1, c_2]$. So all iterates stay in $[c_1, c_2]$. The MAD of the sample is at most $c_2 - c_1$ (the argument is on the [Huber estimator](/huber-m-estimator/) page), so the condition holds when the replaced points are far enough. The tests move up to $\lceil n/2 \rceil - 1$ points to $10^6$ and $10^{12}$ and measure that the estimate stays in $[c_1, c_2]$; at $\lceil n/2 \rceil$ points it follows them.
- **Not convex.** $Q$ is bounded, so it can have several local minima, for example one near each of two clusters. The root found depends on the start. This page does not prove a breakdown point for arbitrary replacements; for the global minimizer and for regression, see the cited books.
- **Equivariance.** With the median start and the MAD scale, the computed estimate is location and scale equivariant.

## Variants and improvements

- **Regression.** Replace $x_i - \theta$ by residuals $y_i - x_i^{\mathsf T}\beta$ and the weighted mean by weighted least squares; see [iteratively reweighted least squares](/iteratively-reweighted-least-squares/). A median start is not enough there; the [MM-estimator](/mm-estimator/) supplies a high-breakdown start and scale.
- **The biweight midvariance.** A scale estimate from the same weights, used together with the biweight location in exploratory work.
- **Other redescending functions.** Hampel's three-part $\psi$, Andrews' sine $\psi(u) = \sin(u)$ for $|u| \le \pi$, and the Welsch weight $e^{-u^2/2}$ behave in the same way.
- **One-step version.** One Newton step from the median, with the derivative $\sum \psi_c'(r_i)$, gives the same first-order asymptotics if the derivative stays positive.
- **Choice of $c$.** Smaller values reject more points and lose efficiency at the normal. $c = 4.685$ gives 95%. In units of the raw MAD this is $4.685 \times 0.6745 = 3.16$ MADs.

## When to use it

Use the biweight when gross errors are expected and must have no influence, for example readings from a failing sensor or data entry errors. Use it with a good start and a robust scale. Use the [Huber estimator](/huber-m-estimator/) when you want a convex problem with a unique answer. Use the [median](/median/) when the data are very dirty and efficiency matters less. In regression, use it only inside the [MM-estimator](/mm-estimator/) or another high-breakdown method.

## Pitfalls

- **Bad start.** From the mean, or from a least squares fit, the iteration can converge to a root near the outliers. Always start from the median or another high-breakdown estimate.
- **Scale updated with the weights.** If $\hat\sigma$ is recomputed from the weighted residuals at each step, the descent proof no longer holds, and the scale can implode. Fix it, or update it by an M-scale equation with its own proof.
- **Zero MAD.** If more than half the values are equal, the MAD is 0 and the method returns the median.
- **Units of $c$.** Some texts give $c$ in units of the raw MAD, others in units of $\hat\sigma = \mathrm{MAD}/0.6745$. The value 4.685 is in units of $\hat\sigma$.
- **Inference.** With redescending $\psi$ the sum $\sum \psi_c'(r_i)$ can be small or negative in small samples, so the sandwich standard error can be unstable.

## Implementations

## History

Beaton and Tukey (1974) introduced the biweight to fit polynomials to band spectra that contained gross errors, and computed it by reweighting. Holland and Welsch (1977) studied iteratively reweighted least squares for the bisquare and other weight functions and the constants for 95% efficiency. Hampel, Ronchetti, Rousseeuw and Stahel (1986) placed redescending estimators in the influence function theory with the rejection point. Yohai (1987) used the biweight in the MM-estimator to obtain high breakdown and high efficiency together.

## References
