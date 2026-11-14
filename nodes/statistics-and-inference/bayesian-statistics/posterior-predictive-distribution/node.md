---
tag: Z7WPWJ
kind: definition
slug: posterior-predictive-distribution
name: Posterior predictive distribution
aliases:
- predictive distribution
area: statistics-and-inference/bayesian-statistics
level: core
summary: The distribution of a new observation given the data, the model density averaged over the posterior of the parameters.
prereqs: [bayesian-inference, conjugate-prior, conditional-expectation]
see_also: [prediction-interval, posterior-predictive-check, marginal-likelihood, bayesian-linear-regression, de-finetti-theorem, gaussian-process, conformal-prediction, credible-interval]
sources:
  - book: isbn:9781439840955
    title: "Andrew Gelman, John B. Carlin, Hal S. Stern, David B. Dunson, Aki Vehtari and Donald B. Rubin, Bayesian Data Analysis, 3rd edition, CRC Press, 2013"
    locator: Chapter 1 (prior and posterior predictive distributions), Chapter 2 (the binomial and normal examples) and Chapter 6 (predictive checks)
  - book: isbn:9780387310732
    title: "Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006"
    locator: Section 2.1.1 (the predictive probability of the next trial under a beta prior) and Section 3.3.2 (the predictive distribution of Bayesian linear regression)
---

The posterior predictive distribution is the law of a new observation $Y$ given the observed data $x$. It averages the model density $f(y \mid \theta)$ over the posterior of $\theta$: $p(y \mid x) = \int f(y \mid \theta)\, \pi(d\theta \mid x)$. It carries two kinds of uncertainty, the scatter of $Y$ around its mean and the uncertainty about $\theta$, so it is wider than the plug-in law $f(y \mid \hat\theta)$. It is how a Bayesian predicts, and it is the reference law for posterior predictive checks of a model.

## Definition

Let $X = (X_1, \ldots, X_n)$ and a future $Y$ be conditionally independent given $\theta$, with $X_i \mid \theta$ having density $f(x \mid \theta)$ and $Y \mid \theta$ having density $g(y \mid \theta)$ (often $g = f$). Let $\pi(d\theta \mid x)$ be the posterior from a prior $\pi$, as in [Bayesian inference](/bayesian-inference/).

- The **posterior predictive distribution** of $Y$ has density
$$p(y \mid x) = \int_\Theta g(y \mid \theta)\, \pi(d\theta \mid x).$$
It is the conditional law of $Y$ given $X = x$ under the joint law of $(\theta, X, Y)$.
- The **prior predictive distribution** is $m(y) = \int g(y \mid \theta)\, \pi(d\theta)$, the same average before any data. At the observed data it is the [marginal likelihood](/marginal-likelihood/).
- A draw from $p(y \mid x)$ is a draw $\theta^*$ from the posterior followed by a draw $Y^*$ from $g(\cdot \mid \theta^*)$.

When $Y$ depends on $x$ also through the model, as for the next value of a time series, replace $g(y \mid \theta)$ by $g(y \mid \theta, x)$.

**Mean and variance.** Let $\mu(\theta) = E[Y \mid \theta]$ and $\sigma^2(\theta) = \mathrm{Var}(Y \mid \theta)$. By the tower rules of [conditional expectation](/conditional-expectation/),

$$E[Y \mid x] = E[\mu(\theta) \mid x], \qquad \mathrm{Var}(Y \mid x) = E[\sigma^2(\theta) \mid x] + \mathrm{Var}(\mu(\theta) \mid x).$$

The first term of the variance is the noise of a new observation; the second is the uncertainty about $\theta$. A plug-in law keeps only the first. The second term shrinks as $n$ grows, at rate $1/n$ in regular models, and the first does not.

**Chain rule.** The joint prior predictive density of $x_1, \ldots, x_n$ factors as $m(x_1, \ldots, x_n) = \prod_{i=1}^n p(x_i \mid x_1, \ldots, x_{i-1})$, a product of one-step posterior predictive densities. This is a way to compute the [marginal likelihood](/marginal-likelihood/), and it is the base of prequential (one-step-ahead) model evaluation.

**Calibration over the prior.** Let $\theta$ be drawn from the proper prior $\pi$, then $X$ and $Y$ from the model. If $C(x)$ is a set with $P(Y \in C(x) \mid x) = 1 - \alpha$ under the posterior predictive, then $P(Y \in C(X)) = 1 - \alpha$ under the joint law, by the same Fubini argument as for a [credible interval](/credible-interval/). At a fixed $\theta$ there is no such guarantee; that statement belongs to a frequentist [prediction interval](/prediction-interval/).

## Examples and non-examples

**Beta-binomial.** With $n = 10$ trials, $x = 3$ successes and the uniform prior, the posterior is Beta$(a, b)$ with $a = 4$, $b = 8$ (a [conjugate prior](/conjugate-prior/)). For $Y \mid p \sim$ Binomial$(m, p)$,

$$P(Y = k \mid x) = \binom{m}{k} \frac{B(a + k, b + m - k)}{B(a, b)}, \qquad k = 0, \ldots, m,$$

where $B$ is the beta function. For $m = 5$ the probabilities of $k = 0, \ldots, 5$ are $33/182$, $55/182$, $25/91$, $15/91$, $5/78$ and $1/78$, that is 0.1813, 0.3022, 0.2747, 0.1648, 0.0641 and 0.0128. Expanding $p^{a-1+k}(1 - p)^{b-1+m-k}$ as a polynomial and integrating term by term gives the same six fractions exactly. The mean is $ma/(a + b) = 5/3$ and the variance is

$$\frac{m\, a b\, (a + b + m)}{(a + b)^2 (a + b + 1)} = \frac{170}{117} = 1.4530.$$

The binomial law with $p$ fixed at the posterior mean $1/3$ has variance $10/9$; the ratio is $(a + b + m)/(a + b + 1) = 17/13$, the factor that the uncertainty about $p$ adds. The plug-in law Binomial$(5, 0.3)$ at the MLE gives 0.1681, 0.3602, 0.3087, 0.1323, 0.0284 and 0.0024, with variance $1.05$. It gives 5 successes in 5 about one fifth of the predictive probability.

**The next trial.** For $m = 1$ the predictive probability of a success is $E[p \mid x] = (x + 1)/(n + 2) = 4/12 = 1/3$, Laplace's rule of succession.

**Normal with known variance.** With $X_i \mid \mu$ iid $N(\mu, \sigma^2)$, $\sigma = 0.5$, data 9.8, 10.4, 10.1, 9.6, 10.6 and the prior $\mu \sim N(9, 0.4^2)$, the posterior is $N(\mu_n, \tau_n^2)$ with $\mu_n = 9.8381$ and $\tau_n = 0.1952$. The posterior predictive of a new $Y$ is $N(\mu_n, \sigma^2 + \tau_n^2)$, with standard deviation 0.53675, and its 95% interval is $[8.7861, 10.8901]$. The plug-in law $N(\mu_n, \sigma^2)$ gives $[8.8581, 10.8181]$, which is too narrow.

**Calibration, measured.** Draw $\mu$ from the prior $N(9, 0.4^2)$, then five observations and one new $Y$, $r = 20000$ times with seed 1. The 95% posterior predictive interval contained $Y$ in 0.95245 of the runs; the exact value is 0.95 by the calibration result, and the Monte Carlo standard error is 0.0015. The interval $\bar x \pm 1.959964\,\sigma$ contained $Y$ in 0.93025 of the runs. Its exact coverage at every fixed $\mu$ is $2\Phi(1.959964/\sqrt{1 + 1/5}) - 1 = 0.9264$, because $Y - \bar X \sim N(0, \sigma^2(1 + 1/n))$.

**Normal with unknown variance.** With the improper prior density $1/\sigma$ on $(\mu, \sigma)$ (see [improper prior](/improper-prior/)), the posterior predictive of $Y$ is $\bar x + s\sqrt{1 + 1/n}\; t_{n-1}$, where $s^2$ uses divisor $n - 1$. For the data 2.1, 3.4, 2.9, 3.8, $\bar x = 3.05$, $s = 0.73258$ and $t_{(3, 0.975)} = 3.18245$, so the 95% interval is $[0.4434, 5.6566]$. These are the numbers of the exact normal [prediction interval](/prediction-interval/), with a different meaning: a posterior probability, not a coverage at every fixed $(\mu, \sigma)$.

**Non-example: the plug-in law.** $f(y \mid \hat\theta)$ treats the estimate as the truth. It is not a posterior predictive distribution, and its intervals are too narrow, most of all for small $n$ and for tail events.

**Non-example: the posterior of the mean.** In the normal example the 95% [credible interval](/credible-interval/) for $\mu$ is $[9.4555, 10.2206]$. It describes $\mu$, not a new observation, and it shrinks to a point as $n$ grows; the predictive interval does not.

**Non-example: the prior predictive.** $m(y)$ ignores the data. It is useful for checking what a prior implies before the data come in, and its value at the data is the marginal likelihood, but it is not a prediction from the data.

## Related definitions

- **[Prediction interval](/prediction-interval/).** The frequentist interval for a new observation, with coverage at every fixed parameter value.
- **[Posterior predictive check](/posterior-predictive-check/).** Compares the data with replicated data drawn from the posterior predictive to find misfit.
- **[Marginal likelihood](/marginal-likelihood/).** The prior predictive density at the data; the chain rule writes it as a product of posterior predictive densities.
- **[De Finetti's theorem](/de-finetti-theorem/).** For an exchangeable sequence, the predictive law of the next value given the past is the posterior predictive of a mixture model.
- **[Bayesian linear regression](/bayesian-linear-regression/) and [Gaussian process](/gaussian-process/) regression.** Their posterior predictive laws are a Student t and a normal law in closed form.
- **[Conformal prediction](/conformal-prediction/).** Prediction sets with finite-sample marginal coverage under exchangeability alone, with no prior.

## References
