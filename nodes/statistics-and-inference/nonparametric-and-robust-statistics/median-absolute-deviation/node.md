---
tag: KS6NA3
kind: definition
slug: median-absolute-deviation
name: Median absolute deviation
aliases:
- MAD
area: statistics-and-inference/nonparametric-and-robust-statistics
level: intro
summary: The median of the absolute deviations from the median. Scaled by 1.4826 it estimates the normal standard deviation with breakdown point 1/2.
prereqs: [median, quantile, sample-variance]
see_also: [breakdown-point, influence-function, huber-m-estimator, tukey-biweight, trimmed-mean, minimum-covariance-determinant, statistical-outlier-removal, q-q-plot]
sources:
  - paper: doi:10.1080/01621459.1974.10482962
    title: Frank R. Hampel, The influence curve and its role in robust estimation, Journal of the American Statistical Association 69(346), 1974
    locator: pp. 383 to 393 (the median deviation as a robust scale estimator, and its influence function)
  - paper: doi:10.1080/01621459.1993.10476408
    title: Peter J. Rousseeuw and Christophe Croux, Alternatives to the median absolute deviation, Journal of the American Statistical Association 88(424), 1993
    locator: pp. 1273 to 1283 (the MAD, its breakdown point and its 37 percent efficiency, and the estimators Sn and Qn)
  - paper: doi:10.1007/BF02481078
    title: Peter Hall and A. H. Welsh, Limit theorems for the median deviation, Annals of the Institute of Statistical Mathematics 37, 1985
    locator: pp. 27 to 36 (the asymptotic normality of the MAD)
  - book: isbn:9781119214687
    title: Ricardo A. Maronna, R. Douglas Martin, Victor J. Yohai and Matías Salibián-Barrera, Robust Statistics, Theory and Methods (with R), second edition, Wiley, 2019
    locator: Chapter 2 (dispersion estimators, the normalized MAD)
  - book: isbn:9780470129906
    title: Peter J. Huber and Elvezio M. Ronchetti, Robust Statistics, second edition, Wiley, 2009
    locator: Chapter 5 (scale estimates, the median absolute deviation)
---

The median absolute deviation (MAD) is a robust measure of spread. Take the [median](/median/) of the sample, then the median of the distances of the points from it. Half of the points are within one MAD of the median. Multiplied by $1/\Phi^{-1}(3/4) \approx 1.4826$, it estimates the standard deviation of a normal law. Unlike the standard deviation, it can carry almost half of the sample as outliers.

## Definition

For a sample $x_1, \ldots, x_n$, let $\operatorname{med}$ be the sample median (the average of the two middle values when $n$ is even). The **median absolute deviation** is
$$\mathrm{MAD}(x) = \operatorname{med}_i\, |x_i - \operatorname{med}_j x_j|.$$
The **normalized MAD** is
$$\hat\sigma = \frac{\mathrm{MAD}(x)}{\Phi^{-1}(3/4)} \approx 1.4826\,\mathrm{MAD}(x),$$
where $\Phi^{-1}(3/4) = 0.6744897\ldots$ is the upper [quartile](/quantile/) of the standard normal law.

For a law $F$ with median $m$, the functional is the median of the law of $|X - m|$: the value $q$ with $P_F(|X - m| \le q) = 1/2$.

Computing the MAD needs two medians, so it takes linear time with a selection method such as [quickselect](/quickselect/).

**Proof of the constant.** Let $X \sim N(\mu, \sigma^2)$. Its median is $\mu$. For $c > 0$,
$$P(|X - \mu| \le c) = \Phi(c/\sigma) - \Phi(-c/\sigma) = 2\Phi(c/\sigma) - 1.$$
This equals $1/2$ if and only if $\Phi(c/\sigma) = 3/4$, that is $c = \sigma\,\Phi^{-1}(3/4)$. So the population MAD is $\sigma\,\Phi^{-1}(3/4)$, and $\mathrm{MAD}/\Phi^{-1}(3/4)$ has the functional value $\sigma$. The sample MAD tends to the population MAD almost surely when $F$ is continuous and the two medians are unique, so $\hat\sigma$ is consistent for $\sigma$ at the normal. $\square$

The constant is $1/0.6744897 = 1.482602\ldots$. At another law the same factor gives a different number. At the Laplace law with scale $b$ (standard deviation $b\sqrt2$), the MAD is $b \ln 2$.

## Examples and non-examples

**A small sample by hand.** Take $x = (2, 4, 4, 5, 7, 9, 30)$. The median is 5. The absolute deviations are $(3, 1, 1, 0, 2, 4, 25)$; sorted, $(0, 1, 1, 2, 3, 4, 25)$. Their median is 2, so $\mathrm{MAD} = 2$ and $\hat\sigma = 2 \times 1.4826 = 2.9652$. The sample standard deviation is 9.656, mostly because of the point 30. Change 30 to 3000: the MAD stays 2, and the standard deviation becomes 1131.9.

**An even sample.** For $(1, 2, 3, 4, 5, 6)$ the median is 3.5, the deviations are $(2.5, 1.5, 0.5, 0.5, 1.5, 2.5)$, and the MAD is 1.5.

**Breakdown point $\lfloor n/2 \rfloor / n$.** Let the clean sample have distinct values, with $n = 2r + 1$ or $n = 2r$. Replace $m$ points. A scale estimate breaks down if it can go to infinity (explosion) or to zero (implosion); see [breakdown point](/breakdown-point/).

*Proof.* Explosion. If $m < \lfloor (n+1)/2 \rfloor$, the median stays in $[c_-, c_+]$, the range of the clean points (the [breakdown point](/breakdown-point/) page proves this). Then every clean point has a deviation at most $D = c_+ - c_-$. There are $n - m$ clean points. For odd $n$, $m \le r$ gives at least $r + 1$ deviations at most $D$, so the middle deviation is at most $D$. For even $n$, $m \le r - 1$ gives at least $r + 1$ such deviations, so both middle deviations are at most $D$. So no explosion happens with fewer than $\lfloor (n+1)/2 \rfloor$ points.

Implosion. Let $\delta > 0$ be the least gap between two clean values. An open interval of length less than $\delta$ holds at most one clean point. So at most $m + 1$ deviations are less than $\delta/2$. If $m \le \lfloor n/2 \rfloor - 1$, then $m + 1 \le r$ in both cases, so the $(r+1)$-th smallest deviation is at least $\delta/2$, and the MAD is at least $\delta/4$. Conversely, put $\lfloor n/2 \rfloor = r$ replaced points on top of one clean point $x_1$. Then $r + 1$ points equal $x_1$. They are a majority of the sample, so the median is $x_1$, and $r + 1$ deviations are 0. The $(r+1)$-th smallest deviation is 0, and so is the MAD.

So implosion needs $\lfloor n/2 \rfloor$ points and explosion needs $\lfloor (n+1)/2 \rfloor$, and $\varepsilon^*_n = \lfloor n/2 \rfloor / n$. This tends to $1/2$, the best value for an equivariant scale estimator. $\square$

**Influence function and efficiency.** Let $F$ be symmetric about $m$ with a density $f$ that is continuous and positive at $m \pm q$, where $q$ is the population MAD. Contaminate with $t\,\delta_x$. The median moves by $O(t)$, but by symmetry its first-order effect on $P(|X - m| \le q)$ is $f(m+q) - f(m-q) = 0$. Differentiate $(1-t)\,[F(m + q_t) - F(m - q_t)] + t\,\mathbf 1\{|x - m| \le q_t\} = 1/2$ at $t = 0$:
$$-\tfrac12 + 2f(m+q)\,q' + \mathbf 1\{|x - m| \le q\} = 0, \qquad \mathrm{IF}(x; \mathrm{MAD}, F) = \frac{\operatorname{sign}(|x - m| - q)}{4 f(m+q)}.$$
For $\hat\sigma$ at $F = \Phi$, with $q = \Phi^{-1}(3/4) = 0.6745$ and $\varphi(q) = 0.3178$, this is $\operatorname{sign}(|x| - q)/(4 q \varphi(q))$. It takes only the two values $\pm 1.1664$. The asymptotic variance is $E[\mathrm{IF}^2] = 1/(4 q \varphi(q))^2 = 1.3605$. The standard deviation has the influence function $(x^2 - 1)/2$ and the variance $1/2$. So the efficiency of the MAD at the normal is $0.5/1.3605 = 0.3675$, about 37 percent. Hall and Welsh (1985) proved the asymptotic normality.

**Non-examples.**

- **The mean absolute deviation** $\frac1n\sum|x_i - \bar x|$ is not robust. Its breakdown point is $1/n$, like the standard deviation.
- **A MAD that is zero.** If more than half of the sample has one value, the MAD is 0, even if the other points are spread out. For example, $(0, 0, 0, 0, 1, 50)$ has MAD 0. Data that are rounded or counts often show this. Then a scale of 0 makes standardized residuals $(x_i - \operatorname{med})/\hat\sigma$ infinite.
- **The constant 1.4826** gives $\sigma$ only at the normal law. It is not a general conversion from MAD to standard deviation.

## Related definitions

- **Interquartile range.** $Q_3 - Q_1$, divided by $2\Phi^{-1}(3/4) = 1.349$ at the normal. Its breakdown point is $1/4$. For a symmetric law the MAD is half the interquartile range.
- **$S_n$ and $Q_n$ of Rousseeuw and Croux (1993).** $S_n = c\,\operatorname{med}_i \operatorname{med}_j |x_i - x_j|$ and $Q_n$, the first quartile of the pairwise distances $|x_i - x_j|$ for $i < j$. Both have breakdown point $1/2$ and need no location estimate. $Q_n$ has an efficiency of about 82 percent at the normal.
- **Scale of an M-estimator.** The [Huber M-estimator](/huber-m-estimator/) and [Tukey's biweight](/tukey-biweight/) use the normalized MAD as a fixed scale, to make the location estimate scale equivariant.
- **Outlier rules.** The rule $|x_i - \operatorname{med}| / \hat\sigma > 3$ (or 2.5) flags outliers. It is the robust form of the z-score rule, and [statistical outlier removal](/statistical-outlier-removal/) for point clouds uses a related rule.

## References
