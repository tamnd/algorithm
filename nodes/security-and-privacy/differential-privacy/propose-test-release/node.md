---
tag: DV793R
kind: algorithm
slug: propose-test-release
name: Propose-test-release
aliases:
- PTR
area: security-and-privacy/differential-privacy
level: advanced
summary: Proposes a bound on the local sensitivity, tests with noise that the data is far from any dataset that breaks it, and only then releases the answer with noise for that bound.
model: real-ram
complexity:
  vars: {n: the number of values}
  time: {worst: O(n^2)}
  space: {extra: O(n)}
history:
  year: 2009
  people: [Cynthia Dwork, Jing Lei]
  note: Dwork and Lei gave the framework at STOC 2009, in a paper on differential privacy and robust statistics, with private estimates of scale, the median and regression coefficients.
prereqs: [differential-privacy-definition, approximate-differential-privacy, global-sensitivity, laplace-mechanism]
see_also: [smooth-sensitivity, subsample-and-aggregate, median, trimmed-mean, sparse-vector-technique, post-processing-theorem, zero-concentrated-differential-privacy, exponential-mechanism]
sources:
  - paper: doi:10.1007/978-3-319-57048-8_7
    title: "Salil Vadhan, The complexity of differential privacy, in Tutorials on the Foundations of Cryptography, Springer, 2017, pages 347 to 450"
    locator: "Section 3: Proposition 3.2 (propose-test-release, (2 epsilon, delta)-DP) and Proposition 3.3 (releasing stable values)"
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), 2014"
    locator: "Section 7: Algorithm 12 (Scale, the interquartile range) with Theorem 7.1 ((4 epsilon, delta)-DP), and Algorithm 13 (A_dist, release based on the distance to instability)"
  - paper: "Cynthia Dwork and Jing Lei, Differential privacy and robust statistics, STOC 2009"
    locator: the propose-test-release framework and its use for scale, location and regression
  - paper: "Ilya Mironov, On significance of the least significant bits for differential privacy, ACM CCS 2012"
    locator: the attack on floating-point noise and the snapping defense
---

Propose-test-release (PTR) is a way to add noise for the typical case and not the worst case. The analyst proposes a bound $b$ on the local sensitivity of a function $f$. The mechanism computes how many records of $x$ must change before the local sensitivity is above $b$, adds Laplace noise to that distance, and compares it with $\ln(1/\delta)/\varepsilon$. If the noisy distance is too small it outputs $\bot$, "no answer". Otherwise it releases $f(x) + \mathrm{Lap}(b/\varepsilon)$. The result is $(2\varepsilon, \delta)$-differentially private for every $f$ and $b$. For the [median](/median/) of dense data the noise is far smaller than the [global sensitivity](/global-sensitivity/) requires.

## In plain words

You want to publish the middle value of a list and you guess that one change can move it by at most $b$. The guess may be wrong for this list, or for a list close to it.

So first count how many values you must change to make the guess wrong. If that count is large, the guess is safe here and also for all lists close to this one. Add noise to the count and compare it with a safety margin. If the noisy count is too small, say nothing. If it is large, publish the middle value with noise for the guess $b$. The noise on the count hides each value, and the margin makes a wrong answer very unlikely.

## The problem

A dataset is a list $x$ of $n$ values in $[0, \Lambda]$, with $n$ odd and $\Lambda$ public. Two datasets are neighbors if one value is replaced by another (replace), so $n$ is fixed, and $d(x, y)$ is the number of replacements from $x$ to $y$. The median is $f(x) = x_m$ with $m = (n+1)/2$, its local sensitivity is $LS(y) = \max_{d(y,y')=1} |f(y) - f(y')|$, and its global sensitivity is $\Lambda$. The distance to instability is $\gamma(x) = \min\{d(x, y) : LS(y) > b\}$. The goal is an $(\varepsilon, \delta)$-DP estimate of $x_m$, or $\bot$.

Notation: $\mathrm{Lap}(b)$ has the density $(1/(2b))e^{-|z|/b}$, the variance $2b^2$ and $P(|Z| > t) = e^{-t/b}$.

## The algorithm

This is the form of Vadhan (2017, Proposition 3.2), with the median as $f$. Sort $x$ and set $x_i = 0$ for $i \le 0$ and $x_i = \Lambda$ for $i > n$.

```pseudo id=main
PTR-MEDIAN(x₁ ≤ ... ≤ xₙ, Λ, b, ε, δ)
L1  γ ← min{k ≥ 0 : max_{0≤t≤k+1} (x_{m+t} − x_{m+t−k−1}) > b}    ▷ ∞ if no k works
L2  γ̂ ← γ + Lap(1/ε)                                     ▷ γ has sensitivity 1
L3  if γ̂ ≤ ln(1/δ)/ε then output ⊥ and halt
L4  output x_m + Lap(b/ε)
```

Line L1 is the distance to instability. The inner maximum is the largest local sensitivity of the median within $k$ replacements, from the closed form of Nissim, Raskhodnikova and Smith (2007, Proposition 3.4). It grows with $k$, so the first $k$ above $b$ is the distance. Line L2 is the [Laplace mechanism](/laplace-mechanism/) on $\gamma$. Line L3 is the test. Line L4 is the release with the proposed bound.

## Example

Take $n = 101$ values $0, 1, \dots, 100$, with $\Lambda = 100$, $\varepsilon = 1$ and $\delta = 10^{-6}$, so the threshold in line L3 is $\ln 10^6 \approx 13.8$. Each gap is 1, so $k$ changes move the median by at most $k + 1$, and $\gamma = b$ for whole numbers $b$. From the code:

| $b$ | $\gamma$ | P(the test passes) | noise in line L4 | median absolute error |
|---|---|---|---|---|
| 5 | 5 | 0.00007 | Lap(5) | 3.5 |
| 10 | 10 | 0.011 | Lap(10) | 6.9 |
| 15 | 15 | 0.847 | Lap(15) | 10.4 |
| 20 | 20 | 0.999 | Lap(20) | 13.9 |
| 30 | 30 | 1.000 | Lap(30) | 20.8 |

A small $b$ gives small noise but the test fails, and a large $b$ always passes but adds more noise. With $b = 20$ the release is $(2, 10^{-6})$-DP with the median absolute error 13.9. The Laplace mechanism with the global sensitivity 100 at $\varepsilon = 2$ needs $\mathrm{Lap}(50)$, with the median absolute error 34.7. These values are exact for the noise laws (a theorem), not a measurement.

## Correctness

**Line L1 is the distance (a theorem).** By NRS Proposition 3.4, the inner maximum is $\max_{d(x,y) \le k} LS(y)$, so the least $k$ with a value above $b$ is $\gamma(x)$. The test file checks line L1 against a breadth-first search over all small datasets.

**$\gamma$ has sensitivity 1 (a theorem).** $d$ is a metric, so $|\gamma(x) - \gamma(x')| \le 1$ for neighbors.

**Privacy (Vadhan Proposition 3.2, a theorem).** The test of lines L2 and L3 is $\varepsilon$-DP. If $\gamma(x) \ge 1$, then $LS(x) \le b$, so line L4 is $\varepsilon$-DP for this pair, and the total is $2\varepsilon$. If $\gamma(x) = 0$, the test passes with probability $P(\mathrm{Lap}(1/\varepsilon) > \ln(1/\delta)/\varepsilon) = \delta/2$. So the output is $(2\varepsilon, \delta/2)$-DP. Vadhan states $\delta$; the same proof gives $\delta/2$.

**Utility (a theorem).** If $\gamma(x) \ge \ln(1/\delta)/\varepsilon + t/\varepsilon$, the test passes with probability at least $1 - \frac{1}{2}e^{-t}$.

The full proofs are in proofs/correctness.md.

## Complexity

In the [real-RAM model](/real-ram/), sorting takes $O(n \log n)$. Line L1 tries $k = 0, 1, \dots, \gamma$ and each try scans $k + 2$ terms, so it takes $O(\min(\gamma, n)^2)$. Lines L2 to L4 take $O(1)$. The total is $O(n^2)$ time in the worst case and $O(n)$ extra space. For a general $f$, line L1 can be hard to compute, and this is the main limit of PTR.

## Properties

- **Any function.** The privacy proof uses only the sensitivity 1 of $\gamma$ and the bound $LS(x) \le b$ when $\gamma(x) \ge 1$. It works for every $f$ and $b$.
- **Approximate DP only.** The output is $(2\varepsilon, \delta)$-DP and not pure DP, because a dataset with $\gamma = 0$ still passes with probability $\delta/2$. Bun and Steinke note that it is also not zero-concentrated DP.
- **A private "no".** The output $\bot$ is itself private: it tells only that the data is close to an unstable dataset.
- **Data-dependent error.** When the test passes, the error is that of $\mathrm{Lap}(b/\varepsilon)$, set by the proposal and not by $\Lambda$.

## Variants and improvements

- **Release of stable values.** If $f$ is constant on all datasets within distance $\gamma$, line L4 can output $f(x)$ with no noise (Vadhan Proposition 3.3; Dwork and Roth Algorithm 13). This gives a private mode and the stability-based histogram.
- **Scale first.** Dwork and Lei, and Dwork and Roth Algorithm 12, first estimate the interquartile range with PTR on a log scale, and then use it as the proposal $b$ for the median. Dwork and Roth Theorem 7.1 gives $(4\varepsilon, \delta)$-DP for the scale step.
- **Many proposals.** Try $b = 1, 2, 4, \dots$ and stop at the first pass. With the [sparse vector technique](/sparse-vector-technique/) the cost of the failed tests is small.
- **Smooth sensitivity.** [Smooth sensitivity](/smooth-sensitivity/) scales the noise to the local sensitivity near $x$ without a test, and it can give pure DP with heavy-tailed noise.

## When to use it

Use PTR when a statistic has a large global sensitivity but is stable on typical data, and when a "no answer" output is acceptable: a median, a quantile, a mode, or a robust regression estimate on a large sample. Use the [Laplace mechanism](/laplace-mechanism/) when the global sensitivity is small. Use [subsample and aggregate](/subsample-and-aggregate/) when the distance to instability is hard to compute.

## Pitfalls

- **Release without the test.** Skipping line L3, or releasing $\gamma$ itself, breaks privacy. The proposal $b$ alone is not a bound on the local sensitivity of every dataset.
- **No noise in line L2.** A test on the exact $\gamma$ leaks whether $\gamma$ is above the threshold, which can single out one record. The noise $\mathrm{Lap}(1/\varepsilon)$ is required.
- **A data-dependent proposal.** The bound $b$ must not depend on $x$, unless it comes from a private step whose cost is counted, as in the scale step of Dwork and Lei. A $b$ read from the data makes line L4 leak.
- **The wrong distance.** Line L1 must be the distance to the nearest dataset with $LS > b$, not $LS(x)$ itself. A dataset with $LS(x) \le b$ can have a neighbor with a large $LS$.
- **The privacy cost.** The total is $2\varepsilon$, not $\varepsilon$. Count both lines L2 and L4 in the budget.
- **Float noise.** The code uses `random.Random` and float noise, for tests only. A deployment needs a cryptographic source of randomness and exact sampling (Mironov 2012; Canonne, Kamath and Steinke 2020).

## Implementations

## History

Nissim, Raskhodnikova and Smith (STOC 2007) showed that noise scaled to the local sensitivity is not safe and gave smooth sensitivity. Dwork and Lei (STOC 2009) gave propose-test-release and used it to make robust estimators of scale, location and regression private. Dwork and Roth (2014) and Vadhan (2017) gave the general form used here, and Vadhan used the stable-value form for private histograms over large universes.

## References
