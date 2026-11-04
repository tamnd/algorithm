---
tag: 69VCE3
kind: problem
slug: rectangle-intersection-detection
name: Rectangle intersection detection
aliases:
- axis-parallel rectangle intersection
area: techniques/sweep-line
level: core
summary: Decide whether any two of n axis-parallel rectangles overlap.
prereqs: [sweep-line-technique, element-distinctness]
see_also: [rectangle-intersection-sweep, segment-intersection-detection, interval-tree, interval-overlap-query, area-of-union-of-rectangles, element-distinctness-lower-bound, algebraic-decision-tree]
sources:
  - paper: "J. L. Bentley and D. Wood, An optimal worst case algorithm for reporting intersections of rectangles, IEEE Transactions on Computers C-29(7) (1980), doi:10.1109/TC.1980.1675628"
    locator: pages 571 to 577 (the reporting problem, the O(n log n + k) algorithm and its optimality)
  - paper: "H.-W. Six and D. Wood, The rectangle intersection problem revisited, BIT 20(4) (1980), doi:10.1007/BF01933636"
    locator: pages 426 to 433
  - paper: "M. Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th ACM Symposium on Theory of Computing (1983), doi:10.1145/800061.808735"
    locator: pages 80 to 86 (the lower bound from the number of connected components)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction
    locator: Chapter 8, The Geometry of Rectangles
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition
    locator: Chapter 10, More Geometric Data Structures (interval trees and segment trees for axis-parallel objects)
---

Rectangle intersection detection asks whether any two of $n$ axis-parallel rectangles in the plane intersect. It is the rectangle form of [element distinctness](/element-distinctness/): it has the same $\Theta(n \log n)$ worst-case cost in the [algebraic decision tree](/algebraic-decision-tree/) model, and a [sweep line](/sweep-line-technique/) solves it within that bound. The reporting version, which lists all $k$ intersecting pairs, takes $\Theta(n \log n + k)$ time. The algorithm itself is on the page [rectangle intersection sweep](/rectangle-intersection-sweep/).

## In plain words

You have many rectangles on a sheet of paper, all with sides parallel to the edges of the sheet. Do any two of them overlap or touch? Testing every pair works, but for a million rectangles that is half a million million tests.

Two such rectangles overlap only if their shadows on the floor overlap and their shadows on the wall overlap. This makes the question much easier than it looks. A line that moves across the sheet, and a sorted list of the shadows on the wall of the rectangles that it cuts, answers it in about as many steps as sorting the rectangles. No method can do much better, because the question already contains the question "are two numbers in this list equal?".

## Definition

**Input.** A list of $n \ge 0$ closed axis-parallel rectangles $R_i = [a_i, b_i] \times [c_i, d_i]$ with real coordinates, $a_i \le b_i$ and $c_i \le d_i$, for $i = 1, \ldots, n$. A rectangle of zero width or height is a segment or a point; the problem allows these.

**Output.** YES if there are indices $i \ne j$ with $R_i \cap R_j \ne \emptyset$, and NO otherwise. In the search form, the output is such a pair $(i, j)$, or NONE.

**The test for one pair.** Two closed rectangles intersect if and only if their projections on both axes meet:

$$R_i \cap R_j \ne \emptyset \iff \max(a_i, a_j) \le \min(b_i, b_j) \ \text{ and } \ \max(c_i, c_j) \le \min(d_i, d_j).$$

So rectangles that share only an edge or a corner intersect. The point $(\max(a_i, a_j), \max(c_i, c_j))$ is then a common point.

## Variants

- **Reporting.** Output all the $k$ pairs $\{i, j\}$ with $R_i \cap R_j \ne \emptyset$. The output can have $k = \binom{n}{2}$ pairs, for example when all rectangles share a point.
- **Counting.** Output the number $k$ of intersecting pairs, without listing them.
- **Open rectangles.** Count a pair only if the interiors $(a_i, b_i) \times (c_i, d_i)$ overlap. Then touching rectangles do not intersect. The rectangles must then have positive width and height.
- **Edge crossings and containment.** Two intersecting rectangles either have crossing or touching boundaries, or one contains the other. Some algorithms, among them that of Bentley and Wood, solve these two cases with different structures.
- **Red-blue.** Two sets of rectangles are given, and only pairs with one rectangle from each set count. Map layers and the "broad phase" of collision detection in games have this form.
- **Higher dimensions.** Boxes $\prod_{t=1}^{d} [a_{i,t}, b_{i,t}]$ intersect if and only if they meet on each of the $d$ axes.
- **Segments.** For segments of any direction, the problem is [segment intersection detection](/segment-intersection-detection/). Axis-parallel segments are a special case of both problems.

## Examples

**No intersection.** The rectangles $[1,3] \times [1,2]$, $[2,5] \times [4,6]$, $[4,7] \times [0,3]$, $[6,9] \times [5,7]$ and $[8,10] \times [1,4]$ are pairwise disjoint, so the answer is NO. The pairs $([1,3] \times [1,2], [2,5] \times [4,6])$ and $([2,5] \times [4,6], [4,7] \times [0,3])$ meet on the $x$-axis but not on the $y$-axis. The pair $([1,3] \times [1,2], [8,10] \times [1,4])$ meets on the $y$-axis but not on the $x$-axis.

**Touching.** Add $[5,6] \times [3,4]$. It meets $[2,5] \times [4,6]$ in the single point $(5, 4)$ and meets $[4,7] \times [0,3]$ in the segment from $(5,3)$ to $(6,3)$. The answer is YES, and the reporting version outputs these 2 pairs. For open rectangles, the answer stays NO.

**A cross.** The rectangles $[0,10] \times [4,5]$ and $[4,5] \times [0,10]$ intersect in the square $[4,5] \times [4,5]$, but no corner of either rectangle lies in the other. A test that checks only the corners of each rectangle misses this pair.

## Known algorithms

- **All pairs.** Test each of the $\binom{n}{2}$ pairs with the formula above: $\Theta(n^2)$ time, $O(1)$ extra space. It also solves the reporting version in $\Theta(n^2)$ time, which is optimal only when $k = \Theta(n^2)$.
- **[Rectangle intersection sweep](/rectangle-intersection-sweep/).** Sweep a vertical line over the $x$-coordinates, keep the $y$-intervals of the active rectangles in a balanced search tree, and test a new interval against its two neighbors: $O(n \log n)$ time and $O(n)$ space for detection.
- **Sweep with an interval tree.** The same sweep with an [interval tree](/interval-tree/) as the status, and an [overlap query](/interval-overlap-query/) at each insert, reports all pairs in $O(n \log n + k)$ time. Bentley and Wood (1980) first reached this bound; Six and Wood (1980) gave another algorithm with the same bound.
- **Counting sweep.** At each insert, count the active intervals that meet the new one as the number of active intervals, minus those that end below it, minus those that start above it. With [Fenwick trees](/fenwick-tree/) over the compressed $y$-coordinates this counts all pairs in $O(n \log n)$ time, whatever $k$ is.

## Bounds

**Upper bounds.** Detection: $O(n \log n)$ worst-case time on a [real RAM](/real-ram/), by the sweep. Reporting: $O(n \log n + k)$ worst-case time (Bentley and Wood 1980). Counting: $O(n \log n)$.

**Lower bound for detection.** Each algebraic decision tree that solves detection has depth $\Omega(n \log n)$. The proof is a reduction from [element distinctness](/element-distinctness/), which needs $\Omega(n \log n)$ in this model ([element distinctness lower bound](/element-distinctness-lower-bound/), Ben-Or 1983). Given numbers $x_1, \ldots, x_n$, form the degenerate rectangles $R_i = [x_i, x_i] \times [0, 0]$, which are points. Two of them intersect if and only if $x_i = x_j$ for some $i \ne j$. The reduction costs no comparisons, so a faster detection algorithm would give a faster test of distinctness.

**The bound holds for proper rectangles too.** Let $W \subseteq \mathbb{R}^{2n}$ be the set of inputs $(u_1, v_1, \ldots, u_n, v_n)$ with $u_i < v_i$ for each $i$ and the intervals $[u_i, v_i]$ pairwise disjoint. The rectangles $[u_i, v_i] \times [0, 1]$ have positive area, and they are pairwise disjoint if and only if the input is in $W$. On $W$ the left ends $u_i$ are pairwise distinct, so each point of $W$ has a left-to-right order of the intervals, a permutation $\pi$. A path in $W$ cannot change $\pi$: two left ends would have to become equal on the way, and then two intervals would meet. Each of the $n!$ orders occurs, so $W$ has at least $n!$ connected components. By Ben-Or's theorem, a tree that decides membership in $W$ has depth $\Omega(\log(n!) - 2n) = \Omega(n \log n)$. A detection algorithm decides membership in $W$ after $n$ extra tests $u_i < v_i$.

**Reporting.** Each algorithm needs $\Omega(k)$ time to write the output, and $\Omega(n \log n)$ for the detection part. So $\Theta(n \log n + k)$ is tight.

## Reductions

- **From element distinctness** in $O(n)$ time, as above. So detection is at least as hard as element distinctness.
- **To segment intersection detection, plus containment.** Two rectangles of positive area intersect if and only if their boundaries intersect or one rectangle contains the other. So a test on the $4n$ boundary segments finds every intersecting pair except the nested ones, and the nested pairs need a separate test.
- **From interval overlap.** One-dimensional interval overlap detection is the case $c_i = 0$, $d_i = 1$ for each $i$.

## Applications

- **Design rule checking.** In the layout of integrated circuits, the parts of a layer are rectangles, and two parts that are too close or that overlap are an error. This application motivated the work of Bentley and Wood.
- **Collision detection.** Physics engines first test the axis-aligned bounding boxes of the objects. Only pairs whose boxes intersect go to the exact and costly test. The sweep form of this test is called "sweep and prune".
- **Maps and windows.** Geographic information systems test map objects by their bounding boxes, and window systems test windows for overlap.

## References
