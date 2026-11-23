---
tag: N0BZVC
kind: definition
slug: zero-concentrated-differential-privacy
name: Zero-concentrated differential privacy
aliases:
- zCDP
- concentrated differential privacy
area: security-and-privacy/differential-privacy
level: advanced
summary: "A mechanism is rho-zCDP if the Renyi divergence of every order alpha between its outputs on neighbors is at most rho times alpha. The Gaussian meets it with equality; rho adds under composition."
prereqs: [renyi-differential-privacy, gaussian-mechanism]
see_also: [renyi-differential-privacy, privacy-loss-random-variable, discrete-gaussian-mechanism, gaussian-differential-privacy, approximate-differential-privacy, advanced-composition-theorem, group-privacy-theorem, moments-accountant]
sources:
  - paper: doi:10.1007/978-3-662-53641-4_24
    title: "Mark Bun and Thomas Steinke, Concentrated differential privacy: simplifications, extensions, and lower bounds, TCC 2016-B, LNCS 9985, pages 635 to 658"
    locator: "Definition 1.1 (zCDP), Proposition 1.3 (zCDP to approximate DP), Proposition 1.4 (pure DP to zCDP), Proposition 1.6 (Gaussian mechanism), Lemmas 1.7 and 1.8 (composition and post-processing), Proposition 1.9 (group privacy), Theorem 1.10 (mutual information bound), Definition 1.12 (approximate zCDP), Section 4 and Appendix A (comparison with mCDP)"
  - url: "https://arxiv.org/abs/1603.01887"
    title: "Cynthia Dwork and Guy N. Rothblum, Concentrated differential privacy, arXiv 1603.01887, 2016"
    locator: "the definition of (mu, tau)-concentrated differential privacy, a bound on the mean of the privacy loss and a subgaussian bound on its deviation"
  - url: "https://arxiv.org/abs/2004.00010"
    title: "Clement L. Canonne, Gautam Kamath and Thomas Steinke, The discrete Gaussian for differential privacy, NeurIPS 2020, arXiv 2004.00010"
    locator: "Theorem 4 (the discrete Gaussian mechanism satisfies the same zCDP bound as the continuous one)"
---

Zero-concentrated differential privacy (zCDP) asks that the [privacy loss random variable](/privacy-loss-random-variable/) of a mechanism behaves like a Gaussian with small mean. Formally, a mechanism is $\rho$-zCDP if, for every pair of neighbors and every order $\alpha > 1$, the Renyi divergence of order $\alpha$ between its two output laws is at most $\rho\alpha$. So zCDP is a linear bound on the whole [Renyi DP](/renyi-differential-privacy/) curve with one parameter. Bun and Steinke defined it in 2016, as a variant of the concentrated differential privacy of Dwork and Rothblum. The [Gaussian mechanism](/gaussian-mechanism/) with $\ell_2$ sensitivity $\Delta$ and noise $\sigma$ is exactly $\Delta^2/(2\sigma^2)$-zCDP, the parameter $\rho$ adds under composition, and one formula converts $\rho$ to $(\varepsilon, \delta)$-DP for every $\delta > 0$. This makes zCDP a simple budget unit for systems that add Gaussian noise many times.

## Definition

Let $D_\alpha$ be the Renyi divergence of order $\alpha$ (see [Renyi DP](/renyi-differential-privacy/)).

**Definition (Bun and Steinke).** Let $\xi \ge 0$ and $\rho \ge 0$. A randomized mechanism $M$ is **$(\xi, \rho)$-zCDP** if for all neighbors $x, x'$ and all $\alpha \in (1, \infty)$,

$$D_\alpha(M(x)\|M(x')) \le \xi + \rho\alpha.$$

It is **$\rho$-zCDP** if it is $(0, \rho)$-zCDP.

Bun and Steinke state it for datasets of $n$ entries that differ in a single entry, that is, for replace neighbors. Other systems use add/remove, and a guarantee must name the relation.

An equivalent form uses the privacy loss $Z$ of the pair: $E[e^{(\alpha - 1)Z}] \le e^{(\alpha - 1)(\xi + \rho\alpha)}$ for all $\alpha > 1$. This makes $Z$ subgaussian, close to a Gaussian with mean $\xi + \rho$ and variance $2\rho$, and gives the tail bound $\Pr[Z > \lambda + \xi + \rho] \le e^{-\lambda^2/(4\rho)}$ for $\lambda > 0$.

These properties are in Bun and Steinke's paper.

1. **Gaussian mechanism (Proposition 1.6).** Releasing $N(q(x), \sigma^2)$ for a query with sensitivity $\Delta$ is $\Delta^2/(2\sigma^2)$-zCDP, with equality at every $\alpha$.
2. **Composition (Lemma 1.7).** If $M$ is $\rho$-zCDP and $M'$ is $\rho'$-zCDP, then $x \mapsto (M(x), M'(x))$ is $(\rho + \rho')$-zCDP. The proof goes through the Renyi divergence and also covers adaptive choice of $M'$.
3. **Post-processing (Lemma 1.8).** If $M$ is $\rho$-zCDP, then $f(M(x))$ is $\rho$-zCDP for every randomized $f$.
4. **From pure DP (Proposition 1.4).** An $\varepsilon$-DP mechanism is $\frac12\varepsilon^2$-zCDP.
5. **To approximate DP (Proposition 1.3).** A $\rho$-zCDP mechanism is $(\rho + 2\sqrt{\rho\ln(1/\delta)}, \delta)$-DP for every $\delta > 0$. Lemma 3.6 of the paper is a slight sharpening.
6. **Group privacy (Proposition 1.9).** For datasets that differ in up to $k$ entries, a $\rho$-zCDP mechanism has $D_\alpha \le k^2\rho\alpha$. The Gaussian mechanism shows that $k^2$ is exact.

## Examples and non-examples

**Gaussian mechanism.** For sensitivity 1 and $\sigma = 2$, $\rho = 1/8$. With $\delta = 10^{-5}$, Proposition 1.3 gives $\varepsilon = 0.125 + 2\sqrt{0.125\ln 10^5} = 2.524$. This is the same number that the Renyi conversion $\min_\alpha(\alpha/8 + \ln(10^5)/(\alpha - 1))$ gives near $\alpha = 10.6$. The exact $\varepsilon$ of this Gaussian pair at $\delta = 10^{-5}$, from its [privacy loss distribution](/privacy-loss-random-variable/), is $1.993$; the zCDP conversion loses a little.

**Many Gaussian queries.** Answering $k$ queries of sensitivity 1, each with noise $N(0, \sigma^2)$, is $k/(2\sigma^2)$-zCDP. The $\varepsilon$ grows like $\sqrt{k\ln(1/\delta)}/\sigma$, without the extra factors that the [advanced composition theorem](/advanced-composition-theorem/) gives.

**Discrete Gaussian.** The [discrete Gaussian mechanism](/discrete-gaussian-mechanism/), which adds integer noise with mass proportional to $e^{-y^2/(2\sigma^2)}$, has the same bound $\Delta^2/(2\sigma^2)$-zCDP for an integer query of sensitivity $\Delta$ (Canonne, Kamath and Steinke, Theorem 4).

**Pure DP mechanisms.** The [Laplace mechanism](/laplace-mechanism/) with parameter $\varepsilon$ and [randomized response](/randomized-response/) with $\varepsilon = \ln 3$ are $\frac12\varepsilon^2$-zCDP, that is $0.5$-zCDP for $\varepsilon = 1$ and $0.6035$-zCDP for $\varepsilon = \ln 3$.

**Non-example: approximate DP with $\delta > 0$.** A mechanism that outputs the dataset with probability $\delta$ has infinite Renyi divergence of every order, so it is not $\rho$-zCDP for any $\rho$. Bun and Steinke also show (Theorem 1.10) that a $\rho$-zCDP mechanism on $n$ entries reveals at most $\rho n^2$ nats of mutual information about its input. This rules out stability-based methods such as propose-test-release, which are $(\varepsilon, \delta)$-DP. Their *approximate zCDP* (Definition 1.12) allows a failure event of probability $\delta$ to cover them.

**Non-example: mean-concentrated DP is a different definition.** Dwork and Rothblum's $(\mu, \tau)$-concentrated DP, which Bun and Steinke call mCDP, bounds the mean of the privacy loss by $\mu$ and its deviation from the mean by a subgaussian bound with parameter $\tau$. A $(\mu, \tau)$-mCDP mechanism is $(\mu - \tau^2/2, \tau^2/2)$-zCDP, but the converse is false, and mCDP is not closed under post-processing (Bun and Steinke, Appendix A). So "concentrated differential privacy" without a prefix is ambiguous; this page is about zCDP.

## Related definitions

- [Renyi DP](/renyi-differential-privacy/) bounds one order at a time; $\rho$-zCDP is the same as $(\alpha, \rho\alpha)$-RDP for all $\alpha > 1$.
- The [privacy loss random variable](/privacy-loss-random-variable/) is the object whose moment generating function zCDP bounds.
- [Gaussian differential privacy](/gaussian-differential-privacy/) also takes the Gaussian mechanism as the model, but compares full trade-off curves; $\mu$-GDP implies $\frac12\mu^2$-zCDP, and the conversion to $(\varepsilon, \delta)$ from GDP is exact.
- [Approximate DP](/approximate-differential-privacy/) is implied by zCDP for every $\delta > 0$ (property 5).

## References
