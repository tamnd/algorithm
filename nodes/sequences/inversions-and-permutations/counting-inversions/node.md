---
tag: D599TE
kind: problem
slug: counting-inversions
name: Counting inversions
aliases:
- inversion counting
- inversion number
area: sequences/inversions-and-permutations
level: intro
summary: Given a sequence, count its inversions in O(n log n) time.
prereqs: [inversion, asymptotic-notation, comparison-model]
see_also: [inversion-count-by-merge-sort, inversion-count-with-fenwick-tree, kendall-tau-distance, ranking-comparison-kendall-tau, lehmer-code, dominance-counting, insertion-sort, comparison-sort-lower-bound]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 5.3 (counting inversions, the Sort-and-Count algorithm) and the exercises of Chapter 5 (significant inversions)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 2, Problem 2-4 (inversions, their relation to insertion sort, and an O(n lg n) algorithm by merge sort)
  - paper: "Timothy M. Chan and Mihai Pătraşcu, Counting inversions, offline orthogonal range counting, and related problems, Proceedings of the 21st ACM-SIAM Symposium on Discrete Algorithms (SODA 2010)"
    locator: the O(n sqrt(lg n)) word-RAM algorithm for counting inversions
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.1.1 (inversions and inversion tables)
---

Counting inversions is the problem of computing the number of [inversions](/inversion/) of a sequence, the pairs of positions $i < j$ with $a_i > a_j$. The direct method checks all $\binom n2$ pairs. Two standard methods count them in $O(n \log n)$ time: a [merge sort that counts while it merges](/inversion-count-by-merge-sort/) and a [left-to-right scan with a Fenwick tree](/inversion-count-with-fenwick-tree/). In the [comparison model](/comparison-model/) $\Omega(n \log n)$ comparisons are necessary, so these methods are optimal there. The count is the [Kendall tau distance](/kendall-tau-distance/) between two rankings, which is the usual reason to compute it.

## In plain words

You have a list of numbers. A pair of numbers is out of order when the bigger one comes first. You want to know how many such pairs the list has. A sorted list has none. A list sorted backwards has every pair out of order.

Checking every pair works, but for a million numbers that is half a million million checks. The fast methods do much less. One splits the list in two halves, counts each half, and then counts the pairs that cross the middle while it merges the two sorted halves. The other walks along the list and keeps a tally of the numbers already seen, so it can ask at each step how many earlier numbers are bigger than the current one.

## Definition

**Input.** A sequence $a = (a_1, \ldots, a_n)$ of items from a [total order](/total-order/).

**Output.** The number

$$\operatorname{inv}(a) = \big|\{(i, j) : 1 \le i < j \le n,\ a_i > a_j\}\big|,$$

an integer between $0$ and $\binom n2$.

The output needs $O(\log n)$ bits, so it is not the bottleneck. In code, use a 64-bit counter: for $n = 10^5$ the answer can be $\binom{10^5}{2} = 4\,999\,950\,000$, which does not fit in 32 bits.

## Variants

- **Per-item counts.** For each $i$, output $c_i = |\{j > i : a_j < a_i\}|$, the number of smaller items to the right. For a permutation this is its [Lehmer code](/lehmer-code/). The sum of the $c_i$ is $\operatorname{inv}(a)$. Both standard algorithms produce these counts at no extra asymptotic cost.
- **Inversions between two rankings.** Given two orders of the same $n$ items, count the pairs that they order differently. This is the [Kendall tau distance](/kendall-tau-distance/), and the [ranking comparison](/ranking-comparison-kendall-tau/) problem reduces it to counting inversions.
- **Significant inversions.** Count the pairs $i < j$ with $a_i > 2a_j$, or more generally $a_i > c \cdot a_j$. The merge sort method still works, with a separate pass over the two halves before each merge. Kleinberg and Tardos give this as an exercise of Chapter 5.
- **Parity only.** For a [permutation](/permutation/) of $[n]$, the parity of $\operatorname{inv}(\pi)$ equals the parity of $n$ minus the number of [cycles](/permutation-cycles/). This takes $O(n)$ time, because it uses the values as array indices and so leaves the comparison model.
- **Dynamic counting.** Maintain $\operatorname{inv}(a)$ while items are inserted, deleted or changed. With an [order-statistic tree](/order-statistic-tree/), each insertion at the end of the sequence costs $O(\log n)$.
- **Approximate and streaming counting.** Estimate $\operatorname{inv}(a)$ within a factor $1 \pm \varepsilon$, possibly in one pass with little memory. Ajtai, Jayram, Kumar and Sivakumar studied this in the data stream model in 2002.

## Examples

| sequence | inversions | per-item counts $c_i$ |
| --- | --- | --- |
| $(2, 4, 1, 3, 5)$ | 3 | $1, 2, 0, 0, 0$ |
| $(3, 1, 2)$ | 2 | $2, 0, 0$ |
| $(8, 4, 2, 1)$ | 6 | $3, 2, 1, 0$ |
| $(1, 20, 6, 4, 5)$ | 5 | $0, 3, 2, 0, 0$ |
| $(7, 5, 3, 1, 8, 6, 4, 2)$ | 18 | $6, 4, 2, 0, 3, 2, 1, 0$ |

The first row is the example of Kleinberg and Tardos: its inversions are the pairs of values $(2, 1)$, $(4, 1)$ and $(4, 3)$. The row $(8, 4, 2, 1)$ is decreasing, so all $\binom 42 = 6$ pairs are inversions. The last sequence has 8 significant inversions with $a_i > 2a_j$, for example $(7, 3)$ but not $(5, 3)$.

## Known algorithms

| algorithm | time | model | note |
| --- | --- | --- | --- |
| check all pairs | $\Theta(n^2)$ | comparison | two nested loops |
| [insertion sort](/insertion-sort/), counting shifts | $\Theta(n + \operatorname{inv}(a))$ | comparison | fast only when the count is small |
| [merge sort count](/inversion-count-by-merge-sort/) | $\Theta(n \log n)$ | comparison | also sorts the input |
| [Fenwick tree count](/inversion-count-with-fenwick-tree/) | $O(n \log n)$ | word RAM | values $1$ to $n$, or after [coordinate compression](/coordinate-compression/) |
| [order-statistic tree](/order-statistic-tree/) scan | $O(n \log n)$ | comparison | online: gives the count of each prefix |
| Chan and Pătraşcu (2010) | $O(n \sqrt{\log n})$ | word RAM | integer keys |

## Bounds

**Upper bound.** $O(n \log n)$ comparisons in the worst case, by the merge sort method.

**Lower bound in the comparison model.** Each comparison-based algorithm that counts inversions makes $\Omega(n \log n)$ comparisons in the worst case, in fact at least $\lceil \lg n! \rceil$.

*Proof.* Fix a correct algorithm and an input permutation $\pi$ of distinct keys. Let $u$ and $v$ be two items whose values are consecutive in sorted order. Suppose the algorithm never compares $u$ with $v$ on input $\pi$. Let $\pi'$ be the input with $u$ and $v$ exchanged. Every other item $w$ is smaller than both or larger than both, so each comparison that the run on $\pi$ makes has the same answer on $\pi'$. The run on $\pi'$ is the same run, with the same output. But no item between the positions of $u$ and $v$ has a value between theirs, so by fact 4 of the [inversion](/inversion/) page, $\operatorname{inv}(\pi') = \operatorname{inv}(\pi) \pm 1$. One of the two outputs is wrong, a contradiction. So on each input the algorithm compares each pair of consecutive values, and the answers to those $n - 1$ comparisons fix the sorted order. Two different permutations therefore end in different leaves of the [decision tree](/comparison-sort-lower-bound/), the tree has at least $n!$ leaves, and its height is at least $\lg n! = n \lg n - O(n)$. $\square$

The argument shows more: an algorithm that counts inversions by comparisons can also sort, at no extra comparisons.

**Word RAM.** When the keys are integers that fit in a machine word, the lower bound above does not apply. Dietz (1989) gave $O(n \log n / \log \log n)$ time, and Chan and Pătraşcu (2010) gave $O(n \sqrt{\log n})$ time. Whether $O(n)$ time is possible is open.

## Reductions

- **Kendall tau to inversions.** Two rankings $\sigma, \tau$ of $n$ items give the sequence $\tau^{-1} \circ \sigma$ in $O(n)$ time, and its inversion count is their distance. See [ranking comparison by Kendall tau](/ranking-comparison-kendall-tau/).
- **Inversions to dominance counting.** The inversions of $a$ are the pairs of points $(i, a_i)$, $(j, a_j)$ with $i < j$ and $a_i > a_j$, so counting them is an offline [dominance counting](/dominance-counting/) problem in the plane with $n$ points. Chan and Pătraşcu solve both with the same method.
- **Sorting to inversions, in comparisons.** The lower bound proof shows that the comparisons of an inversion counter determine the sorted order.

## Applications

- **Comparing rankings.** Collaborative filtering and the evaluation of search results compare two rankings by the number of pairs on which they disagree. Kleinberg and Tardos open Section 5.3 with this use.
- **Running time of simple sorts.** [Insertion sort](/insertion-sort/) makes exactly $\operatorname{inv}(a)$ shifts and [bubble sort](/bubble-sort/) exactly $\operatorname{inv}(a)$ exchanges. The count predicts their cost, and the [minimum number of adjacent swaps](/sorting-by-adjacent-swaps/) to sort a sequence is $\operatorname{inv}(a)$.
- **Measuring presortedness.** $\operatorname{inv}$ is one of the standard [measures of presortedness](/presortedness/) used to state the cost of [adaptive sorts](/adaptive-sorting/).
- **Puzzles.** For the 15 puzzle, the parity of the inversions of the tiles, together with the row of the blank, decides whether a position can be solved.
- **Statistics.** Kendall's rank correlation $\tau = 1 - 4\operatorname{inv}/(n(n-1))$ tests whether two variables are related, and its computation is an inversion count.

## References
