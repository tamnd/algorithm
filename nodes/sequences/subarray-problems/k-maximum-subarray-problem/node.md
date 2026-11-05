---
tag: DZRGMB
kind: problem
slug: k-maximum-subarray-problem
name: k-maximum subarray problem
aliases:
- k disjoint maximum subarrays
area: sequences/subarray-problems
level: advanced
summary: Choose k disjoint subarrays whose total sum is maximum.
prereqs: [maximum-subarray-problem, kadane-algorithm]
see_also: [aliens-trick, min-cost-flow-problem, lagrangian-relaxation, top-k-selection, heap, segment-tree, sorted-matrix-selection, maximum-sum-submatrix]
sources:
  - url: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/
    title: LeetCode, problem 188, Best Time to Buy and Sell Stock IV
    locator: problem statement (at most k transactions, the disjoint form on daily price changes)
  - paper: doi:10.1109/tcbb.2004.43
    title: "Miklós Csűrös, Maximum-scoring segment sets, IEEE/ACM Transactions on Computational Biology and Bioinformatics 1(4) (2004), 139-150"
    locator: the disjoint form, a set of segments of largest total score, with applications to sequence analysis
  - paper: doi:10.1109/ispan.2004.1300488
    title: "Sung Eun Bae and Tadao Takaoka, Algorithms for the problem of K maximum sums and a VLSI algorithm for the K maximum subarrays problem, ISPAN 2004, 247-253"
    locator: the form with the K largest subarray sums
  - paper: doi:10.1007/s00453-006-0076-x
    title: "Fredrik Bengtsson and Jingsen Chen, Efficient Algorithms for k Maximum Sums, Algorithmica 46(1) (2006), 27-41"
    locator: the form with the k largest sums, in O(min(k + n log^2 n, n sqrt(k))) time
  - paper: doi:10.1007/978-3-540-74456-6_40
    title: "Gerth Stølting Brodal and Allan Grønlund Jørgensen, A Linear Time Algorithm for the k Maximal Sums Problem, MFCS 2007, LNCS 4708, 442-453"
    locator: the k largest sums in O(n + k) time
  - paper: doi:10.1007/978-3-540-77120-3_65
    title: "Sung Eun Bae and Tadao Takaoka, A Sub-cubic Time Algorithm for the k-Maximum Subarray Problem, ISAAC 2007, LNCS 4835, 751-762"
    locator: the two-dimensional form with the k largest sums
---

The $k$-maximum subarray problem extends the [maximum subarray problem](/maximum-subarray-problem/) from one subarray to $k$. In the form of this page, the task is to choose at most $k$ disjoint non-empty subarrays with the largest total sum. For $k = 1$ it is the maximum subarray problem, and when $k$ is at least the number of runs of positive items, the answer is the sum of all positive items. A dynamic program solves it in $O(nk)$ time, and a greedy method that merges runs with a [heap](/heap/) solves it in $O(n \log n)$ time for all $k$ at once. The best total $g(k)$ is a concave function of $k$, which allows the penalty method of the [aliens trick](/aliens-trick/). The same name also covers a second problem, the $k$ largest sums among all subarrays, which may overlap; it has an $O(n + k)$ algorithm.

## In plain words

You know the price of a stock on each day, and you may buy and sell at most $k$ times, never holding more than one share. Each trade is a stretch of days, from the day you buy to the day you sell, and its profit is the sum of the daily changes in that stretch. Trades cannot overlap. So the best plan is a choice of at most $k$ separate stretches of daily changes with the largest total.

With one trade, this is the best stretch. With many trades, you take every rising stretch. In between, you must decide which small dips to ride through and which small rises to skip.

## Definition

**Input.** An array $A[0..n-1]$ of numbers and an integer $k \ge 0$.

**Output.** The largest total
$$g(k) = \max \sum_{r=1}^{m} \sum_{t = i_r}^{j_r - 1} A[t]$$
over $m \le k$ and $0 \le i_1 < j_1 \le i_2 < j_2 \le \dots \le i_m < j_m \le n$, and one such choice of subarrays. With $m = 0$ the total is $0$, so $g(k) \ge 0$.

**Exactly $k$.** If exactly $k$ subarrays are required, with $k \le n$, the answer can be below $g(k)$, for example when all items are negative. The dynamic program below handles both forms.

**Concavity.** The increments $g(k) - g(k - 1)$ do not increase with $k$. This follows from a [min-cost flow](/min-cost-flow-problem/) model: the subarrays are $k$ units of flow along a path graph, and the cost of the cheapest flow is convex in the amount of flow.

## Variants

- **The $k$ largest sums.** List the $k$ largest values of $A[i] + \dots + A[j-1]$ over all $i < j$, with overlaps allowed. Bae and Takaoka (2004) studied it under the name "K maximum sums", Bengtsson and Chen (2006) gave $O(\min(k + n \log^2 n, n\sqrt{k}))$ time, and Brodal and Jørgensen (2007) gave $O(n + k)$ time, which is optimal. The sums are the differences $P[j] - P[i]$ of [prefix sums](/prefix-sums/), so this is a selection in a structured set of pairs, close to [sorted matrix selection](/sorted-matrix-selection/).
- **Two dimensions.** The $k$ largest rectangle sums of a matrix (Bae and Takaoka, 2007), the $k$-best form of the [maximum sum submatrix](/maximum-sum-submatrix/).
- **Range queries.** For many queries "best total of at most $k$ disjoint subarrays inside $A[l..r)$" with updates, a [segment tree](/segment-tree/) can simulate the flow method by repeated best-subarray queries and sign flips, in $O(k \log n)$ time per query.
- **Segment sets with gaps.** Csűrös (2004) studied sets of disjoint segments of largest total score, with a cost for each segment, for sequence analysis.
- **All maximal segments.** The disjoint segments that cannot be extended or merged with gain, for all $k$ at once, as in the work of Ruzzo and Tompa on maximal scoring subsequences.

## Examples

**Five values of $k$.** $A = [4, -1, 2, -5, 3, -2, 6, -7, 1]$.

| $k$ | $g(k)$ | subarrays | increment |
|---|---|---|---|
| 1 | 7 | $[3, -2, 6]$ | 7 |
| 2 | 12 | $[4, -1, 2]$, $[3, -2, 6]$ | 5 |
| 3 | 14 | $[4, -1, 2]$, $[3]$, $[6]$ | 2 |
| 4 | 15 | $[4]$, $[2]$, $[3]$, $[6]$ | 1 |
| 5 | 16 | $[4]$, $[2]$, $[3]$, $[6]$, $[1]$ | 1 |

For $k \ge 5$ the answer stays $16$, the sum of the positive items. The increments $7, 5, 2, 1, 1$ do not increase, as concavity says. For $k = 1$ the subarray $[4, -1, 2, -5, 3, -2, 6]$ also has sum $7$.

**Stock trades.** Prices $[3, 2, 6, 5, 0, 3]$ give daily changes $[-1, 4, -1, -5, 3]$. With $k = 2$ trades the best total is $4 + 3 = 7$: buy at $2$ and sell at $6$, then buy at $0$ and sell at $3$. With $k = 1$ it is $4$.

## Known algorithms

| method | time | extra space | notes |
|---|---|---|---|
| dynamic programming | $O(nk)$ | $O(k)$ | states: number of subarrays used, and whether one is open |
| greedy merging of runs | $O(n \log n)$ | $O(n)$ | gives $g(k)$ for all $k$ |
| [aliens trick](/aliens-trick/) | $O(n \log R)$ | $O(1)$ | a penalty per subarray, binary search over it; uses concavity |
| flow simulation on a segment tree | $O(k \log n)$ per query | $O(n)$ | range queries, with updates |

**Dynamic program.** Let $c_t$ be the best total of at most $t$ closed subarrays in the prefix read so far, and $o_t$ the best total with $t$ subarrays, the last one ending at the current item. For each item $x$, $o_t \leftarrow \max(o_t, c_{t-1}) + x$ and then $c_t \leftarrow \max(c_t, o_t)$.

**Greedy merging.** Merge adjacent items of the same sign into runs, so that runs alternate in sign, and drop negative runs at the two ends. Take all positive runs. While there are more than $k$ positive runs, take the run of smallest absolute value. If it lies at an end, drop it and the negative run next to it. Otherwise merge it with its two neighbors into one run with the sum of the three. Each step lowers the count of positive runs by one and costs the absolute value of the chosen run, which is the next increment of $g$. A heap and a doubly linked list of runs give $O(n \log n)$ time. On the example the steps cost $1$ (merge $4, -1, 2$), $1$ (drop the final $1$), $2$ (merge $3, -2, 6$) and $5$ (merge $5, -5, 7$).

## Bounds

**Linear time for small $k$.** Each item must be read, so $\Omega(n)$ time is needed. For a fixed $k$ the dynamic program meets this bound. The greedy method gives every $g(k)$ at once in $O(n \log n)$ time.

**The $k$ largest sums.** Writing all $k$ sums takes $\Omega(k)$ time, so the $O(n + k)$ algorithm of Brodal and Jørgensen is optimal.

## Reductions

- **From the maximum subarray problem.** The case $k = 1$, solved by [Kadane's algorithm](/kadane-algorithm/).
- **To min-cost flow.** Make a node for each gap $0, \dots, n$ between items, an edge $t \to t + 1$ of cost $-A[t]$ for flow inside a subarray, and free edges from a source to every node and from every node to a sink. A flow of $k$ units of least cost gives $-g(k)$. The successive shortest paths are the steps of the greedy method.
- **To a penalty problem.** For a penalty $\lambda \ge 0$ on each subarray, the best value of $(\text{total}) - \lambda m$ is found by a Kadane-like scan. Concavity of $g$ means that some $\lambda$ makes the best $m$ equal to $k$; see [Lagrangian relaxation](/lagrangian-relaxation/).

## Applications

- **Stock trading.** At most $k$ buy and sell trades, as in the example, on the array of daily price changes.
- **Sequence analysis.** Sets of high-scoring segments of a DNA or protein sequence, such as several separate regions with a high content of some feature (Csűrös, 2004).
- **Image analysis.** The $k$ brightest rectangles of an image in two dimensions (Bae and Takaoka).
- **Data mining.** The $k$ best ranges of a numeric attribute with respect to a score.

## References
