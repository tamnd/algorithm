---
tag: 4TVWVM
kind: algorithm
slug: rectangle-union-sweep
name: Bentley's rectangle union sweep
aliases:
- Bentley rectangle union algorithm
area: techniques/sweep-line
level: core
summary: Sweep over vertical edges with a segment tree over compressed y-coordinates to compute union area.
solves: [area-of-union-of-rectangles]
model: real-ram
complexity:
  vars: {n: the number of rectangles}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: false, recursive: true}
prereqs: [sweep-line-technique, segment-tree, coordinate-compression]
see_also: [area-of-union-of-rectangles, klee-measure-problem, rectangle-intersection-sweep, skyline-sweep, event-queue, sweep-invariant, lazy-propagation]
sources:
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction
    locator: Chapter 8, The Geometry of Rectangles (the measure of a union of rectangles, with Bentley's segment tree sweep)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition
    locator: Chapter 10, Section 10.3, Segment Trees (canonical subsets and the O(log n) nodes of an interval)
  - paper: "J. L. Bentley, Algorithms for Klee's rectangle problems, unpublished notes, Computer Science Department, Carnegie Mellon University (1977)"
    locator: the O(n log n) sweep for the measure of a union of rectangles
  - paper: "M. L. Fredman and B. Weide, On the complexity of computing the measure of the union of intervals, Communications of the ACM 21(7) (1978), doi:10.1145/359545.359553"
    locator: pages 540 to 544 (the Omega(n log n) lower bound that makes the sweep optimal)
  - paper: "V. Klee, Can the measure of the union of intervals be computed in less than O(n log n) steps?, The American Mathematical Monthly 84(4) (1977), doi:10.1080/00029890.1977.11994336"
    locator: pages 284 to 285 (the question)
---

Bentley's rectangle union sweep computes the [area of the union](/area-of-union-of-rectangles/) of $n$ axis-parallel rectangles in $O(n \log n)$ time. A vertical [sweep line](/sweep-line-technique/) stops at each left and right edge. A [segment tree](/segment-tree/) over the [compressed](/coordinate-compression/) $y$-coordinates keeps the total length of the line that the active rectangles cover, and the area grows by that length times the distance to the next stop. Each node of the tree keeps only a count and a covered length, and needs no [lazy propagation](/lazy-propagation/), because each removal undoes an earlier insertion on exactly the same nodes. Fredman and Weide's lower bound shows that $O(n \log n)$ is optimal.

## In plain words

Cut the plane into vertical strips at each left and right edge of a rectangle. Inside one strip, each rectangle either covers the full width of the strip or does not touch its inside. So the union, inside the strip, is a set of full-width bars, and its area is the width of the strip times the length of the line that the bars cover.

Move a vertical line from strip to strip. When a rectangle starts, add its vertical extent to a counter structure; when it ends, take it out. The structure answers one question fast: how much of the line is covered by at least one rectangle now? Add that length times the strip width to the total. The structure is a tree over the sorted heights, and each update touches only a few of its nodes.

## The problem

The input is a list of $n$ rectangles $R_i = [a_i, b_i] \times [c_i, d_i]$ with $a_i \le b_i$ and $c_i \le d_i$. The output is the area $\mu\big(\bigcup_i R_i\big)$ of their union, where $\mu$ is the Lebesgue measure in the plane. Whether the rectangles are open or closed does not change the area. This is the [area of union of rectangles](/area-of-union-of-rectangles/) problem, the planar case of [Klee's measure problem](/klee-measure-problem/).

## The algorithm

Let $Y[0] < Y[1] < \cdots < Y[m-1]$ be the distinct values among all $c_i$ and $d_i$, so $m \le 2n$. The $m - 1$ *elementary intervals* are $[Y[j], Y[j+1]]$ for $j = 0, \ldots, m-2$. Each $y$-interval $[c_i, d_i]$ is the union of the elementary intervals with index in $[\operatorname{idx}(c_i), \operatorname{idx}(d_i))$, where $\operatorname{idx}(Y[j]) = j$.

The segment tree $T$ has one leaf for each elementary interval. A node $u$ covers a range $[l_u, r_u)$ of elementary indices, which is the $y$-range $[Y[l_u], Y[r_u]]$. Each node has two fields:

- $cnt[u]$: the number of active intervals that were stored at $u$ (see UPDATE);
- $len[u]$: the length of the part of $[Y[l_u], Y[r_u]]$ covered by the active intervals stored at $u$ or at a node below $u$.

```pseudo id=main
UNION-AREA(R[1 .. n])                     ▷ R[i] = [a_i, b_i] × [c_i, d_i]
L1  Y ← the sorted distinct values of all c_i and d_i
L2  E ← the events (a_i, +1, c_i, d_i) and (b_i, −1, c_i, d_i) for i = 1 .. n
L3  sort E by x
L4  T ← a segment tree over the m − 1 elementary intervals, with all cnt and len equal to 0
L5  area ← 0, prev ← the x of the first event
L6  for each event (x, v, c, d) of E, in order do
L7      area ← area + len[root] · (x − prev)
L8      UPDATE(root, idx(c), idx(d), v)
L9      prev ← x
L10 return area

UPDATE(u, lo, hi, v)                      ▷ add v to the elementary indices in [lo, hi)
L11 if hi ≤ l_u or r_u ≤ lo then return
L12 if lo ≤ l_u and r_u ≤ hi then cnt[u] ← cnt[u] + v
L13 else UPDATE(left(u), lo, hi, v), UPDATE(right(u), lo, hi, v)
L14 if cnt[u] > 0 then len[u] ← Y[r_u] − Y[l_u]
L15 else if u is a leaf then len[u] ← 0
L16 else len[u] ← len[left(u)] + len[right(u)]
```

Line L7 adds the area of the strip between the previous stop and this one, before the event changes the covered length. Line L12 stores the interval at a node whose range lies inside $[lo, hi)$ and does not go further down. These nodes are the *canonical nodes* of the interval: their ranges are disjoint and their union is $[lo, hi)$. Lines L14 to L16 recompute $len[u]$ from the node's own count and from its children. If some interval is stored at $u$, the whole range of $u$ is covered. If not, the covered part is what the children report.

**Why no lazy propagation.** An update never pushes $cnt[u]$ down to the children, and a query reads only $len[root]$. The $-1$ event of a rectangle has the same $[lo, hi)$ as its $+1$ event, so it reaches exactly the same canonical nodes and decrements the counts that the $+1$ incremented. So each $cnt[u]$ stays at least 0, and it equals the number of active intervals with $u$ as a canonical node.

## Example

Take $R_1 = [1, 4] \times [1, 3]$, $R_2 = [2, 6] \times [2, 5]$ and $R_3 = [5, 7] \times [0, 2]$. Then $Y = [0, 1, 2, 3, 5]$, and the four elementary intervals are $[0,1]$, $[1,2]$, $[2,3]$ and $[3,5]$.

| $x$ | event | strip | covered length in the strip | area added | area | covered length after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | $+[1,3]$ | none | | 0 | 0 | 2 |
| 2 | $+[2,5]$ | $[1, 2]$ | 2 | 2 | 2 | 4 |
| 4 | $-[1,3]$ | $[2, 4]$ | 4 | 8 | 10 | 3 |
| 5 | $+[0,2]$ | $[4, 5]$ | 3 | 3 | 13 | 5 |
| 6 | $-[2,5]$ | $[5, 6]$ | 5 | 5 | 18 | 2 |
| 7 | $-[0,2]$ | $[6, 7]$ | 2 | 2 | 20 | 0 |

The area is 20. Inclusion and exclusion agree: $6 + 12 + 4 - 2 = 20$, since only $R_1 \cap R_2 = [2,4] \times [2,3]$ has positive area.

After the event at $x = 2$, the tree is as follows. The root covers $[0, 4)$, with children $[0, 2)$ and $[2, 4)$. The interval $[1, 3)$ of indices, which is $y \in [1, 3]$, has the canonical nodes leaf $[1,2)$ and leaf $[2,3)$. The interval $[2, 4)$, which is $y \in [2, 5]$, has the single canonical node $[2, 4)$. So $cnt = 1$ at these three nodes. Then $len[[2,4)] = 5 - 2 = 3$ by line L14, $len[[0,2)] = 0 + 1 = 1$ by line L16, and $len[root] = 1 + 3 = 4$. The leaf $[2,3)$ also has $cnt = 1$, but its parent already covers it, and the length 1 is not counted twice.

## Correctness

Two facts give the result. First, the *node invariant*: after each update, $len[u]$ equals the length of the union of the ranges of the nodes $w$ in the subtree of $u$ with $cnt[w] > 0$. At the root, these ranges are exactly the canonical nodes of the active intervals, so $len[root]$ is the length of the union of the active $y$-intervals. Second, between two consecutive event coordinates $x < x'$, the set of rectangles whose $x$-range contains the open strip $(x, x')$ is constant, so the union meets the strip in a set of area $(x' - x)$ times that length. Adding over all strips gives the area. The full proof is below.

## Complexity

- **Preparation.** Lines L1 to L3 sort $2n$ numbers twice: $O(n \log n)$ time. Line L4 builds a tree with $m - 1 < 2n$ leaves and fewer than $4m$ nodes in the array layout: $O(n)$ time and space. The function idx is a dictionary or a binary search: $O(\log n)$ for each lookup.
- **One update.** At each depth of the tree, line L13 runs for at most two nodes: such a node meets $[lo, hi)$ but is not inside it, so $lo$ or $hi$ lies strictly inside its range, and the nodes of one depth have disjoint ranges. These at most two nodes have at most four children, so UPDATE visits at most four nodes at each depth. The depth is $\lceil \lg(m-1) \rceil$, so one update costs $O(\log n)$.
- **Total.** $2n$ updates and $2n$ strip additions: $\Theta(n \log n)$ time in each case, since the sort alone takes $\Theta(n \log n)$ comparisons in the worst case and the updates take $\Theta(\log n)$ each when the intervals are long. The extra space is $\Theta(n)$.
- **Optimality.** Computing the length of a union of $n$ intervals on a line needs $\Omega(n \log n)$ operations in the worst case in a decision tree model with linear tests (Fredman and Weide 1978). The intervals $[a_i, b_i]$ become the rectangles $[a_i, b_i] \times [0, 1]$, whose union has the same measure. So the sweep is optimal in that model. The [problem page](/area-of-union-of-rectangles/) states the model exactly.
- **Numbers.** With integer coordinates up to $C$ in absolute value, the area is at most $4C^2$ and each partial sum is an integer. With 64-bit integers this is safe for $C \le 2^{30}$.

## Properties

- **Exact.** Line L7 multiplies a sum of coordinate differences by a coordinate difference. With integer input the area is an exact integer.
- **Not comparison-only.** It subtracts and multiplies coordinates, so the model is the [real RAM](/real-ram/).
- **Order of events at equal $x$.** Events with the same $x$ give strips of width 0, so their order does not change the area. This differs from the [intersection sweep](/rectangle-intersection-sweep/), where the order at equal $x$ matters.
- **Recursive.** UPDATE recurses to depth $O(\log n)$ only.

## Variants and improvements

- **Area covered at least $k$ times.** Keep at each node the lengths covered at least $1, 2, \ldots, k$ times, from the node's count and its children. This costs $O(k)$ for each node and $O(kn \log n)$ in total.
- **Perimeter of the union.** Sort the inserts before the deletes at equal $x$. Then the vertical part of the boundary is the sum, over the events, of $|len_{\text{after}} - len_{\text{before}}|$. The horizontal part is $2 \times$ (number of disjoint covered pieces) $\times$ strip width, and each node can keep the number of pieces and whether its two ends are covered. This gives $O(n \log n)$ time.
- **Brute force over the grid.** Mark each cell of the $(2n-1) \times (2n-1)$ grid of compressed coordinates that some rectangle covers: $O(n^3)$ time with a direct marking, $O(n^2)$ with 2D prefix sums of the corners. Use it as a test oracle.
- **Dimension $d \ge 3$.** The same sweep, with a structure for the measure of a union of $(d-1)$-dimensional boxes, is the start of the algorithms for [Klee's measure problem](/klee-measure-problem/). The best known time for $d \ge 3$ is $O(n^{d/2})$ (Chan 2013).
- **Floating-point coordinates.** The algorithm works with floats, but the area then has rounding errors. Sum the strips with compensated summation, or use rationals for exact answers.

## When to use it

Use the sweep for many rectangles, for example $10^5$ or more. For fewer than a few hundred, the grid brute force is shorter and fast enough. When the rectangles arrive one at a time and you need the area after each one, the static sweep does not apply; a dynamic structure or a recomputation is needed. When the coordinates are small integers, a 2D difference array over the grid is simpler.

## Pitfalls

- **Adding the strip after the update.** Line L7 must come before line L8. If the update comes first, each strip gets the covered length of the next strip.
- **Elementary intervals as points.** A leaf stands for the interval $[Y[j], Y[j+1]]$, not for the point $Y[j]$. A tree indexed by points, with leaf length $Y[j+1] - Y[j]$ but with the update range $[idx(c), idx(d)]$ closed, adds an extra elementary interval above $d$. The update range must be the half-open $[idx(c), idx(d))$.
- **Leaf with zero count.** Line L15 sets the length of an uncovered leaf to 0. Without it, a leaf reads children that do not exist.
- **Pushing counts down.** Pushing $cnt$ to the children, as in lazy propagation for range assignment, breaks the matching of $+1$ and $-1$ and can make counts negative. The counts stay where the canonical decomposition puts them.
- **Overflow.** In C or Java, the product in line L7 overflows 32-bit integers already for coordinates near $2^{16}$. Use 64-bit integers.

## Implementations

## History

Victor Klee asked in 1977 whether the length of a union of $n$ intervals can be computed in fewer than $O(n \log n)$ steps. Fredman and Weide (1978) showed that it cannot in a decision tree model with linear tests. In the same year as Klee's question, Jon Bentley gave the sweep of this page for the planar case in unpublished notes. Applied one dimension at a time, his method takes $O(n^{d-1} \log n)$ time in $d$ dimensions. Preparata and Shamos present the sweep with the segment tree, which Bentley had introduced for such problems.

## References
