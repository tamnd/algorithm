---
tag: B2J1EZ
kind: problem
slug: trapping-rain-water
name: Trapping rain water
aliases:
- rain water trapping
area: techniques/two-pointers-and-windows
level: intro
summary: Given elevation bars, compute the total water trapped between them; solvable in O(n) time and O(1) space with two pointers.
prereqs: [two-pointers, prefix-sums, loop-invariant]
see_also: [container-with-most-water, monotonic-stack, largest-rectangle-in-histogram, adversary-argument, prefix-sums]
sources:
  - url: https://leetcode.com/problems/trapping-rain-water/
    title: LeetCode, problem 42, Trapping Rain Water
    locator: problem statement
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 8, Algorithm design techniques (scanning algorithms that keep a summary of the prefix)
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition
    locator: Chapter 3, Data structures (stacks and queues)
---

The trapping rain water problem gives an elevation map of $n$ bars of width 1 and heights $h_0, \ldots, h_{n-1}$, and asks how much water stays on it after rain. The water above bar $k$ is $\min(L_k, R_k) - h_k$, where $L_k$ and $R_k$ are the highest bars at or to the left and at or to the right of $k$. [Prefix sums](/prefix-sums/) style running maxima solve it in $O(n)$ time and $O(n)$ space, a [monotonic stack](/monotonic-stack/) also in $O(n)$, and a [two-pointer](/two-pointers/) scan in $O(n)$ time and $O(1)$ extra space.

## In plain words

Think of the bars as a cross-section of a landscape, and let rain fill every pit. The water above one bar rises until it would spill over the left or the right. It spills over the lower of two walls: the highest bar on the left and the highest bar on the right. So the water level over a bar is the smaller of these two maxima, and the water depth is that level minus the bar height.

The two-pointer method works from both ends. It keeps the highest bar seen from the left and the highest seen from the right. Whichever side has the lower maximum is the side where the level is already known: the other side is surely at least as high. So it fills the next bar on that side and moves inward.

## Definition

**Input.** An array $h[0 \ldots n-1]$ of non-negative numbers, $n \ge 0$.

**Output.** The total trapped water
$$ W(h) = \sum_{k=0}^{n-1} w_k, \qquad w_k = \min(L_k, R_k) - h_k, $$
where $L_k = \max(h_0, \ldots, h_k)$ and $R_k = \max(h_k, \ldots, h_{n-1})$.

Since $L_k \ge h_k$ and $R_k \ge h_k$, each $w_k \ge 0$. The two end bars hold no water: $w_0 = 0$ because $L_0 = h_0$, and $w_{n-1} = 0$ because $R_{n-1} = h_{n-1}$.

## Variants

- **Water per bar.** Return the array $(w_0, \ldots, w_{n-1})$ instead of the sum.
- **Two dimensions.** Heights on an $m \times n$ grid, where water can leak in four directions. The level of a cell is the lowest "highest point" on a path to the border. A priority queue that grows the region from the border inward, always from the lowest boundary cell, solves it in $O(mn \log(mn))$ time. The one-dimensional two-pointer argument does not carry over.
- **Bars of different widths.** Each bar has a width $b_k$, and the water is $\sum_k b_k w_k$. The levels are the same.
- **Container with most water.** A different problem: only two chosen lines hold water, and the lines between them do not matter. See [container with most water](/container-with-most-water/).

## Examples

**The standard instance.** $h = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]$. The water per bar is $[0, 0, 1, 0, 1, 2, 1, 0, 0, 1, 0, 0]$, and $W = 6$.

**A trace of the two-pointer scan.** $h = [4, 2, 0, 3, 2, 5]$, with answer $W = 9$. Here $lm$ and $rm$ are the running maxima from the left and from the right, both 0 at the start.

| step | side | bar $k$ | $h_k$ | $lm$ after | $rm$ after | $w_k$ | total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | left, $lm \le rm$ | 0 | 4 | 4 | 0 | 0 | 0 |
| 2 | right, $lm > rm$ | 5 | 5 | 4 | 5 | 0 | 0 |
| 3 | left | 1 | 2 | 4 | 5 | 2 | 2 |
| 4 | left | 2 | 0 | 4 | 5 | 4 | 6 |
| 5 | left | 3 | 3 | 4 | 5 | 1 | 7 |
| 6 | left | 4 | 2 | 4 | 5 | 2 | 9 |

From step 3 on, $lm = 4 \le rm = 5$, so the level over each remaining bar is 4, set by the left wall: the right side is known to have a wall of height 5.

**No water.** A non-decreasing or non-increasing $h$ holds no water, and neither does a single peak such as $[1, 3, 2]$.

## Known algorithms

| algorithm | time | extra space |
| --- | --- | --- |
| for each bar, scan left and right for the maxima | $\Theta(n^2)$ | $O(1)$ |
| running maxima: arrays $L$ and $R$, then the sum | $\Theta(n)$ | $\Theta(n)$ |
| [monotonic stack](/monotonic-stack/) of bars with decreasing heights | $\Theta(n)$ | $O(n)$ |
| two pointers | $\Theta(n)$ | $O(1)$ |

**Running maxima.** Fill $L$ from the left by $L_k = \max(L_{k-1}, h_k)$ and $R$ from the right by $R_k = \max(R_{k+1}, h_k)$, then add the $w_k$. This follows the definition directly.

**Monotonic stack.** Scan from the left and keep a stack of positions with decreasing heights. When $h_k$ is higher than the top, pop the top $b$; if the stack is not empty, its new top $a$ and position $k$ are walls around $b$, and the layer of width $k - a - 1$ and height $\min(h_a, h_k) - h_b$ is water. This counts the water in horizontal layers instead of vertical columns.

**Two pointers.** Keep $lo = 0$, $hi = n - 1$, $lm = 0$, $rm = 0$ and $W = 0$. While $lo \le hi$: if $lm \le rm$, set $lm \leftarrow \max(lm, h_{lo})$, add $lm - h_{lo}$ to $W$ and increase $lo$; else set $rm \leftarrow \max(rm, h_{hi})$, add $rm - h_{hi}$ to $W$ and decrease $hi$. The loop keeps this invariant:

> **(R)** $lm = \max(h_0, \ldots, h_{lo-1})$ and $rm = \max(h_{hi+1}, \ldots, h_{n-1})$, with the maximum of an empty range equal to 0, and $W = \sum_{k < lo} w_k + \sum_{k > hi} w_k$.

*Why the water at the moved bar is exact.* Take the case $lm \le rm$ and $k = lo \le hi$. Then $L_k = \max(lm, h_k)$ by (R). On the right, $R_k \ge h_k$, and $R_k \ge rm \ge lm$ because the bars $hi + 1, \ldots, n - 1$ lie to the right of $k$. So $R_k \ge \max(lm, h_k) = L_k$, which gives $\min(L_k, R_k) = L_k$ and $w_k = \max(lm, h_k) - h_k$. This is exactly what the step adds, and the new $lm$ is $\max(h_0, \ldots, h_k)$, so (R) holds with $lo + 1$. The case $lm > rm$ is the mirror: $L_k \ge lm > rm$, so $w_k = \max(rm, h_k) - h_k$. Each bar is filled once, with its exact water, and the scan never needs to come back to it. When the loop stops, $lo = hi + 1$ and (R) gives $W = \sum_k w_k$. The loop runs exactly $n$ times.

The rule "move the side with the lower maximum" is what makes the scan correct. The level over a bar needs both maxima, but only the smaller one matters, and the side with the smaller running maximum is the side where the smaller one is already known.

## Bounds

**Upper bound.** $\Theta(n)$ time and $O(1)$ extra space, by the two-pointer scan, with $n$ steps and one maximum, one subtraction and one addition in each.

**Lower bound.** For $n \ge 3$, each algorithm that learns the heights only by reading them must read all $n$ heights on some input. Take $h = [1, 0, 0, \ldots, 0, 1]$, with $W = n - 2$. If an algorithm does not read $h_k$ for some interior $k$, set $h_k = 1$ instead; then $W = n - 3$. If it does not read $h_0$, set $h_0 = 0$; then no bar on the left can hold water and $W = 0$. The case of $h_{n-1}$ is the mirror. In each case the algorithm sees the same values and gives the same answer for two inputs with different answers. This is an [adversary argument](/adversary-argument/), and it shows that the scan is optimal.

## Reductions

- **To two prefix maxima.** $W = \sum_k \min(L_k, R_k) - \sum_k h_k$, and $L$ and $R$ are prefix and suffix maxima, the max analog of [prefix sums](/prefix-sums/).
- **Shape of the water level.** The water level $\min(L_k, R_k)$ is the lower envelope of two staircases, one non-decreasing and one non-increasing. The level is non-decreasing up to the first highest bar and non-increasing after the last one.
- **Split at the maximum.** Let $m$ be a position of the highest bar. Left of $m$ the level is $L_k$, and right of $m$ it is $R_k$. So two one-sided scans toward $m$ also solve the problem; the two-pointer scan does the same without finding $m$ first.

## Applications

- **Terrain and reservoirs.** The one-dimensional model of how much water a cross-section holds; the two-dimensional version models pits on a height map.
- **Teaching two pointers.** The problem shows a two-pointer move whose safety comes from comparing running maxima, not the current items.

## References
