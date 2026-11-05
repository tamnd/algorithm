---
tag: 7C8C0R
kind: definition
slug: spearman-footrule
name: Spearman's footrule
aliases:
- footrule distance
area: sequences/inversions-and-permutations
level: core
summary: Sum of absolute differences between the positions of each element in two permutations.
prereqs: [permutation, permutation-inverse]
see_also: [kendall-tau-distance, cayley-distance, ulam-distance, ranking-comparison-kendall-tau, hamming-distance, assignment-problem, presortedness, symmetric-group]
sources:
  - paper: "Persi Diaconis and R. L. Graham, Spearman's footrule as a measure of disarray, Journal of the Royal Statistical Society, Series B 39(2) (1977) 262-268"
    locator: the inequalities I + T <= D <= 2I between the footrule D, Kendall's distance I and Cayley's distance T, and the mean and variance of the footrule
  - paper: "Persi Diaconis, Group Representations in Probability and Statistics, Institute of Mathematical Statistics Lecture Notes, Monograph Series, Volume 11, 1988"
    locator: Chapter 6 (metrics on permutations, including Spearman's footrule)
  - paper: "Cynthia Dwork, Ravi Kumar, Moni Naor and D. Sivakumar, Rank aggregation methods for the Web, Proceedings of the 10th International World Wide Web Conference (2001) 613-622"
    locator: footrule-optimal aggregation by minimum-cost matching and its relation to Kemeny aggregation
---

Spearman's footrule is the total displacement between two rankings of the same $n$ items: for each item, take the difference of its positions in the two rankings, and add up the absolute values. It takes $\Theta(n)$ time to compute, much less than the $O(n \log n)$ of the [Kendall tau distance](/kendall-tau-distance/), and the two are never more than a factor 2 apart, by an inequality of Diaconis and Graham. The footrule is a metric on the [symmetric group](/symmetric-group/), always even, at most $\lfloor n^2/2 \rfloor$, and $(n^2 - 1)/3$ on average. It was proposed by Charles Spearman in 1906 as a simple measure of rank correlation.

## Definition

**Rankings.** As on the Kendall tau page, a ranking of a set $X$ of $n$ items is a list of them, best first, and $\operatorname{pos}_a(x)$ is the position of $x$ in the ranking $a$.

**Footrule.** For two rankings $a, b$ of $X$,
$$F(a, b) = \sum_{x \in X} |\operatorname{pos}_a(x) - \operatorname{pos}_b(x)|.$$
For a [permutation](/permutation/) $\pi$ of $[n]$ against the identity, $F(\pi) = \sum_{i=1}^{n} |\pi(i) - i|$, the total distance that the items must travel to reach their sorted places. In general $F(a, b) = F(w)$ for the relabeled permutation $w = \operatorname{pos}_b \circ a$, as for Kendall's distance.

**Properties.**

- **A metric.** $F$ is the $\ell_1$ distance between the position vectors $(\operatorname{pos}_a(x))_x$ and $(\operatorname{pos}_b(x))_x$, so it is a metric.
- **Invariant under renaming items**, and symmetric under inversion: $F(\pi^{-1}) = F(\pi)$, because the pairs $(i, \pi(i))$ and $(\pi(i), i)$ have the same difference.
- **Even.** $\sum_i (\pi(i) - i) = 0$, so the positive and the negative displacements have the same total, and $F(\pi) = 2 \sum_i \max(\pi(i) - i, 0)$.
- **Range.** $0 \le F \le \lfloor n^2/2 \rfloor$, with the maximum at the reversal, among others.
- **Mean.** For a uniform random $\pi$, $\mathbb{E}[F(\pi)] = (n^2 - 1)/3$. Each item $i$ lands on a uniform position $j$, and $\frac1n\sum_{j=1}^{n} |j - i|$ summed over $i$ is $\frac1n \sum_{i, j} |i - j| = \frac{1}{n} \cdot \frac{(n-1)n(n+1)}{3}$.
- **Computing it.** One pass over the items after building $\operatorname{pos}_b$, in $\Theta(n)$ time.

**The Diaconis-Graham inequality.** For every $\pi \in S_n$,
$$\operatorname{inv}(\pi) + T(\pi) \;\le\; F(\pi) \;\le\; 2\operatorname{inv}(\pi),$$
where $\operatorname{inv}$ is the Kendall distance to the identity and $T(\pi) = n - c(\pi)$ is the [Cayley distance](/cayley-distance/). The upper bound has a short proof: an adjacent exchange moves two items by one place each, so it changes $F$ by at most 2, and $\operatorname{inv}(\pi)$ adjacent exchanges sort $\pi$. So the footrule is a factor 2 approximation of the Kendall distance that takes linear time.

## Examples and non-examples

**One permutation.** For $\pi = 3\,1\,4\,5\,2$, the displacements are $2, 1, 1, 1, 3$, so $F = 8$. It has $\operatorname{inv} = 4$ and $T = 4$, so both sides of the Diaconis-Graham inequality are tight: $4 + 4 = 8 = 2 \cdot 4$.

**Two more.** $2\,4\,1\,3\,6\,5$ has displacements $1, 2, 2, 1, 1, 1$ and $F = 8$, with $\operatorname{inv} = 4$ and $T = 4$. $3\,1\,6\,2\,5\,4$ has displacements $2, 1, 3, 2, 0, 2$ and $F = 10$, with $\operatorname{inv} = 6$ and $T = 4$.

**The reversal.** $n\,(n-1) \cdots 1$ has $F = \sum_i |n + 1 - 2i| = \lfloor n^2/2 \rfloor$ and $\operatorname{inv} = \binom n2$. For $n = 5$: $4 + 2 + 0 + 2 + 4 = 12$ against 10 inversions.

**One item moved far.** Moving the top item of $n$ to the bottom gives $F = (n - 1) + (n - 1) \cdot 1 = 2(n-1)$ and $\operatorname{inv} = n - 1$, the upper end of the inequality.

**Non-example: squared differences.** $\sum_x (\operatorname{pos}_a(x) - \operatorname{pos}_b(x))^2$ is not the footrule but the statistic of Spearman's rho, $\rho = 1 - 6\sum_x d_x^2/(n(n^2 - 1))$. It is not a metric, because the square of a metric is not one in general, though its square root is the $\ell_2$ distance.

## Related definitions

- **[Kendall tau distance](/kendall-tau-distance/).** The number of discordant pairs; between $F/2$ and $F - T$ by the inequality above.
- **[Cayley distance](/cayley-distance/).** The least number of exchanges, at most $F/2$.
- **[Ulam distance](/ulam-distance/)** and **[Hamming distance](/hamming-distance/).** The least number of single-item moves, and the number of displaced items.
- **Footrule aggregation.** Given several rankings, a ranking that minimizes the sum of footrule distances to them is a minimum-cost perfect matching between items and positions, solvable by the [assignment problem](/assignment-problem/) in polynomial time. Since $F$ is within a factor 2 of Kendall's distance, it is a 2-approximation of the Kemeny ranking, which minimizes the sum of Kendall distances and is NP-hard to find. Dwork, Kumar, Naor and Sivakumar used this for rank aggregation on the Web.
- **Measures of presortedness.** $F(\pi)$, the total displacement, is one of the measures of [presortedness](/presortedness/), and it is within a factor 2 of the number of inversions.

## References
