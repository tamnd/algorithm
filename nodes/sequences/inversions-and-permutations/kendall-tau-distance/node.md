---
tag: YXPVKF
kind: definition
slug: kendall-tau-distance
name: Kendall tau distance
aliases:
- Kendall tau
area: sequences/inversions-and-permutations
level: core
summary: Number of discordant pairs between two rankings, equal to the inversions of one relative to the other.
prereqs: [inversion, permutation-inverse]
see_also: [ranking-comparison-kendall-tau, sorting-by-adjacent-swaps, spearman-footrule, cayley-distance, ulam-distance, counting-inversions, expected-number-of-inversions, mahonian-numbers]
sources:
  - paper: "Maurice G. Kendall, A new measure of rank correlation, Biometrika 30(1/2) (1938) 81-93"
    locator: the coefficient tau defined from the numbers of concordant and discordant pairs
  - paper: "Persi Diaconis and R. L. Graham, Spearman's footrule as a measure of disarray, Journal of the Royal Statistical Society, Series B 39(2) (1977) 262-268"
    locator: the inequalities between Spearman's footrule, Kendall's distance and Cayley's distance
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.1.1 (inversions, their generating function and their distribution)
---

The Kendall tau distance between two rankings of the same $n$ items is the number of pairs of items that the two rankings put in opposite orders, the *discordant* pairs. If each item is relabeled by its position in the second ranking, the distance is the number of [inversions](/inversion/) of the relabeled first ranking, so it is computed in $O(n \log n)$ time by [counting inversions](/counting-inversions/). It equals the least number of exchanges of neighbors that turn one ranking into the other, which is the [bubble sort](/bubble-sort/) distance. Its normalized form is Kendall's rank correlation coefficient $\tau$, one of the two classic measures of agreement between rankings.

## Definition

**Rankings.** A ranking of a set $X$ of $n$ items is a list $a = (a_1, \ldots, a_n)$ of all of them, best first. Write $\operatorname{pos}_a(x)$ for the position of item $x$ in $a$, so $\operatorname{pos}_a$ is the [inverse](/permutation-inverse/) of $a$ as a map from positions to items.

**Distance.** For two rankings $a$ and $b$ of $X$,
$$K(a, b) = \big|\{\, \{x, y\} \subseteq X : (\operatorname{pos}_a(x) - \operatorname{pos}_a(y))(\operatorname{pos}_b(x) - \operatorname{pos}_b(y)) < 0 \,\}\big|,$$
the number of unordered pairs that $a$ and $b$ order differently. The other pairs are *concordant*.

**As an inversion count.** Let $w_i = \operatorname{pos}_b(a_i)$, the position in $b$ of the $i$-th item of $a$. Then $w = \operatorname{pos}_b \circ a$ is a [permutation](/permutation/) of $[n]$, and the pair of items $a_i, a_j$ with $i < j$ is discordant exactly when $w_i > w_j$. So
$$K(a, b) = \operatorname{inv}(w) = \operatorname{inv}(b^{-1} a),$$
where $a$ and $b$ are read as maps from positions to items. In particular, $K(a, \iota) = \operatorname{inv}(a)$ for a permutation $a$ of $[n]$ against the sorted order.

**As a swap distance.** $K(a, b)$ is the least number of exchanges of two adjacent entries that turn $a$ into $b$. This is the theorem of [sorting by adjacent swaps](/sorting-by-adjacent-swaps/) applied to $w$.

**Properties.**

- **A metric.** $K$ is zero only for equal rankings, symmetric, and satisfies the triangle inequality, since it is a shortest-path distance with adjacent swaps as moves.
- **Invariant under renaming items.** If both rankings rename their items by the same bijection, $K$ does not change. It is not invariant under permuting positions: moving an item from the top to the bottom of both lists can change the distance.
- **Range.** $0 \le K(a, b) \le \binom n2$, with the maximum exactly when $b$ is $a$ reversed.
- **Distribution.** For $b$ fixed and $a$ uniform, $K(a, b)$ has the distribution of the number of inversions of a uniform permutation: mean $n(n-1)/4$, variance $n(n-1)(2n+5)/72$, and $M(n, k)$ rankings at distance $k$, the [Mahonian numbers](/mahonian-numbers/). See [expected number of inversions](/expected-number-of-inversions/).

**Kendall's coefficient.** With $C$ concordant and $D = K(a, b)$ discordant pairs, $C + D = \binom n2$, and
$$\tau = \frac{C - D}{\binom n2} = 1 - \frac{4K(a, b)}{n(n-1)}.$$
It is $1$ for equal rankings, $-1$ for reversed ones, and $0$ on average for a random ranking.

## Examples and non-examples

**Two judges.** Judge 1 ranks five films $a = (A, B, C, D, E)$ and judge 2 ranks them $b = (B, E, A, C, D)$. The positions in $b$ of $A, B, C, D, E$ are $w = 3\,1\,4\,5\,2$. Its 4 inversions are the discordant pairs $\{A, B\}$, $\{A, E\}$, $\{C, E\}$ and $\{D, E\}$. So $K(a, b) = 4$ and $\tau = 1 - 16/20 = 0.2$. Four adjacent swaps turn $b$ into $a$: move $E$ down past $A$, $C$ and $D$, then exchange $B$ and $A$.

**Reversed rankings.** $K\big((1, 2, \ldots, n), (n, \ldots, 2, 1)\big) = \binom n2$ and $\tau = -1$.

**One item moved far.** Moving one item from the top to the bottom of a ranking of $n$ items creates $n - 1$ discordant pairs, one with each other item. The [Ulam distance](/ulam-distance/), which counts such moves, is 1 here.

**Non-example: positions instead of pairs.** The total displacement $\sum_x |\operatorname{pos}_a(x) - \operatorname{pos}_b(x)|$ is [Spearman's footrule](/spearman-footrule/), not Kendall's distance. For $w = 3\,1\,4\,5\,2$ it is $2 + 1 + 1 + 1 + 3 = 8$, against $K = 4$.

**Non-example: ties.** If a ranking puts two items in a tie, the pair is neither concordant nor discordant, and the definition above does not apply as it stands. The variants tau-b and tau-c of Kendall's coefficient adjust the denominator for ties; see [ranking comparison by Kendall tau](/ranking-comparison-kendall-tau/).

## Related definitions

- **[Spearman's footrule](/spearman-footrule/).** $F(a, b) = \sum_x |\operatorname{pos}_a(x) - \operatorname{pos}_b(x)|$. Diaconis and Graham proved $K + C \le F \le 2K$, where $C$ is the [Cayley distance](/cayley-distance/), so $F$ and $K$ are always within a factor 2.
- **[Cayley distance](/cayley-distance/).** The least number of exchanges of any two items, $n$ minus the number of cycles of $b^{-1}a$. It is at most $K$.
- **[Ulam distance](/ulam-distance/).** The least number of moves of a single item to another place, $n$ minus the longest common subsequence of the two rankings. It is at most $K$.
- **Spearman's rho.** The rank correlation computed from $\sum_x (\operatorname{pos}_a(x) - \operatorname{pos}_b(x))^2$, the squared version of the footrule.
- **The problem.** Computing $K$ for large $n$, with ties, partial lists and weights, is [ranking comparison by Kendall tau](/ranking-comparison-kendall-tau/).

## References
