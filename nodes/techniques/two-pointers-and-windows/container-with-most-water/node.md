---
tag: W7YGEW
kind: problem
slug: container-with-most-water
name: Container with most water
aliases:
- maximum area between two lines
area: techniques/two-pointers-and-windows
level: intro
summary: Choose two vertical lines that, with the x-axis, hold the most water; solvable by inward two-pointer scan.
prereqs: [two-pointers, loop-invariant]
see_also: [two-pointer-pair-search, trapping-rain-water, largest-rectangle-in-histogram, adversary-argument, monotone-window-property]
sources:
  - url: https://leetcode.com/problems/container-with-most-water/
    title: LeetCode, problem 11, Container With Most Water
    locator: problem statement
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition
    locator: Chapter 4, Sorting (applications of sorting)
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 8, Algorithm design techniques (from a quadratic scan of all pairs to a linear scan)
---

The container with most water problem gives $n$ vertical lines of heights $h_0, \ldots, h_{n-1}$ at positions $0, \ldots, n-1$, and asks for two lines that, with the x-axis, form the container with the largest area $(j - i)\min(h_i, h_j)$. All pairs give a $\Theta(n^2)$ algorithm; the inward [two-pointer](/two-pointers/) scan, which always moves the shorter line, solves it in $n - 1$ steps. The proof that the scan never skips the best pair is the standard example of a two-pointer move that removes a whole row of candidate pairs at once.

## In plain words

Picture a row of walls of different heights, all one step apart. You pick two walls and pour water between them. The water level is the height of the shorter wall, and the width is the distance between the walls. You want the most water.

Start with the two walls at the ends, which give the widest container. Any other choice is narrower, so it only helps if it is taller. Now look at the shorter of the two walls. Pairing it with any wall closer in cannot help: the width shrinks and the water still cannot rise above this short wall. So this short wall is finished, and you step past it. Repeat until the two sides meet, and keep the best amount you saw.

## Definition

**Input.** An array $h[0 \ldots n-1]$ of non-negative numbers, $n \ge 2$.

**Output.** The value
$$ \mathrm{OPT}(h) = \max_{0 \le i < j \le n-1} (j - i) \cdot \min(h_i, h_j), $$
and, in the search version, a pair $(i, j)$ that attains it. Write $\mathrm{area}(i, j) = (j - i)\min(h_i, h_j)$.

Only the two chosen lines hold the water: the lines between them do not matter, and the water can stand above them. This is the difference from [trapping rain water](/trapping-rain-water/), where every bar holds water, and from the [largest rectangle in a histogram](/largest-rectangle-in-histogram/), where the rectangle must fit under every bar between its ends.

## Variants

- **Real positions.** The lines stand at positions $x_0 < x_1 < \cdots < x_{n-1}$ and the area is $(x_j - x_i)\min(h_i, h_j)$. The same scan and the same proof work, since the width still grows with $j - i$ in both directions.
- **All optimal pairs.** Report every pair with area $\mathrm{OPT}$. When all heights are positive, the scan evaluates every optimal pair, so it can list them in the same pass: the strict inequality in the proof below shows that a dropped row or column holds no pair with area $\mathrm{OPT}$ except the corner $(i, j)$, which was evaluated.
- **Minimum width for a given area.** Different problem; the scan does not apply directly.

## Examples

**The standard instance.** $h = [1, 8, 6, 2, 5, 4, 8, 3, 7]$. The answer is $49$, from the lines at positions 1 and 8: width 7, height $\min(8, 7) = 7$. The scan:

| step | $i$ | $j$ | $h_i$ | $h_j$ | area | best | move |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 8 | 1 | 7 | 8 | 8 | $h_i \le h_j$, $i \leftarrow 1$ |
| 2 | 1 | 8 | 8 | 7 | 49 | 49 | $h_i > h_j$, $j \leftarrow 7$ |
| 3 | 1 | 7 | 8 | 3 | 18 | 49 | $j \leftarrow 6$ |
| 4 | 1 | 6 | 8 | 8 | 40 | 49 | $h_i \le h_j$, $i \leftarrow 2$ |
| 5 | 2 | 6 | 6 | 8 | 24 | 49 | $i \leftarrow 3$ |
| 6 | 3 | 6 | 2 | 8 | 6 | 49 | $i \leftarrow 4$ |
| 7 | 4 | 6 | 5 | 8 | 10 | 49 | $i \leftarrow 5$ |
| 8 | 5 | 6 | 4 | 8 | 4 | 49 | $i \leftarrow 6$, stop |

The scan looks at 8 of the 36 pairs.

**All equal.** $h = [3, 3, 3, 3]$. The answer is $3 \cdot 3 = 9$, from the two end lines.

**The wrong move.** On $h = [4, 2, 1, 4, 1]$ the answer is $12$, from positions 0 and 3. A scan that moves the *taller* line first sees $\mathrm{area}(0, 4) = 4$, moves $i$ past the line of height 4, and never sees the pair $(0, 3)$; it returns 4.

## Known algorithms

**All pairs.** Compute $\mathrm{area}(i, j)$ for each of the $\binom{n}{2}$ pairs: $\Theta(n^2)$ time, $O(1)$ space.

**Inward two-pointer scan.** Start with $i = 0$, $j = n - 1$ and $best = 0$. While $i < j$: set $best \leftarrow \max(best, \mathrm{area}(i, j))$; then if $h_i \le h_j$ set $i \leftarrow i + 1$, else set $j \leftarrow j - 1$. Return $best$. It runs exactly $n - 1$ iterations, so $\Theta(n)$ time and $O(1)$ space.

*Invariant.* At each test of the loop:

> **(C)** $best = \mathrm{OPT}$, or some optimal pair $(p, q)$ has $i \le p < q \le j$.

*Why no optimal pair is skipped.* At the start the range is all of $[0, n-1]$, so (C) holds. Suppose (C) holds and $best$ has just been updated with $\mathrm{area}(i, j)$. Let $h_i \le h_j$, so the scan drops $i$. Each pair $(i, q)$ with $i < q < j$ has
$$ \mathrm{area}(i, q) = (q - i)\min(h_i, h_q) \le (q - i) h_i < (j - i) h_i = (j - i)\min(h_i, h_j) = \mathrm{area}(i, j) \le best. $$
(The middle step is strict only when $h_i > 0$; if $h_i = 0$ every pair with $i$ has area $0 \le best$.) So no pair that uses $i$ inside the range beats $best$. If an optimal pair with $p = i$ was in the range, then $best \ge \mathrm{area}(i, q) = \mathrm{OPT}$ and $best = \mathrm{OPT}$; otherwise an optimal pair with $p \ge i + 1$ is still in the new range. So (C) holds after $i \leftarrow i + 1$. The case $h_i > h_j$ is the mirror: each $(p, j)$ with $i < p < j$ has $\mathrm{area}(p, j) \le (j - p) h_j < (j - i) h_j = \mathrm{area}(i, j)$. When $h_i = h_j$, both lines are finished, and moving either one is safe.

*End.* Each iteration decreases $j - i$ by 1, so the loop stops after $n - 1$ iterations with $i = j$. No pair is left in the range, so by (C) $best = \mathrm{OPT}$.

In the language of the [two-pointer template](/two-pointers/), the corner $(i, j)$ of the open triangle of pairs dominates its whole row when $h_i \le h_j$, and its whole column when $h_i \ge h_j$.

## Bounds

**Upper bound.** $n - 1$ evaluations of $\mathrm{area}$ and $\Theta(n)$ time, by the scan.

**Lower bound.** Each correct algorithm that learns the heights only by reading them reads at least $n - 1$ of the $n$ heights on some input. Proof by an [adversary argument](/adversary-argument/). Answer every read with height 1. If the algorithm stops after reading all heights but two, at positions $k < l$, it has seen only ones, and it must answer on the input of all ones, where $\mathrm{OPT} = n - 1$. Set $h_k = h_l = n$ instead. Then $\mathrm{area}(k, l) \ge 1 \cdot n > n - 1$, the algorithm's answer is wrong on this input, and it saw the same values. So at most one height can stay unread, and the scan is optimal up to one read.

## Reductions

- **To the two-pointer template.** The problem is an instance of the opposite-ends template with VALUE$(i, j) = \mathrm{area}(i, j)$ and DROP-LEFT$(i, j) = (h_i \le h_j)$.
- **Sorted by height.** An $O(n \log n)$ alternative processes the lines from the tallest down, and for each line uses the leftmost and rightmost positions among the lines at least as tall. The pair of a line with the farthest of these is the best pair in which this line is the shorter one.

## Applications

The problem is mainly a teaching example: it is the clearest case where a two-pointer move needs a short exchange argument, and where the obvious alternative rule (move the taller line) is wrong.

## References
