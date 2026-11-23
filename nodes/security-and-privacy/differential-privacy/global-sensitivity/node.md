---
tag: RRCN85
kind: definition
slug: global-sensitivity
name: Global sensitivity
aliases:
- l1 sensitivity
- query sensitivity
area: security-and-privacy/differential-privacy
level: intro
summary: "The largest change in a function's value, in a given norm, over all pairs of datasets that differ in one record."
prereqs: [differential-privacy-definition]
see_also: [laplace-mechanism, gaussian-mechanism, exponential-mechanism, smooth-sensitivity, propose-test-release, matrix-mechanism, histogram, median]
sources:
  - paper: doi:10.1007/11681878_14
    title: "Cynthia Dwork, Frank McSherry, Kobbi Nissim and Adam Smith, Calibrating noise to sensitivity in private data analysis, TCC 2006, LNCS 3876, pages 265 to 284"
    locator: the definition of the sensitivity of a function and its use to set the scale of the noise
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), 2014, pages 211 to 407"
    locator: "Section 3.3, Definition 3.1 (sensitivity in the l1 norm); Section 3.4, the sensitivity of a utility function; Section 3.5.3, Definition 3.8 (sensitivity in the l2 norm)"
  - paper: doi:10.1145/1250790.1250803
    title: "Kobbi Nissim, Sofya Raskhodnikova and Adam Smith, Smooth sensitivity and sampling in private data analysis, STOC 2007, pages 75 to 84"
    locator: local sensitivity, why noise cannot be scaled to it, and smooth sensitivity
---

The global sensitivity of a function of a dataset is the largest change of its value, measured in a norm, between two datasets that differ in one record. It is the maximum over all pairs of neighbors, not only the pairs near the actual data. The basic mechanisms of [differential privacy](/differential-privacy-definition/) add noise in proportion to it: the [Laplace mechanism](/laplace-mechanism/) uses the sensitivity in the $\ell_1$ norm, and the [Gaussian mechanism](/gaussian-mechanism/) uses the sensitivity in the $\ell_2$ norm. Dwork, McSherry, Nissim and Smith (2006) defined it. The value depends on the neighbor relation, so it must always be stated with one.

## Definition

Datasets and the two neighbor relations, add/remove and replace, are as on the page of [differential privacy](/differential-privacy-definition/). Let $f$ map datasets to $\mathbb R^k$, and let $1 \le p \le \infty$.

**Definition.** The **global sensitivity** of $f$ in the $\ell_p$ norm, under a neighbor relation $\sim$, is

$$\Delta_p f = \max_{x \sim x'} \lVert f(x) - f(x') \rVert_p.$$

If the maximum does not exist, the supremum is used, and it can be $+\infty$. The two common cases are $\Delta_1 f = \max \sum_i |f(x)_i - f(x')_i|$ and $\Delta_2 f = \max \sqrt{\sum_i (f(x)_i - f(x')_i)^2}$. A mechanism only needs an upper bound $\Delta \ge \Delta_p f$; a larger bound gives more noise and the same privacy.

**Sensitivity of a utility.** For a utility $u(x, r)$ of each candidate $r$, as in the [exponential mechanism](/exponential-mechanism/), the sensitivity is $\Delta u = \max_r \max_{x \sim x'} |u(x, r) - u(x', r)|$: one bound for all candidates at the same time.

**Local sensitivity.** The local sensitivity at a fixed dataset $x$ is $\mathrm{LS}_f(x) = \max_{x' \sim x} \lVert f(x) - f(x') \rVert$, a maximum over the neighbors of $x$ only. So $\Delta f = \max_x \mathrm{LS}_f(x)$. Noise scaled to $\mathrm{LS}_f(x)$ is not private, because the scale itself depends on $x$ and can reveal it (Nissim, Raskhodnikova and Smith 2007). [Smooth sensitivity](/smooth-sensitivity/) and [propose-test-release](/propose-test-release/) are safe ways to use it.

**Properties.** These follow from the definition and the triangle inequality.

1. **Norms.** For $f$ with $k$ coordinates, $\Delta_\infty f \le \Delta_2 f \le \Delta_1 f \le \sqrt{k}\,\Delta_2 f$, because $\lVert v \rVert_\infty \le \lVert v \rVert_2 \le \lVert v \rVert_1 \le \sqrt k \lVert v \rVert_2$ holds for every vector $v$ in $\mathbb R^k$.
2. **Concatenation.** For $h(x) = (f(x), g(x))$, $\Delta_1 h \le \Delta_1 f + \Delta_1 g$ and $\Delta_2 h \le \sqrt{(\Delta_2 f)^2 + (\Delta_2 g)^2}$.
3. **Lipschitz maps.** If $\lVert g(a) - g(b) \rVert \le c \lVert a - b \rVert$ for all $a, b$, then $\Delta(g \circ f) \le c\,\Delta f$ in those norms.
4. **Relations.** A replace step is at most a removal and an addition, so $\Delta f$ under replace is at most twice $\Delta f$ under add/remove. It can be smaller, as for a mean with a known $n$, or equal, as for a count.
5. **Linear queries.** For a histogram $h$ and $f(h) = A h$, adding or removing one record changes $h$ by one unit vector $e_j$, so $\Delta_p f$ under add/remove is the largest $\ell_p$ norm of a column of $A$. The [matrix mechanism](/matrix-mechanism/) is built on this fact.

## Examples and non-examples

**A count.** The number of records with a property changes by at most 1 when one record is added, removed or changed. So $\Delta_1 = \Delta_2 = 1$ under both relations.

**A histogram.** The [histogram](/histogram/) over $k$ bins has $\Delta_1 = 1$ and $\Delta_2 = 1$ under add/remove, because one bin changes by 1. Under replace one bin falls by 1 and another rises by 1, so $\Delta_1 = 2$ and $\Delta_2 = \sqrt 2 = 1.414214$.

**Counts that one record can all change.** If each record can add 1 to each of $k$ counts, as for $k$ overlapping predicates, then $\Delta_1 = k$ and $\Delta_2 = \sqrt k$. With $k = 100$, the Laplace mechanism with $\varepsilon = 1$ has scale 100 and standard deviation $141.42$ per count. The analytic Gaussian mechanism with $\varepsilon = 1$ and $\delta = 10^{-5}$ needs $\sigma = 3.730632 \times 10 = 37.31$, so the gap between the two norms decides which mechanism adds less noise.

**A sum of bounded values.** Clip each value to $[0, B]$. The sum changes by at most $B$ under both relations, so $\Delta_1 = B$. For the ages $x = (23, 35, 41, 58, 90)$ clipped to $[0, 100]$, the sum is 247 and $\Delta_1 = 100$.

**A mean.** Under replace with a public $n$, the mean of values in $[0, B]$ has $\Delta_1 = B/n$; for the ages above, $100/5 = 20$. Under add/remove, $n$ is not fixed, and a single dataset of size 1 shows that the change can be as large as $B/2$. The usual fix is to release a noisy sum and a noisy count and divide them, which is [post-processing](/post-processing-theorem/).

**Non-example: an unbounded sum.** If the values are not clipped, one record can change the sum by any amount, and $\Delta_1 = +\infty$. No finite Laplace noise makes the sum private. Clipping is part of the mechanism, and the bound $B$ must be chosen without looking at the data.

**Non-example: a small local sensitivity.** The [median](/median/) of the ages above is 41. Changing one age can move it only to a value from 35 to 58, so $\mathrm{LS}(x) = 17$ under replace. But for the dataset $(0, 0, 0, 100, 100)$, changing one 0 to 100 moves the median from 0 to 100, so the global sensitivity is the whole range, 100. Laplace noise of scale $17/\varepsilon$ would not be private; this is the case that smooth sensitivity and propose-test-release handle.

## Related definitions

- **The mechanisms.** The [Laplace mechanism](/laplace-mechanism/) adds $\mathrm{Lap}(\Delta_1 f/\varepsilon)$ to each coordinate. The [geometric mechanism](/geometric-mechanism/) is its integer form. The [Gaussian mechanism](/gaussian-mechanism/) calibrates $\sigma$ to $\Delta_2 f$. [Report noisy max](/report-noisy-max/) and the [exponential mechanism](/exponential-mechanism/) use the sensitivity of each score.
- **Data-dependent sensitivity.** Local sensitivity, [smooth sensitivity](/smooth-sensitivity/) and the test of [propose-test-release](/propose-test-release/) adapt the noise to the actual data while keeping privacy.
- **Sensitivity of a whole workload.** For many linear queries at once, the [matrix mechanism](/matrix-mechanism/) and [private query release](/private-query-release/) work with the sensitivity of a matrix, property 5 above, and not with the sensitivity of each query alone.

## References
