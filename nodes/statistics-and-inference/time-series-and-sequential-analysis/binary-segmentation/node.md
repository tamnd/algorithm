---
tag: PQ8R7K
kind: algorithm
slug: binary-segmentation
name: Binary segmentation
aliases:
- binary segmentation for change points
- wild binary segmentation
area: statistics-and-inference/time-series-and-sequential-analysis
level: core
summary: Cuts a series at its single best change point, then repeats on each part while the split statistic exceeds a threshold. Cost O(n(m+1)) for m changes, O(n²) in the worst case.
solves: [change-point-detection]
model: real-ram
complexity:
  vars: {n: "the length of the series", m: "the number of change points found"}
  time: {worst: Θ(n(m+1))}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: false, online: false, recursive: true}
history:
  year: 1974
  people: [A. J. Scott, M. Knott, L. Yu. Vostrikova]
  note: Scott and Knott used recursive binary splitting to group ordered means in 1974. Vostrikova gave the change-point form and its consistency in 1981. Fryzlewicz introduced wild binary segmentation in 2014.
prereqs: [change-point-detection]
see_also: [pelt-algorithm, cusum, segmented-least-squares, bayesian-online-changepoint-detection, divide-and-conquer-paradigm, prefix-sums, decision-tree, bayesian-information-criterion]
sources:
  - paper: doi:10.2307/2529204
    title: A. J. Scott and M. Knott, A cluster analysis method for grouping means in the analysis of variance, Biometrics 30(3) (1974)
    locator: the method of splitting ordered group means into two groups by the largest between-group sum of squares, applied again to each group
  - paper: doi:10.1214/14-AOS1245
    title: Piotr Fryzlewicz, Wild binary segmentation for multiple change-point detection, Annals of Statistics 42(6) (2014)
    locator: the CUSUM statistic, the description and consistency conditions of binary segmentation, the wild binary segmentation algorithm, and the threshold of the form C sqrt(2 log n)
  - paper: doi:10.1093/biostatistics/kxh008
    title: Adam B. Olshen, E. S. Venkatraman, Robert Lucito and Michael Wigler, Circular binary segmentation for the analysis of array-based DNA copy number data, Biostatistics 5(4) (2004)
    locator: the circular binary segmentation algorithm and its application to copy number data
  - paper: doi:10.1080/01621459.2012.737745
    title: R. Killick, P. Fearnhead and I. A. Eckley, Optimal detection of changepoints with a linear computational cost, Journal of the American Statistical Association 107(500) (2012)
    locator: the discussion of binary segmentation as an approximate search and its comparison with exact penalized segmentation
  - paper: doi:10.1016/j.sigpro.2019.107299
    title: Charles Truong, Laurent Oudre and Nicolas Vayatis, Selective review of offline change point detection methods, Signal Processing 167 (2020)
    locator: the section on search methods, including binary segmentation and its variants
---

Binary segmentation finds several changes in the mean of a series by repeated single splits. It looks at the whole series, finds the one split point that best separates it into two parts with different means, and keeps the split if a test statistic exceeds a threshold $\zeta$. Then it does the same on each part, and stops on a part when no split is strong enough. With prefix sums each split statistic costs $O(1)$, so a part of length $L$ costs $O(L)$ and the whole run costs $O(n(m+1))$ for $m$ change points: $O(n \log n)$ when the splits are balanced and $O(n^2)$ in the worst case. It is a greedy method. It does not minimize a global cost, and it can miss short segments that the first split hides. Wild binary segmentation repairs this by also searching random sub-intervals.

## In plain words

You have a long record of a measurement and you suspect its average level changed a few times. First you ask: if I could cut the record in exactly one place, where would the two parts differ most? If the difference there is clearly larger than noise, you make the cut. Then you treat each part as a new record and ask the same question. You stop cutting a part when no cut in it gives a clear difference. The method is fast and simple. Its weakness is that it judges each cut alone, so a short burst in the middle of a long flat record can look too small to cut at first, and then it is never found.

## The problem

Given $x_1, \ldots, x_n$, modelled as a piecewise constant mean plus noise of variance $\sigma^2$, find the change points $0 < \tau_1 < \cdots < \tau_m < n$, where $\tau_j$ is the last index of segment $j$. See [change-point detection](/change-point-detection/) for the problem and the exact methods.

For a segment $x_{s+1}, \ldots, x_e$ and a split $s < b < e$, the CUSUM contrast is
$$C(s, b, e) = \sqrt{\frac{(b - s)(e - b)}{e - s}}\;\bigl|\bar x_{s+1..b} - \bar x_{b+1..e}\bigr|,$$
where $\bar x_{i..j}$ is the mean of $x_i, \ldots, x_j$. Its square is the drop in the residual sum of squares when the segment is cut at $b$. Under no change and Gaussian noise, $C(s, b, e)/\sigma$ is the absolute value of a standard normal variable for each fixed $b$.

## The algorithm

```pseudo id=main
BINARY-SEGMENTATION(x_1, ..., x_n, ζ)
L1  P ← prefix sums of x; stack ← [(0, n)]; CP ← ∅
L2  while stack is not empty do
L3      pop (s, e); if e - s < 2 then continue             ▷ the segment is x_{s+1..e}
L4      b ← the smallest maximizer of C(s, b, e) over s < b < e; c ← C(s, b, e)
L5      if c ≤ ζ then continue                             ▷ no change in this segment
L6      add b to CP; push (s, b) and (b, e)
L7  return CP in increasing order
```

Line L4 uses $\bar x_{i..j} = (P_j - P_{i-1})/(j - i + 1)$, so each contrast costs $O(1)$ and the scan costs $O(e - s)$. The stack replaces the recursion; the order in which segments are processed does not change the result. Usual thresholds are $\zeta = C\sigma\sqrt{2\log n}$ with a constant $C$ a little above 1, for example $C = 1.3$ as in Fryzlewicz (2014), with $\sigma$ estimated robustly from the differences $x_{i+1} - x_i$. An alternative is to grow the full tree with a very small $\zeta$ and choose the number of changes by a criterion such as the [BIC](/bayesian-information-criterion/).

## Example

Take $n = 12$, $\zeta = 1.5$ and
$$x = (0.1, -0.3, 0.2, 0.0, 2.1, 1.8, 2.2, 1.9, 2.0, -0.1, 0.2, 0.1).$$
The contrasts on the whole series, $C(0, b, 12)$, rounded to 3 decimals, are:

| $b$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $C(0, b, 12)$ | 0.783 | 1.472 | 1.700 | **2.082** | 1.259 | 0.693 | 0.088 | 0.735 | 1.567 | 1.084 | 0.783 |

The best split is $b = 4$, and $2.082 > 1.5$, so 4 is a change point. On the right part $(4, 12)$ the contrasts for $b = 5, \ldots, 11$ are 0.882, 1.102, 1.661, 2.051, **2.647**, 1.837 and 1.256, so 9 is a change point. The remaining parts have best contrasts 0.200 on $(0, 4)$ at $b = 2$, 0.112 on $(4, 9)$ and 0.204 on $(9, 12)$, all below $\zeta$. The result is $\{4, 9\}$: means about 0, 2 and 0.

Note that the whole-series contrast at the true change 9 is only 1.567, because the two outer low parts pull the mean of the right side down. The method finds 9 only after the first cut has removed the left part.

## Correctness

Binary segmentation is a heuristic: it does not compute an optimal segmentation, and what it returns is defined by the procedure itself. Two facts are proved in full below.

1. **The contrast is the gain of a cut.** For every $s < b < e$, $C(s, b, e)^2 = \mathrm{RSS}(s, e) - \mathrm{RSS}(s, b) - \mathrm{RSS}(b, e)$, where $\mathrm{RSS}(i, j)$ is the residual sum of squares of $x_{i+1}, \ldots, x_j$ about their mean. So line L4 chooses the single cut that best fits a two-mean model to the segment by least squares.
2. **The stack version computes the recursive definition.** Define $\mathrm{BS}(s, e) = \emptyset$ if $e - s < 2$ or if the best contrast is at most $\zeta$, and otherwise $\mathrm{BS}(s, e) = \{b\} \cup \mathrm{BS}(s, b) \cup \mathrm{BS}(b, e)$. Each push makes the segment strictly shorter, so the loop ends after at most $2n - 1$ pops, and it returns exactly $\mathrm{BS}(0, n)$.

Fryzlewicz (2014) gives conditions under which binary segmentation is consistent: the segments must not be too short compared to $n$, and the jumps not too small. When these fail, as in the burst example under Variants, it can miss changes.

## Complexity

The segments popped from the stack form a binary tree. Segments at the same depth are disjoint, so the scans of line L4 at one depth cost $O(n)$ together. Each internal node of the tree is a change point, so the depth is at most $m + 1$, and the total time is $O(n(m + 1))$. When the splits are balanced the depth is $O(\log n)$ and the time is $O(n \log n)$. When every split cuts off one point, the depth is $n - 1$ and the time is $\Theta(n^2)$. This happens for $x_i = 3^i$ with $\zeta = 0$: on every prefix $x_1, \ldots, x_e$ the best cut is $b = e - 1$. The extra space is $O(n)$ for the prefix sums and the stack.

## Properties

- **Greedy.** Each cut is chosen without regard to later cuts, and a cut is never moved.
- **Nested results.** Lowering $\zeta$ only adds change points, so a single run with a small threshold gives the whole sequence of nested segmentations.
- **Simple and fast.** It needs only prefix sums and one scan per segment.
- **Not optimal.** For a given number of changes, the segmentation can have a larger residual sum of squares than the best one found by dynamic programming in [segmented least squares](/segmented-least-squares/) or [PELT](/pelt-algorithm/).
- **Weak on short segments.** A short segment far from the ends of a long parent gives a small contrast, because the contrast compares long averages.

## Variants and improvements

- **Wild binary segmentation (WBS).** Fryzlewicz (2014) draws $M$ random intervals $[s_j, e_j]$ once. On each segment, line L4 is replaced by a search over the segment itself and every drawn interval inside it, and the largest contrast decides the cut. When $M$ is large enough, with high probability some interval contains only one change with enough room on both sides, so short segments are found. The cost is $O(Mn)$ per level of the tree. Example: let $x$ be 50 zeros, then 4 values equal to 3, then 50 zeros, so $n = 104$ and $\zeta = 1.3\sqrt{2\log 104} = 3.962$. The best contrast on the whole series is 1.132 at $b = 50$, below $\zeta$, so binary segmentation finds nothing. WBS with 100 random intervals finds $\{50, 54\}$, and so does PELT with penalty $2\log n$.
- **Circular binary segmentation.** Olshen et al. (2004) look for a pair of cuts at once, the best segment that differs from the rest of the circle. It finds a short middle segment in one step and is standard for DNA copy number data.
- **Other costs.** The contrast can be replaced by any likelihood ratio for a single change, for example for a change in variance or in a Poisson rate.
- **Exact alternatives.** [PELT](/pelt-algorithm/) and optimal partitioning minimize the penalized cost exactly; their expected cost can be linear when changes are frequent.
- **Online detection.** For data that arrive one at a time, use the [CUSUM](/cusum/) or [Bayesian online changepoint detection](/bayesian-online-changepoint-detection/).

## When to use it

Use binary segmentation as a fast first pass on long series with a few well separated changes, or to produce the nested set of candidate segmentations for a model selection step. Use WBS or circular binary segmentation when short segments matter, and an exact penalized method when the best segmentation for a given cost is required.

## Pitfalls

- **Masking.** Two changes close together with opposite jumps can cancel in the whole-series contrast, so neither is found. WBS and exact methods are much less affected.
- **Threshold on the wrong scale.** The threshold must scale with the noise level $\sigma$. Estimate $\sigma$ robustly, for example from the median absolute difference of neighbours, because the plain standard deviation of the series includes the jumps.
- **Dependent noise.** Positive autocorrelation makes contrasts larger under no change, so the method finds false changes. Inflate $\zeta$ or model the dependence.
- **Reading the order of the cuts as importance.** The first cut is the strongest single cut of the whole series, not necessarily the largest jump.
- **Off-by-one in the output.** Here a change point is the last index of a segment. Other software reports the first index of the new segment.

## Implementations

## History

Scott and Knott (1974) proposed splitting a set of ordered group means into two groups by the largest between-group sum of squares, and then splitting each group again, which is binary segmentation applied to means. Vostrikova (1981, Soviet Mathematics Doklady 24) studied the method for change points in a multivariate process and proved its consistency. Olshen et al. (2004) introduced circular binary segmentation for DNA copy number arrays. Fryzlewicz (2014) introduced wild binary segmentation and analysed both methods.

## References
