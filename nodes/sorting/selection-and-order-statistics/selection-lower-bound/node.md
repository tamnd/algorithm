---
tag: RST1FC
kind: theorem
slug: selection-lower-bound
name: Selection lower bound
aliases:
- adversary lower bound for selection
- median lower bound
- order statistic lower bound
area: sorting/selection-and-order-statistics
level: advanced
summary: Any comparison-based algorithm for selection needs Ω(n) comparisons in the worst case, so linear time is optimal.
prereqs: [selection-problem, adversary-argument, max-finding-lower-bound]
see_also: [second-largest-lower-bound, max-min-lower-bound, median-of-medians, deterministic-linear-selection, floyd-rivest-select, median-finding, small-order-statistics, comparison-sort-lower-bound]
sources:
  - paper: doi:10.1016/S0022-0000(73)80033-9
    title: Manuel Blum, Robert W. Floyd, Vaughan Pratt, Ronald L. Rivest and Robert E. Tarjan, Time bounds for selection, Journal of Computer and System Sciences 7(4) (1973)
    locator: pages 448 to 461 (the linear upper bound and lower bounds of the form n + min(i, n - i + 1) - 2)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.3, Minimum-comparison selection (the numbers V_t(n), their lower bounds, and the adversary arguments)
  - book: isbn:9780201612448
    title: Sara Baase and Allen Van Gelder, Computer Algorithms, Introduction to Design and Analysis, third edition
    locator: Chapter 5, Selection and adversary arguments (crucial comparisons and the lower bound 3n/2 - 3/2 for the median)
  - paper: "Samuel W. Bent and John W. John, Finding the median requires 2n comparisons, Proceedings of the 17th Annual ACM Symposium on Theory of Computing (1985)"
    locator: the lower bound 2n - o(n) for the median
  - paper: "Dorit Dor and Uri Zwick, Median selection requires (2 + epsilon)n comparisons, SIAM Journal on Discrete Mathematics 14(3) (2001)"
    locator: pages 312 to 325 (the lower bound (2 + 2^(-80))n for the median)
  - paper: "Frank Fussenegger and Harold N. Gabow, A counting approach to lower bounds for selection problems, Journal of the ACM 26(2) (1979)"
    locator: pages 227 to 238 (the bound n - k + ceil(lg C(n, k - 1)))
---

The selection lower bound says that each comparison algorithm that finds the item of rank $k$ among $n$ distinct items must make at least $n - 1 + \min(k - 1, n - k)$ comparisons in the worst case. For the median this is about $3n/2$, so the linear time of [median of medians](/median-of-medians/) is optimal up to a constant factor, and selection, unlike sorting, has no $\log n$ factor to remove. The proof has two parts: each item other than the answer must take part in a comparison of a special kind, and an [adversary](/adversary-argument/) can force about $\min(k, n - k)$ comparisons that are not of that kind.

## Statement

**Theorem.** Let $1 \le k \le n$. Each algorithm in the [comparison model](/comparison-model/) that, on each input of $n$ distinct items, returns the item of rank $k$ makes at least

$$ n - 1 + \min(k - 1, \, n - k) $$

comparisons on some input. In particular each such algorithm makes $\Omega(n)$ comparisons, and the median, with $k = \lceil n/2 \rceil$, needs at least $\lceil 3n/2 \rceil - 2$.

For $k = 1$ or $k = n$ the bound is $n - 1$, the [max-finding lower bound](/max-finding-lower-bound/). The count $\lceil 3n/2 \rceil - 2$ for the median is $n - 1 + \lceil n/2 \rceil - 1$, which is $n - 1 + \min(k - 1, n - k)$ with $k = \lceil n/2 \rceil$, for odd and even $n$.

## In plain words

To be sure that an item is the $k$-th smallest, an algorithm must have seen, for each other item, a reason why it is below or above the answer. Each such reason ends in a comparison where that item lost to something no larger than the answer, or beat something no smaller. One comparison can be this kind of reason for only one item, so there must be at least $n - 1$ of them.

On top of that, an opponent who makes up the items as the algorithm asks can make many early comparisons useless. Each time a fresh item is compared, the opponent places it far below or far above the eventual answer, so the comparison says nothing about the answer. The opponent can keep this up for about as many items as there are on the shorter side of the answer.

## Proof

Fix a correct algorithm, and run it on distinct items. Think of its comparisons as a directed graph on the items, with an edge $u \to v$ for each comparison that found $u < v$.

**Lemma 1 (each item needs a chain).** When the algorithm stops with answer $x$, for each item $y \ne x$ there is a directed path from $y$ to $x$ if $y < x$, and from $x$ to $y$ if $y > x$.

*Proof.* Let $y < x$ and assume that no path goes from $y$ to $x$. Let $R$ be the set of items that can be reached from $y$, including $y$; then $x \notin R$. Each edge with its tail in $R$ has its head in $R$, so each comparison between an item of $R$ and an item outside $R$ found the outside item smaller. Add to each item of $R$ the same large number $c$, chosen so that the items stay distinct and each item of $R$ becomes larger than each item outside $R$. All comparisons made so far keep their answers: those inside $R$ because both sides moved by $c$, and those across because the inside item was larger and is still larger. A deterministic algorithm that gets the same answers makes the same comparisons and returns the same item $x$. But now $y > x$, and no item went from above $x$ to below it, so fewer than $k - 1$ items are below $x$ and the answer is wrong. The case $y > x$ is the mirror one: subtract $c$ from each item that can reach $y$. $\square$

**Crucial comparisons.** Call a comparison between $y$ and $z$ *crucial for* $y$ if $y < z \le x$, or if $y > z \ge x$. By Lemma 1, each $y < x$ has a path $y \to z \to \cdots \to x$, and its first edge is a comparison with $y < z \le x$; each $y > x$ has a path $x \to \cdots \to z \to y$, and its last edge gives $y > z \ge x$. So each of the $n - 1$ items other than $x$ has a crucial comparison. A comparison between $u < v$ cannot be crucial for both: that would need $v \le x$ and $u \ge x$, so $x \le u < v \le x$. So the algorithm makes at least $n - 1$ crucial comparisons.

**The adversary.** It remains to force $\min(k - 1, n - k)$ comparisons that are crucial for no item. The adversary gives each item a status: N (new, not yet compared), S (small) or L (large). All items start as N. In phase 1, which lasts while fewer than $k - 1$ items are S and fewer than $n - k$ are L, it answers as follows.

| compared | answer and new status |
|---|---|
| N with N | one becomes S, the other L, and the S one is smaller |
| N with L | the N item becomes S and is smaller |
| N with S | the N item becomes L and is larger |
| two items of the same status, or S with L | the S item is smaller; inside a status, the item with the smaller index is smaller |

When phase 1 ends, the items still N stay N, and in phase 2 the adversary answers by the order "each S item, then each N item, then each L item, by index inside each group". These answers are realized by an actual input: give the S items the values $1, 2, \ldots$ in index order, then the N items the next values, then the L items. Each answer of phase 1 agrees with this input, since an item gets the status S only when it is the smaller side, and L only when it is the larger side, of a comparison with an item that is N, or of the opposite status.

Three facts about this run:

1. *Phase 1 ends, and at least one item is still N when it does.* Each comparison of phase 1 changes at most one item to S and at most one to L. So phase 1 ends with at most $k - 1$ items S and at most $n - k$ items L, and at least one of the two counts at its limit, or else the algorithm stops during phase 1. In the first case at most $n - 1$ items have a status other than N, so at least one item is N. In the second case at least three items are N and have never been compared; the answer $x$ is one item, so some other item $y$ was never compared, and has no crucial comparison, which contradicts Lemma 1.
2. *The answer is an N item, with each S item below it and each L item above it.* If $k - 1$ items are S, the item of rank $k$ is the smallest N item. If $n - k$ items are L, it is the largest N item. In both cases it was never compared in phase 1.
3. *The comparisons of phase 1 that change a status are crucial for no item.* Such a comparison is between an S item and an L item, or a new S item and an old L item, or a new L item and an old S item, and in each case the S side is below $x$ and the L side above. A comparison $s < l$ with $s < x < l$ is crucial for $s$ only if $l \le x$, and for $l$ only if $s \ge x$. Neither holds.

Each such comparison makes at most one item S and at most one item L. When phase 1 ends, either $k - 1$ items are S or $n - k$ items are L, so there were at least $\min(k - 1, n - k)$ of these comparisons. Together with the $n - 1$ crucial comparisons, which are different comparisons, the algorithm made at least $n - 1 + \min(k - 1, n - k)$ comparisons on this input. $\blacksquare$

## Consequences

- **Linear time is optimal.** Selection needs $\Omega(n)$ comparisons, so the $O(n)$ algorithms, [median of medians](/median-of-medians/), [introselect](/introselect/) and the [deterministic linear selection](/deterministic-linear-selection/) bound, are optimal up to a constant factor. Selection is easier than sorting, which needs $\Omega(n \log n)$ by the [comparison sort lower bound](/comparison-sort-lower-bound/), and the gap is the whole $\log n$ factor.
- **The median is the hardest rank for this bound.** The term $\min(k - 1, n - k)$ is largest at the median, where the bound is $\lceil 3n/2 \rceil - 2$. Near the ends it is close to $n$, which matches the cheap methods for [small order statistics](/small-order-statistics/).
- **Randomized algorithms.** The [Floyd-Rivest](/floyd-rivest-select/) method finds rank $k$ with $n + \min(k, n - k) + o(n)$ comparisons on average. Cunto and Munro showed that this is optimal on average up to the lower-order term, so for random algorithms the right answer is the same form as this bound.

## Tightness

The bound is exact for $k = 1$ and $k = n$, where it is $n - 1$, and for small cases such as the median of $3$ (three comparisons) and of $5$ (six). It is not exact in general:

- For $k = 2$ it gives $n$, while the exact value is $n + \lceil \lg n \rceil - 2$ ([second largest lower bound](/second-largest-lower-bound/)). Fussenegger and Gabow (1979) proved $n - k + \lceil \lg \binom{n}{k-1} \rceil$, which is exact for $k = 2$ and better than this bound for small $k$.
- For the median the truth lies between $(2 + 2^{-80})n - o(n)$, the lower bound of Dor and Zwick (2001), which improves the $2n - o(n)$ of Bent and John (1985), and the upper bound of fewer than $2.95n$, also by Dor and Zwick (1999).
- With repeated items the problem is not harder: the bound is stated for distinct items, which is the hardest case, since a method for any input works on distinct ones.

## History

Blum, Floyd, Pratt, Rivest and Tarjan gave lower bounds of this form, $n + \min(k, n - k + 1) - 2$ in their notation, in the 1973 paper that also gave the first linear-time selection algorithm, so the order of growth of selection was settled at once. The crucial-comparison argument used here is the textbook form of the proof, as in Baase and Van Gelder. Later work sharpened the constant for the median: Bent and John reached $2n - o(n)$ in 1985 and Dor and Zwick passed $2n$ in 2001.

## References
