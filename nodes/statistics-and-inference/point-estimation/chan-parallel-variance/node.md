---
tag: EJXH8E
kind: algorithm
slug: chan-parallel-variance
name: Chan-Golub-LeVeque parallel variance algorithm
aliases:
- pairwise variance algorithm
- parallel variance merge
area: statistics-and-inference/point-estimation
level: advanced
summary: Merges the counts, means and sums of squared deviations of two partitions into those of their union, so that variance can be computed in parallel or by divide and conquer.
model: floating-point-model
complexity:
  vars: {n: "the number of data values, at least 2"}
  time: {worst: Θ(n), best: Θ(n)}
  depth: {worst: Θ(log n)}
  space: {extra: Θ(log n)}
  flops: {worst: "10 n - 9"}
properties: {deterministic: true, recursive: true, parallel: true, online: false, exact_in_exact_arithmetic: true}
history:
  year: 1979
  people: [Tony F. Chan, Gene H. Golub, Randall J. LeVeque]
  note: Chan, Golub and LeVeque gave the updating formula for two samples and the pairwise algorithm in a 1979 Stanford report, and surveyed the variance algorithms in The American Statistician in 1983. Barlow proved in 1990 that the pairwise algorithm is numerically stable.
prereqs: [sample-variance, welford-algorithm, divide-and-conquer-paradigm]
see_also: [pairwise-summation, parallel-reduction, monoid, work-span-model, catastrophic-cancellation, variance, covariance-matrix, kahan-summation]
sources:
  - paper: doi:10.1080/00031305.1983.10483115
    title: Tony F. Chan, Gene H. Golub and Randall J. LeVeque, Algorithms for computing the sample variance, analysis and recommendations, The American Statistician 37(3), 1983
    locator: pp. 242 to 247 (the formulas (1.5) and (1.6) for combining two samples, the pairwise algorithm, Table 1 of error bounds, and Section 4 on parallel use)
  - paper: "Tony F. Chan, Gene H. Golub and Randall J. LeVeque, Updating formulae and a pairwise algorithm for computing sample variances, Technical Report STAN-CS-79-773, Computer Science Department, Stanford University, 1979"
    title: Updating formulae and a pairwise algorithm for computing sample variances
    locator: the whole report (the first presentation of the pairwise algorithm)
  - paper: doi:10.1007/BF01385641
    title: Jesse L. Barlow, Error analysis of a pairwise summation algorithm to compute the sample variance, Numerische Mathematik 58(6), 1990
    locator: pp. 583 to 590 (the rounding error analysis that proves the pairwise algorithm stable)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 1.9 (computing the sample variance)
---

The Chan-Golub-LeVeque algorithm combines the summaries $(n_a, \bar x_a, \mathrm{SS}_a)$ and $(n_b, \bar x_b, \mathrm{SS}_b)$ of two disjoint parts of a data set, each a count, a mean and a sum of squared deviations, into the summary of their union, in a constant number of operations. Because the merge is exact and associative, the [sample variance](/sample-variance/) of $n$ values can be computed by any tree of merges: in parallel with span $\Theta(\log n)$, or by the pairwise recursion, whose rounding error grows more slowly than that of a one-pass loop. [Welford's algorithm](/welford-algorithm/) is the special case in which the second part has one value.

## In plain words

Split the data into two piles and give each pile to a different worker. Each worker reports three numbers: how many values it has, their average, and their total squared distance from that average. To get the same three numbers for all the data, add the counts, and take the average of the two averages weighted by the counts. The total squared distance is the two totals plus a correction for the gap between the two averages: the square of the gap, times the two counts multiplied together, divided by the total count.

Since piles can be merged in any order and grouping, the data can be cut into many piles and the results merged in a tree. Cutting the data in halves again and again and merging back up also makes the rounding errors smaller than in a loop over the values one at a time.

## The problem

**The merge.** The input is two summaries $a = (n_a, m_a, M_a)$ and $b = (n_b, m_b, M_b)$, where $(n_a, m_a, M_a)$ are the count, the mean and the sum of squared deviations $\sum (x - m_a)^2$ of a nonempty multiset $A$ of reals, and likewise for $B$. The output is the summary of $A \uplus B$. The data themselves are not available.

**The variance.** The input is $x_1, \ldots, x_n$ with $n \ge 2$. The output is $\bar x$, $\mathrm{SS} = \sum_i (x_i - \bar x)^2$ and $S^2 = \mathrm{SS}/(n-1)$, computed by merges.

## The algorithm

```pseudo id=main
COMBINE((n_a, m_a, M_a), (n_b, m_b, M_b))      ▷ n_a, n_b ≥ 1
L1  n ← n_a + n_b
L2  δ ← m_b - m_a                               ▷ gap between the means
L3  m ← m_a + δ · n_b / n
L4  M ← M_a + M_b + δ · δ · n_a · n_b / n       ▷ between-part term
L5  return (n, m, M)

PAIRWISE(x, lo, hi)                             ▷ summary of x[lo .. hi - 1], hi - lo ≥ 1
L6  if hi - lo = 1 then return (1, x[lo], 0)
L7  mid ← lo + ⌊(hi - lo) / 2⌋
L8  a ← PAIRWISE(x, lo, mid)                    ▷ lines L8 and L9 may run in parallel
L9  b ← PAIRWISE(x, mid, hi)
L10 return COMBINE(a, b)

PAIRWISE-VARIANCE(x_1, ..., x_n)                ▷ n ≥ 2
L11 (n, m, M) ← PAIRWISE(x, 0, n)
L12 return m, M / (n - 1), M
```

Line L3 moves the mean of $A$ toward the mean of $B$ by the fraction $n_b/n$ of the gap. Line L4 adds the between-part sum of squares, $n_a(m_a - m)^2 + n_b(m_b - m)^2$, written in the form $\delta^2 n_a n_b/n$. Both lines use the difference $\delta$ of two means, not the difference of two large sums of squares, so nothing in the merge cancels catastrophically.

Chan, Golub and LeVeque state the merge with the sums $T_a = n_a m_a$ and $T_b = n_b m_b$ in place of the means, as $M = M_a + M_b + \frac{n_a}{n_b\, n}\big(\frac{n_b}{n_a} T_a - T_b\big)^2$ (their formula (1.5b)). Since $\frac{n_b}{n_a}T_a - T_b = -n_b\delta$, it is the same number in exact arithmetic. For equal halves, $n_a = n_b = h$, it reduces to $M = M_a + M_b + (T_a - T_b)^2/(2h)$ (their (1.6)).

Any other tree of merges gives the same exact result: one Welford accumulator per thread, or per block of a file, followed by a tree of COMBINE calls, is the usual parallel form.

## Example

Take $x = (3, 7, 7, 9, 14)$, in exact arithmetic. PAIRWISE splits it at $mid = 2$ into $(3, 7)$ and $(7, 9, 14)$, and the second part at its middle into $(7)$ and $(9, 14)$.

| merge | $a$ | $b$ | $\delta$ | $m$ | $M$ |
|---|---|---|---|---|---|
| $(3) + (7)$ | $(1, 3, 0)$ | $(1, 7, 0)$ | 4 | 5 | $0 + 0 + 16 \cdot 1 \cdot 1/2 = 8$ |
| $(9) + (14)$ | $(1, 9, 0)$ | $(1, 14, 0)$ | 5 | $23/2$ | $25/2$ |
| $(7) + (9, 14)$ | $(1, 7, 0)$ | $(2, 23/2, 25/2)$ | $9/2$ | 10 | $25/2 + \frac{81}{4}\cdot\frac{2}{3} = 26$ |
| $(3, 7) + (7, 9, 14)$ | $(2, 5, 8)$ | $(3, 10, 26)$ | 5 | 8 | $8 + 26 + 25 \cdot 6/5 = 64$ |

So $\bar x = 8$, $\mathrm{SS} = 64$ and $S^2 = 16$, as on [sample variance](/sample-variance/). The last merge reads: $\delta = 10 - 5 = 5$, $m = 5 + 5 \cdot 3/5 = 8$ and $M = 8 + 26 + 25 \cdot 2 \cdot 3/5 = 64$.

## Correctness

With $m$ the mean of the union, $m_a - m = -\delta n_b/n$ and $m_b - m = \delta n_a/n$, so the term of line L4 equals $n_a(m_a - m)^2 + n_b(m_b - m)^2$. The shift identity $\sum_{v \in A}(v - m)^2 = M_a + n_a(m_a - m)^2$, applied to $A$ and to $B$, then shows that $M$ is the sum of squared deviations of the union around its mean. So one merge is exact. The same identity, with the counts as weights, shows that merging three summaries in either grouping gives $M_a + M_b + M_c + \sum_i n_i(m_i - m)^2$, so COMBINE is associative and commutative, and PAIRWISE is correct by induction on the length. The full proofs are below.

## Complexity

PAIRWISE on $n$ values makes $n - 1$ merges. Counting the counts as integers, each merge does 10 floating-point operations (one in line L2, three in line L3, six in line L4), and line L12 adds one division, so the count is exactly $10n - 9$. Chan, Golub and LeVeque count the sum form for $n$ a power of 2 as $2n$ multiplications and $4n$ additions; their form needs fewer operations per merge.

- **Work and span.** In the [work-span model](/work-span-model/) with lines L8 and L9 in parallel, the work is $\Theta(n)$ and the span is $\Theta(\log n)$. With $p$ processors, each running Welford's algorithm on a block of $n/p$ values and then merging in a tree, the time is $\Theta(n/p + \log p)$.
- **Space.** The recursion is $\lceil \log_2 n \rceil$ deep, so the stack is $\Theta(\log n)$. A bottom-up version that keeps one summary per level of a binary counter also uses $\Theta(\log n)$ summaries and reads the data once, in order.

**Rounding error.** With the condition number $\kappa = \sqrt{1 + n\bar x^2/\mathrm{SS}}$ defined on [Welford's algorithm](/welford-algorithm/), Table 1 of Chan, Golub and LeVeque gives the bound $n\kappa u$ for the updating algorithms and $\kappa u \log n$ for the pairwise algorithm, with small constants dropped. They mark the pairwise bound as a conjecture, based on the bound for Youngs and Cramer's updating and on experiments. Barlow (1990) gave a rounding error analysis of the pairwise algorithm and proved that it is numerically stable. The same improvement from $n$ to $\log n$ is proved for plain sums by [pairwise summation](/pairwise-summation/).

**Measured errors.** The relative error of $S^2$ in double precision against the exact value of the stored data, computed with `fractions.Fraction`, for data $10^6 + Z_i$ with $Z_i$ standard normal ($\kappa \approx 10^6$). The rows come from `random.Random(1)`, one run each, drawn after the four rows of the table on [Welford's algorithm](/welford-algorithm/), in the order 1000, $10^4$ (that table's third row), $10^5$.

| $n$ | textbook | Welford | pairwise |
|---|---|---|---|
| 1000 | $2.9 \times 10^{-3}$ | $1.4 \times 10^{-11}$ | $3.7 \times 10^{-12}$ |
| $10^4$ | $6.4 \times 10^{-3}$ | $2.1 \times 10^{-11}$ | $7.2 \times 10^{-13}$ |
| $10^5$ | $2.4 \times 10^{-2}$ | $4.5 \times 10^{-12}$ | $3.1 \times 10^{-13}$ |

These are single runs, not bounds. In each row the pairwise error is 4 to 30 times smaller than the Welford error, and both are far below their bounds. One run per row cannot show the growth in $n$ that the bounds describe; the Welford error at $n = 10^5$ happens to be the smallest of its column.

## Properties

- **Exact in exact arithmetic,** for every split and every tree of merges.
- **Associative and commutative.** The summaries form a commutative [monoid](/monoid/) with the identity $(0, 0, 0)$, if COMBINE returns the other argument when one count is 0. So the merge is a valid operator for a [parallel reduction](/parallel-reduction/), a segment tree, or the combine step of MapReduce.
- **Order dependent in floating point.** Different trees give results that differ in the last digits.
- **Constant size summaries.** A part of any size is described by three numbers.

## Variants and improvements

- **Welford's algorithm.** COMBINE with $b = (1, x, 0)$ gives $\delta = x - m_a$, $m = m_a + \delta/n$ and $M = M_a + \frac{n-1}{n}\delta^2$, which is [Welford's update](/welford-algorithm/).
- **Covariance.** For pairs, merge the two means separately and the co-moment by $C = C_a + C_b + \delta_x \delta_y n_a n_b/n$; the vector version merges [covariance matrices](/covariance-matrix/) with the outer product $\delta\delta^{\mathsf T}$.
- **Weights.** Replace the counts by sums of weights; the formulas do not change.
- **Higher moments.** The third and fourth central sums also merge in closed form, with more terms in $\delta$.
- **Removing a part.** Solving the merge for $a$ given the union and $b$ removes a part, but it subtracts and can lose accuracy.
- **Corrected two-pass.** When the data fit in memory, Chan, Golub and LeVeque recommend the corrected two-pass algorithm, $\mathrm{SS} = \sum_i (x_i - \bar x)^2 - \frac1n\big(\sum_i (x_i - \bar x)\big)^2$, where the second term estimates the rounding error of the first.

## When to use it

Use the merge whenever partial results must be combined: threads, GPU blocks, distributed workers, database partitions, or a stream summarized per time window and later rolled up. Use the pairwise recursion when the data are in memory and the accuracy of a one-pass method is not enough but a second pass is not wanted. When one pass over a stream on one processor is all that is needed, [Welford's algorithm](/welford-algorithm/) is simpler.

## Pitfalls

- **Merging variances instead of sums.** Averaging the two variances, even weighted by counts, ignores the between-part term $\delta^2 n_a n_b/n$. For $(3, 7)$ and $(7, 9, 14)$ the parts have $\mathrm{SS}$ 8 and 26, which add to 34, while the union has 64.
- **The divisor.** Merge the sums of squared deviations $M$, not $S^2$ or $\hat\sigma^2$, and divide only at the end by $n - 1$ or $n$, saying which one.
- **Integer overflow.** In a language with fixed-width integers, $n_a n_b$ can overflow; compute it in floating point.
- **Empty parts.** Line L3 divides by $n$, so two empty parts cannot be merged; treat a part with count 0 as the identity.
- **Textbook parts.** If each part computes its $M$ by the textbook formula $\sum x^2 - n_a m_a^2$, the merge inherits that cancellation. Compute the parts with Welford's algorithm or by pairwise merging.

## Implementations

## History

Chan, Golub and LeVeque gave the formula for combining two samples and the pairwise algorithm in a Stanford report in 1979 and surveyed the algorithms for the sample variance in The American Statistician in 1983, with error bounds in terms of the condition number $\kappa$. Their bound for the pairwise algorithm was stated as a conjecture. Barlow (1990) proved, by a rounding error analysis, that the pairwise algorithm is numerically stable.

## References
