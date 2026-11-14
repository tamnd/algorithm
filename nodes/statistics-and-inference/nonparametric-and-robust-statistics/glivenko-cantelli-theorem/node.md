---
tag: TMG7CE
kind: theorem
slug: glivenko-cantelli-theorem
name: Glivenko-Cantelli theorem
aliases:
- fundamental theorem of statistics
area: statistics-and-inference/nonparametric-and-robust-statistics
level: core
summary: The empirical distribution function converges to the true distribution function uniformly in x, almost surely, as the sample size grows.
prereqs: [empirical-distribution-function, law-of-large-numbers]
see_also: [dkw-inequality, kolmogorov-smirnov-test, vc-dimension, empirical-risk-minimization, rademacher-complexity, bootstrap-method, consistent-estimator, quantile]
sources:
  - paper: "V. Glivenko, Sulla determinazione empirica delle leggi di probabilità, Giornale dell'Istituto Italiano degli Attuari 4, 1933, pages 92 to 99"
    locator: the uniform convergence of the empirical distribution function to a continuous distribution function
  - paper: "F. P. Cantelli, Sulla determinazione empirica delle leggi di probabilità, Giornale dell'Istituto Italiano degli Attuari 4, 1933, pages 421 to 424"
    locator: the extension of the uniform convergence to every distribution function
  - book: isbn:9780521496032
    title: A. W. van der Vaart, Asymptotic Statistics, Cambridge University Press, 1998
    locator: Chapter 19 (empirical processes), Section 19.1 (the empirical distribution function and the proof of the Glivenko-Cantelli theorem with a finite grid)
  - paper: doi:10.1214/aoms/1177728174
    title: A. Dvoretzky, J. Kiefer and J. Wolfowitz, Asymptotic minimax character of the sample distribution function and of the classical multinomial estimator, Annals of Mathematical Statistics 27(3), 1956
    locator: pp. 642 to 669 (the exponential bound on the uniform distance, which gives the rate)
---

The Glivenko-Cantelli theorem says that the [empirical distribution function](/empirical-distribution-function/) $F_n$ of an independent sample converges to the true distribution function $F$ uniformly over the whole real line, with probability 1. The [law of large numbers](/law-of-large-numbers/) gives $F_n(t) \to F(t)$ at each single point $t$; the theorem adds that the convergence is uniform in $t$, for every $F$, with no condition of continuity or moments. So the whole distribution, and with it every quantity that depends continuously on the distribution function, can be learned from data. The [DKW inequality](/dkw-inequality/) gives the rate, and the [Kolmogorov-Smirnov test](/kolmogorov-smirnov-test/) uses the limit law of the uniform distance.

## Statement

Let $X_1, X_2, \ldots$ be independent random variables with the same distribution function $F$, and let $F_n(t) = \frac{1}{n} \#\{i \le n : X_i \le t\}$. Put

$$D_n = \sup_{t \in \mathbb{R}} \lvert F_n(t) - F(t) \rvert.$$

**Theorem (Glivenko, Cantelli).** For every distribution function $F$, $D_n \to 0$ almost surely as $n \to \infty$.

$F_n - F$ is right-continuous, so the sup equals the sup over the rational numbers and $D_n$ is a random variable. Glivenko proved the theorem for continuous $F$, and Cantelli for every $F$.

## In plain words

Draw a sample and plot the share of the sample below each value. As the sample grows, this staircase comes close to the true curve, and it comes close everywhere at the same time, not only at one point that you chose in advance.

This holds for every distribution of real numbers: smooth or with jumps, with heavy tails or without. Nothing about the shape of the distribution must be known. So a large enough sample tells you the whole distribution, up to a small error everywhere.

## Proof

Fix an integer $k \ge 2$. For $j = 1, \ldots, k - 1$ let $q_j = \inf\{t : F(t) \ge j/k\}$, and let $q_0 = -\infty$ and $q_k = +\infty$, with $F(-\infty) = F_n(-\infty) = 0$ and $F(+\infty-) = F_n(+\infty-) = 1$. Write $G(t-)$ for the limit from the left.

**Step 1: the grid controls the jumps of $F$.** By right-continuity, $F(q_j) \ge j/k$. For $t < q_j$, $F(t) < j/k$, so $F(q_j-) \le j/k$. Hence $F(q_j-) - F(q_{j-1}) \le j/k - (j-1)/k = 1/k$ for $j = 1, \ldots, k$.

**Step 2: the error between grid points.** Let $t \in [q_{j-1}, q_j)$. Both $F_n$ and $F$ are nondecreasing, so

$$F_n(t) - F(t) \le F_n(q_j-) - F(q_{j-1}) = \left(F_n(q_j-) - F(q_j-)\right) + \left(F(q_j-) - F(q_{j-1})\right),$$

$$F(t) - F_n(t) \le F(q_j-) - F_n(q_{j-1}) = \left(F(q_{j-1}) - F_n(q_{j-1})\right) + \left(F(q_j-) - F(q_{j-1})\right).$$

The intervals $[q_{j-1}, q_j)$ for $j = 1, \ldots, k$ cover $\mathbb{R}$; some can be empty when $F$ has a jump that covers several levels $j/k$. With Step 1,

$$D_n \le \max_{1 \le j \le k - 1} \max\left(\lvert F_n(q_j-) - F(q_j-) \rvert, \lvert F_n(q_j) - F(q_j) \rvert\right) + \frac{1}{k} =: M_{n,k} + \frac{1}{k},$$

because the terms with $q_0 = -\infty$ and $q_k = +\infty$ are 0.

**Step 3: finitely many points.** $F_n(q_j) = \frac{1}{n}\sum_{i \le n} \mathbf{1}\{X_i \le q_j\}$ is an average of independent Bernoulli variables with mean $F(q_j)$, and $F_n(q_j-) = \frac{1}{n}\sum_{i \le n} \mathbf{1}\{X_i < q_j\}$ is an average of independent Bernoulli variables with mean $F(q_j-)$. By the strong law of large numbers each of these $2(k - 1)$ averages converges to its mean almost surely. A finite intersection of events of probability 1 has probability 1, so $M_{n,k} \to 0$ almost surely, and $\limsup_n D_n \le 1/k$ almost surely.

**Step 4: all $k$.** The event $\{\limsup_n D_n \le 1/k \text{ for all } k \ge 2\}$ is a countable intersection of events of probability 1, so it has probability 1, and on it $D_n \to 0$. $\blacksquare$

The proof uses only independence for the strong law at each grid point, so the same argument works for any sequence for which the strong law holds at each fixed $t$, for example a stationary ergodic sequence.

## Consequences

**Consistency of plug-in estimators.** If a functional $T$ is continuous at $F$ for the sup distance, then $T(F_n) \to T(F)$ almost surely. The $p$-quantile $F_n^{-1}(p)$ converges to $F^{-1}(p)$ when $F$ is strictly increasing at $F^{-1}(p)$, so sample medians and sample [quantiles](/quantile/) are [consistent](/consistent-estimator/).

**Consistency of the Kolmogorov-Smirnov test.** If the true $F$ differs from the hypothesized $F_0$, then $\sup_t \lvert F_n - F_0 \rvert \to \sup_t \lvert F - F_0 \rvert > 0$, while the critical value tends to 0. So the test rejects with probability tending to 1 against every fixed alternative.

**The bootstrap.** The [bootstrap](/bootstrap-method/) draws from $F_n$ in place of $F$. The theorem says that $F_n$ is uniformly close to $F$ for large $n$, which is the first step of every proof that the bootstrap works.

**Learning theory.** Half-lines $(-\infty, t]$ form a class of sets of [VC dimension](/vc-dimension/) 1. The theorem is the simplest case of the uniform law of large numbers over a class of finite VC dimension, which makes [empirical risk minimization](/empirical-risk-minimization/) consistent.

**The rate.** The DKW inequality, $P(D_n > \varepsilon) \le 2e^{-2n\varepsilon^2}$, gives the rate $1/\sqrt{n}$ and, by the Borel-Cantelli lemma, a second proof of the theorem. In a Monte Carlo run with uniform data, $r = 200$ samples for each $n$ and seed 2026, the mean of $D_n$ was $0.2592$, $0.08732$, $0.02814$ and $0.008991$ for $n = 10$, $100$, $1000$ and $10000$. Times $\sqrt{n}$ these are $0.820$, $0.873$, $0.890$ and $0.899$, near the mean $\sqrt{\pi/2} \ln 2 = 0.8687$ of the Kolmogorov limit law.

## Tightness

**Not over all sets.** For continuous $F$, $\sup_A \lvert P_n(A) - P(A) \rvert = 1$ for every $n$ when the sup runs over all Borel sets $A$: the finite set $A = \{X_1, \ldots, X_n\}$ has $P_n(A) = 1$ and $P(A) = 0$. The uniform convergence needs a small class of sets, such as the half-lines.

**Not without independence or ergodicity.** If $X_i = X_1$ for all $i$ and $F$ is continuous, $F_n$ is the single step at $X_1$, and $D_n = \max(F(X_1), 1 - F(X_1)) \ge 1/2$ for every $n$. Each $X_i$ still has the distribution function $F$.

**No faster than $1/(2n)$.** For continuous $F$, $F_n$ jumps by $1/n$ at $x_{(i)}$ while $F$ does not jump, so $F_n - F$ changes by $1/n$ there and $D_n \ge 1/(2n)$ for every sample. The typical size is $1/\sqrt{n}$, by the Monte Carlo run above.

## History

Valery Glivenko (1933) proved the uniform convergence for continuous $F$, and Francesco Paolo Cantelli (1933) gave the result for every $F$; both papers appeared in volume 4 of the Giornale dell'Istituto Italiano degli Attuari, after Kolmogorov's paper on the limit law of $\sqrt{n} D_n$ in the same volume. Dvoretzky, Kiefer and Wolfowitz (1956) gave an exponential bound for $P(D_n > \varepsilon)$, and the theory of empirical processes later extended the theorem from half-lines to classes of sets and functions.

## References
