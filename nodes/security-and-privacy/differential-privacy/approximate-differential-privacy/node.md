---
tag: 8KEDN3
kind: definition
slug: approximate-differential-privacy
name: Approximate differential privacy
aliases:
- (epsilon delta)-differential privacy
area: security-and-privacy/differential-privacy
level: core
summary: Relaxes differential privacy by an additive delta, so that the e^epsilon bound may fail with a small probability.
prereqs: [differential-privacy-definition, total-variation-distance]
see_also: [gaussian-mechanism, privacy-loss-random-variable, group-privacy-theorem, advanced-composition-theorem, renyi-differential-privacy, zero-concentrated-differential-privacy, gaussian-differential-privacy, propose-test-release]
sources:
  - paper: doi:10.1007/11761679_29
    title: "Cynthia Dwork, Krishnaram Kenthapadi, Frank McSherry, Ilya Mironov and Moni Naor, Our data, ourselves: privacy via distributed noise generation, EUROCRYPT 2006, LNCS 4004, pages 486 to 503"
    locator: the first definition with an additive delta, used for noise that is a sum of many small shares
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), 2014, pages 211 to 407"
    locator: "Section 2.3, Definition 2.4 and the discussion of delta after it, Proposition 2.1, and the footnote to Theorem 2.2 (group privacy with delta); Section 3.5, Theorem 3.16 (composition) and Lemma 3.17 (the characterization by a delta-close distribution)"
  - url: "https://arxiv.org/abs/1805.06530"
    title: "Borja Balle and Yu-Xiang Wang, Improving the Gaussian mechanism for differential privacy: analytical calibration and optimal denoising, ICML 2018, PMLR 80"
    locator: "Theorem 5 (the exact condition for (epsilon, delta)-DP in terms of the privacy loss) and Theorem 8 (the analytic Gaussian mechanism)"
---

Approximate differential privacy, or $(\varepsilon, \delta)$-differential privacy, relaxes [pure differential privacy](/differential-privacy-definition/) by an additive term $\delta$. A mechanism is $(\varepsilon, \delta)$-DP if, for neighboring datasets, the probability of each set of outputs grows by at most the factor $e^{\varepsilon}$ plus $\delta$. The term $\delta$ lets the multiplicative bound fail on rare outputs, and this is what allows Gaussian noise, the [advanced composition theorem](/advanced-composition-theorem/) and other tools with much less noise than pure DP. Dwork, Kenthapadi, McSherry, Mironov and Naor (2006) introduced it. The value of $\delta$ must be much smaller than $1/n$, because a mechanism that publishes whole records with probability $\delta$ is $(0, \delta)$-DP.

## Definition

Datasets, the two neighbor relations (add/remove and replace) and mechanisms are as on the page of [pure differential privacy](/differential-privacy-definition/). Every claim must say which relation it uses.

**Definition.** Let $\varepsilon \ge 0$ and $0 \le \delta < 1$. A mechanism $M$ is **$(\varepsilon, \delta)$-differentially private** under a neighbor relation $\sim$ if, for all $x \sim x'$ and all sets $S$ of outputs,

$$\Pr[M(x) \in S] \le e^{\varepsilon}\Pr[M(x') \in S] + \delta.$$

The case $\delta = 0$ is $\varepsilon$-DP. The case $\varepsilon = 0$ says that the [total variation distance](/total-variation-distance/) between $M(x)$ and $M(x')$ is at most $\delta$. The probability is over the coins of $M$, and the bound must hold for both orders of each pair.

**Hockey-stick form.** For distributions $P$ and $Q$ and $a \ge 1$, the hockey-stick divergence is

$$H_a(P \,\|\, Q) = \sup_S \big(P(S) - a\,Q(S)\big) = \sum_y \max\big(0,\ P(y) - a\,Q(y)\big),$$

where the sum is for discrete outputs and becomes an integral of densities otherwise. The supremum is reached at $S = \{y : P(y) > aQ(y)\}$. So $M$ is $(\varepsilon, \delta)$-DP if and only if $H_{e^{\varepsilon}}(M(x) \,\|\, M(x')) \le \delta$ for every ordered pair of neighbors. The smallest such $\delta$, as a function of $\varepsilon$, is the **privacy profile** $\delta(\varepsilon)$ of the mechanism.

**Privacy loss form.** With the [privacy loss random variable](/privacy-loss-random-variable/) $L = \ln(P(Y)/Q(Y))$, $Y \sim P = M(x)$ and $Q = M(x')$,

$$H_{e^{\varepsilon}}(P \,\|\, Q) = \mathbb E\big[\max(0,\ 1 - e^{\varepsilon - L})\big] \le \Pr[L > \varepsilon].$$

The equality is the sum above with $P(y)$ taken out. So a bound $\Pr[L > \varepsilon] \le \delta$ for every ordered pair is enough for $(\varepsilon, \delta)$-DP. It is not necessary; the exact condition is the bound on the expectation. Balle and Wang (2018, Theorem 5) give the exact condition as $\Pr[L \ge \varepsilon] - e^{\varepsilon}\Pr[L' \le -\varepsilon] \le \delta$, where $L'$ is the privacy loss of the pair in the other order, which is the same quantity written with two tails.

**Close-distribution form (Dwork-Roth Lemma 3.17, part 1).** $\Pr[M(x) \in S] \le e^{\varepsilon}\Pr[M(x') \in S] + \delta$ for all $S$ if and only if there is a distribution $P'$ with total variation distance at most $\delta$ from $M(x)$ and $P'(S) \le e^{\varepsilon}\Pr[M(x') \in S]$ for all $S$. So $\delta$ is the mass that must be moved before the pure bound holds.

**Basic properties.** $(\varepsilon, \delta)$-DP is kept by any processing of the output that does not read the data (the [post-processing theorem](/post-processing-theorem/); Dwork-Roth Proposition 2.1). Mechanisms with $(\varepsilon_i, \delta_i)$, run in sequence, give $(\sum_i \varepsilon_i, \sum_i \delta_i)$ (the [sequential composition theorem](/sequential-composition-theorem/); Dwork-Roth Theorem 3.16). Datasets at distance $k$ get $(k\varepsilon, k e^{(k-1)\varepsilon}\delta)$ (the [group privacy theorem](/group-privacy-theorem/)), so $\delta$ grows much faster than $\varepsilon$.

## Examples and non-examples

**The Gaussian mechanism.** Add $N(0, \sigma^2)$ noise to a query whose value moves by $\Delta = 1$ in the $\ell_2$ norm between neighbors. The privacy profile is $\delta(\varepsilon) = \Phi(\frac{1}{2\sigma} - \varepsilon\sigma) - e^{\varepsilon}\Phi(-\frac{1}{2\sigma} - \varepsilon\sigma)$, where $\Phi$ is the standard normal distribution function (Balle and Wang 2018, Theorem 8). With $\sigma = 1$ it gives $\delta(1) = 0.126937$; with $\sigma = 2$ it gives $\delta(1) = 0.0068296$. Its privacy loss is unbounded, so it is not $\varepsilon$-DP for any $\varepsilon$, and $\delta > 0$ is needed. See the [Gaussian mechanism](/gaussian-mechanism/).

**Pure DP mechanisms have a profile too.** The [Laplace mechanism](/laplace-mechanism/) with sensitivity 1 and scale $b = 1$ is $(1, 0)$-DP. For a smaller $\varepsilon'$ it is $(\varepsilon', \delta)$-DP with $\delta = 1 - e^{(\varepsilon' - 1)/2}$, from a direct integration of the hockey-stick divergence of two Laplace densities at distance 1. At $\varepsilon' = 0.5$ this is $0.221199$, and at $\varepsilon' = 0$ it is the total variation distance $1 - e^{-1/2} = 0.393469$. So one mechanism satisfies a whole curve of $(\varepsilon, \delta)$ pairs.

**Non-example: the release of a few whole records.** Let $M$ publish each record independently with probability $\delta$. Under add/remove, $M(x)$ is the output of $M(x')$ plus, with probability $\delta$, the extra record. So the hockey-stick divergence at $e^{0} = 1$ is exactly $\delta$, and $M$ is $(0, \delta)$-DP. Yet it publishes about $n\delta$ records in full: with $n = 10^6$ and $\delta = 10^{-5}$, about 10 people lose all privacy. This is why $\delta$ must be much smaller than $1/n$. Dwork and Roth (Section 2.3) say that $\delta$ of the order $1/\lVert x \rVert_1$ is very dangerous for this reason, and ask for $\delta$ below the inverse of any polynomial in $n$.

**Non-example: "the loss is at most $\varepsilon$ with probability $1 - \delta$".** This informal reading is not exact. Let $M(x)$ output 1 with probability 0.51 and 0 with probability 0.49, and let $M(x')$ output each bit with probability 0.5. The total variation distance is 0.01, so the pair is $(0, 0.01)$-DP. But the privacy loss is $\ln 1.02 = 0.0198$ or $\ln 0.98 = -0.0202$, so $|L| > 0 = \varepsilon$ with probability 1. The reading holds only in the other direction (a bound on $\Pr[L > \varepsilon]$ gives $(\varepsilon, \delta)$-DP), or with changed parameters.

**Non-example: a mechanism with a data-dependent noise scale.** Add Laplace noise scaled to the local sensitivity at $x$, the largest change of the query between $x$ and its own neighbors. If that value is 0 at $x$ and positive at a neighbor $x'$, then $M(x)$ is the exact answer with probability 1, while $M(x')$ hits that one point with probability 0. So $M$ is not $(\varepsilon, \delta)$-DP for any $\varepsilon$ and any $\delta < 1$: the scale itself reveals the data. [Propose-test-release](/propose-test-release/) fixes this with a private test, and it is $(\varepsilon, \delta)$-DP and not pure.

## Related definitions

- **Pure DP.** [$\varepsilon$-DP](/differential-privacy-definition/) is the case $\delta = 0$. It composes and protects groups with no growth of $\delta$.
- **Privacy loss and accounting.** The [privacy loss random variable](/privacy-loss-random-variable/) gives the exact profile. [Numerical privacy accounting](/numerical-privacy-accounting/) composes profiles exactly, and the [advanced composition theorem](/advanced-composition-theorem/) gives a closed-form bound of about $\varepsilon\sqrt{k}$ for $k$ mechanisms with a small $\varepsilon$.
- **Divergence forms.** [Renyi DP](/renyi-differential-privacy/), [zero-concentrated DP](/zero-concentrated-differential-privacy/) and [Gaussian DP](/gaussian-differential-privacy/) bound other measures of distance and convert to $(\varepsilon, \delta)$-DP. They compose more simply, which is why they are used for the Gaussian mechanism and [DP-SGD](/dp-sgd/).
- **The mechanisms.** The [Gaussian mechanism](/gaussian-mechanism/) calibrates its noise to the sensitivity in the $\ell_2$ norm and needs $\delta > 0$.

## References
