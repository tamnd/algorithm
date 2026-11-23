---
tag: B229GK
kind: algorithm
slug: gaussian-mechanism
name: Gaussian mechanism
aliases:
- Gaussian noise mechanism
area: security-and-privacy/differential-privacy
level: core
summary: Adds Gaussian noise scaled to the l2 sensitivity, which gives (epsilon, delta)-differential privacy and composes well.
model: real-ram
complexity:
  vars: {k: the number of coordinates of the query, T: the number of bisection steps of the analytic calibration}
  time: {worst: O(k + T)}
  space: {extra: O(k)}
properties: {deterministic: false, randomized: true}
history:
  year: 2006
  people: [Cynthia Dwork, Krishnaram Kenthapadi, Frank McSherry, Ilya Mironov, Moni Naor]
  note: Dwork, Kenthapadi, McSherry, Mironov and Naor used Gaussian noise for (epsilon, delta)-privacy at EUROCRYPT 2006. Balle and Wang gave the exact calibration in 2018.
prereqs: [approximate-differential-privacy, global-sensitivity]
see_also: [laplace-mechanism, discrete-gaussian-mechanism, privacy-loss-random-variable, zero-concentrated-differential-privacy, gaussian-differential-privacy, renyi-differential-privacy, dp-sgd, bisection-method]
sources:
  - paper: doi:10.1007/11761679_29
    title: "Cynthia Dwork, Krishnaram Kenthapadi, Frank McSherry, Ilya Mironov and Moni Naor, Our data, ourselves: privacy via distributed noise generation, EUROCRYPT 2006, LNCS 4004, pages 486 to 503"
    locator: the relaxed definition with an additive delta and the use of Gaussian noise
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), 2014, pages 211 to 407"
    locator: "Section 3.5.3, Definition 3.8 (l2 sensitivity) and Theorem 3.22 (the classical bound, for epsilon in (0, 1)); Appendix A, Theorem A.1 (the same theorem with its proof)"
  - paper: arxiv:1805.06530
    title: "Borja Balle and Yu-Xiang Wang, Improving the Gaussian mechanism for differential privacy: analytical calibration and optimal denoising, ICML 2018, PMLR 80"
    locator: "Theorem 1 (the classical mechanism), Lemma 3 (the privacy loss is Gaussian), Theorem 5 (the exact condition for (epsilon, delta)-DP), Theorem 8 (the analytic Gaussian mechanism)"
  - paper: "Ilya Mironov, On significance of the least significant bits for differential privacy, ACM CCS 2012, pages 650 to 661"
    locator: why floating-point noise is not private
  - paper: "Clement L. Canonne, Gautam Kamath and Thomas Steinke, The discrete Gaussian for differential privacy, NeurIPS 2020"
    locator: the discrete Gaussian and its exact sampler
---

The Gaussian mechanism answers a numeric query about a private dataset with independent normal noise added to each coordinate. The noise has standard deviation $\sigma$ proportional to the $\ell_2$ [sensitivity](/global-sensitivity/) $\Delta_2 f$, and the output is $(\varepsilon, \delta)$-[differentially private](/approximate-differential-privacy/). It is never $\varepsilon$-DP with $\delta = 0$. Its strength is that it scales to the $\ell_2$ norm and not to the $\ell_1$ norm, so a vector of $k$ counts needs noise of size about $\sqrt k$ per count in place of $k$, and that its privacy loss is itself a normal random variable, so many runs compose in a simple closed form. It is the noise of [DP-SGD](/dp-sgd/).

## In plain words

You want to publish many numbers about a table at once, for example 100 counts, and one person can change each count by at most one. The [Laplace mechanism](/laplace-mechanism/) must protect the worst total change, which is 100, so it adds a lot of noise to each count. The Gaussian mechanism measures the change of the whole vector as a length, which is only $\sqrt{100} = 10$. It adds bell-shaped noise of that scale to each count.

The price is a small $\delta$. Bell-shaped noise has thin tails. On a rare output far out in a tail, the ratio between the probabilities under two neighboring tables can be very large. So the guarantee is "the ratio is at most $e^{\varepsilon}$, except on events of total probability about $\delta$". You choose $\delta$ much smaller than one over the number of people.

## The problem

The input is a dataset $x = (x_1, \ldots, x_n)$ of records from a universe $\mathcal X$, a query $f$ that maps datasets to $\mathbb R^k$, a number $\Delta \ge \Delta_2 f$, and privacy parameters $\varepsilon \ge 0$ and $0 < \delta < 1$. Here

$$\Delta_2 f = \max_{x \sim x'} \lVert f(x) - f(x') \rVert_2 ,$$

and $x \sim x'$ means that $x$ and $x'$ are neighbors. The page uses add/remove neighbors (one record added or removed) unless it says otherwise. A histogram has $\Delta_2 = 1$ under add/remove and $\Delta_2 = \sqrt 2$ under replace (one record changes, so one count falls and one rises). Note that $\sqrt 2 < 2 = \Delta_1$ under replace.

The output is a random vector $y \in \mathbb R^k$. The map from $x$ to the distribution of $y$ must be $(\varepsilon, \delta)$-DP: $\Pr[y \in S \mid x] \le e^{\varepsilon} \Pr[y \in S \mid x'] + \delta$ for all neighbors and all sets $S$.

The normal distribution $N(0, \sigma^2)$ has density $\frac{1}{\sigma\sqrt{2\pi}} e^{-z^2/(2\sigma^2)}$. We write $\Phi$ for the standard normal distribution function. The site has no page on the normal distribution, so this is its definition here.

## The algorithm

There are two ways to choose $\sigma$. The classical bound of Dwork and Roth is a closed form, and it is proved only for $0 < \varepsilon < 1$. The analytic bound of Balle and Wang is the smallest $\sigma$ that works, for every $\varepsilon \ge 0$, and it is found by [bisection](/bisection-method/) on the function

$$\delta_\Delta(s) = \Phi\Big(\frac{\Delta}{2s} - \frac{\varepsilon s}{\Delta}\Big) - e^{\varepsilon}\, \Phi\Big(-\frac{\Delta}{2s} - \frac{\varepsilon s}{\Delta}\Big),$$

which falls as $s$ grows.

```pseudo id=main
GAUSSIAN-MECHANISM(x, f, Delta, epsilon, delta)    ▷ Delta >= the l2 sensitivity of f
L1  sigma <- the smallest s with delta_Delta(s) <= delta    ▷ analytic; classical: Delta sqrt(2 ln(1.25/delta)) / epsilon
L2  v <- f(x)                                      ▷ v = (v_1, ..., v_k)
L3  for i <- 1 to k do
L4      draw z from N(0, sigma^2)
L5      y_i <- v_i + z
L6  return y = (y_1, ..., y_k)
```

Line L1 does not read the data. It depends only on $\Delta$, $\varepsilon$ and $\delta$, so it can run once and be reused for every query with the same parameters. The code doubles an upper end until $\delta_\Delta$ is at most $\delta$, then halves the bracket $T$ times, and returns the upper end of the final bracket, so the returned $\sigma$ is never too small. Line L2 is the only line that reads the data. Line L4 draws a fresh normal sample for each coordinate, and the samples are never published or reused.

The code on this site uses floats and the seeded generator `random.Random.gauss`, so that the tests can repeat each run. A deployment needs a cryptographic source of randomness and an exact sampler, because float noise leaks through its low-order bits (Mironov 2012). The [discrete Gaussian mechanism](/discrete-gaussian-mechanism/) adds integer noise with an exact sampler (Canonne, Kamath and Steinke 2020).

## Example

The universe is $\{0, 1, 2\}$ and the dataset is $x = (0, 0, 1, 2, 2, 2)$, so the [histogram](/histogram/) is $f(x) = (2, 1, 3)$ with $\Delta_2 f = 1$ under add/remove neighbors. Take $\varepsilon = 1$ and $\delta = 10^{-5}$. The classical bound does not apply, because it needs $\varepsilon < 1$. Line L1 with the analytic bound gives $\sigma = 3.730632$. Assume that line L4 draws $z = \sigma g$ for the standard normal values $g = 0.5, -1.2, 0.1$.

| step | $i$ | $v_i$ | $g$ | $z$ (line L4) | $y_i$ (line L5) |
|---|---|---|---|---|---|
| L1, L2 | | | | | $\sigma = 3.730632$, $v = (2, 1, 3)$ |
| L3 to L5 | 1 | 2 | 0.5 | 1.865316 | 3.865316 |
| L3 to L5 | 2 | 1 | $-1.2$ | $-4.476758$ | $-3.476758$ |
| L3 to L5 | 3 | 3 | 0.1 | 0.373063 | 3.373063 |
| L6 | | | | | $y = (3.865316, -3.476758, 3.373063)$ |

A negative count is a normal output. Rounding and clamping it to $[0, n]$ is [post-processing](/post-processing-theorem/) and keeps the guarantee.

The two calibrations for $\Delta = 1$, $\delta = 10^{-5}$:

| $\varepsilon$ | classical $\sigma$ | analytic $\sigma$ | ratio of the variances |
|---|---|---|---|
| 0.1 | 48.448053 | 30.749566 | 0.403 |
| 0.5 | 9.689611 | 7.031827 | 0.527 |
| 0.9 | 5.383117 | 4.106624 | 0.582 |
| 1 | not proved | 3.730632 | |
| 2 | not proved | 1.993812 | |

So the analytic bound removes 40 to 60 percent of the variance in this range. At the classical $\sigma = 9.6896$ for $\varepsilon = 0.5$, the exact $\delta_\Delta$ is only $1.6 \times 10^{-8}$, far below the target $10^{-5}$. Two more check values: with $\Delta = 1$ and $\varepsilon = 1$, $\sigma = 1$ gives the exact $\delta = 0.126937$ and $\sigma = 2$ gives $\delta = 0.0068296$.

## Correctness

**Theorem (classical; Dwork-Roth Theorem 3.22, proved as Theorem A.1).** Let $0 < \varepsilon < 1$ and $0 < \delta < 1$. If $\sigma \ge c\Delta/\varepsilon$ with $c^2 \ge 2\ln(1.25/\delta)$ and $\Delta \ge \Delta_2 f$, then GAUSSIAN-MECHANISM is $(\varepsilon, \delta)$-DP. Dwork and Roth state it with a strict inequality for $c^2$; the proof of this page covers equality, which is what the code uses.

**Theorem (analytic; Balle and Wang 2018, Theorem 8).** For every $\varepsilon \ge 0$ and $\delta \in [0, 1]$, adding $N(0, \sigma^2 I)$ noise to a query of $\ell_2$ sensitivity $\Delta$ is $(\varepsilon, \delta)$-DP if and only if $\delta_\Delta(\sigma) \le \delta$.

The key step is that the [privacy loss](/privacy-loss-random-variable/) is normal. For neighbors with $D = \lVert f(x) - f(x') \rVert_2$ and $\mu = D/\sigma$, the loss $L = \ln(p_x(Y)/p_{x'}(Y))$ with $Y \sim M(x)$ has the distribution $N(\mu^2/2, \mu^2)$, because only the noise along the direction of $f(x) - f(x')$ matters. The tight $\delta$ for this pair is $\Pr[L > \varepsilon] - e^{\varepsilon}\Pr[L' > \varepsilon]$, with $L' \sim N(-\mu^2/2, \mu^2)$ the loss under $x'$, and this is exactly $\delta_D(\sigma)$. It grows with $D$, so the worst pair has $D = \Delta$. The full proofs, with the proof of the classical bound from the normal tail, are in the correctness proof of this page.

**Accuracy.** Each coordinate has error $N(0, \sigma^2)$, so $\Pr[|y_i - f(x)_i| > t] = 2\Phi(-t/\sigma)$. By a [union bound](/union-bound/), with probability at least $1 - \beta$ all $k$ errors are at most $\sigma \sqrt{2 \ln(2k/\beta)}$. The total squared error has mean $k\sigma^2$.

## Complexity

The model is the [real RAM](/real-ram/): a normal sample, an exponential, an evaluation of $\Phi$ and an arithmetic step each cost one unit. The cost is counted per query, after the one evaluation of $f$ in line L2.

- **Time.** Line L1 with the classical bound is $O(1)$. With the analytic bound it is $O(T)$ evaluations of $\delta_\Delta$, where $T$ is the number of bisection steps; the code stops when the bracket is below $10^{-12}$ times its upper end, which is about 40 steps, plus a few doublings to find the bracket. The loop of line L3 runs $k$ times with $O(1)$ work. So the time is $O(k + T)$ in the worst case.
- **Space.** The output has $k$ numbers, and the rest is $O(1)$. So the extra space is $O(k)$.

## Properties

- **Approximate only.** For $\delta = 0$ no $\sigma$ works: the log ratio of the two densities at $y$ is linear in $y$, so it is unbounded. The tests measure it on a grid: 3.5 on $[-3, 3]$ and 30.5 on $[-30, 30]$ for $\Delta = \sigma = 1$.
- **Tight.** The analytic condition is necessary and sufficient. A $\sigma$ below the analytic value fails for the worst pair, and the tests check that $0.999999\,\sigma$ gives a $\delta$ above the target.
- **$\ell_2$ scale.** For $k$ counts that one record can each change by 1, $\Delta_2 = \sqrt k$ while $\Delta_1 = k$. So the noise per count grows like $\sqrt k$ for the Gaussian mechanism and like $k$ for the Laplace mechanism, for a fixed $\varepsilon$ and $\delta$.
- **Closed-form composition.** For one pair of neighbors, the losses of $m$ independent runs add, and a sum of independent normal losses $N(\mu_j^2/2, \mu_j^2)$ is the normal loss with $\mu^2 = \sum_j \mu_j^2$. Dong, Roth and Su (2019) prove the same rule for adaptive runs: the composition is $\sqrt{\sum_j \mu_j^2}$-GDP. In the language of other pages, the mechanism is $\mu$-GDP with $\mu = \Delta/\sigma$ ([Gaussian differential privacy](/gaussian-differential-privacy/)), $\rho$-zCDP with $\rho = \Delta^2/(2\sigma^2)$ ([zero-concentrated DP](/zero-concentrated-differential-privacy/)), and $(\alpha, \alpha\Delta^2/(2\sigma^2))$-RDP for every $\alpha > 1$ ([Renyi DP](/renyi-differential-privacy/)). With $\Delta = 1$ and $\sigma = 2$ this is $\rho = 1/8$.
- **Unbiased.** $\mathbb E[y] = f(x)$ and the covariance is $\sigma^2 I$, so the noise adds cleanly to other normal errors in a statistical analysis.

## Variants and improvements

- **Analytic calibration.** Balle and Wang (2018) give the condition of line L1 and a stable way to solve it. This is the version the code uses by default.
- **Discrete Gaussian.** The [discrete Gaussian mechanism](/discrete-gaussian-mechanism/) adds integer noise with $\Pr[Z = z] \propto e^{-z^2/(2\sigma^2)}$, with almost the same guarantees and an exact sampler.
- **Correlated noise.** Noise $N(0, \Sigma)$ with a general covariance fits queries whose sensitivity set is an ellipsoid. The [matrix mechanism](/matrix-mechanism/) is one way to design it.
- **Denoising.** Balle and Wang also post-process the output with estimators that know the noise distribution, which reduces the error in high dimension. This is post-processing and costs no privacy.
- **Noisy gradients.** [DP-SGD](/dp-sgd/) clips each gradient to $\ell_2$ norm $C$, so that the sum has $\Delta_2 = C$, and adds Gaussian noise to the sum at each step. Its accounting uses the [moments accountant](/moments-accountant/) or [numerical privacy accounting](/numerical-privacy-accounting/).

## When to use it

Use the Gaussian mechanism when you answer many numeric queries, or a vector query whose $\ell_2$ sensitivity is much smaller than its $\ell_1$ sensitivity, and a small $\delta$ is acceptable. It is also the right choice when the release is one step of an iterative algorithm, because its composition is exact in closed form. For one or a few low-dimensional queries with pure $\varepsilon$-DP, use the [Laplace mechanism](/laplace-mechanism/). For integer output, use the discrete Gaussian mechanism.

## Pitfalls

- **The classical formula for $\varepsilon \ge 1$.** Line L1 with $\sigma = \Delta\sqrt{2\ln(1.25/\delta)}/\varepsilon$ is proved only for $\varepsilon < 1$, and it fails for larger $\varepsilon$. With $\Delta = 1$, $\varepsilon = 10$ and $\delta = 10^{-5}$ it gives $\sigma = 0.4845$, and the exact $\delta$ at this $\sigma$ is $2.27 \times 10^{-5}$, more than twice the target. Use the analytic calibration for any $\varepsilon$; the code raises an error for the classical formula outside $(0, 1)$.
- **$\ell_1$ in place of $\ell_2$, or the reverse.** Line L1 must use $\Delta_2 f$. Using $\Delta_1$ is safe but wastes accuracy. Using $\Delta_2$ in the Laplace mechanism is not safe.
- **The wrong neighbor relation.** A histogram has $\Delta_2 = 1$ under add/remove and $\sqrt 2$ under replace. A calibration with $\Delta = 1$ under replace gives a larger $\delta$ than claimed.
- **A large $\delta$.** The mechanism that publishes each record with probability $\delta$ is $(0, \delta)$-DP, and it publishes about $n\delta$ records. Choose $\delta$ much smaller than $1/n$ (Dwork-Roth Section 2.3).
- **Float noise.** `random.gauss` on floats is fine for study and not for a release (Mironov 2012). Use an exact discrete sampler from a cryptographic source.

## Implementations

## History

Dwork, Kenthapadi, McSherry, Mironov and Naor (EUROCRYPT 2006) introduced the additive $\delta$ in the definition and used Gaussian noise, which is a sum of many small contributions in their distributed setting. Dwork and Roth (2014) give the classical bound for $\varepsilon < 1$ with its proof, and note that the bound is folklore. Balle and Wang (ICML 2018) showed that the classical bound is loose for small $\varepsilon$ and does not extend to large $\varepsilon$, and gave the exact condition. Bun and Steinke (2016), Mironov (2017) and Dong, Roth and Su (2019) built the zCDP, RDP and GDP frameworks around the normal privacy loss of this mechanism.

## References
