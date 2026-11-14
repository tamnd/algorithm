---
tag: 8EGW3R
kind: definition
slug: empirical-distribution-function
name: Empirical distribution function
aliases:
- ECDF
- empirical CDF
area: statistics-and-inference/nonparametric-and-robust-statistics
level: intro
summary: The step function that gives, at each x, the fraction of the sample at most x. It is the nonparametric MLE of the distribution function.
prereqs: [random-variable, order-statistic]
see_also: [glivenko-cantelli-theorem, dkw-inequality, kolmogorov-smirnov-test, q-q-plot, bootstrap-method, kernel-density-estimation, inverse-transform-sampling, empirical-likelihood]
sources:
  - book: isbn:9780521496032
    title: A. W. van der Vaart, Asymptotic Statistics, Cambridge University Press, 1998
    locator: Chapter 19 (empirical processes), Section 19.1 (the empirical distribution function, its pointwise laws and the Glivenko-Cantelli theorem)
  - paper: "A. N. Kolmogorov, Sulla determinazione empirica di una legge di distribuzione, Giornale dell'Istituto Italiano degli Attuari 4, 1933, pages 83 to 91"
    locator: the empirical distribution function of a sample and its largest distance from the true distribution function
  - paper: "V. Glivenko, Sulla determinazione empirica delle leggi di probabilità, Giornale dell'Istituto Italiano degli Attuari 4, 1933, pages 92 to 99"
    locator: the uniform convergence of the empirical distribution function for a continuous distribution function
  - paper: doi:10.1214/aop/1176990746
    title: P. Massart, The tight constant in the Dvoretzky-Kiefer-Wolfowitz inequality, Annals of Probability 18(3), 1990
    locator: pp. 1269 to 1283 (the bound 2 exp(-2 n epsilon^2) that gives the confidence band)
---

The empirical distribution function of a sample $x_1, \ldots, x_n$ is the function $F_n(t) = \frac{1}{n} \#\{i : x_i \le t\}$, the fraction of the sample at most $t$. It is a step function that starts at 0, rises by $1/n$ at each data point, and ends at 1. For an independent sample from a distribution function $F$, each value $F_n(t)$ is an unbiased estimate of $F(t)$, and by the [Glivenko-Cantelli theorem](/glivenko-cantelli-theorem/) the whole function converges to $F$ uniformly. It is the distribution function of the empirical measure, which puts mass $1/n$ on each data point. It is the basis of the [Kolmogorov-Smirnov test](/kolmogorov-smirnov-test/), of the [bootstrap](/bootstrap-method/), and of every plug-in estimator that applies a functional of $F$ to $F_n$.

## Definition

Let $x_1, \ldots, x_n$ be real numbers. The **empirical distribution function** is

$$F_n(t) = \frac{1}{n} \sum_{i=1}^{n} \mathbf{1}\{x_i \le t\}, \qquad t \in \mathbb{R}.$$

With the sorted values $x_{(1)} \le \cdots \le x_{(n)}$, the [order statistics](/order-statistic/), $F_n(t) = i/n$ for $x_{(i)} \le t < x_{(i+1)}$, with $x_{(0)} = -\infty$ and $x_{(n+1)} = +\infty$. A value that occurs $k$ times gives one jump of size $k/n$. $F_n$ is nondecreasing and right-continuous, with limits 0 and 1, so it is a distribution function: that of the empirical measure $P_n = \frac{1}{n} \sum_i \delta_{x_i}$.

When $X_1, \ldots, X_n$ are random with distribution function $F$, $F_n$ is a random function, and:

- **Pointwise law.** For independent $X_i$, $nF_n(t)$ is Binomial$(n, F(t))$. So $E F_n(t) = F(t)$ and $\mathrm{Var} F_n(t) = F(t)(1 - F(t))/n$, and $F_n(t)$ is asymptotically normal for each $t$ with $0 < F(t) < 1$.
- **Joint law.** For $s < t$, $\mathrm{Cov}(F_n(s), F_n(t)) = F(s)(1 - F(t))/n$. As a process, $\sqrt{n}(F_n - F)$ converges to a Brownian bridge composed with $F$.
- **Nonparametric maximum likelihood.** Among all probability measures $Q$, the product $\prod_i Q(\{x_i\})$ is largest for $Q = P_n$. If the distinct values $v_j$ occur $c_j$ times, the product is $\prod_j q_j^{c_j}$ with $q_j = Q(\{v_j\})$ and $\sum_j q_j \le 1$, and Gibbs' inequality gives the maximum at $q_j = c_j/n$. So $F_n$ is the nonparametric MLE of $F$.

## Examples and non-examples

**A small sample.** For $x = 3.1, 1.4, 2.2, 1.4, 5.0$, $n = 5$ and the value $1.4$ occurs twice. Then $F_n(1.0) = 0$, $F_n(1.4) = 2/5$ (one jump of $2/5$), $F_n(2.0) = 2/5$, $F_n(2.2) = 3/5$, $F_n(3.1) = 4/5$, $F_n(4.0) = 4/5$ and $F_n(5.0) = 1$. The sample median is $2.2$, the smallest $t$ with $F_n(t) \ge 1/2$.

**A confidence band.** The [DKW inequality](/dkw-inequality/) gives $P(\sup_t \lvert F_n(t) - F(t) \rvert > \varepsilon) \le 2e^{-2n\varepsilon^2}$, so $F_n \pm \sqrt{\ln(2/\alpha)/(2n)}$ holds all of $F$ with probability at least $1 - \alpha$. At $\alpha = 0.05$ the half-width is $0.1358$ for $n = 100$ and $0.04295$ for $n = 1000$. A pointwise 95% interval at a point with $F(t) = 1/2$ has the half-width $1.96 \cdot \frac{1}{2}/\sqrt{100} = 0.098$ for $n = 100$, narrower because it covers one point and not the whole function.

**Sampling from it.** Drawing from $F_n$ by [inverse transform sampling](/inverse-transform-sampling/) is the same as drawing one of the data points uniformly at random. This is the resampling step of the nonparametric bootstrap.

**Non-example: the left-continuous version.** $\frac{1}{n} \#\{i : x_i < t\}$ agrees with $F_n$ except at the data points, where it takes the value before the jump. It is the empirical version of $P(X < t)$, not of the distribution function.

**Non-example: plotting positions.** Q-Q plots often place the $i$-th order statistic at the level $(i - 1/2)/n$ or $i/(n+1)$. These levels are not values of $F_n$; they are chosen so that the extreme points do not land at levels 0 or 1.

**Non-example: a smoothed estimate.** Integrating a [kernel density estimate](/kernel-density-estimation/) gives a continuous estimate of $F$. It is not a step function and it is not $F_n$, although it tends to $F_n$ at every point other than the data points as the bandwidth tends to 0.

**Non-example: censored data.** With right-censored times, the fraction of observed times at most $t$ is biased. The [Kaplan-Meier estimator](/kaplan-meier-estimator/) is the nonparametric MLE in that case, and it equals $1 - F_n$ when no time is censored.

## Related definitions

- **Empirical measure.** $P_n(A) = \frac{1}{n} \#\{i : x_i \in A\}$ for any set $A$. $F_n(t) = P_n((-\infty, t])$. It also makes sense for data in $\mathbb{R}^d$ or in any space.
- **Empirical quantile function.** $F_n^{-1}(p) = \inf\{t : F_n(t) \ge p\} = x_{(\lceil np \rceil)}$ for $0 < p \le 1$. Sample [quantiles](/quantile/) and the sample median are its values.
- **Empirical process.** $\sqrt{n}(F_n(t) - F(t))$ as a function of $t$. Its sup is $\sqrt{n}$ times the Kolmogorov-Smirnov statistic.
- **Empirical survival function.** $1 - F_n(t)$, the fraction of the sample above $t$.

## References
