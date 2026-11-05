---
tag: BGDNMA
kind: problem
slug: largest-rectangle-in-histogram
name: Largest rectangle in histogram
aliases:
- Largest rectangle in a histogram
- maximal rectangle in histogram
- maximal rectangle under a histogram
area: sequences/subarray-problems
level: core
summary: Given bar heights, find the largest rectangle that fits under the histogram.
prereqs: [subarray, monotonic-stack]
see_also: [histogram-stack-algorithm, maximal-rectangle-binary-matrix, next-greater-element, cartesian-tree, range-minimum-query, largest-empty-rectangle, container-with-most-water, trapping-rain-water]
sources:
  - url: https://leetcode.com/problems/largest-rectangle-in-histogram/
    title: LeetCode, problem 84, Largest Rectangle in Histogram
    locator: problem statement and the example with heights 2, 1, 5, 6, 2, 3
  - url: https://www.drdobbs.com/database/the-maximal-rectangle-problem/184410529
    title: "David Vandevoorde, The Maximal Rectangle Problem, Dr. Dobb's Journal 23(4), April 1998"
    locator: the stack of open rectangles over a row profile
  - paper: doi:10.1006/jagm.1993.1018
    title: "Omer Berkman, Baruch Schieber and Uzi Vishkin, Optimal doubly logarithmic parallel algorithms based on finding all nearest smaller values, Journal of Algorithms 14(3) (1993), 344-370"
    locator: the all nearest smaller values problem and its parallel algorithm
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 8, Amortized analysis, the section Nearest smaller elements
---

The largest rectangle in a histogram problem gives a row of $n$ bars of width $1$ and heights $h_0, \dots, h_{n-1}$, and asks for the rectangle of largest area that lies inside the bars. Such a rectangle covers a [subarray](/subarray/) of bars $h_i, \dots, h_j$ and has the height of the lowest of them, so the area is $(j - i + 1) \cdot \min(h_i, \dots, h_j)$. The key fact is that a best rectangle has the full height of some bar $k$ and reaches out to the nearest strictly lower bars on both sides. These nearest lower bars, for all $k$, come from one scan with a [monotonic stack](/monotonic-stack/), which gives the [histogram stack algorithm](/histogram-stack-algorithm/) in $\Theta(n)$ time. The problem is the inner step of the [maximal rectangle in a binary matrix](/maximal-rectangle-binary-matrix/).

## In plain words

You have a bar chart. The bars stand side by side, each one unit wide, with different heights. You want to draw the biggest rectangle that stays inside the bars.

A rectangle is as tall as the lowest bar it covers. So for every bar, imagine a rectangle exactly as tall as that bar, stretched left and right until it hits a lower bar. That is the widest rectangle of that height. One of these rectangles, one per bar, is the answer.

The work is to find, for every bar, where the first lower bar is on each side. A stack of bars that rise from bottom to top finds all of them in one pass.

## Definition

**Input.** Heights $h_0, \dots, h_{n-1} \ge 0$, with $n \ge 0$.

**Output.** The largest area
$$A^* = \max_{0 \le i \le j \le n-1} (j - i + 1) \cdot \min_{i \le k \le j} h_k,$$
with $A^* = 0$ for $n = 0$, and a pair $(i, j)$ that reaches it.

**Nearest lower bars.** For bar $k$, let $L_k$ be the largest index $l < k$ with $h_l < h_k$, or $-1$ if there is none, and let $R_k$ be the smallest index $r > k$ with $h_r < h_k$, or $n$ if there is none. Then
$$A^* = \max_{0 \le k \le n-1} h_k \cdot (R_k - L_k - 1).$$
*Why.* Each term is the area of the rectangle on bars $L_k + 1, \dots, R_k - 1$, all of height at least $h_k$, so the right side is at most $A^*$. Conversely, a best rectangle on bars $i..j$ has height $h_k$ for some lowest bar $k$ in $i..j$, so no bar in $i..j$ is lower than $h_k$, and $L_k < i \le j < R_k$. Its area is at most $h_k (R_k - L_k - 1)$.

## Variants

- **Binary matrix.** The largest rectangle of ones in a $0/1$ matrix runs this problem once per row, on the column heights of the ones above; see the [maximal rectangle in a binary matrix](/maximal-rectangle-binary-matrix/).
- **Bars of different widths.** With widths $w_k > 0$, the rectangle for bar $k$ has width $\sum_{L_k < l < R_k} w_l$, which prefix sums of the widths give. The stack algorithm is unchanged.
- **Largest square.** The largest square under the histogram has side $\max_k \min(h_k, R_k - L_k - 1)$.
- **Points instead of bars.** The [largest empty rectangle](/largest-empty-rectangle/) among points in the plane is the continuous relative of this problem.
- **Container with most water.** The area there is the width times the lower of the two *end* bars only, not the lowest bar in between; see [container with most water](/container-with-most-water/), which two pointers solve.
- **Range version.** For the best rectangle inside bars $a..b$, many times, use a [range minimum query](/range-minimum-query/) structure and divide at the minimum.

## Examples

**The standard example.** For $h = [2, 1, 5, 6, 2, 3]$ the answer is $10$: height $5$ over bars $2$ and $3$. The bar of height $2$ at index $4$ reaches from index $2$ to index $5$, an area of $8$, and the bar of height $1$ covers all six bars, an area of $6$.

**Rising bars.** For $h = [1, 2, 3, 4, 5]$ the answer is $9$, height $3$ over bars $2..4$. Neither the tallest bar alone ($5$) nor the full width ($5$) is best.

**Two bars.** For $h = [2, 4]$ the answer is $4$, from either the bar of height $4$ alone or height $2$ over both bars.

**Equal bars.** For $h = [3, 3, 3]$ the answer is $9$. If $L_k$ and $R_k$ both stopped at bars that are lower *or equal*, every bar would get width $1$ and the formula would give $3$. One of the two sides may stop at equal bars, because the leftmost or rightmost of the equal bars still gets the full width, but not both.

## Known algorithms

| method | time | extra space | idea |
|---|---|---|---|
| all pairs with a running minimum | $\Theta(n^2)$ | $O(1)$ | for each $i$, extend $j$ and keep $\min$ |
| divide at the minimum, linear scan | $O(n^2)$, $O(n \log n)$ for random heights | $O(n)$ | the best rectangle uses the lowest bar or lies on one side |
| divide at the minimum with a [range minimum query](/range-minimum-query/) | $O(n \log n)$ or $O(n)$ | $O(n)$ | as above, the minimum found in $O(1)$ |
| nearest lower bars, two stack passes | $\Theta(n)$ | $\Theta(n)$ | compute $L$ and $R$, then $\max_k h_k (R_k - L_k - 1)$ |
| [histogram stack algorithm](/histogram-stack-algorithm/) | $\Theta(n)$ | $\Theta(n)$ | one pass, each bar's area computed when it is popped |
| [Cartesian tree](/cartesian-tree/) | $\Theta(n)$ | $\Theta(n)$ | each node gives height times subtree size |

**Divide at the minimum.** If bar $m$ is a lowest bar, a best rectangle either covers bar $m$, with area $n \cdot h_m$, or lies in bars $0..m-1$ or $m+1..n-1$. With a range minimum structure, the recursion visits each bar once as a minimum, so $O(n)$ calls after the structure is built. This recursion is exactly the [Cartesian tree](/cartesian-tree/) of the heights, with the minimum at the root: the rectangle of node $k$ spans its subtree.

## Bounds

**Linear time is optimal.** Every height must be read: if bar $k$ is not read, raising it to a very large value makes the single bar $k$ the best rectangle. So $\Omega(n)$ time is needed, and the stack algorithm reaches it.

**Parallel.** The nearest lower bars are the all nearest smaller values problem. Berkman, Schieber and Vishkin (1993) solve it in $O(\log \log n)$ time on a CRCW PRAM with $n / \log \log n$ processors, which then gives the areas and their maximum within the same bounds.

## Reductions

- **To all nearest smaller values.** By the formula of the definition, the problem is $L$ and $R$ for every bar, then one maximum. Both $L$ and $R$ come from a scan with a monotonic stack, as in [next greater element](/next-greater-element/) with the order reversed.
- **To the Cartesian tree.** The subtree of node $k$ in the min-rooted Cartesian tree is exactly the bars $L_k + 1, \dots, R_k - 1$, when ties are broken in a fixed way, so the area of node $k$ is $h_k$ times its subtree size.
- **Binary matrix to histograms.** The maximal rectangle of ones in an $r \times c$ matrix is the best of $r$ histogram problems of size $c$, so it takes $\Theta(rc)$ time.

## Applications

- **Binary images.** The largest rectangle of ones, or of free cells, in an image or a grid map is found row by row through this problem, for example the largest free area in an occupancy grid or the largest uniform block in a bitmap.
- **Layout.** The largest free rectangle on a page, a chip or a storage area with fixed obstacles.
- **Skyline questions.** Questions about the largest block under a skyline, where the bars are building heights.
- **Teaching.** It is the standard example of an amortized stack scan where the useful information is computed at the time an item leaves the stack.

## References
