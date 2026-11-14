---
tag: 2M9Y88
kind: definition
slug: pivotal-quantity
name: Pivotal quantity
aliases:
- pivot method
area: statistics-and-inference/hypothesis-testing
level: core
summary: A function of the data and the parameter whose distribution does not depend on the parameter. Inverting its quantiles gives an exact confidence interval.
prereqs: [sampling-distribution, confidence-interval, random-variable]
see_also: [t-confidence-interval, test-interval-duality, prediction-interval, fieller-theorem, clopper-pearson-interval, bootstrap-t-interval, student-t-test, welch-t-test]
sources:
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 9.2 (methods of finding interval estimators, with the subsections on pivotal quantities and on pivoting the CDF)
  - book: isbn:9780387988641
    title: E. L. Lehmann and Joseph P. Romano, Testing Statistical Hypotheses, third edition, Springer, 2005
    locator: Section 3.5 (confidence bounds) and Chapter 5 (confidence intervals and families of tests)
  - paper: doi:10.1098/rsta.1937.0005
    title: Jerzy Neyman, Outline of a theory of statistical estimation based on the classical theory of probability, Philosophical Transactions of the Royal Society A 236, 1937
    locator: pp. 333 to 380 (confidence intervals and their construction)
---

A pivotal quantity, or pivot, is a function $Q(X, \theta)$ of the data and the parameter whose distribution is the same for every value of the parameter. It is not a [statistic](/estimator/), because it contains the unknown $\theta$, but its [sampling distribution](/sampling-distribution/) is known exactly. Taking two quantiles of that known law and solving for $\theta$ gives a [confidence interval](/confidence-interval/) whose coverage is exactly $1 - \alpha$ for every $\theta$. The t ratio $(\bar X - \mu)/(S/\sqrt n)$ of normal data is the standard example.

## Definition

Let $X = (X_1, \ldots, X_n)$ have a law $P_\theta$ with $\theta \in \Theta$, possibly $\theta = (\psi, \lambda)$ with a parameter of interest $\psi$ and a nuisance parameter $\lambda$.

**Pivot.** A measurable function $Q(X, \psi)$ is a *pivotal quantity* for $\psi$ if the law of $Q(X, \psi)$ under $P_\theta$, with $\psi$ the first part of $\theta$, is the same for every $\theta \in \Theta$. In particular it may depend on neither $\psi$ nor $\lambda$.

**Interval from a pivot.** Let $G$ be the common law of $Q$, and choose $a \le b$ with $G([a, b]) \ge 1 - \alpha$, for example the $\alpha/2$ and $1 - \alpha/2$ quantiles. Define

$$C(x) = \{\psi : a \le Q(x, \psi) \le b\}.$$

Then for every $\theta$, $P_\theta(\psi \in C(X)) = P_\theta(a \le Q(X, \psi) \le b) = G([a, b])$. The first equality holds because the two events are the same event; the second holds because the law of $Q(X, \psi)$ under $P_\theta$ is $G$. So the coverage equals $G([a, b])$ for every $\theta$: exactly $1 - \alpha$ when $G$ is continuous and $a$, $b$ are quantiles. This is a full proof. If $Q(x, \psi)$ is monotone in $\psi$ for each $x$, then $C(x)$ is an interval; otherwise it can be a union of intervals or unbounded, as in [Fieller's theorem](/fieller-theorem/). The coverage is marginal, over the sampling distribution at a fixed $\theta$.

**Approximate pivot.** $Q_n(X, \psi)$ is an *asymptotic pivot* if it converges in distribution to the same law $G$ under every $\theta$. The interval then has coverage tending to $G([a, b])$ at each fixed $\theta$, but not necessarily uniformly in $\theta$.

**Pivoting the CDF.** If a real statistic $T$ has a continuous distribution function $F_T(t; \psi)$ under every $\theta$ that depends on $\theta$ only through $\psi$, then $F_T(T; \psi)$ is uniform on $(0, 1)$, so it is a pivot. This turns any such statistic into an interval. For a discrete $T$ the transform is not exactly uniform, and inverting the two tails gives a conservative interval instead, such as the [Clopper-Pearson interval](/clopper-pearson-interval/).

## Examples and non-examples

The examples use the five values $x = (4.1, 5.3, 4.8, 6.0, 5.2)$, with $\bar x = 5.08$ and $s^2 = 0.487$ (divisor $n - 1 = 4$), unless they say otherwise. Quantiles are lower quantiles.

**Normal mean, $\sigma$ known.** $Z = (\bar X - \mu)/(\sigma/\sqrt n) \sim N(0, 1)$ for every $\mu$. Solving $-z_{0.975} \le Z \le z_{0.975}$ for $\mu$ gives $\bar X \pm z_{0.975}\, \sigma/\sqrt n$.

**Normal mean, $\sigma$ unknown.** $T = (\bar X - \mu)/(S/\sqrt n)$ has the Student t law with $n - 1$ degrees of freedom for every $(\mu, \sigma)$, because $\bar X$ and $S^2$ are independent with known laws (Student 1908; see [sampling distribution](/sampling-distribution/)). With $t_{(4, 0.975)} = 2.776445$ and $s/\sqrt 5 = 0.31209$, the interval is $5.08 \pm 0.86650 = [4.2135, 5.9465]$. This is the [t interval](/t-confidence-interval/). Note that $\sigma$, the nuisance parameter, cancels; this is what makes $T$ a pivot for $\mu$ in the two-parameter family.

**Normal variance.** $(n - 1) S^2/\sigma^2$ has the chi-square law with $n - 1$ degrees of freedom for every $(\mu, \sigma)$. With $\chi^2_{(4, 0.025)} = 0.48442$ and $\chi^2_{(4, 0.975)} = 11.14329$, the 95% interval for $\sigma^2$ is $[4 \times 0.487/11.14329,\; 4 \times 0.487/0.48442] = [0.1748, 4.0213]$. The interval is not symmetric about $s^2$.

**Exponential rate.** For iid exponential data with rate $\lambda$, $2\lambda \sum X_i$ has the chi-square law with $2n$ degrees of freedom. For the data $(0.8, 2.1, 0.3, 1.5, 0.9)$ with sum $5.6$, and $\chi^2_{(10, 0.025)} = 3.24697$, $\chi^2_{(10, 0.975)} = 20.48318$, the 95% interval for $\lambda$ is $[3.24697/11.2,\; 20.48318/11.2] = [0.2899, 1.8289]$.

**Uniform scale.** For iid Uniform$(0, \theta)$ data with maximum $M$, $P_\theta(M/\theta \le u) = u^n$ on $[0, 1]$ for every $\theta$, so $M/\theta$ is a pivot. From $\alpha \le (M/\theta)^n \le 1$ the interval is $[M, M \alpha^{-1/n}]$. For $n = 5$, $M = 4.1$ and $\alpha = 0.05$ it is $[4.1, 7.464]$. This interval is one-sided in shape, because the pivot has its mass near 1.

**A future observation.** $(X_{n+1} - \bar X)/(S\sqrt{1 + 1/n})$ has the t law with $n - 1$ degrees of freedom for normal data. It contains no parameter at all but involves a future value, and it gives the [prediction interval](/prediction-interval/).

**A ratio of means.** For the ratio $\rho = \mu_1/\mu_2$ of two normal means, $(\bar X - \rho \bar Y)/(S\sqrt{v_{11} - 2\rho v_{12} + \rho^2 v_{22}})$ is a t-distributed pivot. Its set $C(x)$ is a bounded interval, the complement of an interval, or the whole line, which is the content of [Fieller's theorem](/fieller-theorem/).

**Non-example: a nuisance parameter left in.** For normal data with both parameters unknown, $\bar X - \mu \sim N(0, \sigma^2/n)$ has a law that depends on $\sigma$. It is a pivot for the one-parameter family with $\sigma$ fixed, but not for the family with $\sigma$ unknown.

**Non-example: the binomial z statistic.** For $X \sim \text{Binomial}(n, p)$, the law of $(X - np)/\sqrt{np(1 - p)}$ depends on $p$; it is only an asymptotic pivot. Solving it for $p$ gives the [Wilson interval](/wilson-score-interval/), whose coverage is not exact. No exact pivot with a continuous law exists for a discrete family.

**Non-example: the wrong model.** The t ratio is a pivot only under normal data. For iid exponential data with mean 1 and $n = 5$, the 95% t interval covered the mean in 0.8816 of $r = 20000$ samples (simulation with `random.Random(1)`), not 0.95. The law of the ratio depends on the shape of the data law.

**Non-example: the Behrens-Fisher problem.** For two normal samples with unequal unknown variances, no exact pivot for $\mu_1 - \mu_2$ of the familiar studentized form is known; the [Welch t-test](/welch-t-test/) uses an approximate one.

**Not a pivot, but related: an ancillary statistic.** For $N(\mu, 1)$ data, $X_1 - X_2 \sim N(0, 2)$ for every $\mu$. Its law is free of the parameter, but it does not contain the parameter, so it cannot be solved for $\mu$. An ancillary statistic is a statistic with a parameter-free law; a pivot is a function of data and parameter with a parameter-free law.

## Related definitions

- **Confidence interval.** A [confidence interval](/confidence-interval/) is any random set with a coverage statement. A pivot is one way to build one, with exact coverage; [inverting a family of tests](/test-interval-duality/) is the general way, and every pivot gives such a family: reject $\psi_0$ when $Q(x, \psi_0) \notin [a, b]$.
- **Studentization.** Dividing an estimator's error by an estimate of its [standard error](/standard-error/) removes a scale nuisance parameter, as in the t ratio. The [bootstrap-t interval](/bootstrap-t-interval/) uses a studentized quantity as an approximate pivot and estimates its law by resampling.
- **Fiducial inference.** Fisher's fiducial argument (1930) also starts from a pivot, but reads the pivot's law as a distribution for $\theta$ given the data. That is a different claim from coverage over repeated samples; this page uses only the coverage reading.
- **Location and scale families.** If $X_i = \mu + \sigma \varepsilon_i$ with $\varepsilon_i$ from a fixed law, then for equivariant estimators $\hat\mu$ and $\hat\sigma$, the quantities $(\hat\mu - \mu)/\hat\sigma$ and $\hat\sigma/\sigma$ are pivots. This is why exact pivots are common in these families and rare elsewhere.

## References
