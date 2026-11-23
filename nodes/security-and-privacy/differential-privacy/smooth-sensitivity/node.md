---
tag: 0ZFFMP
kind: algorithm
slug: smooth-sensitivity
name: Smooth sensitivity framework
aliases:
- Nissim-Raskhodnikova-Smith smooth sensitivity
area: security-and-privacy/differential-privacy
level: advanced
summary: Adds noise scaled to a smooth upper bound on the local sensitivity at the actual dataset. For the median this is often far less noise than the global sensitivity needs.
model: real-ram
complexity:
  vars: {n: the number of values}
  time: {worst: O(n^2)}
  space: {extra: O(n)}
history:
  year: 2007
  people: [Kobbi Nissim, Sofya Raskhodnikova, Adam Smith]
  note: Nissim, Raskhodnikova and Smith gave the framework at STOC 2007, with the median, the minimum spanning tree cost and subsample and aggregate as examples.
prereqs: [differential-privacy-definition, global-sensitivity, laplace-mechanism, approximate-differential-privacy]
see_also: [propose-test-release, subsample-and-aggregate, median, laplace-mechanism, exponential-mechanism, output-perturbation, trimmed-mean, inverse-transform-sampling]
sources:
  - paper: "Kobbi Nissim, Sofya Raskhodnikova and Adam Smith, Smooth sensitivity and sampling in private data analysis, STOC 2007"
    locator: "Definition 2.1 (a smooth upper bound), Definition 2.2 (smooth sensitivity), Lemma 2.3 and Corollary 2.4 (Cauchy noise for epsilon-DP, Laplace noise for (epsilon, delta)-DP), Proposition 3.4 (the median)"
  - paper: "Ilya Mironov, On significance of the least significant bits for differential privacy, ACM CCS 2012"
    locator: the attack on floating-point noise and the snapping defense
  - paper: arxiv:2004.00010
    title: "Clement Canonne, Gautam Kamath and Thomas Steinke, The discrete Gaussian for differential privacy, NeurIPS 2020"
    locator: exact sampling of discrete noise
---

The smooth sensitivity framework adds noise that fits the actual dataset and not the worst case. The [global sensitivity](/global-sensitivity/) of the [median](/median/) of values in $[0, \Lambda]$ is $\Lambda$, so the [Laplace mechanism](/laplace-mechanism/) must add noise of scale $\Lambda/\varepsilon$, even when the data is dense near the median. The local sensitivity at $x$ is often tiny, but noise scaled to it leaks the data, because the scale itself then tells about $x$. Nissim, Raskhodnikova and Smith fix this with the $\beta$-smooth sensitivity $S^*(x) = \max_y e^{-\beta d(x,y)} LS(y)$: the largest local sensitivity near $x$, with a discount that falls with the distance. Noise of scale $S^*(x)/\varepsilon$ from a suitable law is then private.

## In plain words

You want to release the middle value of a list of numbers, and you must hide each number. The safe rule for any list adds noise as large as the whole range, because for some lists one change moves the middle value from one end to the other.

For most lists, one change moves the middle value only a little. But a list that is close to a risky list could still be a risk, so the method looks at the lists that are a few changes away. It takes the largest movement among them, made smaller the farther away the list is. This number changes only slowly from one list to the next. Noise of that size, from a law with heavy tails, hides each number.

## The problem

A dataset is a list $x$ of $n$ values in $[0, \Lambda]$, with $n$ odd and $\Lambda$ public. Two datasets are neighbors if one value is replaced by another (replace), so $n$ is fixed. The distance $d(x, y)$ is the number of replacements from $x$ to $y$. The median is $f(x) = x_m$ with $m = (n+1)/2$ in sorted order. The local sensitivity is $LS(y) = \max_{d(y,y')=1} |f(y) - f(y')|$, and the global sensitivity is $\max_y LS(y) = \Lambda$. The goal is an $\varepsilon$-DP estimate of $x_m$ whose error follows the local shape of $x$.

Notation: $\mathrm{Lap}(b)$ has the density $(1/(2b))e^{-|z|/b}$, the variance $2b^2$ and $P(|Z| > t) = e^{-t/b}$. The standard Cauchy law has the density $1/(\pi(1+z^2))$ and $P(|Z| \le 1) = 1/2$.

## The algorithm

Sort $x$, and set $x_i = 0$ for $i \le 0$ and $x_i = \Lambda$ for $i > n$. Lines L1 to L3 are the closed form of NRS Proposition 3.4, and line L4 is the Cauchy release of NRS Corollary 2.4 with $\gamma = 2$.

```pseudo id=main
SMOOTH-MEDIAN(x₁ ≤ ... ≤ xₙ, Λ, ε)
L1  for k ← 0 to n do                                 ▷ β = ε/6 and S = 0 at the start
L2      A_k ← max_{0 ≤ t ≤ k+1} (x_{m+t} − x_{m+t−k−1})    ▷ the largest local sensitivity within k changes
L3      S ← max(S, e^{−kβ} · A_k)                        ▷ the discount for the distance
L4  output x_m + (6S/ε) · Z, with Z standard Cauchy
```

Line L2 is $A(k, x) = \max_{d(x,y) \le k} LS(y)$. To move the median by a lot with $k$ changes, take a run of $k+1$ consecutive gaps that contains the median and move the $k$ values inside it out of it. The padding with 0 and $\Lambda$ covers runs that reach an end of the range. Line L3 takes the maximum over $k$ of the discounted value, which is $S^*(x)$. For $k \ge n$ the value $A_k$ is $\Lambda$, so the loop can stop at $n$. Line L4 adds noise of scale $6S^*/\varepsilon$. For $(\varepsilon, \delta)$-DP, use $\beta = \varepsilon/(2\ln(2/\delta))$ and the noise $(2S^*/\varepsilon) \cdot \mathrm{Lap}(1)$ in line L4.

## Example

Take $n = 101$ values $0, 1, 2, \dots, 100$, with $\Lambda = 100$ and $\varepsilon = 1$, so $\beta = 1/6$ and the median is 50. Each gap is 1, so $A_k = k + 1$ until a run reaches an end. From the code:

| $k$ | $A_k$ | $e^{-k/6} A_k$ |
|---|---|---|
| 0 | 1 | 1.000 |
| 1 | 2 | 1.693 |
| 2 | 3 | 2.150 |
| 3 | 4 | 2.426 |
| 4 | 5 | 2.567 |
| 5 | 6 | 2.608 |
| 6 | 7 | 2.575 |
| 8 | 9 | 2.372 |
| 50 | 51 | 0.012 |

So $S^* = 6e^{-5/6} \approx 2.61$, and line L4 adds Cauchy noise of scale 15.6. The median absolute error of Cauchy noise is its scale, 15.6. The Laplace mechanism with the global sensitivity 100 needs $\mathrm{Lap}(100)$, with the median absolute error $100 \ln 2 \approx 69.3$. The $(\varepsilon, \delta)$ form with $\delta = 10^{-6}$ has $\beta \approx 0.0345$, $S^* \approx 11.05$ and $\mathrm{Lap}(22.1)$ noise, with the median absolute error 15.3 and light tails. These are exact values of the noise laws (a theorem), not a measurement.

## Correctness

**The closed form (NRS Proposition 3.4, a theorem).** Lines L1 to L3 compute $S^*(x)$. One change moves the median by at most one position, so $LS(y) = \max(y_m - y_{m-1}, y_{m+1} - y_m)$. Within $k$ changes the widest gap that can sit at the median spans $k+1$ consecutive gaps of $x$, which is line L2. The test file checks lines L1 to L3 against the definition by brute force on every dataset of the grid $\{0, \dots, \Lambda\}^n$ for $n \le 5$ and $\Lambda \le 4$.

**A smooth bound (a theorem).** $S^*(x) \ge LS(x)$, and $S^*(x) \le e^{\beta} S^*(x')$ for neighbors, by the triangle inequality for $d$.

**Privacy (NRS Lemma 2.3 and Corollary 2.4, a theorem).** Between neighbors the center moves by at most $LS(x) \le S^*(x)$, which is $\varepsilon/6$ in units of the scale, and the scale changes by a factor at most $e^{\varepsilon/6}$. The Cauchy log density has slope at most 1, and a change of scale by $e^{\lambda}$ changes it by at most $3|\lambda|$. So the log density ratio is at most $\varepsilon/6 + \varepsilon/2 < \varepsilon$ at every output. Laplace noise does not have this property for a change of scale at large $|z|$, which is why it gives only $(\varepsilon, \delta)$-DP.

The proofs are in proofs/correctness.md. The Laplace case there is a sketch with the locator in NRS.

## Complexity

In the [real-RAM model](/real-ram/), sorting takes $O(n \log n)$, and lines L1 to L3 as written take $O(n^2)$ time, because line L2 scans $k + 2$ terms. The extra space is $O(n)$ for the sorted copy. NRS give an $O(n \log n)$ algorithm for the median. Line L4 takes $O(1)$.

## Properties

- **Instance-based noise.** The noise follows the gaps of $x$ near the median, not the worst case over all datasets.
- **Pure DP with heavy tails.** The Cauchy form is $\varepsilon$-DP, but its noise has no mean. A single release can be far off with a small probability.
- **Approximate DP with light tails.** The Laplace form has exponential tails and is $(\varepsilon, \delta)$-DP.
- **A general framework.** Any function with a computable smooth bound on its local sensitivity can use line L4. Computing $S^*$ exactly is hard for some functions, and any smooth upper bound on $LS$ is also enough (NRS Definition 2.1).

## Variants and improvements

- **Other noise laws.** NRS give a general condition for "admissible" noise. Bun and Steinke (NeurIPS 2019) give laws with lighter tails for pure DP and for concentrated DP.
- **Subsample and aggregate.** When no smooth bound is easy to compute, split the data, run the function on each part, and combine with a private median. See [subsample and aggregate](/subsample-and-aggregate/).
- **Propose-test-release.** Test privately that the dataset is far from any dataset with large local sensitivity, and only then add small noise. See [propose-test-release](/propose-test-release/).
- **Other statistics.** The same scheme works for the [trimmed mean](/trimmed-mean/) and for other order statistics, with a different formula in line L2.

## When to use it

Use smooth sensitivity for a statistic whose global sensitivity is huge but whose local sensitivity is small on typical data, such as a median or a quantile of a large, dense sample. Use the [Laplace mechanism](/laplace-mechanism/) when the global sensitivity is already small, such as for counts. Use the [exponential mechanism](/exponential-mechanism/) over a grid of candidates for a quantile when a discrete output is fine.

## Pitfalls

- **Noise scaled to the local sensitivity.** Replacing $S$ in line L4 by $LS(x) = A_0$ is not private, because the scale depends on the data. A dataset with $LS = 0$ releases its median with no noise, and a neighbor with large $LS$ does not.
- **Too large a $\beta$.** Line L1 needs $\beta \le \varepsilon/6$ for the Cauchy form and $\beta \le \varepsilon/(2\ln(2/\delta))$ for the Laplace form. A larger $\beta$ gives a smaller $S$ but breaks the proof.
- **Laplace noise with the pure DP claim.** Line L4 with Laplace noise and $\beta = \varepsilon/6$ is not $\varepsilon$-DP. Laplace noise needs $\delta > 0$.
- **The padding.** Line L2 must use $x_i = 0$ below the data and $x_i = \Lambda$ above it. Without the padding, $S$ ignores the datasets whose median moves to an end of the range, and the bound is not smooth.
- **Float noise.** The code uses `random.Random` and float noise, for tests only. A deployment needs a cryptographic source of randomness and exact sampling (Mironov 2012; Canonne, Kamath and Steinke 2020).

## Implementations

## History

Dwork, McSherry, Nissim and Smith (2006) calibrated noise to the global sensitivity. Nissim, Raskhodnikova and Smith (STOC 2007) showed that the local sensitivity alone is not safe, and gave smooth sensitivity, its closed form for the median, its use for the cost of a minimum spanning tree, and the subsample and aggregate framework. Dwork and Lei (2009) gave the related propose-test-release framework. Bun and Steinke (2019) gave better noise laws for the framework.

## References
