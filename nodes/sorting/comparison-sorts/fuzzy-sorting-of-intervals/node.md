---
tag: N1ZK3Q
kind: problem
slug: fuzzy-sorting-of-intervals
name: Fuzzy sorting of intervals
area: sorting/comparison-sorts
level: advanced
summary: Sorting intervals so that for each pair there is a choice of points that respects order, solved by exploiting overlap structure of the intervals.
prereqs: [randomized-quicksort, three-way-quicksort, quicksort-expected-running-time]
see_also: [sorting-problem, topological-sort, interval-piercing, helly-property-intervals, comparison-sort-lower-bound, quicksort, las-vegas-algorithm, average-sorting]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 7 problems, Fuzzy sorting of intervals (a randomized algorithm with expected time Θ(n lg n) in general and Θ(n) when all intervals overlap), and Section 7.4.2 (the expected running time of randomized quicksort)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.2, Sorting by exchanging (quicksort and the analysis of its partitioning stages)
---

Fuzzy sorting asks for an order of $n$ closed intervals $[a_i, b_i]$ in which one can pick a point from each interval so that the points are in non-decreasing order. When the intervals are single points, this is ordinary [sorting](/sorting-problem/), so it needs $\Omega(n \log n)$ comparisons in the worst case. When all the intervals share a point, every order is valid, and an algorithm should notice this in $O(n)$ time. The problem, from CLRS Chapter 7, asks for one randomized algorithm that does both: a variant of [quicksort](/quicksort/) that takes expected $O(n \log n)$ time on every input and expected $O(n)$ time when the intervals overlap at a common point.

## In plain words

Each item is not a single number but a range of possible numbers. Put the items in a row so that you can choose one number from each range and the numbers go up from left to right.

If two ranges overlap, either one can go first. If one range ends before the other starts, it must go first. Ranges that all share a common point can go in any order among themselves, because you can choose that common point from each of them.

So the more the ranges overlap, the less sorting there is to do. A good method takes a random range, finds a point that many ranges share, and puts all the ranges that contain this point in the middle with no more work. It then sorts the ranges on each side of the point in the same way.

## Definition

**Input.** A sequence of $n$ closed intervals $I_1, \ldots, I_n$ with $I_i = [a_i, b_i]$ and $a_i \le b_i$. The endpoints come from a totally ordered set, and the algorithm can compare endpoints.

**Output.** A permutation $\sigma$ of $\{1, \ldots, n\}$ such that there are points $c_1 \le c_2 \le \cdots \le c_n$ with $c_j \in I_{\sigma(j)}$ for each $j$. Such a permutation is a **fuzzy sort** of the intervals.

**A test with no points.** A permutation $\sigma$ is a fuzzy sort if and only if

$$a_{\sigma(j)} \le b_{\sigma(l)} \qquad \text{for each } j < l.$$

*Proof.* If the points exist and $j < l$, then $a_{\sigma(j)} \le c_j \le c_l \le b_{\sigma(l)}$. Conversely, let the condition hold, and set $c_l = \max_{j \le l} a_{\sigma(j)}$. These points do not decrease. Each $c_l$ is at least $a_{\sigma(l)}$, and by the condition each term of the maximum is at most $b_{\sigma(l)}$, so $c_l \in I_{\sigma(l)}$. $\square$

In other words, write $I_i \prec I_j$ when $b_i < a_j$, so that $I_i$ lies entirely to the left of $I_j$. This relation is a strict partial order, an *interval order*, and a fuzzy sort is exactly a linear extension of it: an order in which no interval comes after an interval that lies entirely to its left.

## Variants

- **Points only.** If $a_i = b_i$ for each $i$, a fuzzy sort is a sort of the points.
- **A common point.** If $\max_i a_i \le \min_i b_i$, the intervals share the point $\max_i a_i$, and each permutation is a fuzzy sort. This is the case of CLRS where the algorithm must take expected linear time.
- **Strict order.** Asking for $c_1 < c_2 < \cdots < c_n$ gives a different problem. For example, two copies of the point interval $[1, 1]$ then have no valid order at all. This page uses $\le$.
- **A general partial order.** A fuzzy sort is a [topological sort](/topological-sort/) of the interval order. Topological sort needs the relation as a graph, which can have $\Theta(n^2)$ edges, so it is not a fast method here. The intervals give a compact form of the order, and the algorithms below use it.

## Examples

**Eight intervals.** Take

$$[5,9],\ [1,3],\ [7,8],\ [2,6],\ [10,12],\ [4,7],\ [11,11],\ [0,2].$$

Sorting by left endpoint gives $[0,2], [1,3], [2,6], [4,7], [5,9], [7,8], [10,12], [11,11]$, which is a fuzzy sort with the points $0, 1, 2, 4, 5, 7, 10, 11$. The output is not unique. The randomized algorithm below, with $[2,6]$ as its first pivot, does this:

| step | pivot | common region found | left of $t$ | contain $t$ | right of $t$ |
|---|---|---|---|---|---|
| 1 | $[2,6]$ | $[5,6]$, $t = 5$ | $[1,3], [0,2]$ | $[5,9], [2,6], [4,7]$ | $[7,8], [10,12], [11,11]$ |
| 2 (left part) | $[1,3]$ | $[1,2]$, $t = 1$ | none | $[1,3], [0,2]$ | none |
| 3 (right part) | $[10,12]$ | $[11,11]$, $t = 11$ | $[7,8]$ | $[10,12], [11,11]$ | none |

The output is $[1,3], [0,2], [5,9], [2,6], [4,7], [7,8], [10,12], [11,11]$, with the points $1, 1, 5, 5, 5, 7, 11, 11$. The three intervals of the middle group of step 1 are in their input order, and they need no comparisons among themselves.

**Points.** For $[3,3], [1,1], [2,2]$ the only fuzzy sort is $[1,1], [2,2], [3,3]$.

## Known algorithms

**Sort by left endpoints.** Sort the intervals by $a_i$ with any [comparison sort](/comparison-sort/). Then $a_{\sigma(j)} \le a_{\sigma(l)} \le b_{\sigma(l)}$ for $j < l$, so by the test above the result is a fuzzy sort. This takes $\Theta(n \log n)$ time always, even when all intervals share a point. Sorting by right endpoints works for the same reason.

**Fuzzy quicksort.** This is the randomized algorithm that the CLRS problem asks for, in the form of a [three-way quicksort](/three-way-quicksort/) on a point:

1. If there are at most 1 interval, return them.
2. Choose a pivot interval $[x, y]$ uniformly at random.
3. Scan all the intervals. For each interval $[a, b]$ that meets the current region $[x, y]$, that is, with $b \ge x$ and $a \le y$, set $x \leftarrow \max(x, a)$ and $y \leftarrow \min(y, b)$. The region stays a non-empty interval, because the two intervals meet.
4. Let $t = x$. Split the intervals into $L = \{[a,b] : b < t\}$, $M = \{[a,b] : a \le t \le b\}$ and $R = \{[a,b] : a > t\}$.
5. Return the fuzzy sort of $L$, then $M$ in any order, then the fuzzy sort of $R$.

*Correctness.* Each interval of $L$ ends before $t$, each interval of $R$ starts after $t$, and each interval of $M$ contains $t$. By induction the recursive calls return fuzzy sorts of $L$ and $R$ with points less than $t$ and greater than $t$, and the point $t$ serves for each interval of $M$. So the points do not decrease. The pivot meets the region at each step, so $t \in [x, y]$ lies in the pivot, the pivot is in $M$, and each recursive call is on fewer intervals.

*Cost.* Each call makes at most 6 endpoint comparisons for each interval: 4 in the scan and 2 in the split. With $n = 100{,}000$ intervals, the counts of endpoint comparisons were:

| intervals | comparisons | per interval |
|---|---|---|
| all contain the point 0 | 600,000 | 6.0 |
| random, of lengths 1, 10, 100 or 1000 on $[0, n]$ | 3,998,310 | 40.0 |
| pairwise disjoint | 6,279,726 | 62.8 |

For comparison, quicksort on $n$ distinct keys makes about $2 n \ln n \approx 2.3$ million comparisons for this $n$. The disjoint case is a sort with a constant factor of about 2.7 more comparisons, because each call compares each interval up to 6 times instead of once.

## Bounds

**Worst case: $\Theta(n \log n)$.** For intervals that are single distinct points, the only fuzzy sort is the sorted order, so a [decision tree](/decision-tree-model/) for fuzzy sorting must have at least $n!$ leaves, and its height is at least $\lg n! = n \lg n - O(n)$. This is the [comparison sort lower bound](/comparison-sort-lower-bound/). It also holds for the expected number of comparisons of a randomized algorithm on its worst input. Sorting by left endpoints meets it.

**Fuzzy quicksort takes expected $O(n \log n)$ time on each input.** Let $P$ be the pivot. The point $t$ lies in $P$, so $a_P \le t \le b_P$. Each interval of $R$ has $a > t \ge a_P$, so $|R|$ is at most the number of intervals whose left endpoint is greater than $a_P$. Each interval of $L$ has $b < t \le b_P$, so $|L|$ is at most the number of intervals whose right endpoint is less than $b_P$. For a uniform random pivot, each of these two counts is at most a uniform random value in $\{0, \ldots, n-1\}$. Let $T(m)$ be the largest expected cost of a call on $m$ intervals; it does not decrease in $m$. Then

$$T(n) \le c\,n + \mathbb{E}[T(|L|)] + \mathbb{E}[T(|R|)] \le c\,n + \frac{2}{n} \sum_{m=0}^{n-1} T(m),$$

which is the recurrence of [randomized quicksort](/randomized-quicksort/), with solution $T(n) = O(n \log n)$. See [the expected running time of quicksort](/quicksort-expected-running-time/).

**Fuzzy quicksort takes $\Theta(n)$ time when all intervals share a point.** Let $Z = [\max_i a_i, \min_i b_i]$ be the common part of all the intervals, and let it be non-empty. The region starts as the pivot, which contains $Z$. Each interval contains $Z$, so it meets the region, and the region becomes its intersection with the interval, which still contains $Z$. After the scan the region is the intersection of all the intervals, which is $Z$. So $t \in Z$, each interval is in $M$, and $L$ and $R$ are empty. The call makes $6n$ comparisons and returns, with no recursion. Any algorithm must look at each interval, so $\Omega(n)$ is a lower bound here.

**Between the two cases.** If the intervals form a few groups, each with a common point, the recursion ends early inside each group. The table above shows the effect: intervals that overlap in random ways cost less than disjoint intervals.

## Reductions

- **From sorting.** Sorting $n$ keys reduces to fuzzy sorting the point intervals $[x_i, x_i]$ with no extra work. So the worst-case lower bound of sorting carries over.
- **To sorting.** Fuzzy sorting reduces to sorting the left endpoints, by the test in the Definition.
- **To topological sorting.** A fuzzy sort is a [topological sort](/topological-sort/) of the interval order $b_i < a_j$. The reduction is correct but slow, because the order can have $\Theta(n^2)$ pairs.
- **Groups with a common point.** The intervals that contain one point $t$ form a group that needs no sorting. The least number of points that meet all the intervals is the [interval piercing](/interval-piercing/) number, and by the [Helly property of intervals](/helly-property-intervals/) a set of intervals that meet pairwise has a common point.

## Applications

- **Teaching.** The problem shows how to change the partition of quicksort so that its work adapts to ties, as in [three-way quicksort](/three-way-quicksort/), where keys equal to the pivot need no further work. Here the "ties" are intervals that share a point.
- **Data with measurement error.** When each value is known only up to an interval, as with timestamps from clocks with a known error bound, a fuzzy sort is an order that is consistent with some choice of true values.

## References
