---
tag: J7QH00
kind: problem
slug: red-blue-intersection
name: Red-blue intersection
aliases:
- red-blue-segment-intersection
- bichromatic segment intersection
area: geometry/intersections
level: research
summary: Report or count the intersections between a set of red and a set of blue segments, ignoring red-red and blue-blue pairs; for disjoint colour classes O(n log n + k) and O(n log n) are optimal.
prereqs: [all-segment-intersections]
see_also: [bentley-ottmann-algorithm, chazelle-edelsbrunner-algorithm, segment-intersection-lower-bound, planar-subdivision, doubly-connected-edge-list, segment-tree, orientation-test, geometric-cutting]
sources:
  - paper: doi:10.1007/BF01182771
    title: Bernard Chazelle, Herbert Edelsbrunner, Leonidas J. Guibas and Micha Sharir, Algorithms for bichromatic line-segment problems and polyhedral terrains, Algorithmica 11(2), 1994, 116-132
    locator: the O(n log n) counting and O(n log n + k) reporting of red-blue intersections when no two red and no two blue segments intersect, by a hereditary segment tree
  - paper: doi:10.1006/gmip.1994.1028
    title: Larry Palazzi and Jack Snoeyink, Counting and reporting red/blue segment intersections, Graphical Models and Image Processing 56(4), 1994, 304-310
    locator: the sweep and the list of slabs that store one level of a segment tree, giving O(n log n) counting in O(n) space
  - paper: doi:10.1007/3-540-47738-1_23
    title: Andrea Mantler and Jack Snoeyink, Intersecting red and blue line segments in optimal time and precision, Japanese Conference on Discrete and Computational Geometry (JCDCG 2000), LNCS 2098
    locator: the sweep with bundles of segments that reports in O(n log n + k) and counts in O(n log n) time using only orientation tests
  - paper: doi:10.1007/3-540-61680-2_64
    title: Julien Basch, Leonidas J. Guibas and G. D. Ramkumar, Reporting red-blue intersections between two sets of connected line segments, European Symposium on Algorithms (ESA 1996), LNCS 1136
    locator: the O(n log n + k) reporting when each colour class is connected, even if a class has intersections of its own
  - paper: doi:10.1016/s0925-7721(99)00057-7
    title: Jean-Daniel Boissonnat and Jack Snoeyink, Efficient algorithms for line and curve segment intersection using restricted predicates, Computational Geometry 16(1), 2000
    locator: the red-blue reporting with predicates of low degree and the discussion of the precision needed by the sweep
---

The red-blue intersection problem gives two sets of segments in the plane, the red set $R$ and the blue set $B$, and asks to report or count the pairs $(r, b) \in R \times B$ that intersect. Pairs of the same colour do not count. The classical case is the one where no two red segments and no two blue segments cross, as for the edges of two planar maps that are overlaid. Then the answer can have size $\Theta(n^2)$, but reporting takes $O(n \log n + k)$ time and counting takes $O(n \log n)$ time, independent of $k$, by the algorithms of Mairson and Stolfi, of Chazelle, Edelsbrunner, Guibas and Sharir, and of Palazzi and Snoeyink. When a colour class may cross itself, the problem is harder, and counting is as hard as counting all crossings of lines.

## In plain words

Take two road maps of the same area, one drawn in red and one in blue. Inside each map, roads only meet at their ends. You want the places where a red road crosses a blue road, or only how many there are.

You could find all crossings of all roads and throw away the red-red and blue-blue ones, but in this setting there are none of those. The trick is that the red roads, which never cross each other, can be kept in a fixed order from bottom to top, and so can the blue roads. Counting then becomes a question about how these two orders interleave, which can be answered without visiting each crossing.

## Definition

**Input.** Two finite sets $R$ and $B$ of closed segments in $\mathbb{R}^2$ with $|R| + |B| = n$. In the main version, the segments of $R$ are pairwise disjoint except at shared end points, and so are the segments of $B$.

**Output.** *Reporting:* all $k$ pairs $(r, b) \in R \times B$ with $r \cap b \ne \emptyset$, with the intersection point or overlap. *Counting:* the number $k$. *Detection:* whether $k > 0$.

**Notation.** $k$ is the number of red-blue intersecting pairs. "Disjoint colour classes" means the main version above. The intersection points are rational with integer input, as on the [segment intersection](/segment-intersection-point/) page.

**Model.** The [real RAM](/real-ram/) with the [orientation test](/orientation-test/) and comparisons of $x$-coordinates of intersection points. Some algorithms use only orientation tests of input points, which keeps the arithmetic degree at $2$.

## Variants

- **Disjoint colour classes.** The main version; the classes are, for example, the edge sets of two planar subdivisions.
- **Connected colour classes.** Each colour forms a connected set of segments, and segments of one colour may cross each other; Basch, Guibas and Ramkumar report in $O(n \log n + k)$ time.
- **General classes.** No condition on the classes. Reporting and counting then lead to the hard problem of counting crossings in an arrangement, solved with [cuttings](/geometric-cutting/) in about $O(n^{4/3})$ time up to polylogarithmic factors.
- **Map overlay.** Compute the full overlay of two [planar subdivisions](/planar-subdivision/), with faces and a [doubly connected edge list](/doubly-connected-edge-list/); this is red-blue reporting plus the construction of the new faces.
- **Per-segment counts.** For each red segment, the number of blue segments that cross it.
- **Curves.** Red and blue $x$-monotone curve pieces that meet a bounded number of times.

## Examples

Red: $r_1 = (0, 0)(6, 0)$, $r_2 = (0, 2)(6, 4)$, $r_3 = (1, 5)(5, 5)$. Blue: $b_1 = (1, -1)(1, 6)$, $b_2 = (3, -2)(4, 6)$, $b_3 = (5, 1)(7, -1)$. No two red and no two blue segments meet.

| pair | point | kind |
| --- | --- | --- |
| $r_1, b_1$ | $(1, 0)$ | proper crossing |
| $r_1, b_2$ | $(13/4, 0)$ | proper crossing |
| $r_1, b_3$ | $(6, 0)$ | end point of $r_1$ on $b_3$ |
| $r_2, b_1$ | $(1, 7/3)$ | proper crossing |
| $r_2, b_2$ | $(84/23, 74/23)$ | proper crossing |
| $r_3, b_1$ | $(1, 5)$ | end point of $r_3$ on $b_1$ |
| $r_3, b_2$ | $(31/8, 5)$ | proper crossing |

So $k = 7$ of the $9$ pairs meet; $r_2, b_3$ and $r_3, b_3$ do not. With closed segments the two touching pairs count, and a program that tests only proper crossings reports $5$.

## Known algorithms

**Brute force.** Test all $|R| \cdot |B|$ pairs in $O(n^2)$ time; this is optimal for reporting only when $k = \Theta(n^2)$.

**General segment sweep.** Run [Bentley-Ottmann](/bentley-ottmann-algorithm/) on $R \cup B$ and keep the red-blue pairs, in $O((n + k) \log n)$ time; or use the optimal [Chazelle-Edelsbrunner algorithm](/chazelle-edelsbrunner-algorithm/) in $O(n \log n + k)$. With disjoint classes all crossings are red-blue, so these bounds are in terms of the right $k$.

**Mairson and Stolfi (1988).** A sweep that keeps the red and the blue segments in two separate orders, and finds the red-blue crossings between neighbouring bundles, reports in $O(n \log n + k)$ time and $O(n)$ space.

**Hereditary segment trees.** Chazelle, Edelsbrunner, Guibas and Sharir (1994) store both colours in one [segment tree](/segment-tree/) over the $x$-coordinates. In a node, the segments that span the node's slab are ordered from bottom to top because a colour class does not cross itself, and the crossings of spanning red segments with segments of the other colour that end in the slab are found by merging these orders. This counts in $O(n \log n)$ time and reports in $O(n \log n + k)$ time.

**Palazzi and Snoeyink (1994).** A plane sweep that presorts the segments and then works on a list of slabs that stores a single level of a segment tree at a time; it counts in $O(n \log n)$ time with $O(n)$ space and reports in additional time proportional to $k$.

**Low-degree predicates.** Boissonnat and Snoeyink (2000) report red-blue intersections with predicates of low degree, and Mantler and Snoeyink (2000) sweep with bundles of segments and use only orientation tests on input points, never comparisons of intersection points, so integer input needs only about twice the input precision; they keep $O(n \log n + k)$ reporting and $O(n \log n)$ counting.

## Bounds

For disjoint colour classes, the bounds $O(n \log n + k)$ for reporting and $O(n \log n)$ for counting are regarded as optimal in the literature, as in the title of Mantler and Snoeyink: $\Omega(k)$ is the output size of reporting, and $\Omega(n \log n)$ is the lower bound in the [algebraic decision tree](/algebraic-decision-tree/) model for intersection problems of this kind, as on the [segment intersection lower bound](/segment-intersection-lower-bound/) page. Counting in $O(n \log n)$ is far below $k$, which can be $\Theta(n^2)$: $n/2$ horizontal red segments and $n/2$ vertical blue segments form a grid with $n^2 / 4$ crossings. For general classes, counting is at least as hard as counting the crossings of $n$ segments, for which the best known bounds are about $n^{4/3}$.

## Reductions

- **Map overlay to red-blue reporting.** The crossings of the edges of two subdivisions are the new vertices of the overlay.
- **Red-blue to general reporting.** Report all crossings of $R \cup B$ and drop the monochromatic pairs; this is optimal when the classes are disjoint.
- **Counting to slab problems.** In a slab where all segments span it, a disjoint colour class is a sorted list, and the crossings of two sorted lists across the slab are the inversions between their orders at the left and the right side, which is counted by a merge.

## Applications

- **Geographic information systems.** Overlay of two thematic maps, such as soil type and land use, by their edge crossings.
- **Boolean operations on polygons.** The union, intersection and difference of two polygonal regions, each without self-crossings, start by finding the red-blue crossings of their boundaries; see [polygon clipping](/polygon-clipping/).
- **Terrains.** Chazelle, Edelsbrunner, Guibas and Sharir use bichromatic segment problems to answer visibility and intersection questions on polyhedral terrains.
- **VLSI.** Checking the wires of two layers for crossings.

## References
