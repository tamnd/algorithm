---
tag: 9D3W52
kind: definition
slug: quantile
name: Quantile
aliases:
- percentile
- q-quantile
area: sorting/selection-and-order-statistics
level: intro
summary: Order statistics at evenly spaced ranks, such as quartiles or percentiles.
prereqs: [order-statistic, median]
see_also: [multiple-selection, selection-problem, median, kll-sketch, t-digest, count-min-sketch, sample-sort, random-sampling]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 9, Section 9.3, Selection in worst-case linear time, exercises (the k-th quantiles of a set in O(n lg k) time)
  - paper: "Rob J. Hyndman and Yanan Fan, Sample quantiles in statistical packages, The American Statistician 50(4) (1996)"
    locator: pages 361 to 365 (the nine definitions of a sample quantile)
  - book: isbn:9780471389262
    title: H. A. David and H. N. Nagaraja, Order Statistics, third edition
    locator: Chapter 2, Basic distribution theory (sample quantiles as order statistics)
---

A quantile is an [order statistic](/order-statistic/) chosen by a fraction of the data instead of a rank. The $p$-quantile of $n$ items, for $0 < p \le 1$, is the item with about a fraction $p$ of the items at or below it. The $q$-quantiles are the $q - 1$ items that cut the sorted order into $q$ parts of nearly equal size: the [median](/median/) for $q = 2$, the quartiles for $q = 4$, and the percentiles for $q = 100$.

## Definition

Let $a_1, \ldots, a_n$ be $n \ge 1$ items with a [total order](/total-order/), and let $a_{(i)}$ be the item of rank $i$.

**The $p$-quantile.** For a real $p$ with $0 < p \le 1$, the $p$-quantile is

$$ Q(p) = a_{(\lceil pn \rceil)}. $$

It is the smallest item $x$ of the input such that at least a fraction $p$ of the items are at most $x$. So it is the inverse of the empirical distribution function $F(x) = |\{ j : a_j \le x \}| / n$: $Q(p) = \min \{ x : F(x) \ge p \}$, the minimum taken over the input items. With $p = 1/2$ it is the lower median.

**The $q$-quantiles.** For an integer $q \ge 2$, the $q$-quantiles are the $q - 1$ items

$$ a_{(\lceil jn/q \rceil)}, \qquad j = 1, \ldots, q - 1. $$

When $q$ divides $n$, they cut the sorted order into $q$ blocks of exactly $n/q$ items each, counting each cut item in the block on its left. In general each block has $\lfloor n/q \rfloor$ or $\lceil n/q \rceil$ items. Named cases are the median ($q = 2$), the tertiles ($q = 3$), the quartiles ($q = 4$), the quintiles ($q = 5$), the deciles ($q = 10$) and the percentiles ($q = 100$). The $j$-th quartile is $Q(j/4)$, and the $j$-th percentile is $Q(j/100)$.

**Interpolated quantiles.** In statistics the items are numbers, and the sample quantile is often a weighted mean of two neighbouring order statistics, not an item. Hyndman and Fan (1996) list nine definitions in use. Their type 1 is the definition above. Their type 7, the default of R and of NumPy, sets $h = (n - 1)p + 1$ and returns $a_{(\lfloor h \rfloor)} + (h - \lfloor h \rfloor)(a_{(\lfloor h \rfloor + 1)} - a_{(\lfloor h \rfloor)})$. Each type is a selection of one or two order statistics followed by arithmetic, so the algorithms are the same for all types.

## Examples and non-examples

Let $A = [31, 41, 59, 26, 53, 58, 97, 93, 23, 84]$, with sorted order $23, 26, 31, 41, 53, 58, 59, 84, 93, 97$ and $n = 10$.

**Quartiles.** The ranks are $\lceil 10/4 \rceil = 3$, $\lceil 20/4 \rceil = 5$ and $\lceil 30/4 \rceil = 8$, so the quartiles are $31$, $53$ and $84$. The blocks are $\{23, 26, 31\}$, $\{41, 53\}$, $\{58, 59, 84\}$ and $\{93, 97\}$, of sizes $3, 2, 3, 2$.

**Other definitions.** Type 7 gives $33.5$, $55.5$ and $77.75$: for $p = 1/4$, $h = 3.25$ and $31 + 0.25 \cdot (41 - 31) = 33.5$. Type 6, with $h = (n + 1)p$, gives $29.75$, $55.5$ and $86.25$. These are the values of Python's `statistics.quantiles` with `method='inclusive'` and with the default method. So "the first quartile of $A$" is $29.75$, $31$ or $33.5$, depending on the definition, and code that reports quantiles must say which one it uses.

**Deciles.** For $q = 10$ and $n = 10$, $\lceil jn/q \rceil = j$, so the deciles are $a_{(1)}, \ldots, a_{(9)}$: each item except the maximum.

**Non-example: the quantile is not a fraction of the range.** The value $23 + \frac{1}{4}(97 - 23) = 41.5$ lies a quarter of the way from the minimum to the maximum, but it is not a quartile: it depends only on the two extremes and ignores the other items.

**Non-example: $p = 0$.** $Q(0)$ would need rank $0$, which does not exist. Some definitions set $Q(0)$ to the minimum by convention.

## Related definitions

- **[Order statistic](/order-statistic/).** Each quantile is an order statistic of a rank that depends on $n$ and $p$.
- **[Median](/median/).** The $1/2$-quantile.
- **[Multiple selection](/multiple-selection/).** Computing the $q - 1$ quantiles is selection of $q - 1$ ranks at once. Select the middle quantile, split the input around it, and recurse on both halves: the recursion has depth $\lceil \lg q \rceil$ and each level costs $O(n)$, so the total is $O(n \log q)$ time, against $O(n \log n)$ for a full sort.
- **Approximate quantiles.** A rank within $\varepsilon n$ of $\lceil pn \rceil$ is accepted. A [random sample](/random-sampling/) of $O(\varepsilon^{-2} \log (1/\delta))$ items gives such an answer with probability at least $1 - \delta$, and stream sketches such as the [KLL sketch](/kll-sketch/) and the [t-digest](/t-digest/) keep approximate quantiles of a stream in small space.
- **Splitters.** [Sample sort](/sample-sort/) uses the $q$-quantiles of a sample as bucket boundaries, so the buckets have nearly equal sizes.

## References
