---
tag: ES82YY
kind: technique
slug: importance-sampling
name: Importance sampling
aliases:
- IS
- importance weighting
- self-normalized importance sampling
area: randomized/sampling
level: advanced
summary: Estimate expectations under a target distribution by sampling a proposal and reweighting the samples.
prereqs: [monte-carlo-integration, expected-value, variance]
see_also: [monte-carlo-integration, rejection-sampling, multiple-importance-sampling, annealed-importance-sampling, sequential-monte-carlo, effective-sample-size, path-tracing, cross-entropy-method]
sources:
  - url: https://artowen.su.domains/mc/
    title: Art B. Owen, Monte Carlo theory, methods and examples, 2013
    locator: Chapter 9 (importance sampling), the sections on the variance, the optimal density, self-normalized importance sampling and the effective sample size
  - book: isbn:9780387212395
    title: Christian P. Robert and George Casella, Monte Carlo Statistical Methods, second edition, Springer, 2004
    locator: Section 3.3 (importance sampling)
  - paper: "Augustine Kong, A note on importance sampling using standardized weights, Technical Report 348, Department of Statistics, University of Chicago, 1992"
    locator: the whole report (the effective sample size)
  - paper: "Augustine Kong, Jun S. Liu and Wing Hung Wong, Sequential imputations and Bayesian missing data problems, Journal of the American Statistical Association 89(425), 1994"
    locator: pages 278 to 288
  - paper: "Herman Kahn and Andrew W. Marshall, Methods of reducing sample size in Monte Carlo computations, Journal of the Operations Research Society of America 1(5), 1953"
    locator: pages 263 to 278
---

Importance sampling estimates an expectation $\mu = \mathbb{E}_p[f(X)]$ under a target density $p$ from samples of a different proposal density $q$: draw $X_1, \ldots, X_n$ from $q$ and return $\hat\mu = \frac{1}{n}\sum_j w_j f(X_j)$ with weights $w_j = p(X_j)/q(X_j)$. The estimate is unbiased when $q > 0$ wherever $f p \ne 0$, and its variance is $\frac{1}{n}\bigl(\int f^2 p^2 / q - \mu^2\bigr)$. The best proposal is $q^* \propto |f| p$, which gives zero variance when $f \ge 0$. When $p$ is known only up to a constant, the self-normalized form divides by $\sum_j w_j$ instead of $n$; it is consistent but biased by $O(1/n)$. Kong's effective sample size $(\sum w_j)^2 / \sum w_j^2$ measures how much the weights waste. Unlike [rejection sampling](/rejection-sampling/), importance sampling does not produce samples of $p$; it produces weighted samples and estimates.

## In plain words

Suppose you want the average of some quantity over a population, but the cases that matter are rare. Sampling the population as it is wastes most draws on cases that add almost nothing.

So draw from a different population, one where the important cases are common. Every draw is now too likely or too unlikely compared to the real population. Fix this with a weight: the ratio of how likely the draw is in the real population to how likely it was in yours. Multiply each value by its weight, and the average is right again, on average.

A good choice of the second population makes the estimate much more precise. A bad one, with some cases far rarer than in the real population, makes a few weights huge and the estimate unstable.

## When it applies

- The goal is an expectation, an integral or a probability, not a sample.
- $p$ is hard to sample, or plain [Monte Carlo integration](/monte-carlo-integration/) under $p$ has high variance, for example because $f$ is large only on a rare set.
- A proposal $q$ is available that can be sampled and evaluated, and $q > 0$ wherever $f p \ne 0$. For the self-normalized form, $q > 0$ wherever $p > 0$.
- The tails of $q$ are at least as heavy as those of $|f| p$, so that $\int f^2 p^2 / q$ is finite.

In high dimension the weights of a product proposal tend to be extremely uneven, so importance sampling alone works well only in low or moderate dimension, or with a proposal built by [sequential Monte Carlo](/sequential-monte-carlo/) or [annealed importance sampling](/annealed-importance-sampling/).

## The template

Notation: $p$ is the target density, $\tilde p = Z p$ an unnormalized form with unknown $Z$, $q$ the proposal, $f$ the integrand, $\mu = \mathbb{E}_p[f]$, and $w(x) = p(x)/q(x)$. The holes are $q$ and its sampler.

```pseudo id=main
IS(f, p, q, n)
L1  for j ← 1 to n do  X_j ← a sample from q;  w_j ← p(X_j) / q(X_j)
L2  return (1/n) · Σ_j w_j f(X_j)

SELF-NORMALIZED-IS(f, p̃, q, n)
L3  for j ← 1 to n do  X_j ← a sample from q;  w_j ← p̃(X_j) / q(X_j)
L4  return Σ_j w_j f(X_j) / Σ_j w_j

EFFECTIVE-SAMPLE-SIZE(w[1..n])
L5  return (Σ_j w_j)² / Σ_j w_j²
```

### Example

**A discrete target.** Take three values with $p = (0.7, 0.2, 0.1)$ and $f = (0, 1, 10)$, so $\mu = 0.2 + 1 = 1.2$.

| proposal $q$ | weights $p/q$ | $\int f^2 p^2/q$ | variance of one term |
|---|---|---|---|
| $p$ itself (plain Monte Carlo) | $(1, 1, 1)$ | 10.2 | 8.76 |
| uniform $(\frac13, \frac13, \frac13)$ | $(2.1, 0.6, 0.3)$ | 3.12 | 1.68 |
| $q^* \propto f p = (0, \frac16, \frac56)$ | $(\cdot, 1.2, 0.12)$ | 1.44 | 0 |

With the uniform proposal, the variance falls by a factor of $8.76/1.68 \approx 5.2$. With $q^*$, every term $w f$ equals $1.2$ exactly. The exact law of $\hat\mu$, computed over all $3^n$ draws with fractions, has mean $\frac{6}{5}$ and variance $\frac{42}{25n}$ for $n = 1, \ldots, 4$.

The self-normalized form with the uniform proposal is biased: for $n = 1$ it returns $f(X_1)$, with mean $\mathbb{E}_q[f] = \frac{11}{3}$, and $n$ times the bias is $2.47$, $2.48$, $2.31$, $2.17$ for $n = 1, 2, 3, 4$, falling toward the first-order value $-\mathbb{E}_q[w^2(f - \mu)] = 1.524$.

**A rare event.** For $\Pr[Z > 4] \approx 3.167 \times 10^{-5}$ with $Z$ standard normal, take $q$ the normal density with mean 4. The weight is $e^{-4x + 8}$. One term has relative standard deviation $2.12$, against $177.7$ for plain Monte Carlo: the variance is about $7{,}000$ times smaller.

### Why it is correct

**Theorem 1 (unbiased).** If $q(x) > 0$ wherever $f(x)p(x) \ne 0$, then $\mathbb{E}_q[\hat\mu] = \mu$.

*Proof.* Each term has $\mathbb{E}_q[w(X)f(X)] = \int_{q > 0} q(x)\frac{p(x)}{q(x)} f(x)\,dx = \int_{q > 0} f p = \int f p = \mu$, because $fp = 0$ where $q = 0$. Average over $j$ by [linearity of expectation](/linearity-of-expectation/). $\blacksquare$

If $q = 0$ on a set where $fp \ne 0$, the estimate misses $\int f p$ over that set, and no amount of sampling shows it.

**Theorem 2 (variance).** The terms are independent, so

$$\operatorname{Var}_q[\hat\mu] = \frac{\sigma_q^2}{n}, \qquad \sigma_q^2 = \int \frac{f^2 p^2}{q} - \mu^2.$$

*Proof.* $\operatorname{Var}_q[wf] = \mathbb{E}_q[w^2 f^2] - \mu^2 = \int q \frac{p^2 f^2}{q^2} - \mu^2$. Independent terms add their variances. $\blacksquare$

**Theorem 3 (the optimal proposal).** Among all proposals, $\sigma_q^2$ is smallest for $q^* = |f| p / \int |f| p$, with $\sigma_{q^*}^2 = (\int |f| p)^2 - \mu^2$. If $f \ge 0$, this is 0.

*Proof.* By the Cauchy-Schwarz inequality,

$$\Bigl(\int |f| p\Bigr)^2 = \Bigl(\int \frac{|f| p}{\sqrt q}\sqrt q\Bigr)^2 \le \int \frac{f^2 p^2}{q} \int q = \int \frac{f^2 p^2}{q},$$

with equality when $|f| p / \sqrt q$ is proportional to $\sqrt q$, that is, $q \propto |f| p$. If $f \ge 0$, then $\int |f| p = \mu$ and the variance is 0: every term equals $\mu$. $\blacksquare$

The zero-variance proposal needs $\mu$ itself as its normalizing constant, so it is not usable directly. It is a guide: a good proposal is roughly proportional to $|f| p$.

**Self-normalized importance sampling.** With $\tilde p = Z p$, the weights $\tilde w = Z w$ have $\mathbb{E}_q[\tilde w] = Z$. The estimate $\tilde\mu = \sum \tilde w_j f(X_j) / \sum \tilde w_j$ does not depend on $Z$. By the [law of large numbers](/law-of-large-numbers/), the numerator over $n$ tends to $Z\mu$ and the denominator over $n$ tends to $Z$, so $\tilde\mu \to \mu$ with probability 1 when $q > 0$ wherever $p > 0$ and $\mathbb{E}_p|f| < \infty$. It is biased for finite $n$: for $n = 1$ it returns $f(X_1)$, with mean $\mathbb{E}_q[f]$. A second-order expansion of the ratio (the delta method) gives, to first order in $1/n$,

$$\mathbb{E}[\tilde\mu] - \mu \approx -\frac{1}{n}\mathbb{E}_q\bigl[w^2 (f - \mu)\bigr], \qquad \operatorname{Var}[\tilde\mu] \approx \frac{1}{n}\mathbb{E}_q\bigl[w^2 (f - \mu)^2\bigr],$$

with $w = p/q$ normalized. These are asymptotic approximations under moment conditions, not exact formulas (Owen, Chapter 9).

**Effective sample size.** Kong (1992) compared the variance of the self-normalized estimate with that of plain Monte Carlo with $n$ samples from $p$, and found the ratio is about $1 + \operatorname{Var}_q[w] = \mathbb{E}_q[w^2]$ for normalized weights, when $f$ is not too correlated with $w$. So $n$ weighted samples are worth about $n / \mathbb{E}_q[w^2]$ samples from $p$. Replacing the expectation by its sample estimate gives

$$n_{\text{eff}} = \frac{(\sum_j w_j)^2}{\sum_j w_j^2},$$

which does not depend on $Z$ and lies between 1 (one weight dominates) and $n$ (equal weights). It is a heuristic that ignores $f$, not a bound. See [effective sample size](/effective-sample-size/).

### Cost

- **Per sample.** One draw from $q$, one evaluation each of $p$ (or $\tilde p$), $q$ and $f$.
- **Error.** The standard error is $\sigma_q / \sqrt{n}$, so a relative error $\varepsilon$ needs about $\sigma_q^2 / (\mu^2 \varepsilon^2)$ samples. For rare events, a good proposal can turn an exponentially large count into a polynomial one; a poor proposal can make $\sigma_q^2$ infinite.
- **Error estimate.** The sample variance of the terms $w_j f(X_j)$ estimates $\sigma_q^2$, but when the weights have heavy tails, this estimate is itself unreliable.

## Classic examples

- **Rare-event simulation.** Shift or tilt the proposal toward the rare set, as in the normal tail example. Exponential tilting $q(x) \propto e^{\theta x} p(x)$ is the standard choice for sums of independent variables.
- **[Path tracing](/path-tracing/) in rendering.** Sample light paths by the BRDF or by the light sources, and weight them. [Multiple importance sampling](/multiple-importance-sampling/) combines several proposals with weights that keep the estimate unbiased.
- **Bayesian computation.** Posterior expectations and the marginal likelihood $Z = \mathbb{E}_q[\tilde p / q]$, which is estimated without bias by the plain form.
- **[Sequential Monte Carlo](/sequential-monte-carlo/) and [particle filters](/particle-filter/).** Importance sampling step by step, with [resampling](/resampling/) when the effective sample size falls below a threshold; the context in which Kong, Liu and Wong (1994) used the effective sample size.
- **Off-policy evaluation in reinforcement learning.** Estimate the value of one policy from episodes of another, with weights that are products of action probability ratios.
- **The [cross-entropy method](/cross-entropy-method/).** Fits the proposal from a parametric family step by step toward $q^*$.

## Variations

- **Defensive importance sampling.** Use the mixture $q_\alpha = \alpha p + (1 - \alpha) q$. The weights are at most $1/\alpha$, so the variance is at most a fixed multiple of the plain Monte Carlo variance plus a constant.
- **[Multiple importance sampling](/multiple-importance-sampling/).** Several proposals with a balance heuristic.
- **[Annealed importance sampling](/annealed-importance-sampling/).** A sequence of intermediate densities between $q$ and $p$, linked by MCMC steps, with a product of weight ratios.
- **Control variates with the weights.** Since $\mathbb{E}_q[w] = 1$, the term $\beta(\bar w - 1)$ can be subtracted from $\hat\mu$ to reduce the variance.
- **Importance sampling and rejection.** With an envelope $p \le M q$, rejection sampling turns the same $p$ and $q$ into exact samples; importance sampling keeps all draws but weights them.

## Pitfalls

- **Light-tailed proposals.** If $q$ falls off faster than $|f| p$, $\int f^2 p^2/q$ can be infinite. The estimate is still unbiased and consistent, but its error does not shrink like $1/\sqrt{n}$, and the sample variance can look small for a long time before a huge weight appears.
- **Missing support.** If $q = 0$ where $f p \ne 0$, the estimate is biased, and the bias does not show in the samples.
- **Treating weighted samples as samples.** The pairs $(X_j, w_j)$ are not draws from $p$. To get approximate draws, resample with probabilities proportional to $w_j$; the result is still only approximate for finite $n$.
- **The effective sample size as a guarantee.** A large $n_{\text{eff}}$ does not prove that the estimate is good: if $q$ misses a mode of $p$ entirely, all weights can be similar and still wrong.
- **Overflow.** Compute the weights in the log domain and subtract the largest log-weight before exponentiating, as in the [log-sum-exp trick](/log-sum-exp-trick/). The self-normalized form does not change; for the plain form, add the shift back.
- **Normalizing constants.** The plain form needs the normalized $p$ and $q$. With an unnormalized $\tilde p$, either use the self-normalized form or estimate $Z$ separately.

## Exercises

1. For $p$ the standard normal, $q$ the normal with mean 0 and standard deviation $\sigma$, and $f = 1$, show that $\mathbb{E}_q[w^2] = \sigma^2/\sqrt{2\sigma^2 - 1}$ for $\sigma^2 > 1/2$ and is infinite otherwise.
2. Show that the plain estimate of $Z = \int \tilde p$, namely $\frac{1}{n}\sum \tilde p(X_j)/q(X_j)$, is unbiased, and that its reciprocal is not.
3. Derive the first-order bias of the self-normalized estimate by expanding $a/b$ around $(\mathbb{E}a, \mathbb{E}b)$.
4. For $\Pr[Z > c]$ with the proposal of mean $c$, show that the second moment of one term is $e^{c^2}\Pr[Z > 2c]$, and find the relative error as $c \to \infty$.

## References
