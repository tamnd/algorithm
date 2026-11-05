---
tag: KC8NBK
kind: concept
slug: presortedness
name: Measures of presortedness
aliases:
- adaptive sorting measures
area: sequences/inversions-and-permutations
level: advanced
summary: Measures such as Inv, Runs and Rem that quantify how sorted an input already is.
prereqs: [inversion, descents, longest-increasing-subsequence]
see_also: [adaptive-sorting, kendall-tau-distance, ulam-distance, cayley-distance, spearman-footrule, mahonian-numbers, eulerian-numbers, natural-merge-sort]
sources:
  - paper: "Heikki Mannila, Measures of presortedness and optimal sorting algorithms, IEEE Transactions on Computers C-34(4) (1985) 318-325"
    locator: the axioms for a measure of presortedness and the measures Inv, Runs, Rem, Exc and Max
  - paper: "Vladimir Estivill-Castro and Derick Wood, A survey of adaptive sorting algorithms, ACM Computing Surveys 24(4) (1992) 441-476"
    locator: the catalogue of measures, including Dis, Osc, SUS and Enc, and the comparison of measures
  - paper: "Christos Levcopoulos and Ola Petersson, Adaptive heapsort, Journal of Algorithms 14(3) (1993) 395-413"
    locator: the measure Osc and a heapsort that adapts to it
  - paper: "Persi Diaconis and R. L. Graham, Spearman's footrule as a measure of disarray, Journal of the Royal Statistical Society, Series B 39(2) (1977) 262-268"
    locator: the inequalities between the footrule and the number of inversions
---

A measure of presortedness is a function that assigns to every sequence of distinct keys a number saying how far it is from sorted, zero for a sorted sequence and larger for more disorder. The classic ones each count a different kind of disorder: inverted pairs (Inv), step-downs (Runs), keys that must be removed (Rem), exchanges needed (Exc), and how far an inversion or a key reaches (Dis, Max). Each depends only on the relative order of the keys, so it is a statistic of a permutation, and most of them are distances to the identity that appear elsewhere, such as the [Kendall tau](/kendall-tau-distance/), [Ulam](/ulam-distance/) and [Cayley](/cayley-distance/) distances. This page is about the measures themselves, how they relate and how they are computed; how a sort exploits them is the topic of [adaptive sorting](/adaptive-sorting/).

## In plain words

A list can be "almost sorted" in several ways. A few cards may be swapped with their neighbors. The list may be made of a few long sorted stretches. One card may be far out of place while all others are fine. Or every card may be close to where it belongs.

A measure of presortedness is a way to put a number on one of these kinds of near-order. Different measures disagree: a list made of two sorted halves in the wrong order looks nearly sorted to one measure and badly disordered to another. That is why there is no single best measure, and why each fast method for nearly sorted data is tuned to one of them.

## The idea

**The measures.** Let $X = x_1 \cdots x_n$ be distinct keys and $r_i$ the rank of $x_i$, its position in sorted order. After replacing keys by ranks, $X$ is a permutation.

- $\mathrm{Inv}(X)$, the number of [inversions](/inversion/), pairs $i < j$ with $x_i > x_j$. It is the Kendall tau distance to the sorted order and the least number of exchanges of neighbors that sort $X$.
- $\mathrm{Runs}(X)$, the number of step-downs, the [descents](/descents/) $i$ with $x_i > x_{i+1}$. The input is $\mathrm{Runs}(X) + 1$ maximal ascending runs.
- $\mathrm{Rem}(X)$, the least number of keys whose removal leaves a sorted sequence, $n - \operatorname{LIS}(X)$ with LIS the length of a [longest increasing subsequence](/longest-increasing-subsequence/). It is the Ulam distance to the sorted order.
- $\mathrm{Exc}(X)$, the least number of exchanges of any two keys that sort $X$, which is $n$ minus the number of [cycles](/permutation-cycles/) of the rank permutation. It is the Cayley distance to the sorted order.
- $\mathrm{Dis}(X)$, the largest distance $j - i$ of an inverted pair, and $\mathrm{Max}(X) = \max_i |i - r_i|$, the largest distance of a key from its place.
- $\mathrm{Ham}(X)$, the number of keys not in their place, and the [footrule](/spearman-footrule/) $D(X) = \sum_i |i - r_i|$, the total displacement.
- $\mathrm{Osc}(X)$, the oscillation of Levcopoulos and Petersson: for each key, count the adjacent pairs $x_j, x_{j+1}$ that it lies strictly between in value, and add up. In ranks this is $\sum_{j} (|r_{j+1} - r_j| - 1)$, so it is small when consecutive keys are close in value, whether the sequence goes up or down.
- $\mathrm{SUS}(X)$, the least number of ascending subsequences into which $X$ splits, which by the patience sorting argument is the length of a longest decreasing subsequence. It is 1, not 0, on a sorted input.

**Mannila's axioms.** Mannila proposed that a measure $M$ of presortedness should satisfy five conditions: (1) $M(X) = 0$ if $X$ is sorted; (2) $M(X) = M(Y)$ if $X$ and $Y$ have the same relative order; (3) $M(X) \le M(Y)$ if $X$ is a subsequence of $Y$; (4) $M(XY) \le M(X) + M(Y)$ if every key of $X$ is smaller than every key of $Y$; (5) $M(xX) \le |X| + M(X)$ for a single key $x$ placed in front. Inv, Runs, Rem, Dis and Max satisfy all five. Exc and Ham fail the third: $4\,2\,3\,1$ is sorted by one exchange and has 2 keys out of place, while its subsequence $4\,2\,3$, the pattern $3\,1\,2$, needs 2 exchanges and has 3 keys out of place. Ham also fails the fifth, since $2\,1$ has 2 keys out of place and $1$ has none.

**How the measures compare.** For every permutation:

- $\mathrm{Runs}, \mathrm{Rem}, \mathrm{Exc}, \mathrm{Dis} \le \mathrm{Inv}$. Each step-down is an inversion; deleting one key of each inverted pair leaves a sorted sequence; an exchange of neighbors is an exchange; and if $x_i > x_j$ with $j - i = d$, each key $x_k$ between them is inverted with $x_i$ or with $x_j$, which together with the pair itself gives $d$ inversions.
- $\mathrm{Runs} \le 2\,\mathrm{Rem}$, since every step-down involves a removed key and each removed key is in at most two step-downs.
- $\mathrm{Exc} \le \mathrm{Ham} \le 2\,\mathrm{Exc}$ and $\mathrm{Rem} \le \mathrm{Ham}$: a cycle of length $L \ge 2$ contributes $L - 1$ to Exc and $L$ to Ham, and the keys in their place form an increasing subsequence. So $\mathrm{Rem} \le 2\,\mathrm{Exc}$.
- $\mathrm{Max} \le \mathrm{Dis} \le 2\,\mathrm{Max}$. If keys $a > b$ sit at positions $i < j$, then $j - i < (j - r_b) + (r_a - i) \le 2\,\mathrm{Max}$.
- $\mathrm{Inv} \le D \le 2\,\mathrm{Inv}$, the inequality of Diaconis and Graham, and $\mathrm{Inv} \le n \cdot \mathrm{Dis}$, since each key is inverted with at most $\mathrm{Dis}$ keys to its right.
- $\mathrm{SUS} - 1 \le \mathrm{Runs}$ and $\mathrm{SUS} - 1 \le \mathrm{Rem}$, since the runs are ascending subsequences and a decreasing subsequence shares at most one key with an increasing one.

Other pairs are incomparable: no inequality $M_1 \le c\,M_2 + c'$ holds between Runs and Dis, Rem and Exc, or Inv and Runs, as the examples below show. This is why an algorithm that is optimal for one measure can be far from optimal for another.

**The sizes of the sets of nearly sorted inputs.** The lower bound for sorting inputs with $M(X) \le k$ is $\lg |\{X : M(X) \le k\}|$ comparisons, so the number of permutations with a given value of a measure matters. These numbers are classical: the [Mahonian numbers](/mahonian-numbers/) for Inv, the [Eulerian numbers](/eulerian-numbers/) for Runs, the [Stirling numbers](/stirling-numbers/) of the first kind for Exc, $\binom{n}{k}$ times the number of [derangements](/derangement/) of $k$ items for Ham, and the distribution of the longest increasing subsequence for Rem. The permutations with $\mathrm{Dis} \le 1$, which are products of disjoint exchanges of neighbors, are counted by the [Fibonacci numbers](/fibonacci-numbers/) $F_{n+1}$, and they are also exactly those with $\mathrm{Max} \le 1$.

**Computing the measures.** Each takes at most $O(n \log n)$ comparisons, most of it to find ranks.

- Runs in $n - 1$ comparisons by one scan.
- Inv in $O(n \log n)$ time by [merge sort](/inversion-count-by-merge-sort/) or a [Fenwick tree](/inversion-count-with-fenwick-tree/).
- Rem and SUS in $O(n \log n)$ by [patience sorting](/patience-sorting/).
- Exc, Ham, Max, $D$ and Osc in $O(n)$ time once the ranks are known, by following cycles or by one scan.
- Dis in $O(n \log n)$: the suffix minima $m_j = \min(x_j, \ldots, x_n)$ do not decrease in $j$, so the farthest key to the right of $x_i$ that is smaller than it is found by binary search over them.

## Examples

**A small input.** For $X = 3\,1\,4\,5\,2$:

| Measure | Inv | Runs | Rem | Exc | Dis | Max | Ham | $D$ | Osc | SUS |
|---|---|---|---|---|---|---|---|---|---|---|
| Value | 4 | 2 | 2 | 4 | 4 | 3 | 5 | 8 | 5 | 2 |

The inversions are $(3,1)$, $(3,2)$, $(4,2)$ and $(5,2)$; the step-downs are $3\,1$ and $5\,2$; removing $3$ and $2$ leaves $1\,4\,5$; the ranks form one 5-cycle, so 4 exchanges are needed; and the farthest inverted pair, $3$ and $2$, spans 4 positions.

**Measures that disagree.** On eight keys:

| $X$ | Inv | Runs | Rem | Exc | Dis | Max | Osc |
|---|---|---|---|---|---|---|---|
| $2\,1\,4\,3\,6\,5\,8\,7$ | 4 | 4 | 4 | 4 | 1 | 1 | 6 |
| $5\,6\,7\,8\,1\,2\,3\,4$ | 16 | 1 | 4 | 4 | 7 | 4 | 6 |
| $8\,1\,2\,3\,4\,5\,6\,7$ | 7 | 1 | 1 | 7 | 7 | 7 | 6 |
| $8\,7\,6\,5\,4\,3\,2\,1$ | 28 | 7 | 7 | 4 | 7 | 7 | 0 |

The first input has every key one place from home, so Dis and Max are 1, yet half of its gaps are step-downs. The second is two sorted runs, so Runs is 1, yet it has 16 of the 28 possible inversions. The third needs only one key moved, but its ranks form one 8-cycle. The reversed input is the worst case for Inv, Runs and Rem, but it is sorted by 4 exchanges, and Osc is 0 because consecutive keys are adjacent in value.

**Distributions for $n = 5$.** The numbers of permutations of $[5]$ with each value $0, 1, 2, \ldots$ of a measure are:

| Measure | Counts |
|---|---|
| Inv | 1, 4, 9, 15, 20, 22, 20, 15, 9, 4, 1 |
| Runs | 1, 26, 66, 26, 1 |
| Rem | 1, 16, 61, 41, 1 |
| Exc | 1, 10, 35, 50, 24 |
| Dis | 1, 7, 17, 35, 60 |
| Max | 1, 7, 23, 47, 42 |
| Ham | 1, 0, 10, 20, 45, 44 |

So 8 permutations have $\mathrm{Dis} \le 1$, which is $F_6$, and half of all 120 have $\mathrm{Dis} = 4$, the largest value, which happens exactly when the first key is larger than the last.

## Where it is used

- **Adaptive sorting.** A sort is optimal for a measure $M$ if it makes $O(n + \lg |\{Y : M(Y) \le M(X)\}|)$ comparisons on every input $X$. [Insertion sort](/insertion-sort/) runs in $O(n + \mathrm{Inv})$ time, [natural merge sort](/natural-merge-sort/) and [Timsort](/timsort/) adapt to Runs, and adaptive heapsort adapts to Osc; see [adaptive sorting](/adaptive-sorting/) for the optimality results.
- **Choosing an algorithm.** A cheap scan for Runs, or a sample estimate of Inv, tells a hybrid sort whether to merge runs, insert, or fall back to a general sort. Data with small Max, such as timestamps that arrive slightly out of order, is sorted by a window of size $\mathrm{Max}$, see [average sorting](/average-sorting/).
- **Rank correlation and data quality.** Inv normalized by $\binom{n}{2}$ is Kendall's tau, and Rem normalized by $n$ is the fraction of records that must be corrected to make a log or a column sorted. Streaming algorithms estimate both in small space for data too large to store.
- **Testing sortedness.** Property testing asks whether an array is sorted or has $\mathrm{Rem} \ge \varepsilon n$, and $O(\log n / \varepsilon)$ queries suffice to tell the two cases apart with high probability.
- **Genomes and rankings.** The same statistics, together with [breakpoints](/breakpoint-distance/), measure the disorder between two gene orders or two ranked lists.

## References
