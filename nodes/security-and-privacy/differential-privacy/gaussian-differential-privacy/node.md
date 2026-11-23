---
tag: BW8JS6
kind: definition
slug: gaussian-differential-privacy
name: Gaussian differential privacy
aliases:
- f-differential privacy
- GDP
- mu-GDP
area: security-and-privacy/differential-privacy
level: research
summary: "States privacy as a lower bound f on the type II error of any test that tells neighbors apart at each type I error. mu-GDP takes f as the curve of N(0,1) against N(mu,1)."
prereqs: [type-i-and-type-ii-errors, neyman-pearson-lemma, privacy-loss-random-variable]
see_also: [optimal-composition-theorem, central-limit-theorem, gaussian-mechanism, zero-concentrated-differential-privacy, renyi-differential-privacy, numerical-privacy-accounting, convex-conjugate, dp-sgd]
sources:
  - url: "https://arxiv.org/abs/1905.02383"
    title: "Jinshuo Dong, Aaron Roth and Weijie J. Su, Gaussian differential privacy, Journal of the Royal Statistical Society Series B 84(1), 2022, arXiv 1905.02383"
    locator: "the definitions of trade-off functions, f-DP and mu-GDP, the composition theorem for f-DP, the central limit theorem, and the conversion between f-DP and (epsilon, delta)-DP"
  - paper: "Peter Kairouz, Sewoong Oh and Pramod Viswanath, The composition theorem for differential privacy, IEEE Transactions on Information Theory 63(6), 2017"
    locator: "the hypothesis testing view of (epsilon, delta)-DP as a region of type I and type II errors"
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), pages 211 to 407, 2014"
    locator: "Appendix A (the Gaussian mechanism), for the classical (epsilon, delta) analysis that GDP replaces"
---

Gaussian differential privacy states a privacy guarantee as a statement about hypothesis tests. An observer sees the output of a mechanism and must decide between two neighboring datasets $x$ and $x'$. Each test has a type I error (it says $x'$ when the truth is $x$) and a type II error (it says $x$ when the truth is $x'$). **$f$-differential privacy** asks that, at each type I error $a$, every test has type II error at least $f(a)$. **$\mu$-GDP** is the case where $f$ is the curve of the best test of $N(0, 1)$ against $N(\mu, 1)$. Dong, Roth and Su introduced both in 2019. The curve holds all $(\varepsilon, \delta)$ guarantees at once, without loss. The [Gaussian mechanism](/gaussian-mechanism/) with sensitivity $\Delta$ and noise $\sigma$ is exactly $(\Delta/\sigma)$-GDP, composition of $\mu_i$-GDP steps is $\sqrt{\sum \mu_i^2}$-GDP, and a central limit theorem says that the composition of many private steps of any kind tends to a Gaussian curve.

## Definition

Let $P$ and $Q$ be distributions on the same space. A test is a map $\phi$ from outputs to $[0, 1]$, the probability of rejecting $P$. Its type I error is $\alpha_\phi = E_P[\phi]$ and its type II error is $\beta_\phi = 1 - E_Q[\phi]$.

The **trade-off function** of the pair is

$$T(P, Q)(a) = \inf\{\beta_\phi : \alpha_\phi \le a\}, \qquad a \in [0, 1].$$

By the [Neyman-Pearson lemma](/neyman-pearson-lemma/), the infimum is reached by tests that reject when the [privacy loss](/privacy-loss-random-variable/) $\ln(p/q)$ is below a threshold. A function $f : [0, 1] \to [0, 1]$ is a trade-off function of some pair if and only if it is convex, continuous, non-increasing, and $f(a) \le 1 - a$ for all $a$.

**Definition ($f$-DP).** Let $f$ be a trade-off function. A mechanism $M$ is **$f$-DP** if $T(M(x), M(x')) \ge f$ pointwise for all neighbors $x, x'$.

**Definition ($\mu$-GDP).** For $\mu \ge 0$ let

$$G_\mu(a) = T(N(0, 1), N(\mu, 1))(a) = \Phi\left(\Phi^{-1}(1 - a) - \mu\right),$$

where $\Phi$ is the standard normal distribution function. A mechanism is **$\mu$-GDP** if it is $G_\mu$-DP.

These facts connect the definitions to the rest of differential privacy. They are in the paper of Dong, Roth and Su.

1. **Approximate DP is a special case.** $M$ is $(\varepsilon, \delta)$-DP if and only if it is $f_{\varepsilon, \delta}$-DP, where
$$f_{\varepsilon, \delta}(a) = \max\left(0,\; 1 - \delta - e^{\varepsilon}a,\; e^{-\varepsilon}(1 - \delta - a)\right).$$
This hypothesis testing view of $(\varepsilon, \delta)$-DP goes back to Wasserman and Zhou (2010) and to Kairouz, Oh and Viswanath, who used it for the [optimal composition theorem](/optimal-composition-theorem/).
2. **Exact conversion.** If $M$ is $f$-DP, then for each $\varepsilon$ it is $(\varepsilon, \delta(\varepsilon))$-DP with $\delta(\varepsilon) = 1 + f^*(-e^{\varepsilon})$, where $f^*$ is the [convex conjugate](/convex-conjugate/), and no smaller $\delta$ follows from $f$. For $\mu$-GDP this gives
$$\delta(\varepsilon) = \Phi\left(-\frac{\varepsilon}{\mu} + \frac{\mu}{2}\right) - e^{\varepsilon}\Phi\left(-\frac{\varepsilon}{\mu} - \frac{\mu}{2}\right) \quad\text{for all } \varepsilon \ge 0,$$
and $\mu$-GDP is equivalent to this whole family of $(\varepsilon, \delta(\varepsilon))$ guarantees.
3. **Post-processing.** If $M$ is $f$-DP, so is $g \circ M$ for every randomized map $g$.
4. **Composition.** Adaptive composition of an $f$-DP and a $g$-DP mechanism is $(f \otimes g)$-DP, where $f \otimes g$ is the trade-off function of the product pair. For Gaussian curves, $G_{\mu_1} \otimes G_{\mu_2} = G_{\sqrt{\mu_1^2 + \mu_2^2}}$.
5. **Central limit theorem.** If $k$ mechanisms are each $f_i$-DP with $f_i$ close to the identity curve $1 - a$, then under mild conditions their composition is close to $G_\mu$-DP, with $\mu$ given by simple functionals of the $f_i$. So $\mu$-GDP is the natural limit for long compositions, as in [DP-SGD](/dp-sgd/).
6. **Group privacy.** A $\mu$-GDP mechanism is $k\mu$-GDP for groups of $k$ records.

## Examples and non-examples

**Gaussian mechanism.** For a query with $\ell_2$ sensitivity $\Delta$, the pair $N(f(x), \sigma^2 I)$ and $N(f(x'), \sigma^2 I)$ is, after a rotation and a scaling, $N(0, 1)$ against $N(\mu, 1)$ with $\mu = \|f(x) - f(x')\|_2/\sigma \le \Delta/\sigma$. So the mechanism is $(\Delta/\sigma)$-GDP, and this is exact. For $\mu = 1$, $G_1(0.05) = \Phi(1.6449 - 1) = 0.7405$: a test that wrongly accuses $x'$ at most 5% of the time misses $x'$ at least 74% of the time. Fact 2 gives $\delta(1) = 0.126937$ for $\mu = 1$ and $\delta(1) = 0.0068296$ for $\mu = 1/2$.

**Composition of Gaussian steps.** Ten Gaussian steps, each $\mu_i = 1/\sqrt{10}$, compose to exactly $1$-GDP, so the whole run is $(1, 0.126937)$-DP. No Renyi or zCDP conversion loss appears.

**Randomized response.** [Randomized response](/randomized-response/) with $\varepsilon = \ln 3$ has trade-off function $\max(1 - 3a, (1 - a)/3)$, which is $f_{\ln 3, 0}$. Its curve is a broken line with a corner at $a = 1/4$. The composition of $n$ copies with parameter $1/\sqrt n$ tends to $G_1$ by fact 5: for $n = 10000$, the exact $\delta$ at $\varepsilon = 1$ is $0.126924$, against $0.126937$ for $1$-GDP.

**Non-example: a positive $\delta$ at zero type I error.** A mechanism that outputs the dataset with probability $\delta$ allows a test with type I error 0 and type II error $1 - \delta$: reject $x$ when the output is $x'$. So its trade-off function has $f(0) \le 1 - \delta < 1$, while $G_\mu(0) = 1$ for every finite $\mu$. It is $f_{0, \delta}$-DP but not $\mu$-GDP for any $\mu$.

**Non-example: GDP is not a bound on one divergence.** Two mechanisms can have the same $(\varepsilon, \delta)$ at one $\varepsilon$, or the same Renyi divergence at one order, and different trade-off curves. A single number pair does not give $f$; only the whole family of fact 2 does.

## Related definitions

- [Approximate DP](/approximate-differential-privacy/) is $f_{\varepsilon, \delta}$-DP (fact 1).
- [Zero-concentrated DP](/zero-concentrated-differential-privacy/) also models the Gaussian. Since a $\mu$-GDP pair is a post-processing of the Gaussian pair, $\mu$-GDP implies $\frac12\mu^2$-zCDP. The converse fails, and the zCDP conversion to $(\varepsilon, \delta)$ is looser than fact 2.
- The [privacy loss random variable](/privacy-loss-random-variable/) and the trade-off function carry the same information about a pair. For the Gaussian pair, the privacy loss is $N(\mu^2/2, \mu^2)$.
- [Numerical privacy accounting](/numerical-privacy-accounting/) composes privacy loss distributions exactly, which is the numerical form of the tensor product in fact 4.
- The [optimal composition theorem](/optimal-composition-theorem/) is the tensor product of fact 4 for $f_{\varepsilon, \delta}$ curves.

## References
