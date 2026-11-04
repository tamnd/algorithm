---
tag: 8E0M7X
kind: problem
slug: multiple-selection
name: Multiple selection
aliases:
- multiselection
- batch selection
area: sorting/selection-and-order-statistics
level: advanced
summary: Find the order statistics for several ranks k1 < ... < km in one computation.
model: comparison-model
complexity:
  vars: {n: the number of items, m: the number of ranks}
  time: {worst: Θ(n log m)}
prereqs: [selection-problem, quantile]
see_also: [selection-problem, quantile, quickselect, median-of-medians, partial-sorting, sample-sort, floyd-rivest-select, comparison-sort-lower-bound]
sources:
  - paper: "David P. Dobkin and J. Ian Munro, Optimal time minimal space selection algorithms, Journal of the ACM 28(3) (1981)"
    locator: pages 454 to 461 (multiple selection and the information-theoretic lower bound)
  - paper: doi:10.1007/11523468_9
    title: Kanela Kaligosi, Kurt Mehlhorn, J. Ian Munro and Peter Sanders, Towards optimal multiple selection, Automata, Languages and Programming (ICALP 2005), Lecture Notes in Computer Science 3580
    locator: pages 103 to 114 (B + o(B) + O(n) comparisons, where B is the information-theoretic bound)
  - paper: "Helmut Prodinger, Multiple quickselect, Hoare's Find algorithm for several elements, Information Processing Letters 56(3) (1995)"
    locator: pages 123 to 129 (the average cost of multiple quickselect)
  - paper: "J. M. Chambers, Algorithm 410: Partial sorting, Communications of the ACM 14(5) (1971)"
    locator: pages 357 to 358 (quickselect for several ranks at once)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 9 exercises, the k quantiles of a set in O(n lg k) time
---

Multiple selection asks for the items of several ranks $k_1 < k_2 < \cdots < k_m$ among $n$ unsorted items at once, for example the $99$ percentiles of a data set. Running a [selection](/selection-problem/) algorithm $m$ times costs $\Theta(mn)$, and sorting costs $\Theta(n \log n)$; the right answer is in between. Selecting the middle rank, splitting the items around it and recursing on both sides takes $O(n \log m)$ time, and a lower bound from counting shows that, for evenly spaced ranks, $n \lg m - O(n)$ comparisons are needed.

## In plain words

You want the quartiles of a list of numbers: the items one quarter, one half and three quarters of the way up the sorted list. You could find each one from scratch, but each search would walk through the whole list.

A better way finds the middle item first, and in doing so splits the list into a lower half and an upper half. The first quartile is the middle of the lower half, and the third quartile is the middle of the upper half, so each of the later searches looks at only half the list. With many ranks to find, this halving goes on, and the work grows only with the logarithm of the number of ranks, not with the number itself.

## Definition

**Input.** A list of $n$ items with a [total order](/total-order/), and integers $1 \le k_1 < k_2 < \cdots < k_m \le n$.

**Output.** The items $x_1, \ldots, x_m$, where $x_i$ is the item of rank $k_i$, the $k_i$-th entry of the sorted order.

**Cost.** The number of comparisons, in the worst case or on average. Write $k_0 = 0$, $k_{m+1} = n$ and $\Delta_i = k_i - k_{i-1}$ for $1 \le i \le m + 1$ for the gaps between the ranks. The cost depends on these gaps, through

$$ B = \lg \frac{n!}{\Delta_1! \, \Delta_2! \cdots \Delta_{m+1}!} = n \lg n - \sum_{i=1}^{m+1} \Delta_i \lg \Delta_i - O(n), $$

the logarithm of a [multinomial coefficient](/multinomial-coefficient/). In terms of [entropy](/shannon-entropy/), $B \approx n H$, with $H$ the entropy of the distribution $(\Delta_i / n)$.

## Variants

- **Quantiles.** Evenly spaced ranks, $k_i \approx i n / (m + 1)$: the $m$-quantiles of the data ([quantile](/quantile/)). Then $B \approx n \lg(m + 1)$.
- **One rank.** $m = 1$ is the [selection problem](/selection-problem/), and $B = O(n)$.
- **All ranks.** $m = n$ is sorting, and $B = \lg n! = n \lg n - O(n)$.
- **With the segments.** Also report, for each item, which gap $(k_{i-1}, k_i]$ its rank lies in. Algorithms based on splitting give this for free, and it is what a [sample sort](/sample-sort/) or a range partition of a database table needs.
- **Online or deferred.** The ranks arrive one at a time and each must be answered before the next is known. A partly sorted structure that splits only as needed answers $q$ queries in $O(n \log q)$ total time.

## Examples

Let $A = [31, 41, 59, 26, 53, 58, 97, 93, 23, 84]$, with sorted order $23, 26, 31, 41, 53, 58, 59, 84, 93, 97$, and the ranks $k_1 = 3$, $k_2 = 8$. The answer is $(31, 84)$.

**By splitting.** Select rank $3$, which is $31$, and split around it: $L = [26, 23]$ and $G = [41, 59, 53, 58, 97, 93, 84]$. The rank $8$ is now rank $8 - 3 = 5$ in $G$, which is $84$. The second search works on $7$ items instead of $10$.

**The bound.** Here $\Delta = (3, 5, 2)$, and $B = \lg \frac{10!}{3! \, 5! \, 2!} = \lg 2520 \approx 11.3$. For so small an input this is about the $n - 1 = 9$ comparisons that even one rank needs; for large $n$ and many ranks, $B$ is the main term.

## Known algorithms

**Repeated selection.** Run a linear-time selection once for each rank: $O(mn)$. Good only for very small $m$.

**Sort.** Sort and read the $m$ entries: $O(n \log n)$. Good when $m$ is close to $n$.

**Divide by the middle rank.** Select the middle rank $k_{\lceil m/2 \rceil}$ with [median of medians](/median-of-medians/), split the items around it, and recurse with the lower ranks on the lower part and the higher ranks, shifted, on the upper part. Each level of the recursion is a set of selections on disjoint parts of the items, so it costs $O(n)$, and there are $\lceil \lg(m + 1) \rceil$ levels. The time is $O(n \log m)$ in the worst case, the CLRS exercise on quantiles. A finer count gives $O(B + n)$.

**Multiple quickselect.** As [quickselect](/quickselect/), with a random pivot, but recurse into each side that holds at least one of the wanted ranks. This is Chambers's Algorithm 410 of 1971, analyzed on average by Prodinger (1995). It takes $O(n \log m)$ expected time and is simple and fast in practice.

**Near-optimal comparisons.** Kaligosi, Mehlhorn, Munro and Sanders (2005) gave an algorithm with $B + o(B) + O(n)$ comparisons, so the leading term matches the lower bound, using sampling in the style of [Floyd-Rivest selection](/floyd-rivest-select/) and a careful merging of runs.

## Bounds

**Lower bound, $B - n$ comparisons.** Let an algorithm find the items of ranks $k_1, \ldots, k_m$. At the end its comparisons determine, for each item, which gap it lies in: an item whose side of some $x_i$ is not fixed by a chain of comparisons could be moved across $x_i$ without changing any answer, as in the proof of the [selection lower bound](/selection-lower-bound/). So after the algorithm the items fall into the $m + 1$ known groups of sizes $\Delta_i$, and sorting each group by binary insertion takes at most $\sum_i (\lg \Delta_i! + \Delta_i)$ more comparisons. Together these sort the input, which needs $\lg n!$ comparisons in the worst case by the [comparison sort lower bound](/comparison-sort-lower-bound/). So the algorithm needs at least $\lg n! - \sum_i \lg \Delta_i! - n = B - n$ comparisons. Dobkin and Munro gave this bound in 1981.

**Evenly spaced ranks.** For the $m$-quantiles, $B = n \lg(m + 1) - O(n)$, so the $O(n \log m)$ of the splitting method is optimal up to a constant factor.

**Upper bound.** $B + o(B) + O(n)$ comparisons suffice, by Kaligosi, Mehlhorn, Munro and Sanders. The term $O(n)$ cannot be dropped, since already one rank needs about $n$ comparisons.

## Reductions

- **From sorting.** With $m = n$ the output is the sorted order, so multiple selection is at least as hard as sorting for large $m$.
- **To single selection.** Each rank can be found on its own, which gives $O(mn)$.
- **Sorted output for one range.** Finding the items of ranks $k$ through $k + j$ in order reduces to selecting ranks $k$ and $k + j$, taking the items between them, and sorting those, the idea of [partial sorting](/partial-sorting/).

## Applications

- **Quantiles and histograms.** Statistics packages and database query optimizers compute percentiles and the bucket boundaries of equi-depth [histograms](/histogram/).
- **Splitters for parallel and external sorting.** [Sample sort](/sample-sort/) and [parallel sorting by regular sampling](/parallel-sorting-by-regular-sampling/) pick $p - 1$ splitters that divide the input into $p$ parts of nearly equal size: a multiple selection on a sample or on the whole input.
- **Load balancing.** Splitting a set of keys into $p$ ranges of equal size, for example to place them on $p$ machines, is the problem with ranks $n/p, 2n/p, \ldots$.

## References
