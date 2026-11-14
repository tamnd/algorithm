---
tag: 9XP8YC
kind: definition
slug: breakdown-point
name: Breakdown point
aliases:
- finite-sample breakdown point
area: statistics-and-inference/nonparametric-and-robust-statistics
level: core
summary: The smallest fraction of the data that, when replaced by arbitrary values, can carry an estimator to infinity. The mean has 0, the median 1/2.
prereqs: [estimator, median, order-statistic, huber-contamination-model]
see_also: [influence-function, trimmed-mean, median-absolute-deviation, hodges-lehmann-estimator, minimum-covariance-determinant, mm-estimator, least-median-of-squares, geometric-median]
sources:
  - book: isbn:9780534980443
    title: David L. Donoho and Peter J. Huber, The notion of breakdown point, in P. J. Bickel, K. A. Doksum and J. L. Hodges (eds.), A Festschrift for Erich L. Lehmann, Wadsworth, 1983
    locator: pp. 157 to 184 (the finite-sample replacement and addition breakdown points)
  - paper: doi:10.1214/aoms/1177693054
    title: Frank R. Hampel, A general qualitative definition of robustness, The Annals of Mathematical Statistics 42(6), 1971
    locator: pp. 1887 to 1896 (the asymptotic breakdown point)
  - book: isbn:9780470129906
    title: Peter J. Huber and Elvezio M. Ronchetti, Robust Statistics, second edition, Wiley, 2009
    locator: Chapter 1 (quantitative robustness and the breakdown point) and Chapter 11 (finite sample breakdown point)
  - book: isbn:9780471829218
    title: Frank R. Hampel, Elvezio M. Ronchetti, Peter J. Rousseeuw and Werner A. Stahel, Robust Statistics, The Approach Based on Influence Functions, Wiley, 1986
    locator: Chapter 2 (one-dimensional estimators, with the breakdown point of location estimators)
  - paper: doi:10.1214/aos/1176346396
    title: Peter J. Huber, Finite sample breakdown of M- and P-estimators, The Annals of Statistics 12(1), 1984
    locator: pp. 119 to 126 (breakdown of M-estimators of location)
  - paper: doi:10.1214/aos/1176347978
    title: Hendrik P. Lopuhaä and Peter J. Rousseeuw, Breakdown points of affine equivariant estimators of multivariate location and covariance matrices, The Annals of Statistics 19(1), 1991
    locator: pp. 229 to 248 (upper bounds for equivariant estimators and the breakdown points of the MCD and the MVE)
---

The breakdown point of an [estimator](/estimator/) is the smallest fraction of the sample that an adversary must replace to make the estimate arbitrarily bad. The sample mean breaks down with one bad point. The [median](/median/) holds until about half of the points are bad. It is the global measure of robustness, while the [influence function](/influence-function/) is the local one.

## Definition

Let $T$ be an estimator of a location in $\mathbb{R}^d$ and let $X = (x_1, \ldots, x_n)$ be a sample. For $0 \le m \le n$, let $\mathcal{Y}_m$ be the set of all samples $Y$ that agree with $X$ in at least $n - m$ positions; the other $m$ points are arbitrary. The **finite-sample (replacement) breakdown point** of $T$ at $X$ is
$$\varepsilon^*_n(T, X) = \frac1n \min\Big\{ m : \sup_{Y \in \mathcal{Y}_m} \|T(Y) - T(X)\| = \infty \Big\}.$$
If no $m \le n$ makes the supremum infinite, put $\varepsilon^*_n = 1$.

For a scale estimator $S > 0$, or a scatter matrix with eigenvalues $\lambda_1 \ge \cdots \ge \lambda_p$, the estimate also breaks when it can go to zero. The supremum is then over $|\log S(Y) - \log S(X)|$, or over $\max_i |\log \lambda_i(Y) - \log \lambda_i(X)|$. Growth to infinity is **explosion**, and decay to zero is **implosion**.

The **asymptotic breakdown point** uses the functional $T(P)$ and the [contamination model](/huber-contamination-model/). It is the largest $\varepsilon$ with
$$\sup_G \big\|T\big((1-\varepsilon)F + \varepsilon G\big) - T(F)\big\| < \infty.$$
Hampel (1971) defined it with Prokhorov neighbourhoods. Donoho and Huber (1983) gave the finite-sample form above. They also defined an addition version, where $m$ points are added and none is removed. For the estimators on this page, $\varepsilon^*_n$ tends to the asymptotic value as $n$ grows.

The breakdown point measures only the bias that the outliers can cause. It says nothing about the efficiency of $T$ at the model, or about its bias for small $\varepsilon$.

## Examples and non-examples

Use the order statistics $x_{(1)} \le \cdots \le x_{(n)}$ (see [order statistic](/order-statistic/)). The sample median here is $x_{((n+1)/2)}$ for odd $n$ and $(x_{(n/2)} + x_{(n/2+1)})/2$ for even $n$.

**The mean: $\varepsilon^*_n = 1/n$.** Replace $x_1$ by $x_1 + t$. The mean moves by $t/n$, which is unbounded in $t$. So one point is enough. The sample standard deviation and the least squares fit ([ordinary least squares](/ordinary-least-squares/)) also have $\varepsilon^*_n = 1/n$.

**The median: $\varepsilon^*_n = \lfloor (n+1)/2 \rfloor / n$.**

*Proof.* Let $m$ points be replaced. Call the other $n - m$ points clean, with minimum $c_-$ and maximum $c_+$. Below $c_-$ there are at most $m$ points, and above $c_+$ there are at most $m$ points.

- $n = 2r + 1$ odd and $m \le r$. The median $y_{(r+1)}$ has $r$ points below it, so it is not below $c_-$. It has $r$ points above it, so it is not above $c_+$. So the median stays in $[c_-, c_+]$ for every $Y$.
- $n = 2r$ even and $m \le r - 1$. Then $y_{(r)} \ge c_-$, because only $r - 1$ points can be below $c_-$. Also $y_{(r+1)} \le c_+$, because $y_{(r+1)}$ has $r - 1$ points above it. Since $y_{(r)} \le y_{(r+1)}$, both lie in $[c_-, c_+]$, and so does their average.

In both cases the median is bounded. Now replace $\lfloor (n+1)/2 \rfloor$ points by $t$. For odd $n$ these are $r + 1$ points, and $y_{(r+1)} = t$. For even $n$ these are $r$ points, and $y_{(r+1)} = t$, so the median is at least $(c_- + t)/2$. In both cases the median tends to infinity with $t$. $\square$

So the breakdown point is $1/2$ for even $n$ and $(n+1)/(2n)$ for odd $n$. The lower median $x_{(\lceil n/2 \rceil)}$ of the [median](/median/) page has the same value: for even $n$, $r$ points at $-\infty$ move $x_{(r)}$ to $-\infty$.

**The trimmed mean: $\varepsilon^*_n = (g+1)/n$.** The $\alpha$-[trimmed mean](/trimmed-mean/) with $g = \lfloor \alpha n \rfloor$ and $n - 2g \ge 1$ is the average of $x_{(g+1)}, \ldots, x_{(n-g)}$.

*Proof.* Let $m \le g$ points be replaced. At most $g$ points are below $c_-$, so $y_{(g+1)} \ge c_-$. At most $g$ points are above $c_+$, so $y_{(n-g)} \le c_+$. All kept values lie in $[c_-, c_+]$, and so does their mean. Now replace $g + 1$ points by $t$. Then $y_{(n-g)} = t$, and the mean of the kept values is at least $((n - 2g - 1) c_- + t)/(n - 2g)$, which tends to infinity. $\square$

So $\varepsilon^*_n \to \alpha$. A trap follows: with $\alpha = 0.1$ and $n = 7$, $g = 0$, and the "trimmed" mean is the mean, with $\varepsilon^*_7 = 1/7$.

**The upper bound $\lfloor (n+1)/2 \rfloor / n$.** Let $T$ be invariant under a permutation of the points and translation equivariant, $T(y_1 + c, \ldots, y_n + c) = T(y) + c$. Then $\varepsilon^*_n(T, X) \le \lfloor (n+1)/2 \rfloor / n$ for every sample $X$ in $\mathbb{R}$.

*Proof.* Let $k = \lfloor n/2 \rfloor$ and $t > 0$. For $n = 2k$ put
$$A = (x_1, \ldots, x_k, x_1 + t, \ldots, x_k + t), \qquad B = (x_1, \ldots, x_k, x_1 - t, \ldots, x_k - t).$$
For $n = 2k + 1$ add $x_n$ as the last entry of $A$ and $x_n - t$ as the last entry of $B$. Each of $A$ and $B$ differs from $X$ in at most $\lfloor (n+1)/2 \rfloor$ positions. The sample $A - t$ is a permutation of $B$, so $T(A) - t = T(B)$. Thus $|T(A) - T(B)| = t$, and one of $|T(A) - T(X)|$ and $|T(B) - T(X)|$ is at least $t/2$. Let $t \to \infty$. $\square$

So the median has the highest breakdown point that a translation equivariant estimator can have. An estimator that is not equivariant can do "better": the constant $T \equiv 0$ never breaks down, but it is not an estimator of location in any useful sense.

**A worked count.** Take $X = (1, 2, 3, 4, 5, 6, 7)$. Replace 3 points by $10^6$: the sample is $(1, 2, 3, 4, 10^6, 10^6, 10^6)$, and the median is 4. Replace a fourth point: the median is $10^6$. The mean moves from 4 to $1\,000\,021/7 \approx 142\,860$ after one replacement. The 20 percent trimmed mean has $g = 1$. After one replacement it is the mean of $(2, 3, 4, 5, 6)$, which is 4. After two it is the mean of $(2, 3, 4, 5, 10^6)$.

**Known values.** These are cited, except the four proved above.

| estimator | $\varepsilon^*_n$ | limit |
|---|---|---|
| mean, standard deviation, least squares | $1/n$ | 0 |
| median | $\lfloor (n+1)/2 \rfloor / n$ | 1/2 |
| $\alpha$-trimmed mean | $(\lfloor \alpha n \rfloor + 1)/n$ | $\alpha$ |
| [Hodges-Lehmann estimator](/hodges-lehmann-estimator/) | see its page | $1 - 1/\sqrt2 \approx 0.293$ |
| [MAD](/median-absolute-deviation/) | $\lfloor n/2 \rfloor / n$ | 1/2 |
| interquartile range | about $1/4$ | 1/4 |
| [Huber M-estimator](/huber-m-estimator/) with MAD scale | Huber (1984) | 1/2 |
| [MCD](/minimum-covariance-determinant/), $h$ points, general position | $\min(n - h + 1, h - p)/n$ | up to 1/2 |
| [MM-estimator](/mm-estimator/) of regression | Yohai (1987) | 1/2 |

**Non-examples.**

- A high breakdown point is not a small bias. The median has the least maximum bias at the normal (see the [contamination model](/huber-contamination-model/)), but a high breakdown estimator can still have a large bias at $\varepsilon = 0.2$.
- A bounded [influence function](/influence-function/) does not give a positive breakdown point in general. In regression, M-estimators with a bounded $\psi$ in the residual still break down with one point at a high leverage.
- In $\mathbb{R}^d$ the breakdown point can depend on the sample. For affine equivariant estimators of scatter the bound is $\lfloor (n - p + 1)/2 \rfloor / n$, and it needs the data in general position (Lopuhaä and Rousseeuw 1991).

## Related definitions

- **Influence function.** The derivative of $T$ at $F$ in the direction of a point mass. It describes small contamination, while the breakdown point describes large contamination.
- **Maximum bias curve.** The function $\varepsilon \mapsto b_T(\varepsilon)$ of the [contamination model](/huber-contamination-model/). The asymptotic breakdown point is where it becomes infinite.
- **Addition breakdown point.** Donoho and Huber also add $m$ points to the sample instead of replacing them. The value is then $m/(n+m)$ at the first $m$ that breaks $T$.
- **Masking.** In outlier detection, a group of outliers can hide each other in a fit with a low breakdown point. High breakdown estimators such as the [MCD](/minimum-covariance-determinant/) and [least median of squares](/least-median-of-squares/) avoid it.
- **Exact fit property.** In regression, if a large enough majority of the points lie exactly on one hyperplane, a fit with breakdown point near 1/2 returns that hyperplane. This property is close to breakdown, because the other points act as outliers.

## References
