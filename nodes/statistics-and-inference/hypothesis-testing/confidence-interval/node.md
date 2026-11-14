---
tag: KDG5NV
kind: definition
slug: confidence-interval
name: Confidence interval
aliases:
- interval estimate
- confidence set
area: statistics-and-inference/hypothesis-testing
level: intro
summary: A random interval computed from the data that contains the true parameter with a stated probability, such as 95 percent, over repeated samples.
prereqs: [estimator, standard-error, sampling-distribution]
see_also: [t-confidence-interval, test-interval-duality, pivotal-quantity, credible-interval, prediction-interval, wilson-score-interval, clopper-pearson-interval, confidence-sequence]
sources:
  - paper: doi:10.1098/rsta.1937.0005
    title: "Jerzy Neyman, Outline of a theory of statistical estimation based on the classical theory of probability, Philosophical Transactions of the Royal Society A 236, 1937, pp. 333 to 380"
    locator: The whole paper (confidence intervals and the confidence coefficient as a property of the procedure over repeated samples)
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Chapter 9 (interval estimation; Section 9.2.1 on inverting a test statistic, Section 9.2.2 on pivotal quantities, Section 9.3.1 on size and coverage probability)
  - book: isbn:9780387402727
    title: Larry Wasserman, All of Statistics, Springer, 2004
    locator: Section 6.3.2 (confidence sets, and the warning that a confidence interval is not a probability statement about the parameter)
  - book: isbn:9780387988641
    title: E. L. Lehmann and Joseph P. Romano, Testing Statistical Hypotheses, third edition, Springer, 2005
    locator: Section 5.4 (confidence intervals and families of tests)
---

A confidence interval for a parameter $\theta$ is an interval $[L(X), U(X)]$ computed from the data $X$ by a rule that, whatever the true $\theta$, covers it with probability at least $1 - \alpha$ over repeated samples. The probability belongs to the rule, not to a computed interval: after the data are in, $[L(x), U(x)]$ either contains $\theta$ or does not (Neyman, 1937). Intervals are built from pivots, such as the standardized mean of the [t interval](/t-confidence-interval/), or by collecting the null values that a level-$\alpha$ test does not reject. A confidence set is the same idea without the restriction to intervals.

## Definition

Let $X$ have distribution $P_\theta$, $\theta \in \Theta$, and let $C(X) \subseteq \Theta$ be a set computed from $X$ alone (for an interval, $C(X) = [L(X), U(X)]$).

- The **coverage probability** at $\theta$ is $P_\theta(\theta \in C(X))$; the randomness is in $X$, and $\theta$ is fixed.
- The **confidence coefficient** is $\inf_{\theta \in \Theta}P_\theta(\theta \in C(X))$.
- $C$ is a **$1 - \alpha$ confidence set** if its confidence coefficient is at least $1 - \alpha$.

The same definitions apply to a function $g(\theta)$, such as one mean when the variance is unknown, with $g(\theta) \in C(X)$ in place of $\theta \in C(X)$. One-sided sets $[L(X), \infty)$ and $(-\infty, U(X)]$ are lower and upper confidence bounds. The coverage of a rule has one of three types:

- **exact**: $P_\theta(\theta \in C(X)) = 1 - \alpha$ for every $\theta$, such as the t interval under normal data;
- **conservative**: $P_\theta(\theta \in C(X)) \ge 1 - \alpha$ for every $\theta$, with strict inequality somewhere, such as the [Clopper-Pearson interval](/clopper-pearson-interval/) for a binomial proportion;
- **asymptotic**: $P_\theta(\theta \in C(X)) \to 1 - \alpha$ as $n \to \infty$ for each $\theta$, which allows the coverage at a fixed $n$ to be far below $1 - \alpha$ for some $\theta$.

**Duality with tests.** If for each $\theta_0$ there is a level-$\alpha$ test of $H_0: \theta = \theta_0$ with acceptance region $A(\theta_0)$, then $C(x) = \{\theta_0 : x \in A(\theta_0)\}$ is a $1 - \alpha$ confidence set, because $\theta \in C(X)$ exactly when $X \in A(\theta)$, an event of probability at least $1 - \alpha$ under $\theta$. The converse holds too. This is [test-interval duality](/test-interval-duality/).

**Marginal, not conditional.** The coverage is an average over all samples. For a particular kind of sample, the coverage given that kind can differ, as the uniform example shows.

## Examples and non-examples

**A z interval.** Nine packs with known $\sigma = 4$ g have mean $4525/9 = 502.78$ g. The 95% interval $\bar x \pm 1.959964 \times 4/3$ is $[500.16, 505.39]$, exact under normal data with known $\sigma$; it excludes 500, matching the z-test p-value 0.037.

**A t interval.** For the sleep differences of Cushny and Peebles ($n = 10$, $\bar d = 1.58$, $S^2 = 1.512889$ with divisor 9), the 95% interval $1.58 \pm 2.262157 \times 0.388959$ is $[0.7001, 2.4599]$.

**Repeated sampling.** In 100 simulated samples of 10 standard normal values (seed 43), 97 of the 100 95% t intervals contained the true mean 0. The count is Binomial$(100, 0.95)$, with mean 95 and standard deviation 2.18. Which 3 intervals missed cannot be told from the intervals themselves.

**Exact marginal coverage, wrong conditional coverage.** Let $X_1, X_2$ be iid uniform on $(\theta - \tfrac12, \theta + \tfrac12)$ and $C = [\min(X_1, X_2), \max(X_1, X_2)]$. It covers $\theta$ exactly when one observation is below $\theta$ and one above, which has probability $2 \cdot \tfrac12 \cdot \tfrac12 = \tfrac12$: a 50% confidence interval. But if $\max - \min \ge \tfrac12$, the interval must contain $\theta$: two points on the same side of $\theta$ lie in an interval of length $\tfrac12$ and so are less than $\tfrac12$ apart. $X_1 - X_2$ has the triangular density on $(-1, 1)$, so $P(\max - \min \ge \tfrac12) = (\tfrac12)^2 = \tfrac14$. Given a wide interval the coverage is 1, and given a narrow one it is $(\tfrac12 - \tfrac14)/\tfrac34 = \tfrac13$. Monte Carlo with $r = 20000$ and seed 42 gives coverage 0.5021, a wide interval in 0.2505 of the samples, coverage 1 given wide and 0.3356 given narrow. Seeing a wide interval and still saying "50% confidence" is correct about the procedure and useless about this sample.

**Asymptotic coverage that fails.** The Wald interval $\hat p \pm 1.959964\sqrt{\hat p(1 - \hat p)/n}$ for a binomial proportion has nominal 95% coverage. Its exact coverage, a sum of binomial probabilities over the outcomes it covers, is 0.9586 at $n = 20$, $p = 0.5$; 0.8760 at $n = 20$, $p = 0.1$; 0.9324 at $n = 100$, $p = 0.1$; and 0.8664 at $n = 100$, $p = 0.02$. The [Wilson score interval](/wilson-score-interval/) does much better.

**Non-example: a probability statement about $\theta$.** "There is a 95% probability that the mean lies in $[0.7001, 2.4599]$" is false in the frequentist frame, where $\theta$ is fixed and the computed interval either contains it or not. A posterior probability statement of that form is what a Bayesian [credible interval](/credible-interval/) gives, under a prior.

**Non-example: a prediction interval.** An interval that covers a future observation with probability $1 - \alpha$ is a [prediction interval](/prediction-interval/); it is wider, because it adds the scatter of the new observation to the uncertainty of the estimate.

**Non-example: an error bar of one standard error.** $\hat\theta \pm \text{SE}$ is a confidence interval only with its true coefficient stated: about 0.683 for a normal estimator, and less for a t-based one with few degrees of freedom.

## Related definitions

- **[Pivotal quantity](/pivotal-quantity/).** A function of the data and $\theta$ whose distribution does not depend on $\theta$; inverting it gives an exact interval.
- **Expected length.** Among intervals with the same coefficient, shorter is better; uniformly most accurate intervals cover each false value with the smallest probability.
- **Simultaneous intervals.** A family of intervals that all cover their parameters at once with probability $1 - \alpha$, such as Bonferroni intervals.
- **[Confidence sequence](/confidence-sequence/).** A sequence of intervals that covers $\theta$ at all sample sizes at once, so the data can be monitored and the analysis stopped at any time.
- **[Credible interval](/credible-interval/).** The Bayesian counterpart, with posterior probability $1 - \alpha$; it has a different meaning even when the numbers agree.

## References
