---
tag: 48TJ7A
kind: algorithm
slug: interval-partitioning-greedy
name: Interval partitioning greedy
aliases:
- Greedy by start time with a min-heap of free times
- Meeting rooms greedy
area: sequences/interval-problems
level: core
summary: Sort by start time and reuse the resource that becomes free earliest, opening a new one only when none is free.
solves: [interval-partitioning]
model: comparison-model
complexity:
  vars: {n: the number of intervals, d: the depth of the intervals}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [interval-partitioning, binary-heap, priority-queue, loop-invariant]
see_also: [interval-coloring-depth-theorem, sweep-maximum-overlap, maximum-overlap, greedy-coloring, chordal-graph, perfect-elimination-ordering, k-machine-interval-scheduling, earliest-finish-time-first]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.1, Interval Scheduling, the subsection on interval partitioning (the greedy by start time and the depth bound)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 15.1, the exercise on scheduling all activities in the fewest lecture halls
  - paper: doi:10.1145/330249.330250
    title: "Massimiliano Poletto and Vivek Sarkar, Linear scan register allocation, ACM Transactions on Programming Languages and Systems 21(5) (1999), pages 895 to 913"
    locator: the allocation of live intervals in order of start point
---

The interval partitioning greedy assigns $n$ intervals to the fewest resources so that no two intervals on one resource meet, which solves [interval partitioning](/interval-partitioning/). It takes the intervals by start time and keeps a min-heap of the times at which the open resources become free; each interval reuses the resource that becomes free first if that resource is already free, and opens a new one otherwise. It uses exactly $d$ resources, where $d$ is the [depth](/maximum-overlap/), and it runs in $\Theta(n \log n)$ time. The only line that depends on the end point type is the test "free in time": a resource that frees at $x$ can take an interval that starts at $x$ for half-open and open intervals, but not for closed ones.

## In plain words

Think of lecture rooms. Go through the lectures in order of their start. For each one, look at the room that becomes empty first. If it is already empty when the lecture starts, use it. If even that room is still busy, every room is busy, so open a new room.

Whenever a new room opens, all the other rooms hold a lecture that is still going on at that moment, and the new lecture starts then too. So that many lectures run at one moment, and no plan can do with fewer rooms.

Whether a room that empties at ten can take a lecture that starts at ten depends on whether the lecture times include their end moment.

## The problem

The input is a list $I[1 \ldots n]$ of intervals of one type. The output is a number $k$ and a label $res[j] \in \{1, \ldots, k\}$ for each interval such that two intervals with the same label are disjoint, with $k$ as small as possible. For closed intervals $[l, r]$ two intervals that share an end point are not disjoint; for half-open $[l, r)$ and open $(l, r)$ intervals they are. The [depth theorem](/interval-coloring-depth-theorem/) says that the smallest $k$ is the depth $d$.

## The algorithm

```pseudo id=main
PARTITION(I[1 .. n])                    ▷ half-open intervals [l, r)
L1  order ← the indices 1 .. n sorted by l ascending
L2  H ← an empty min-heap of pairs (free time, resource), k ← 0
L3  for each j in order do
L4      if H is not empty and H.min.time ≤ I[j].l then     ▷ closed: H.min.time < I[j].l
L5          (t, c) ← EXTRACT-MIN(H)        ▷ resource c is free when I[j] starts
L6      else k ← k + 1, c ← k              ▷ every open resource is busy at I[j].l
L7      res[j] ← c, INSERT(H, (I[j].r, c))
L8  return (k, res)
```

The heap holds one pair per open resource: the right end of the last interval on it, and its number. Line L4 looks only at the minimum, because if the resource that frees first is still busy at $I[j].l$, so are all the others. For half-open intervals, a resource whose last interval is $[l', r')$ is free at $x$ when $r' \le x$; for closed intervals $[l', r']$, when $r' < x$. Open intervals behave like half-open ones. Line L7 puts the resource back with its new free time.

## Example

Take the intervals with end points $(1, 3), (2, 5), (3, 4), (5, 8), (6, 7), (8, 9), (7, 10)$, the example of the [maximum overlap](/maximum-overlap/) page. Line L1 gives the order $(1, 3), (2, 5), (3, 4), (5, 8), (6, 7), (7, 10), (8, 9)$.

*As half-open intervals* (touching intervals can share a resource):

| interval | heap minimum | test of L4 | resource | heap after |
|---|---|---|---|---|
| $[1, 3)$ | none | none | open 1 | $(3, 1)$ |
| $[2, 5)$ | $(3, 1)$ | $3 \le 2$ fails | open 2 | $(3, 1), (5, 2)$ |
| $[3, 4)$ | $(3, 1)$ | $3 \le 3$, a touch | 1 | $(4, 1), (5, 2)$ |
| $[5, 8)$ | $(4, 1)$ | $4 \le 5$ | 1 | $(5, 2), (8, 1)$ |
| $[6, 7)$ | $(5, 2)$ | $5 \le 6$ | 2 | $(7, 2), (8, 1)$ |
| $[7, 10)$ | $(7, 2)$ | $7 \le 7$, a touch | 2 | $(8, 1), (10, 2)$ |
| $[8, 9)$ | $(8, 1)$ | $8 \le 8$, a touch | 1 | $(9, 1), (10, 2)$ |

Two resources: $\{[1, 3), [3, 4), [5, 8), [8, 9)\}$ and $\{[2, 5), [6, 7), [7, 10)\}$. The depth is 2, reached at the point 2.

*As closed intervals*, the touches at 3, 7 and 8 are conflicts. $[3, 4]$ finds the minimum $(3, 1)$, and $3 < 3$ fails, so it opens resource 3; the rest reuse resources. The result is $\{[1, 3], [5, 8]\}$, $\{[2, 5], [7, 10]\}$, $\{[3, 4], [6, 7], [8, 9]\}$, three resources, and the depth is 3, at the point 3. When resource 3 opens, the last intervals $[1, 3]$ and $[2, 5]$ of resources 1 and 2 and the new interval $[3, 4]$ all contain 3.

## Correctness

Two facts give correctness. First, the labels are valid: an interval goes to resource $c$ only when the last interval on $c$ ends in time, by the test of line L4, and every earlier interval on $c$ ends even sooner, so the intervals on one resource are pairwise disjoint. Second, the count is optimal: when line L6 opens resource $k$, the heap holds $k - 1$ resources, each busy at $x = I[j].l$. The last interval on each of them starts at or before $x$, because of the order of line L1, and it is still busy at $x$, so it contains $x$. With $I[j]$, that is $k$ intervals through $x$, so $k \le d$. Every valid labeling needs at least $d$ labels, since the $d$ intervals through one point pairwise meet. So $k = d$. The [proof](proofs/correctness.md) states the invariant and handles the three types.

## Complexity

- **Time.** The sort of line L1 takes $\Theta(n \log n)$. The loop does $n$ steps, each with at most one EXTRACT-MIN and one INSERT on a heap of at most $d$ pairs, so $O(n \log d)$ time. The total is $\Theta(n \log n)$ in the worst case.
- **Space.** $\Theta(n)$ for $order$ and $res$, and $O(d)$ for the heap.
- **Lower bound.** Computing $d$ alone needs $\Omega(n \log n)$ operations in the algebraic decision tree model, by the element distinctness reduction on the [maximum overlap](/maximum-overlap/) page, so the greedy is optimal there.

## Properties

- **Any free resource works.** The proof only needs that some free resource is used when one exists. The heap is one way to find a free resource fast; a resource that frees later but is still free in time also works.
- **Gives a witness.** The interval that opens resource $d$ and the last intervals of the other $d - 1$ resources are $d$ intervals through one point, a certificate that $d$ resources are needed.
- **Optimal coloring of an interval graph.** The labels are an optimal coloring of the interval graph, and the order of line L1 is the reverse of a [perfect elimination ordering](/perfect-elimination-ordering/), so this is [greedy coloring](/greedy-coloring/) of a [chordal graph](/chordal-graph/) in that order.
- **Online in the order of start.** It needs the intervals in order of start, but then it decides each one at once. If the intervals arrive in another order, the proof of optimality does not apply.

## Variants and improvements

- **Lowest free label.** To give each interval the smallest free resource number, keep a second min-heap of free labels: move the labels whose time has come from $H$ to it before each step. Same bound.
- **Only the depth.** Drop the labels and keep only the size of the heap, or use the [sweep for maximum overlap](/sweep-maximum-overlap/), which needs no heap.
- **Integer times.** For integer end points in a range of size $U$, sorting by counting and a free list per time step give $O(n + U)$ time.
- **A fixed number of resources.** With only $k$ resources, the problem changes to choosing the most intervals that fit, [k-machine interval scheduling](/k-machine-interval-scheduling/); the greedy here does not apply.
- **Register allocation.** Linear scan register allocation, by Poletto and Sarkar, walks the live intervals in order of start point with a list of active intervals sorted by end point, in the same way, and spills when the registers run out.

## When to use it

Use it to assign rooms, gates, platforms or machines to jobs with fixed times, or to color an interval graph given by its intervals. If only the number of resources is needed, the counting sweep is simpler. If the intervals come one by one in an arbitrary order and must be placed at once, the guarantee of $d$ resources is lost. If resources are limited, solve the $k$-machine scheduling problem instead.

## Pitfalls

- **The wrong test for the type.** With $\le$ in line L4 for closed intervals, $[1, 3]$ and $[3, 4]$ share a resource though they meet at 3. With $<$ for half-open intervals, $[1, 3)$ and $[3, 4)$ get two resources, and the result exceeds the depth.
- **Sorting by end time.** Taking intervals by right end, not by left end in line L1, breaks the proof. For $[0, 1), [0, 2), [2, 3), [1, 4)$, in this order by right end, the rule opens resources 1 and 2 for the first two, puts $[2, 3)$ on resource 1, and then finds both resources busy at 1 for $[1, 4)$, so it opens resource 3. The depth is 2, and the two resources $\{[0, 1), [1, 4)\}$ and $\{[0, 2), [2, 3)\}$ are enough.
- **Testing all resources.** Scanning every open resource at each step is correct but takes $O(nd)$ time; the heap minimum is enough, by the argument under line L4.
- **Forgetting to reinsert.** If line L7 does not push the reused resource back, resources disappear, and line L6 opens more than needed.

## Implementations

## History

Kleinberg and Tardos present this greedy as the algorithm for interval partitioning and prove that it uses as many resources as the depth; CLRS give the problem as an exercise in its section on activity selection. The same pass over live intervals in order of start is the basis of linear scan register allocation, by Poletto and Sarkar in 1999.

## References
