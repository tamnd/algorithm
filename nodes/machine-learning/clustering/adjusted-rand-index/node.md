---
tag: W19B99
kind: definition
slug: adjusted-rand-index
name: Adjusted Rand index
aliases:
- ARI
- Hubert-Arabie adjusted Rand index
area: machine-learning/clustering
level: advanced
summary: "The Rand index corrected for chance under the permutation model: (index - expected)/(max - expected). It is 1 for equal partitions, 0 on average for random ones, and can be negative."
prereqs: [rand-index, binomial-coefficient, expected-value, linearity-of-expectation]
see_also: [normalized-mutual-information, cluster-validity, cluster-purity, random-permutation, consensus-clustering]
sources:
  - paper: doi:10.1007/BF01908075
    title: "Lawrence Hubert and Phipps Arabie, Comparing partitions, Journal of Classification 2(1), 1985, pages 193 to 218"
    locator: the expected Rand index under the generalized hypergeometric model and the corrected index (index - expected)/(max - expected)
  - paper: doi:10.1080/01621459.1971.10482356
    title: "William M. Rand, Objective criteria for the evaluation of clustering methods, Journal of the American Statistical Association 66(336), 1971, pages 846 to 850"
    locator: the unadjusted index c over pairs of points
  - paper: "Nguyen Xuan Vinh, Julien Epps and James Bailey, Information theoretic measures for clusterings comparison: variants, properties, normalization and correction for chance, Journal of Machine Learning Research 11, 2010, pages 2837 to 2854"
    locator: the comparison of the adjusted Rand index with the adjusted mutual information, and the bias of unadjusted indices toward more clusters
---

The adjusted Rand index (ARI) compares two partitions of the same objects, like the [Rand index](/rand-index/), but it subtracts the agreement that is expected by chance. Hubert and Arabie defined it in 1985 as

$$\mathrm{ARI} = \frac{\text{index} - \text{expected index}}{\text{maximum index} - \text{expected index}},$$

where the expectation is over random partitions with the same block sizes. The ARI is 1 when the two partitions are equal, its mean over random partitions with those sizes is exactly 0, and it can be negative. It is the most common external [cluster validity](/cluster-validity/) index when true classes are known.

## Definition

**Setting.** $X$ is a set of $n$ objects, and $U = \{U_1, \ldots, U_r\}$ and $V = \{V_1, \ldots, V_s\}$ are two [partitions](/set-partitions/) of $X$. No distance is used. In clustering, $U$ is the output of a method and $V$ is the partition into known classes.

**Counts.** Let $n_{ij} = |U_i \cap V_j|$ be the contingency table, with row sums $a_i = |U_i|$ and column sums $b_j = |V_j|$. Let $N = \binom{n}{2}$ and

$$S = \sum_{i,j} \binom{n_{ij}}{2}, \qquad A = \sum_i \binom{a_i}{2}, \qquad B = \sum_j \binom{b_j}{2}.$$

$S$ is the number of pairs that are together in both partitions, $A$ the number together in $U$, and $B$ the number together in $V$. The [Rand index](/rand-index/) is $(N + 2S - A - B)/N$, so it is an increasing linear function of $S$ when the block sizes are fixed.

**The permutation model.** Keep the block sizes $(a_i)$ and $(b_j)$ fixed. Apply a uniform [random permutation](/random-permutation/) $\sigma$ of $X$ to the blocks of $V$. Then the table $(n_{ij})$ has the generalized hypergeometric distribution.

**Lemma.** Under this model, $E[S] = AB/N$.

*Proof.* $S$ is the sum, over the $A$ pairs $\{x, y\}$ that are together in $U$, of the [indicator](/indicator-random-variable/) that $x$ and $y$ are together in $\sigma(V)$. The pair $\{\sigma^{-1}(x), \sigma^{-1}(y)\}$ is a uniform random pair of distinct objects, so this probability is $B/N$. By [linearity of expectation](/linearity-of-expectation/), $E[S] = A \cdot B/N$. $\square$

**The index.** $S \le \min(A, B) \le (A + B)/2$, and Hubert and Arabie take $(A + B)/2$ as the maximum. Then

$$\mathrm{ARI}(U, V) = \frac{S - \dfrac{AB}{N}}{\dfrac{A + B}{2} - \dfrac{AB}{N}}.$$

Because the Rand index is $\mathrm{RI} = (N + 2S - A - B)/N$ and $\mathrm{RI} = 1$ exactly when $S = (A + B)/2$, the same value is

$$\mathrm{ARI} = \frac{\mathrm{RI} - E[\mathrm{RI}]}{1 - E[\mathrm{RI}]}.$$

In terms of the pair counts $a = S$, $b = A - S$, $c = B - S$ and $d = N - A - B + S$ of the Rand index page, the ARI is $2(ad - bc)/((a + b)(b + d) + (a + c)(c + d))$, which is Cohen's kappa of the $2 \times 2$ table of pair decisions.

**When the denominator is 0.** By the inequality of the arithmetic and geometric means, and because $A, B \le N$,

$$\frac{A + B}{2} \ \ge\ \sqrt{AB} \ \ge\ \frac{AB}{N}.$$

Equality in both steps needs $A = B$ and either $AB = 0$ or $AB = N^2$. So the denominator is 0 only when $A = B = 0$ (both partitions are all singletons) or $A = B = N$ (both partitions are one block). In both cases $U = V$, and the convention, which the implementation follows, is $\mathrm{ARI} = 1$. The same convention applies to $n < 2$, where there are no pairs. The implementation computes the index as an exact fraction.

**Properties.**

- **Maximum.** $\mathrm{ARI} \le 1$, with equality if and only if $U = V$. Equality needs $S = (A + B)/2$, so $S = A = B$. $S = A$ means that every pair together in $U$ is together in $V$, and $S = B$ means the converse, so the partitions are equal.
- **Zero mean.** The ARI is a linear function of $S$ for fixed block sizes, so its mean under the permutation model is exactly 0.
- **Negative values.** If the partitions agree less than chance, $S < AB/N$ and the ARI is negative. Over all pairs of partitions with $n \le 6$, the least value is $-1/2$.
- **A trivial side.** If $U$ is one block, then $S = B = E[S]$ and the ARI is 0 for any $V$ with $B < N$. If $U$ is all singletons, $S = A = 0 = E[S]$ and the ARI is 0 for any $V$ with $B > 0$.
- **Symmetry.** The formula is symmetric in $U$ and $V$, and it does not change when the labels are renamed.
- **Cost.** One pass over the $n$ label pairs builds the nonzero cells of the table. The rest is $O(r + s + \text{number of nonzero cells})$ arithmetic.

## Examples and non-examples

**The example of Manning, Raghavan and Schütze.** 17 objects, three clusters and three classes, with the table

| | x | o | d | $a_i$ |
|---|---|---|---|---|
| cluster 1 | 5 | 1 | 0 | 6 |
| cluster 2 | 1 | 4 | 1 | 6 |
| cluster 3 | 2 | 0 | 3 | 5 |
| $b_j$ | 8 | 5 | 4 | 17 |

Here $N = 136$, $S = 20$, $A = 40$ and $B = 44$. The expected value is $E[S] = 40 \cdot 44/136 = 220/17 \approx 12.94$. So

$$\mathrm{ARI} = \frac{20 - 220/17}{42 - 220/17} = \frac{120/17}{494/17} = \frac{60}{247} \approx 0.243.$$

The Rand index of the same table is $92/136 \approx 0.676$. The large gap between the two numbers shows how much of the Rand index comes from chance: a random clustering with the same sizes has a mean Rand index of $331/578 \approx 0.573$.

**A negative value.** Take $n = 4$, $U = \{\{0, 1\}, \{2, 3\}\}$ and $V = \{\{0, 2\}, \{1, 3\}\}$. No pair is together in both, so $S = 0$, while $A = B = 2$ and $N = 6$. Then $E[S] = 2/3$ and

$$\mathrm{ARI} = \frac{0 - 2/3}{2 - 2/3} = -\frac{1}{2}.$$

The two partitions cross each other: they agree less than two random partitions with blocks of size 2.

**The mean over all arrangements.** For $U = \{\{0, 1, 2\}, \{3, 4, 5\}\}$, take $V$ with the same block sizes in all possible ways. The mean of $S$ is $6 \cdot 6/15 = 12/5$ and the mean ARI is 0, while the mean Rand index is $13/25 = 0.52$. This holds for any block sizes and any $n \ge 2$.

**Non-examples.**

- The ARI is not the Rand index on a new scale. The expected value depends on the block sizes, so two clusterings with the same Rand index can have different ARI values.
- The ARI is not bounded below by 0. A value below 0 is not an error. It means less agreement than chance.
- A mean of 0 holds under the permutation model with fixed block sizes. If the sizes of the random partition also vary, the mean ARI is not 0 in general.
- The ARI does not score a clustering without labels. For that, use an internal index such as the [silhouette coefficient](/silhouette-coefficient/).

## Related definitions

- [Rand index](/rand-index/): the unadjusted share of agreeing pairs.
- [Normalized mutual information](/normalized-mutual-information/) and its chance-corrected form, the adjusted mutual information, which uses the same permutation model.
- [Cluster purity](/cluster-purity/): a simple external index with no chance correction.
- [Consensus clustering](/consensus-clustering/) uses the ARI or similar indices to compare the members of an ensemble.
- [Cluster validity](/cluster-validity/) gives the overview of external and internal indices.

## References
