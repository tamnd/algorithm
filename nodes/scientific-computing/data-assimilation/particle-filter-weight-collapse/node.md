---
tag: AKHZXV
kind: theorem
slug: particle-filter-weight-collapse
name: Particle filter collapse in high dimensions
aliases:
- particle filter weight collapse
area: scientific-computing/data-assimilation
level: research
summary: In a bootstrap particle filter with Gaussian log weights of standard deviation τ, one particle takes almost all the weight unless the number of particles grows like exp(τ²/2).
prereqs: [particle-filter, effective-sample-size]
see_also: [local-particle-filter, curse-of-dimensionality, importance-sampling, resampling, sequential-monte-carlo, ensemble-kalman-filter, central-limit-theorem]
sources:
  - paper: doi:10.1175/2008MWR2529.1
    title: C. Snyder, T. Bengtsson, P. Bickel and J. Anderson, Obstacles to high-dimensional particle filtering, Monthly Weather Review 136(12) (2008) 4629-4640
    locator: the asymptotic largest weight 1 + sqrt(2 log N)/τ, the Gaussian example, and the estimate of at least 10^11 members for a 200-dimensional state in the abstract
  - paper: doi:10.1214/193940307000000518
    title: T. Bengtsson, P. Bickel and B. Li, Curse-of-dimensionality revisited, collapse of the particle filter in very large scale systems, in Probability and Statistics, Essays in Honor of David A. Freedman, IMS Collections 2 (2008)
    locator: the collapse of the largest weight when the log likelihood variance grows faster than log N
  - paper: doi:10.1002/qj.3551
    title: P. J. van Leeuwen, H. R. Künsch, L. Nerger, R. Potthast and S. Reich, Particle filters for high-dimensional geoscience applications, a review, Quarterly Journal of the Royal Meteorological Society 145(723) (2019) 2335-2365
    locator: the discussion of weight degeneracy and the methods that avoid it
---

The weights of a bootstrap [particle filter](/particle-filter/) are proportional to the likelihood of each particle. When there are many independent observations, the log likelihood is a sum of many terms, so across the particles it is close to Gaussian with a variance $\tau^2$ that grows with the number of observations. If the number of particles $N$ grows more slowly than $\exp(c\,\tau^2)$ for every $c > 0$, the largest weight tends to 1 and the filter keeps only copies of one particle. Snyder, Bengtsson, Bickel and Anderson (2008) showed that the [effective sample size](/effective-sample-size/) stays useful only if $\log N$ grows like $\tau^2$, so that $N$ grows like $\exp(\tau^2/2)$, and Bengtsson, Bickel and Li (2008) gave the collapse in this form.

## Statement

**Setting.** The log weights are $\ell_i = \tau z_i$, $i = 1, \ldots, N$, with $z_1, \ldots, z_N$ independent $N(0, 1)$ and $\tau > 0$, and the normalized weights are $w_i = e^{\ell_i}/\sum_m e^{\ell_m}$. Let $w_{\max} = \max_i w_i$. This is the Gaussian model of the log likelihood: for $p$ independent observations with independent errors the log likelihood is a sum of $p$ independent terms, and by the [central limit theorem](/central-limit-theorem/) it is close to Gaussian across the particles, with $\tau^2$ of order $p$.

**Theorem (weight collapse).** Let $N \to \infty$ and $\tau \to \infty$ with $(\log N)/\tau^2 \to 0$. Then $w_{\max} \to 1$ in probability.

**Gaussian observations.** Let the prior of the particles be $N(0, B)$, let $y = Hx + \epsilon$ with $\epsilon \sim N(0, R)$, and let $\lambda_1^2, \ldots, \lambda_p^2$ be the eigenvalues of $R^{-1/2}HBH^\top R^{-1/2}$. The variance of the log likelihood over the particles, averaged over $y$, is

$$\tau^2 = \sum_{j=1}^p \lambda_j^2\Big(1 + \tfrac32\lambda_j^2\Big).$$

For $B = I$, $H = I$ and $R = I$ in $n$ dimensions, $\tau^2 = \tfrac52 n$, which grows linearly with the dimension.

## In plain words

A particle filter scores each guess of the state by how likely the measurements are if that guess were true. With many measurements the scores add up from many small parts, and the gaps between the guesses grow. The best guess then has a score so much higher than all others that it gets almost all the weight, and the filter in effect keeps one guess. To stop this, the number of guesses must grow exponentially with the number of independent measurements. For a weather model this number is far too large.

## Proof

Let $a_N > 0$ solve $N(1 - \Phi(a_N)) = 1$, where $\Phi$ is the standard normal distribution function and $\varphi$ its density. Then $a_N \to \infty$ and $a_N^2/(2\log N) \to 1$, so the hypothesis gives $a_N/\tau \to 0$. The proof uses the Mills ratio: $1 - \Phi(s) = \varphi(s)/s\,(1 + o(1))$ as $s \to \infty$.

Let $M = \max_i z_i$, attained at $i^\ast$. Then $w_{\max} = 1/(1 + S)$ with $S = \sum_{i \ne i^\ast} e^{\tau(z_i - M)}$, and it is enough to show that $S \to 0$ in probability. Fix $\varepsilon > 0$ and $\lambda > 0$, and let $s = a_N - \lambda/a_N$.

*The level $s$.* By the Mills ratio, $N(1 - \Phi(s)) = \frac{\varphi(s)}{\varphi(a_N)}\frac{a_N}{s}(1 + o(1)) = e^{\lambda - \lambda^2/(2a_N^2)}(1 + o(1)) \to e^\lambda$. So the number $C$ of the $z_i$ above $s$ is binomial with mean $\mu_N \to e^\lambda$, and $P(M \le s) = \Phi(s)^N \to \exp(-e^\lambda)$. Choose $\lambda$ so large that $\exp(-e^\lambda) < \varepsilon$.

*The terms below $s$.* On the event $M > s$,

$$\sum_{i:\, z_i \le s} e^{\tau(z_i - M)} \le e^{-\tau s} \sum_{i=1}^N e^{\tau z_i}\,\mathbf 1\{z_i \le s\} =: T .$$

Completing the square gives $\mathbb E[e^{\tau z}\mathbf 1\{z \le s\}] = e^{\tau^2/2}\,\Phi(s - \tau)$. Since $s/\tau \to 0$, $\tau - s \to \infty$, and the Mills ratio gives $\Phi(s - \tau) \le \varphi(\tau - s)/(\tau - s)$. With $e^{-\tau s}e^{\tau^2/2}\varphi(\tau - s) = \varphi(s)$,

$$\mathbb E[T] \le \frac{N\varphi(s)}{\tau - s} = \frac{N(1 - \Phi(s))\,s\,(1 + o(1))}{\tau - s} \to 0,$$

because $N(1 - \Phi(s)) \to e^\lambda$ and $s/\tau \to 0$. By the Markov inequality, $T \to 0$ in probability.

*The terms above $s$.* Let $E_\delta$ be the event that two of the values above $s$ lie within $\delta$ of each other. Given $C$, the values above $s$ are independent with the density $\varphi(x)/(1 - \Phi(s))$ on $(s, \infty)$, which is at most $\varphi(s)/(1 - \Phi(s)) = s(1 + o(1))$. So two given values are within $\delta$ of each other with probability at most $2\delta s(1 + o(1))$, and

$$P(E_\delta) \le \mathbb E\Big[\binom C2\Big]\,2\delta s\,(1 + o(1)) \le \mu_N^2\,\delta s\,(1 + o(1)),$$

using $\mathbb E[C(C - 1)] \le \mu_N^2$ for a binomial $C$. Take $\delta = \eta/a_N$ with $\eta > 0$ so small that $e^{2\lambda}\eta < \varepsilon$. Then $P(E_\delta) < 2\varepsilon$ for large $N$. Outside $E_\delta$, every $z_i > s$ with $i \ne i^\ast$ satisfies $z_i \le M - \delta$, so the terms above $s$ sum to at most $C\,e^{-\eta\tau/a_N}$, and $C$ is bounded in probability while $\eta\tau/a_N \to \infty$.

*Together.* Outside an event of probability at most $4\varepsilon$ for large $N$, $S \le T + C\,e^{-\eta\tau/a_N}$, and both terms tend to 0 in probability. Since $\varepsilon$ is arbitrary, $S \to 0$ and $w_{\max} \to 1$ in probability. $\square$

*The Gaussian variance.* Rotate and scale so that $R = I$ and $HBH^\top = \mathrm{diag}(\lambda_j^2)$; then $\ell = -\tfrac12\sum_j (y_j - v_j)^2$ up to a constant, with independent $v_j = (Hx)_j \sim N(0, \lambda_j^2)$ over the particles. For fixed $y_j$, $y_j - v_j \sim N(y_j, \lambda_j^2)$, and the variance of the square of an $N(m, \sigma^2)$ variable is $2\sigma^4 + 4m^2\sigma^2$, so $\mathrm{Var}(\ell \mid y) = \sum_j(\tfrac12\lambda_j^4 + y_j^2\lambda_j^2)$. Under the model $\mathbb E[y_j^2] = \lambda_j^2 + 1$, which gives $\sum_j \lambda_j^2(1 + \tfrac32\lambda_j^2)$. With $\lambda_j = 1$ each term is $\tfrac52$. $\square$

## Consequences

- **The number of particles must grow exponentially.** For $\tau^2 = \tfrac52 n$, the theorem says that any $N = e^{o(n)}$ collapses, so a useful $N$ grows exponentially with the number of independent observations (a theorem).
- **The asymptotic rate.** Snyder, Bengtsson, Bickel and Anderson (2008) derive $\mathbb E[1/w_{\max}] \approx 1 + \sqrt{2\log N}/\tau$ for large $N$ (an asymptotic approximation, a heuristic for finite $N$). To keep $\mathbb E[1/w_{\max}]$ at $1 + \kappa$, $\log N$ must be about $\kappa^2\tau^2/2$, so $N$ grows like $\exp(\kappa^2\tau^2/2)$; $\kappa = 1$ gives $\exp(\tau^2/2)$.
- **Weather models.** Snyder and coworkers estimate from simulations that the Gaussian example with independent unit variances needs at least $10^{11}$ particles for a 200-dimensional state (a measurement). Weather models have far more independent observations, so the global bootstrap filter cannot be used.
- **The ways out.** The [local particle filter](/local-particle-filter/) bounds the number of observations in each weight. Proposal densities that use the observations, tempering, and Gaussian methods such as the [ensemble Kalman filter](/ensemble-kalman-filter/) are the other ways out (van Leeuwen and coworkers 2019).

## Tightness

The condition $(\log N)/\tau^2 \to 0$ is the right scale. If $\sqrt{2\log N}/\tau$ stays at a fixed $\kappa > 0$, the approximation of Snyder and coworkers gives $\mathbb E[1/w_{\max}] \to 1 + \kappa$, so $w_{\max}$ does not tend to 1 (a heuristic; Bengtsson, Bickel and Li study this boundary). A measurement with $\ell_i = \tau z_i$, the mean over 200 cases for $N = 100$ and 40 cases for $N = 10^4$:

| $N$ | $\tau$ | mean $w_{\max}$ | mean $1/w_{\max}$ | $1 + \sqrt{2\log N}/\tau$ |
|---|---|---|---|---|
| 100 | 5 | 0.66 | 1.79 | 1.61 |
| 100 | 10 | 0.83 | 1.30 | 1.30 |
| 100 | 20 | 0.91 | 1.15 | 1.15 |
| $10^4$ | 10 | 0.65 | 1.81 | 1.43 |
| $10^4$ | 20 | 0.83 | 1.32 | 1.22 |
| $10^4$ | 40 | 0.96 | 1.06 | 1.11 |

The approximation is good once $\tau$ is several times $\sqrt{2\log N}$, and the collapse is slow: $10^4$ particles at $\tau = 20$ keep about the same largest weight as $100$ particles. The Gaussian model itself is also an approximation. For a small number of observations the log likelihood is skewed, and the collapse can be faster or slower than the model predicts.

## History

Snyder, Bengtsson, Bickel and Anderson (2008) showed with asymptotic analysis and simulations that the ensemble size of the bootstrap particle filter must grow exponentially with the variance of the log likelihood, and gave the estimate of $10^{11}$ particles for a 200-dimensional state. Bengtsson, Bickel and Li (2008) gave the collapse of the largest weight in very large systems in a probabilistic form. These results motivated the local particle filters and the proposal density methods reviewed by van Leeuwen and coworkers (2019).

## References
