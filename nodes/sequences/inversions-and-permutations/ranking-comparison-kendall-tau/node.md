---
tag: HV184N
kind: problem
slug: ranking-comparison-kendall-tau
name: Ranking comparison by Kendall tau distance
aliases:
- Collaborative filtering / rankings comparison
area: sequences/inversions-and-permutations
level: core
summary: Measures how different two rankings of the same items are by counting the pairs ordered oppositely, computed with inversion counting in O(n log n) time.
prereqs: [kendall-tau-distance, counting-inversions]
see_also: [inversion-count-by-merge-sort, inversion-count-with-fenwick-tree, spearman-footrule, sorting-by-adjacent-swaps, expected-number-of-inversions, ulam-distance, cayley-distance, assignment-problem]
sources:
  - paper: "William R. Knight, A computer method for calculating Kendall's tau with ungrouped data, Journal of the American Statistical Association 61(314) (1966) 436-439"
    locator: the O(n log n) method that sorts by one variable and counts exchanges in a merge sort of the other, with ties
  - paper: "Maurice G. Kendall, The treatment of ties in ranking problems, Biometrika 33(3) (1945) 239-251"
    locator: the coefficient tau-b corrected for ties
  - paper: "Ronald Fagin, Ravi Kumar and D. Sivakumar, Comparing top k lists, SIAM Journal on Discrete Mathematics 17(1) (2003) 134-160"
    locator: Kendall distances with a penalty parameter for top k lists, and their equivalence classes
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 5.3 (counting inversions as a measure of the similarity of two rankings)
---

Ranking comparison by Kendall tau asks how much two rankings of the same items disagree, measured by the number of pairs of items that they put in opposite orders, the [Kendall tau distance](/kendall-tau-distance/). After the items are relabeled by their positions in one ranking, the answer is the inversion count of the other, so the problem is [counting inversions](/counting-inversions/) and takes $\Theta(n \log n)$ comparisons. With scores instead of rankings, ties appear, and Knight's method of 1966 computes the tie-corrected coefficients in the same time by one sort and one merge sort. The same count is used to compare search results, recommendations, and the outputs of two statistical variables.

## In plain words

Two friends each rank the same ten films. How much do they disagree? Look at every pair of films. If one friend prefers the first film and the other prefers the second, the pair is a disagreement. Count the disagreements.

Checking every pair one by one is slow for long lists. A faster way is to write the films in the order of the first friend, and under each film write its place in the list of the second friend. A disagreement is now a pair of these places that is out of order, and such pairs can be counted while sorting, as merge sort does.

If the lists have ties, for example two films with the same score, those pairs are neither agreements nor disagreements, and the count has to leave them out.

## Definition

**Input.** Two rankings $a$ and $b$ of the same $n$ items, or more generally $n$ pairs of scores $(x_1, y_1), \ldots, (x_n, y_n)$ from two [total orders](/total-order/), one pair per item.

**Pairs.** For $i < j$ the pair is *concordant* if $(x_i - x_j)(y_i - y_j) > 0$, *discordant* if it is $< 0$, and *tied* if $x_i = x_j$ or $y_i = y_j$.

**Output.** The number $D$ of discordant pairs, which is the Kendall tau distance when there are no ties, and usually also the number $C$ of concordant pairs and one of the coefficients below. With $n_0 = \binom n2$, $n_1$ the number of pairs tied in $x$, $n_2$ the number tied in $y$, and $n_3$ the number tied in both,

$$\tau_a = \frac{C - D}{n_0}, \qquad \tau_b = \frac{C - D}{\sqrt{(n_0 - n_1)(n_0 - n_2)}}, \qquad C + D = n_0 - n_1 - n_2 + n_3.$$

Without ties, $n_1 = n_2 = n_3 = 0$, $C + D = n_0$, and $\tau_a = \tau_b = 1 - 2D/n_0$.

## Variants

- **Permutations.** If $a$ is a permutation of $[n]$ and $b$ is the identity, $D = \operatorname{inv}(a)$, the [inversion](/inversion/) count.
- **Ties.** The coefficient $\tau_b$ of Kendall corrects for ties in both rankings. A further variant $\tau_c$, due to Stuart, is meant for contingency tables with unequal numbers of rows and columns.
- **Top-$k$ lists.** Search engines return only the first $k$ items, and two top-$k$ lists may contain different items. Fagin, Kumar and Sivakumar define a Kendall distance with a penalty $p \in [0, 1]$ for a pair whose order is not determined by the lists, and show which of these distances are metrics.
- **Weighted versions.** Disagreements near the top of the lists can be weighted more than those near the bottom. For weights that are products or sums of weights of the two items, the weighted count still takes $O(n \log n)$ time by a merge sort that carries sums of weights.
- **Swap distance.** The least number of adjacent exchanges that turn $a$ into $b$ is $D$, by [sorting by adjacent swaps](/sorting-by-adjacent-swaps/).
- **Many rankings.** Given $m$ rankings, the Kemeny problem asks for a ranking with the least sum of Kendall distances to them. It is NP-hard already for 4 rankings, and the [footrule](/spearman-footrule/) aggregation gives a 2-approximation.

## Examples

**Two rankings.** $a = (A, B, C, D, E)$ and $b = (B, E, A, C, D)$. Writing the position in $b$ under each item of $a$ gives $3\,1\,4\,5\,2$, with 4 inversions. So $D = 4$, $C = 6$ and $\tau = (6 - 4)/10 = 0.2$. The discordant pairs are $\{A, B\}$, $\{A, E\}$, $\{C, E\}$ and $\{D, E\}$.

**Scores with ties.** Six items have the scores

| item | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | 1 | 2 | 2 | 3 | 4 | 5 |
| $y$ | 2 | 1 | 3 | 3 | 5 | 4 |

Of the 15 pairs, $\{2, 3\}$ is tied in $x$, $\{3, 4\}$ is tied in $y$, the pairs $\{1, 2\}$ and $\{5, 6\}$ are discordant, and the other 11 are concordant. So $n_1 = n_2 = 1$, $n_3 = 0$, $\tau_a = 9/15 = 0.6$ and $\tau_b = 9/\sqrt{14 \cdot 14} = 9/14 \approx 0.643$.

**Extremes.** Equal rankings give $D = 0$ and $\tau = 1$. Reversed rankings give $D = \binom n2$ and $\tau = -1$. For two independent uniform rankings, $D$ has mean $n(n-1)/4$ and variance $n(n-1)(2n+5)/72$, by the [expected number of inversions](/expected-number-of-inversions/), which is the basis of the test of independence based on $\tau$.

## Known algorithms

- **All pairs.** Check every pair in $\Theta(n^2)$ time. Simple and fine for small $n$.
- **Relabel and count inversions.** Build the position map of $b$, write the positions under the items of $a$, and count inversions with the [merge sort method](/inversion-count-by-merge-sort/) or the [Fenwick tree method](/inversion-count-with-fenwick-tree/), in $O(n \log n)$ time.
- **Knight's method with ties.** Sort the items by $x$, breaking ties in $x$ by $y$. Then count the strict inversions of the resulting $y$ sequence by merge sort. Within a group tied in $x$ the $y$ values are sorted, so no tied pair is counted, and every strict inversion is a discordant pair. The tie counts $n_1$, $n_2$ and $n_3$ come from the runs of equal values in the sorted orders, and $C = n_0 - n_1 - n_2 + n_3 - D$. The total time is $O(n \log n)$.
- **Word RAM.** For integer ranks, faster inversion counting gives $O(n \sqrt{\log n})$ time, see [counting inversions](/counting-inversions/).
- **Approximation in linear time.** [Spearman's footrule](/spearman-footrule/) is computed in $O(n)$ time and lies between $D$ and $2D$ for rankings without ties.

## Bounds

- **Comparisons.** $\Theta(n \log n)$ comparisons are necessary and sufficient in the [comparison model](/comparison-model/), because the problem contains counting inversions, whose lower bound is proved on the [counting inversions](/counting-inversions/) page.
- **Range.** $0 \le D \le \binom n2$, and $-1 \le \tau_a, \tau_b \le 1$.
- **Output size.** The count can reach $\binom n2$, so a signed 32-bit counter overflows from $n = 65{,}537$ and an unsigned one from $n = 92{,}683$.

## Reductions

- **To counting inversions.** Relabel by the positions in one ranking in $O(n)$ time, then count the inversions of the result.
- **From counting inversions.** The inversion count of a permutation $a$ is the Kendall distance between $a$ and the sorted order, so the two problems are equivalent up to $O(n)$ work.
- **With ties, to strict inversions.** Knight's sort by $(x, y)$ turns the tie-aware count into a strict inversion count on one sequence.
- **To dominance counting.** Each discordant pair is a pair of points $(x_i, y_i)$, $(x_j, y_j)$ in which one is above-left of the other, so $D$ is a two-dimensional dominance count.

## Applications

- **Statistics.** Kendall's $\tau$ measures the association of two variables without assuming a linear relation, and its distribution under independence gives a rank test.
- **Search and recommendation.** Comparing the rankings of two search engines, two versions of a ranking model, or a model and a human judge, often with top-$k$ and weighted variants.
- **Collaborative filtering.** Two users are similar when their rankings of the same items have a small Kendall distance, which is the motivating example of the counting inversions problem in Kleinberg and Tardos.
- **Rank aggregation.** Voting and meta-search combine several rankings into one, using the Kendall distance as the measure of disagreement.
- **Sorting analysis.** The distance between the input order and the sorted order is the number of adjacent exchanges that bubble sort or insertion sort makes.

## References
