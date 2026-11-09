---
tag: FY0W28
kind: algorithm
slug: seidel-polygon-triangulation
name: Seidel's randomized polygon triangulation
aliases:
- Randomized incremental polygon triangulation
- Seidel's algorithm
- Seidel's trapezoidation
area: geometry/triangulations
level: advanced
summary: Randomized incremental triangulation with expected O(n log* n) time.
solves: [polygon-triangulation]
model: real-ram
complexity:
  vars: {n: the number of polygon vertices}
  time: {worst: O(n^2), expected: O(n log* n)}
  space: {extra: O(n) expected}
properties: {online: false, deterministic: false, recursive: false}
history:
  year: 1991
  people: [Raimund Seidel]
  note: Seidel built the trapezoidal decomposition of the polygon edges by inserting them in random order with a history DAG for point location, and showed that tracing the polygon through the partial map at a few phase boundaries brings the expected time down to O(n log* n). The decomposition gives monotone pieces and then a triangulation in linear time.
prereqs: [polygon-triangulation, trapezoidal-map, randomized-incremental-construction, monotone-polygon, monotone-polygon-triangulation, simple-polygon, orientation-test]
see_also: [ear-clipping, monotone-polygon-partition, chazelle-polygon-triangulation, tarjan-van-wyk-triangulation, polygon-with-holes-triangulation, kirkpatrick-point-location, triangulation-dual-tree, planar-subdivision]
sources:
  - paper: "Raimund Seidel, A simple and fast incremental randomized algorithm for computing trapezoidal decompositions and for triangulating polygons, Computational Geometry: Theory and Applications 1(1), 51 to 64 (1991), doi:10.1016/0925-7721(91)90012-4 (DOI to be checked)"
    locator: the randomized incremental trapezoidation, the history DAG, the phases with N(h) segments, and the O(n log* n) bound for polygons
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 6 (trapezoidal maps, the randomized incremental algorithm, the search structure and its backwards analysis) and Chapter 3 (monotone pieces and their stack triangulation)
  - paper: "Kenneth L. Clarkson, Robert E. Tarjan and Christopher J. Van Wyk, A fast Las Vegas algorithm for triangulating a simple polygon, Discrete and Computational Geometry 4(5), 423 to 432 (1989)"
    locator: the earlier expected O(n log* n) algorithm (pages to be checked)
  - paper: "Atul Narkhede and Dinesh Manocha, Fast polygon triangulation based on Seidel's algorithm, in Graphics Gems V, edited by Alan W. Paeth, Academic Press, 1995"
    locator: a C implementation with the phase trick (pages to be checked)
  - paper: "Nancy M. Amato, Michael T. Goodrich and Edgar A. Ramos, A randomized algorithm for triangulating a simple polygon in linear time, Discrete and Computational Geometry 26(2), 245 to 265 (2001)"
    locator: expected linear time by randomizing Chazelle's approach (pages to be checked)
---

Seidel's algorithm solves the [polygon triangulation](/polygon-triangulation/) problem by first building the [trapezoidal map](/trapezoidal-map/) of the polygon edges. It inserts the edges one at a time in random order and keeps a history DAG that locates points in the current map. Each trapezoid inside the polygon then gives at most one diagonal, and these diagonals cut the polygon into [monotone pieces](/monotone-polygon/), which the stack method of [monotone triangulation](/monotone-polygon-triangulation/) finishes in linear time. Plain random insertion takes expected $O(n \log n)$ time. Seidel's extra idea is to trace the whole polygon through the partial map a few times, at phase boundaries, so that each later point location starts close to its answer. That brings the expected time down to $O(n \log^* n)$. The algorithm is a Las Vegas algorithm: the output is always correct, and only the running time depends on the random order.

## In plain words

Draw a horizontal line through every corner of the shape and stop each line at the first edge it meets on either side. The shape falls apart into thin slabs with flat tops and bottoms. Each slab touches one corner at its top and one at its bottom. If those two corners are not on the same side wall, joining them is a safe cut. All these cuts together split the shape into pieces that are easy to triangulate in one top to bottom pass.

To build the slabs, add the edges one at a time in random order. A history of past splits tells you which slab a new corner lands in. Random order keeps the history shallow on average. Seidel also remembers, every so often, where every corner of the shape currently lies, so later lookups start near the answer.

## The problem

The input is a simple polygon $P$ with vertices $v_0, \ldots, v_{n-1}$ in counterclockwise order. Edge $i$ is the segment $v_i v_{i+1}$, with indices modulo $n$. The output is a list of $n - 2$ triangles, as counterclockwise index triples, with disjoint interiors and union $P$.

"Above" compares points by $(y, x)$ in lexicographic order. This is a symbolic shear: after a tiny shear that keeps every orientation sign, all vertices have distinct heights, so the words horizontal, top and bottom always refer to the sheared picture, and equal $y$ coordinates need no special case. The implementation assumes distinct vertices with no three collinear. A trapezoid is stored as (top vertex, bottom vertex, left edge, right edge), with `None` for an unbounded side.

## The algorithm

The history DAG has three kinds of node. A **leaf** holds a trapezoid of the current map. A **point node** at a vertex $r$ sends a query to the child above or below $r$. A **segment node** at an edge $t$ sends a query to the child left or right of $t$. Inserting a segment never removes a leaf from the DAG. It turns leaves into inner nodes, so the DAG records the history of every split.

```pseudo id=main
SEIDEL-TRIANGULATE(P)                     ▷ P simple, counterclockwise, no three vertices collinear
L1  shuffle the n edges of P into a random order s[1 .. n]; D ← one leaf for the whole plane
L2  for i ← 1 to n do
L3      for each end point p of s[i] that is not yet in D do
L4          t ← the leaf reached from the root of D by testing p at every node
L5          replace t by a point node at p whose children are the parts of t above and below p
L6      t[1 .. k] ← the leaves whose trapezoids meet the open segment s[i], sorted from top to bottom
L7      cut every t[j] into a part left of s[i] and a part right of s[i]
L8      merge each part with the part just above it when the cut between them now ends at s[i]
L9      replace every t[j] by a segment node at s[i] whose children are its two parts
L10 keep the trapezoids whose left side is an edge of P directed downward    ▷ the inside ones
L11 for each inside trapezoid T with top u and bottom w do
        if u and w are both end points of the left side, or both of the right side, of T then skip T
L12     add the diagonal uw
L13 for each face Q of P cut by these diagonals do                       ▷ Q is monotone
        u[1 .. m] ← the vertices of Q from top to bottom; S ← stack (u[1], u[2])
        for j ← 3 to m − 1 do
L14         if u[j] and top(S) lie on different chains of Q then
                pop every vertex s of S except the bottom one, output (u[j], s, the vertex under s)
                S ← stack (u[j − 1], u[j])
            else
L15             last ← pop(S)
                while S is not empty and the corner at last between top(S) and u[j] is strictly convex do
                    output (u[j], last, top(S)); last ← pop(S)
                push last; push u[j]
L16     pop the vertices of S and output the fan from u[m]
L17 return all triangles output for all faces
```

Lines L1 to L9 are the randomized incremental construction of the trapezoidal map. Line L6 finds the trapezoids crossed by the new segment by searching the DAG with the whole segment: at a point node it goes to one child or both, depending on whether the segment lies on one side of the cut or crosses it. At a segment node it goes to the side of the old segment on which the new one lies. Line L8 is the merge step. Before $s_i$ was inserted, the cut through the vertex $w$ between $t_j$ and $t_{j+1}$ crossed the position of $s_i$. After insertion, the half of that cut on the far side of $s_i$ from $w$ is gone. So the two parts on that side form a single trapezoid.

Line L10 uses the orientation of the polygon. The interior of a counterclockwise polygon lies to the left of each directed edge. An edge directed downward has its left on the east, so the trapezoid to its east is inside. Lines L11 and L12 add the diagonals, and lines L13 to L16 are the stack triangulation of each monotone face.

### The phases

The $O(n \log^* n)$ bound needs one change to lines L3 and L4. Let $\log^{(h)} n$ be the logarithm iterated $h$ times, and let $N(h) = \lceil n / \log^{(h)} n \rceil$ for $h = 1, \ldots, \log^* n$. These numbers grow very fast: $N(\log^* n) = n$. After the first $N(h)$ segments are inserted, walk once along the whole polygon boundary through the current map. This records, for every vertex not yet inserted, the leaf that contains it. In the next phase, the point location of line L4 starts at that recorded leaf instead of at the root. The walk is possible because the boundary is connected: following an edge from one trapezoid to the next costs one step per crossing.

## Example

Take the notched rectangle $v_0 = (0, 0)$, $v_1 = (6, 0)$, $v_2 = (6, 4)$, $v_3 = (4, 4)$, $v_4 = (3, 1)$, $v_5 = (2, 4)$, $v_6 = (0, 4)$, with doubled area 42. The notch at $v_4$ is a downward cusp, because both of its neighbors lie above it. The map of the 7 edges has $2 \cdot 7 + 1 = 15$ trapezoids, and 6 of them lie inside $P$:

| top | bottom | left edge | right edge | diagonal |
|---|---|---|---|---|
| $v_1$ | $v_0$ | $v_6 v_0$ | $v_0 v_1$ | none: both ends of the right edge |
| $v_2$ | $v_3$ | $v_2 v_3$ | $v_1 v_2$ | none: both ends of the left edge |
| $v_3$ | $v_4$ | $v_3 v_4$ | $v_1 v_2$ | none: both ends of the left edge |
| $v_4$ | $v_1$ | $v_6 v_0$ | $v_1 v_2$ | $v_1 v_4$ |
| $v_5$ | $v_6$ | $v_5 v_6$ | $v_4 v_5$ | none: both ends of the left edge |
| $v_6$ | $v_4$ | $v_6 v_0$ | $v_4 v_5$ | $v_4 v_6$ |

The first, second and fifth rows have height zero in $y$. They exist because the horizontal edges $v_0 v_1$, $v_2 v_3$ and $v_5 v_6$ become slightly tilted under the $(y, x)$ order. The two diagonals both leave the cusp $v_4$, one up to $v_6$ and one down to $v_1$. They cut $P$ into three monotone pieces: $(v_0, v_1, v_4, v_6)$, $(v_1, v_2, v_3, v_4)$ and $(v_4, v_5, v_6)$.

In the second piece the order from top to bottom is $v_2, v_3, v_4, v_1$. The stack starts as $(v_2, v_3)$. Then $v_4$ is on the same chain as $v_3$, and the corner at $v_3$ is convex, so the triangle $(v_4, v_2, v_3)$ is cut off. Last, $v_1$ fans to the stack $(v_2, v_4)$ and gives $(v_1, v_2, v_4)$. The output for all pieces is $(v_0, v_1, v_4)$, $(v_0, v_4, v_6)$, $(v_4, v_2, v_3)$, $(v_1, v_2, v_4)$, $(v_4, v_5, v_6)$, with doubled areas $6 + 12 + 6 + 12 + 6 = 42$.

## Correctness

The [correctness proof](proofs/correctness.md) has three parts. The first is an invariant of the construction: after each insertion, the leaves of the DAG are exactly the trapezoids of the map of the segments inserted so far, and the DAG locates points correctly. Splitting at a point changes one trapezoid. The trapezoids crossed by a new segment form a vertical chain, and the merge rule of line L8 follows from which side of the segment each shared vertex lies on.

The second part is about the diagonals. Each one lies inside its trapezoid, so no two cross. The faces they cut out are monotone. An interior cusp at a vertex $v$ would have, directly above or below it, a trapezoid that is not bounded by an edge at $v$, and that trapezoid would contribute a diagonal at $v$ into the face, which is impossible. The third part is the usual reflex-chain invariant of the stack triangulation. Counting triangles over the $d + 1$ pieces gives exactly $n - 2$.

## Complexity

**Plain random order.** By backwards analysis, each trapezoid of the map after $i$ insertions is determined by at most four of the $i$ segments. So the $i$th insertion creates $O(1)$ trapezoids in expectation, and the DAG has expected size $O(n)$. A query point changes its trapezoid at step $i$ with probability $O(1/i)$, so a query descends $O(\log n)$ nodes in expectation. With $2n$ point locations, the expected total is $O(n \log n)$ ([de Berg, Cheong, van Kreveld and Overmars](#references), Chapter 6). This is the version in the Python code below.

**With the phases.** A vertex located in the map of the first $N(h-1)$ segments changes trapezoid during the insertion of segment $i$ with probability $O(1/i)$. Summed over the segments of phase $h$, this is $O(\log(N(h)/N(h-1))) = O(\log^{(h)} n)$ expected steps per location, and phase $h$ has at most $N(h) = n / \log^{(h)} n$ insertions, so each phase costs $O(n)$ in expectation. The walk at the end of a phase costs $O(n)$ plus the number of crossings between polygon edges and cuts of the current map. Seidel shows that this number is $O(n)$ in expectation: each of the $O(r)$ cuts of a random sample of $r$ edges is crossed by $O(n/r)$ other edges on average. With $\log^* n$ phases, the total is $O(n \log^* n)$ expected time.

**The rest.** The final map has $2n + 1$ trapezoids, so lines L10 to L12 take $O(n)$ time. Neighboring trapezoids are linked in the map, so the monotone pieces can be read off in $O(n)$ time, and merging the two chains of a piece avoids any sort. The stack phase is linear.

**Worst case.** An unlucky order can make one insertion cross $\Theta(n)$ trapezoids each time, so the running time is $O(n^2)$ in the worst case. The probability of being far above the expectation is small, and the output does not depend on the order.

## Properties

- The map does not depend on the order of insertion, only the DAG does, so the output triangulation is the same for every random seed.
- The algorithm is Las Vegas. It is always correct, and only the time is random.
- The intermediate map is a point location structure for the polygon with expected $O(\log n)$ query time, which is useful in its own right.
- It needs only orientation tests and comparisons in the $(y, x)$ order, so it runs exactly on integer or rational coordinates.
- It is not online. The diagonals come from the final map.

## Variants and improvements

- **General segments.** On $n$ non-crossing segments that need not form a polygon, the same insertion gives the trapezoidal map in expected $O(n \log n)$ time. That is optimal, because without connectivity the points can be in any order. The phase trick needs the segments to be connected.
- **Polygons with holes.** The map of all boundary edges gives the inside trapezoids of a [polygon with holes](/polygon-with-holes-triangulation/) in the same way. The walk at a phase boundary then needs one point location per boundary component, because the components are not connected to each other.
- **Expected linear time.** Amato, Goodrich and Ramos (2001) combined random sampling with ideas from [Chazelle's algorithm](/chazelle-polygon-triangulation/) and gave a randomized algorithm with expected $O(n)$ time.
- **Deterministic bounds.** [Tarjan and Van Wyk](/tarjan-van-wyk-triangulation/) gave $O(n \log \log n)$ deterministically, and Chazelle gave $O(n)$. Both are much more complicated than Seidel's method.
- **Different second phase.** The inside trapezoids can also be merged into monotone mountains, polygons with one chain a single edge, and then triangulated by cutting off convex vertices. This avoids the two-chain bookkeeping.

## When to use it

Seidel's method suits large polygons where a near-linear time bound matters and a short implementation is wanted. The C implementation by Narkhede and Manocha has been reused widely. For small polygons, [ear clipping](/ear-clipping/) is shorter and often faster in practice despite its quadratic worst case. When a deterministic $O(n \log n)$ bound is enough, the [monotone partition sweep](/monotone-polygon-partition/) needs no randomness. When the trapezoidal map is wanted anyway, for point location, its second phase is almost free.

## Pitfalls

- The search structure is a DAG, not a tree: two segment nodes can share a merged child. A traversal that lists the leaves, or that finds the crossed leaves, must remember visited nodes.
- The merge of line L8 depends on which side of the new segment the shared vertex lies. Getting it backwards leaves cuts that pass through a segment, and the count $2n + 1$ breaks.
- At a segment node during line L6, the old and new segments may share an end point. The side test must then use the other end point, the one that lies strictly inside the span of the other segment.
- Equal $y$ coordinates are common in real data. Breaking ties by $x$ is a valid symbolic perturbation only if it is used consistently in every comparison, including the chain test of the stack phase.
- Without the phase walk, the method is "only" $O(n \log n)$ expected. Stating $O(n \log^* n)$ for plain random insertion is wrong.
- Recursion along the DAG can be as deep as the number of insertions in the worst case. The code walks it with explicit loops and stacks.

## Implementations

The Python version follows the pseudocode. `Trapezoidation` holds the DAG, with `locate` (L4), `add_point` (L5), `crossed` (L6) and `insert` (L7 to L9). `trapezoidal_decomposition` shuffles the edges and returns the inside trapezoids (L10), `monotone_diagonals` adds the diagonals (L11, L12), `faces` traces the pieces, and `triangulate_monotone` runs the stack algorithm (L13 to L16). The code uses plain random order without the phase walk, so its expected time is $O(n \log n)$. For simplicity it also sorts each piece and the neighbors of each vertex instead of reading the order off the map. It assumes counterclockwise input with distinct vertices and no three collinear.

The tests check the map and the output against brute force:

- the map has $2n + 1$ trapezoids, and the exact areas of the inside trapezoids sum to the polygon area
- every piece is monotone, and there is one more piece than there are diagonals
- the inside trapezoids are the same for every seed
- every result has $n - 2$ counterclockwise triangles whose exact doubled areas sum to the doubled polygon area, every polygon edge is used, there are $n - 3$ diagonals, no two edges cross, and the midpoint of every diagonal is strictly inside

The inputs are 150 random simple polygons, jittered combs, convex polygons, polygons with horizontal edges, very large integers and `Fraction` coordinates.

## History

Randomized incremental construction of trapezoidal maps was developed around 1990 by Mulmuley and by Seidel, after the random sampling methods of Clarkson and Shor. In 1989 Clarkson, Tarjan and Van Wyk gave the first expected $O(n \log^* n)$ polygon triangulation, but their algorithm was intricate. Seidel's 1991 paper gave the simple insertion with a history DAG, which is the version now taught in textbooks, and showed how phases bring it to $O(n \log^* n)$ for polygons. Chazelle's deterministic linear-time algorithm appeared in the same year. Narkhede and Manocha's 1995 implementation in Graphics Gems V made Seidel's method a common choice in graphics software.

## References
