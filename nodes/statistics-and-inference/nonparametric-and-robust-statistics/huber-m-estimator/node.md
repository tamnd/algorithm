---
tag: ASDS28
kind: algorithm
slug: huber-m-estimator
name: Huber M-estimator
aliases:
- Huber estimator of location
area: statistics-and-inference/nonparametric-and-robust-statistics
level: core
summary: Huber's M-estimator with a loss that is quadratic near zero and linear beyond a threshold. It is minimax for the variance under the contamination model.
model: real-ram
complexity:
  vars: {n: the sample size}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, randomized: false, exact_in_exact_arithmetic: true, in_place: false, online: false}
history:
  year: 1964
  people: [Peter J. Huber]
  note: Huber defined the estimator in 1964 and proved that it minimizes the maximum asymptotic variance over the epsilon-contaminated normal laws.
prereqs: [m-estimator, median-absolute-deviation, huber-contamination-model, influence-function, convex-function]
see_also: [tukey-biweight, mm-estimator, trimmed-mean, breakdown-point, hodges-lehmann-estimator, iteratively-reweighted-least-squares, robust-model-fitting, median]
sources:
  - paper: doi:10.1214/aoms/1177703732
    title: Peter J. Huber, Robust estimation of a location parameter, The Annals of Mathematical Statistics 35(1), 1964
    locator: pp. 73 to 101 (the estimator, the minimax theorem for the contaminated normal, and the joint estimation of location and scale)
  - book: isbn:9780470129906
    title: Peter J. Huber and Elvezio M. Ronchetti, Robust Statistics, second edition, Wiley, 2009
    locator: Chapter 3 (M-estimators of location) and Chapter 4 (the minimax variance results)
  - book: isbn:9781119214687
    title: Ricardo A. Maronna, R. Douglas Martin, Victor J. Yohai and Matías Salibián-Barrera, Robust Statistics, Theory and Methods (with R), second edition, Wiley, 2019
    locator: Chapter 2 (location M-estimators, the choice of k, the MAD scale and the iterative algorithms)
  - book: isbn:9780471829218
    title: Frank R. Hampel, Elvezio M. Ronchetti, Peter J. Rousseeuw and Werner A. Stahel, Robust Statistics, The Approach Based on Influence Functions, Wiley, 1986
    locator: Chapter 2 (the Huber estimator as the optimal B-robust estimator of location)
  - paper: doi:10.1214/aos/1176346396
    title: Peter J. Huber, Finite sample breakdown of M- and P-estimators, The Annals of Statistics 12(1), 1984
    locator: pp. 119 to 126 (breakdown of M-estimators of location with a preliminary scale)
  - paper: doi:10.1080/03610927708827533
    title: Paul W. Holland and Roy E. Welsch, Robust regression using iteratively reweighted least-squares, Communications in Statistics, Theory and Methods 6(9), 1977
    locator: pp. 813 to 827 (iteratively reweighted least squares for Huber and other weight functions)
---

The Huber M-estimator of location is the [M-estimator](/m-estimator/) with the loss $\rho_k(u) = u^2/2$ for $|u| \le k$ and $k|u| - k^2/2$ beyond. Small residuals count as in least squares, and large residuals count only linearly, so a few gross errors cannot pull the estimate far. With the scale fixed, the estimating function is piecewise linear and monotone, and its root can be found exactly by a search over its $2n$ breakpoints. Huber proved in 1964 that a suitable $k$ makes this estimator minimax for the asymptotic variance over the [contamination model](/huber-contamination-model/).

## In plain words

You want the center of some measurements, and a few of them may be wrong. The mean listens to every point with a force that grows with its distance, so one far point pulls hard. The Huber estimate lets each point pull with a force that grows with its distance only up to a limit. A point far away pulls exactly as hard as a point at the limit. The estimate is the place where the pulls from the left and from the right cancel. The limit is a number of typical spreads, and the typical spread comes from a robust measure that outliers do not change.

## The problem

The input is a sample $x_1, \ldots, x_n$ of real numbers, a tuning constant $k > 0$ and a scale $\sigma > 0$. By default $\sigma$ is the normalized [median absolute deviation](/median-absolute-deviation/), $\hat\sigma = \mathrm{MAD}/\Phi^{-1}(3/4)$, computed once before the location. Put
$$\psi_k(u) = \max(-k, \min(k, u)), \qquad \Lambda(\theta) = \sum_{i=1}^n \psi_k\!\left(\frac{x_i - \theta}{\sigma}\right).$$
The output is a minimizer of $Q(\theta) = \sum_i \rho_k((x_i - \theta)/\sigma)$, which is the same as a root of $\Lambda$. The roots form a closed interval. The algorithm returns its midpoint, so the output is unique.

## The algorithm

$\Lambda$ is continuous, nonincreasing, and linear between consecutive points of the set $B = \{x_i \pm k\sigma\}$. So it is enough to find the two breakpoints around the root and solve one linear equation.

```pseudo id=main
HUBER(x, k, σ)                                ▷ x[1 .. n], k > 0
L1  if σ is not given then σ ← MAD(x)/Φ⁻¹(3/4); if σ = 0 then return the median of x
L2  b[0 .. M] ← the sorted distinct values of x_i − kσ and x_i + kσ
L3  Λ(θ) = Σ ψ_k((x_i − θ)/σ)                  ▷ O(n) per evaluation
L4  t ← the least index with Λ(b[t]) ≤ 0        ▷ binary search; Λ(b[0]) = nk > 0
L5  θ_lo ← b[t−1] + (b[t] − b[t−1]) · Λ(b[t−1]) / (Λ(b[t−1]) − Λ(b[t]))
L6  u ← the greatest index with Λ(b[u]) ≥ 0     ▷ binary search; Λ(b[M]) = −nk < 0
L7  θ_hi ← b[u] + (b[u+1] − b[u]) · Λ(b[u]) / (Λ(b[u]) − Λ(b[u+1]))
L8  return (θ_lo + θ_hi)/2
```

Line L5 finds the least root and line L7 the greatest root. If $\Lambda(b[t]) < 0$, then $u = t - 1$ and the two lines give the same point.

## Example

Take $x = (1, 4, 5, 6, 8, 30)$, $k = 3/2$ and $\sigma = 2$, so $k\sigma = 3$. The sorted breakpoints are $b = (-2, 1, 2, 3, 4, 5, 7, 8, 9, 11, 27, 33)$, with $M = 11$. The binary searches evaluate $\Lambda$ at these points:

| $\theta$ | clipped scaled residuals $\psi_k((x_i - \theta)/2)$ | $\Lambda(\theta)$ |
|---|---|---|
| 3 | $-1, \tfrac12, 1, \tfrac32, \tfrac32, \tfrac32$ | 5 |
| 5 | $-\tfrac32, -\tfrac12, 0, \tfrac12, \tfrac32, \tfrac32$ | $\tfrac32$ |
| 7 | $-\tfrac32, -\tfrac32, -1, -\tfrac12, \tfrac12, \tfrac32$ | $-\tfrac52$ |
| 9 | $-\tfrac32, -\tfrac32, -\tfrac32, -\tfrac32, -\tfrac12, \tfrac32$ | $-5$ |

Line L4 gives $b[t] = 7$, and line L6 gives $b[u] = 5$. Both lines L5 and L7 give $\theta = 5 + 2 \cdot \frac{3/2}{3/2 + 5/2} = \frac{23}{4} = 5.75$. Check: at $5.75$ the clipped residuals are $-\tfrac32, -\tfrac78, -\tfrac38, \tfrac18, \tfrac98, \tfrac32$, and they sum to 0. The mean is 9, pulled up by the value 30, and the median is 5.5. The MAD of this sample is 2, so the default scale is $2/0.6745 = 2.965$. With the default $k = 1.345$ the estimate is also $5.75$, because then only the points 1 and 30 are clipped, both at $k\sigma = 3.988$.

## Correctness

$\psi_k$ is continuous and nondecreasing, so $\Lambda$ is continuous and nonincreasing. Between two consecutive breakpoints, every point is either in the clipped part on the left, in the clipped part on the right, or in the linear part, and it stays there. So $\Lambda$ is linear on each closed segment between consecutive breakpoints, and linear interpolation between two breakpoints gives an exact root. $Q$ is convex and differentiable with $Q'(\theta) = -\Lambda(\theta)/\sigma$, so its minimizers are exactly the roots of $\Lambda$. The binary searches keep the facts $\Lambda(b[t-1]) > 0 \ge \Lambda(b[t])$ and $\Lambda(b[u]) \ge 0 > \Lambda(b[u+1])$, so they find the segments that hold the least and the greatest root. The full proof is in `proofs/correctness.md`.

## Complexity

- **Time.** The sort in line L2 takes $\Theta(n \log n)$. Each binary search evaluates $\Lambda$ at $O(\log n)$ points, and each evaluation costs $\Theta(n)$. The MAD needs two [medians](/median/), which take expected $\Theta(n)$ with [quickselect](/quickselect/). So the total is $\Theta(n \log n)$.
- **Space.** $\Theta(n)$ for the breakpoints.
- **Arithmetic.** With rational data, $k$ and $\sigma$, all steps are exact, and the root satisfies $\Lambda(\hat\theta) = 0$ exactly. The default scale contains $\Phi^{-1}(3/4)$, which is irrational, so in practice the result is a floating-point number.

## Properties

The page proves the breakdown point below. The influence function is proved on the [influence function](/influence-function/) page. The optimality results are cited.

- **Influence function.** At the normal law with the scale fixed at its true value $\sigma$, $\mathrm{IF}(x) = \sigma\,\psi_k((x - \mu)/\sigma)/(2\Phi(k) - 1)$. It is bounded, and the standardized gross-error sensitivity is $k/(2\Phi(k) - 1)$.
- **Efficiency at the normal.** The asymptotic variance at $N(0, 1)$ is $\mathrm E\psi_k(Z)^2 / (2\Phi(k) - 1)^2$, with $\mathrm E\psi_k(Z)^2 = 2\Phi(k) - 1 - 2k\varphi(k) + 2k^2(1 - \Phi(k))$. A numerical evaluation gives:

| $k$ | 1.0 | 1.345 | 1.5 | 2.0 |
|---|---|---|---|---|
| asymptotic variance | 1.1073 | 1.0526 | 1.0371 | 1.0104 |
| efficiency | 0.903 | 0.950 | 0.964 | 0.990 |
| gross-error sensitivity | 1.465 | 1.637 | 1.731 | 2.095 |

  So $k = 1.345$ gives 95% efficiency at the normal.
- **Minimax variance (cited).** For the model $(1 - \varepsilon)\Phi + \varepsilon H$ with $H$ symmetric, the Huber estimator with $k$ solving $2\varphi(k)/k - 2(1 - \Phi(k)) = \varepsilon/(1 - \varepsilon)$ minimizes the maximum asymptotic variance over the model (Huber 1964). The least favorable law has a normal center and exponential tails. A numerical solution gives:

| $\varepsilon$ | 0.01 | 0.05 | 0.10 | 0.20 |
|---|---|---|---|---|
| minimax $k$ | 1.945 | 1.398 | 1.140 | 0.862 |

- **Optimal B-robustness (cited).** Among location M-estimators with a bound on the gross-error sensitivity, the Huber estimator has the least asymptotic variance at the normal (Hampel, Ronchetti, Rousseeuw and Stahel 1986, Chapter 2).
- **Breakdown point $\lceil n/2 \rceil / n$ with the MAD scale (proved).** Replace $m < n/2$ points by any values, and let $c_1 \le c_2$ be the least and the greatest of the clean points and $R = c_2 - c_1$. For $\theta > c_2 + k\sigma$ every clean term is $-k$, so $\Lambda(\theta) \le -(n - m)k + mk < 0$. In the same way $\Lambda(\theta) > 0$ for $\theta < c_1 - k\sigma$. So every root lies in $[c_1 - k\sigma, c_2 + k\sigma]$. The median of the new sample lies in $[c_1, c_2]$, because more than half of the points are clean. So more than half of the absolute deviations are at most $R$, which gives $\mathrm{MAD} \le R$ and $\sigma \le R/\Phi^{-1}(3/4)$. If $\sigma = 0$, the output is the median, which is also in $[c_1, c_2]$. So the estimate stays bounded. With $m = \lceil n/2 \rceil$ points at one far value $s$, the median and the estimate follow $s$. This is the largest value that a translation equivariant estimator can have (see the [breakdown point](/breakdown-point/) page). With a fixed scale the same argument gives the same bound.
- **Equivariance.** With the MAD scale, the estimate is location and scale equivariant: $T(ax + b) = aT(x) + b$ for $a \ne 0$. With a fixed $\sigma$ it is only location equivariant.
- **Limits.** If $k\sigma$ is larger than the range of the sample, all residuals are in the linear part and the estimate is the mean. As $k \to 0$ the estimate tends to a [median](/median/).

## Variants and improvements

- **Iteratively reweighted means.** Start at the median and repeat $\theta \leftarrow \sum w_i x_i / \sum w_i$ with $w_i = \min(1, k\sigma/|x_i - \theta|)$. Each step does not increase $Q$, and the iteration converges to a root. It is the form that extends to regression; see [iteratively reweighted least squares](/iteratively-reweighted-least-squares/) (Holland and Welsch 1977).
- **Newton steps.** $\theta \leftarrow \theta + \sigma\Lambda(\theta)/|I(\theta)|$, where $I(\theta)$ is the set of points in the linear part. On the segment that holds the root, one step is exact, because $\Lambda$ is linear there.
- **One-step Huber.** Start at the median and do one Newton step. It has the same first-order asymptotics as the full estimator.
- **Joint scale (Proposal 2).** Solve two equations at once: $\Lambda(\theta) = 0$ and $\sum \psi_k((x_i - \theta)/\sigma)^2 = (n - 1)\,\mathrm E\psi_k(Z)^2$ (Huber 1964). Its breakdown point depends on $k$ and is lower than one half (Huber 1984).
- **Regression.** Replace $x_i - \theta$ by the residual $y_i - x_i^{\mathsf T}\beta$. The objective is still convex, but the breakdown point under leverage points is $1/n$. Use the [MM-estimator](/mm-estimator/) when the design can contain outliers.
- **Redescending loss.** The [Tukey biweight](/tukey-biweight/) sets the influence of far points to 0, at the cost of a nonconvex objective.

## When to use it

Use it as the default robust estimate of location for data that are roughly normal with some outliers or heavy tails. It keeps about 95% of the efficiency of the mean at the normal and has the highest possible breakdown point with the MAD scale. Use the [median](/median/) if you need the simplest rule. Use the [Tukey biweight](/tukey-biweight/) if gross outliers are frequent and must have no influence. Use the [trimmed mean](/trimmed-mean/) if you need a rule that is easy to explain. Use the [Hodges-Lehmann estimator](/hodges-lehmann-estimator/) if you want a rank method with a matching test.

## Pitfalls

- **No scale.** Without $\sigma$ the estimate is not scale equivariant: $k = 1.345$ in meters and in millimeters gives different results. Always divide by a robust scale.
- **The standard deviation as scale.** Outliers inflate it, so $k\sigma$ grows and nothing is clipped. Use the MAD or another robust scale.
- **Zero MAD.** If more than half of the values are equal, the MAD is 0. The method then returns the median. A different robust scale, such as $Q_n$, avoids this.
- **A root set that is an interval.** If no residual is in the linear part near the root, $\Lambda$ is 0 on a whole segment. For $x = (0, 10)$, $k = 1$ and $\sigma = 1$, every $\theta$ in $[1, 9]$ is a root. The algorithm returns the midpoint 5. Iterative solvers can stop anywhere in the segment.
- **Stopping rules.** IRLS converges only linearly when many points are clipped. The exact method above has no tolerance to choose.
- **Asymmetric contamination.** The minimax theorem assumes symmetric contamination. Under one-sided contamination the estimate has a bias of order $\varepsilon$, as every location estimator does (see the [contamination model](/huber-contamination-model/)).

## Implementations

## History

Huber (1964) introduced the estimator, proved its minimax property for the symmetric contaminated normal, and gave Proposal 2 for the joint estimation of scale. The influence function approach of Hampel gave it a second optimality: Hampel, Ronchetti, Rousseeuw and Stahel (1986) present it as the optimal B-robust estimator of location. Holland and Welsch (1977) studied the reweighting algorithms for this and other weight functions in regression. Huber (1984) studied the finite-sample breakdown of M-estimators with a preliminary scale.

## References
