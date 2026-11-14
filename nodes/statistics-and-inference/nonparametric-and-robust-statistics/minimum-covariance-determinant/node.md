---
tag: KD8XYJ
kind: algorithm
slug: minimum-covariance-determinant
name: Minimum covariance determinant
aliases:
- MCD estimator
- FAST-MCD
area: statistics-and-inference/nonparametric-and-robust-statistics
level: advanced
summary: Estimates location and scatter from the h points whose covariance matrix has the least determinant. FAST-MCD uses concentration steps; the result flags multivariate outliers.
model: real-ram
complexity:
  vars: {n: the number of points, p: the dimension, m: the number of random starts, t: the number of C-steps for each start}
  time: {worst: O(m t (n p² + p³ + n log n)), average: O(m t (n p² + p³ + n log n)), best: O(m (n p² + p³ + n log n))}
  space: {extra: O(n + p²)}
properties: {deterministic: false, randomized: true, exact_in_exact_arithmetic: false, in_place: false, online: false}
history:
  year: 1984
  people: [Peter J. Rousseeuw, Katrien Van Driessen]
  note: Rousseeuw defined the MCD in 1984 as a high-breakdown estimator of multivariate location and scatter. Rousseeuw and Van Driessen gave the FAST-MCD algorithm and its C-step theorem in 1999.
prereqs: [covariance-matrix, determinant, eigenvalue, breakdown-point, trimmed-mean, huber-contamination-model]
see_also: [least-trimmed-squares, mm-estimator, tukey-median, robust-pca, robust-mean-estimation-filter, principal-component-analysis, statistical-outlier-removal, geometric-median]
sources:
  - paper: doi:10.1080/01621459.1984.10477105
    title: Peter J. Rousseeuw, Least median of squares regression, Journal of the American Statistical Association 79(388), 1984
    locator: pp. 871 to 880 (the definition of the minimum covariance determinant estimator)
  - paper: doi:10.1080/00401706.1999.10485670
    title: Peter J. Rousseeuw and Katrien Van Driessen, A fast algorithm for the minimum covariance determinant estimator, Technometrics 41(3), 1999
    locator: pp. 212 to 223 (the C-step theorem and the FAST-MCD algorithm)
  - paper: doi:10.1002/wics.1421
    title: Mia Hubert, Michiel Debruyne and Peter J. Rousseeuw, Minimum covariance determinant and extensions, WIREs Computational Statistics 10(3), 2018
    locator: the survey of the MCD, its breakdown point, its consistency factor, its efficiency, the reweighting step and the C-step
  - paper: doi:10.1214/aos/1176347978
    title: Hendrik P. Lopuhaä and Peter J. Rousseeuw, Breakdown points of affine equivariant estimators of multivariate location and covariance matrices, The Annals of Statistics 19(1), 1991
    locator: pp. 229 to 248 (the breakdown point of the MCD and its dependence on h)
  - book: isbn:9780471852339
    title: Peter J. Rousseeuw and Annick M. Leroy, Robust Regression and Outlier Detection, Wiley, 1987
    locator: the chapter on multivariate location and covariance (the MVE and the MCD)
  - book: isbn:9781119214687
    title: Ricardo A. Maronna, R. Douglas Martin, Victor J. Yohai and Matías Salibián-Barrera, Robust Statistics, Theory and Methods (with R), second edition, Wiley, 2019
    locator: the chapter on multivariate analysis (the MCD and its computation)
---

The minimum covariance determinant (MCD) estimator of multivariate location and scatter looks at all subsets of $h$ of the $n$ points. It keeps the subset whose covariance matrix has the least determinant, and it returns the mean and a scaled covariance matrix of that subset. The determinant measures the volume of the ellipsoid of the data, so the MCD subset is the tightest group of $h$ points. With $h$ near $n/2$, the estimator has a breakdown point near one half and is affine equivariant. An exact search costs $\binom nh$ determinants, so the FAST-MCD algorithm of Rousseeuw and Van Driessen (1999) starts from many small random subsets and improves each one by C-steps. A C-step never increases the determinant. Distances from the MCD fit then flag multivariate outliers.

## In plain words

The ordinary mean and covariance of a cloud of points are pulled away by a few bad points. The MCD finds the most compact half of the points, or a bit more than half, and computes the center and the spread from those points only. To find that compact group, FAST-MCD starts from a few random points. It measures how far every point lies from their center, taking the shape of the cloud into account, and it keeps the closest points. Then it repeats this with the kept points. Each round makes the group at least as compact as before. It does this from many starts and keeps the best result. Points that lie far from the final center are flagged as outliers.

## The problem

The input is $n$ points $x_1, \ldots, x_n \in \mathbb R^p$ and an integer $h$ with $p < h \le n$. The default is $h = \lfloor (n + p + 1)/2 \rfloor$. For a set $H$ of $h$ indices, let $T(H)$ be the mean and $S(H) = \frac1h\sum_{i \in H}(x_i - T(H))(x_i - T(H))^{\mathsf T}$ the covariance matrix of its points.

- The **raw MCD** is $(T(H^*), S(H^*))$, where $H^*$ minimizes $\det S(H)$ over all sets of $h$ indices.
- The **squared Mahalanobis distance** of a point from a fit $(T, S)$ is $d^2(x; T, S) = (x - T)^{\mathsf T}S^{-1}(x - T)$.
- The **consistency factor** $c_\alpha = \alpha / F_{p+2}(q_\alpha)$, with $\alpha = h/n$, $q_\alpha$ the $\alpha$-quantile of the chi-squared distribution with $p$ degrees of freedom, and $F_{p+2}$ the chi-squared distribution function with $p + 2$ degrees of freedom. The raw scatter is reported as $c_\alpha S(H^*)$, which estimates $\Sigma$ at the normal model $N(\mu, \Sigma)$.
- The **reweighted MCD** keeps the points with $d^2 \le \chi^2_{p, 0.975}$ under the raw fit, and returns their mean and their covariance times $0.975/F_{p+2}(\chi^2_{p,0.975})$.

## The algorithm

```pseudo id=main
FAST-MCD(x_1..x_n, h, m)
L1  for j ← 1 to m do
L2      J ← a random set of p + 1 indices; while S(J) is singular, add a random index to J
L3      (μ, S) ← the mean and the covariance matrix of the points in J
L4      H ← the indices of the h points with the least d²(x_i; μ, S)
L5      repeat                                              ▷ C-steps
L6          (μ, S) ← (T(H), S(H))
L7          if det S = 0 then stop                          ▷ h points on a hyperplane: an exact fit
L8          H' ← the indices of the h points with the least d²(x_i; μ, S)
L9          if H' = H or det S(H') ≥ det S then stop, else H ← H'
L10     if det S is the least so far then (μ*, S*) ← (μ, S)
L11 S* ← c_α S* with α = h/n
L12 w_i ← 1 if d²(x_i; μ*, S*) ≤ χ²_{p,0.975}, else 0
L13 μ_w ← the mean of the points with w_i = 1; S_w ← (0.975 / F_{p+2}(χ²_{p,0.975})) × their covariance matrix
L14 return (μ*, S*), (μ_w, S_w), and the outlier flags d²(x_i; μ_w, S_w) > χ²_{p,0.975}
```

Lines L5 to L9 are the C-steps ("C" for concentration). Each one computes the mean and the covariance of the current $h$ points and keeps the $h$ points that are closest to them in Mahalanobis distance.

## Example

Take $n = 10$ points in the plane, $p = 2$ and $h = 6$:

$$x_1, \ldots, x_{10} = (2,1), (1,3), (5,4), (3,2), (4,1), (3,4), (4,6), (10,-1), (11,2), (10,10).$$

The first seven points form a cloud, and $x_8, x_9, x_{10}$ are outliers. The sample mean of all ten points is $(5.3, 3.2)$.

Start from $J = \{3, 7, 8\}$, a set with one outlier. Its mean is $(19/3, 3)$. Each point of $J$ has $d^2 = 2$, and the next smallest distances are those of $x_6$, $x_9$ and $x_5$. All computations below are exact.

| step | $H$ | $T(H)$ | $\det S(H)$ |
|---|---|---|---|
| 1 | {3, 5, 6, 7, 8, 9} | (37/6, 8/3) | 3397/108 ≈ 31.45 |
| 2 | {3, 4, 5, 6, 7, 8} | (29/6, 8/3) | 1909/108 ≈ 17.68 |
| 3 | {2, 3, 4, 5, 6, 7} | (10/3, 10/3) | 413/108 ≈ 3.82 |
| 4 | {1, 3, 4, 5, 6, 7} | (7/2, 3) | 85/36 ≈ 2.36 |

The C-step from step 4 returns the same set, so the loop stops. The determinant fell at every step, and the outliers left the set one by one. An enumeration of all $\binom{10}{6} = 210$ sets confirms that $85/36$ is the least determinant, so this start found the raw MCD: $T = (7/2, 3)$ and $S = \begin{pmatrix} 11/12 & 5/6 \\ 5/6 & 10/3 \end{pmatrix}$.

Not every start succeeds. Of the 119 nonsingular starts with 3 points, 43 reach $H^* = \{1, 3, 4, 5, 6, 7\}$. The others stop at 7 other sets. For example, the start $\{1, 2, 8\}$ stops at $\{1, 2, 4, 5, 6, 8\}$, which holds the outlier $x_8$ and has determinant $973/108 \approx 9.01$. This is why FAST-MCD uses many starts.

With $\alpha = 0.6$ the consistency factor is $c_{0.6} = 2.5698$. The clean point $x_2$ is outside $H$, but its distance under the corrected raw fit is $3.43$, below $\chi^2_{2, 0.975} = 7.378$, so the reweighting step brings it back. The reweighted mean is the mean of the seven clean points, $(22/7, 3) \approx (3.14, 3.00)$. The final squared distances of $x_8, x_9, x_{10}$ are 45.8, 43.7 and 32.7, so exactly these three points are flagged.

## Correctness

The page proves the C-step theorem and the termination of the loop. It does not prove that FAST-MCD finds the MCD subset, and in general it does not. `proofs/correctness.md` has the full proofs.

- **The C-step theorem (Rousseeuw and Van Driessen 1999).** Let $H_2$ come from a C-step from $H_1$, with $\det S_1 > 0$. Inside $H_1$ the squared distances add up to $\operatorname{tr}(S_1^{-1}hS_1) = hp$. $H_2$ takes the $h$ smallest distances, so their sum is at most $hp$. That sum equals $h\operatorname{tr}(S_1^{-1}S_2) + h(T_2 - T_1)^{\mathsf T}S_1^{-1}(T_2 - T_1)$. So $\operatorname{tr}(S_1^{-1}S_2) \le p$. The eigenvalues of $S_1^{-1}S_2$ are nonnegative, their product is $\det S_2/\det S_1$, and their mean is at most 1. The inequality of the arithmetic and geometric means gives $\det S_2 \le \det S_1$. Equality forces $T_2 = T_1$ and $S_2 = S_1$.
- **Termination.** Line L9 accepts only a strictly smaller determinant, so no set comes back, and the loop stops after at most $\binom nh$ passes. At the stop, the next C-step does not change the mean or the covariance matrix.
- **The optimum is a stopping point.** A C-step from $H^*$ cannot lower the determinant further, so it keeps $T(H^*)$ and $S(H^*)$. Other sets can also be stopping points, as the example shows. FAST-MCD finds $H^*$ when the C-steps from at least one start reach it.
- **The consistency factor.** For a standard normal vector $X$, $\mathbb E[XX^{\mathsf T} \mid \|X\|^2 \le q_\alpha] = \frac{F_{p+2}(q_\alpha)}{\alpha}I$, because $u f_p(u) = p f_{p+2}(u)$ for the chi-squared densities. Line L11 removes this factor.

## Complexity

- **One C-step.** The mean and the covariance cost $O(hp^2)$. The inverse and the determinant cost $O(p^3)$. The $n$ distances cost $O(np^2)$. The $h$ smallest distances cost $O(n)$ with [quickselect](/quickselect/), or $O(n \log n)$ with a sort as in the implementation.
- **All starts.** With $m$ starts and at most $t$ C-steps for each, the total is $O(mt(np^2 + p^3 + n\log n))$. In practice $t$ is small: the C-steps of the example stopped after 4 steps. There is no useful bound on $t$ other than $\binom nh$.
- **Number of starts.** A random $(p+1)$-subset contains no outlier with probability about $(1 - \varepsilon)^{p+1}$, so the number of starts needed grows exponentially in $p$.
- **Exact computation.** The enumeration of all $h$-subsets costs $\binom nh$ determinants. This is feasible only for small $n$, as in the tests.
- **Space.** $O(n + p^2)$ besides the input.

## Properties

Proved on this page: the C-step theorem, the termination of the C-steps, the fixed-point property of the optimum, and the form of the consistency factor. Cited: the breakdown point, the consistency and the efficiency. Measured: the numbers from the tests.

- **Breakdown point (cited).** For points in general position, the finite-sample breakdown point of the raw MCD is $\min(n - h + 1, h - p)/n$ (Lopuhaä and Rousseeuw 1991; Hubert, Debruyne and Rousseeuw 2018). It is largest, $\lfloor (n - p + 1)/2\rfloor / n$, for $\lfloor (n+p)/2 \rfloor \le h \le \lfloor (n+p+1)/2 \rfloor$. The $h - p$ term comes from implosion: $h - p$ replaced points on a hyperplane through $p$ good points make an $h$-subset with determinant 0. In the example, $\min(5, 4)/10 = 0.4$. The reweighted MCD keeps the breakdown point of the raw MCD.
- **Efficiency (cited).** The raw MCD with $\alpha = 0.5$ has a low efficiency at the normal: about 6% when $p = 2$. The reweighting step raises it to about 45.5% for $p = 2$ (Hubert, Debruyne and Rousseeuw 2018).
- **Equivariance.** $T(H)$ and $S(H)$ are affine equivariant, and the Mahalanobis order of the points does not change under an affine map. So the exact MCD and the C-steps are affine equivariant. With the same random starts, FAST-MCD is too. The tests confirm this exactly on the example.
- **Bounded influence (cited).** The influence function of the MCD is bounded (Hubert, Debruyne and Rousseeuw 2018).
- **Measured.** For $p = 2$ and $n \le 12$, the tests compare FAST-MCD with the enumeration of all $h$-subsets in exact arithmetic. Taking every $(p+1)$-subset as a start found the exact MCD determinant on all of the random contaminated sets tried. With 30 random starts it found it on 12 of 12 sets. In a larger trial outside the tests, 30 random starts missed the optimum on 2 of 115 sets, so the test allows a few misses. On 80 normal points in $\mathbb R^3$ with 20 points shifted by 6 in each coordinate, the reweighted MCD flagged all 20 shifted points and 1 of the 80 clean points, and its location was at distance 0.22 from the true center. The distance of the sample mean was 2.05.

## Variants and improvements

- **Selective iteration.** FAST-MCD of Rousseeuw and Van Driessen (1999) runs only two C-steps from each start, keeps the 10 best sets, and runs those to convergence. For large $n$ it works on disjoint subsamples first and merges them.
- **Deterministic MCD.** Start from a few deterministic robust estimates instead of random subsets, as described in the survey of Hubert, Debruyne and Rousseeuw (2018).
- **Small-sample corrections.** Extra factors make the scatter nearly unbiased at the normal for small $n$.
- **Minimum volume ellipsoid.** The MVE, also defined by Rousseeuw (1984), minimizes the volume of a covering ellipsoid of $h$ points. It has the same breakdown point and worse efficiency.
- **Regularized MCD.** For $p \ge h$, the sample covariance of $h$ points is singular. A regularized MCD adds a multiple of a target matrix.
- **Uses.** Robust Mahalanobis distances for outlier detection, robust principal components (see [robust PCA](/robust-pca/)), robust discriminant analysis, and starts for [MM-estimators](/mm-estimator/) of multivariate location and of regression.

## When to use it

Use the MCD to estimate a center and a covariance matrix of moderate-dimensional data ($p$ up to a few dozen) when a sizeable fraction of the points may be outliers, and to flag multivariate outliers that no single coordinate shows. Use the classical mean and covariance on clean data. Use coordinatewise robust estimates, such as the [median](/median/) and the [MAD](/median-absolute-deviation/), when affine equivariance is not needed. In high dimension, where random subsets almost never avoid the outliers, use a spectral method such as the [robust mean estimation filter](/robust-mean-estimation-filter/), or a regularized MCD.

## Pitfalls

- **The breakdown formula.** The breakdown point is $\min(n - h + 1, h - p)/n$, not $(n - h + 1)/n$. The two agree only when $h \ge (n + p + 1)/2$.
- **Forgetting the consistency factor.** $S(H^*)$ comes from the most compact half of the data, so it is far too small. For $p = 2$ and $\alpha = 1/2$, the factor is $3.26$.
- **Not the global optimum.** FAST-MCD gives a local optimum. Too few starts can miss the MCD subset, in particular when $p$ is large or the outliers are many.
- **$h$ must exceed $p$.** For $h \le p$ every covariance matrix of $h$ points is singular. Exact fits, with more than $h$ points on a hyperplane, give determinant 0: then report the hyperplane rather than invert $S$.
- **The cutoff is approximate.** The $\chi^2_{p, 0.975}$ cutoff assumes normal data and large $n$. With small $n$, many clean points can be flagged.
- **Floating point.** Comparing determinants that differ only by rounding can make the C-steps cycle. Stop when the determinant does not decrease, as line L9 does.

## Implementations

## History

Rousseeuw (1984) introduced the MCD and the minimum volume ellipsoid as affine equivariant estimators of multivariate location and scatter with a high breakdown point. The exact computation was out of reach for all but small data sets, and the MVE was used more at first. Lopuhaä and Rousseeuw (1991) gave the breakdown points of affine equivariant estimators, including the MCD. Rousseeuw and Van Driessen (1999) proved the C-step theorem and gave FAST-MCD, which made the MCD practical and the more popular of the two. Hubert, Debruyne and Rousseeuw (2018) survey the estimator, its properties and its extensions.

## References
