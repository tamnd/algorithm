---
tag: X8WKWB
kind: problem
slug: intersecting-segment-pair-search
name: Search for a pair of intersecting segments
aliases: [find two intersecting segments, intersecting pair search]
area: geometry/intersections
level: core
summary: Given n segments, return two of them that have a common point, or report that there is no such pair; a sweep with an ordered set solves it in O(n log n) time.
prereqs: [segment-intersection-detection, segment-intersection-point]
see_also: [shamos-hoey-algorithm, all-segment-intersections, bentley-ottmann-algorithm, polygon-simplicity-test, sweep-status-structure, balanced-binary-search-tree, degeneracy-in-sweeps, segment-intersection-lower-bound]
sources:
  - paper: doi:10.1109/SFCS.1976.16
    title: Michael Ian Shamos and Dan Hoey, Geometric intersection problems, 17th Annual Symposium on Foundations of Computer Science (FOCS 1976), 208-215
    locator: the sweep that finds an intersecting pair of segments
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Chapter 33, Section 33.2 (ANY-SEGMENTS-INTERSECT, and the exercise that asks for the pair)
  - url: https://cp-algorithms.com/geometry/intersecting_segments.html
    title: cp-algorithms, Search for a pair of intersecting segments
    locator: the whole article (the sweep with a std::set, the event order and the returned pair)
---

Intersecting segment pair search is the search version of [segment intersection detection](/segment-intersection-detection/): given $n$ closed segments in the plane, return the indices of two segments that have a common point, or report that no two meet. The [Shamos-Hoey sweep](/shamos-hoey-algorithm/) solves it in $\Theta(n \log n)$ time, because every "yes" it gives comes from one test of two neighbors in the sweep order, and those two segments are the witness. The $\Omega(n \log n)$ lower bound for detection also holds here.

## In plain words

It is not always enough to know that a drawing has two strokes that touch. To repair the drawing, you need to know which two strokes they are.

The sweep that answers the yes or no question already gives this. It only ever says "yes" right after it checks two particular strokes and finds that they touch. So it can return those two. The work is the same as for the yes or no question.

## Definition

**Input.** A list $S = (s_0, \dots, s_{n-1})$ of closed segments in the plane, with the same conventions as in [segment intersection detection](/segment-intersection-detection/): vertical segments, segments of length zero, shared end points and collinear overlaps are allowed.

**Output.** A pair of indices $(i, j)$ with $i \ne j$ and $s_i \cap s_j \ne \emptyset$, or "none" if no such pair exists. Any meeting pair is a correct answer; the problem does not ask for the leftmost one.

**Checking an answer.** A returned pair is checked in $O(1)$ time with the exact [pairwise test](/segment-intersection-point/). The answer "none" cannot be checked faster than solving the problem again.

## Variants

- **Leftmost meeting point.** Return a pair through the lexicographically smallest common point. The Shamos-Hoey sweep does not give this: it can return a pair that meets to the right of the leftmost common point, because the pair it tests first need not be the leftmost one. The [Bentley-Ottmann sweep](/bentley-ottmann-algorithm/), stopped at its first report, gives it in $O(n \log n)$ time, because its events come in lexicographic order.
- **A pair with a given property.** For example the first edge pair of a polygon that crosses properly, ignoring neighboring edges, as in a [simplicity test](/polygon-simplicity-test/).
- **All pairs.** [Reporting all segment intersections](/all-segment-intersections/), with an output-sensitive bound.

## Examples

**Four segments.** For $s_0 = (0,0)$-$(6,2)$, $s_1 = (1,4)$-$(7,5)$, $s_2 = (2,3)$-$(5,0)$ and $s_3 = (3,6)$-$(8,3)$ two pairs meet: $(0, 2)$ at $(15/4, 5/4)$ and $(1, 3)$ at $(119/23, 108/23)$. Both are correct answers. The [Shamos-Hoey](/shamos-hoey-algorithm/) implementation returns $(0, 2)$, because $s_2$ becomes a neighbor of $s_0$ when it is inserted at $x = 2$, and the test of this new pair succeeds at once.

**Shared end point.** For $(0,0)$-$(2,2)$ and $(2,2)$-$(4,0)$ the answer is $(0, 1)$. If the application allows shared end points, as for the two edges at a corner of a polygon, it must filter them out before or during the sweep.

**None.** For $(0,0)$-$(1,0)$ and $(2,0)$-$(3,0)$, which are collinear and disjoint, the answer is none.

## Known algorithms

| algorithm | time | idea |
| --- | --- | --- |
| all pairs | $\Theta(n^2)$ | return the first pair that passes the pairwise test |
| [Shamos-Hoey](/shamos-hoey-algorithm/) | $\Theta(n \log n)$ | the sweep returns the two neighbors that it found to meet |
| [Bentley-Ottmann](/bentley-ottmann-algorithm/), stopped at the first report | $O(n \log n)$ | returns two segments through its first reported point |

A common implementation keeps the active segments in an ordered set, such as a [balanced binary search tree](/balanced-binary-search-tree/) or a C++ `std::set` with a comparator that compares two segments at the current sweep position. The comparator is valid only as long as no two active segments have crossed, which holds until the first "yes". So the sweep stops at the first meeting pair it finds, and it must not continue.

## Bounds

The problem is at least as hard as detection, since the answer "none" is the answer "no". So it needs $\Omega(n \log n)$ time in the algebraic decision tree model; see the [lower bound](/segment-intersection-lower-bound/). The Shamos-Hoey sweep gives the matching $O(n \log n)$ time and $O(n)$ space.

## Reductions

- **Equivalent to detection.** Any detection algorithm that says "yes" only after it has tested a pair gives a witness. Conversely a search algorithm decides detection.
- **From element distinctness.** The vertical segments $\{x_i\} \times [0, 1]$ meet exactly when two numbers are equal, and a returned pair names two equal numbers.

## Applications

- **Repairing polygons and maps.** A program that cleans map data finds a crossing pair, splits the two segments at the crossing, and searches again; for many crossings, [reporting all intersections](/all-segment-intersections/) is faster.
- **Debugging geometric input.** A test of a mesh or a polygon is more useful if it names the bad pair.
- **Programming contests.** The problem is a standard exercise for sweep lines with an ordered set and for the order of events at equal $x$.

## References
