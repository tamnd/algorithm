---
tag: PXWH0K
kind: algorithm
slug: histogram-stack-algorithm
name: Histogram stack algorithm
aliases:
- stack-based largest rectangle algorithm
area: sequences/subarray-problems
level: core
summary: Maintain a stack of increasing bar heights; each popped bar yields its maximal rectangle in O(n) total time.
solves: [largest-rectangle-in-histogram]
model: word-ram
complexity:
  vars: {n: the number of bars}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: true, deterministic: true, comparison: true, recursive: false}
history:
  year: 1992
  people: [David Vandevoorde]
  note: Vandevoorde found the stack of open rectangles for the maximal rectangle in a binary matrix in 1992 and published it in Dr. Dobb's Journal in April 1998; the histogram scan is the inner loop of that method.
prereqs: [largest-rectangle-in-histogram, monotonic-stack, stack, aggregate-method]
see_also: [maximal-rectangle-binary-matrix, next-greater-element, cartesian-tree, range-minimum-query, amortized-cost, loop-invariant, skyline-problem, largest-empty-rectangle]
sources:
  - url: https://www.drdobbs.com/database/the-maximal-rectangle-problem/184410529
    title: "David Vandevoorde, The Maximal Rectangle Problem, Dr. Dobb's Journal 23(4), April 1998"
    locator: the stack of open rectangles, each closed rectangle compared with the best so far
  - url: https://leetcode.com/problems/largest-rectangle-in-histogram/
    title: LeetCode, problem 84, Largest Rectangle in Histogram
    locator: problem statement and the example with heights 2, 1, 5, 6, 2, 3
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 8, Amortized analysis, the section Nearest smaller elements (the stack scan and its linear cost)
---

The histogram stack algorithm finds the [largest rectangle in a histogram](/largest-rectangle-in-histogram/) in one left-to-right pass, in $\Theta(n)$ time. It keeps a [stack](/stack/) of the indices of bars whose rectangles are still open, with heights that strictly increase from the bottom to the top. When a bar that is not higher arrives, it closes every open bar on top that is at least as high. A closed bar $k$ now knows both ends of its widest rectangle: the bar under it on the stack is the nearest lower bar on its left, and the arriving bar stops it on the right. So its area is computed at the moment it is popped. It is the [monotonic stack](/monotonic-stack/) scan with the area computed inside the pop.

## In plain words

Read the bars from left to right and keep a pile of bars that could still grow to the right. The pile always gets taller from the bottom to the top.

When a new bar comes, look at the top of the pile. If that bar is at least as tall as the new one, its rectangle cannot go any further right: the new bar is in the way. Take it off the pile. Its rectangle ends just before the new bar and starts just after the bar that is now on top of the pile, because that bar is lower. Keep its area if it is the best so far. Repeat while the top is at least as tall as the new bar, then put the new bar on the pile.

At the end, a bar of height zero arrives and closes every bar left on the pile.

## The problem

**Input.** Heights $h[0..n-1] \ge 0$.

**Output.** The largest area $(j - i + 1) \cdot \min(h[i..j])$ over all $0 \le i \le j \le n - 1$, or $0$ if $n = 0$.

## The algorithm

```pseudo id=main
LARGEST-RECTANGLE(h[0 .. n-1])
L1  S ← empty stack; best ← 0
L2  for i ← 0 to n do
L3      x ← h[i] if i < n, else 0
L4      while S is not empty and h[top(S)] ≥ x do
L5          k ← pop(S)
L6          left ← top(S) if S is not empty, else −1
L7          best ← max(best, h[k] · (i − left − 1))
L8      push i onto S
L9  return best
```

Line L3 adds a bar of height $0$ after the last bar, so that the final step closes everything that is still open. Line L4 pops the bars that the current bar stops. For a popped bar $k$, line L6 finds its left end and line L7 its area, with width $i - left - 1$, the bars strictly between $left$ and $i$.

## Example

$h = [2, 1, 5, 6, 2, 3]$. In the table, a pop is written as $k\!:\!h[k]$ with its width $i - left - 1$ and its area.

| $i$ | $x$ | pops (bar: height, width, area) | stack after | $best$ |
|---|---|---|---|---|
| 0 | 2 | none | $[0]$ | 0 |
| 1 | 1 | $0\!:\!2$, width 1, area 2 | $[1]$ | 2 |
| 2 | 5 | none | $[1, 2]$ | 2 |
| 3 | 6 | none | $[1, 2, 3]$ | 2 |
| 4 | 2 | $3\!:\!6$, width 1, area 6; $2\!:\!5$, width 2, area 10 | $[1, 4]$ | 10 |
| 5 | 3 | none | $[1, 4, 5]$ | 10 |
| 6 | 0 | $5\!:\!3$, width 1, area 3; $4\!:\!2$, width 4, area 8; $1\!:\!1$, width 6, area 6 | $[6]$ | 10 |

The answer is $10$, found when bar $2$ (height $5$) is popped at $i = 4$: the bar under it is bar $1$, so its rectangle covers bars $2$ and $3$. Each of the six bars is pushed once and popped once.

## Correctness

The stack keeps two invariants at the start of each step $i$, with $S = [s_1, \dots, s_t]$ from the bottom:

> **(S1)** $s_1 < \dots < s_t < i$ and $h[s_1] < \dots < h[s_t]$.
>
> **(S2)** For $1 \le q \le t$, every bar $l$ with $s_{q-1} < l < s_q$ has $h[l] \ge h[s_q]$, where $s_0 = -1$. For $i \ge 1$, $s_t = i - 1$.

Both hold at the start, with an empty stack. Line L4 pops only from the top, and line L8 pushes $i$ after every bar with height at least $x$ is gone, so (S1) holds again. The bars that the pops remove from between the new top and $i$ all have height at least $x = h[i]$, which keeps (S2).

*Valid areas.* When bar $k = s_q$ is popped at step $i$, the bar under it is $left = s_{q-1}$. By (S2) every bar strictly between $left$ and $k$ has height at least $h[k]$. Every bar strictly between $k$ and $i$ lies above $k$ on the stack or between such bars, so by (S1) and (S2) it is higher than $h[k]$. So the rectangle of height $h[k]$ on bars $left + 1..i - 1$ fits, and $best$ is always the area of some rectangle.

*The best area is seen.* Take a best rectangle on bars $a..b$ and let $k$ be the *rightmost* lowest bar in $a..b$. Bar $k$ is popped at the first $i > k$ with $h[i] \le h[k]$, or at $i = n$. All bars in $k+1..b$ are higher than $h[k]$, so $i > b$. When $k$ is popped, $left$ is the nearest bar to the left of $k$ that is strictly lower, so $left < a$. So the width $i - left - 1$ is at least $b - a + 1$, and the recorded area is at least the best one. The [proof page](proofs/correctness.md) gives the invariant in full.

## Complexity

- **Time.** Each index $0..n$ is pushed once in line L8, and each is popped at most once in line L5. So line L4 succeeds at most $n + 1$ times and fails exactly $n + 1$ times, and the total is $\Theta(n)$ on every input. One step can pop $\Theta(n)$ bars, as at $i = 6$ above, but by the [aggregate method](/aggregate-method/) the [amortized cost](/amortized-cost/) of a step is $O(1)$.
- **Space.** The stack holds up to $n + 1$ indices, for rising heights, so $\Theta(n)$ extra space in the worst case.
- **Comparisons.** At most $2n + 2$ comparisons of heights in line L4.

## Properties

- **Online.** Bars can arrive one at a time. A bar's area is known as soon as a bar that is not higher arrives, and the answer for the bars read so far is the larger of $best$ and the areas of the bars still on the stack.
- **One pass.** Unlike the method with separate arrays of nearest lower bars on the left and on the right, it needs only one pass and only the stack.
- **Ties.** With the test $\ge$ in line L4, equal bars close each other. The earlier of two equal bars gets a width that stops at the later one, which may be too short, but the later one, popped later, gets the full width, so the answer is right. With the test $>$, equal bars stay on the stack together. Then the left end of a popped bar can be an equal bar, which makes its width too short, but the leftmost of the equal bars gets the full width. Both forms are correct.
- **Nearest lower bars.** Line L6 gives $L_k$, the nearest strictly lower bar on the left, and $i$ gives the nearest bar on the right that is lower or equal, so the same scan fills both arrays for [next greater element](/next-greater-element/) questions with the order reversed.

## Variants and improvements

- **Report the rectangle.** Store $(left + 1, i - 1, h[k])$ when line L7 improves $best$.
- **Widths.** With bar widths $w$, keep prefix sums $W$ of the widths and use $W[i] - W[left + 1]$ in place of $i - left - 1$.
- **Binary matrix.** Run the scan on each row of column heights for the [maximal rectangle in a binary matrix](/maximal-rectangle-binary-matrix/), in $\Theta(rc)$ total time. This is the form in which Vandevoorde gave it.
- **Largest square.** Use $\min(h[k], i - left - 1)^2$ in line L7.
- **Cartesian tree.** The same pushes and pops build the [Cartesian tree](/cartesian-tree/) of the heights: when bar $k$ is popped, it becomes a child of the lower of $left$ and the arriving bar.
- **Range queries.** For many ranges of one histogram, a [range minimum query](/range-minimum-query/) structure with divide at the minimum is more flexible.

## When to use it

Use it for any question about the widest stretch around each item where all items are at least as large, and in particular for the largest rectangle under a histogram and the largest rectangle of ones in a binary matrix. It is linear and simple. When the stretch must be bounded by items at both ends, as in [container with most water](/container-with-most-water/), the stack is the wrong tool and two pointers are right.

## Pitfalls

- **No final sentinel.** Without the bar of height $0$ at $i = n$, the bars that are still on the stack at the end are never closed. For rising bars $[1, 2, 3]$, nothing is popped and the answer $4$ is missed.
- **Wrong left end.** The left end of a popped bar is the bar *now* under it on the stack, not $k$ itself. Using $i - k$ as the width misses the bars to the left of $k$ that were popped earlier. In the example, bar $1$ would get width $5$ at $i = 6$ instead of $6$.
- **Pushing heights instead of indices.** The widths need positions, so the stack must hold indices.
- **Overflow.** The area can be up to $n \max h$, which can exceed the type of the heights.

## Implementations

## History

The all nearest smaller values problem, which the stack scan solves, is old and appears in the parsing and parallel algorithm literature. For the largest rectangle, David Vandevoorde found the stack of open rectangles in 1992 for the maximal rectangle in a binary matrix and published it in Dr. Dobb's Journal in April 1998. The histogram problem on its own became a standard exercise, as LeetCode problem 84.

## References
