---
tag: VFVYTG
kind: theorem
slug: rao-blackwell-theorem
name: Rao-Blackwell theorem
aliases:
- Rao-Blackwellization
area: statistics-and-inference/point-estimation
level: core
summary: Conditioning an estimator on a sufficient statistic never increases its mean squared error, and strictly lowers it unless the estimator is already a function of that statistic.
prereqs: [sufficient-statistic, conditional-expectation, jensens-inequality, mean-squared-error]
see_also: [lehmann-scheffe-theorem, complete-statistic, minimum-variance-unbiased-estimator, rao-blackwellized-particle-filter, gibbs-sampling, monte-carlo-integration, loss-function]
sources:
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 7.3.3, Theorem 7.3.17 (Rao-Blackwell)
  - book: isbn:9780387985022
    title: E. L. Lehmann and George Casella, Theory of Point Estimation, second edition, Springer, 1998
    locator: Chapter 1, Section 1.7 (convex loss functions and the Rao-Blackwell theorem)
  - paper: "C. Radhakrishna Rao, Information and the accuracy attainable in the estimation of statistical parameters, Bulletin of the Calcutta Mathematical Society 37 (1945), pages 81 to 91"
    title: Rao 1945
    locator: the improvement of an unbiased estimator by conditioning on a sufficient statistic
  - paper: doi:10.1214/aoms/1177730497
    title: David Blackwell, Conditional expectation and unbiased sequential estimation, Annals of Mathematical Statistics 18(1) (1947), pages 105 to 110
    locator: the conditional expectation given a sufficient statistic, with the sequential case
---

The Rao-Blackwell theorem says that if $\delta(X)$ is an estimator and $T$ is a [sufficient statistic](/sufficient-statistic/), then the conditional expectation $\eta(T) = \mathbb{E}[\delta(X) \mid T]$ is an estimator that is at least as good as $\delta$ under every convex loss, and in particular has no larger [mean squared error](/mean-squared-error/) at any parameter value. The bias does not change, so an unbiased estimator stays unbiased and its variance can only go down. The step from $\delta$ to $\eta$ is called Rao-Blackwellization. Rao (1945) and Blackwell (1947) proved it independently.

## Statement

Let $X$ have distribution $P_\theta$, $\theta \in \Theta$, let $T = t(X)$ be sufficient for $\theta$, and let $\delta(X)$ be an estimator of $\psi(\theta)$ with $\mathbb{E}_\theta \lvert \delta(X) \rvert < \infty$ for all $\theta$. Define

$$\eta(T) = \mathbb{E}[\delta(X) \mid T].$$

**Theorem.**

1. $\eta(T)$ is a statistic: it does not depend on $\theta$.
2. $\mathbb{E}_\theta\, \eta(T) = \mathbb{E}_\theta\, \delta(X)$ for every $\theta$, so $\eta$ and $\delta$ have the same bias.
3. **Squared error.** If $\mathbb{E}_\theta\, \delta(X)^2 < \infty$, then for every $\theta$
$$\mathbb{E}_\theta(\delta - \psi(\theta))^2 = \mathbb{E}_\theta(\eta - \psi(\theta))^2 + \mathbb{E}_\theta(\delta - \eta)^2 \ \ge\ \mathbb{E}_\theta(\eta - \psi(\theta))^2,$$
with equality at $\theta$ if and only if $\delta(X) = \eta(T)$ with $P_\theta$-probability 1.
4. **Convex loss.** Let $L(\theta, d)$ be a [loss](/loss-function/) that is convex in $d$ for each $\theta$. Then $R(\theta, \eta) \le R(\theta, \delta)$ for every $\theta$, where $R(\theta, \delta) = \mathbb{E}_\theta L(\theta, \delta(X))$. If $L$ is strictly convex in $d$ and $R(\theta, \delta) < \infty$, the inequality is strict unless $\delta(X) = \eta(T)$ with $P_\theta$-probability 1.

## In plain words

Suppose you have some rough estimate, and a summary of the data that holds all the information about the unknown quantity. Replace your estimate by its average over all the data sets that have the same summary. Because the summary holds all the information, you can compute this average without knowing the unknown quantity. The new estimate is on average just as close to the target as the old one, and closer unless the old one already depended only on the summary. The averaging removes noise that carried no information. It does not change the systematic error.

## Proof

**Step 1: $\eta$ is a statistic.** By sufficiency, the conditional distribution of $X$ given $T$ does not depend on $\theta$, so neither does the conditional expectation of $\delta(X)$ given $T$. (Without sufficiency, $\eta$ would depend on the unknown $\theta$ and could not be computed.)

**Step 2: the mean.** By the tower property of [conditional expectation](/conditional-expectation/), $\mathbb{E}_\theta\, \eta(T) = \mathbb{E}_\theta\, \mathbb{E}[\delta(X) \mid T] = \mathbb{E}_\theta\, \delta(X)$.

**Step 3: squared error.** Write $\delta - \psi = (\eta - \psi) + (\delta - \eta)$ and expand the square. The cross term is

$$\mathbb{E}_\theta[(\eta - \psi)(\delta - \eta)] = \mathbb{E}_\theta\big[(\eta(T) - \psi)\, \mathbb{E}[\delta - \eta(T) \mid T]\big] = 0,$$

because $\eta(T) - \psi$ is a function of $T$ and $\mathbb{E}[\delta \mid T] = \eta(T)$. This gives the identity in part 3. The term $\mathbb{E}_\theta(\delta - \eta)^2 = \mathbb{E}_\theta \operatorname{Var}(\delta \mid T)$ is zero exactly when $\delta = \eta(T)$ with probability 1. When $\delta$ is unbiased, the identity reads $\operatorname{Var}_\theta(\delta) = \operatorname{Var}_\theta(\eta) + \mathbb{E}_\theta \operatorname{Var}(\delta \mid T)$, the law of total variance.

**Step 4: convex loss.** By the conditional form of [Jensen's inequality](/jensens-inequality/), for each $\theta$,

$$L(\theta, \eta(T)) = L\big(\theta, \mathbb{E}[\delta(X) \mid T]\big) \le \mathbb{E}\big[L(\theta, \delta(X)) \mid T\big]$$

with probability 1. Taking $\mathbb{E}_\theta$ of both sides gives $R(\theta, \eta) \le R(\theta, \delta)$. If $L(\theta, \cdot)$ is strictly convex, conditional Jensen is an equality only where the conditional distribution of $\delta(X)$ given $T$ is a point mass, that is, where $\delta(X) = \eta(T)$; if this fails on a set of positive probability, and $R(\theta, \delta) < \infty$, the expected inequality is strict. $\blacksquare$

## Consequences

**A recipe for good unbiased estimators.** Start from any unbiased estimator, however crude, and condition on a sufficient statistic. The result is unbiased with no larger variance. If the sufficient statistic is also [complete](/complete-statistic/), the result does not depend on the starting point, and it is the [minimum variance unbiased estimator](/minimum-variance-unbiased-estimator/); this is the [Lehmann-Scheffé theorem](/lehmann-scheffe-theorem/).

**Example: the Bernoulli variance, exact.** Let $X_1, \ldots, X_n$ be iid Bernoulli$(p)$ and $\psi(p) = p(1-p)$. The estimator $\delta = X_1(1 - X_2)$ is unbiased, since $\mathbb{E}_p\, \delta = p(1-p)$. Given $T = \sum_i X_i = t$, the sample is a uniformly random 0-1 sequence with $t$ ones, so

$$\eta(T) = P(X_1 = 1, X_2 = 0 \mid T) = \frac{T(n - T)}{n(n-1)}.$$

For $n = 3$ the values of $\eta$ at $t = 0, 1, 2, 3$ are $0, 1/3, 1/3, 0$. An exact sum over all 8 outcomes gives:

| $p$ | $\psi(p)$ | $\operatorname{Var}_p(\delta)$ | $\operatorname{Var}_p(\eta)$ |
|---|---|---|---|
| $1/3$ | $2/9$ | $14/81$ | $2/81$ |
| $1/2$ | $1/4$ | $3/16$ | $1/48$ |

Both estimators have mean $\psi(p)$. Conditioning cuts the variance by a factor of 7 at $p = 1/3$ and of 9 at $p = 1/2$.

**Example: a Poisson probability.** Let $X_1, \ldots, X_n$ be iid Poisson$(\lambda)$ and $\psi(\lambda) = P_\lambda(X_1 = 0) = e^{-\lambda}$. The indicator $\delta = \mathbf{1}\{X_1 = 0\}$ is unbiased. Given $T = \sum_i X_i = t$, $X_1$ is Binomial$(t, 1/n)$, so

$$\eta(T) = \Big(1 - \frac{1}{n}\Big)^{T}, \qquad \operatorname{Var}_\lambda(\eta) = e^{-2\lambda}(e^{\lambda/n} - 1).$$

At $n = 5$ and $\lambda = 1$, $\operatorname{Var}(\delta) = e^{-1}(1 - e^{-1}) \approx 0.2325$ and $\operatorname{Var}(\eta) \approx 0.0300$.

**Monte Carlo.** The same identity reduces variance in simulation. If a Monte Carlo estimate averages $h(Y)$ and $\mathbb{E}[h(Y) \mid Z]$ has a closed form, then averaging $\mathbb{E}[h(Y) \mid Z]$ instead has no larger variance. Here the model is known, so no sufficiency is needed: the conditional expectation is computable anyway. This is used in [Gibbs sampling](/gibbs-sampling/), [Monte Carlo integration](/monte-carlo-integration/) and the [Rao-Blackwellized particle filter](/rao-blackwellized-particle-filter/).

## Tightness

**Convexity of the loss is needed.** Let $X_1, X_2$ be iid Bernoulli$(p)$, $\delta = X_1$, $T = X_1 + X_2$ and $\eta = T/2$. Take the loss $L(p, d) = \mathbf{1}\{\lvert d - p \rvert > 0.3\}$, which is not convex in $d$. At $p = 0.1$, $\delta$ has risk $P(X_1 = 1) = 1/10$, but $\eta$ is $0.5$ or $1$ whenever $T \ge 1$, so its risk is $P(T \ge 1) = 19/100$. Rao-Blackwellization made the estimator worse.

**Sufficiency is needed.** If $T$ is not sufficient, $\mathbb{E}[\delta \mid T]$ can depend on $\theta$. With $X_1, X_2$ iid Bernoulli$(p)$ and $T = X_2$, $\mathbb{E}[X_1 \mid X_2] = p$, which is not an estimator.

**The improvement can be zero.** If $\delta$ is already a function of $T$, then $\eta = \delta$. Conditioning twice on the same $T$ gives nothing more.

**The result need not be admissible.** Rao-Blackwellization gives an improvement, not an optimum. Under squared error, $S^2$ (divisor $n - 1$) is the conditioned version of many unbiased estimators of $\sigma^2$ in the normal model, and yet $\sum_i (X_i - \bar X)^2 / (n + 1)$ has smaller mean squared error for every $(\mu, \sigma^2)$: $\sigma^4/3$ against $\sigma^4/2$ at $n = 5$. See [admissible estimator](/admissible-estimator/).

## History

Rao (1945), in the same paper that gave the [Cramér-Rao bound](/cramer-rao-bound/), showed that conditioning an unbiased estimator on a sufficient statistic does not increase its variance. Blackwell (1947) proved the result independently, with conditional expectation as the main tool, and extended it to sequential sampling. Lehmann and Scheffé (1950) combined it with completeness to obtain unique minimum variance unbiased estimators. The extension to convex loss is standard; Lehmann and Casella, Section 1.7, give it.

## References
