---
tag: HJZS27
kind: concept
slug: optimality
name: Algorithm optimality
aliases:
- optimal algorithm
- tight bound
area: foundations/lower-bounds
level: intro
summary: An algorithm is optimal when its cost matches a lower bound up to constant factors.
prereqs: [upper-bound, lower-bound, asymptotic-notation]
see_also: [asymptotic-optimality, merge-sort-optimality, max-finding-lower-bound, max-min-lower-bound, sorted-search-lower-bound, comparison-sort-lower-bound, ford-johnson-algorithm, tilde-notation]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 8.1 (Theorem 8.1 and Corollary 8.2, heapsort and merge sort are asymptotically optimal comparison sorts) and Section 9.1 (minimum and maximum)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.1 (the least worst-case number of comparisons S(n) and merge insertion) and Section 5.3.3 (minimum-comparison selection)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 2.2, Asymptotic Order of Growth (asymptotically tight bounds)
  - paper: "Ronald Fagin, Amnon Lotem and Moni Naor, Optimal aggregation algorithms for middleware, Journal of Computer and System Sciences 66(4) (2003)"
    locator: pp. 614 to 656 (the definition of instance optimality and the threshold algorithm)
  - paper: "Peyman Afshani, Jeremy Barbay and Timothy M. Chan, Instance-optimal geometric algorithms, Journal of the ACM 64(1) (2017)"
    locator: article 3 (instance optimality in the order-oblivious sense, convex hull in two and three dimensions)
  - paper: "Bernhard Haeupler, Richard Hladik, Vaclav Rozhon, Robert E. Tarjan and Jakub Tetek, Universal optimality of Dijkstra via beyond-worst-case heaps, 65th IEEE Symposium on Foundations of Computer Science (FOCS 2024)"
    locator: the main theorem (Dijkstra's algorithm with a suitable heap is universally optimal for ordering vertices by distance)
---

An algorithm is optimal for a problem when its cost meets a [lower bound](/lower-bound/) for that problem: no algorithm of the same [model](/comparison-model/), measured by the same cost and in the same case, can do better. The match can be exact, up to lower-order terms, or up to a constant factor, and the claim must say which. The last and weakest form is [asymptotic optimality](/asymptotic-optimality/), and it is what most textbooks mean by "optimal". A matching pair of an [upper bound](/upper-bound/) and a lower bound is called a tight bound.

## In plain words

A problem has a true cost: the least work that the best possible method needs on its worst input. Nobody knows this number for most problems. We know a ceiling, from the best method found so far, and a floor, from a proof that no method can do better. An algorithm is optimal when its cost reaches the floor, so the ceiling and the floor meet.

They can meet in different ways. Sometimes they meet exactly, to the last comparison: finding the largest item takes exactly one comparison less than the number of items. Sometimes they meet only in the leading term, and the methods differ by a smaller amount. Sometimes they meet only up to a fixed factor. Each claim of optimality also fixes the allowed steps, the thing that is counted, and whether it speaks of the worst input or the average one.

## The idea

Fix a problem $P$, a model $M$, a cost measure and a case. Let $W_A(n)$ be the cost of an algorithm $A$ on inputs of size $n$ in that case (worst, average or expected), and let

$$C_P(n) = \min_{B} W_B(n),$$

the minimum over all algorithms $B$ of $M$ that solve $P$. This is the complexity of $P$ in $M$. Each algorithm gives an upper bound $C_P(n) \le W_A(n)$, and each lower bound $L$ gives $C_P(n) \ge L(n)$. There are four levels of optimality, from strong to weak.

1. **Exactly optimal.** $W_A(n) = C_P(n)$ for each $n$. To prove this one needs a lower bound $L$ with $L(n) = W_A(n)$. Example: the scan for the maximum, with $W_A(n) = C_P(n) = n - 1$.
2. **Optimal up to lower-order terms.** $W_A(n) \sim C_P(n)$, that is $W_A(n)/C_P(n) \to 1$ (see [tilde notation](/tilde-notation/)). It is enough to show $W_A(n) \sim L(n)$ for a lower bound $L$. Example: [merge sort](/merge-sort/) makes $n \lg n - \Theta(n)$ comparisons, and every sort needs $\lceil \lg(n!) \rceil = n \lg n - \Theta(n)$. See [merge sort optimality](/merge-sort-optimality/).
3. **Asymptotically optimal.** $W_A(n) = \Theta(C_P(n))$, that is $W_A(n) = O(L(n))$ for a lower bound $L$. Example: [heapsort](/heapsort/) makes at most about $2 n \lg n$ comparisons, which is $O(n \log n)$, and so it is asymptotically optimal but not optimal in the sense of level 2. See [asymptotic optimality](/asymptotic-optimality/).
4. **Optimal in another case.** The same three levels apply to the average over a distribution, or to the expected cost of a randomized algorithm. [Quicksort](/quicksort/) is asymptotically optimal on average over random orders, with about $1.39\,n \lg n$ comparisons, but not in the worst case, where it makes $n(n-1)/2$.

Level 1 implies level 2, and level 2 implies level 3, when $C_P(n) > 0$. The converses are false, as the examples show.

**Optimal on each input.** The strongest wish is an algorithm that is best on every input, not only on the worst one. Let $c^*(x) = \min_B \mathrm{cost}_B(x)$. For finding the maximum, every correct algorithm makes at least $n - 1$ comparisons on **each** input ([maximum finding lower bound](/max-finding-lower-bound/)), so the scan is optimal on each input. For sorting this wish is impossible. For each order $\pi$ of $n$ items, the algorithm "test whether the input is in order $\pi$ with $n - 1$ comparisons; if not, run merge sort" makes $n - 1$ comparisons on inputs in order $\pi$. So $c^*(x) = n - 1$ for every input $x$, but no single algorithm makes $n - 1$ comparisons on every input, since some input needs $\lceil \lg(n!) \rceil$. Useful versions of this idea weaken it:

- **Instance optimality** (Fagin, Lotem and Naor, 2003): $\mathrm{cost}_A(x) \le c \cdot \mathrm{cost}_B(x) + c'$ for each algorithm $B$ in a stated class and each input $x$, with constants $c$ and $c'$. Their threshold algorithm for top-$k$ queries is instance optimal in this sense. Afshani, Barbay and Chan (2017) use an order-oblivious version, which compares $A$ with each $B$ on the worst order of the same set of points, and give instance-optimal convex hull algorithms in two and three dimensions.
- **Universal optimality**: optimal, up to a constant factor, on the worst input among those with the same structure, such as the same graph with any edge weights. Haeupler, Hladík, Rozhoň, Tarjan and Tětek (2024) proved that [Dijkstra's algorithm](/dijkstra/) with a suitable heap is universally optimal for ordering the vertices by distance.

**What optimality does not say.**

- It does not compare models. An algorithm that is optimal among comparison sorts is beaten by [radix sort](/radix-sort/) on small integers on the [word RAM](/word-ram/).
- It does not compare resources. Merge sort is optimal in comparisons up to lower-order terms and uses $\Theta(n)$ extra memory. Heapsort is only asymptotically optimal in comparisons and uses $O(1)$ extra memory. Neither is better in both.
- It does not say that the algorithm is fast in practice. The constants and the memory access pattern decide that.

## Examples

All rows are in the [comparison model](/comparison-model/), in the worst case, for $n$ distinct items. The value is for $n = 8$, except in the second last row.

| problem | algorithm | its cost | lower bound | value at $n = 8$ | level |
|---|---|---|---|---|---|
| maximum | scan | $n - 1$ | $n - 1$ | 7 and 7 | exact |
| maximum and minimum | compare in pairs | $\lceil 3n/2 \rceil - 2$ | the same | 10 and 10 | exact |
| second largest | tournament | $n + \lceil \lg n \rceil - 2$ | the same | 9 and 9 | exact |
| search in a sorted array | binary search | $\lceil \lg(n+1) \rceil$ | the same | 4 and 4 | exact |
| merge two lists of $n/2$ | standard merge | $n - 1$ | $n - 1$ | 7 and 7 | exact |
| sorting, $n = 12$ | merge insertion | 30 | $\lceil \lg(12!) \rceil = 29$, true value 30 | 30 and 30 | exact at $n = 12$ |
| sorting | merge sort | $n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + 1$ | $\lceil \lg(n!) \rceil$ | 17 and 16 | lower-order terms |

Rows one to five have their own pages: the [maximum](/max-finding-lower-bound/), the [maximum and minimum](/max-min-lower-bound/), the [second largest](/second-largest-lower-bound/), [sorted search](/sorted-search-lower-bound/) and [merging](/merging-lower-bound/). For sorting, the lower bound $\lceil \lg(n!) \rceil$ is not always reached, so exact optimality needs the true value $C_P(n)$, and that is known only for small $n$. Wells found $C_P(12) = 30$ by a computer search, while the bound gives 29 (Knuth, Section 5.3.1). The [merge insertion](/ford-johnson-algorithm/) algorithm of Ford and Johnson reaches $C_P(n)$ for each $n \le 12$.

The two sorting algorithms of the last rows compare as follows.

| $n$ | $\lceil \lg(n!) \rceil$ | merge insertion | merge sort | merge sort minus bound |
|---|---|---|---|---|
| 4 | 5 | 5 | 5 | 0 |
| 5 | 7 | 7 | 8 | 1 |
| 10 | 22 | 22 | 25 | 3 |
| 100 | 525 | 534 | 573 | 48 |
| 1000 | 8530 | 8641 | 8977 | 447 |

The ratio of merge sort to the bound is $1.091$ at $n = 100$ and $1.052$ at $n = 1000$, and it tends to 1. The difference grows linearly. So merge sort is optimal at level 2 and not at level 1.

### Pitfalls

- **"Optimal" without a level.** "Heapsort is optimal" and "the scan is optimal" mean different things. Say "asymptotically optimal" or "exactly optimal".
- **An upper bound only.** An algorithm with cost $O(n \log n)$ is not optimal until someone proves a lower bound of $\Omega(n \log n)$ for the problem in the same model.
- **The wrong case.** A worst-case lower bound does not show that an algorithm is optimal on average, and an average-case result does not show worst-case optimality.
- **A tight bound for an algorithm is not optimality.** "The running time of insertion sort is $\Theta(n^2)$" is a tight bound on one algorithm. It is not a statement about the problem.
- **Optimal on each input.** For most problems no algorithm is best on every input. Use instance optimality with its exact definition, or the worst case.

## Where it is used

- **Closing a problem.** When an algorithm is optimal, research on faster algorithms in that model ends, and work moves to constants, memory, parallel time or other models.
- **Choosing between algorithms.** Among optimal algorithms the choice depends on the resources that the claim does not cover: memory, stability, cache behaviour.
- **Exact optimality in small cases.** Sorting networks, small sorting routines in libraries and tournaments use exact values for small $n$, often found by computer search.
- **Beyond the worst case.** Instance and universal optimality explain why adaptive algorithms, such as natural merge sort on presorted data or output-sensitive convex hull algorithms, beat the worst-case bound on easy inputs.

## References
