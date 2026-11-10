---
tag: 94DN81
kind: concept
slug: bin-packing-lower-bound
name: Bin packing lower bound
aliases:
- total size lower bound
- size bound
- configuration LP bound
area: approximation/covering-and-packing
level: intro
summary: Ceiling of total item size divided by capacity lower-bounds the optimal bin count.
prereqs: [bin-packing, lp-relaxation]
see_also: [configuration-lp, next-fit-bin-packing, first-fit-decreasing, bin-packing-aptas, karmarkar-karp-bin-packing, integrality-gap, cutting-stock-problem]
sources:
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 3.3 (the size bound in the bin packing scheme) and Chapter 4 (the configuration LP in the Karmarkar and Karp algorithm)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 9 (Bin packing)
  - paper: "S. Martello and P. Toth, Lower bounds and reduction procedures for the bin packing problem, Discrete Applied Mathematics 28, 1990"
    title: Martello and Toth 1990
    locator: the bound L2 (big items combined with the size bound)
  - paper: "P. C. Gilmore and R. E. Gomory, A linear programming approach to the cutting-stock problem, Operations Research 9(6), 1961"
    title: Gilmore and Gomory 1961
    locator: the pattern (configuration) formulation and its LP relaxation
---

A lower bound for [bin packing](/bin-packing/) is a number that can be computed fast and is never more than $\mathrm{OPT}$, the least number of bins. The three standard ones are the *size bound* $\lceil S \rceil$, where $S$ is the total item size, the number of items larger than one half, and the value of the [configuration LP](/configuration-lp/). Each approximation guarantee for bin packing is proved by comparing the algorithm with one of these bounds, because $\mathrm{OPT}$ itself is [NP-hard](/np-hard/) to compute.

## In plain words

To show that a packing is good, you must compare it with the best packing. But nobody can compute the best packing fast. So you compare with a number that is easy to compute and that the best packing can never beat.

The simplest such number comes from the total size: if the objects together fill three and a half boxes, you need at least four boxes. A second number counts the objects that are bigger than half a box, because no two of them can share a box. A third number comes from a relaxed problem, where you may use fractions of box patterns. This last number is the strongest of the three, and it is still fast to compute.

## The idea

Notation, as on the [bin packing](/bin-packing/) page: there are $n$ items with sizes $s_1, \ldots, s_n \in (0, 1]$, the bins have capacity 1, $S = \sum_i s_i$, and $\mathrm{OPT}$ is the least number of bins.

### The size bound

**Claim.** $\mathrm{OPT} \ge \lceil S \rceil$.

*Proof.* Take an optimal packing with $\mathrm{OPT}$ bins. Each bin has load at most 1, and each item is in exactly one bin. So $S$ is the sum of the $\mathrm{OPT}$ loads, and $S \le \mathrm{OPT}$. Since $\mathrm{OPT}$ is an integer, $\lceil S \rceil \le \mathrm{OPT}$. $\square$

The bound can be off by a factor close to 2, but not more. [Next fit](/next-fit-bin-packing/) uses at most $2\lceil S \rceil - 1$ bins, so $\mathrm{OPT} \le 2 \lceil S \rceil - 1$. In the other direction, $n$ items of size $\frac12 + \delta$ give $\mathrm{OPT} = n$ and $\lceil S \rceil = \lceil n/2 + n\delta \rceil$, so the ratio tends to 2 when $\delta \to 0$ and $n \to \infty$ with $n\delta \to 0$.

### The count of big items

**Claim.** Let $b$ be the number of items with $s_i > \frac12$. Then $\mathrm{OPT} \ge b$.

*Proof.* Two items larger than $\frac12$ have total size larger than 1, so they are in different bins of each packing. So the $b$ big items need $b$ distinct bins. $\square$

The two bounds combine. For a threshold $\alpha \in [0, \frac12]$, let $J_1$ be the items with $s_i > 1 - \alpha$, let $J_2$ be the items with $\frac12 < s_i \le 1 - \alpha$, and let $J_3$ be the items with $\alpha \le s_i \le \frac12$. Martello and Toth (1990) proved

$$\mathrm{OPT} \;\ge\; L(\alpha) = |J_1| + |J_2| + \max\Bigl(0,\ \Bigl\lceil \textstyle\sum_{i \in J_3} s_i - \bigl(|J_2| - \sum_{i \in J_2} s_i\bigr) \Bigr\rceil\Bigr).$$

*Proof.* Fix an optimal packing. The items of $J_1 \cup J_2$ are larger than $\frac12$, so they are in $|J_1| + |J_2|$ distinct bins. No item of $J_3$ shares a bin with an item of $J_1$, because their sizes add to more than $\alpha + (1 - \alpha) = 1$. The bins of the items of $J_2$ have total free space at most $|J_2| - \sum_{J_2} s_i$, and items of $J_3$ can go only there or in other bins. So the items of $J_3$ in other bins have total size at least $\sum_{J_3} s_i - (|J_2| - \sum_{J_2} s_i)$, and these other bins number at least the ceiling of this amount when it is positive. Items smaller than $\alpha$ are ignored, which can only lower the count. $\square$

The value $L(0)$ is at least the count of big items. For each $\alpha$, $L(\alpha)$ is at least the ceiling of the total size of the items of size at least $\alpha$, because $|J_1| \ge \sum_{J_1} s_i$. Only the values $\alpha = s_i$ with $s_i \le \frac12$ and $\alpha = 0$ need to be tried, so the best $L(\alpha)$ takes $O(n \log n)$ time after a sort.

### The configuration LP bound

A *configuration* is a set $C$ of items with $\sum_{i \in C} s_i \le 1$. Let $\mathcal{C}$ be the set of all configurations. The configuration LP of Gilmore and Gomory (1961) is

$$\mathrm{LP}^* = \min \Bigl\{ \sum_{C \in \mathcal{C}} x_C \;:\; \sum_{C \ni i} x_C \ge 1 \text{ for each item } i,\ \ x \ge 0 \Bigr\}.$$

When items have equal sizes, it is usual to group them into types and to write the demand of each type on the right side. This is the form of the [cutting stock problem](/cutting-stock-problem/).

**Claim.** $\max(S, b) \le \mathrm{LP}^* \le \mathrm{OPT}$.

*Proof.* An optimal packing gives a 0/1 vector $x$ with one configuration for each bin. It covers each item, so it is feasible and $\mathrm{LP}^* \le \mathrm{OPT}$. Now let $x$ be any feasible solution. Each configuration has total size at most 1, and at most one item larger than $\frac12$. So

$$\sum_C x_C \ge \sum_C x_C \sum_{i \in C} s_i = \sum_i s_i \sum_{C \ni i} x_C \ge \sum_i s_i = S,$$

and in the same way, with the count of big items in $C$ in place of the size of $C$, $\sum_C x_C \ge b$. $\square$

So $\lceil \mathrm{LP}^* \rceil$ is at least as strong as both earlier bounds. The LP has exponentially many variables, but its dual has one variable for each item (or each type), and the separation problem of the dual is a [knapsack problem](/knapsack-problem/). So the LP can be solved to any accuracy by the [ellipsoid method](/ellipsoid-method/) or by [column generation](/column-generation/). Karmarkar and Karp (1982) solve it approximately in polynomial time. The gap is small: [Karmarkar and Karp](/karmarkar-karp-bin-packing/) round it to $\mathrm{OPT} \le \mathrm{LP}^* + O(\log^2 \mathrm{OPT})$, and Hoberg and Rothvoss (2017) to $\mathrm{LP}^* + O(\log \mathrm{OPT})$. No instance is known with $\mathrm{OPT} > \lceil \mathrm{LP}^* \rceil + 1$.

The simpler assignment LP, with a variable $x_{ij}$ for "item $i$ in bin $j$", a variable $y_j$ for "bin $j$ is open", the constraints $\sum_j x_{ij} = 1$, $\sum_i s_i x_{ij} \le y_j$ and $x_{ij} \le y_j \le 1$ for $n$ bins, is much weaker. Set $x_{ij} = 1/n$ and $y_j = \max(1, S)/n$. This is feasible, so the value is at most $\max(1, S)$, which is no better than the size bound.

## Examples

All numbers below were computed exactly with fractions.

| instance | $\lceil S \rceil$ | $b$ | $L(\alpha)$ best | $\mathrm{LP}^*$ | $\mathrm{OPT}$ |
|---|---|---|---|---|---|
| $(0.2, 0.5, 0.4, 0.7, 0.1, 0.3, 0.8)$ | 3 | 2 | 3 | 3 | 3 |
| four items of size $0.6$ | 3 | 4 | 4 | 4 | 4 |
| twelve items of size $0.4$ | 5 | 0 | 5 | 6 | 6 |
| three of size $0.7$, three of size $0.4$ | 4 | 3 | 5 | $9/2$ | 5 |

- In the second row, the size bound is weak and the count of big items is exact.
- In the third row, each configuration holds at most two items, so $\mathrm{LP}^* = 12/2 = 6$, while the size bound gives only 5. The Martello and Toth bound with $\alpha = 0.4$ also gives $\lceil 4.8 \rceil = 5$.
- In the fourth row, $\alpha = 0.4$ puts the three items of size $0.7$ in $J_1$, so $L(0.4) = 3 + \lceil 1.2 \rceil = 5$. The configuration LP gives $3 + 3/2 = 9/2$, and its ceiling is also 5.

## Where it is used

- [Next fit](/next-fit-bin-packing/) and [first fit](/first-fit-bin-packing/) are compared with the size bound: each pair of bins, or each bin but one, is more than half full.
- The simple proof that [first fit decreasing](/first-fit-decreasing/) uses at most $\frac32 \mathrm{OPT}$ bins uses both the count of big items and the size bound.
- The [asymptotic scheme](/bin-packing-aptas/) uses the size bound twice: to show that the grouping loses at most $\varepsilon \cdot \mathrm{OPT}$ bins, and to bound the bins that the small items fill.
- The algorithm of [Karmarkar and Karp](/karmarkar-karp-bin-packing/) and the [configuration LP](/configuration-lp/) pages round $\mathrm{LP}^*$.
- Exact branch and bound codes for bin packing prune with $L(\alpha)$ and with the LP bound, and [column generation](/column-generation/) for [cutting stock](/cutting-stock-problem/) computes $\mathrm{LP}^*$.

## References
