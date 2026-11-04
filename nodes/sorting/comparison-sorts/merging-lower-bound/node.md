---
tag: 90H3JS
kind: theorem
slug: merging-lower-bound
name: Merging lower bound
aliases:
- Hwang-Lin merging bound
- merging sorted lists lower bound
area: sorting/comparison-sorts
level: advanced
summary: Merging sorted lists of sizes m and n needs about log2 C(m+n, n) comparisons in the worst case.
prereqs: [merging-sorted-lists, decision-tree-model, binomial-coefficient]
see_also: [comparison-sort-lower-bound, adversary-argument, merging-sorted-lists, binary-search, exponential-search, merge-sort, stirling-approximation, timsort]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.2, Minimum-comparison merging (the function M(m, n), the information bound, M(m, m) = 2m - 1 and M(m, m + 1) = 2m, the formula for M(2, n), and binary merging)
  - paper: "F. K. Hwang and S. Lin, A simple algorithm for merging two disjoint linearly ordered sets, SIAM Journal on Computing 1(1), 1972"
    locator: the binary merging algorithm and its comparison count
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Problem 8-6, Lower bound on merging sorted lists (the bound from C(2n, n) and the bound 2n - 1 from the pairs of neighbours)
---

## Statement

Let $M(m, n)$ be the least number of comparisons that an algorithm in the [decision tree model](/decision-tree-model/) needs in the worst case to [merge](/merging-sorted-lists/) a sorted list $a_1 < \cdots < a_m$ with a sorted list $b_1 < \cdots < b_n$ of distinct items. Then:

1. **The information bound.** $M(m, n) \ge \left\lceil \lg \binom{m+n}{m} \right\rceil$.
2. **The bound for lists of nearly equal length.** If $|m - n| \le 1$, then $M(m, n) = m + n - 1$, and the two-way merge is optimal.
3. **The order of the bound.** For $1 \le m \le n$,
$$m \lg\!\left(\frac{n}{m} + 1\right) \;\le\; \lg \binom{m+n}{m} \;\le\; m \lg\!\left(\frac{n}{m} + 1\right) + m \lg e,$$
so $M(m, n) = \Omega(m \log(n/m + 1))$, and binary merging (Hwang and Lin, 1972) reaches this order.

The [binomial coefficient](/binomial-coefficient/) $\binom{m+n}{m}$ counts the possible interleavings of the two lists.

## In plain words

Two sorted piles of cards must become one sorted pile. Before any comparison, many final orders are possible: each way to mix the two piles, keeping the order inside each pile, is one possible answer. Each comparison has two outcomes, so it can at best cut the number of possible answers in half. So the number of comparisons is at least the number of halvings that bring all these answers down to one.

When the two piles have about the same size, a second argument gives more. If the cards in the answer alternate between the piles, each pair of neighbours in the answer must be compared directly, or the method cannot tell their order. This needs one comparison for each pair of neighbours, which is as many as the plain merge uses.

## Proof

**Part 1.** Each correct algorithm is a decision tree. Each internal node compares some $a_i$ with some $b_j$; comparisons inside one list give no information, because their results are known. Each leaf gives one output. An input is fixed by its *interleaving*: the set of the $m$ positions of the output that hold items of the first list. All $\binom{m+n}{m}$ interleavings are possible inputs with different outputs, so each one needs its own leaf. A binary tree of height $h$ has at most $2^h$ leaves. So $2^h \ge \binom{m+n}{m}$, and the worst case $h$ is at least $\lceil \lg \binom{m+n}{m} \rceil$.

**Part 2.** The two-way merge uses at most $m + n - 1$ comparisons, because each comparison outputs one item, and the last item needs no comparison. For the lower bound, we use an [adversary argument](/adversary-argument/). The adversary fixes in advance an alternating order of all items:

- for $n = m$: $a_1 < b_1 < a_2 < b_2 < \cdots < a_m < b_m$;
- for $n = m + 1$: $b_1 < a_1 < b_2 < a_2 < \cdots < a_m < b_{m+1}$;
- for $m = n + 1$, the same with the roles of the lists exchanged.

It answers each comparison according to this order. In each case the order has $m + n$ items, and each of its $m + n - 1$ pairs of neighbours has one item from each list. Take such a pair, say $x$ directly before $y$, and suppose the algorithm stops without comparing $x$ with $y$. Exchange $x$ and $y$ in the order. The new order still has each list sorted, because $x$ and $y$ are from different lists and no item lies between them. Each comparison that the algorithm made has the same answer in the new order, because only the pair $(x, y)$ changed its relation, and it was not compared. So the algorithm cannot tell the two inputs apart, but their merged outputs differ. This is a contradiction. So the algorithm compares each of the $m + n - 1$ pairs, and it makes at least $m + n - 1$ comparisons.

**Part 3.** Write $\binom{m+n}{m} = \prod_{i=0}^{m-1} \frac{m+n-i}{m-i}$. Each factor is at least $\frac{m+n}{m}$, because $\frac{m+n-i}{m-i} \ge \frac{m+n}{m}$ is equivalent to $i \cdot n \ge 0$. So $\binom{m+n}{m} \ge \left(\frac{n}{m} + 1\right)^m$, which is the lower inequality. For the upper one, $\binom{m+n}{m} \le \frac{(m+n)^m}{m!}$ and $m! \ge (m/e)^m$, so $\binom{m+n}{m} \le \left(\frac{e(m+n)}{m}\right)^m$; taking $\lg$ gives the claim. With part 1, $M(m, n) \ge m \lg(n/m + 1)$. $\blacksquare$

## Consequences

- **Binary search is optimal.** For $m = 1$, the bound is $\lceil \lg(n+1) \rceil$, which is the number of comparisons of [binary search](/binary-search/) to find the place of one item among $n$. So $M(1, n) = \lceil \lg(n+1) \rceil$.
- **The two-way merge is optimal for equal lengths.** $M(n, n) = 2n - 1$, while the information bound is only $\lceil \lg \binom{2n}{n} \rceil = 2n - \frac{1}{2}\lg n - O(1)$. So [merge sort](/merge-sort/) with balanced merges uses the least number of comparisons for each of its merges.
- **The two-way merge is wasteful for unequal lengths.** For $m \ll n$, the bound is about $m \lg(n/m)$, much less than $m + n - 1$. So a merge of a short list into a long one should use binary merging or galloping, as [Timsort](/timsort/) does with [exponential search](/exponential-search/).
- **Set operations.** Computing the union or the intersection of two sorted sets by comparisons needs as much information as merging, so the same order $\Omega(m \log(n/m + 1))$ applies to algorithms that must find the interleaving.
- **The average case.** The information bound also holds on average over the $\binom{m+n}{m}$ equally likely interleavings: the mean depth of the leaves of a binary tree with $L$ leaves is at least $\lg L$.

## Tightness

Part 2 is exact. Part 1 is exact for $m = 1$ and for some other pairs, but not in general. The table gives $M(m, n)$ for small cases, computed by a full search over all decision trees, next to the two lower bounds.

| $m$ | $n$ | $\lceil \lg \binom{m+n}{m} \rceil$ | $m + n - 1$ | $M(m, n)$ |
|---|---|---|---|---|
| 1 | 7 | 3 | 7 | 3 |
| 2 | 4 | 4 | 5 | 5 |
| 2 | 5 | 5 | 6 | 5 |
| 2 | 8 | 6 | 9 | 6 |
| 3 | 3 | 5 | 5 | 5 |
| 3 | 5 | 6 | 7 | 7 |
| 3 | 6 | 7 | 8 | 7 |

So the information bound can be too low by one or more, as for $(2, 4)$ and $(3, 5)$, and the two-way merge can be far from optimal, as for $(1, 7)$ and $(2, 8)$. For $m = 2$, Knuth (Section 5.3.2) gives the exact formula
$$M(2, n) = \left\lceil \lg \tfrac{7}{12}(n+1) \right\rceil + \left\lceil \lg \tfrac{14}{17}(n+1) \right\rceil,$$
which agrees with the search for $2 \le n \le 8$. No closed form is known for general $m$ and $n$.

The order of part 3 is tight: the binary merging algorithm of Hwang and Lin compares the largest item of the shorter list with an item about $n/m$ places from the end of the longer list, and so outputs a whole block or places the item by binary search in it. It uses $O(m \log(n/m + 1))$ comparisons, and Knuth shows that it is close to the information bound for all $m \le n$.

## History

Knuth's Section 5.3.2 collects the results on minimum-comparison merging: the information bound, the exact values $M(m, m) = 2m - 1$ and $M(m, m+1) = 2m$ by the argument of the neighbours, the formula for $M(2, n)$, and the binary merging algorithm that Hwang and Lin published in 1972. CLRS gives both lower bounds as a problem in its chapter on sorting in linear time, as a counterpart to the [comparison sort lower bound](/comparison-sort-lower-bound/).

## References
