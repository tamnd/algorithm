---
tag: J755M3
kind: concept
slug: variance
name: Variance
aliases:
- standard deviation
area: foundations/probabilistic-analysis
level: intro
summary: The expected squared deviation from the mean; variance of a sum of independent variables is the sum of variances.
prereqs: [random-variable, expected-value, linearity-of-expectation]
see_also: [chebyshev-inequality, independent-random-variables, indicator-random-variable, law-of-large-numbers, central-limit-theorem, coupon-collector-problem, expected-number-of-inversions, moment-generating-function]
sources:
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 3.2, Variance and Moments of a Random Variable (3.2.1, the variance of a binomial random variable), and Section 3.3.1, the coupon collector's problem
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C, Section C.3, Discrete random variables (variance and standard deviation), and Section C.4 (the geometric and binomial distributions)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.1.1, Inversions (the mean and the variance of the number of inversions)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.2.2, Accuracy of Floating Point Arithmetic (the stable recurrence for the mean and the standard deviation)
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume 1, third edition
    locator: Chapter IX, Random Variables; Expectation (variance, covariance, the variance of a sum)
---

The variance of a [random variable](/random-variable/) $X$ with finite mean $\mu = \mathrm{E}[X]$ is $\mathrm{Var}[X] = \mathrm{E}[(X - \mu)^2]$, the [expected](/expected-value/) squared distance of $X$ from its mean. Its square root is the standard deviation, which has the same unit as $X$. The variance of a sum is the sum of the variances plus twice the sum of the covariances, so for pairwise [independent](/independent-random-variables/) variables it is the sum of the variances. With [Chebyshev's inequality](/chebyshev-inequality/) it turns a mean into a bound on how far a running time or a count strays from that mean.

## In plain words

The mean of a random quantity says where it is on average. It does not say how far a single run can be from that average. Two programs can both take one second on average, while one always takes one second and the other takes either a tenth of a second or ten seconds.

The variance measures this spread. Take the distance of the result from the mean, square it so that misses on both sides count, and average over all runs. A small variance says that most runs land near the mean. The standard deviation is the square root of the variance, so it is in seconds again, not in seconds squared.

For a sum of parts that do not influence each other, the spreads add. This rule lets you bound the spread of a total count by looking at one part at a time.

## The idea

### Definition

Let $X$ be a real random variable on a [probability space](/probability-space/), with $\mathrm{E}[X^2] < \infty$. Then $\mathrm{E}[|X|] < \infty$ too, because $|x| \le 1 + x^2$, so $\mu = \mathrm{E}[X]$ is a finite number. Define

$$\mathrm{Var}[X] = \mathrm{E}\big[(X - \mu)^2\big], \qquad \sigma_X = \sqrt{\mathrm{Var}[X]}.$$

If $\mathrm{E}[|X|] < \infty$ but $\mathrm{E}[X^2] = \infty$, we say that $X$ has infinite variance. $\mathrm{Var}[X] \ge 0$, because $(X - \mu)^2 \ge 0$. Equality holds exactly when $\Pr[X = \mu] = 1$, because a non-negative variable has mean 0 exactly when it is 0 with probability 1.

For two variables $X, Y$ with finite second moments, the covariance is

$$\mathrm{Cov}(X, Y) = \mathrm{E}\big[(X - \mathrm{E}[X])(Y - \mathrm{E}[Y])\big].$$

It is finite, because $|ab| \le \frac12(a^2 + b^2)$. So $\mathrm{Var}[X] = \mathrm{Cov}(X, X)$.

### Basic rules, with proofs

**Rule 1 (shortcut).** $\mathrm{Var}[X] = \mathrm{E}[X^2] - \mathrm{E}[X]^2$, and $\mathrm{Cov}(X, Y) = \mathrm{E}[XY] - \mathrm{E}[X]\,\mathrm{E}[Y]$.

*Proof.* Expand the product and use [linearity of expectation](/linearity-of-expectation/), with $\mu_X, \mu_Y$ constants: $\mathrm{E}[(X - \mu_X)(Y - \mu_Y)] = \mathrm{E}[XY] - \mu_Y\mathrm{E}[X] - \mu_X\mathrm{E}[Y] + \mu_X\mu_Y = \mathrm{E}[XY] - \mu_X\mu_Y$. Put $Y = X$ for the first identity. $\square$

**Rule 2 (affine maps).** For constants $a, b$, $\mathrm{Var}[aX + b] = a^2\,\mathrm{Var}[X]$, and so $\sigma_{aX+b} = |a|\,\sigma_X$.

*Proof.* $\mathrm{E}[aX + b] = a\mu + b$, so $(aX + b) - (a\mu + b) = a(X - \mu)$. Square it and take the mean. $\square$

A shift does not change the spread, and a scale by $a$ scales the variance by $a^2$.

**Rule 3 (variance of a sum).** Let $X_1, \ldots, X_n$ have finite second moments. Then

$$\mathrm{Var}\Big[\sum_{i=1}^n X_i\Big] = \sum_{i=1}^n \mathrm{Var}[X_i] + 2\sum_{1 \le i < j \le n} \mathrm{Cov}(X_i, X_j).$$

*Proof.* Let $\mu_i = \mathrm{E}[X_i]$ and $D_i = X_i - \mu_i$. By linearity, $\mathrm{E}[\sum_i X_i] = \sum_i \mu_i$, so $\sum_i X_i - \mathrm{E}[\sum_i X_i] = \sum_i D_i$. Then

$$\Big(\sum_i D_i\Big)^2 = \sum_{i=1}^n \sum_{j=1}^n D_i D_j = \sum_i D_i^2 + 2\sum_{i<j} D_i D_j.$$

Each term has a finite mean by the bound $|ab| \le \frac12(a^2 + b^2)$. Take expectations and use linearity: $\mathrm{E}[D_i^2] = \mathrm{Var}[X_i]$ and $\mathrm{E}[D_i D_j] = \mathrm{Cov}(X_i, X_j)$. $\square$

**Rule 4 (independent terms).** If $X_i$ and $X_j$ are independent, then $\mathrm{E}[X_i X_j] = \mathrm{E}[X_i]\,\mathrm{E}[X_j]$ (proved on the page [independent random variables](/independent-random-variables/)), so $\mathrm{Cov}(X_i, X_j) = 0$ by Rule 1. Hence, if the $X_i$ are **pairwise** independent,

$$\mathrm{Var}\Big[\sum_{i=1}^n X_i\Big] = \sum_{i=1}^n \mathrm{Var}[X_i].$$

The proof uses only one pair at a time, so pairwise independence is enough. Mutual independence is not needed. Zero covariance (uncorrelated terms) is also enough, and it is weaker than independence.

## Examples

**Bernoulli.** If $X = 1$ with probability $p$ and $X = 0$ otherwise, then $X^2 = X$, so $\mathrm{Var}[X] = p - p^2 = p(1 - p)$. This is at most $\frac14$, at $p = \frac12$. Each [indicator random variable](/indicator-random-variable/) $I\{A\}$ has variance $\Pr[A](1 - \Pr[A])$.

**Binomial.** A [binomial](/binomial-distribution/) variable with parameters $n, p$ is a sum of $n$ independent Bernoulli($p$) variables, so by Rule 4 its variance is $np(1 - p)$. For 100 fair coin flips, the mean is 50, the variance is 25 and the standard deviation is 5.

**Geometric.** Let $X$ count the trials up to and including the first success, with success probability $p \in (0, 1]$ and $q = 1 - p$, so $\Pr[X = k] = q^{k-1}p$ for $k \ge 1$. The mean is $1/p$ (see the [geometric distribution](/geometric-distribution/)). Differentiate $\sum_{k \ge 0} x^k = 1/(1 - x)$ twice for $|x| < 1$ to get $\sum_{k \ge 2} k(k-1)x^{k-2} = 2/(1 - x)^3$. With $x = q$,

$$\mathrm{E}[X(X - 1)] = pq\sum_{k \ge 2} k(k-1)q^{k-2} = \frac{2pq}{p^3} = \frac{2q}{p^2}.$$

So $\mathrm{Var}[X] = \mathrm{E}[X(X-1)] + \mathrm{E}[X] - \mathrm{E}[X]^2 = \frac{2q}{p^2} + \frac1p - \frac1{p^2} = \frac{2q + p - 1}{p^2} = \frac{q}{p^2}$. For $p = \frac13$ the mean is 3 and the variance is 6. The standard deviation is about $2.45$, close to the mean: a geometric wait is not concentrated.

**The number of hires.** In the [hiring problem](/hiring-problem/), candidates arrive in a uniformly random order, and we hire candidate $i$ when $i$ is better than all of candidates $1, \ldots, i-1$. Let $X_i = I\{\text{candidate } i \text{ is hired}\}$ and $X = \sum_i X_i$. The page [indicator random variable](/indicator-random-variable/) shows $\mathrm{E}[X] = H_n = \sum_{i=1}^n 1/i$. For the spread we need more than the means of the $X_i$.

The $X_i$ are mutually independent, with $\Pr[X_i = 1] = 1/i$. The proof maps each order to the vector of relative ranks $(r_1, \ldots, r_n)$, where $r_i \in \{1, \ldots, i\}$ is the rank of candidate $i$ among the first $i$; this map is a bijection onto a product set, so the $r_i$ are independent and uniform. It is on the page [independent random variables](/independent-random-variables/). Below we use $r_i$ with the convention that rank $i$ is the best, so $X_i = I\{r_i = i\}$.

By Rule 4 and the Bernoulli case,

$$\mathrm{Var}[X] = \sum_{i=1}^n \frac1i\Big(1 - \frac1i\Big) = H_n - H_n^{(2)}, \qquad H_n^{(2)} = \sum_{i=1}^n \frac1{i^2}.$$

| $n$ | $\mathrm{E}[X] = H_n$ | $\mathrm{Var}[X]$ | $\sigma_X$ |
|---|---|---|---|
| 10 | 2.929 | 1.379 | 1.174 |
| 100 | 5.187 | 3.552 | 1.885 |

The variance is less than $H_n \le \ln n + 1$, so the number of hires is $\ln n + O(\sqrt{\log n})$ in the typical case.

**The number of inversions: dependent indicators.** Let $\pi$ be a uniformly [random permutation](/random-permutation/) of $\{1, \ldots, n\}$ and let $I$ be its number of [inversions](/inversion/), pairs of positions $i < j$ with $\pi(i) > \pi(j)$. The indicators $X_{ij} = I\{\pi(i) > \pi(j)\}$ each have mean $\frac12$ and variance $\frac14$, and the page [indicator random variable](/indicator-random-variable/) gets $\mathrm{E}[I] = n(n-1)/4$ from them. But they are not independent. For $n = 3$:

- $\mathrm{Cov}(X_{12}, X_{23}) = \Pr[\pi(1) > \pi(2) > \pi(3)] - \frac14 = \frac16 - \frac14 = -\frac1{12}$.
- $\mathrm{Cov}(X_{12}, X_{13}) = \Pr[\pi(1) \text{ is the largest of three}] - \frac14 = \frac13 - \frac14 = \frac1{12}$.

So summing $\frac14$ over the $\binom n2$ pairs gives the wrong answer $n(n-1)/8$. A clean route avoids the covariances. Let $b_j$ be the number of $i < j$ with $\pi(i) > \pi(j)$, the $j$-th entry of the [inversion table](/inversion-table/) read by position. Then $b_j = j - r_j$ with $r_j$ as in the hiring example, so the $b_j$ are independent and $b_j$ is uniform on $\{0, \ldots, j-1\}$. A uniform variable $U$ on $\{0, \ldots, j-1\}$ has $\mathrm{E}[U] = \frac{j-1}2$ and $\mathrm{E}[U^2] = \frac{(j-1)(2j-1)}6$, so

$$\mathrm{Var}[U] = \frac{(j-1)(2j-1)}{6} - \frac{(j-1)^2}{4} = \frac{(j-1)(j+1)}{12} = \frac{j^2 - 1}{12}.$$

Since $I = \sum_j b_j$, Rule 4 gives

$$\mathrm{Var}[I] = \sum_{j=1}^n \frac{j^2 - 1}{12} = \frac1{12}\Big(\frac{n(n+1)(2n+1)}{6} - n\Big) = \frac{n(n-1)(2n+5)}{72}.$$

For $n = 1, \ldots, 7$ this gives $0, \frac14, \frac{11}{12}, \frac{13}{6}, \frac{25}{6}, \frac{85}{12}, \frac{133}{12}$, the same values as an enumeration of all $n!$ permutations. Knuth derives the same mean and variance with generating functions.

| $n$ | $\mathrm{E}[I]$ | wrong value $n(n-1)/8$ | $\mathrm{Var}[I]$ | $\sigma_I$ |
|---|---|---|---|---|
| 10 | 22.5 | 11.25 | 31.25 | 5.59 |
| 100 | 2475 | 1237.5 | 28187.5 | 167.9 |

The covariances are positive in total here. The ratio of the wrong value to the true one is $9/(2n+5)$: it is $0.36$ at $n = 10$, and it tends to 0, because the true variance is $\Theta(n^3)$ and the wrong value is $\Theta(n^2)$.

**The coupon collector.** Let $X$ be the number of uniform draws from $n$ coupon types until each type is seen. Write $X = \sum_{i=1}^n G_i$, where $G_i$ is the number of draws while exactly $i-1$ types are seen. The $G_i$ are independent and geometric with $p_i = (n - i + 1)/n$. So $\mathrm{E}[X] = nH_n$ and

$$\mathrm{Var}[X] = \sum_{i=1}^n \frac{1 - p_i}{p_i^2} \le \sum_{i=1}^n \frac{n^2}{(n - i + 1)^2} < \frac{\pi^2 n^2}{6}.$$

For $n = 100$, $\mathrm{E}[X] = 518.74$, $\mathrm{Var}[X] = 15831.1$ and $\sigma_X = 125.8$, against the bound $\pi^2 n^2/6 = 16449.3$. This is the analysis of [the coupon collector's problem](/coupon-collector-problem/) in Mitzenmacher and Upfal, Section 3.3.1.

## Where it is used

- **Chebyshev's inequality.** [Chebyshev's inequality](/chebyshev-inequality/) says $\Pr[|X - \mu| \ge a] \le \mathrm{Var}[X]/a^2$. For the inversions above, with $a = n^{3/2}$, the bound is $\mathrm{Var}[I]/n^3 = \frac{(n-1)(2n+5)}{72n^2} < \frac1{36} + \frac1{24n}$, which is $0.0282$ at $n = 100$. So [insertion sort](/insertion-sort/), which shifts items once for each inversion, makes $n(n-1)/4 \pm n^{3/2}$ shifts on a random input of 100 or more items with probability above $0.97$. For the coupon collector, $\Pr[|X - nH_n| \ge nH_n] \le \pi^2/(6H_n^2)$, which is $0.061$ at $n = 100$.
- **Laws of large numbers.** The mean of $k$ independent copies of $X$ has variance $\mathrm{Var}[X]/k$ by Rules 2 and 4. With Chebyshev this gives the weak [law of large numbers](/law-of-large-numbers/), and the [central limit theorem](/central-limit-theorem/) describes the shape of the spread at scale $\sigma/\sqrt k$.
- **Sampling and estimation.** A [Monte Carlo](/monte-carlo-integration/) estimate or a sketch such as [count sketch](/count-sketch/) or the [AMS sketch](/ams-sketch/) is a random variable whose mean is the target. Its variance sets how many copies to average, and the [median trick](/median-trick/) then boosts the success probability.
- **Pairwise independent hashing.** Rule 4 needs only pairwise independence, so a [pairwise independent hash family](/k-wise-independent-hashing/) gives the same variance bounds as truly random hashing. Mitzenmacher and Upfal, Chapter 15, build on this.
- **Second moment method.** $\Pr[X = 0] \le \mathrm{Var}[X]/\mathrm{E}[X]^2$ follows from Chebyshev with $a = \mathrm{E}[X]$. It shows that a count with a large mean is positive with high probability, as in the [probabilistic method](/probabilistic-method/).
- **Tail bounds.** Variance gives polynomial tails. When the terms are independent, the [moment generating function](/moment-generating-function/) gives exponential tails, as in the [Chernoff bound](/chernoff-bound/).

### Pitfalls

- **Adding variances of dependent terms.** Rule 4 needs zero covariance. The inversion indicators show the error: the naive sum gives $11.25$ at $n = 10$, against the true $31.25$. Linearity of expectation needs no independence, but the variance of a sum does.
- **$\mathrm{Var}[2X]$ is not $\mathrm{Var}[X + X']$.** For one variable used twice, $\mathrm{Var}[2X] = 4\,\mathrm{Var}[X]$. For two independent copies, $\mathrm{Var}[X + X'] = 2\,\mathrm{Var}[X]$. Reusing one random choice in two places doubles the standard deviation instead of multiplying it by $\sqrt 2$.
- **Infinite variance.** A finite mean does not give a finite variance. Let $\Pr[X = k] = c/k^3$ for $k \ge 1$, with $c = 1/\sum_k k^{-3} = 0.8319\ldots$. Then $\mathrm{E}[X] = c\,\pi^2/6 = 1.368\ldots$, but $\mathrm{E}[X^2] = c\sum_k 1/k$ diverges. Chebyshev's inequality then says nothing.
- **Units.** The variance is in squared units. Compare the standard deviation, not the variance, with the mean: $\mathrm{Var}[X] = 25$ for 100 coin flips means a typical deviation of 5 heads.
- **Uncorrelated is not independent.** Let $X$ be uniform on $\{-1, 0, 1\}$ and $Y = X^2$. Then $\mathrm{Cov}(X, Y) = \mathrm{E}[X^3] - 0 = 0$, but $Y$ is a function of $X$. Rule 4 still holds for such terms, but a bound that needs independence, such as the Chernoff bound, does not.
- **Population and sample variance.** For observed values $x_1, \ldots, x_m$ with average $\bar x$, the average of $(x_k - \bar x)^2$ divides by $m$ and has mean $\frac{m-1}{m}\mathrm{Var}[X]$ for independent samples. Divide by $m - 1$ for an unbiased estimate.
- **Cancellation in floating point.** The formula $\mathrm{E}[X^2] - \mathrm{E}[X]^2$ subtracts two large, close numbers. For the four values $10^9 + 4$, $10^9 + 7$, $10^9 + 13$, $10^9 + 16$, the true population variance is $22.5$, but this formula in IEEE double precision returns $0.0$. The recurrence of Welford, given by Knuth in Section 4.2.2, keeps a running mean $M_k = M_{k-1} + (x_k - M_{k-1})/k$ and a sum $S_k = S_{k-1} + (x_k - M_{k-1})(x_k - M_k)$, and returns $S_m/m = 22.5$ here. This is a case of [catastrophic cancellation](/catastrophic-cancellation/).

## References
