---
tag: S5KEK2
kind: data-structure
slug: trapezoidal-map
name: Trapezoidal map
aliases:
- trapezoidal decomposition
- vertical decomposition
- trapezoidal map with history DAG
area: geometry/point-location
level: advanced
summary: A decomposition of a set of segments into trapezoids by extending vertical lines from each endpoint.
model: real-ram
complexity:
  vars: {n: the number of segments}
  time: {build: O(n log n) expected, query: O(log n) expected, insert: O(log n) expected}
  space: {map: O(n) worst case, dag: O(n) expected}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1990
  people: [Ketan Mulmuley, Raimund Seidel]
  note: Mulmuley (1990) and Seidel (1991) built the trapezoidal decomposition by randomized incremental construction, with the history of the construction as a search structure for point location.
prereqs: [planar-subdivision, vertical-ray-shooting, randomized-incremental-construction]
see_also: [seidel-point-location, slab-method-point-location, sarnak-tarjan-point-location, kirkpatrick-point-location, backwards-analysis, seidel-polygon-triangulation, planar-point-location, degeneracy-in-sweeps]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 6, Sections 6.1 (trapezoidal maps and their size), 6.2 (the randomized incremental algorithm and the search structure), 6.3 (degenerate cases by a shear) and 6.4 (the tail estimate)
  - paper: doi:10.1016/0925-7721(91)90012-4
    title: Raimund Seidel, A simple and fast incremental randomized algorithm for computing trapezoidal decompositions and for triangulating polygons, Computational Geometry 1(1), 1991
    locator: the whole paper (DOI to be checked)
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 38, Point location, by Jack Snoeyink, Section 38.3 and Table 38.3.1
---

The trapezoidal map of a set of non-crossing segments is the subdivision obtained by drawing, from every end point, a vertical wall up and down until it hits a segment. Every face of the result is a trapezoid, or a triangle, or an unbounded piece, with at most two vertical sides. A set of $n$ segments with $m$ distinct end points has exactly $1 + n + m \le 3n + 1$ trapezoids. Built by inserting the segments in random order, the map comes with a history DAG that answers [point location](/planar-point-location/) and [vertical ray shooting](/vertical-ray-shooting/) queries in $O(\log n)$ expected time, uses $O(n)$ expected space and takes $O(n \log n)$ expected time to build.

## In plain words

Take a map made of straight streets. From every street corner, draw a thin vertical line up until it hits a street, and down until it hits a street. Now every block of the map is cut into simple pieces: each piece has a street above, a street below, and a straight vertical line on the left and on the right. Such a piece is a trapezoid.

Trapezoids are easy to search. If you know which trapezoid you are in, you know the street directly above you. To find the trapezoid of a point, add the streets one at a time in a random order and remember how each new street cut the old trapezoids. To answer a query, replay this history: at each step ask "am I left or right of this corner?" or "am I above or below this street?".

## The abstract type

The structure stores a set $S$ of segments in the plane that meet only at shared end points, and supports:

- **INSERT(s)**: add a segment $s$ that meets the stored ones only at end points.
- **QUERY(q)**: return the vertex $q$, or the segment that contains $q$, or the face answer (top, bottom): the segments directly above and below $q$, which are the top and bottom of the trapezoid that contains $q$.

The face answer is the canonical answer of vertical ray shooting. With a [doubly connected edge list](/doubly-connected-edge-list/) of the [planar subdivision](/planar-subdivision/), the face of the subdivision is the face to the left of the half-edge of "top" that points to the left. The structure is built by $n$ insertions; deletions are possible but are not covered here.

**Notation.** $P$ is the set of end points, $n = |S|$, $m = |P|$, $p = (x, y)$ a point, $d = 2$. $\mathrm{orient}(p, q, r)$ is the sign of $(q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x)$, positive when $p, q, r$ turn counterclockwise. The output size of a query is $h = 1$. The predicate $\mathrm{incircle}$ is not used.

**Degenerate input.** de Berg et al. assume that no two end points have the same $x$, and remove the assumption in their Section 6.3 by a shear $(x, y) \mapsto (x + \varepsilon y, y)$ with $\varepsilon$ symbolic. The shear does not change $\mathrm{orient}$, and in the sheared plane, $p$ is left of $q$ exactly when $(p_x, p_y) < (q_x, q_y)$ lexicographically. So the code compares points as pairs, the walls are the sheared vertical lines, vertical segments become slightly slanted, and query points with the $x$ of a vertex are decided by the $y$ tie-break. No case is special.

## Representation

Each segment is stored as $(a, b)$ with $a <_{\mathrm{lex}} b$. Each trapezoid $\Delta$ has eight fields:

- **top** and **bottom**: the segments that bound $\Delta$ above and below, or none for an unbounded side;
- **leftp** and **rightp**: the end points whose walls bound $\Delta$ on the left and the right, or none;
- **ul, ll, ur, lr**: the upper-left, lower-left, upper-right and lower-right neighbors.

A trapezoid has at most two left neighbors. If its bottom starts at leftp, the left side is a wall from leftp up to top and there is one left neighbor, stored in ul. If its top starts at leftp, the one left neighbor is stored in ll. If both start there, $\Delta$ is a triangle on the left and has no left neighbor. If neither does, both ul and ll are set. The right side is the same, with the segments that end at rightp: the top ends there means one neighbor in lr, and the bottom ends there means one neighbor in ur.

The search structure $D$ is a DAG with one leaf per trapezoid and two kinds of inner nodes: an **X-node** stores an end point $p$ and sends a query left or right of the wall through $p$; a **Y-node** stores a segment $s$ and sends a query above or below $s$.

**Invariant.** (1) The trapezoids are exactly the faces of the trapezoidal map of the inserted segments, and their fields and neighbor pointers follow the rules above. (2) For every point $q$ that is not a vertex and lies on no segment, the search in $D$ ends at the leaf of the trapezoid that contains $q$.

## Operations

INSERT finds the trapezoids that the new segment crosses, from left to right, and replaces them.

```pseudo id=main
TM-INSERT(s = (p, r))
L1  Δ[0] ← the trapezoid found by searching D for the point just right of p on s
L2  j ← 0; while rightp(Δ[j]) < r do
L3      Δ[j+1] ← lr(Δ[j]) if rightp(Δ[j]) is above s, else ur(Δ[j]); j ← j + 1
L4  split each Δ[j] by s into an upper and a lower piece; the upper pieces are merged except at each rightp above s, and the lower pieces except at each rightp below s
L5  if p is a new end point, cut off the part A of Δ[0] left of p; if r is new, cut off the part B of Δ[k] right of r; set all neighbor pointers of the new trapezoids and of their old neighbors
L6  replace the leaf of each Δ[j] by Y(s) with its upper and lower pieces as children; put X(p) with child A above it for Δ[0] when p is new, and X(r) with child B for Δ[k] when r is new
```

- **Line L1.** At an X-node whose point equals $p$, the search goes right. At a Y-node whose segment $t$ has $\mathrm{orient}(t, p) = 0$, the point $p$ is the left end point of $t$, and the search compares $r$ with $t$ instead. This finds the trapezoid that contains the start of $s$.
- **Lines L2 and L3.** The segment leaves $\Delta[j]$ through its right wall, below rightp if rightp lies above $s$ and above it otherwise. The walk stops at the trapezoid whose closure contains $r$.
- **Line L4.** A wall through $v = $ rightp$(\Delta[j])$ that lies above $s$ now ends at $s$ from above, so it still separates two upper pieces, but below $s$ it is gone, and the two lower pieces merge into one. In the code, upper piece $U_i$ cut at $v$ gets $lr(U_i) = U_{i+1}$ and $ur(U_i) = ur(\Delta[j])$, and $U_{i+1}$ gets $ll = U_i$ and $ul = ul(\Delta[j+1])$; the lower chain is symmetric.
- **Line L5.** If $p$ was already an end point, the wall through $p$ already exists and leftp$(\Delta[0]) = p$, so no piece $A$ is needed. The pieces $U_0$ and $L_0$ take the left neighbors of $\Delta[0]$.
- **Line L6** is the only change to $D$. The old leaves become inner nodes in place, so all pointers into them stay valid.

The search follows the DAG from the root.

```pseudo id=query
TM-QUERY(q)
L7  v ← the root of D; while v is not a leaf do
L8      if v = X(p): if q = p then return the vertex p; go to the left child if q < p, else to the right child
L9      if v = Y(s = (a, b)): if orient(a, b, q) = 0 then return the segment s; go to the above child if orient(a, b, q) > 0, else to the below child
L10 return the face (top(Δ), bottom(Δ)) of the trapezoid Δ of the leaf v
```

A Y-node for $s$ is reached only by points strictly inside the $x$-range of $s$ in the sheared plane, so $\mathrm{orient} = 0$ in line L9 means that $q$ lies on $s$. Every vertex $q$ is caught by an X-node with key $q$ in line L8, because a vertex lies in no open trapezoid. The cost of a query is the length of its search path.

## Example

Insert $s_0 = (0,0)(8,2)$, $s_1 = (4,6)(8,2)$, $s_2 = (0,0)(4,6)$ and $s_3 = (2,8)(10,6)$ in this order. A trapezoid is written as [leftp, rightp, top, bottom], with a dash for none.

| after | trapezoids | count $1 + n + m$ | DAG depth |
|---|---|---|---|
| $s_0$ | [−, (0,0), −, −], [(0,0), (8,2), $s_0$, −], [(0,0), (8,2), −, $s_0$], [(8,2), −, −, −] | $1 + 1 + 2 = 4$ | 3 |
| $s_1$ | the region above $s_0$ is split at $(4,6)$ into [(0,0), (4,6), −, $s_0$], [(4,6), (8,2), $s_1$, $s_0$] and [(4,6), (8,2), −, $s_1$] | $1 + 2 + 3 = 6$ | 5 |
| $s_2$ | [(0,0), (4,6), −, $s_0$] is split into [(0,0), (4,6), $s_2$, $s_0$] and [(0,0), (4,6), −, $s_2$]; no end point is new | $1 + 3 + 3 = 7$ | 5 |
| $s_3$ | crosses [(0,0), (4,6), −, $s_2$], [(4,6), (8,2), −, $s_1$] and [(8,2), −, −, −]; new walls at $(2,8)$ and $(10,6)$ | $1 + 4 + 5 = 10$ | 7 |

The insertion of $s_2$ creates one trapezoid net: it crosses one trapezoid and both of its end points exist. The query $q = (4, 7)$ has the $x$ of the vertex $(4,6)$ and is lexicographically larger. Its search path is X$(0,0)$ right, X$(8,2)$ left, Y$(s_0)$ above, X$(4,6)$ right, Y$(s_1)$ above, Y$(s_3)$ below, which ends in [(4,6), (8,2), $s_3$, $s_1$]: the face below $s_3$ and above $s_1$. The test file checks the counts and the answers.

## Correctness

Each insertion keeps the invariant. For part (1), the new segment cuts exactly the trapezoids it crosses, and the walk of lines L2 and L3 finds them in order, since $s$ leaves each one through its right wall, on the side of rightp given by $\mathrm{orient}$. Line L4 removes the parts of the walls through the rightp values that $s$ now blocks, and line L5 adds the walls through new end points. The neighbor rules follow from the slot conventions case by case. For part (2), a point in the new piece of an old trapezoid $\Delta$ reached the leaf of $\Delta$ before, and the new X- and Y-nodes at that leaf send it to the correct piece. The full proof, with the count $1 + n + m$, is in [the correctness proof](proofs/correctness/).

## Complexity

All bounds are on the [real RAM](/real-ram/). The expected bounds are over the random insertion order, for an arbitrary fixed input and an arbitrary fixed query point.

| operation or measure | cost | case |
|---|---|---|
| number of trapezoids | $1 + n + m \le 3n + 1$ | worst case |
| QUERY | $O(\log n)$, at most $12 H_n$ nodes on the path | expected |
| QUERY, maximum over all $q$ | $O(\log n)$ | with high probability |
| QUERY with a bad insertion order | $\Theta(n)$ | worst case |
| INSERT, the $i$-th of a random order | $O(\log i)$ search plus $O(1)$ new trapezoids | expected |
| build by $n$ random insertions | $O(n \log n)$ | expected |
| size of $D$ | $O(n)$; at most $12n + 4H_n$ trapezoids are ever created | expected |
| size of $D$ with a bad order | $\Theta(n^2)$ | worst case |

- **Size of the map.** Each trapezoid except one has a leftp. Just right of an end point $v$, the segments that start at $v$ cut the space into one more sector than there are such segments, and each sector is one trapezoid with leftp $v$. So the count is $1 + \sum_v (1 + \mathrm{starts}(v)) = 1 + m + n$.
- **New trapezoids per insertion.** By [backwards analysis](/backwards-analysis/), after $i$ insertions each of the at most $3i + 1$ trapezoids depends on at most four segments (top, bottom, and the segments of leftp and rightp), so it was created in step $i$ with probability at most $4/i$. The expected number created in step $i$ is at most $4(3i+1)/i = 12 + 4/i$, which sums to $12n + 4H_n$.
- **Query path.** The path of a fixed $q$ grows in step $i$ only if the trapezoid that contains $q$ changes, which has probability at most $4/i$ by the same argument, and then by at most $3$ nodes. So the expected length is at most $\sum 3 \cdot 4/i = 12 H_n = O(\log n)$. The search of line L1 is such a query, so the expected build time is $O(n \log n)$.
- **High probability.** de Berg et al. (Section 6.4) show that the path of a fixed point exceeds $3\lambda \ln(n+1)$ with probability at most $1/(n+1)^{\lambda \ln 1.25 - 1}$, and that the maximum over all query points exceeds it with probability at most $2/(n+1)^{\lambda \ln 1.25 - 3}$. Rebuilding with a new order when the maximum is too large gives $O(\log n)$ worst-case query time with $O(n \log n)$ expected build time; see [Seidel's algorithm](/seidel-point-location/).
- **Lower bound.** $\Omega(\log n)$ tests are needed for any query structure in the [algebraic decision tree](/algebraic-decision-tree/) model; see [planar point location](/planar-point-location/).

The tests of [Seidel's algorithm](/seidel-point-location/) measure the average path length and the number of created trapezoids against these bounds.

## Variants

- **Seidel's algorithm.** The same structure built in random order, analyzed with the tail bound, gives point location in $O(\log n)$ expected query time; see [Seidel point location](/seidel-point-location/). Seidel used the same construction to [triangulate a simple polygon](/seidel-polygon-triangulation/) in $O(n \log^* n)$ expected time.
- **Bounding box.** de Berg et al. start from one rectangle that contains all segments, so every trapezoid is bounded. The code here uses an unbounded start instead.
- **Vertical decomposition in general.** The same walls for curves (each cut into $x$-monotone pieces) or for arrangements of lines give a decomposition of size linear in the arrangement, used in many randomized algorithms; see [randomized incremental construction](/randomized-incremental-construction/).
- **Dynamic point location.** The DAG supports insertions only. Fully dynamic structures with polylogarithmic query and update times exist; see the Handbook, Section 38.4 and Table 38.4.1.

## When to use it

Use it when the subdivision is given as a set of segments and a short, practical $O(\log n)$ structure is needed. It needs no triangulation, unlike [Kirkpatrick's hierarchy](/kirkpatrick-point-location/), and no persistent tree, unlike [Sarnak and Tarjan](/sarnak-tarjan-point-location/). Its constants are small in practice. It also supports insertions. If worst-case guarantees are required without randomness, use Sarnak and Tarjan or the chain method with fractional cascading.

## Pitfalls

- **Swapping the slot conventions.** If line L5 puts the single left neighbor of a trapezoid whose bottom starts at leftp into ll instead of ul, the walk of line L3 later follows a missing pointer. Keep one fixed convention for all four slots and check it in the tests.
- **Searching for $p$ itself in line L1.** When $p$ is already an end point, the search for $p$ stops at an X-node with key $p$, or follows a Y-node of a segment that starts at $p$ with $\mathrm{orient} = 0$. Search for the point just right of $p$ on $s$: go right on equality, and compare $r$ when $p$ lies on the node segment.
- **Updating only one side of a pointer.** When a new trapezoid takes the place of an old one, the old trapezoid's neighbors still point to the old one. Line L5 must also replace these back pointers, or a later walk enters a dead trapezoid.
- **Equal $x$ by real comparison.** If walls are compared by $x$ alone, two end points with the same $x$ give a zero-width trapezoid and the walk of line L3 can loop. Compare points lexicographically, which is the symbolic shear.
- **Floating-point orientation.** A wrong sign in line L3 sends the walk to the wrong neighbor, and the map becomes inconsistent. Use exact integer or rational orientation tests.

## Implementations

## History

Trapezoidal decompositions appear in early work on polygon triangulation and point location, for example in Preparata's 1981 point location method on a trapezoidal search structure. Ketan Mulmuley (1990) and Raimund Seidel (1991) built them by randomized incremental construction and used the history of the construction as the search structure. Seidel's paper gave the simple algorithm with $O(n \log n)$ expected time and $O(\log n)$ expected query time, and the $O(n \log^* n)$ triangulation of simple polygons. The textbook treatment of de Berg, van Kreveld, Overmars and Schwarzkopf (1997) made it the standard first method for point location.

## References
