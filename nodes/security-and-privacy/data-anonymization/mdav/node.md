---
tag: HMJJKR
kind: algorithm
slug: mdav
name: MDAV
aliases:
- maximum distance to average vector
area: security-and-privacy/data-anonymization
level: core
summary: Microaggregation heuristic that builds groups of k around the record farthest from the centroid and the record farthest from it, in turn.
model: real-ram
complexity:
  vars: {n: the number of records, d: the number of attributes, k: the least group size}
  time: {worst: O(n^2 (d + log k) / k + n d)}
  space: {extra: O(n)}
history:
  year: 2005
  people: [Josep Domingo-Ferrer, Vicenc Torra]
  note: "MDAV was first used in the mu-Argus software for statistical disclosure control. Domingo-Ferrer and Torra described MDAV-generic, the form on this page, in 2005."
prereqs: [microaggregation, euclidean-distance]
see_also: [k-anonymity, k-means, ward-method, k-nearest-neighbors, mondrian-anonymization, datafly, generalization-and-suppression]
sources:
  - paper: doi:10.1007/s10618-005-0007-5
    title: "Josep Domingo-Ferrer and Vicenc Torra, Ordinal, continuous and heterogeneous k-anonymity through microaggregation, Data Mining and Knowledge Discovery 11(2), 2005"
    locator: "pp. 195 to 212, the MDAV-generic algorithm, and k-anonymity by joint microaggregation of the quasi-identifiers"
  - paper: doi:10.1109/69.979982
    title: "Josep Domingo-Ferrer and Josep Maria Mateo-Sanz, Practical data-oriented microaggregation for statistical disclosure control, IEEE Transactions on Knowledge and Data Engineering 14(1), 2002"
    locator: "pp. 189 to 201, the optimal k-partition, the bound of 2k - 1 on group sizes, and fixed-size heuristics based on the farthest record from the centroid"
  - book: isbn:9781119978152
    title: "Anco Hundepool, Josep Domingo-Ferrer, Luisa Franconi, Sarah Giessing, Eric Schulte Nordholt, Keith Spicer and Peter-Paul de Wolf, Statistical Disclosure Control, Wiley, 2012"
    locator: "Chapter 3, Microdata, the section on microaggregation and its MDAV heuristic"
  - paper: "Anna Oganian and Josep Domingo-Ferrer, On the complexity of optimal microaggregation for statistical disclosure control, Statistical Journal of the United Nations Economic Commission for Europe 18(4), 2001"
    locator: "pp. 345 to 353, optimal multivariate microaggregation is NP-hard"
---

MDAV (maximum distance to average vector) is the standard heuristic for [microaggregation](/microaggregation/) of records with several numerical attributes. It forms groups of exactly $k$ records, two at a time: one group around the record farthest from the centroid of the records that are left, and one around the record farthest from that first record. When fewer than $3k$ records are left, it forms at most one more group and puts the rest, between $k$ and $2k - 1$ records, in a last group. Each record is then replaced by the centroid of its group. The release is [k-anonymous](/k-anonymity/) by construction. The loss is not optimal, because optimal multivariate microaggregation is NP-hard, but MDAV is simple, deterministic and fast, in $O(n^2 d / k)$ distance work.

## In plain words

Think of the records as points on a map. Find the middle of all the points. Take the point farthest from the middle: it is on the edge of the crowd, and it is the hardest point to hide. Make a group of it and its nearest neighbors, so that the group has the size you want. Then take the point farthest from that first point. It is on the other edge. Make a group around it in the same way. Remove both groups and do this again with the points that are left.

At the end a few points are left. They form the last group, which can be a little larger. Every point is then moved to the middle of its group. Each group shows one point many times, so no single point stands out.

## The problem

The input is a list of $n$ records $x_1, \ldots, x_n \in \mathbb{R}^d$ and an integer $k$ with $1 \le k \le n$. The attributes are on one scale, for example as z-scores. The output is a partition of the records into groups of at least $k$ records, and the masked records, where each record is replaced by the centroid of its group. The goal is a small within-group sum of squared errors,

$$\mathrm{SSE} = \sum_{g} \sum_{i \in g} \lVert x_i - \bar{x}_g \rVert^2 .$$

The least SSE is NP-hard to find for $d \ge 2$ (Oganian and Domingo-Ferrer 2001), so MDAV is a heuristic: only the group sizes are guaranteed. The value of $k$ is a policy choice.

## The algorithm

The distance is the [Euclidean distance](/euclidean-distance/). Ties go to the lowest index, both for the farthest record and for the nearest ones.

```pseudo id=main
MDAV(X, k)
L1  R ← the indices of all records; G ← an empty list
L2  while |R| ≥ 3k do
L3      c ← the centroid of the records of R
L4      r ← the record of R farthest from c
L5      g ← r and its k - 1 nearest records in R; append g to G; R ← R \ g
L6      s ← the record of R farthest from r
L7      g ← s and its k - 1 nearest records in R; append g to G; R ← R \ g
L8  if |R| ≥ 2k then
L9      c ← the centroid of R; r ← the record of R farthest from c
L10     g ← r and its k - 1 nearest records in R; append g to G; R ← R \ g
L11 append R to G                          ▷ k ≤ |R| ≤ 2k - 1
L12 for each group g of G do
L13     replace each record of g by the centroid of g
L14 return G and the replaced records
```

Line L6 picks $s$ after line L5 has removed the group of $r$. Domingo-Ferrer and Torra (2005) take the record farthest from $r$ in the set before the removal. The two choices are the same: the farthest record from $r$ is not among its $k - 1$ nearest unless all the distances tie. With the tie rule here, the version on this page can always form the second group.

## Example

Take $k = 3$ and the 10 records

| record | $x_1$ | $x_2$ | $x_3$ | $x_4$ | $x_5$ | $x_6$ | $x_7$ | $x_8$ | $x_9$ | $x_{10}$ |
|---|---|---|---|---|---|---|---|---|---|---|
| value | (1, 1) | (2, 1) | (1, 2) | (8, 8) | (9, 8) | (8, 9) | (5, 1) | (5, 2) | (6, 1) | (4, 9) |

The squared distances below are exact.

| step | $\lvert R \rvert$ | what happens | group |
|---|---|---|---|
| L3 | 10 | $c = (4.9, 4.2)$ | |
| L4 | 10 | $x_6$ is farthest from $c$, at 32.65 ($x_5$: 31.25, $x_1$: 25.45) | |
| L5 | 7 | the 2 nearest to $x_6$ are $x_4$ (1) and $x_5$ (2) | $\{x_4, x_5, x_6\}$ |
| L6 | 7 | $x_1$ is farthest from $x_6$, at 113 ($x_2$: 100, $x_3$: 98) | |
| L7 | 4 | the 2 nearest to $x_1$ are $x_2$ (1) and $x_3$ (1) | $\{x_1, x_2, x_3\}$ |
| L2, L8 | 4 | $4 < 9$ and $4 < 6$, so no more groups | |
| L11 | 0 | the rest | $\{x_7, x_8, x_9, x_{10}\}$ |

The centroids are $(25/3, 25/3)$, $(4/3, 4/3)$ and $(5, 13/4)$. The first three records are released as $(4/3, 4/3)$, and $x_{10} = (4, 9)$ is released as $(5, 3.25)$. The SSE is $4/3 + 4/3 + 187/4 = 593/12 \approx 49.4$, against a total sum of squares of $405/2 = 202.5$.

The last group shows the weak point of MDAV. The record $x_{10}$ is far from $x_7$, $x_8$ and $x_9$, and alone it adds $34.06$ to the SSE. The optimal 3-partition, found by a search over all partitions, is $\{x_1, x_2, x_3\}$, $\{x_7, x_8, x_9\}$ and $\{x_4, x_5, x_6, x_{10}\}$, with SSE $221/12 \approx 18.4$. MDAV never looked at $x_{10}$: it was not the farthest record at line L4 or line L6.

## Correctness

By induction on the rounds of line L2: each round runs only when $|R| \ge 3k$, so lines L5 and L7 can each take $k$ records, and after the round $|R| \ge k$. When the loop stops, $k \le |R| < 3k$. Line L8 takes one more group when $|R| \ge 2k$, so at line L11, $k \le |R| \le 2k - 1$. The groups are therefore a partition with sizes $k, k, \ldots, k$ and a last size between $k$ and $2k - 1$. Each released value is the centroid of a group of at least $k$ records, so it occurs at least $k$ times, and the release is k-anonymous for any choice of quasi-identifier among the attributes. The centroids also keep the sum of each attribute. The full proof is in proofs/correctness.md.

## Complexity

Let $n$ be the number of records, $d$ the number of attributes and $k$ the group size. The model is the [real RAM](/real-ram/), with one step for each arithmetic operation on a real number.

- A round with $m$ records left computes two centroids or farthest records in $O(m d)$ time, and for lines L5 and L7 it computes $m$ distances and selects the $k - 1$ least with a heap of size $k$, in $O(m (d + \log k))$ time.
- The sizes of $R$ at the rounds are $n, n - 2k, n - 4k, \ldots$, with a sum of at most $n + n^2 / (4k)$.
- So the time is $O(n^2 (d + \log k) / k + n d)$, and the extra space is $O(n)$ for $R$ and the group labels, besides the output.

For a fixed $k$ this is quadratic in $n$. For a large file you can first split the records into blocks of at least $k$ records, for example by the value of one attribute, and run MDAV on each block. The group sizes stay between $k$ and $2k - 1$ in each block, but the SSE is usually higher, because no group crosses a block border.

## Properties

- **Group sizes.** All groups have exactly $k$ records, except the last, which has $k$ to $2k - 1$. This is a theorem.
- **k-anonymous.** If all quasi-identifiers are among the $d$ attributes, the release is k-anonymous. This is a theorem.
- **Not optimal.** The SSE can be much larger than the least SSE, as the example shows. The quality is a measured property on test data, and the papers report it as a percentage loss $\mathrm{SSE}/\mathrm{SST}$.
- **Means kept.** The mean of each attribute does not change. The variance falls by $\mathrm{SSE}/n$.
- **Deterministic.** With a fixed tie rule, the same input gives the same groups. The groups do not depend on the order of the records, except through ties.

## Variants and improvements

- **MDAV-generic with other data types.** Domingo-Ferrer and Torra (2005) use a distance and an average for each type: the mean for numbers, the median for ordinal values and the mode for nominal values. The steps stay the same.
- **Variable group sizes.** Variants let a group grow toward $2k - 1$ records when the next records are close to it and far from the rest. This can help in data with natural clusters, and it can keep an outlier out of the last group.
- **Univariate optimum.** On one attribute, or on a projection to one dimension, the optimal partition is a [shortest path](/shortest-path/) on the sorted values (Hansen and Mukherjee 2003). It needs no heuristic.
- **Ward's method with a least size.** A hierarchical alternative from the same literature (Domingo-Ferrer and Mateo-Sanz 2002), based on [Ward's method](/ward-method/), which merges the two clusters with the least growth of SSE.

## When to use it

Use MDAV to microaggregate a table of a few thousand records with several numerical quasi-identifiers, when you want a k-anonymous release that keeps the numerical scale and the means. It is a good baseline for other microaggregation heuristics. Scale the attributes first. For a single attribute use the optimal univariate method. If the data has strong outliers, check the last group, or use a variable-size variant. If the release needs a formal guarantee against any background knowledge, MDAV is not enough: use [differential privacy](/differential-privacy-definition/).

## Pitfalls

- **A group taken from all records at lines L5 and L7.** The nearest records must come from $R$, the records that are still free. If they come from the full table, a record can join two groups, and some groups have fewer than $k$ free members.
- **Stopping the loop at $|R| \ge 2k$ at line L2.** With the test $|R| \ge 2k$, a round with $2k \le |R| < 3k$ takes $2k$ records and can leave fewer than $k$ for line L11, so the last group is too small. The test must be $|R| \ge 3k$, followed by line L8.
- **Unscaled attributes at line L3.** The centroid and the distances then follow the attribute with the widest range, and the other attributes lose much more than needed.
- **Releasing the group label.** The group number or the order of the groups adds nothing for the analyst and can link records across releases. Release the masked records in a random order.

## Implementations

## History

Microaggregation was in use at statistical offices in the 1990s. Domingo-Ferrer and Mateo-Sanz (2002) stated the optimal k-partition problem, proved that optimal groups have fewer than $2k$ records, and proposed fixed-size heuristics that start from the record farthest from the centroid. Oganian and Domingo-Ferrer (2001) proved that the multivariate optimum is NP-hard. The heuristic called MDAV was implemented in the mu-Argus package for statistical disclosure control. Domingo-Ferrer and Torra (2005) gave MDAV-generic for continuous, ordinal and nominal data, and showed that joint microaggregation of the quasi-identifiers gives k-anonymity.

## References
