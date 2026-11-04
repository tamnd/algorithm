---
tag: DB0KJF
kind: definition
slug: order-statistic
name: Order statistic
aliases:
- i-th order statistic
- k-th smallest element
area: sorting/selection-and-order-statistics
level: intro
summary: The i-th smallest element of a set of n elements, for 1 ≤ i ≤ n.
prereqs: [total-order]
see_also: [selection-problem, median, quantile, minimum-and-maximum-finding, quickselect, median-of-medians, order-statistic-tree]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 9, Medians and Order Statistics, chapter introduction (the i-th order statistic, the minimum, the maximum, the lower and upper medians)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.3, Minimum-comparison selection (the t-th largest of n elements)
  - book: isbn:9780471389262
    title: H. A. David and H. N. Nagaraja, Order Statistics, third edition
    locator: Chapter 1, Introduction, and Chapter 2, Basic distribution theory (order statistics of a random sample)
---

The $i$-th order statistic of a set of $n$ items is the $i$-th smallest item, for $1 \le i \le n$. The first order statistic is the minimum, the $n$-th is the maximum, and the order statistics near $n/2$ are the [medians](/median/). Finding an order statistic without sorting is the [selection problem](/selection-problem/).

## Definition

Let $a_1, \ldots, a_n$ be $n \ge 1$ items from a set with a [total order](/total-order/) $\le$. Let $b_1 \le b_2 \le \cdots \le b_n$ be the items in sorted order. For $1 \le i \le n$, the **$i$-th order statistic** is

$$ a_{(i)} = b_i. $$

Two sorted orders of the same items can differ only in the order of equal items, so they have the same entry at each position, and $a_{(i)}$ is well defined. Without a sort, $a_{(i)}$ is the item $x$ of the input with

$$ \bigl|\{ j : a_j < x \}\bigr| \le i - 1 \quad \text{and} \quad \bigl|\{ j : a_j \le x \}\bigr| \ge i. $$

The index $i$ is the **rank**. When the items are distinct, $a_{(i)}$ is the unique item with exactly $i - 1$ items below it, and the rank of each item is a single number. With repeated items, a value $v$ fills the ranks from $|\{ j : a_j < v \}| + 1$ to $|\{ j : a_j \le v \}|$.

The notation $a_{(i)}$, with the index in brackets, comes from statistics. Algorithm books also write "the item of rank $i$" or "the $i$-th smallest". Some authors count from the top and speak of the $t$-th largest; the $t$-th largest is $a_{(n + 1 - t)}$.

In probability, for a random sample $X_1, \ldots, X_n$, the order statistic $X_{(i)}$ is a [random variable](/random-variable/): the $i$-th smallest value of the sample. Its [distribution](/probability-distribution/) is a subject of statistics; this page uses only the fixed-input meaning.

## Examples and non-examples

**Distinct items.** For $A = [31, 41, 59, 26, 53, 58, 97, 93, 23, 84]$, the sorted order is $23, 26, 31, 41, 53, 58, 59, 84, 93, 97$.

| $i$ | 1 | 2 | 3 | 5 | 6 | 9 | 10 |
|---|---|---|---|---|---|---|---|
| $a_{(i)}$ | 23 | 26 | 31 | 53 | 58 | 93 | 97 |

The minimum is $a_{(1)} = 23$ and the maximum is $a_{(10)} = 97$. The lower median is $a_{(5)} = 53$ and the upper median is $a_{(6)} = 58$. The second largest is $a_{(9)} = 93$.

**Repeated items.** For $A = [5, 1, 5, 3, 5]$, the sorted order is $1, 3, 5, 5, 5$, so $a_{(1)} = 1$, $a_{(2)} = 3$ and $a_{(3)} = a_{(4)} = a_{(5)} = 5$. The value 5 fills ranks 3 to 5: two items are less than 5 and five items are at most 5.

**Strings.** For the words $[\text{pear}, \text{fig}, \text{apple}, \text{kiwi}]$ in alphabetical order, $a_{(1)} = \text{apple}$, $a_{(2)} = \text{fig}$, $a_{(3)} = \text{kiwi}$ and $a_{(4)} = \text{pear}$. Any total order works, not only the order of numbers.

**Non-example: a position, not a rank.** For the first array, $a_5 = 53$ is the fifth item in input order and $a_{(5)} = 53$ is the fifth smallest. They agree here only by chance: $a_3 = 59$, but $a_{(3)} = 31$.

**Non-example: the mean.** For $[1, 2, 2, 3, 100]$, the mean is $21.6$, which is not an item of the list, and the median $a_{(3)} = 2$ is. An order statistic is always one of the input items.

**Non-example: no total order.** The pairs $(1, 2)$ and $(2, 1)$ under the order "$(x, y) \le (x', y')$ when $x \le x'$ and $y \le y'$" are not comparable, so this order gives no sorted order and no order statistics. A key that orders the pairs totally, such as $x + y$ with ties broken by $x$, is needed first.

**Non-example: rank out of range.** $a_{(0)}$ and $a_{(n+1)}$ are not defined. Code that counts ranks from 0 must convert: rank $i$ is index $i - 1$ of the sorted array.

## Related definitions

- **[Selection problem](/selection-problem/).** Compute $a_{(k)}$ for a given $k$. It takes $\Theta(n)$ time in the [comparison model](/comparison-model/), with [quickselect](/quickselect/) in expectation and [median of medians](/median-of-medians/) in the worst case.
- **[Median](/median/).** The order statistic of rank $\lceil n/2 \rceil$, the lower median; for even $n$ the upper median has rank $n/2 + 1$.
- **[Quantile](/quantile/).** Order statistics at evenly spaced ranks, such as the quartiles and percentiles.
- **[Minimum and maximum](/minimum-and-maximum-finding/).** The order statistics $a_{(1)}$ and $a_{(n)}$.
- **[Weighted median](/weighted-median/).** The analogue of the median when each item has a weight and rank is measured by weight.
- **Rank of an item.** The inverse question: given an item $x$, count the items below it. An [order-statistic tree](/order-statistic-tree/) answers both questions for a changing set in $O(\log n)$ time.
- **[Permutation](/permutation/).** Sorting distinct items applies a permutation $\pi$ with $a_{\pi(i)} = a_{(i)}$; the order statistics are the items read in the order of $\pi$.

## References
