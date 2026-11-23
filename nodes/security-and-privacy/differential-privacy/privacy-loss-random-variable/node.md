---
tag: XCQTAN
kind: definition
slug: privacy-loss-random-variable
name: Privacy loss random variable
aliases:
- privacy loss
- privacy loss distribution
area: security-and-privacy/differential-privacy
level: advanced
summary: "The log ratio ln(p(Y)/q(Y)) of the output laws of a mechanism on two neighbors, at an output Y drawn on the first. Its law gives the exact delta for each epsilon."
prereqs: [approximate-differential-privacy, gaussian-mechanism]
see_also: [renyi-differential-privacy, zero-concentrated-differential-privacy, gaussian-differential-privacy, numerical-privacy-accounting, kullback-leibler-divergence, neyman-pearson-lemma, likelihood-ratio-test, moment-generating-function]
sources:
  - paper: doi:10.1007/978-3-662-53641-4_24
    title: "Mark Bun and Thomas Steinke, Concentrated differential privacy: simplifications, extensions, and lower bounds, TCC 2016-B, LNCS 9985, pages 635 to 658"
    locator: "Definition 1.2 (privacy loss random variable) and the statement of zCDP through it"
  - url: "https://arxiv.org/abs/2004.00010"
    title: "Clement L. Canonne, Gautam Kamath and Thomas Steinke, The discrete Gaussian for differential privacy, NeurIPS 2020, arXiv 2004.00010"
    locator: "Definition 8 (privacy loss random variable) and the characterization of approximate DP by the privacy loss after it, which cites Meiser and Mohammadi (CCS 2018, Lemma 1)"
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), pages 211 to 407, 2014"
    locator: "the definition of the privacy loss of an outcome in Chapter 2, and Section 3.5 (its use in the proof of advanced composition)"
  - paper: doi:10.1109/FOCS.2010.12
    title: "Cynthia Dwork, Guy N. Rothblum and Salil Vadhan, Boosting and differential privacy, FOCS 2010, pages 51 to 60"
    locator: "the privacy loss as a sum of bounded terms in the proof of the composition theorem"
---

The privacy loss random variable measures how much one output of a mechanism tells about which of two neighboring datasets was used. For a mechanism $M$ and neighbors $x \sim x'$, it is the log ratio $\ln(p(Y)/q(Y))$ of the probabilities of the output $Y$ under $x$ and under $x'$, where $Y$ is drawn from $M(x)$. A large positive value is an output that strongly points to $x$. The whole law of this variable, the *privacy loss distribution*, fixes every privacy guarantee of the pair: pure DP is a bound on its absolute value, the tight $\delta$ for each $\varepsilon$ is one expectation of it, [Renyi DP](/renyi-differential-privacy/) and [zCDP](/zero-concentrated-differential-privacy/) are bounds on its moment generating function, and [numerical accountants](/numerical-privacy-accounting/) compose mechanisms by convolving its law. It is the log likelihood ratio of the [Neyman-Pearson lemma](/neyman-pearson-lemma/), so it is also the best statistic for a test that tries to tell $x$ from $x'$.

## Definition

Let $M$ be a randomized mechanism and $x \sim x'$ neighbors under a stated relation (add/remove or replace). Let $P$ and $Q$ be the laws of $M(x)$ and $M(x')$, with densities $p$ and $q$ with respect to a common measure (for discrete outputs, the probability mass functions).

The **privacy loss function** of the ordered pair $(P, Q)$ is

$$\ell(y) = \ln\frac{p(y)}{q(y)},$$

with $\ell(y) = +\infty$ when $q(y) = 0 < p(y)$. The **privacy loss random variable** is $L = \ell(Y)$ with $Y \sim P$. Its law, a distribution on $\mathbb R \cup \{+\infty\}$, is the **privacy loss distribution** of the pair. The pair $(Q, P)$ has its own privacy loss, and both orders matter.

These facts follow from the definition. The function $\max(0, \cdot)$ is written $(\cdot)_+$.

1. **Exact delta.** For each $\varepsilon \ge 0$, the smallest $\delta$ with $P(S) \le e^{\varepsilon}Q(S) + \delta$ for all events $S$ is
$$\delta_{P\|Q}(\varepsilon) = \int (p - e^{\varepsilon}q)_+ = E\left[\left(1 - e^{\varepsilon - L}\right)_+\right],$$
where the term is 1 on the event $L = +\infty$. The first form is the hockey-stick divergence, reached at $S = \{\ell > \varepsilon\}$. The second form follows from $(p - e^{\varepsilon}q)_+ = p\,(1 - e^{\varepsilon}q/p)_+$. So $M$ is $(\varepsilon, \delta)$-DP if and only if $\delta_{P\|Q}(\varepsilon) \le \delta$ for every ordered pair of neighbors.
2. **Pure DP.** $M$ is $\varepsilon$-DP if and only if $|L| \le \varepsilon$ with probability 1 for every ordered pair of neighbors.
3. **A sufficient tail condition.** $\Pr[L > \varepsilon] \le \delta$ for every ordered pair implies $(\varepsilon, \delta)$-DP, because $(1 - e^{\varepsilon - L})_+ \le \mathbf 1[L > \varepsilon]$. The converse is false.
4. **Moments.** $E[L]$ is the [KL divergence](/kullback-leibler-divergence/) $D(P\|Q)$, and for $\lambda > 1$, $E[e^{(\lambda - 1)L}] = e^{(\lambda - 1)D_\lambda(P\|Q)}$, where $D_\lambda$ is the Renyi divergence. So the [moment generating function](/moment-generating-function/) of $L$ holds the Renyi divergences of all orders.
5. **Composition.** If two mechanisms run with independent coins, the privacy loss of the pair of outputs is the sum of the two privacy losses, and the two terms are independent. So the privacy loss distribution of a composition is the convolution of the distributions of its steps.

## Examples and non-examples

**Gaussian mechanism.** Let $M(x) = f(x) + N(0, \sigma^2)$ with $|f(x) - f(x')| = \Delta$, and let $\mu = \Delta/\sigma$. With $Y = f(x) + \sigma Z$ and $Z$ standard normal, a direct computation gives $\ell(Y) = \mu Z + \mu^2/2$. So $L \sim N(\mu^2/2, \mu^2)$, and fact 1 gives the analytic formula of Balle and Wang:
$$\delta(\varepsilon) = \Phi\left(-\frac{\varepsilon}{\mu} + \frac{\mu}{2}\right) - e^{\varepsilon}\Phi\left(-\frac{\varepsilon}{\mu} - \frac{\mu}{2}\right).$$
For $\mu = 1$ and $\varepsilon = 1$ this is $0.126937$; for $\mu = 1/2$ it is $0.0068296$. The law of $L$ has no bound, so the [Gaussian mechanism](/gaussian-mechanism/) is not $\varepsilon$-DP for any $\varepsilon$, by fact 2. The tail condition of fact 3 at $\mu = 1$, $\varepsilon = 1$ gives only $\Pr[L > 1] = \Pr[Z > 1/2] = 0.3085$, more than twice the exact value.

**Laplace mechanism.** Let $M(x) = f(x) + \mathrm{Lap}(b)$ with $f(x) = 0$, $f(x') = 1$ and $\varepsilon_0 = 1/b$. Then $\ell(y) = \varepsilon_0(|y - 1| - |y|)$. So $L = \varepsilon_0$ with probability $1/2$ (outputs $y \le 0$), $L = -\varepsilon_0$ with probability $e^{-\varepsilon_0}/2$ (outputs $y \ge 1$), and the rest of the mass is spread over the open interval $(-\varepsilon_0, \varepsilon_0)$. Since $|L| \le \varepsilon_0$, the [Laplace mechanism](/laplace-mechanism/) is $\varepsilon_0$-DP. Fact 1 gives $\delta(\varepsilon) = 1 - e^{(\varepsilon - \varepsilon_0)/2}$ for $0 \le \varepsilon \le \varepsilon_0$; for $\varepsilon_0 = 1$ and $\varepsilon = 0.5$ this is $0.2212$.

**Randomized response.** With parameter $\varepsilon_0 = \ln 3$, [randomized response](/randomized-response/) reports the true bit with probability $3/4$. For neighbors with bits 1 and 0, $L = \ln 3$ with probability $3/4$ and $L = -\ln 3$ with probability $1/4$. Then $E[L] = (\ln 3)/2 = 0.5493$, the KL divergence of the pair.

**The value $+\infty$.** A mechanism that outputs the whole dataset with probability $\delta$, and a fixed symbol otherwise, has $L = +\infty$ with probability $\delta$ and $L = 0$ otherwise. Fact 1 gives $\delta(\varepsilon) = \delta$ for every $\varepsilon$. It is $(0, \delta)$-DP and not $\varepsilon$-DP for any $\varepsilon$.

**Non-example: one order is not enough.** Let $P = (1/2, 1/2)$ and $Q = (1/4, 3/4)$ on two outputs. At $\varepsilon = \ln 1.2$, $\delta_{P\|Q} = 0.2$ but $\delta_{Q\|P} = 0.15$. A guarantee needs the larger value, so a page or a program that tracks only $\ell$ for $(P, Q)$ can be wrong.

**Non-example: a small mean is not privacy.** A small KL divergence $E[L]$ does not bound the tail of $L$. Two laws can have $E[L]$ close to 0 while $L$ is large on a rare output. This is why accountants track the full law, or all moments, and not only the mean.

## Related definitions

- [Approximate DP](/approximate-differential-privacy/) is the bound of fact 1 for all neighbors.
- [Renyi differential privacy](/renyi-differential-privacy/) bounds $E[e^{(\lambda - 1)L}]$ for one order; [zero-concentrated DP](/zero-concentrated-differential-privacy/) bounds it for all orders by a quadratic.
- [Gaussian differential privacy](/gaussian-differential-privacy/) compares a pair with the Gaussian pair, whose privacy loss is $N(\mu^2/2, \mu^2)$.
- The [moments accountant](/moments-accountant/) adds the logs of the moments of $L$ over the steps of an algorithm; [numerical privacy accounting](/numerical-privacy-accounting/) convolves the laws of $L$ directly.
- The [likelihood ratio test](/likelihood-ratio-test/) and the [Neyman-Pearson lemma](/neyman-pearson-lemma/) use the same statistic; the best test of $x$ against $x'$ rejects when $\ell(Y)$ is above a threshold.

## References
