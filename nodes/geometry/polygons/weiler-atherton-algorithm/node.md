---
tag: TS2VAV
kind: algorithm
slug: weiler-atherton-algorithm
name: Weiler-Atherton algorithm
aliases:
- Weiler-Atherton clipping
- weiler-atherton
- Weiler-Atherton polygon clipping
area: geometry/polygons
level: advanced
summary: Polygon clipping that traces intersection points between the subject and clip boundaries.
solves: [polygon-clipping]
model: real-ram
complexity:
  vars: {n: the number of subject vertices, m: the number of clip vertices, k: the number of boundary crossings}
  time: {worst: O(n m + k log k)}
  space: {extra: O(n + m + k)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1977
  people: [Kevin Weiler, Peter Atherton]
  note: Introduced as the clipping step of a hidden surface removal method that sorts polygons by area.
prereqs: [simple-polygon, orientation-test, segment-intersection-point, linked-list]
see_also: [polygon-clipping, sutherland-hodgman, greiner-hormann-algorithm, vatti-clipping, polygon-union, polygon-with-holes, hidden-surface-removal, winding-number-algorithm]
sources:
  - paper: doi:10.1145/965141.563896
    title: Kevin Weiler and Peter Atherton, Hidden surface removal using polygon area sorting, Computer Graphics (SIGGRAPH '77) 11(2), 214 to 222 (1977)
    locator: the clipping algorithm and its use for hidden surface removal
  - paper: doi:10.1145/274363.274364
    title: Günther Greiner and Kai Hormann, Efficient clipping of arbitrary polygons, ACM Transactions on Graphics 17(2), 71 to 83 (1998)
    locator: Sections 1 and 2 (the walk between the two boundaries, entry and exit flags, and the degenerate cases)
  - book: isbn:9780201848403
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 19, the Weiler polygon clipping algorithm
---

The Weiler-Atherton algorithm computes the intersection, union or difference of two [simple polygons](/simple-polygon/), the subject $S$ with $n$ vertices and the clip polygon $C$ with $m$ vertices, neither of which needs to be convex. It finds the $k$ points where the two boundaries cross, inserts them into both vertex lists, and labels each as a point where the subject enters or leaves the clip polygon. Then it walks: along the subject while it is on the wanted side, and at each crossing it jumps to the other list. Each walk closes one boundary cycle of the result. Unlike [Sutherland-Hodgman](/sutherland-hodgman/), it accepts a concave clip polygon and returns the separate pieces of the result, with holes. It needs general position: the boundaries must meet only in proper crossings.

## In plain words

Draw both shapes and mark every point where their outlines cross. Walk along the outline of the first shape. When you reach a crossing where you step into the second shape, start tracing: keep walking along the first outline until the next crossing, where you would step out. There, turn onto the outline of the second shape and walk along it until the next crossing, where you turn back onto the first. When you return to the point where you began, you have traced one piece of the overlap. Repeat from any crossing you have not used.

For the union, start where the first outline steps out of the second shape. For the difference, do the same, but walk the second outline backward. If the outlines never cross, one shape is inside the other or they are apart, and one point test decides which.

## The problem

The input is two simple polygons $S = (u_0, \ldots, u_{n-1})$ and $C = (c_0, \ldots, c_{m-1})$, in either orientation, and an operation: intersection $S \cap C$, union $S \cup C$, or difference $S \setminus C$. The output is a list of closed polygons whose winding numbers add up to 1 inside the result and to 0 outside. Outer boundaries come out counterclockwise and holes clockwise, so the result is a set of [polygons with holes](/polygon-with-holes/).

General position: no vertex of one polygon lies on the boundary of the other. Then the boundaries meet only in proper crossings of edge interiors. Shared vertices, a vertex on an edge, and overlapping edges are rejected with an error; handling them needs the extra rules discussed under Pitfalls. Notation: $\mathrm{orient}(a, b, x) = (b - a) \times (x - a)$.

## The algorithm

```pseudo id=main
WEILER-ATHERTON(S, C, op)                  ▷ S, C simple and counterclockwise, in general position
L1  X ← all crossings of an edge ab of S with an edge cd of C
L2  label x ∈ X entering if (b − a) × (d − c) < 0, else exiting
L3  if X is empty then return the result by containment: test one vertex of each polygon in the other
L4  build the lists of S and of C with each x ∈ X inserted in order along its edge, linked to its twin
L5  for each unmarked x0 ∈ X that is entering (op = ∩) or exiting (op = ∪ or ∖) do
        x ← x0, list ← S, Q ← empty polygon
        repeat
L6          mark x and append it to Q
L7          walk list from x (forward on S; forward on C, or backward for ∖) appending vertices until the next crossing x′; x ← x′
L8          if x = x0 then output Q and leave the repeat loop
L9          list ← the other list, at the twin of x
L10 return the output polygons
```

- **Line L2.** The subject edge $ab$ enters $C$ when it points to the left of the counterclockwise clip edge $cd$, which is when $(b - a) \times (d - c) < 0$. Along the subject, entering and exiting crossings alternate.
- **Line L4.** Each crossing is stored with its parameter along both edges, so sorting by parameter places it in both lists. The twin link connects its two copies.
- **Line L5.** For the intersection, the walk starts on a subject arc inside $C$; for the union and the difference, on a subject arc outside $C$.
- **Line L7.** The subject is always walked forward. The clip polygon is walked forward for the intersection and the union, and backward for the difference, because there the result lies outside $C$.

## Example

Let $S$ be the U shape $(0,0), (6,0), (6,6), (4,6), (4,2), (2,2), (2,6), (0,6)$, of area 28, and let $C$ be the bar $(-1,4), (7,4), (7,5), (-1,5)$, of area 8. The bar crosses each of the four vertical edges of the U twice, at $y = 4$ and $y = 5$, so there are $k = 8$ crossings. Walking the U from $(0,0)$, the edge $(6,0) \to (6,6)$ enters the bar at $(6,4)$ and leaves it at $(6,5)$; the edge $(4,6) \to (4,2)$ enters at $(4,5)$ and leaves at $(4,4)$; and so on.

- **Intersection.** From the entering crossing $(6,4)$, walk the U to $(6,5)$, jump to the bar and walk it forward to $(4,5)$, jump back and walk the U to $(4,4)$, jump to the bar and return to $(6,4)$. The first piece is the square $(6,4), (6,5), (4,5), (4,4)$. The walk from $(2,4)$ gives the square $(2,4), (2,5), (0,5), (0,4)$. Total area 4.
- **Union.** The walks start at exiting crossings. One walk traces the outer boundary, 16 vertices around the U and the two ends of the bar, of area 36. Another traces $(4,4), (4,2), (2,2), (2,4)$, clockwise, of signed area $-4$: the bar closes the U into a ring, and this is the hole. Total $36 - 4 = 32 = 28 + 8 - 4$.
- **Difference.** Three pieces: the bottom of the U below the bar, $(4,4), (4,2), (2,2), (2,4), (0,4), (0,0), (6,0), (6,4)$, of area 20, and the two tips above the bar, of area 2 each. Total 24.

## Correctness

**Theorem.** For simple polygons in general position, the output polygons have winding numbers that add up to 1 at every point inside the result and to 0 at every point outside it, off the two boundaries.

The proof is in [proofs/correctness.md](proofs/correctness.md). The crossings cut each boundary into arcs, and each arc lies entirely inside or entirely outside the other polygon. An arc belongs to the boundary of the result exactly when the result is on one side of it and not on the other; the table of these arcs, with the direction that puts the result on the left, is: for the intersection, the subject arcs inside $C$ and the clip arcs inside $S$, both forward; for the union, the arcs outside the other polygon, forward; for the difference, the subject arcs outside $C$, forward, and the clip arcs inside $S$, backward. Near a crossing, the result covers one of the four sectors or three of them, so exactly one boundary arc arrives and one leaves, and they are on different polygons. So the boundary arcs form disjoint cycles that alternate between the polygons, and the walk traces each of them. Finally, moving a point across a boundary arc changes the result's indicator and the total winding number by the same amount, and both are 0 far away.

## Complexity

- **Crossings.** Line L1 tests all $n m$ pairs of edges, in $O(n m)$ time. A sweep such as [Bentley-Ottmann](/bentley-ottmann-algorithm/) finds them in $O((n + m + k) \log(n + m))$ time instead.
- **Lists.** Sorting the crossings along each edge takes $O(k \log k)$ time in all.
- **Walks.** Every vertex and every crossing is appended at most once over all the walks, so they cost $O(n + m + k)$.
- **In all.** $O(n m + k \log k)$ time with the pairwise test, and $O(n + m + k)$ space. The result has $O(n + m + k)$ vertices, and $k$ can be as large as $n m$: two combs with $n/4$ and $m/4$ long teeth placed crosswise have $\Theta(n m)$ crossings. So the output size alone can be $\Theta(n m)$.
- **Checks.** The implementation also checks that both polygons are simple and in general position. The simplicity check is an all-pairs test in $O(n^2 + m^2)$ time; a [Shamos-Hoey](/shamos-hoey-algorithm/) sweep does it in $O((n + m) \log(n + m))$.

## Properties

- **Exact.** Each crossing is a rational point, computed with one division per coordinate from integer or rational input. The entering test is the sign of an exact cross product.
- **Separate pieces and holes.** Each output polygon is one boundary cycle. Outer boundaries are counterclockwise and holes clockwise.
- **Symmetric roles for intersection and union.** Exchanging $S$ and $C$ gives the same result as a point set for the intersection and the union. The difference is not symmetric.
- **Simple pieces.** In general position the output cycles are simple polygons, pairwise disjoint as curves.

## Variants and improvements

- **Greiner-Hormann.** The [Greiner-Hormann algorithm](/greiner-hormann-algorithm/) uses the same walk with doubly linked lists, decides entering and exiting by a point-in-polygon test of one vertex followed by alternation, and handles self-intersecting polygons with the even-odd rule. Its paper treats degenerate crossings by perturbing them.
- **Sweep-based clipping.** [Vatti's algorithm](/vatti-clipping/) uses a sweep over scanbeams instead of walks, handles self-intersecting polygons and holes in the input, and handles more degenerate cases.
- **Several polygons with holes.** The original algorithm allows each input to be a polygon with holes: the holes are extra cycles in the lists, walked in the same way, and the containment test of line L3 is applied to the cycles without crossings.
- **Hidden surfaces.** Weiler and Atherton used the clipper to split polygons against the front polygon in depth order, keeping the inside part as visible and passing the outside part on. See [hidden surface removal](/hidden-surface-removal/).

## When to use it

Use Weiler-Atherton for boolean operations on two simple polygons that may be concave, when you need the pieces of the result as separate polygons with holes, and the input is known to be in general position, or can be perturbed into it. For a convex clip window where one output list is acceptable, [Sutherland-Hodgman](/sutherland-hodgman/) is simpler. For self-intersecting input, many polygons at once, or input with shared edges, a sweep-based method like [Vatti's](/vatti-clipping/) is more robust.

## Pitfalls

- **Degenerate crossings.** When a vertex of one polygon lies on an edge of the other, the boundaries touch there, and the point is neither a clean entry nor a clean exit; it may be both or neither. When edges overlap, there is a segment of contact, not a point. The labels of line L2 are then wrong, and the walk can stop early or skip a piece. The implementation rejects these inputs. Common fixes are a symbolic perturbation of one polygon, or extra labels for touching points with rules for each case.
- **Orientation.** The entering test assumes that $C$ is counterclockwise, and the forward walk of $S$ assumes that $S$ is. Reverse a clockwise input first, using the sign of the [shoelace formula](/shoelace-formula/).
- **Self-intersecting input.** The proof uses that each arc is entirely inside or outside the other polygon and that entering and exiting alternate. A self-intersecting polygon breaks both.
- **No crossings.** If the boundaries do not cross, the walk outputs nothing, and the result must come from a containment test: one polygon inside the other, or the two apart. Forgetting this loses the whole result, for example the hole in $S \setminus C$ when $C$ is inside $S$.
- **Floating point.** In floating point the computed order of two crossings on one edge, or the label of a crossing near a vertex, can come out wrong, and the walk then fails to close or produces crossing loops. Exact arithmetic avoids that.

## Implementations

The Python version uses exact integers and fractions. It checks simplicity and general position, finds the crossings by testing all edge pairs, builds the two lists, and walks them for intersection, union and difference. The tests check the U and bar example, all containment cases with no crossings, rejection of shared edges, shared vertices, vertices on edges and self-intersecting input, both orientations, two interleaved combs, and random simple polygons in general position: the total signed area against an exact slab measure of the result region, and the total winding number at many rational sample points against membership in both inputs.

## History

Kevin Weiler and Peter Atherton described the algorithm in 1977 as part of a method for hidden surface removal. Their method clips the polygons of a scene against the front polygon, and needs a clipper for concave polygons with holes. The walk between the two boundaries became the standard approach for clipping general polygons. Greiner and Hormann simplified the data structure in 1998, and Vatti gave a sweep-based alternative in 1992.

## References
