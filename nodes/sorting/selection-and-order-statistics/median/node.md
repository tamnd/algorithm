---
tag: AYRX3B
kind: definition
slug: median
name: Median
aliases:
- lower median
- upper median
area: sorting/selection-and-order-statistics
level: intro
summary: The element of rank ⌈n/2⌉; for even n the lower and upper medians have ranks n/2 and n/2+1.
prereqs: [order-statistic]
see_also: [median-finding, selection-problem, quantile, weighted-median, median-of-medians, geometric-median, median-filter, sliding-window-median]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 9, Medians and Order Statistics, chapter introduction (lower median at rank floor((n+1)/2), upper median at rank ceil((n+1)/2))
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.3, Minimum-comparison selection (the median as the hardest case of selection)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 2, Section 2.4, Medians
  - book: isbn:9780471389262
    title: H. A. David and H. N. Nagaraja, Order Statistics, third edition
    locator: Chapter 1, Introduction (the sample median)
---

The median of $n$ items is the item in the middle of their sorted order: the [order statistic](/order-statistic/) of rank $\lceil n/2 \rceil$. For odd $n$ the middle is a single rank. For even $n$ there are two middle ranks, $n/2$ and $n/2 + 1$, which give the lower and the upper median. In statistics the median of an even number of values is often the mean of the two, but algorithms usually return one of the input items.

## Definition

Let $a_1, \ldots, a_n$ be $n \ge 1$ items with a [total order](/total-order/), and let $a_{(i)}$ be the item of rank $i$.

- The **lower median** is $a_{(\lfloor (n+1)/2 \rfloor)} = a_{(\lceil n/2 \rceil)}$.
- The **upper median** is $a_{(\lceil (n+1)/2 \rceil)} = a_{(\lfloor n/2 \rfloor + 1)}$.

For odd $n = 2m + 1$ both are $a_{(m+1)}$, and this item is **the median**. For even $n = 2m$ the lower median is $a_{(m)}$ and the upper median is $a_{(m+1)}$. When the text says "the median" without a qualifier, it means the lower median, as in CLRS.

For numbers, the **statistical median** of an even count is $\frac{1}{2}(a_{(m)} + a_{(m+1)})$. It need not be an input item, and it needs arithmetic on the items, not only comparisons.

**Balance property.** An item $x$ of the input is a lower or upper median, or lies between them, exactly when

$$ \bigl|\{ j : a_j < x \}\bigr| \le n/2 \quad \text{and} \quad \bigl|\{ j : a_j > x \}\bigr| \le n/2. $$

At most half of the items lie strictly on each side. This is the form that generalizes to the [weighted median](/weighted-median/), where counts become sums of weights.

**Least absolute deviation.** For real numbers, a real $m$ minimizes $f(m) = \sum_j |a_j - m|$ exactly when $a_{(\lceil n/2 \rceil)} \le m \le a_{(\lfloor n/2 \rfloor + 1)}$. Moving $m$ to the right by a small step changes $f$ by the step times (the number of items at most $m$) minus (the number of items greater than $m$), so $f$ goes down while fewer than half the items are at most $m$ and goes up once more than half are. For odd $n$ the minimizer is unique and equals the median.

## Examples and non-examples

**Even count.** For $A = [31, 41, 59, 26, 53, 58, 97, 93, 23, 84]$, $n = 10$ and the sorted order is $23, 26, 31, 41, 53, 58, 59, 84, 93, 97$. The lower median is $a_{(5)} = 53$, the upper median is $a_{(6)} = 58$, and the statistical median is $55.5$. The sum of distances $\sum_j |a_j - m|$ is $217$ for each $m$ from $53$ to $58$, and $223$ for $m = 50$ and for $m = 60$.

**Odd count.** For $[5, 1, 5, 3, 5]$, the sorted order is $1, 3, 5, 5, 5$ and the median is $a_{(3)} = 5$. Two items are less than $5$, which is at most $5/2$, and no item is greater.

**Robustness.** For $[1, 2, 2, 3, 100]$, the median is $2$ and the mean is $21.6$. The one large value moves the mean far from the bulk of the data, but the median stays. The sum of distances is $100$ from the median and $156.8$ from the mean.

**Non-example: the middle position.** The item in the middle position of the input, $a_{\lceil n/2 \rceil}$, is not the median unless the input is sorted. For the first array, $a_5 = 53$ is the lower median only by chance; for $[3, 1, 2]$, $a_2 = 1$ but the median is $2$.

**Non-example: an approximate median.** An item whose rank is between $n/4$ and $3n/4$ is a good pivot for [quicksort](/quicksort/), and [median of medians](/median-of-medians/) finds one, but it is not the median in general. For $[1, 2, 3, 20, 21, 4, 5, 6, 22, 23, 7, 8, 9, 24, 25]$ in groups of five, the group medians are $3$, $6$ and $9$, so the median of medians is $6$, of rank 6. The median is $a_{(8)} = 8$.

## Related definitions

- **[Order statistic](/order-statistic/).** The median is the order statistic of the middle rank.
- **[Quantile](/quantile/).** The median is the $1/2$-quantile, the second quartile and the 50th percentile.
- **[Weighted median](/weighted-median/).** Each item has a weight, and the balance property uses sums of weights.
- **[Geometric median](/geometric-median/).** The point that minimizes the sum of Euclidean distances to points in the plane or in space; on a line it is the median.
- **[Median finding](/median-finding/).** The problem of computing the median, in $\Theta(n)$ time by [selection](/selection-problem/).
- **[Median filter](/median-filter/) and [sliding window median](/sliding-window-median/).** The median of each window of a sequence.

## References
