---
tag: 5KC31P
kind: technique
slug: monotonic-stack
name: Monotonic stack
aliases:
- stack-based nearest greater or smaller
area: data-structures/linear-structures
level: intro
summary: Stack kept in monotone order so nearest greater or smaller elements are found in linear time.
prereqs: [stack, array, amortized-cost, loop-invariant]
see_also: [next-greater-element, monotonic-deque, largest-rectangle-in-histogram, histogram-stack-algorithm, cartesian-tree, trapping-rain-water, andrew-monotone-chain, min-stack]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook (free PDF edition)
    locator: Chapter 8, Amortized analysis, the section Nearest smaller elements
  - paper: doi:10.1006/jagm.1993.1018
    title: Omer Berkman, Baruch Schieber and Uzi Vishkin, Optimal doubly logarithmic parallel algorithms based on finding all nearest smaller values, Journal of Algorithms 14(3) (1993)
    locator: pp. 344 to 370
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.2.1, Stacks, queues, and deques
---

A monotonic stack is a [stack](/stack/) of array positions whose items stay in sorted order from the bottom to the top, kept that way by popping every item that the new item would break the order with. One left-to-right scan with such a stack finds, for every position of an [array](/array/), its nearest smaller or greater item on the left, and its nearest smaller or greater item on the right, in $\Theta(n)$ total time, although a single step can take $\Theta(n)$. It solves the [next greater element](/next-greater-element/) problem and its mirror forms, and through them the [largest rectangle in a histogram](/largest-rectangle-in-histogram/), the [Cartesian tree](/cartesian-tree/) and many questions of the form "how far does this item reach before a larger one stops it".

## In plain words

You read a row of numbers from left to right and keep a pile of the numbers that are still "open". The pile always goes up from the bottom to the top. When a new number comes, every open number on top of the pile that is not smaller than the new one is closed: the new number is the first smaller number to its right. It can never be the answer for anyone later, because the new number is smaller and closer. You take those numbers off the pile and record their answers. The number that is now on top is the first smaller number to the left of the new one. Then the new number goes on the pile.

Each number goes on the pile once and comes off at most once, so the whole scan does work in proportion to the length of the row.

## When it applies

- The question for each position $i$ is about the **nearest** position to the left or right whose item beats $A[i]$ in a fixed order: the first greater, the first smaller, the first at least as large.
- A position that is **dominated** can be thrown away for good. In the left-to-right scan for "previous smaller", a position $k < i$ with $A[k] \ge A[i]$ is never the answer for a position after $i$, because $i$ is closer and at least as small.
- The quantity of interest is a **span**: how far $A[i]$ is the minimum or the maximum. The span of $A[i]$ as a minimum is the open interval between its previous smaller and its next smaller position.
- The order of the scan is fixed and each item is seen once. If items also leave from the old end, as in a [sliding window](/sliding-window/), use a [monotonic deque](/monotonic-deque/) instead.

## The template

The holes are POPS (the test that closes the top), RESOLVE (what to do when position $k$ is closed by position $i$), VISIT (what to do with $i$ and its nearest survivor on the left) and FINISH (what to do with the positions that are never closed).

```pseudo id=main
MONOTONIC-SCAN(A)                          ▷ A[0 .. n − 1]
L1  S ← an empty stack of positions
L2  for i ← 0 to n − 1 do
L3      while S is not empty and POPS(A[TOP(S)], A[i]) do
L4          k ← POP(S)
L5          RESOLVE(k, i)                   ▷ i is the nearest closer of k on the right
L6      VISIT(i, TOP(S) or nil)             ▷ the top is the nearest survivor on the left
L7      PUSH(S, i)
L8  for each k still in S do FINISH(k)      ▷ no closer on the right
```

With POPS$(x, y) = (x \ge y)$, the items on the stack strictly increase from the bottom to the top. Then RESOLVE$(k, i)$ receives the next smaller or equal position of $k$, VISIT$(i, t)$ receives the previous strictly smaller position $t$ of $i$, and FINISH gets the positions with no smaller or equal item on the right. The other three choices give the other directions:

| POPS$(x, y)$ | stack from bottom to top | RESOLVE gets the next | VISIT gets the previous |
|---|---|---|---|
| $x \ge y$ | strictly increasing | smaller or equal | strictly smaller |
| $x > y$ | non-decreasing | strictly smaller | smaller or equal |
| $x \le y$ | strictly decreasing | greater or equal | strictly greater |
| $x < y$ | non-increasing | strictly greater | greater or equal |

**Invariant.** Before line L3 in round $i$, the stack holds, from the bottom to the top, exactly the positions $k < i$ with no position $j$, $k < j < i$, such that POPS$(A[k], A[j])$. In words: the positions not yet closed. With POPS$(x, y) = (x \ge y)$ these are the "suffix minima" of $A[0 \ldots i-1]$, and their items increase strictly. The loop of line L3 removes exactly the positions that $i$ closes: they are on top, because the items increase towards the top and POPS is monotone in $x$. The first survivor is the nearest position $t < i$ with $A[t] < A[i]$, because every position $m$ between $t$ and $i$ was closed by a chain of positions $m < j_1 < \cdots < j_r = i$, each closing the one before, so $A[m] \ge A[j_1] \ge \cdots \ge A[i]$, while $A[t] < A[i]$.

**Cost.** Line L7 runs $n$ times, so there are $n$ pushes, and so at most $n$ pops in total. Each test of line L3 either pops (at most $n$ times over the whole scan) or ends the loop (once per round). So the scan does $\Theta(n)$ work plus the cost of the holes. This is the aggregate form of [amortized analysis](/amortized-cost/): one round can pop $i$ items, but the average round costs $O(1)$. With the potential $\Phi = |S|$, a round that pops $p$ positions costs $1 + p$ units (one for each pop and one for the push) and changes $\Phi$ by $1 - p$, so its amortized cost is $2$. This gives the same bound by the [potential method](/potential-method/). The extra space is at most $n$ positions, reached on a sorted input.

## Classic examples

### Next greater element

[Next greater element](/next-greater-element/) uses POPS$(x, y) = (x < y)$, RESOLVE$(k, i)$ sets $N[k] = i$, and FINISH$(k)$ sets $N[k] = \bot$. VISIT is empty, or it records the previous greater or equal element for free.

### Largest rectangle in a histogram

In the [largest rectangle in a histogram](/largest-rectangle-in-histogram/), the best rectangle that uses the full height of bar $i$ spans the open interval between the previous and the next strictly lower bars. Take POPS$(x, y) = (x \ge y)$, let VISIT record $L[i] = t$ (or $-1$), and let RESOLVE and FINISH record $R[k] = i$ (or $n$). The answer is $\max_i h_i (R[i] - L[i] - 1)$. Ties close with the later equal bar, so $R[k]$ can stop too early for a bar with an equal bar on its right. That later equal bar then has the full interval, so the maximum stays right.

For $h = [2, 1, 5, 6, 2, 3]$:

| $i$ | $h_i$ | closed by $i$ | $L[i]$ | stack after (positions) | heights on the stack |
|---|---|---|---|---|---|
| 0 | 2 | none | $-1$ | 0 | 2 |
| 1 | 1 | 0 | $-1$ | 1 | 1 |
| 2 | 5 | none | 1 | 1, 2 | 1, 5 |
| 3 | 6 | none | 2 | 1, 2, 3 | 1, 5, 6 |
| 4 | 2 | 3, then 2 | 1 | 1, 4 | 1, 2 |
| 5 | 3 | none | 4 | 1, 4, 5 | 1, 2, 3 |
| end | | 5, 4, 1 get $R = 6$ | | | |

So $R = [1, 6, 4, 4, 6, 6]$ and $L = [-1, -1, 1, 2, 1, 4]$. The areas are $2, 6, 10, 6, 8, 3$, and the largest is 10: height 5 over the bars 2 and 3. The [histogram stack algorithm](/histogram-stack-algorithm/) is this scan with the area computed inside RESOLVE.

### Cartesian tree

A [Cartesian tree](/cartesian-tree/) of distinct items is built by the same scan with POPS$(x, y) = (x > y)$ for a min-tree: the last position popped in round $i$ becomes the left child of $i$, and $i$ becomes the right child of the new top. The stack is the right spine of the tree built so far. The build takes $\Theta(n)$ time.

### Trapping rain water

In [trapping rain water](/trapping-rain-water/), with POPS$(x, y) = (x < y)$, a bar $k$ popped by a higher bar $i$ is the floor of a pool whose walls are $i$ and the new top $t$. The pool adds $(\min(h_t, h_i) - h_k)(i - t - 1)$ units. If the stack is empty after the pop, no pool forms. This fills the water layer by layer in one scan.

### Monotone chain convex hull

[Andrew's monotone chain](/andrew-monotone-chain/) algorithm sorts the points by $x$ and keeps each hull chain on a stack whose consecutive triples all turn the same way. A new point pops the points that would make a wrong turn. The order is on turns, not on values, but the cost argument is the same: each point is pushed once per chain and popped at most once.

## Variations

- **Values or positions.** Store positions, not items. A position gives both the item and the distance, which most uses need.
- **Right-to-left scan.** Scan from $n - 1$ down to 0 and keep the candidates for the answer instead of the positions that wait for one. VISIT then gets the next greater or smaller element directly, and no FINISH is needed.
- **Two passes for both sides.** One pass gives the previous neighbour in VISIT and the next neighbour in RESOLVE at once, so one scan is enough even when both sides are needed. Two separate passes are easier to get right with ties.
- **Circular arrays.** Run the scan over $i = 0, \ldots, 2n - 1$ with $A[i \bmod n]$, and push only in the first lap.
- **Monotonic deque.** If positions also leave from the bottom when they fall out of a window, the stack becomes a [monotonic deque](/monotonic-deque/), and the bottom is the minimum of the window.
- **Greedy subsequences.** To delete $k$ digits from a number so that the rest is as small as possible, scan the digits and pop a larger digit on top while deletions remain. The kept digits form a non-decreasing stack.
- **Parallel.** Berkman, Schieber and Vishkin solve all nearest smaller values in $O(\log \log n)$ time with linear work on a CRCW PRAM.

## Pitfalls

- **The wrong comparison for ties.** For the sum of the minimums of all subarrays, each subarray must count its minimum once. With strict comparisons on both sides, a subarray with two equal minimums counts twice. Use "strictly smaller" on one side and "smaller or equal" on the other, which the template gives with one POPS, as in the first row of the table.
- **A test on an empty stack.** Line L3 must test that $S$ is not empty before it reads TOP$(S)$, and line L6 must pass nil when the stack is empty. A sentinel item smaller than every input at the bottom of the stack also works, but it must never be resolved.
- **Forgetting the positions that are never closed.** Positions still on the stack after the loop have no answer on the right. If the program only writes answers in RESOLVE, those entries keep their old value. Initialise the output to $\bot$ or run line L8.
- **Storing items instead of positions.** With items only, widths and distances are lost, and equal items cannot be told apart.
- **A per-step bound.** The bound is amortized. A real-time use that needs $O(1)$ for each step cannot use the plain template: a decreasing run followed by a small item makes one round pop $\Theta(n)$ positions.

## Exercises

1. Show that MONOTONIC-SCAN does at most $2n - 1$ stack operations on $n \ge 1$ items, and find an input that needs exactly that many.
2. Give the holes that compute, for each $i$, the number of subarrays in which $A[i]$ is the leftmost minimum, and use them to compute the sum of the minimums of all subarrays in $\Theta(n)$ time.
3. Solve the circular next greater element problem in $\Theta(n)$ time with one stack.
4. Given a string of digits and a number $k$, delete $k$ digits so that the remaining number is as small as possible. Prove that the greedy monotonic stack gives the optimum.

## References
