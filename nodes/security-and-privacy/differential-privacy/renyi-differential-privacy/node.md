---
tag: V30J0B
kind: definition
slug: renyi-differential-privacy
name: Renyi differential privacy
aliases:
- Renyi DP
- RDP
area: security-and-privacy/differential-privacy
level: advanced
summary: "A mechanism is (alpha, epsilon)-RDP if the Renyi divergence of order alpha between its outputs on neighbors is at most epsilon. Composition adds epsilons; the Gaussian has alpha/(2 sigma^2)."
prereqs: [privacy-loss-random-variable, kullback-leibler-divergence]
see_also: [zero-concentrated-differential-privacy, moments-accountant, gaussian-mechanism, approximate-differential-privacy, sequential-composition-theorem, privacy-amplification-by-subsampling, dp-sgd, gaussian-differential-privacy]
sources:
  - paper: doi:10.1109/CSF.2017.11
    title: "Ilya Mironov, Renyi differential privacy, IEEE 30th Computer Security Foundations Symposium (CSF 2017), pages 263 to 275"
    locator: "Definition 3 (Renyi divergence), Definition 4 ((alpha, epsilon)-RDP), Proposition 1 (composition), Proposition 2 (group privacy), Proposition 3 (conversion to (epsilon, delta)-DP), Lemma 1, Propositions 5, 6 and 7 (randomized response, Laplace and Gaussian), Table I and Table II"
  - url: "https://arxiv.org/abs/1908.10530"
    title: "Ilya Mironov, Kunal Talwar and Li Zhang, Renyi differential privacy of the sampled Gaussian mechanism, arXiv 1908.10530, 2019"
    locator: "the RDP of the subsampled Gaussian mechanism, Section 3"
  - paper: doi:10.1007/978-3-662-53641-4_24
    title: "Mark Bun and Thomas Steinke, Concentrated differential privacy: simplifications, extensions, and lower bounds, TCC 2016-B, LNCS 9985, pages 635 to 658"
    locator: "Definition 1.1 (zCDP as a bound on all Renyi divergences)"
---

Renyi differential privacy (RDP) measures privacy with the Renyi divergence of one order $\alpha > 1$. A mechanism is $(\alpha, \varepsilon)$-RDP when, for all neighbors, the Renyi divergence of order $\alpha$ from the output law on one dataset to the output law on the other is at most $\varepsilon$. Mironov introduced it in 2017. The definition sits between pure DP, which is the case $\alpha = \infty$, and approximate DP, to which it converts. Its main use is accounting: under composition the $\varepsilon$ values of the same order just add, the [Gaussian mechanism](/gaussian-mechanism/) has the simple curve $\varepsilon(\alpha) = \alpha\Delta^2/(2\sigma^2)$, and a final conversion gives an $(\varepsilon, \delta)$ guarantee that is much smaller than the one from the [advanced composition theorem](/advanced-composition-theorem/). The [moments accountant](/moments-accountant/) of DP-SGD is RDP accounting at integer orders.

## Definition

Let $P$ and $Q$ be distributions with densities $p$ and $q$ (or mass functions). For $\alpha > 1$ the **Renyi divergence** of order $\alpha$ is

$$D_\alpha(P\|Q) = \frac{1}{\alpha - 1}\ln E_{Y \sim Q}\left[\left(\frac{p(Y)}{q(Y)}\right)^{\alpha}\right] = \frac{1}{\alpha - 1}\ln \int p^{\alpha}q^{1 - \alpha},$$

with value $+\infty$ when $P$ puts mass where $Q$ has none. The limit $\alpha \to 1$ is the [KL divergence](/kullback-leibler-divergence/), and the limit $\alpha \to \infty$ is $D_\infty(P\|Q) = \sup \ln(p/q)$. In terms of the [privacy loss random variable](/privacy-loss-random-variable/) $L$ of the pair, $E[e^{(\alpha - 1)L}] = e^{(\alpha - 1)D_\alpha(P\|Q)}$.

**Definition (Mironov).** A randomized mechanism $M$ is **$(\alpha, \varepsilon)$-RDP** if $D_\alpha(M(x)\|M(x')) \le \varepsilon$ for every ordered pair of neighbors $x \sim x'$. A function $\alpha \mapsto \varepsilon(\alpha)$ that holds for each order is the **RDP curve** of $M$.

The neighbor relation (add/remove or replace) is part of the claim. These properties follow, with the numbers from Mironov's paper.

1. **Monotone in the order.** $D_\alpha$ does not decrease in $\alpha$. So $\varepsilon$-DP, which is $D_\infty \le \varepsilon$, implies $(\alpha, \varepsilon)$-RDP for every $\alpha$. Lemma 1 gives the sharper $(\alpha, 2\alpha\varepsilon^2)$-RDP for $\varepsilon$-DP.
2. **Post-processing.** If $M$ is $(\alpha, \varepsilon)$-RDP, so is $g \circ M$ for every randomized map $g$.
3. **Adaptive composition (Proposition 1).** If $M_1$ is $(\alpha, \varepsilon_1)$-RDP and $M_2(\cdot\,; y_1)$ is $(\alpha, \varepsilon_2)$-RDP for each first output $y_1$, then the pair is $(\alpha, \varepsilon_1 + \varepsilon_2)$-RDP. Curves add order by order.
4. **Conversion (Proposition 3).** If $M$ is $(\alpha, \varepsilon)$-RDP, then for every $0 < \delta < 1$ it is $\left(\varepsilon + \frac{\ln(1/\delta)}{\alpha - 1}, \delta\right)$-DP. With a full curve, take the minimum over $\alpha$. Later papers give slightly sharper conversions; the one here is the original.
5. **Group privacy (Proposition 2).** For a group of $2^c$ records, an $(\alpha, \varepsilon)$-RDP mechanism with $\alpha \ge 2^{c+1}$ is $(\alpha/2^c, 3^c\varepsilon)$-RDP.

## Examples and non-examples

**Gaussian mechanism (Proposition 7).** $D_\alpha(N(0, \sigma^2)\|N(\mu, \sigma^2)) = \alpha\mu^2/(2\sigma^2)$. So $f(x) + N(0, \sigma^2)$ with $\ell_2$ sensitivity $\Delta$ is $(\alpha, \alpha\Delta^2/(2\sigma^2))$-RDP for every $\alpha$, and $k$ such steps give $k\alpha\Delta^2/(2\sigma^2)$, the curve of one Gaussian with noise $\sigma/\sqrt k$. For $\Delta = 1$ and $\sigma = 2$ the curve is $\alpha/8$. With $\delta = 10^{-5}$, the conversion $\alpha/8 + \ln(10^5)/(\alpha - 1)$ has its minimum $2.524$ near $\alpha = 10.6$.

**Laplace mechanism (Proposition 6).** For $\mathrm{Lap}(b)$ noise and sensitivity 1,
$$D_\alpha = \frac{1}{\alpha - 1}\ln\left(\frac{\alpha}{2\alpha - 1}e^{(\alpha - 1)/b} + \frac{\alpha - 1}{2\alpha - 1}e^{-\alpha/b}\right).$$
For $b = 1$ this is $0.6191$ at $\alpha = 2$ and $0.9930$ at $\alpha = 100$, and it tends to $1/b = 1$, the pure DP parameter, as $\alpha \to \infty$.

**Randomized response (Proposition 5).** If the true bit is reported with probability $p > 1/2$,
$$D_\alpha = \frac{1}{\alpha - 1}\ln\left(p^{\alpha}(1-p)^{1-\alpha} + (1-p)^{\alpha}p^{1-\alpha}\right).$$
For $p = 3/4$ this is $\ln(7/3) = 0.8473$ at $\alpha = 2$. It tends to $(2p - 1)\ln\frac{p}{1-p} = 0.5493$ as $\alpha \to 1$ and to $\ln 3 = 1.0986$ as $\alpha \to \infty$.

**Subsampled Gaussian.** When each record joins a batch with probability $q$ and the batch gets Gaussian noise, the curve has no simple closed form. At integer orders it is a finite sum (Mironov, Talwar and Zhang), which the [moments accountant](/moments-accountant/) evaluates. For small $q$ it is about $q^2$ times the curve without sampling, which is the effect of [amplification by subsampling](/privacy-amplification-by-subsampling/).

**Non-example: approximate DP with $\delta > 0$.** Let $M$ output the whole dataset with probability $\delta$ and a fixed symbol otherwise. It is $(0, \delta)$-DP. But $M(x)$ puts mass $\delta$ on the output $x$, where $M(x')$ has none, so $D_\alpha(M(x)\|M(x')) = +\infty$ for every $\alpha > 1$. No $(\varepsilon, \delta)$ guarantee with $\delta > 0$ gives a finite RDP bound. Such mechanisms must be accounted for in another way, for example with [numerical privacy accounting](/numerical-privacy-accounting/).

**Non-example: one order is not pure DP.** The Gaussian mechanism is $(\alpha, \alpha/8)$-RDP for each finite $\alpha$ when $\Delta = 1$ and $\sigma = 2$, but the curve grows without bound, and the mechanism is not $\varepsilon$-DP for any $\varepsilon$. A finite $(\alpha, \varepsilon)$ bound at one order says nothing about outputs of very small probability; it gives only $(\varepsilon', \delta)$ with $\delta > 0$.

## Related definitions

- [Zero-concentrated DP](/zero-concentrated-differential-privacy/) asks for an RDP curve $\varepsilon(\alpha) \le \rho\alpha$ at all orders at once. The Gaussian mechanism meets it with equality.
- The [privacy loss random variable](/privacy-loss-random-variable/) gives the same quantity: $(\alpha, \varepsilon)$-RDP bounds the moment $E[e^{(\alpha - 1)L}]$ by $e^{(\alpha - 1)\varepsilon}$.
- The [moments accountant](/moments-accountant/) of Abadi et al. (2016) tracks $\ln E[e^{\lambda L}]$, which is $\lambda D_{\lambda + 1}$, so it is RDP with the order shifted by 1.
- [Gaussian differential privacy](/gaussian-differential-privacy/) uses the full trade-off curve instead of one divergence, and does not lose in the conversion to $(\varepsilon, \delta)$.
- [Approximate DP](/approximate-differential-privacy/) is the target of the conversion in property 4.

## References
