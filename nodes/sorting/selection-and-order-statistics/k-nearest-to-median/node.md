---
tag: 9ED04Z
kind: problem
slug: k-nearest-to-median
name: k numbers nearest to the median
aliases:
- k nearest neighbors to the median
area: sorting/selection-and-order-statistics
level: core
summary: Finding the k elements of a set closest in value to its median in linear time using selection.
model: comparison-model
complexity:
  vars: {n: the number of items, k: the number of items to report}
  time: {worst: Θ(n)}
prereqs: [median-finding, selection-problem]
see_also: [median-of-medians, quickselect, top-k-selection, median, deterministic-linear-selection, kth-smallest-pair-distance, binary-search, weighted-median]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 9, Section 9.3, Selection in worst-case linear time, exercises (the k numbers of a set that are closest to its median, in O(n) time)
  - paper: doi:10.1016/S0022-0000(73)80033-9
    title: Manuel Blum, Robert W. Floyd, Vaughan Pratt, Ronald L. Rivest and Robert E. Tarjan, Time bounds for selection, Journal of Computer and System Sciences 7(4) (1973)
    locator: pages 448 to 461 (linear worst-case selection, used twice by the method)
---

The problem asks, for a set of $n$ numbers and an integer $k$, for the $k$ numbers whose distance to the [median](/median/) of the set is smallest. It is a standard exercise on [selection](/selection-problem/): find the median, then select the $k$ smallest distances to it. With [median of medians](/median-of-medians/) both steps take $O(n)$ time in the worst case, so the whole problem does too, and since the median itself is always among the answers, the problem is no easier than [median finding](/median-finding/).

## In plain words

You have the heights of the people in a group, and you want the $k$ people whose height is closest to the middle height. Sorting everyone and looking around the middle works, but takes more time than needed.

Instead, first find the middle height. Then, for each person, write down how far their height is from it. Now you want the $k$ smallest of these numbers, which is again a selection: find the $k$-th smallest distance and keep everyone at most that far away.

The answer is not always the same number of people above and below the middle. If the heights are crowded on one side, all $k$ can come from that side.

## Definition

**Input.** A set $S$ of $n$ distinct real numbers and an integer $k$ with $1 \le k \le n$.

**Output.** A subset $R \subseteq S$ of size $k$ such that $|x - m| \le |y - m|$ for each $x \in R$ and each $y \in S \setminus R$, where $m$ is the lower median of $S$, the [order statistic](/order-statistic/) of rank $\lceil n/2 \rceil$.

Some numbers can be at the same distance from $m$, one above and one below. Then the set $R$ is not unique, and any choice that meets the condition is correct, unless a tie rule is given, such as "prefer the smaller number".

**Model.** The distances $|x - m|$ need subtraction, so the model is the comparison model with arithmetic on the numbers, or the real RAM. In the pure comparison model, the method of the second algorithm below avoids the subtraction in the first step.

## Variants

- **Another centre.** Replace $m$ by any given value $q$: the $k$ numbers nearest to $q$. The same method works, without the first selection.
- **Statistical median.** For even $n$ use $m = \frac{1}{2}(a_{(n/2)} + a_{(n/2+1)})$; only the first step changes.
- **Sorted input.** If the numbers are given sorted, the answer is a window of $k$ consecutive items that holds the median position, whose left end is found in $O(\log k)$ steps by [binary search](/binary-search/), or in $O(k)$ steps by growing the window one item at a time from the median.
- **Exclude the median.** Ask for the $k$ nearest numbers other than $m$ itself: select with $k + 1$ and drop $m$.
- **Weights or higher dimensions.** With weights, the centre becomes the [weighted median](/weighted-median/); with points in the plane, the problem is a $k$ nearest neighbours query.

## Examples

**Even count.** Let $S = \{31, 41, 59, 26, 53, 58, 97, 93, 23, 84\}$, so $n = 10$ and the lower median is $m = 53$. The distances to $53$ are

| $x$ | 53 | 58 | 59 | 41 | 31 | 26 | 23 | 84 | 93 | 97 |
|---|---|---|---|---|---|---|---|---|---|---|
| $\lvert x - 53 \rvert$ | 0 | 5 | 6 | 12 | 22 | 27 | 30 | 31 | 40 | 44 |

For $k = 4$, the fourth smallest distance is $12$, and the answer is $\{53, 58, 59, 41\}$: three numbers above or at $m$ and one below.

**All on one side.** Let $S = \{1, 2, 3, 4, 10, 11, 12\}$, with median $m = 4$. The distances are $0, 1, 2, 3$ for $4, 3, 2, 1$ and $6, 7, 8$ for $10, 11, 12$. For $k = 3$ the answer is $\{4, 3, 2\}$: no number above the median is in it. So the answer is not "the $\lfloor k/2 \rfloor$ items on each side of the median" in general.

**Ties.** For $S = \{1, 3, 5, 7, 9\}$, with $m = 5$, and $k = 2$, the numbers $3$ and $7$ are both at distance $2$, so $\{5, 3\}$ and $\{5, 7\}$ are both correct.

## Known algorithms

**Two selections, $O(n)$.** This is the textbook method.

1. Find the median $m$ by selection, in $O(n)$ time.
2. Make the list of pairs $(|x - m|, x)$ for $x \in S$, in $O(n)$ time.
3. Select the pair $(d, y)$ of rank $k$ among them, ordered by the first entry and then by the second, in $O(n)$ time.
4. Return each $x$ whose pair is at most $(d, y)$, in one pass.

The order on pairs breaks ties, so exactly $k$ items pass step 4. With [median of medians](/median-of-medians/) for steps 1 and 3 the worst case is $O(n)$; with [quickselect](/quickselect/) the expected time is $O(n)$ and the method is simpler and faster in practice.

**A window of ranks, $O(n)$.** An answer can always be chosen as $k$ consecutive items of the sorted order: if $x < y < z$ with $x$ and $z$ in the answer, then $|y - m| \le \max(|x - m|, |z - m|)$, so $y$ can take the place of the farther of the two. Such a window holds rank $\lceil n/2 \rceil$, so it lies inside the ranks from $\lceil n/2 \rceil - k + 1$ to $\lceil n/2 \rceil + k - 1$. Select these two boundary items and keep the at most $2k - 1$ items between them, in $O(n)$ time. Then sort these candidates in $O(k \log k)$ time and slide a window of $k$ items, or run the two-selection method on them in $O(k)$ time. This uses only comparisons for the first phase.

**Sort.** Sort $S$ and grow the window from the median: $O(n \log n)$ time.

## Bounds

- **Lower bound.** Each algorithm must read each number, so $\Omega(n)$ time is needed. For $k = 1$ the answer is the median itself, so each algorithm for this problem also finds the median, and the lower bounds of [median finding](/median-finding/), at least $(2 + 2^{-80})n - o(n)$ comparisons in the worst case, apply.
- **Upper bound.** The two-selection method makes a constant number of linear-time selections, so $O(n)$ comparisons and time in the worst case, by the [deterministic linear selection](/deterministic-linear-selection/) theorem.

## Reductions

- **To selection.** As above: the problem is two selections and two linear passes.
- **From median finding.** With $k = 1$, the output is the median.
- **To top-k selection.** Step 3 and step 4 together are [top-k selection](/top-k-selection/) on the distances.

## Applications

- **Trimmed statistics.** The items nearest to the median form a robust core of the data, used to estimate the spread or the centre without the effect of outliers.
- **Exercises in selection.** The problem is a standard example of a selection applied to derived keys, here the distances, instead of to the items themselves; the same idea solves the [k-th smallest pair distance](/kth-smallest-pair-distance/) and similar problems.

## References
