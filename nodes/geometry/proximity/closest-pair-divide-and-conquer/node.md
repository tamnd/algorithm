---
tag: N8YEH7
kind: algorithm
slug: closest-pair-divide-and-conquer
name: Closest pair by divide and conquer
aliases:
- Shamos closest pair algorithm
- Shamos-Hoey closest pair
- divide and conquer closest pair
area: geometry/proximity
level: core
summary: Split by the median x, recurse on both halves, then scan a y-sorted strip; O(n log n) time.
solves: [closest-pair-of-points]
model: real-ram
complexity:
  vars: {n: the number of input points}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: true}
history:
  year: 1975
  people: [Michael Ian Shamos, Dan Hoey, Jon Louis Bentley]
  note: Shamos and Hoey gave the planar divide and conquer algorithm in 1975, and Bentley and Shamos extended divide and conquer to closest pairs in any fixed dimension in 1976.
prereqs: [closest-pair-of-points, euclidean-distance, divide-and-conquer-paradigm, merge-sort]
see_also: [closest-pair-sweep-line, randomized-closest-pair, closest-pair-lower-bound, all-nearest-neighbors, bichromatic-closest-pair, divide-and-conquer-recurrence]
sources:
  - paper: doi:10.1109/SFCS.1975.8
    title: Michael Ian Shamos and Dan Hoey, Closest-point problems, 16th Annual Symposium on Foundations of Computer Science, 1975, 151-162
    locator: the divide and conquer closest pair algorithm in the plane and its O(n log n) bound
  - paper: doi:10.1145/800113.803652
    title: Jon Louis Bentley and Michael Ian Shamos, Divide-and-conquer in multidimensional space, Proceedings of the 8th Annual ACM Symposium on Theory of Computing (STOC 1976), 220-230
    locator: the closest pair in d dimensions in O(n log n) time by divide and conquer and the sparsity of the slab
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 33, Section 33.4, Finding the closest pair of points (presorting, the strip, and the bound of 7 points after each strip point)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Chapter 5, Section 5.4, Finding the closest pair of points (the packing argument with boxes of side delta/2)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 5, Section 5.4 (the closest pair problem, a divide and conquer approach)
---

The divide and conquer algorithm for the [closest pair of points](/closest-pair-of-points/) splits the points by a vertical line through the median $x$-coordinate, solves both halves recursively, and then checks only the pairs that cross the line inside a narrow strip. A packing argument shows that each strip point needs to be compared with at most 7 points that follow it in $y$-order. With one presort by $y$ that is split, not re-sorted, at each level, it runs in $\Theta(n \log n)$ time, which is optimal in the [algebraic decision tree](/algebraic-decision-tree/) model by the [closest pair lower bound](/closest-pair-lower-bound/). It compares only squared distances, so it is exact on integer input.

## In plain words

Draw a vertical line that cuts the points into a left half and a right half. Find the closest pair on each side with the same method. Call the smaller of the two answers the best gap so far.

The only pairs not checked yet have one point on each side. Such a pair can beat the best gap only if both points are close to the line, within one best gap of it. So keep only the points in that narrow band, and list them from bottom to top. A point in the band only needs to be compared with the next few points in the list, because points on the same side are at least one best gap apart, and only a few of them fit in a small box. This makes the work after the two calls linear.

## The problem

**Input.** A list $P$ of $n$ points $p = (x, y)$ with integer or rational coordinates. Duplicates and collinear points are allowed.

**Output.** For $n \ge 2$, a pair of items $p \ne q$ of the list (different positions, possibly equal values) with the smallest squared distance $\delta^2(P) = \min \|p - q\|^2$, and that squared distance. For $n < 2$ there is no pair.

The [Euclidean distance](/euclidean-distance/) is never computed with a root. Every test below compares squared distances, which is exact for integers and for `fractions.Fraction`.

## The algorithm

The points are referred to by their positions in $P$, so equal points stay different items.

```pseudo id=main
CLOSEST-PAIR(P)
L1  if n < 2 then return none
L2  X ← P sorted by (x, y); Y ← P sorted by (y, x)
L3  return REC(X, Y)

REC(X, Y)                                     ▷ X and Y hold the same m points, sorted by x and by y
L4  m ← |X|
L5  if m ≤ 3 then return the best of all pairs of X
L6  h ← ⌊m / 2⌋; xm ← X[h].x                  ▷ X[0 .. h − 1] is left, X[h .. m − 1] is right
L7  XL ← X[0 .. h − 1]; XR ← X[h .. m − 1]
L8  YL ← the points of Y that are in XL, in order; YR ← the others, in order
L9  best ← the better of REC(XL, YL) and REC(XR, YR)
L10 δ² ← best.d2; if δ² = 0 then return best
L11 S ← the points s of Y with (s.x − xm)² < δ², in order
L12 for i ← 0 to |S| − 1 do
L13     j ← i + 1
L14     while j < |S| and (S[j].y − S[i].y)² < δ² do
L15         if ‖S[i] − S[j]‖² < best.d2 then best ← (‖S[i] − S[j]‖², S[i], S[j])
L16         j ← j + 1
L17 return best
```

Line L2 sorts twice, once for each order. Line L8 splits $Y$ in linear time: give each point its rank in the global order $X$ once, and send a point left when its rank is less than the rank of $X[h]$. This keeps both halves sorted by $y$ without a new sort. Every left point has $x \le x_m$ and every right point has $x \ge x_m$; with many equal $x$-coordinates the ranks still split the points into two halves of sizes $h$ and $m - h$. Line L10 stops early when two equal points were found, since no distance is smaller than 0. Line L11 keeps the points whose horizontal distance to the line $x = x_m$ is less than $\delta$, and the loop of lines L12 to L16 compares each of them with the points above it until the vertical gap reaches $\delta$.

## Example

Take the eight points $(0,0)$, $(1,9)$, $(3,6)$, $(4,2)$, $(5,3)$, $(7,0)$, $(8,8)$, $(9,5)$. They are already in $x$-order.

| call | split $x_m$ | $\delta^2$ of the halves | strip $S$ in $y$-order | pairs compared in L15 (squared distance) | result |
| --- | --- | --- | --- | --- | --- |
| left four | $3$ | $82$ and $17$ | $(0,0), (4,2), (3,6), (1,9)$ | $(0,0)(4,2)$: 20; $(4,2)(3,6)$: 17; $(3,6)(1,9)$: 13 | $13$, $(1,9)(3,6)$ |
| right four | $8$ | $13$ and $10$ | $(7,0), (5,3), (9,5), (8,8)$ | $(7,0)(5,3)$: 13; $(5,3)(9,5)$: 20; $(9,5)(8,8)$: 10 | $10$, $(8,8)(9,5)$ |
| all eight | $5$ | $13$ and $10$ | $(7,0), (4,2), (5,3), (3,6), (8,8)$ | $(7,0)(4,2)$: 13; $(7,0)(5,3)$: 13; $(4,2)(5,3)$: 2; $(5,3)(3,6)$: 13; $(3,6)(8,8)$: 29 | $2$, $(4,2)(5,3)$ |

The calls on two points are the base case of line L5. In the top call, $\delta^2 = 10$. The point $(8,8)$ is in the strip because $(8 - 5)^2 = 9 < 10$, and $(9,5)$ is not because $16 \ge 10$. The scan from $(4,2)$ stops at $(3,6)$, because $(6 - 2)^2 = 16 \ge 10$. The answer is the crossing pair $(4,2)$, $(5,3)$ at squared distance $2$, which neither half could see.

## Correctness

Two facts make the algorithm correct. First, a closest pair of $X$ is a closest pair of the left half, a closest pair of the right half, or a crossing pair; a crossing pair that is closer than $\delta$ has both points within horizontal distance $\delta$ of the line $x = x_m$, so both are in $S$. Second, for such a pair the vertical gap is less than $\delta$, so the one that comes later in $S$ is reached by the scan of line L14 from the earlier one, because $S$ is sorted by $y$ and the scan stops only at a gap of at least $\delta$. Induction on $m$ finishes the proof. The full proof is in the correctness proof below.

## Complexity

- **Presort.** Line L2 takes $O(n \log n)$ time with any optimal sort, such as [merge sort](/merge-sort/).
- **One call.** Lines L7, L8 and L11 take $O(m)$ time. The loop of lines L12 to L16 runs line L15 at most $7$ times for each $i$, by the packing lemma: the points of $S$ that follow $S[i]$ and are within vertical distance $\delta$ lie in a rectangle of width $2\delta$ and height $\delta$, which holds at most $8$ points of $X$ because points on the same side are at least $\delta$ apart. So the strip scan takes $O(m)$ time, and the constant is at most $8$ evaluations of the test of line L14 for each strip point.
- **Recurrence.** $T(m) = T(\lfloor m/2 \rfloor) + T(\lceil m/2 \rceil) + \Theta(m)$ for $m \ge 4$, so $T(n) = \Theta(n \log n)$ on the [real RAM](/real-ram/), in the worst, average and best case, since the split work is $\Theta(m)$ on every input that does not stop early at line L10.
- **Space.** $\Theta(n)$ for $X$, $Y$, the ranks and the lists of one level; the recursion depth is $\lceil \lg n \rceil$.

The proof of the packing lemma and the solution of the recurrence are in the complexity proof below. The constant 7 is the one that this proof gives; sharper geometric arguments reduce the number of points that must be checked, but the bound stays $\Theta(n \log n)$. The bound is optimal: the [closest pair lower bound](/closest-pair-lower-bound/) gives $\Omega(n \log n)$ in the algebraic decision tree model, and every test of this algorithm is a polynomial of degree 2, so it runs in that model.

## Properties

- **Exact.** Only differences, products and comparisons of coordinates appear. No root, no division.
- **Deterministic and input-independent cost.** The work is $\Theta(n \log n)$ for every input with distinct points.
- **Handles duplicates.** Two equal items give $\delta^2 = 0$, and line L10 returns at once.
- **Any fixed dimension.** Bentley and Shamos split on a hyperplane and recurse on the slab in one dimension lower, which gives $O(n \log n)$ for fixed $d$; the packing constant grows exponentially with $d$.

## Variants and improvements

- **Sort inside the recursion.** Re-sorting the strip by $y$ in each call gives $T(m) = 2T(m/2) + O(m \log m) = O(n \log^2 n)$. Merging the $y$-lists bottom up, as in merge sort, restores $O(n \log n)$ without the presort by $y$.
- **Shrinking the scan bound.** Using the current best instead of $\delta$ in line L14 can only stop the scan earlier, and stays correct.
- **Sweep line.** The [sweep line algorithm](/closest-pair-sweep-line/) keeps the strip in a balanced tree while it scans from left to right; same bound, no recursion.
- **Randomized grid.** The [randomized closest pair](/randomized-closest-pair/) algorithm uses the floor function and hashing to get $O(n)$ expected time. It is outside the algebraic decision tree model.
- **All nearest neighbors.** The same split and merge idea, with more care in the merge, finds the nearest neighbor of every point in $O(n \log n)$; see [all nearest neighbors](/all-nearest-neighbors/).

## When to use it

Use it when you need a deterministic $O(n \log n)$ bound with exact integer arithmetic and no extra data structure. The [sweep line](/closest-pair-sweep-line/) version is shorter if a balanced tree or a sorted container is at hand. For very large inputs, the [randomized grid](/randomized-closest-pair/) method is often faster in practice. For many queries on a fixed set, build a [kd-tree](/kd-tree-nearest-neighbor-search/) or a [Voronoi diagram](/voronoi-diagram/) instead.

## Pitfalls

- **Re-sorting in each call.** Sorting $S$ by $y$ in line L11 costs $O(m \log m)$ per call and gives $O(n \log^2 n)$. Split the presorted $Y$ in line L8.
- **Splitting $Y$ by $x$ alone.** With several points on the line $x = x_m$, the test "$x < x_m$" can send more than $h$ points left, or none, so the halves no longer match $X$ and the recursion can loop forever. Split by the rank in $X$, as line L8 does.
- **Taking roots.** Comparing `math.sqrt(dx*dx + dy*dy)` instead of squared distances can tie two different distances: for the points $(0,0)$, $(10^8, 1)$ and $(-10^8, 0)$ both roots round to $10^8$ in double precision. Use the squared tests of lines L11, L14 and L15.
- **A wrong strip test.** Using $|x - x_m| \le \delta$ is also correct, but $(x - x_m)^2 < \delta^2$ avoids the root and keeps the strip smaller. Using a strip of half width $\delta/2$ is wrong: it misses crossing pairs.
- **A fixed number of comparisons without the early stop.** Some versions replace the test of line L14 by "compare with the next 7 points". That is correct only under the hypothesis of the packing lemma, that points on the same side are at least $\delta > 0$ apart. With duplicates $\delta = 0$, and the return of line L10 is what keeps the count valid.

## Implementations

## History

Shamos and Hoey published the divide and conquer algorithm for the planar closest pair in their 1975 paper on closest-point problems. Bentley and Shamos extended the method to every fixed dimension in 1976, using the fact that the points near the cutting hyperplane are sparse. The presentation with a presorted $y$-list and a bound of 7 points per strip point is the one of CLRS; Kleinberg and Tardos give the same packing argument with boxes of side $\delta/2$.

## References
