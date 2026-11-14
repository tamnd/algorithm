---
tag: ETJZAW
kind: algorithm
slug: triangle-mesh-slicing
name: Triangle mesh slicing
aliases:
- plane mesh slicing
- contour construction
area: cad/cam-and-additive-manufacturing
level: core
summary: Intersects each triangle with the planes it spans and links the segments into oriented polygons with a hash of endpoints, in O(n log k + k + m) time.
solves: [slicing-for-additive-manufacturing]
model: real-ram
complexity:
  vars: {n: number of triangles, k: number of slicing planes, m: number of triangle-plane segments}
  time: {expected: "O(n log k + k + m)", worst: "O(n log k + k + m log m)"}
  space: {extra: "O(n + k)"}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 2017
  people: [Rodrigo Minetto, Neri Volpato, Jorge Stolfi, Rodrigo M. M. H. Gregori, Murilo V. G. da Silva]
  note: Minetto, Volpato, Stolfi, Gregori and da Silva gave the bucket and sweep method with a lower bound in Computer-Aided Design. A corrigendum by Minetto and Stolfi in 2018 says that the bounds of the loop step are expected time.
prereqs: [indexed-face-set, manifold-mesh, binary-search, hash-table]
see_also: [adaptive-slicing, staircase-effect, vertex-welding, consistent-mesh-orientation, polygon-with-holes, sweep-line-technique, simulation-of-simplicity, contour-parallel-toolpath]
sources:
  - paper: doi:10.1016/j.cad.2017.07.001
    title: Rodrigo Minetto, Neri Volpato, Jorge Stolfi, Rodrigo M. M. H. Gregori and Murilo V. G. da Silva, An optimal algorithm for 3D triangle mesh slicing, Computer-Aided Design 92, 2017, 1 to 10
    locator: the slicing algorithm with buckets and a sweep, the lower bound, and the linking of segments with a hash table
  - paper: doi:10.1016/j.cad.2018.01.002
    title: Rodrigo Minetto and Jorge Stolfi, Corrigendum to An optimal algorithm for 3D triangle mesh slicing, Computer-Aided Design 98, 2018, 39
    locator: the correction that the bounds of the loop step hold in expected time
  - book: isbn:978-3-030-56126-0
    title: Ian Gibson, David Rosen, Brent Stucker and Mahyar Khorasani, Additive Manufacturing Technologies, 3rd edition, Springer, 2021
    locator: the chapter on the generalized additive manufacturing process chain (STL input and slicing)
  - book: isbn:978-1-56881-426-1
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, A K Peters, 2010
    locator: the chapter on mesh data structures (face sets, shared vertices and halfedges)
---

Triangle mesh slicing cuts a closed triangle mesh with the horizontal planes $z = Z_1 < Z_2 < \dots < Z_k$ and returns, for each plane, the closed polygons where the plane meets the solid. Each triangle that crosses a plane gives one segment. The segments of one plane are then linked end to end into loops. The method on this page is the one of Minetto, Volpato, Stolfi, Gregori and da Silva (2017). It puts each triangle into the bucket of the first plane above its lowest vertex with a [binary search](/binary-search/), sweeps the planes from the bottom up with a list of active triangles, and links the segments with a [hash table](/hash-table/) keyed by the crossed mesh edge. It runs in $O(n \log k + k + m)$ expected time for $n$ triangles and $m$ segments, which matches their lower bound. It is the first step of most [slicers for additive manufacturing](/slicing-for-additive-manufacturing/).

## In plain words

Think of a model made of many small flat triangles, like a paper shell. You cut it with flat horizontal knives at different heights, and for each knife you want the outline of the cut.

A triangle meets a knife only if the knife is between its lowest and its highest corner. So go up through the knives one by one, and keep a list of the triangles that the current knife can touch. Add a triangle when the knives reach its lowest corner, and drop it when they pass its highest corner.

Each touched triangle gives one short straight piece of the outline. Pieces from neighbouring triangles meet on their common edge, so a table keyed by edges gives the next piece. Follow the pieces until you come back to the start, and you have one closed outline.

## The problem

The input is a mesh with vertices $v_1, \dots, v_N \in \mathbb{R}^3$ and $n$ triangles given as index triples, an [indexed face set](/indexed-face-set/). The mesh is closed, oriented and edge-manifold: each edge belongs to exactly two triangles, and they traverse it in opposite directions. Each triangle is listed counterclockwise as seen from outside, so its normal $(v_b - v_a) \times (v_c - v_a)$ points out by the right-hand rule. The input also has plane heights $Z_1 < \dots < Z_k$.

The output is, for each $j$, a set of closed polygons in the plane $z = Z_j$. They are the boundary of the cross-section of the solid, with the solid on the left of each directed segment: outer loops run counterclockwise as seen from above, and holes run clockwise. This is the convention of [polygon orientation](/polygon-orientation/) and of [polygons with holes](/polygon-with-holes/). The total [shoelace](/shoelace-formula/) area of the loops of one plane is then the area of the cross-section.

**Degenerate cases.** A vertex can lie exactly at a plane height, an edge can lie in a plane, and a whole face can lie in a plane. Real models have many such cases, because layer heights are round numbers and so are the coordinates of flat faces. The rule of this page treats them as part of the input: a vertex with $z = Z_j$ counts as above the plane. This is the same as moving the plane to $Z_j - \varepsilon$ for an infinitely small $\varepsilon > 0$, a simple form of [simulation of simplicity](/simulation-of-simplicity/). With the rule, a triangle crosses the plane exactly when $z_{\min}(t) < Z_j \le z_{\max}(t)$, it has then exactly one vertex alone on its side, and it gives exactly one segment. A face that lies in the plane gives no segment.

## The algorithm

For a triangle $t$ and a height $z$, CROSS$(t, z)$ marks each vertex as above ($z_v \ge z$) or below ($z_v < z$). In the cyclic order of $t$, exactly one edge $e_{\text{out}}$ goes from an above vertex to a below vertex, and exactly one edge $e_{\text{in}}$ goes from below to above. CROSS returns $e_{\text{out}}$, the point $p$ where $e_{\text{out}}$ meets the plane, and $e_{\text{in}}$. An edge key is the unordered pair of its vertex indices. For the edge from $a$ to $b$, $p = a + (b - a)\,(z - z_a)/(z_b - z_a)$, and $z_a \ne z_b$ because one end is above and the other below. The segment of $t$ runs from $p$ to the point on $e_{\text{in}}$.

```pseudo id=main
SLICE(V, T, Z)                      ▷ mesh (V, T), heights Z[1] < ... < Z[k]
L1  B[1..k+1] ← empty lists
L2  for each triangle t ∈ T do
L3      j ← number of i with Z[i] ≤ zmin(t)           ▷ binary search
L4      append t to B[j + 1]                           ▷ first plane above zmin(t)
L5  A ← empty list                                     ▷ active triangles
L6  for j ← 1 to k do
L7      A ← A + B[j]
L8      remove from A each t with zmax(t) < Z[j]
L9      S ← empty hash table                           ▷ edge key → (point, edge key)
L10     for each t ∈ A do
L11         (e_out, p, e_in) ← CROSS(t, Z[j])
L12         S[e_out] ← (p, e_in)
L13     P[j] ← LINK(S)
L14 return P[1..k]

LINK(S)
L15 C ← empty list
L16 while S is not empty do
L17     e0 ← any key of S; e ← e0; L ← empty loop
L18     repeat
L19         (p, e') ← S[e]; delete S[e]; append p to L; e ← e'
L20     until e = e0
L21     append L to C
L22 return C
```

Lines L1 to L4 put each triangle into the bucket of the first plane strictly above its lowest vertex. Line L8 drops the triangles whose highest vertex is below the plane. After line L8, a triangle is in $A$ exactly when $z_{\min}(t) < Z_j \le z_{\max}(t)$, so every triangle in $A$ crosses the plane. Line L12 files the segment of $t$ under the edge where it starts. The segment that follows it in the loop starts where it ends, on the edge $e_{\text{in}}$, so line L19 finds it with one lookup.

The key is the edge and not the point. A vertex on the plane is the crossing point of several edges, so points are not unique keys there, but edges are. The loop then contains the vertex more than once, and a triangle with a vertex on the plane and an edge with both ends at the same side can give a segment of length zero. A later pass can remove repeated points. They do not change the area or the orientation of the loop.

**Exact arithmetic.** The only predicate is the comparison $z_v \ge Z_j$ of two input numbers, so the topology of the loops is exact even in floating point, if each plane height is one stored number and each vertex has one stored $z$. The points are constructions. With integer or rational input and [exact geometric computation](/exact-geometric-computation/) they are exact rationals, as in the code of this page. In floating point they are rounded, and the result depends on the direction of the edge. For the edge from $a = (0.1, 0.2, 0)$ to $b = (0.7, 0.9, 1)$ and $z = 0.3$, the formula from $a$ gives $(0.28, 0.41000000000000003)$, and the same formula from $b$ gives $(0.27999999999999997, 0.4100000000000001)$. A slicer that links segments by equal points then breaks a loop at such an edge. Edge keys avoid this, and so does computing each crossing point once per edge.

## Example

Take the tetrahedron with $v_0 = (0, 0, 0)$, $v_1 = (6, 0, 2)$, $v_2 = (0, 6, 4)$ and $v_3 = (2, 2, 8)$, with the faces $t_0 = (0, 2, 1)$, $t_1 = (0, 1, 3)$, $t_2 = (1, 2, 3)$ and $t_3 = (0, 3, 2)$, all counterclockwise from outside (the signed volume is $+36$). The planes are $Z = (1, 2, 4, 6)$.

| step | value |
|---|---|
| L1 to L4 | $z_{\min} = 0, 0, 2, 0$. Buckets: $B[1] = \{t_0, t_1, t_3\}$, and $B[3] = \{t_2\}$ because $Z[2] = 2 \le z_{\min}(t_2)$ |
| $j = 1$, L10 to L12 | $S[\{0,1\}] = ((3, 0), \{0,2\})$, $S[\{0,3\}] = ((\tfrac14, \tfrac14), \{0,1\})$, $S[\{0,2\}] = ((0, \tfrac32), \{0,3\})$ |
| $j = 1$, LINK | from $\{0,1\}$: $(3, 0) \to (0, \tfrac32) \to (\tfrac14, \tfrac14)$, back to $\{0,1\}$. Area $\tfrac{27}{16}$ |
| $j = 2$ | $v_1$ is on the plane and counts as above. $t_2$ is not active. Loop $(6, 0) \to (0, 3) \to (\tfrac12, \tfrac12)$, area $\tfrac{27}{4}$ |
| $j = 3$, L7 | $A = \{t_0, t_1, t_3, t_2\}$. No triangle is dropped, since $z_{\max}(t_0) = 4 \ge 4$ |
| $j = 3$, L11 | $t_0$ gives a segment of length zero at $v_2 = (0, 6)$. $t_1$ starts at $(1, 1)$, $t_2$ at $(\tfrac{14}{3}, \tfrac23)$, $t_3$ at $(0, 6)$ |
| $j = 3$, LINK | $(0, 6) \to (0, 6) \to (1, 1) \to (\tfrac{14}{3}, \tfrac23)$, area $9$ |
| $j = 4$, L8 | $t_0$ is dropped, since $z_{\max}(t_0) = 4 < 6$. Loop $(\tfrac32, \tfrac32) \to (\tfrac{10}{3}, \tfrac43) \to (1, 4)$, area $\tfrac94$ |

All four loops are counterclockwise, as outer loops must be. At $j = 1$ the cut points lie on the edges $v_0v_1$, $v_0v_2$ and $v_0v_3$ at the fractions $\tfrac12$, $\tfrac14$ and $\tfrac18$, and the shoelace formula on them gives $\tfrac{27}{16}$ directly. At $j = 3$ the loop is the triangle $v_2$, $(1, 1)$, $(\tfrac{14}{3}, \tfrac23)$ of area 9, with $v_2$ written twice.

## Correctness

After line L8 the active list holds exactly the triangles with $z_{\min} < Z_j \le z_{\max}$, because the planes increase, so a triangle that is dropped never crosses a later plane. Each such triangle has one or two above vertices and one or two below vertices, so its cyclic order has exactly one edge from above to below and one from below to above. A crossing edge belongs to two triangles that traverse it in opposite directions, so it is $e_{\text{out}}$ of one of them and $e_{\text{in}}$ of the other. The map from a segment to the segment that starts at its end edge is therefore a permutation of the segments of the plane, and LINK writes out its cycles, which are closed loops. A computation with the cross product shows that the outward normal of the triangle points to the right of its segment, so the solid is on the left. The full proof is below.

## Complexity

Lines L1 to L4 take $O(n \log k)$ time for the binary searches and $O(n + k)$ for the buckets. In the loop of line L6, every triangle is added once. At plane $j$, line L8 scans $|A|$ triangles, and each of them is either dropped, which happens once per triangle, or kept and gives a segment. So all scans together take $O(n + k + m)$ time. Lines L10 to L22 do $O(1)$ hash operations per segment. With hashing, each operation takes $O(1)$ expected time (see [universal hashing](/universal-hashing/)), so the total is $O(n \log k + k + m)$ expected time. With a balanced search tree in place of the hash table, the same steps take $O(n \log k + k + m \log m)$ time in the worst case.

When the planes are evenly spaced, $Z_j = Z_1 + (j - 1)\,h$, line L3 is the arithmetic $\lfloor (z_{\min} - Z_1)/h \rfloor + 1$, clamped to the range from $0$ to $k$, and the first term becomes $O(n)$. Minetto et al. state $O(n + k + m)$ for this case, and also when the triangles come sorted by their lowest vertex. They also prove a lower bound of $\Omega(n \log k + k + m)$ in the worst case for planes with arbitrary spacing, so the method is asymptotically optimal. The extra space is $O(n + k)$ for the buckets and the active list, and the table $S$ of one plane holds at most $n$ entries. The output itself has size $O(m)$.

## Properties

- **Exact.** With integer or rational coordinates, every point and every area is exact, also when planes pass through vertices, edges or faces.
- **Closed loops.** On a closed, oriented, edge-manifold mesh, every loop is closed, and every segment is in exactly one loop.
- **Oriented.** The solid is on the left of every segment. Outer loops are counterclockwise and holes are clockwise as seen from $+z$, so the sum of signed areas is the area of the cross-section.
- **One sided rule.** A vertex on the plane counts as above, so the result is the cross-section at $Z_j - \varepsilon$. The plane through the bottom face of a cube gives nothing, and the plane through the top face gives the full square.
- **Output sensitive.** The cost depends on $m$, not on $n k$.
- **Only one predicate.** The topology depends only on comparisons of input heights.

## Variants and improvements

- **One plane at a time.** The simplest slicer tests every triangle against every plane, in $\Theta(nk)$ time. It is the brute force that the tests of this page compare against.
- **Sorted triangles.** Sorting the triangles by $z_{\min}$ and sweeping gives $O(n \log n + k + m)$. The buckets of line L4 replace the sort and give $n \log k$ in place of $n \log n$.
- **Interval structures.** Each triangle is the interval $[z_{\min}, z_{\max})$, and a plane needs all intervals that contain it, a stabbing query in an [interval tree](/interval-tree/) or a [segment tree](/segment-tree/). This also allows planes in any order, at a cost of $O(\log n)$ per plane.
- **Edge numbers.** If the mesh is stored with numbered edges, for example in a [doubly connected edge list](/doubly-connected-edge-list/), the table $S$ can be an array indexed by the edge number, a [direct address table](/direct-address-table/). Resetting only the entries in use gives the bound in the worst case.
- **Meshes from STL.** STL files store each triangle with its own three points and no shared indices. [Vertex welding](/vertex-welding/) must first merge equal points into shared vertices. If the file has gaps or flipped faces, [mesh repair](/mesh-repair-problem/) and [consistent orientation](/consistent-mesh-orientation/) come first, or the loops do not close.
- **Variable layers.** [Adaptive slicing](/adaptive-slicing/) chooses the heights $Z_j$ from the surface slope. The method of this page then slices at those heights unchanged.

## When to use it

Use it to turn a mesh into layer outlines for additive manufacturing, for the planar [toolpaths](/contour-parallel-toolpath/) of machining, or for cross-section views. It needs a watertight, consistently oriented mesh with shared vertices. If the mesh may have holes or self-intersections, repair it first, or use a method that does not rely on edge adjacency, such as sampling an inside test on a grid and tracing the result with [marching squares](/marching-squares/). If you need only one plane, test each triangle once and skip the buckets.

## Pitfalls

- **Linking by points.** Floating point crossing points depend on the direction of the edge, and a vertex on the plane is the end of several segments. Key the table by the edge.
- **Epsilon shifts.** Moving every plane by a fixed small number, such as $10^{-6}$, makes vertex hits rarer but not impossible, and the right value depends on the scale of the model. The symbolic rule handles every case.
- **Rules that differ between triangles.** If one triangle counts a vertex as above and its neighbour counts it as below, the loop breaks. The rule must depend on the vertex only.
- **Unwelded meshes.** A mesh read from STL has no shared vertices, so the edge keys of neighbouring triangles never match.
- **Wrong orientation.** One flipped face reverses its segment, and the successor lookup fails at both of its ends. Check orientation before slicing.
- **Zero-length segments.** Faces with a vertex on the plane give repeated points. They are harmless for areas, but they can upset an offset or a toolpath step that expects distinct points.

## Implementations

## History

Slicers have cut triangle meshes into layers since the first stereolithography machines of the late 1980s, which read the STL format. For a long time the usual method tested each triangle against each plane, or sorted the triangles and swept, and linked the segments by comparing end points. Minetto, Volpato, Stolfi, Gregori and da Silva published the bucket and sweep method in Computer-Aided Design in 2017. They proved the $O(n \log k + k + m)$ bound, the matching lower bound, and the linear bound for evenly spaced planes. In 2018 Minetto and Stolfi published a corrigendum that states the bounds of the hash-based loop step as expected time.

## References
