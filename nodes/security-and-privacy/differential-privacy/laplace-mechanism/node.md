---
tag: ZJZCN9
kind: algorithm
slug: laplace-mechanism
name: Laplace mechanism
aliases:
- Laplace noise mechanism
area: security-and-privacy/differential-privacy
level: intro
summary: Adds Laplace noise with scale equal to the l1 sensitivity over epsilon to a numeric query, which gives epsilon-differential privacy.
model: real-ram
complexity:
  vars: {k: the number of coordinates of the query}
  time: {worst: O(k)}
  space: {extra: O(k)}
properties: {deterministic: false, randomized: true}
history:
  year: 2006
  people: [Cynthia Dwork, Frank McSherry, Kobbi Nissim, Adam Smith]
  note: Dwork, McSherry, Nissim and Smith defined the sensitivity of a query and the Laplace mechanism at TCC 2006.
prereqs: [differential-privacy-definition, global-sensitivity]
see_also: [geometric-mechanism, gaussian-mechanism, discrete-gaussian-mechanism, report-noisy-max, sequential-composition-theorem, smooth-sensitivity, inverse-transform-sampling, output-perturbation]
sources:
  - paper: doi:10.1007/11681878_14
    title: "Cynthia Dwork, Frank McSherry, Kobbi Nissim and Adam Smith, Calibrating noise to sensitivity in private data analysis, TCC 2006, LNCS 3876, pages 265 to 284"
    locator: the definition of sensitivity and the mechanism that adds Laplace noise scaled to it
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), 2014, pages 211 to 407"
    locator: "Section 3.3, Definition 3.1 (l1 sensitivity), Definition 3.2 (the Laplace distribution), Definition 3.3 (the Laplace mechanism), Theorem 3.6 (privacy), Fact 3.7 (the tail) and Theorem 3.8 (accuracy)"
  - paper: "Ilya Mironov, On significance of the least significant bits for differential privacy, ACM CCS 2012, pages 650 to 661"
    locator: why floating-point Laplace noise is not private, and the snapping mechanism
  - paper: "Clement L. Canonne, Gautam Kamath and Thomas Steinke, The discrete Gaussian for differential privacy, NeurIPS 2020"
    locator: exact samplers for discrete Laplace and discrete Gaussian noise
---

The Laplace mechanism answers a numeric query about a private dataset with noise from the Laplace distribution added to each coordinate. The scale of the noise is the [global sensitivity](/global-sensitivity/) $\Delta_1 f$ divided by $\varepsilon$, and then the output is $\varepsilon$-[differentially private](/differential-privacy-definition/). The error of each coordinate is about $\Delta_1 f / \varepsilon$ and does not grow with the size of the dataset. It is the first mechanism of differential privacy, and the [geometric mechanism](/geometric-mechanism/) and the [Gaussian mechanism](/gaussian-mechanism/) are its discrete and its $\ell_2$ versions.

## In plain words

You want to publish a count, such as the number of people in a table who have a disease. One person can change that count by at most one. So you add random noise that is often of size about one, and sometimes larger. Then the published number looks almost the same whether or not a given person is in the table.

The noise comes from a fixed bell-like shape with a sharp peak at zero and two tails that fall at a steady rate. A smaller privacy budget gives wider noise. A query that one person can change more also gets wider noise. The noise does not depend on how many people are in the table, so a large table gives an accurate answer.

## The problem

The input is a dataset $x = (x_1, \ldots, x_n)$ of records from a universe $\mathcal X$, a query $f$ that maps datasets to $\mathbb R^k$, a number $\Delta \ge \Delta_1 f$, and a privacy parameter $\varepsilon > 0$. Here

$$\Delta_1 f = \max_{x \sim x'} \lVert f(x) - f(x') \rVert_1,$$

where $x \sim x'$ means that $x$ and $x'$ are neighbors. The page uses add/remove neighbors unless it says otherwise: $x'$ is $x$ with one record added or removed. Under replace neighbors, where one record changes and $n$ stays fixed, the same query can have a larger sensitivity. A histogram has $\Delta_1 = 1$ under add/remove and $\Delta_1 = 2$ under replace.

The output is a random vector $y \in \mathbb R^k$. The map from $x$ to the distribution of $y$ must be $\varepsilon$-differentially private, and $y$ must be close to $f(x)$.

The **Laplace distribution** $\mathrm{Lap}(b)$ with scale $b > 0$ has the density and the distribution function

$$p_b(z) = \frac{1}{2b} e^{-|z|/b}, \qquad F_b(z) = \begin{cases} \tfrac12 e^{z/b} & z < 0, \\ 1 - \tfrac12 e^{-z/b} & z \ge 0. \end{cases}$$

Its mean is 0, its variance is $2b^2$, its mean absolute value is $b$, and $\Pr[|Z| > t] = e^{-t/b}$ for $t \ge 0$.

## The algorithm

```pseudo id=main
LAPLACE-MECHANISM(x, f, Delta, epsilon)      ▷ Delta >= the l1 sensitivity of f
L1  b <- Delta / epsilon
L2  v <- f(x)                                ▷ v = (v_1, ..., v_k)
L3  for i <- 1 to k do
L4      draw u uniform in (-1/2, 1/2)        ▷ draw again if u = -1/2
L5      z <- -b sgn(u) ln(1 - 2|u|)          ▷ the inverse of F_b at u + 1/2
L6      y_i <- v_i + z
L7  return y = (y_1, ..., y_k)
```

Line L1 sets the scale. Line L2 computes the true answer, and this is the only line that reads the data. Lines L4 and L5 draw one sample of $\mathrm{Lap}(b)$ by [inverse transform sampling](/inverse-transform-sampling/): if $u$ is uniform, then $F_b^{-1}(u + 1/2)$ has the distribution function $F_b$. Line L6 adds an independent sample to each coordinate. The output of line L7 is the only thing that is published. The noise of line L4 is never published, and it is never used again.

The code on this site uses floats and a seeded pseudorandom generator, so that the tests can repeat each run. A deployment needs a cryptographic source of randomness and an exact sampler, because float noise leaks through its low-order bits (Mironov 2012; Canonne, Kamath and Steinke 2020). The [discrete Gaussian mechanism](/discrete-gaussian-mechanism/) page shows the exact samplers.

## Example

The universe is $\{0, 1, 2\}$ and the dataset is $x = (0, 0, 1, 2, 2, 2)$, with $n = 6$. The query is the [histogram](/histogram/) $f(x) = (2, 1, 3)$, with $\Delta_1 f = 1$ under add/remove neighbors. With $\varepsilon = 1$, line L1 gives $b = 1$. Assume that line L4 draws $u = 0.3$, $u = -0.1$ and $u = 0.45$.

| step | $i$ | $v_i$ | $u$ | $z$ (line L5) | $y_i$ (line L6) |
|---|---|---|---|---|---|
| L1, L2 | | | | | $b = 1$, $v = (2, 1, 3)$ |
| L3 to L6 | 1 | 2 | 0.3 | $-\ln 0.4 = 0.916291$ | 2.916291 |
| L3 to L6 | 2 | 1 | $-0.1$ | $\ln 0.8 = -0.223144$ | 0.776856 |
| L3 to L6 | 3 | 3 | 0.45 | $-\ln 0.1 = 2.302585$ | 5.302585 |
| L7 | | | | | $y = (2.916291, 0.776856, 5.302585)$ |

The accuracy theorem below says that, with probability at least $1 - \beta = 0.9$, each of the $k = 3$ errors is at most $b \ln(k / \beta) = \ln 30 = 3.401197$. Here the largest error is 2.302585.

A second check: with $\Delta = 1$ and $\varepsilon = 0.5$, the scale is $b = 2$, the variance of the noise is 8, and $\Pr[|Z| > 2 \ln 10] = \Pr[|Z| > 4.6052] = 0.1$.

## Correctness

**Theorem (Dwork, McSherry, Nissim and Smith 2006; Dwork-Roth Theorem 3.6).** If $\Delta \ge \Delta_1 f$ under a neighbor relation, then LAPLACE-MECHANISM is $\varepsilon$-differentially private under that relation.

The key step is a bound on the ratio of the output densities. For neighbors $x \sim x'$ and every output $y$, the triangle inequality $|a| - |a'| \le |a - a'|$ gives

$$\frac{p_{x}(y)}{p_{x'}(y)} = \prod_{i=1}^{k} \exp\!\Big(\frac{|y_i - f(x')_i| - |y_i - f(x)_i|}{b}\Big) \le \exp\!\Big(\frac{\lVert f(x) - f(x') \rVert_1}{b}\Big) \le e^{\varepsilon}.$$

The integral of this bound over a set $S$ of outputs gives the definition. The full proof, with the proof that lines L4 and L5 sample $\mathrm{Lap}(b)$ and the proof of the accuracy bound, is in the correctness proof of this page.

**Theorem (accuracy, Dwork-Roth Theorem 3.8).** For $0 < \beta < 1$, with probability at least $1 - \beta$, $\max_i |y_i - f(x)_i| \le (\Delta / \varepsilon) \ln(k / \beta)$. The proof is a [union bound](/union-bound/) over the $k$ tails $\Pr[|Z_i| > t] = e^{-t/b}$.

## Complexity

The model is the [real RAM](/real-ram/): a uniform real number in $(-1/2, 1/2)$, a logarithm and an addition each cost one step. The cost is counted per query, after the one evaluation of $f$ in line L2.

- **Time.** The loop of line L3 runs $k$ times. Each pass draws one uniform number and does $O(1)$ arithmetic. The event $u = -1/2$ of line L4 has probability 0 in this model. So the time is $O(k)$ in the worst case.
- **Space.** The output $y$ has $k$ numbers, and the loop keeps $O(1)$ other numbers. So the extra space is $O(k)$.

On real machines with 53-bit floats, line L4 draws again with probability $2^{-53}$, so the expected number of draws is still $k (1 + O(2^{-53}))$.

## Properties

- **Pure privacy.** The output is $(\varepsilon, 0)$-DP. The bound is tight: when $f(x) - f(x')$ has one nonzero coordinate equal to $\Delta$, the ratio of the densities is exactly $e^{\varepsilon}$ on a half-line of outputs. The tests check this on a grid (a measurement on the test data: the largest log ratio is 0.5 for $\varepsilon = 0.5$).
- **Unbiased.** $\mathbb E[y] = f(x)$, and each coordinate has variance $2 (\Delta / \varepsilon)^2$ and mean absolute error $\Delta / \varepsilon$.
- **No dependence on $n$.** The error is the same for 10 records and for $10^9$ records. The relative error of a count of size $c$ is about $1 / (\varepsilon c)$.
- **Closed under post-processing.** Rounding, clamping or any other map of $y$ that does not read $x$ keeps $\varepsilon$-DP, by the [post-processing theorem](/post-processing-theorem/).
- **Composition.** Two runs on the same data with $\varepsilon_1$ and $\varepsilon_2$ are $(\varepsilon_1 + \varepsilon_2)$-DP together, by the [sequential composition theorem](/sequential-composition-theorem/).

## Variants and improvements

- **Integer outputs.** The [geometric mechanism](/geometric-mechanism/) adds the discrete analog of Laplace noise to an integer query. It needs no floats.
- **The $\ell_2$ version.** The [Gaussian mechanism](/gaussian-mechanism/) calibrates to $\Delta_2 f$ and gives $(\varepsilon, \delta)$-DP. For $k$ counts that one record can all change by one, $\Delta_1 = k$ and $\Delta_2 = \sqrt k$, so the Gaussian error is much smaller for large $k$.
- **Snapping.** Mironov (2012) rounds and clamps the float output so that the low-order bits no longer depend on the data. This gives a slightly larger $\varepsilon$, which his paper bounds.
- **Data-dependent noise.** [Smooth sensitivity](/smooth-sensitivity/) and [propose-test-release](/propose-test-release/) add less noise when the dataset is far from the worst case, such as for a median.
- **Selection.** To publish only the index of the largest of $m$ counts, [report noisy max](/report-noisy-max/) adds Laplace noise and releases only the index.
- **Release of a model.** [Output perturbation](/output-perturbation/) adds Laplace or Gaussian noise to the parameters of a trained model, with the sensitivity of the training map.

## When to use it

Use the Laplace mechanism for a small number of numeric queries with a low $\ell_1$ sensitivity, when you need pure $\varepsilon$-DP: counts, histograms, and sums or means of values that are clipped to a known range. If the answer is an integer and you want integer output with exact sampling, use the geometric mechanism. If you answer many queries, or the $\ell_2$ sensitivity is much smaller than the $\ell_1$ sensitivity, and a small $\delta$ is acceptable, the Gaussian mechanism adds less noise. If you need the best item of a set and not a number, use the [exponential mechanism](/exponential-mechanism/) or report noisy max.

## Pitfalls

- **The sensitivity of the wrong neighbor relation.** A histogram has $\Delta_1 = 1$ under add/remove and 2 under replace. Line L1 with $b = 1/\varepsilon$ is only $2\varepsilon$-DP under replace. The tests measure a log ratio of 1.0 for $\varepsilon = 0.5$ there. Under replace, line L1 must use $\Delta = 2$, and then $b = 2/\varepsilon$.
- **The scale of one coordinate.** For $k$ queries that one record can each change by 1, line L1 with $\Delta = 1$ gives only $k\varepsilon$-DP. Line L1 must use the $\ell_1$ sensitivity of the whole vector, $\Delta = k$.
- **Local sensitivity.** Line L1 with the change of $f$ at the actual $x$, in place of the maximum over all neighbor pairs, is not private, because the scale itself then depends on the data. Use the global $\Delta_1 f$, or the methods of [smooth sensitivity](/smooth-sensitivity/).
- **Float noise.** Lines L4 and L5 on floats with a non-cryptographic generator are fine for study, but not for a release (Mironov 2012). Use an exact sampler from a cryptographic source, or the snapping mechanism.
- **Fresh noise for a repeated query.** Each call of the mechanism draws fresh noise in line L4 and costs $\varepsilon$ again. The average of $r$ answers to one query has $r$ times the cost. Store and reuse a published answer.

## Implementations

## History

Dwork, McSherry, Nissim and Smith (TCC 2006) defined the sensitivity of a query and proved that Laplace noise scaled to it gives what is now called $\varepsilon$-differential privacy. The same paper gives the privacy definition in its first form. Dwork and Roth (2014) give the mechanism in the form of this page, with the accuracy bound for $k$ coordinates. Mironov (2012) showed that the textbook float implementation is not private, and Canonne, Kamath and Steinke (2020) gave exact samplers for the discrete versions.

## References
