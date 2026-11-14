---
tag: SRYNEE
kind: definition
slug: u-statistic
name: U-statistic
aliases:
- Hoeffding U-statistic
area: statistics-and-inference/nonparametric-and-robust-statistics
level: advanced
summary: The average of a symmetric kernel over all subsets of size r of the sample. It is unbiased, has minimum variance in large nonparametric families, and is asymptotically normal.
prereqs: [estimator, sample-variance, sufficient-statistic, complete-statistic]
see_also: [mann-whitney-u-test, wilcoxon-signed-rank-test, jackknife-resampling, lehmann-scheffe-theorem, hoeffding-inequality, hodges-lehmann-estimator, subsampling-inference, central-limit-theorem]
sources:
  - paper: doi:10.1214/aoms/1177730196
    title: Wassily Hoeffding, A class of statistics with asymptotically normal distribution, The Annals of Mathematical Statistics 19(3), 1948
    locator: pp. 293 to 325 (the definition, the variance formula with the covariances zeta_c, and the asymptotic normality)
  - book: isbn:9780471219279
    title: Robert J. Serfling, Approximation Theorems of Mathematical Statistics, Wiley, 1980 (paperback 2002)
    locator: Chapter 5 (U-statistics, their variance, the projection, the asymptotic distribution theory and the degenerate case)
  - paper: "P. R. Halmos, The theory of unbiased estimation, The Annals of Mathematical Statistics 17(1), 34 to 43, 1946"
    title: P. R. Halmos, The theory of unbiased estimation, 1946
    locator: the symmetric unbiased estimator of a regular functional is unique and has minimum variance in a large nonparametric family
  - book: isbn:9780387985022
    title: E. L. Lehmann and George Casella, Theory of Point Estimation, second edition, Springer, 1998
    locator: Chapter 2 (unbiasedness, UMVU estimation in nonparametric families and in the normal family)
  - book: isbn:9780521496032
    title: A. W. van der Vaart, Asymptotic Statistics, Cambridge University Press, 1998
    locator: Chapter 11 (projections, the Hajek projection) and Chapter 12 (U-statistics, including the degenerate case)
---

A U-statistic is the average of a fixed function $h$, the kernel, over all subsets of $r$ distinct observations of a sample. It is an unbiased estimator of the parameter $\theta(F) = E\, h(X_1, \ldots, X_r)$, and many familiar statistics are U-statistics: the sample mean, the [sample variance](/sample-variance/), the [Mann-Whitney](/mann-whitney-u-test/) statistic and the Wilcoxon signed-rank statistic. Wassily Hoeffding (1948) defined the class and proved that its members are asymptotically normal. In a nonparametric family large enough for the order statistics to be complete, a U-statistic is the minimum variance unbiased estimator of its parameter; in a smaller, parametric family it usually is not.

## Definition

Let $X_1, \ldots, X_n$ be independent with common distribution $F$, and let $h(x_1, \ldots, x_r)$ be a function of $r \le n$ arguments that is **symmetric**, that is, unchanged by any permutation of its arguments. Suppose $\theta(F) = E_F\, h(X_1, \ldots, X_r)$ is finite. The **U-statistic** with kernel $h$ is

$$U_n = \binom{n}{r}^{-1} \sum_{1 \le i_1 < \cdots < i_r \le n} h(X_{i_1}, \ldots, X_{i_r}).$$

The number $r$ is the **degree** (or order) of the kernel. It is fixed as $n$ grows. A kernel that is not symmetric can be replaced by its average over the $r!$ orders of its arguments, which has the same expectation. A parameter of the form $\theta(F) = E_F h$ for some kernel of degree $r$ is called **regular** or **estimable** of degree $r$.

The following facts are part of the standard theory and explain why the class matters.

**Unbiased.** Each term has expectation $\theta$, so $E U_n = \theta$.

**A conditional expectation.** $U_n = E[h(X_1, \ldots, X_r) \mid X_{(1)}, \ldots, X_{(n)}]$, where $X_{(1)} \le \cdots \le X_{(n)}$ are the order statistics. Given the order statistics, the sample is a uniformly random arrangement of these values, and $(X_1, \ldots, X_r)$ is a uniformly random $r$-subset of them.

**Minimum variance, with a condition.** The order statistics are [sufficient](/sufficient-statistic/) for every family of iid laws. So, by the [Rao-Blackwell theorem](/rao-blackwell-theorem/), conditioning any unbiased estimator of $\theta$ on them gives a symmetric unbiased estimator whose variance is not larger. If the family $\mathcal F$ is large enough that the order statistics are also [complete](/complete-statistic/), for example all distributions with finite support, or all distributions with a density for which the needed moments are finite, then there is only one symmetric unbiased estimator, namely $U_n$. By the [Lehmann-Scheffé theorem](/lehmann-scheffe-theorem/) it is then the [minimum variance unbiased estimator](/minimum-variance-unbiased-estimator/) of $\theta$ over $\mathcal F$ (Halmos 1946). In a parametric family the order statistics are not complete, and a function of a smaller sufficient statistic can do better; the non-examples show a case.

**Variance.** For $0 \le c \le r$ let $\zeta_c = \mathrm{Cov}\bigl(h(X_1, \ldots, X_r),\ h(X_1, \ldots, X_c, X'_{c+1}, \ldots, X'_r)\bigr)$, the covariance of the kernel on two subsets that share exactly $c$ observations, with the $X'$ independent copies. Then $\zeta_0 = 0$ and

$$\mathrm{Var}\, U_n = \binom{n}{r}^{-1} \sum_{c=1}^{r} \binom{r}{c}\binom{n-r}{r-c}\, \zeta_c = \frac{r^2 \zeta_1}{n} + O(n^{-2}).$$

**Projection and asymptotic normality.** Let $h_1(x) = E\, h(x, X_2, \ldots, X_r) - \theta$, so $\zeta_1 = \mathrm{Var}\, h_1(X_1)$. The Hájek projection of $U_n$ onto sums of functions of single observations is $\hat U_n = \theta + \frac{r}{n}\sum_{i=1}^n h_1(X_i)$, and $E(U_n - \hat U_n)^2 = O(n^{-2})$. If $E h^2 < \infty$ and $\zeta_1 > 0$, the [central limit theorem](/central-limit-theorem/) applied to $\hat U_n$ gives

$$\sqrt n\,(U_n - \theta) \xrightarrow{d} N(0,\ r^2 \zeta_1).$$

**Degenerate kernels.** If $\zeta_1 = 0$, the kernel is degenerate, the projection is constant, and $U_n - \theta$ is of order $1/n$. For $r = 2$, $n(U_n - \theta)$ converges to $\sum_j \lambda_j (Z_j^2 - 1)$, with independent standard normal $Z_j$ and the eigenvalues $\lambda_j$ of the integral operator with kernel $h(x, y) - \theta$ (Serfling, Chapter 5).

## Examples and non-examples

**Examples.**

- **Sample mean.** $r = 1$, $h(x) = x$, $U_n = \bar X$ and $\theta = E X$.
- **Sample variance.** $r = 2$, $h(x, y) = (x - y)^2/2$. Since $E(X_1 - X_2)^2/2 = \sigma^2$, $U_n = \binom n2^{-1}\sum_{i<j}(X_i - X_j)^2/2$ estimates $\sigma^2$, and expanding the squares shows that $U_n = S^2 = \frac{1}{n-1}\sum_i (X_i - \bar X)^2$ exactly. Here $h_1(x) = ((x - \mu)^2 - \sigma^2)/2$ and $\zeta_1 = (\mu_4 - \sigma^4)/4$, so $\sqrt n(S^2 - \sigma^2) \to N(0, \mu_4 - \sigma^4)$, with $\mu_4$ the fourth central moment.
- **Gini mean difference.** $r = 2$, $h(x, y) = \lvert x - y \rvert$, which estimates $E\lvert X_1 - X_2\rvert$, a measure of spread that is less sensitive to outliers than the variance.
- **Wilcoxon signed-rank statistic.** With $h(x, y) = \mathbf 1\{x + y > 0\}$ and the differences $D_i$ of paired data, the [Wilcoxon signed-rank](/wilcoxon-signed-rank-test/) statistic is $W^+ = \sum_{i \le j}\mathbf 1\{D_i + D_j > 0\} = n U_{n,1} + \binom n2 U_{n,2}$, where $U_{n,1}$ is the fraction of positive $D_i$ (degree 1) and $U_{n,2}$ is the U-statistic with this kernel (degree 2). Its asymptotic normality follows from the theory above.
- **Mann-Whitney statistic.** A two-sample U-statistic averages a kernel over all pairs of one observation from each sample. With $h(x, y) = \mathbf 1\{x > y\} + \frac12\mathbf 1\{x = y\}$, the average over the $m n$ pairs is $U/(mn)$, the [Mann-Whitney](/mann-whitney-u-test/) statistic scaled to $[0, 1]$, which estimates $P(X > Y) + \frac12 P(X = Y)$.
- **Square of the mean.** $h(x, y) = x y$ gives $U_n = \frac{(\sum X_i)^2 - \sum X_i^2}{n(n-1)}$, an unbiased estimator of $\mu^2$, while $\bar X^2$ is biased upward by $\sigma^2/n$. Here $h_1(x) = \mu(x - \mu)$, so $\zeta_1 = \mu^2\sigma^2$. If $\mu = 0$ the kernel is degenerate, and $n U_n \to \sigma^2(Z^2 - 1)$, which is not normal.

**Non-examples.**

- **V-statistics.** The average of the kernel over all $n^r$ tuples, repeats included, is a V-statistic, or von Mises statistic. With $h(x, y) = (x - y)^2/2$ it is the plug-in variance $\frac1n\sum(X_i - \bar X)^2$, which is biased. The [jackknife](/jackknife-resampling/) bias correction turns every degree-2 V-statistic into the U-statistic with the same kernel.
- **The sample median.** It is a symmetric function of the data, but not the average of a kernel of fixed degree. It is not unbiased in general, and its asymptotic theory is that of the [quantile](/quantile/), not of U-statistics. Every symmetric statistic is trivially a U-statistic of degree $n$, which is why the definition fixes $r$.
- **Not minimum variance in the normal family.** For $X_i$ normal with unknown mean $\mu$ and variance 1, the parameter $P(X > 0) = \Phi(\mu)$ is estimated without bias by the U-statistic $\frac1n\sum\mathbf 1\{X_i > 0\}$. But $\bar X$ is complete and sufficient in this family, and the unbiased estimator $\Phi\bigl(\bar X\sqrt{n/(n-1)}\bigr)$, a function of $\bar X$, has smaller variance (Lehmann and Casella, Chapter 2). The U-statistic is the best unbiased estimator only over a large nonparametric family.
- **Infinite expectation.** For a Cauchy sample and $h(x) = x$, $E h$ does not exist, so $\theta$ is not defined and $\bar X$ is not a U-statistic estimator of anything.

## Related definitions

- **V-statistic.** The average over all $n^r$ tuples with repetition, as above. It differs from $U_n$ by $O_p(1/n)$ when the kernel has finite moments on the diagonal.
- **Hoeffding decomposition.** $U_n - \theta = \sum_{c=1}^r \binom rc \binom nc^{-1} \sum_{\lvert S\rvert = c} g_c(X_S)$, with orthogonal terms $g_c$; the first term is the Hájek projection. It gives the variance formula and the degenerate limits.
- **Generalized U-statistics.** For $k$ samples, average a kernel over all choices of $r_j$ distinct observations from sample $j$; the Mann-Whitney statistic is the case $k = 2$, $r_1 = r_2 = 1$.
- **Incomplete U-statistics.** Average the kernel over a random or designed selection of the $\binom nr$ subsets. They are still unbiased, with a larger variance; [subsampling](/subsampling-inference/) uses averages of this kind.
- **Concentration.** Hoeffding also showed that a U-statistic with a bounded kernel satisfies a [Hoeffding inequality](/hoeffding-inequality/) with $n$ replaced by $\lfloor n/r \rfloor$, because $U_n$ is an average of averages of $\lfloor n/r \rfloor$ independent terms.
- **Estimators from U-statistics.** The [Hodges-Lehmann estimator](/hodges-lehmann-estimator/) is the median of the Walsh averages, the values whose signs the Wilcoxon kernel counts.

## References
