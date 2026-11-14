---
tag: 9NG63E
kind: definition
slug: credible-interval
name: Credible interval
aliases:
- Bayesian confidence interval
- equal-tailed credible interval
area: statistics-and-inference/bayesian-statistics
level: intro
summary: An interval that holds the parameter with a stated posterior probability. Unlike a confidence interval, the probability is about the parameter given the data.
prereqs: [bayesian-inference, bayes-theorem, quantile, confidence-interval]
see_also: [highest-posterior-density-interval, bernstein-von-mises-theorem, jeffreys-prior, prediction-interval, posterior-predictive-distribution, clopper-pearson-interval, wilson-score-interval, simulation-based-calibration]
sources:
  - book: isbn:9781439840955
    title: "Andrew Gelman, John B. Carlin, Hal S. Stern, David B. Dunson, Aki Vehtari and Donald B. Rubin, Bayesian Data Analysis, 3rd edition, CRC Press, 2013"
    locator: Chapter 2 (posterior intervals for the binomial and normal models, central intervals and highest posterior density regions)
  - book: isbn:9780387715988
    title: "Christian P. Robert, The Bayesian Choice, 2nd edition, Springer, 2007"
    locator: Chapter 5, Section 5.5.1 (credible intervals) and Section 5.5.2 (classical confidence intervals)
  - paper: doi:10.1214/ss/1009213286
    title: "Lawrence D. Brown, T. Tony Cai and Anirban DasGupta, Interval estimation for a binomial proportion, Statistical Science 16(2), 2001"
    locator: pages 101 to 133 (the frequentist coverage of the equal-tailed Jeffreys credible interval)
---

A $1 - \alpha$ credible interval is an interval of parameter values that has posterior probability $1 - \alpha$ given the observed data. It comes from a prior and a model through [Bayes' theorem](/bayes-theorem/), and its statement is about the parameter $\theta$ after the data $x$ are fixed: $P(\theta \in [a, b] \mid x) = 1 - \alpha$. The usual choice cuts $\alpha/2$ of posterior probability from each tail, so its ends are two posterior [quantiles](/quantile/). A credible interval is not a [confidence interval](/confidence-interval/): its coverage over repeated samples at a fixed $\theta$ is a separate property, which can be far from $1 - \alpha$.

## Definition

Let $\theta \in \Theta \subseteq \mathbb{R}$ have a proper prior $\pi$, and let the data $x$ have density $f(x \mid \theta)$. The posterior $\pi(d\theta \mid x)$ is the conditional law of $\theta$ given $x$, as in [Bayesian inference](/bayesian-inference/).

- A set $C(x) \subseteq \Theta$ is a **$1 - \alpha$ credible set** if $\pi(C(x) \mid x) \ge 1 - \alpha$. For a continuous posterior the usual choice has probability exactly $1 - \alpha$.
- A **credible interval** is a credible set that is an interval $[a(x), b(x)]$.
- The **equal-tailed** credible interval is $[q_{\alpha/2}(x), q_{1 - \alpha/2}(x)]$, where $q_p(x)$ is the $p$-quantile of the posterior. Each tail outside it has posterior probability $\alpha/2$.
- A **one-sided** credible bound is $q_{1-\alpha}(x)$ (upper) or $q_\alpha(x)$ (lower).
- The **[highest posterior density region](/highest-posterior-density-interval/)** is the credible set of smallest length; for a skewed posterior it differs from the equal-tailed interval.

The same definitions apply to a function $g(\theta)$, with the posterior law of $g(\theta)$ in place of that of $\theta$. An improper prior is allowed when the posterior it gives is proper (see [improper prior](/improper-prior/)).

### The Bayesian statement

Given $x$, the interval is fixed and $\theta$ is random under the posterior. "$\theta$ is in $[0.1093, 0.6097]$ with probability 0.95" is a correct sentence about a credible interval, under the stated prior and model. Another prior gives another interval, and the statement is only as good as the prior and the model.

**Invariance under monotone maps.** Let $\phi = g(\theta)$ with $g$ strictly increasing. Then $P(g(\theta) \le g(q) \mid x) = P(\theta \le q \mid x)$, so the posterior quantiles of $\phi$ are $g$ of the posterior quantiles of $\theta$, and the equal-tailed interval for $\phi$ is $[g(q_{\alpha/2}(x)), g(q_{1-\alpha/2}(x))]$. For a decreasing $g$ the two ends change places. The highest posterior density region does not have this property.

### Frequentist coverage of a credible interval

The coverage of the rule $x \mapsto C(x)$ at a fixed $\theta$ is $P_\theta(\theta \in C(X))$, the probability over repeated samples, as for a confidence interval. Two facts connect it with the posterior probability.

1. **Averaged over the prior, the coverage is $1 - \alpha$.** If $\pi$ is proper and $\pi(C(x) \mid x) = 1 - \alpha$ for every $x$, then $\int P_\theta(\theta \in C(X))\, \pi(d\theta) = 1 - \alpha$. Proof: the joint law of $(\theta, X)$ is $\pi(d\theta) f(x \mid \theta)\, dx$, and it is also $m(dx)\, \pi(d\theta \mid x)$, where $m$ is the marginal law of $X$. By Fubini's theorem, $\iint 1\{\theta \in C(x)\}\, \pi(d\theta) f(x \mid \theta)\, dx = \int \pi(C(x) \mid x)\, m(dx) = 1 - \alpha$.
2. **At a fixed $\theta$ the coverage can take any value.** A prior that puts little mass near $\theta$ gives low coverage there, and high coverage elsewhere, so that the average stays at $1 - \alpha$.

Coverage at a fixed $\theta$ tends to $1 - \alpha$ in regular parametric models under the conditions of the [Bernstein-von Mises theorem](/bernstein-von-mises-theorem/). That theorem is the only general bridge between the two statements. Below, all coverage numbers are measured: they are exact sums of binomial probabilities at each $\theta$, and they are not a theorem.

## Examples and non-examples

**A binomial proportion.** Let $X \mid p \sim$ [Binomial](/binomial-distribution/)$(10, p)$ and observe $x = 3$. Under the uniform prior Beta$(1, 1)$ the posterior is Beta$(4, 8)$, with mean $1/3$. Its equal-tailed 95% credible interval is $[0.1093, 0.6097]$, of length 0.5005. Under the [Jeffreys prior](/jeffreys-prior/) Beta$(1/2, 1/2)$ the posterior is Beta$(3.5, 7.5)$ and the interval is $[0.0927, 0.6058]$. For comparison, the [Clopper-Pearson](/clopper-pearson-interval/) 95% confidence interval for the same data is $[0.0667, 0.6525]$; it has a different meaning.

**Invariance.** Map the Beta$(4, 8)$ interval to the odds $p/(1 - p)$: the 95% interval for the odds is $[0.1227, 1.5624]$, and for the log-odds it is $[-2.0983, 0.4462]$. These are the ends of $[0.1093, 0.6097]$ put through the map, and each still cuts 2.5% from each tail.

**A normal mean with known variance.** Let $X_1, \ldots, X_5 \mid \mu$ be iid $N(\mu, 0.5^2)$ with data 9.8, 10.4, 10.1, 9.6, 10.6, so $\bar x = 10.1$. With the prior $\mu \sim N(9, 0.4^2)$ the posterior is normal with precision $1/0.4^2 + 5/0.5^2 = 26.25$, mean 9.8381 and standard deviation 0.1952 ([conjugate prior](/conjugate-prior/)). The 95% credible interval is $9.8381 \pm 1.959964 \times 0.1952 = [9.4555, 10.2206]$. It is pulled toward the prior mean 9. With the flat prior on $\mu$ the posterior is $N(10.1, 0.5^2/5)$ and the interval is $[9.6617, 10.5383]$, the same numbers as the z confidence interval, with the meaning of a posterior probability.

**Coverage at a fixed $p$ (measured).** For $n = 10$ and the uniform prior, the 95% equal-tailed interval has exact coverage 0.9298 at $p = 0.1$, 0.9244 at $p = 0.3$ and 0.9785 at $p = 0.5$. For $p$ in $[0.05, 0.95]$ the lowest value is 0.8824, at $p = 0.06$. For $p < 0.0023$ the coverage is 0, because the interval for $x = 0$ is $[0.0023, 0.2849]$ and every other interval starts higher. The mean coverage over the grid $p = 0.001, 0.002, \ldots, 0.999$ is 0.9506, close to the exact prior average 0.95 of fact 1.

**A strong prior (measured).** With the prior Beta$(20, 20)$ and the same $n = 10$, the interval for $x = 3$ is $[0.3253, 0.5977]$; it does not contain the sample proportion 0.3. The exact coverage is 0 at $p = 0.1$, 0.1493 at $p = 0.3$ and 1 at $p = 0.5$. Its average over the Beta$(20, 20)$ prior is still 0.95 (fact 1; a midpoint sum with 20000 points gives 0.94998). The posterior statement is correct for a person who holds that prior, and the coverage is poor for a true $p$ far from 0.5.

**Non-example: a confidence statement.** "95% of intervals made this way contain the true $\theta$, whatever it is" is the definition of a 95% confidence interval. A credible interval does not promise this, as the strong-prior example shows. A credible interval is not a confidence interval, even when the numbers agree.

**Non-example: an interval for a new observation.** An interval that holds a future $X_{n+1}$ with probability $1 - \alpha$ comes from the [posterior predictive distribution](/posterior-predictive-distribution/), not from the posterior of $\theta$. In the normal example the 95% posterior predictive interval is $[8.7861, 10.8901]$, much wider than the credible interval for $\mu$. The frequentist version is a [prediction interval](/prediction-interval/).

**Non-example: a posterior that is not proper.** With $X_i \mid \theta_i \sim N(\theta_i, 1)$ for $i = 1, \ldots, k$, $\theta_i \mid \tau^2 \sim N(0, \tau^2)$ and the prior density $1/\tau^2$ for $\tau^2$, the posterior of $\tau^2$ has infinite mass near 0. Quantiles of it do not exist, so no credible interval does, even though a sampler can still produce numbers (see [improper prior](/improper-prior/)).

## Related definitions

- **[Highest posterior density region](/highest-posterior-density-interval/).** The shortest credible set; for Beta$(4, 8)$ it is $[0.0934, 0.5880]$, shorter than the equal-tailed interval but not invariant under reparametrization.
- **[Confidence interval](/confidence-interval/).** A rule whose coverage over repeated samples is at least $1 - \alpha$ at every $\theta$; the probability is about the rule, not about $\theta$.
- **Jeffreys interval.** The equal-tailed credible interval of the Beta$(x + 1/2, n - x + 1/2)$ posterior of a binomial proportion. Brown, Cai and DasGupta (2001) studied its frequentist coverage and recommend it with the [Wilson score interval](/wilson-score-interval/) for small $n$.
- **[Bernstein-von Mises theorem](/bernstein-von-mises-theorem/).** In regular models the posterior is close to a normal law at the MLE, so credible intervals have coverage tending to $1 - \alpha$.
- **[Simulation-based calibration](/simulation-based-calibration/).** A check of a posterior sampler that uses fact 1: with $\theta$ drawn from the prior, credible intervals must cover at the stated rate.
- **[Maximum a posteriori estimate](/maximum-a-posteriori-estimation/).** The posterior mode, which lies inside the highest posterior density region of every level.

## References
