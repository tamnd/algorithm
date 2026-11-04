---
tag: GRVAHK
kind: definition
slug: weighted-median
name: Weighted median
area: sorting/selection-and-order-statistics
level: core
summary: An element at which the total weight of smaller elements and of larger elements are each at most half.
prereqs: [median]
see_also: [weighted-median-post-office-location, median, median-finding, median-of-medians, selection-problem, geometric-median, prune-and-search, quantile]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 9, end-of-chapter problem "Weighted median" (the definition with total weight 1, the O(n lg n) and Θ(n) algorithms, and the post-office location problem)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.3, Minimum-comparison selection (selection, of which the weighted median is a generalization)
---

A weighted median of items with positive weights is an item that splits the total weight in two halves: the items less than it weigh at most half of the total, and the items greater than it weigh at most half of the total. With equal weights it is the ordinary [median](/median/). It is the point on a line that minimizes the weighted sum of distances, which is why it solves the one-dimensional [post office location problem](/weighted-median-post-office-location/).

## Definition

Let $x_1, \ldots, x_n$ be $n \ge 1$ items with a [total order](/total-order/), and let $w_1, \ldots, w_n > 0$ be weights with total $W = \sum_i w_i$. For an item $x$, write

$$ L(x) = \sum_{i : x_i < x} w_i, \qquad G(x) = \sum_{i : x_i > x} w_i. $$

An item $x_k$ of the input is a **weighted median** when

$$ L(x_k) \le W/2 \quad \text{and} \quad G(x_k) \le W/2. $$

A weighted median always exists. Sort the items and walk up from the smallest, adding weights. Let $x_k$ be the first item at which the running total, including $x_k$ and the items equal to it, reaches at least $W/2$. The items before it weigh less than $W/2$, so $L(x_k) < W/2$, and the items after it weigh $W$ minus at least $W/2$, so $G(x_k) \le W/2$.

The item found this way is the **lower weighted median**: the smallest $x_k$ with $L(x_k) < W/2$ and $G(x_k) \le W/2$. This is the form in CLRS, which takes distinct items and $W = 1$, so the conditions read $\sum_{x_i < x_k} w_i < 1/2$ and $\sum_{x_i > x_k} w_i \le 1/2$. The lower weighted median is unique. The **upper weighted median** is the mirror case, with $L \le W/2$ and $G < W/2$. Each weighted median lies between the two.

**Equal weights.** With $w_i = 1$ for each $i$, $L(x)$ and $G(x)$ count the items below and above $x$, and the conditions are the balance property of the median. For distinct items the lower weighted median is then the lower median $x_{(\lceil n/2 \rceil)}$ and the upper weighted median is the upper median.

**Least weighted distance.** For real items, a real $m$ minimizes

$$ f(m) = \sum_{i=1}^{n} w_i \, |x_i - m| $$

exactly when $m$ lies between the lower and the upper weighted median. Just to the right of $m$, the slope of $f$ is the weight of the items at most $m$ minus the weight of the items greater than $m$. It is negative while the items at most $m$ weigh less than $W/2$, and positive once they weigh more than $W/2$. So $f$ decreases up to the lower weighted median, is constant between the two weighted medians, and increases after the upper one.

## Examples and non-examples

**Two weighted medians.** Let the items be $1, 3, 4, 7, 9$ with weights $0.1, 0.3, 0.1, 0.2, 0.3$, so $W = 1$.

| $x$ | 1 | 3 | 4 | 7 | 9 |
|---|---|---|---|---|---|
| $w$ | 0.1 | 0.3 | 0.1 | 0.2 | 0.3 |
| $L(x)$ | 0 | 0.1 | 0.4 | 0.5 | 0.7 |
| $G(x)$ | 0.9 | 0.6 | 0.5 | 0.3 | 0 |

The items $4$ and $7$ satisfy both conditions, so both are weighted medians. The lower weighted median is $4$, since $L(4) = 0.4 < 0.5$. The item $7$ is the upper one: $L(7) = 0.5$ is not less than $1/2$, so it fails the CLRS condition, but $G(7) = 0.3 < 0.5$. The weighted distance $f(m)$ is $2.7$ for each $m$ from $4$ to $7$, and $2.9$ at $m = 3$ and $3.1$ at $m = 8$.

**Weighted median is not the median.** In the same example the ordinary median of the five items is $4$, but with weights $0.1, 0.1, 0.1, 0.1, 0.6$ the only weighted median is $9$: $L(9) = 0.4 \le 0.5$ and $G(9) = 0$, while $G(7) = 0.6$. One heavy item pulls the weighted median to itself.

**Equal weights.** Items $2, 5, 8, 10$ with weight $1/4$ each: $L(5) = 1/4$ and $G(5) = 1/2$, so $5$ is the lower weighted median; $8$ has $L(8) = 1/2$ and $G(8) = 1/4$, so it is the upper one. These are the lower and upper medians.

**Non-example: the weighted mean.** For the first example, $\sum_i w_i x_i = 5.5$. It is not an item, and its cost $f(5.5) = 2.7$ is the minimum only because $5.5$ happens to lie in $[4, 7]$. With weights $0.1, 0.1, 0.1, 0.1, 0.6$ the weighted mean is $6.9$ and $f(6.9) = 2.54$, more than $f(9) = 2.1$.

**Non-example: half the items by count.** The item $4$ of the second weighting has two items below and two above, so it is the median by count, but $G(4) = 0.7 > 0.5$, so it is not a weighted median.

## Related definitions

- **[Median](/median/).** The case of equal weights.
- **[Weighted median and post office location](/weighted-median-post-office-location/).** The problem of computing a weighted median. Sorting and a prefix sum take $O(n \log n)$ time; a [median-of-medians](/median-of-medians/) style recursion that keeps only the side holding the half-weight point takes $\Theta(n)$ time in the worst case.
- **[Quantile](/quantile/).** The weighted $p$-quantile replaces $W/2$ by $pW$ in the walk above.
- **[Geometric median](/geometric-median/).** The point that minimizes the weighted sum of Euclidean distances in the plane or in space. In the Manhattan metric the problem splits into one weighted median per coordinate.
- **[Prune and search](/prune-and-search/).** Linear-time weighted median finding is a standard step of prune-and-search algorithms, which use it to drop a fixed fraction of the input weight in each round.

## References
