---
tag: 12AV55
kind: algorithm
slug: closest-pair-sweep-line
name: Closest pair by sweep line
aliases:
- Bentley-Shamos sweep
- plane-sweep closest pair
- sweep line closest pair
area: geometry/proximity
level: advanced
summary: Sweep points left to right while keeping a balanced tree of the active points ordered by y; O(n log n) time.
solves: [closest-pair-of-points]
model: real-ram
complexity:
  vars: {n: the number of input points}
  time: {worst: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1988
  people: [Klaus Hinrichs, Jürg Nievergelt, Peter Schorn]
  note: Hinrichs, Nievergelt and Schorn published the plane-sweep closest pair algorithm in 1988 as a simpler alternative to divide and conquer.
prereqs: [closest-pair-of-points, sweep-line-technique, sweep-status-structure, balanced-binary-search-tree]
see_also: [closest-pair-divide-and-conquer, randomized-closest-pair, closest-pair-lower-bound, segment-intersection-detection, red-black-tree]
sources:
  - paper: "Klaus Hinrichs, Jürg Nievergelt and Peter Schorn, Plane-sweep solves the closest pair problem elegantly, Information Processing Letters 26(5), 1988, 255-261"
    locator: the sweep with a y-ordered dictionary of the points within delta of the sweep line and the O(n log n) bound
  - paper: doi:10.1109/SFCS.1975.8
    title: Michael Ian Shamos and Dan Hoey, Closest-point problems, 16th Annual Symposium on Foundations of Computer Science, 1975, 151-162
    locator: the closest pair problem and the earlier O(n log n) divide and conquer solution that the sweep replaces
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 5, Proximity, fundamental algorithms (the closest pair problem and its lower bound)
  - paper: "Michiel Smid, Closest-point problems in computational geometry, in J.-R. Sack and J. Urrutia (eds.), Handbook of Computational Geometry, Elsevier, 2000, 877-935"
    locator: the survey section on the static closest pair problem, including the plane sweep algorithm
---

The sweep line algorithm for the [closest pair of points](/closest-pair-of-points/) moves a vertical line from left to right over the points sorted by $x$. It keeps the points within the current best distance $\delta$ to the left of the line in a [balanced search tree](/balanced-binary-search-tree/) ordered by $y$, and compares each new point only with the tree points whose $y$ is within $\delta$ of its own. A packing argument bounds those candidates by a constant, so the algorithm takes $\Theta(n \log n)$ time, the same as [divide and conquer](/closest-pair-divide-and-conquer/), with no recursion. All tests compare squared distances, so it is exact on integer input.

## In plain words

Sort the points from left to right and visit them in that order. Keep track of the smallest gap found so far.

When you reach a new point, only points a little to its left can beat the best gap: anything farther left than the gap is too far away and can be forgotten for good, because later points are even farther right. Keep the remembered points in a list ordered from bottom to top. Among them, look only at the ones just above and just below the new point, stopping as soon as the vertical difference reaches the best gap.

The remembered points near the new point are all at least the best gap apart, so only a handful fit in the small box that is searched. That keeps the work per point small.

## The problem

**Input.** A list $P$ of $n$ points $p = (x, y)$ with integer or rational coordinates. Duplicates and collinear points are allowed.

**Output.** For $n \ge 2$, two items $p \ne q$ of the list (different positions, possibly equal values) with the smallest squared [Euclidean distance](/euclidean-distance/) $\delta^2(P)$, and that value. For $n < 2$ there is no pair.

**Notation.** $\delta^2$ is the smallest squared distance found so far, and $\infty$ before the first pair. $T$ is the sweep status, a balanced search tree of points keyed by $(y, x, \text{index})$, so that equal points are different keys.

## The algorithm

```pseudo id=main
CLOSEST-PAIR-SWEEP(P)
L1  if n < 2 then return none
L2  sort P by (x, y)                                  ▷ P[0], …, P[n − 1] left to right
L3  best ← none; δ² ← ∞
L4  T ← empty tree keyed by (y, x, index); left ← 0
L5  for k ← 0 to n − 1 do
L6      while left < k and (P[k].x − P[left].x)² ≥ δ² do
L7          delete P[left] from T; left ← left + 1
L8      q ← successor of P[k] in T                    ▷ walk upward
L9      while q exists and (q.y − P[k].y)² < δ² do
L10         if ‖P[k] − q‖² < δ² then best ← (q, P[k]); δ² ← ‖P[k] − q‖²
L11         q ← successor of q in T
L12     q ← predecessor of P[k] in T                  ▷ walk downward
L13     while q exists and (q.y − P[k].y)² < δ² do
L14         if ‖P[k] − q‖² < δ² then best ← (q, P[k]); δ² ← ‖P[k] − q‖²
L15         q ← predecessor of q in T
L16     insert P[k] into T
L17 return (δ², best)
```

Line L6 removes the points that are at least $\delta$ to the left of the new point; since the points come in $x$-order and $\delta$ never grows, a removed point is never needed again. After line L7, $T$ holds exactly the points $P[\mathit{left}], \ldots, P[k-1]$. Lines L8 to L15 visit the points of $T$ in $y$-order on both sides of $P[k]$ and stop at the first vertical gap of at least $\delta$; $\delta$ may shrink during the walk, which only stops it earlier. If two equal points occur, $\delta^2$ becomes $0$, every later walk stops at once, and line L6 empties $T$.

The successor and predecessor in lines L8 and L12 are taken with respect to the key of $P[k]$, which is not yet in $T$. The implementation knows all keys in advance, so it uses a Fenwick tree over the $y$-ranks of the points instead of a balanced search tree; both give $O(\log n)$ time for insert, delete, successor and predecessor.

## Example

Take the points $(0,0)$, $(1,9)$, $(3,6)$, $(4,2)$, $(5,3)$, $(7,0)$, $(8,8)$, $(9,5)$, already in $x$-order. The table shows the state after line L7, the distances computed in lines L10 and L14, and $\delta^2$ after the step.

| new point | removed by L6 | $T$ in $y$-order | pairs compared (squared distance) | $\delta^2$ after |
| --- | --- | --- | --- | --- |
| $(0,0)$ | none | empty | none | $\infty$ |
| $(1,9)$ | none | $(0,0)$ | $(0,0)$: 82 | $82$ |
| $(3,6)$ | none | $(0,0), (1,9)$ | $(1,9)$: 13 | $13$ |
| $(4,2)$ | $(0,0)$ | $(3,6), (1,9)$ | none | $13$ |
| $(5,3)$ | $(1,9)$ | $(4,2), (3,6)$ | $(3,6)$: 13; $(4,2)$: 2 | $2$ |
| $(7,0)$ | $(3,6), (4,2), (5,3)$ | empty | none | $2$ |
| $(8,8)$ | none | $(7,0)$ | none | $2$ |
| $(9,5)$ | $(7,0)$ | $(8,8)$ | none | $2$ |

At $(3,6)$ the downward walk stops at $(0,0)$ because $(6 - 0)^2 = 36 \ge 13$. At $(4,2)$ the point $(1,9)$ stays in $T$ because $(4 - 1)^2 = 9 < 13$, but the upward walk stops at $(3,6)$ since $(6 - 2)^2 = 16 \ge 13$. At $(7,0)$ the gap is already $2$, and the three points with $x \le 5$ leave the tree because $(7 - 5)^2 = 4 \ge 2$. The answer is $(4,2)$, $(5,3)$ with $\delta^2 = 2$.

## Correctness

The invariant at the start of step $k$ is: $\delta^2$ is the smallest squared distance among $P[0], \ldots, P[k-1]$ (or $\infty$ for $k < 2$), and $T$ holds $P[\mathit{left}], \ldots, P[k-1]$. A point removed by line L6 is at horizontal distance at least $\delta$ from $P[k]$, hence from every later point, so it cannot form a pair closer than $\delta$ with any of them. If $P[j]$ with $j < k$ forms a pair with $P[k]$ at squared distance less than the final $\delta^2$ of step $k$, then $P[j]$ is in $T$, and every point of $T$ between $P[k]$ and $P[j]$ in $y$-order has a vertical gap to $P[k]$ smaller than that distance, so the walk in its direction reaches $P[j]$. So step $k$ keeps the invariant, and after the last step $\delta^2 = \delta^2(P)$. The full proof is in the correctness proof below.

## Complexity

- **Sorting.** Line L2 takes $O(n \log n)$ time.
- **Tree updates.** Each point is inserted once (line L16) and deleted at most once (line L7), each in $O(\log n)$ time, so all updates take $O(n \log n)$.
- **Walks.** In step $k$, every point that lines L10 and L14 compare lies in the rectangle $(P[k].x - \delta, P[k].x] \times (P[k].y - \delta, P[k].y + \delta)$, with $\delta$ taken at the start of the step. Its points other than $P[k]$ are at least $\delta$ apart, and the rectangle splits into 8 squares of side $\delta/2$, each of diameter $\delta/\sqrt{2} < \delta$, so it holds at most $8$ of them. So each step computes at most $8$ distances and makes at most $10$ successor or predecessor calls, $O(\log n)$ time per step.
- **Total.** $O(n \log n)$ time on the [real RAM](/real-ram/), and $\Theta(n)$ extra space for the sorted list and the tree. With a comparison sort in line L2 the time is $\Theta(n \log n)$ in the worst case, and it is optimal in the algebraic decision tree model by the [closest pair lower bound](/closest-pair-lower-bound/).

The details are in the complexity proof below. The tests count the distances computed per step on random and grid inputs and confirm the bound of $8$; the largest count seen was $3$.

## Properties

- **Exact.** Only differences, squares and comparisons of coordinates. No root and no division.
- **No recursion.** The whole state is the sorted array, the index $\mathit{left}$ and the tree, which makes it attractive where deep recursion is unwelcome.
- **Incremental from the left.** After step $k$ the algorithm knows the closest pair of the first $k + 1$ points in $x$-order, which the divide and conquer method does not.
- **Duplicates.** Two equal points give $\delta^2 = 0$, after which every step costs $O(\log n)$ for its tree updates and nothing else.

## Variants and improvements

- **Sorted container instead of a tree.** A sorted array with binary search gives the same walks, but each insertion and deletion moves $\Theta(n)$ entries in the worst case, so the time bound becomes $O(n^2)$ worst case, even if it is fast in practice.
- **Offline status.** Because all $y$-values are known before the sweep, the status can be a Fenwick tree or a bit vector over the $y$-ranks, as in the implementation here, instead of a dynamic tree.
- **Higher dimensions.** In $\mathbb{R}^3$ the status must answer box queries in two dimensions, which a balanced tree alone does not do; divide and conquer extends more easily.
- **All nearest neighbors.** A sweep can be adapted to find the nearest neighbor of each point, but the window must then use each point's own nearest distance and the simple packing bound no longer holds; see [all nearest neighbors](/all-nearest-neighbors/).
- **Divide and conquer and randomized grids.** [Divide and conquer](/closest-pair-divide-and-conquer/) has the same bound without a tree; the [randomized grid](/randomized-closest-pair/) is $O(n)$ expected with floor and hashing.

## When to use it

Use it when a balanced tree or an ordered map is available and a short, non-recursive, exact $O(n \log n)$ method is wanted, for example in a library that already has a [sweep line](/sweep-line-technique/) framework. It is also a good choice when points arrive sorted by $x$ and the closest pair of every prefix is of interest. Prefer the [randomized grid](/randomized-closest-pair/) for very large inputs with integer coordinates, and the [divide and conquer](/closest-pair-divide-and-conquer/) version when no ordered container is at hand.

## Pitfalls

- **Keying the tree by $y$ alone.** Two points with the same $y$ then collide, and one of them is lost or overwritten. Line L4 keys by $(y, x, \text{index})$, so equal points stay distinct items and duplicates are found.
- **A range query with $\delta$ instead of $\delta^2$.** Asking the tree for $y \in [P[k].y - \delta, P[k].y + \delta]$ needs the root $\delta$, which is irrational in general and rounded in floating point. Lines L9 and L13 test $(q.y - P[k].y)^2 < \delta^2$ while walking, which is exact.
- **Removing with a strict test.** Using $(P[k].x - P[\mathit{left}].x)^2 > \delta^2$ in line L6 is still correct but keeps more points; using the root $|P[k].x - P[\mathit{left}].x| \ge \sqrt{\delta^2}$ with floats can remove a point whose true distance is just below $\delta$ and lose the closest pair.
- **Inserting before walking.** If line L16 is moved before line L8, $P[k]$ meets itself in the tree at distance $0$ and the algorithm reports a false duplicate.
- **Assuming a stable left boundary.** Line L6 must run in a loop, not once per step, because one new point can push several old points out at once, as $(7,0)$ does in the example.

## Implementations

## History

The closest pair problem was solved in $O(n \log n)$ time by divide and conquer by Shamos and Hoey in 1975. Hinrichs, Nievergelt and Schorn published the plane-sweep algorithm in 1988 and argued that it is simpler than divide and conquer, since the only data structure is a dictionary of the points near the sweep line. The method is a standard example of the [sweep line technique](/sweep-line-technique/), together with the Shamos and Hoey sweep for [segment intersection detection](/segment-intersection-detection/). The alias "Bentley-Shamos sweep" is used in some places for this algorithm; the 1976 paper of Bentley and Shamos uses divide and conquer, not a sweep.

## References
