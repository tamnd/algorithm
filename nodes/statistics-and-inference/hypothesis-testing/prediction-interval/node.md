---
tag: KKNWHF
kind: definition
slug: prediction-interval
name: Prediction interval
aliases:
- predictive interval
area: statistics-and-inference/hypothesis-testing
level: core
summary: An interval that contains a future observation, not a parameter, with a stated probability. It is wider than the confidence interval for the mean.
prereqs: [confidence-interval, pivotal-quantity, t-confidence-interval]
see_also: [conformal-prediction, split-conformal-prediction, order-statistic, posterior-predictive-distribution, credible-interval, highest-posterior-density-interval, ordinary-least-squares, test-interval-duality]
sources:
  - book: isbn:9780471687177
    title: William Q. Meeker, Gerald J. Hahn and Luis A. Escobar, Statistical Intervals, A Guide for Practitioners and Researchers, second edition, Wiley, 2017
    locator: Chapter 2 (types of intervals), Chapter 4 (normal-distribution prediction intervals), Chapter 5 (distribution-free intervals, Section 5.4 on ordered observations) and Appendix E.6 (prediction intervals from pivotal quantities)
  - book: isbn:9780387001524
    title: Vladimir Vovk, Alex Gammerman and Glenn Shafer, Algorithmic Learning in a Random World, Springer, 2005
    locator: Chapter 2 (conformal prediction and its validity under exchangeability)
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Chapter 5 (the t distribution and order statistics) and Chapter 9 (interval estimation)
---

A prediction interval is an interval, computed from observed data $X_1, \ldots, X_n$, that contains a *future* observation $Y$ with a stated probability $1 - \alpha$. The target is a random variable, not a fixed parameter, so the interval must allow both for the error in estimating the parameters and for the spread of $Y$ itself. For normal data the exact interval is $\bar X \pm t_{(n-1, 1-\alpha/2)}\, S\sqrt{1 + 1/n}$, which is wider than the [t confidence interval](/t-confidence-interval/) for the mean by the factor $\sqrt{n + 1}$ and does not shrink to a point as $n$ grows.

## Definition

Let $X = (X_1, \ldots, X_n)$ and a future value $Y$ have a joint law $P_\theta$, $\theta \in \Theta$. Usually $X_1, \ldots, X_n, Y$ are iid, or $Y$ is a new response at a known covariate value in a regression.

**Prediction interval.** A pair of statistics $L(X) \le U(X)$ is a *prediction interval of level $1 - \alpha$* for $Y$ if

$$P_\theta\big(L(X) \le Y \le U(X)\big) \ge 1 - \alpha \quad \text{for every } \theta \in \Theta.$$

The probability is over both $X$ and $Y$. This is *marginal* coverage. The *conditional* coverage $\pi(X) = P_\theta(L(X) \le Y \le U(X) \mid X)$ is a random variable whose mean is the marginal coverage; the definition does not ask that it be at least $1 - \alpha$ for each data set. A one-sided *prediction bound* has $L = -\infty$ or $U = +\infty$.

**Construction from a pivot.** If $Q(X, Y)$ has a law $G$ that is the same for every $\theta$, then $\{y : a \le Q(X, y) \le b\}$ with $G([a, b]) \ge 1 - \alpha$ is a prediction set of level $1 - \alpha$. The proof is the one on the [pivotal quantity](/pivotal-quantity/) page, with $Y$ in place of the parameter: the event that $Y$ is in the set is the event $a \le Q(X, Y) \le b$.

**Normal model.** If $X_1, \ldots, X_n, Y$ are iid $N(\mu, \sigma^2)$ with both parameters unknown, then $Y - \bar X \sim N(0, \sigma^2(1 + 1/n))$, it is independent of $S^2$ (since $Y$ is independent of the sample and $\bar X$ is independent of $S^2$), and $(n - 1)S^2/\sigma^2$ is chi-square with $n - 1$ degrees of freedom. So

$$\frac{Y - \bar X}{S\sqrt{1 + 1/n}} \sim t_{n-1}$$

for every $(\mu, \sigma)$, and the interval $\bar X \pm t_{(n-1, 1-\alpha/2)}\, S\sqrt{1 + 1/n}$ has marginal coverage exactly $1 - \alpha$. Here $t_{(n-1, p)}$ is the lower $p$ quantile.

**Distribution-free interval from order statistics.** Let $X_1, \ldots, X_n, Y$ be iid from any continuous law, and let $X_{(1)} < \cdots < X_{(n)}$ be the [order statistics](/order-statistic/) of the sample. For $0 \le j < k \le n + 1$, with $X_{(0)} = -\infty$ and $X_{(n+1)} = +\infty$,

$$P\big(X_{(j)} < Y < X_{(k)}\big) = \frac{k - j}{n + 1}.$$

*Proof.* The $n + 1$ values are iid and continuous, so they are distinct with probability 1, and every ordering of them is equally likely. The rank $R$ of $Y$ among them is therefore uniform on $\{1, \ldots, n + 1\}$. $Y$ lies strictly between $X_{(j)}$ and $X_{(k)}$ exactly when $j + 1 \le R \le k$, which happens for $k - j$ of the $n + 1$ ranks. $\square$

The proof uses only that the $n + 1$ values are exchangeable with no ties, and it holds for every continuous law. This is the simplest case of [conformal prediction](/conformal-prediction/), which ranks a conformity score instead of the raw value.

## Examples and non-examples

The examples use the data $x = (4.1, 5.3, 4.8, 6.0, 5.2)$, with $\bar x = 5.08$, $s = 0.697854$ and $t_{(4, 0.975)} = 2.776445$.

**Normal prediction interval.** The 95% interval is $5.08 \pm 2.776445 \times 0.697854 \times \sqrt{1.2} = 5.08 \pm 2.12248 = [2.9575, 7.2025]$. The 95% t confidence interval for $\mu$ from the same data is $[4.2135, 5.9465]$. The ratio of the half-widths is $\sqrt{1 + 1/n}/\sqrt{1/n} = \sqrt 6 = 2.449$. As $n \to \infty$ the prediction interval tends to $\mu \pm z_{0.975}\sigma$, of width about $3.92\sigma$, while the confidence interval shrinks to the point $\mu$.

**Order-statistic interval.** For the same five values, $[X_{(1)}, X_{(5)}] = [4.1, 6.0]$ has coverage $4/6 = 0.667$ for any continuous law. To reach 95% with the range $[X_{(1)}, X_{(n)}]$ one needs $(n - 1)/(n + 1) \ge 0.95$, that is $n \ge 39$. With $n = 19$ the range has coverage $18/20 = 0.90$; a simulation of 20000 uniform samples (seed 3) gave 0.8978.

**Conditional coverage varies.** For normal data with $n = 5$, the conditional coverage $\pi(X)$ of the 95% interval has mean 0.95 but is spread out. In 20000 simulated samples (seed 1) its median was 0.990, it was below 0.90 in 15.5% of samples and below 0.80 in 6.8%. These are measured, not proved. A tolerance interval, which asks that $\pi(X) \ge \beta$ with confidence $\gamma$, controls this, and is wider.

**Regression.** In the [least squares](/ordinary-least-squares/) linear model $Y = x^\top \beta + \varepsilon$ with normal errors and $p$ coefficients, a new response at $x_0$ has the interval $x_0^\top \hat\beta \pm t_{(n-p, 1-\alpha/2)}\, S\sqrt{1 + x_0^\top (X^\top X)^{-1} x_0}$. The confidence interval for the mean response $x_0^\top \beta$ has the same form without the 1 under the root.

**Non-example: the normal interval on skewed data.** The t-based interval is exact only for normal data. For iid exponential data with mean 1, simulation with 20000 repetitions (seed 2) gave coverage 0.923 at $n = 5$ and 0.945 at $n = 50$. At $n = 50$ the total is close to 0.95, but all of the misses were above the interval (5.5%) and none below, so each one-sided bound is wrong. Unlike a confidence interval for the mean, the prediction interval does not become valid as $n$ grows under the central limit theorem, because $Y$ keeps its own non-normal law.

**Non-example: a confidence interval used to predict.** The 95% t confidence interval $[4.2135, 5.9465]$ for $\mu$ does not contain a new observation with probability 0.95. For normal data with $n = 5$ its marginal coverage of $Y$ is $P(\lvert T \rvert \le 2.776445/\sqrt 6)$ for $T \sim t_4$, which is 0.680.

**Non-example: a credible interval for $\mu$.** A Bayesian [credible interval](/credible-interval/) for $\mu$ is a statement about the parameter, like a confidence interval. The Bayesian analogue of a prediction interval is an interval of the [posterior predictive distribution](/posterior-predictive-distribution/), and its highest-density form is the [HPD](/highest-posterior-density-interval/) region of that distribution. With the reference prior $p(\mu, \sigma) \propto 1/\sigma$ and normal data, the 95% posterior predictive interval equals the frequentist interval $\bar x \pm t_{(n-1, 0.975)}\, s\sqrt{1 + 1/n}$, but its probability is conditional on the data, not marginal over samples.

## Related definitions

- **Confidence interval.** A [confidence interval](/confidence-interval/) covers a fixed parameter. A prediction interval covers a random future value, so it adds the variance of $Y$ to the variance of the estimate.
- **Tolerance interval.** An interval that contains at least a proportion $\beta$ of the population with confidence $\gamma$. It is a statement about the conditional coverage $\pi(X)$, while a prediction interval is a statement about its mean.
- **Conformal prediction.** [Conformal prediction](/conformal-prediction/) and [split conformal prediction](/split-conformal-prediction/) extend the order-statistic interval to any model and any score, with marginal coverage at least $1 - \alpha$ under exchangeability alone.
- **Test inversion.** A prediction set is the set of values $y$ that a level-$\alpha$ test of "$Y = y$ comes from the same law as the sample" does not reject; this is the [test-interval duality](/test-interval-duality/) with $Y$ in place of the parameter.

## References
