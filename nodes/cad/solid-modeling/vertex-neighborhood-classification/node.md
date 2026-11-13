---
tag: QA5D08
kind: algorithm
slug: vertex-neighborhood-classification
name: Vertex neighborhood classification
aliases:
- Mantyla Boolean algorithm
area: cad/solid-modeling
level: advanced
summary: Mantyla's B-rep Boolean algorithm that intersects the two boundaries, classifies the neighbourhood of each new vertex by sectors and joins the kept faces with Euler operators.
solves: [solid-boolean-operations]
model: real-ram
complexity:
  vars: {n: the number of edges of the two boundaries}
  time: {worst: O(n^2 log n)}
  space: {extra: O(n^2)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1986
  people: [Martti Mäntylä]
  note: Mäntylä gave a Boolean algorithm for 2-manifold boundary models that decides all coincident cases by classifying the sectors around the new vertices, and builds the result with Euler operators.
prereqs: [boundary-representation, euler-operators, regularized-set-operations, set-membership-classification]
see_also: [boundary-evaluation, winged-edge-data-structure, manifold-solid, polygon-clipping, vatti-clipping, mesh-boolean-operations, geometric-robustness-problem]
sources:
  - paper: doi:10.1145/7529.7530
    title: Martti Mäntylä, Boolean operations of 2-manifolds through vertex neighborhood classification, ACM Transactions on Graphics 5(1), 1 to 29, 1986
    locator: the whole paper (the generate, classify and connect steps, the vertex neighborhoods and their sectors, and the reclassification of the on sectors for each operation)
  - book: isbn:9780881751086
    title: Martti Mäntylä, An Introduction to Solid Modeling, Computer Science Press, 1988
    locator: the chapter on Boolean set operations for the half-edge data structure (chapter number not confirmed)
  - book: isbn:9781558600676
    title: Christoph M. Hoffmann, Geometric and Solid Modeling, An Introduction, Morgan Kaufmann, 1989
    locator: Chapter 3, Boolean operations on boundary representations
  - paper: doi:10.1109/38.41469
    title: Christoph M. Hoffmann, John E. Hopcroft and Michael S. Karasick, Robust set operations on polyhedral solids, IEEE Computer Graphics and Applications 9(6), 50 to 59, 1989
    locator: the whole paper (set operations on polyhedra in floating point that keep the topological decisions consistent)
---

Vertex neighborhood classification is Mäntylä's algorithm for Boolean operations on two solids given as [boundary representations](/boundary-representation/). It cuts the two boundaries along their intersection, so that the new vertices lie on both solids. At each such vertex it looks at the *neighborhood*: the sectors between the faces of one solid around the vertex, each classified as inside, outside or on the other solid. These local decisions settle every coincident case, such as two faces in one plane or a vertex on a face. The kept faces are then joined with [Euler operators](/euler-operators/) into a valid B-rep of the regularized result.

## In plain words

Take two solids and their skins. Find every place where the two skins cross and cut both skins there. Now every part of one skin is inside the other solid, outside it, or lies exactly on it.

Most parts are easy: follow a skin from a part you know, and the answer stays the same until you reach a cut. The hard places are the cuts. There, look closely at a tiny ball around the cut point and ask, for each wedge of the ball, whether it is inside the other solid.

Then keep the parts that you need. For a union, keep the outside parts. For an intersection, keep the inside parts. For a difference, keep the first skin outside the second, and the second skin inside the first, turned around. Join the kept parts at the cuts.

## The problem

The input is two solids $A$ and $B$ given by boundary representations of [manifold solids](/manifold-solid/) and an operation $\operatorname{op}$ among $\cup^*$, $\cap^*$ and $-^*$. The output is a boundary representation of $A \operatorname{op}^* B$, in the sense of the [regularized set operations](/regularized-set-operations/). This is [solid Boolean operations](/solid-boolean-operations/) with B-rep input. The code on this page solves the planar case: $A$ and $B$ are simple polygons with rational vertices, given counterclockwise, and the output is the set of boundary loops of the result with the region on the left of every edge.

## The algorithm

The planar form has the four steps of Mäntylä's algorithm. In the plane, the neighborhood of a boundary vertex has two sectors, the inside one and the outside one, between its outgoing edge and its incoming edge.

```pseudo id=main
BOOLEAN(A, B, op)
L1  split the edges of A where they meet the boundary of B, and the edges of B likewise
L2  classify every edge of A against B and every edge of B against A:
L3      if the edge is also an edge of the other loop then on-same or on-opposite
L4      else if its tail v is on the other boundary then in or out by the sector of the other polygon at v that holds it
L5      else the class of the previous edge of the loop     ▷ a loop that never meets: point in polygon
L6  S ← the edges that the table SELECT keeps for op, the edges of B reversed for a difference
L7  return CONNECT(S)

CONNECT(S)
L8  for each edge e of S that is in no loop yet do
L9      start a loop with e
L10     at the head of the current edge, go on with the edge of S that starts there and is first clockwise from the current edge
L11     stop when the loop is back at e
```

The table SELECT says which classes each operation keeps:

| operation | edges of $A$ | edges of $B$ |
|---|---|---|
| $A \cup^* B$ | out, on-same | out |
| $A \cap^* B$ | in, on-same | in |
| $A -^* B$ | out, on-opposite | in, reversed |

An edge that lies on both boundaries is taken from $A$ only. When the two solids lie on the same side of a shared edge, it is on-same and stays for a union or an intersection. When they lie on opposite sides, it is on-opposite and stays only for a difference.

Line L4 is the vertex neighborhood test. Let $d_{\text{out}}$ be the direction of the outgoing edge of $B$ at $v$ and $d_{\text{back}}$ the direction from $v$ back along its incoming edge. The inside sector of $B$ at $v$ is the counterclockwise sweep from $d_{\text{out}}$ to $d_{\text{back}}$, and the edge of $A$ is in when its direction falls in this sweep. The code compares angles with a rational pseudo-angle, so the test is exact.

**The solid version.** In three dimensions the steps are the same, with sectors between faces in place of sectors between edges:

1. **Generate.** Intersect each edge of $A$ with the faces of $B$ and each edge of $B$ with the faces of $A$. Split the edges at the intersection points, and record each new vertex as a vertex of one solid on a face of the other, or as a vertex of both.
2. **Classify.** At a vertex on a face of the other solid, classify each sector of the vertex neighborhood as above, below or on the plane of that face. At a vertex of both solids, classify the pairs of sectors against each other. Reclassify the on sectors by the operation, with rules like the table above, and insert null edges between the in and out sectors.
3. **Connect.** Join the null edges into loops, which become new null faces along the intersection curve.
4. **Finish.** Cut each solid along its null faces, keep the pieces that the operation selects, and glue them along the null faces with Euler operators.

The planar code covers steps 1 to 3. It does not build the 3D B-rep or use Euler operators.

## Example

Let $A$ be the square $[0, 2]^2$ and $B$ the square $[1, 3]^2$. The boundary of $B$ crosses the edges of $A$ at $(2, 1)$ and $(1, 2)$, so line L1 splits both loops there:

- $A$: $(0, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2)$
- $B$: $(1, 1), (2, 1), (3, 1), (3, 3), (1, 3), (1, 2)$

At $(2, 1)$ the outgoing edge of $B$ points in the direction $(1, 0)$ and its incoming edge goes back in the direction $(-1, 0)$, so the inside sector of $B$ is the upper half-plane. The edge of $A$ from $(2, 1)$ to $(2, 2)$ points up, so it is in. The next edge, from $(2, 2)$ to $(1, 2)$, starts at a vertex that is not on $B$, so line L5 gives it the class in as well. At $(1, 2)$ the inside sector of $B$ is the right half-plane, and the edge of $A$ toward $(0, 2)$ points left, so it is out.

| loop | edges in | edges out |
|---|---|---|
| $A$ | $(2, 1) \to (2, 2) \to (1, 2)$ | the other four |
| $B$ | $(1, 2) \to (1, 1) \to (2, 1)$ | the other four |

For $A -^* B$, SELECT keeps the four out edges of $A$ and the two in edges of $B$ reversed, $(2, 1) \to (1, 1) \to (1, 2)$. CONNECT joins them into one loop with six vertices, $(0, 0), (2, 0), (2, 1), (1, 1), (1, 2), (0, 2)$, the square with its upper right corner removed. Its area is $3$. The union keeps the eight out edges, area $7$, and the intersection keeps the four in edges, the unit square of area $1$.

Touching squares show the on cases. The squares $[0, 2]^2$ and $[2, 4] \times [0, 2]$ share the segment $x = 2$. Each one has it as an edge, in opposite directions, so it is on-opposite: the union drops it and gives one loop around $[0, 4] \times [0, 2]$, and the intersection is empty. The squares $[0, 2]^2$ and $[2, 4]^2$ touch at the single vertex $(2, 2)$. Their union has two outgoing edges at that vertex, and line L10 picks the one that keeps each square in its own loop. The result is two loops that share a vertex, which is a non-manifold point of the result.

## Correctness

After line L1, an edge of $A$ and an edge of $B$ are equal or meet only at end points. So the inside of each split edge is all in the other polygon, all out of it, or on it, and the neighborhood test at line L4 reads which sector of the other polygon holds the edge near its tail. A vertex that is not on the other boundary does not change the class, which justifies line L5. Near a point inside an edge, each polygon is a whole disk, an empty disk or a half-disk, and the table SELECT lists exactly the cases where the regularized result is a half-disk. At every vertex the kept edges alternate between incoming and outgoing around the vertex, so CONNECT closes the loops. The [full proof](proofs/correctness.md) shows that the winding number of the output is $1$ inside the result and $0$ outside.

## Complexity

The costs are in the [real RAM](/real-ram/), for the planar code with $n$ edges in all.

- **Generate.** All pairs of edges are tested, $O(n^2)$, and there are $k = O(n^2)$ cut points. Sorting the cuts along each edge costs $O(n^2 \log n)$ in all.
- **Classify.** Each of the $O(n + k)$ split edges costs one lookup and one sector test. With the vertices kept in a sorted table, this is $O((n + k) \log n)$.
- **Connect.** Each kept edge is chosen once, among the edges at its vertex.

So the time is $O(n^2 \log n)$ and the space is $O(n^2)$. With a sweep that reports only the $k$ actual crossings, the generate step costs $O((n + k) \log n)$. For solids, generate tests edges against faces, and practical systems cut the work with bounding boxes.

## Properties

- **Local decisions.** Each in, out or on answer comes from the sectors around one vertex, so coincident faces and edges need no global special case.
- **Regularized.** The table SELECT drops shared faces that the result does not bound, such as the face between two touching solids in a union.
- **Exact when the signs are exact.** All decisions are signs of [orientation tests](/orientation-test/). With rational input they are exact, and the output is the exact boundary.
- **The result may be non-manifold.** Two solids that touch along an edge or at a vertex give a result whose boundary is not a 2-manifold there. A B-rep for 2-manifolds must split such a vertex or edge into copies.

## Variants and improvements

- **Polygon clipping.** In the plane the same problem is [polygon clipping](/polygon-clipping/). [Vatti clipping](/vatti-clipping/) uses a sweep instead of vertex neighborhoods and works on any number of polygons with holes.
- **Robust set operations.** Hoffmann, Hopcroft and Karasick worked in floating point and kept the topological decisions consistent with each other, so that a sign that cannot be trusted is derived from decisions already made.
- **Meshes.** For triangle meshes, [mesh Boolean operations](/mesh-boolean-operations/) use the same generate and classify plan, with a winding number or a ray test as the classifier.
- **Non-manifold structures.** With a [radial edge data structure](/radial-edge-data-structure/), the result can keep the shared edges and vertices of touching solids instead of splitting them.

## When to use it

Use it to combine two solids that are already B-reps, which is the usual case in a modeler that stores B-reps and applies one Boolean at a time. It fits faceted models with exact or filtered predicates. For a solid given as a CSG tree, [boundary evaluation](/boundary-evaluation/) builds the B-rep from the whole tree at once. For triangle soups with self-intersections, use a mesh method.

## Pitfalls

- **Classifying by a sample point only.** A test at the midpoint of an edge says on for both on-same and on-opposite. The decision needs the direction, which only the neighborhood gives. With the touching squares, a midpoint test cannot tell that the shared edge goes for a union and stays for a difference.
- **Taking an on edge twice.** If the shared edges are kept from both polygons, the output has a doubled edge and a loop that runs back along itself.
- **The wrong exit at a touching vertex.** At a vertex with two outgoing edges, taking the first one counterclockwise instead of clockwise joins the two touching squares into one loop that passes the vertex twice. The area and the winding numbers are still right, but the loop does not match the two faces that a B-rep needs, and a later Euler operator that splits the loop at the vertex is required.
- **Inconsistent rounded signs.** In floating point, the cut point of two edges may be classified differently from each of the two edges, and the loops then do not close. Compute the cut points and the signs exactly, or derive the uncertain signs from earlier ones as Hoffmann, Hopcroft and Karasick do. See the [geometric robustness problem](/geometric-robustness-problem/).

## Implementations

## History

Mäntylä published vertex neighborhood classification in 1986 for 2-manifold boundary models, and his book of 1988 treats Boolean operations on half-edge models. Requicha and Voelcker's merging algorithms of 1985 combined a B-rep with a new primitive by classification with neighborhoods, and Hoffmann, Hopcroft and Karasick turned to the consistency of the decisions in floating point in 1989.

## References
