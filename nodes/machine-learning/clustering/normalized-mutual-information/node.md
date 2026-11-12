---
tag: 3MRTH1
kind: definition
slug: normalized-mutual-information
name: Normalized mutual information
aliases:
- NMI
- normalized mutual information of two clusterings
area: machine-learning/clustering
level: advanced
summary: The mutual information of two partitions divided by a mean of their entropies, so it lies in [0, 1]. It is not corrected for chance; the adjusted mutual information is.
prereqs: [shannon-entropy, conditional-entropy, clustering-problem]
see_also: [adjusted-rand-index, rand-index, cluster-purity, cluster-validity, information-gain, consensus-clustering]
sources:
  - paper: "Alexander Strehl and Joydeep Ghosh, Cluster ensembles, a knowledge reuse framework for combining multiple partitions, Journal of Machine Learning Research 3, 2002, pages 583 to 617"
    locator: the normalized mutual information I(X;Y)/sqrt(H(X)H(Y)) and its use to compare and combine clusterings
  - paper: "Nguyen Xuan Vinh, Julien Epps and James Bailey, Information theoretic measures for clusterings comparison: variants, properties, normalization and correction for chance, Journal of Machine Learning Research 11, 2010, pages 2837 to 2854"
    locator: the normalizations of the mutual information, the expected mutual information under the hypergeometric model, and the adjusted mutual information
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Chapter 2 (entropy, conditional entropy and mutual information, and the inequality I(X;Y) <= min(H(X), H(Y)))
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schütze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Section 16.3 (evaluation of clustering), with the NMI of the 17-point example of Figure 16.4
---

Normalized mutual information (NMI) compares two partitions of the same $n$ objects with information theory. The mutual information $I(U; V)$ is the amount of information that one partition gives about the other. NMI divides it by a mean of the two [entropies](/shannon-entropy/), so the value is between 0 and 1. It is an external [cluster validity](/cluster-validity/) index: usually one partition is a clustering and the other is a set of known classes. There are four common normalizations, and the values differ, so a report must say which one it uses. NMI is not corrected for chance. The adjusted mutual information (AMI) of Vinh, Epps and Bailey subtracts the expected value under the same permutation model as the [adjusted Rand index](/adjusted-rand-index/).

## Definition

**Setting.** $X$ is a set of $n$ objects, and $U = \{U_1, \ldots, U_r\}$ and $V = \{V_1, \ldots, V_s\}$ are two [partitions](/set-partitions/) of $X$. No distance is used. Let $n_{ij} = |U_i \cap V_j|$, $a_i = |U_i|$ and $b_j = |V_j|$. Pick an object of $X$ uniformly at random. The block of $U$ and the block of $V$ that hold it are two random variables, with the joint law $p_{ij} = n_{ij}/n$ and the marginal laws $p_i = a_i/n$ and $q_j = b_j/n$.

**Entropy and mutual information.** With the natural logarithm and $0 \log 0 = 0$,

$$H(U) = -\sum_i \frac{a_i}{n} \log \frac{a_i}{n}, \qquad I(U; V) = \sum_{i,j} \frac{n_{ij}}{n} \log \frac{n \, n_{ij}}{a_i \, b_j}.$$

Also $I(U; V) = H(U) - H(U \mid V)$, with the [conditional entropy](/conditional-entropy/) $H(U \mid V)$. The base of the logarithm cancels in every ratio below.

**The normalizations.** For a mean $M$ of $H(U)$ and $H(V)$, $\mathrm{NMI}_M = I(U; V)/M$. The four usual choices:

| name | $M$ | used by |
|---|---|---|
| sqrt | $\sqrt{H(U) H(V)}$ | Strehl and Ghosh 2002 |
| arithmetic | $(H(U) + H(V))/2$ | Manning, Raghavan and Schütze; equal to the V-measure |
| max | $\max(H(U), H(V))$ | Vinh, Epps and Bailey, as a metric-based form |
| min | $\min(H(U), H(V))$ | rarely |

Because $\min \le \sqrt{\cdot\,\cdot} \le$ arithmetic $\le \max$ for two nonnegative numbers, the values are ordered: $\mathrm{NMI}_{\max} \le \mathrm{NMI}_{\mathrm{arith}} \le \mathrm{NMI}_{\mathrm{sqrt}} \le \mathrm{NMI}_{\min}$. **The implementation uses the sqrt form by default** and accepts the other three as an option.

**Edge cases.** If both partitions have one block, both entropies are 0 and the partitions are equal; the implementation returns 1. If only the normalizer is 0, then one partition has one block, $I = 0$, and the implementation returns 0.

**Properties.**

- $0 \le I(U; V) \le \min(H(U), H(V))$, so each NMI is between 0 and 1.
- $\mathrm{NMI} = 0$ if and only if $n_{ij}/n = (a_i/n)(b_j/n)$ for all cells, that is, the table is exactly independent.
- $\mathrm{NMI}_{\mathrm{sqrt}} = 1$ if and only if $U = V$. Equality needs $I = H(U) = H(V)$, so $H(U \mid V) = H(V \mid U) = 0$, and each partition fixes the other. The same holds for the arithmetic and max forms.
- $\mathrm{NMI}_{\min} = 1$ whenever one partition refines the other, so the min form cannot tell a partition from its refinements.
- NMI is symmetric in $U$ and $V$ and does not change when the labels are renamed.

**Adjusted mutual information.** Under the permutation model (fix the block sizes and apply a uniform random permutation of $X$ to $V$), each cell $n_{ij}$ has the hypergeometric law

$$P(n_{ij} = t) = \frac{\binom{b_j}{t} \binom{n - b_j}{a_i - t}}{\binom{n}{a_i}}, \qquad \max(0, a_i + b_j - n) \le t \le \min(a_i, b_j).$$

$I$ is a sum of one term for each cell, so by [linearity of expectation](/linearity-of-expectation/),

$$E[I] = \sum_{i,j} \ \sum_{t} \frac{t}{n} \log \frac{n t}{a_i b_j} \, P(n_{ij} = t),$$

where the terms with $t = 0$ are 0. Then

$$\mathrm{AMI}_M = \frac{I(U; V) - E[I]}{M - E[I]}.$$

**The implementation uses the arithmetic mean for the AMI by default.** If the denominator is 0, it returns 1 when the partitions are equal and 0 otherwise. The inner sum has at most $\min(a_i, b_j)$ terms, so $E[I]$ costs $O(n \min(r, s))$ evaluations, and $I$ itself costs $O(n)$ with a hash map of the nonzero cells.

## Examples and non-examples

**The example of Manning, Raghavan and Schütze.** 17 objects in three classes x, o and d, and three clusters:

| | x | o | d | $a_i$ |
|---|---|---|---|---|
| cluster 1 | 5 | 1 | 0 | 6 |
| cluster 2 | 1 | 4 | 1 | 6 |
| cluster 3 | 2 | 0 | 3 | 5 |
| $b_j$ | 8 | 5 | 4 | 17 |

In nats, $I = 0.39194$, $H(\text{clusters}) = 1.09508$ and $H(\text{classes}) = 1.05510$. The four normalizations and the AMI with the same mean:

| $M$ | NMI | AMI |
|---|---|---|
| sqrt | 0.36462 | 0.2602 |
| arithmetic | 0.36456 | 0.2602 |
| max | 0.35791 | 0.2547 |
| min | 0.37147 | 0.2659 |

The expected mutual information is $E[I] = 0.15168$, so about 40% of the observed $I$ is what random clusters of the same sizes give. The arithmetic value rounds to 0.36, the number that Manning, Raghavan and Schütze report.

**NMI is not corrected for chance.** Take $n = 7$, $U = \{\{0, 1\}, \{2, 3\}, \{4, 5\}, \{6\}\}$ and $V = \{\{0\}, \{1, 2\}, \{3, 4\}, \{5, 6\}\}$. Then $I = 0.7577$, $E[I] = 0.8425$ and $\mathrm{NMI}_{\mathrm{sqrt}} = 0.5605$. The mean of $\mathrm{NMI}_{\mathrm{sqrt}}$ over all arrangements of $V$ with the same block sizes is 0.6233, which is higher. So a value of 0.56 here is worse than random, and the AMI (arithmetic) is about $-0.17$. With many small blocks, the NMI of random partitions is far from 0. For this reason NMI favors clusterings with more clusters.

**Refinements.** $U = \{\{0, 1\}, \{2, 3\}\}$ and $V = \{\{0\}, \{1\}, \{2\}, \{3\}\}$ give $I = H(U) = \log 2$ and $H(V) = \log 4$. So $\mathrm{NMI}_{\mathrm{sqrt}} = \sqrt{1/2} \approx 0.707$, but $\mathrm{NMI}_{\min} = 1$, although $U \ne V$.

**One block.** If $V$ has one block, it carries no information, $I = 0$ and the NMI is 0 for every $U$ with more than one block.

**Non-examples.**

- NMI is not the [information gain](/information-gain/) of a decision tree split, although both are mutual informations. The information gain is not normalized, and it compares a split with class labels, not two partitions.
- NMI is not a distance between partitions. The variation of information $H(U) + H(V) - 2I(U; V)$ is a metric, and $1 - \mathrm{NMI}_{\max}$ is also a metric, but $1 - \mathrm{NMI}_{\mathrm{sqrt}}$ need not be.
- NMI does not score one clustering without labels. For that, use an internal index such as the [silhouette coefficient](/silhouette-coefficient/).

## Related definitions

- [Shannon entropy](/shannon-entropy/) and [conditional entropy](/conditional-entropy/): the quantities from which $I$ is built.
- [Adjusted Rand index](/adjusted-rand-index/): the pair-counting index with the same chance correction.
- [Rand index](/rand-index/) and [cluster purity](/cluster-purity/): simpler external indices without chance correction.
- [Consensus clustering](/consensus-clustering/): Strehl and Ghosh defined the sqrt form to find the partition that shares the most information with an ensemble of partitions.
- [Cluster validity](/cluster-validity/) gives the overview of external and internal indices.

## References
