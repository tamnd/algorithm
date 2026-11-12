---
tag: C0AH5H
kind: definition
slug: rand-index
name: Rand index
aliases:
- Rand measure
- Rand similarity of two partitions
area: machine-learning/clustering
level: intro
summary: The share of the n(n-1)/2 pairs of objects on which two partitions agree, as together in both or apart in both. It is 1 only for equal partitions.
prereqs: [clustering-problem, binomial-coefficient, set-partitions]
see_also: [adjusted-rand-index, cluster-validity, normalized-mutual-information, cluster-purity, confusion-matrix]
sources:
  - paper: doi:10.1080/01621459.1971.10482356
    title: "William M. Rand, Objective criteria for the evaluation of clustering methods, Journal of the American Statistical Association 66(336), 1971, pages 846 to 850"
    locator: the similarity c of two clusterings, counted over all pairs of points, and its properties
  - paper: doi:10.1007/BF01908075
    title: "Lawrence Hubert and Phipps Arabie, Comparing partitions, Journal of Classification 2(1), 1985, pages 193 to 218"
    locator: the Rand index written with the sums of binomial coefficients of the contingency table, and its expected value under the hypergeometric model
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schütze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Section 16.3 (evaluation of clustering), with the Rand index of the 17-point example of Figure 16.4
---

The Rand index measures how much two partitions of the same $n$ objects agree. It looks at all $\binom{n}{2}$ pairs of objects and counts the share of pairs on which the partitions agree: both put the two objects in the same cluster, or both put them in different clusters. William Rand proposed it in 1971. It is an external [cluster validity](/cluster-validity/) index: usually one partition is the output of a [clustering](/clustering-problem/) method and the other is a set of known classes. The value is between 0 and 1, and it is 1 only when the two partitions are equal. Its main weakness is that two random partitions also get a high value, which the [adjusted Rand index](/adjusted-rand-index/) corrects.

## Definition

**Setting.** $X$ is a finite set of $n$ objects. The index uses no distance and no coordinates, only two [partitions](/set-partitions/) of $X$: $U = \{U_1, \ldots, U_r\}$ and $V = \{V_1, \ldots, V_s\}$. The numbers of blocks $r$ and $s$ can be different. In clustering, $U$ is the clustering with $r = k$ clusters and $V$ is the partition into true classes.

**Pair counts.** Each of the $N = \binom{n}{2}$ unordered pairs $\{x, y\}$ of distinct objects falls into exactly one of four types:

| type | in $U$ | in $V$ | count |
|---|---|---|---|
| agree, together | same block | same block | $a$ |
| disagree | same block | different blocks | $b$ |
| disagree | different blocks | same block | $c$ |
| agree, apart | different blocks | different blocks | $d$ |

So $a + b + c + d = N$. The **Rand index** is

$$\mathrm{RI}(U, V) = \frac{a + d}{a + b + c + d} = \frac{a + d}{\binom{n}{2}}.$$

For $n < 2$ there are no pairs. The implementation returns 1 in that case, because the two partitions are equal.

**From the contingency table.** Let $n_{ij} = |U_i \cap V_j|$, with row sums $a_i = |U_i|$ and column sums $b_j = |V_j|$. Write

$$S = \sum_{i,j} \binom{n_{ij}}{2}, \qquad A = \sum_i \binom{a_i}{2}, \qquad B = \sum_j \binom{b_j}{2}.$$

A pair that is together in both partitions lies in exactly one cell $U_i \cap V_j$, so $a = S$. A pair that is together in $U$ lies in exactly one row, so $a + b = A$, and in the same way $a + c = B$. Then $d = N - a - b - c = N - A - B + S$, and

$$\mathrm{RI}(U, V) = \frac{N + 2S - A - B}{N}.$$

With a hash map over the nonempty cells, this takes $O(n)$ time after one pass over the labels, against $O(n^2)$ for the direct count over all pairs. The [binomial coefficient](/binomial-coefficient/) $\binom{m}{2} = m(m-1)/2$ is the only function that the formula needs.

**Properties.**

- $0 \le \mathrm{RI} \le 1$, and the index is symmetric in $U$ and $V$.
- $\mathrm{RI}(U, V) = 1$ if and only if $U = V$ (for $n \ge 2$). If $U \ne V$, some pair is together in one partition and apart in the other.
- $1 - \mathrm{RI}$ is a metric on the partitions of $X$. Let $E_U$ be the set of pairs that are together in $U$. A partition is fixed by $E_U$, and $b + c = |E_U \,\triangle\, E_V|$. The size of a symmetric difference is a metric on sets, so $1 - \mathrm{RI} = |E_U \,\triangle\, E_V| / N$ is a metric too. The count $2(b + c)$ is also known as the Mirkin distance.
- The index does not change when the labels are renamed, because it uses only the blocks.
- The index can be 0. If $U$ has one block and $V$ has $n$ singletons, every pair is of type $b$.

## Examples and non-examples

**The example of Manning, Raghavan and Schütze.** 17 objects are in three classes x, o and d, and a method returns three clusters. The contingency table is:

| | x | o | d | $a_i$ |
|---|---|---|---|---|
| cluster 1 | 5 | 1 | 0 | 6 |
| cluster 2 | 1 | 4 | 1 | 6 |
| cluster 3 | 2 | 0 | 3 | 5 |
| $b_j$ | 8 | 5 | 4 | 17 |

Then $N = \binom{17}{2} = 136$, and

- $S = \binom{5}{2} + \binom{4}{2} + \binom{3}{2} + \binom{2}{2} = 10 + 6 + 3 + 1 = 20$, so $a = 20$,
- $A = 15 + 15 + 10 = 40$, so $b = A - a = 20$,
- $B = 28 + 10 + 6 = 44$, so $c = B - a = 24$,
- $d = 136 - 20 - 20 - 24 = 72$.

So $\mathrm{RI} = (20 + 72)/136 = 92/136 \approx 0.676$. In the words of information retrieval, $a$ is the number of true positive pairs, $b$ the false positives, $c$ the false negatives and $d$ the true negatives. The Rand index is the accuracy of the pair decisions.

**High values by chance.** Keep the sizes of the blocks fixed and put the objects into them at random. The mean Rand index over all such arrangements is $(N + 2AB/N - A - B)/N$ (the [adjusted Rand index](/adjusted-rand-index/) page proves $E[S] = AB/N$). For the table above it is $331/578 \approx 0.573$, so the clustering is only about 0.10 above a random clustering with the same sizes. The baseline also depends on the number of blocks. For $n = 6$:

| both partitions | mean RI over random arrangements |
|---|---|
| two blocks of 3 | $13/25 = 0.52$ |
| three blocks of 2 | $17/25 = 0.68$ |

With more and smaller blocks, most pairs are apart in both partitions, so $d$ is large for any arrangement. For this reason a raw Rand index cannot compare clusterings with different numbers of clusters in a fair way.

**Two extremes.** For $U = \{\{0, 1, 2, 3\}\}$ and $V = \{\{0\}, \{1\}, \{2\}, \{3\}\}$, all 6 pairs are of type $b$ and $\mathrm{RI} = 0$. For $U = V$, $b = c = 0$ and $\mathrm{RI} = 1$.

**Non-examples.**

- The Rand index is not the share of objects that are in the correct cluster. That needs a matching of clusters to classes, as in [purity](/cluster-purity/). The Rand index counts pairs, so it needs no matching.
- It does not score a single clustering. It always compares two partitions. To score one clustering without labels, use an internal index such as the [silhouette coefficient](/silhouette-coefficient/).
- It is not corrected for chance. A value of 0.68 can be no better than random, as the table above shows.

## Related definitions

- [Adjusted Rand index](/adjusted-rand-index/): $(\mathrm{RI} - E[\mathrm{RI}])/(1 - E[\mathrm{RI}])$ under the permutation model, so that random partitions score 0 on average.
- [Normalized mutual information](/normalized-mutual-information/): an external index from information theory that uses the same contingency table.
- [Cluster purity](/cluster-purity/): the share of objects in the majority class of their cluster.
- The pair counts $a, b, c, d$ are a [confusion matrix](/confusion-matrix/) for the decision "same cluster or not" on each pair. Other pair indices use them in other ways, for example the Jaccard index $a/(a + b + c)$ and the Fowlkes and Mallows index $a/\sqrt{(a + b)(a + c)}$, which ignore $d$.
- [Cluster validity](/cluster-validity/) gives the overview of external and internal indices.

## References
