---
tag: RBGNXS
kind: algorithm
slug: brep-reconstruction-from-scans
name: B-rep reconstruction from segmented scans
aliases:
- boundary model reconstruction
area: cad/reverse-engineering-and-inspection
level: research
summary: Benko, Martin and Varady's pipeline that fits faces to segments, computes edges and vertex blends between them and stitches a consistent B-rep.
solves: [reverse-engineering-of-geometric-models]
model: real-ram
complexity:
  vars: {m: the number of points, F: the number of regions, k: the largest number of points in the 27 grid cells around one cell, a: the number of adjacent pairs, T: the number of triangles of the adjacency graph, V: the number of vertices, E: the number of edges}
  time: {worst: "Θ(m k + F³ + T m + T V + a V log V + F E)"}
  space: {extra: "Θ(m + F² + V + E)"}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2001
  people: [Pál Benkő, Ralph R. Martin, Tamás Várady]
  note: They described a full procedure that turns a segmented multi-view point cloud of a conventional engineering part into a consistent boundary model, with primary surfaces, edges, blends and vertex blends.
prereqs: [boundary-representation, primitive-segmentation, geometric-primitive-fitting]
see_also: [euler-poincare-formula, euler-operators, brep-healing, constrained-primitive-fitting, rolling-ball-blend, vertex-blend, surface-surface-intersection, attributed-adjacency-graph]
sources:
  - paper: doi:10.1016/S0010-4485(01)00100-2
    title: Pál Benkő, Ralph R. Martin and Tamás Várady, Algorithms for reverse engineering boundary representation models, Computer-Aided Design 33(11), 2001, 839 to 851
    locator: the whole paper, which summarizes the phases of the approach, from segmentation and surface fitting to the creation of edges, blends and vertex blends and a topologically consistent B-rep (general locator; section numbers not confirmed)
  - paper: doi:10.1016/S0010-4485(96)00054-1
    title: Tamás Várady, Ralph R. Martin and Jordan Cox, Reverse engineering of geometric models, an introduction, Computer-Aided Design 29(4), 1997, 255 to 268
    locator: the sections on segmentation and surface fitting and on the creation of B-rep models, with the adjacency of regions, the intersection of the fitted surfaces and the stitching of faces
  - book: isbn:9780881751086
    title: Martti Mäntylä, An Introduction to Solid Modeling, Computer Science Press, 1988
    locator: Section 3.5.6, Euler characteristic (p. 43), for the check V − E + F = 2 of a closed solid without holes
---

B-rep reconstruction from segmented scans is the last step of [reverse engineering](/reverse-engineering-of-geometric-models/): it turns a point cloud that is already cut into regions, one region per face, into a [boundary representation](/boundary-representation/) with faces, edges, vertices and their connections. Benkő, Martin and Várady (2001) described the full procedure for conventional engineering parts. Each region gets a surface by [geometric fitting](/geometric-primitive-fitting/); two faces are neighbors when their regions touch; the edge of two neighbors lies on the curve where their surfaces meet; a vertex lies where three or more faces meet; blends and vertex blends are fitted in the gaps between the faces; and the pieces are stitched into one closed model whose topology is consistent. This page gives the core of that procedure for parts with planar faces and sharp edges, where every step is exact: fit a plane to each region, find the adjacent pairs, intersect planes into edge lines and vertices, cut the lines into edges, and close the face loops. The output is checked with the [Euler formula](/euler-poincare-formula/).

## In plain words

A scanner gives many points on the surface of a part, and an earlier step has sorted them into groups, one group for each flat side. Now a CAD model must be built. First, a flat plane is laid through each group. Then the method looks for groups that come close to each other: these sides touch, so they share an edge. Two touching planes cross in a straight line, and the edge lies on that line. Where three touching sides meet, their planes cross in one point, a corner, if the scan really comes close to that point. The corners cut each line into edges, and the edges of a side close into a ring around it. In the end the method counts corners, edges and sides, to check that the model is a closed solid.

## The problem

**Input.** Regions $R_1, \dots, R_F$ of points in space, where region $R_f$ samples one planar face $f$ of a solid, as a [segmentation into primitives](/primitive-segmentation/) gives them; a distance $\delta$ such that points of two faces that share an edge come within $\delta$ of each other; a distance $\eta$ such that every corner has points of each of its faces within $\eta$.

**Output.** A boundary model: a plane $n_f \cdot x = c_f$ with a unit normal $n_f$ for each face; the set $A$ of adjacent pairs of faces; vertices with the set of faces that meet at each; edges, each a pair of vertices with the two faces that meet along it; and for each face the cycle of its vertices around the boundary, or an empty loop if its edges do not close.

## The algorithm

```pseudo id=main
BREP-FROM-SEGMENTS(R_1..R_F, δ, η)
L1  for each region R_f: P_f ← the plane that minimizes the sum of squared orthogonal distances to R_f
L2  A ← the pairs {j, k} with some p in R_j and q in R_k and |p − q| ≤ δ
L3  for each {j, k} in A: ℓ_jk ← the line P_j ∩ P_k (none if the planes are nearly parallel)
L4  for each triangle {j, k, l} of the graph A: v ← P_j ∩ P_k ∩ P_l; keep v if R_j, R_k and R_l each have a point within η of v
L5  merge kept vertices within η of each other; a merged vertex gets the union of the face sets
L6  for each {j, k} in A: sort the vertices whose faces include j and k along ℓ_jk; join them in consecutive pairs into edges
L7  for each face f: loop_f ← the cycle formed by the edges of f, or empty if they do not form one cycle
L8  return the planes, A, the vertices, the edges and the loops
```

**Line L1.** The plane goes through the centroid of the region, with the normal along the eigenvector of the smallest eigenvalue of the covariance matrix, as in [principal component analysis](/principal-component-analysis/). It minimizes the sum of the squared orthogonal distances, which is the geometric distance; for a plane with a unit normal the algebraic distance $n \cdot x - c$ is the same as the geometric one, so this fit has none of the bias of algebraic fits of curved primitives.

**Line L2.** The points go into a grid of cubes of side $\delta$ with [spatial hashing](/spatial-hashing/); two points within $\delta$ lie in the same cube or in two cubes that touch, so each point is compared only with the points of $27$ cubes. This is a [fixed-radius near neighbors](/fixed-radius-near-neighbors/) search.

**Lines L3 and L4.** With $d = n_j \times n_k$, the line $P_j \cap P_k$ has the direction $d$ and passes through $x_0 = (c_j (n_k \times d) + c_k (d \times n_j)) / \lvert d \rvert^2$, which satisfies both plane equations. The vertex of three planes solves the $3 \times 3$ system with the rows $n_j, n_k, n_l$; it is rejected when the determinant is near $0$. The nearness test of line L4 keeps only the corners that the scan supports: three faces can be pairwise adjacent without a common corner, for example the three sides of a triangular prism, whose planes have no common point.

**Lines L5 to L7.** At a corner where four or more faces meet, several triangles give the same point, and line L5 joins them. A line can carry several edges of the same two faces when the faces touch at more than one place; consecutive vertices along the line, taken in pairs, give them. A face without holes has a boundary that is one cycle, which line L7 follows.

## Example

The box $[0, 2] \times [0, 1] \times [0, 0.5]$ is sampled at the centers of square cells of side $s = 0.1$ on each face: $100$ points on each of the two faces $x = 0$ and $x = 2$, $200$ on $y = 0$ and $y = 1$, and $50$ on $z = 0$ and $z = 0.5$, $700$ points in all. The points nearest to an edge are at distance $s/2$ from it on both faces, so the gap across an edge is $s / \sqrt 2 \approx 0.0707$; opposite faces are at least $0.5$ apart. So any $\delta$ in $[0.0707, 0.5)$ gives the true adjacency, and the run uses $\delta = \eta = 0.15$.

| step | result |
| --- | --- |
| L1 | six planes, for example $x = 0$ with the normal $(1, 0, 0)$, exact to the last digit |
| L2 | $12$ adjacent pairs: each face with the four faces that are not opposite to it |
| L3 | $12$ lines, for example $y = 0, z = 0$ along the $x$ axis for the faces $y = 0$ and $z = 0$ |
| L4 | $8$ triangles of the graph, one from each of the pairs $x = 0$ or $2$, $y = 0$ or $1$, $z = 0$ or $0.5$; each corner has points within $0.0707$ on its three faces, so all $8$ are kept |
| L5 | no merge: the corners are at least $0.5$ apart |
| L6 | each line carries $2$ corners, which give $1$ edge: $12$ edges |
| L7 | each face has a loop of $4$ corners, for example $(0,0,0), (0,1,0), (2,1,0), (2,0,0)$ on $z = 0$ |

So $V - E + F = 8 - 12 + 6 = 2$. The tests compare this result with the true box: the same $12$ adjacent pairs, the same $8$ corners within $10^{-12}$ with the same face sets, and the same $12$ edges with the same two faces each.

**Rigid motions and noise.** For $20$ boxes with random sides between $0.5$ and $2$, a random rotation and a random shift, sampled with $s = 0.1$, $\delta = 0.15$ and $\eta = 0.2$, and Gaussian noise of standard deviation $\sigma$ on every coordinate, the code gave these results (seed $7$):

| $\sigma$ | boxes with the true adjacency, corners and edges | largest corner error |
| --- | --- | --- |
| $0$ | $20$ of $20$ | $2.2 \times 10^{-15}$ |
| $0.002$ | $20$ of $20$ | $0.00195$ |
| $0.01$ | $20$ of $20$ | $0.0095$ |
| $0.03$ | $20$ of $20$ | $0.027$ |

These are measurements with the code of this page on these boxes, not a bound. The noise-free row agrees with the theorem below up to rounding; the other rows are not covered by it.

**A concave edge.** An L-shaped prism, the L $[0, 2] \times [0, 0.5] \cup [0, 0.5] \times [0, 1.5]$ extruded to the height $1$, has $8$ faces. The code finds $12$ corners, $18$ edges and $8$ faces, loops of $6$ corners on the two L-shaped faces and of $4$ on the six sides, and $V - E + F = 2$. The two faces at the concave edge are adjacent because their points come within $s / \sqrt 2$ of each other inside the corner.

## Correctness

The correctness file proves, in exact arithmetic, that the algorithm stops, and that it returns exactly the faces, the adjacency, the vertices, the edges and the face loops of a polyhedron when the data are exact and the two distances separate the right things:

- every region lies on the plane of its face and has three points that are not on one line;
- two faces that share an edge have points within $\delta$, and two faces that do not have none;
- each vertex is simple, with exactly three faces, has points of each of its faces within $\eta$, and is more than $\eta$ from every other vertex; for three pairwise adjacent faces without a common vertex, the planes have no common point or it is farther than $\eta$ from one of the regions;
- two faces share at most one edge, faces are disks, and the thresholds of lines L3 and L4 are below the angles of the true edges and vertices.

Then the result has the same numbers of vertices, edges and faces as the polyhedron, so $V - E + F = 2$ holds exactly when the polyhedron has no handles. The tests check this on random boxes ($20$ of $20$ exact) and on the L-shaped prism. Not proved: anything for noisy data, where the corners move with the planes and $\delta$ and $\eta$ can join or split faces and corners.

## Complexity

Line L1 is $\Theta(m)$, with $3 \times 3$ eigenproblems. Line L2 compares each point with the points of $27$ cells, $\Theta(m k)$. Line L4 lists the triples of faces, $\Theta(F^3)$, and tests each of the $T$ triangles against the points of three regions, $\Theta(T m)$ in the worst case; line L5 compares each new vertex with the $V$ kept ones, $\Theta(T V)$. Line L6 finds and sorts the vertices of each of the $a$ lines, $\Theta(a V \log V)$, and line L7 follows the edges of each face, $\Theta(F E)$. Together this is the bound in the front matter on the [real RAM](/real-ram/). For a part with bounded sampling density and faces of bounded degree, $k$, $T$, $V$ and $E$ are small and the work is dominated by $\Theta(m)$ for the fits and the hashing and $\Theta(T m)$ for the corner tests; a list of triangles from the adjacency lists, as in [triangle counting](/triangle-counting/), removes the $F^3$ term.

## Properties

- **Topology from data.** The adjacency, and with it the whole topology, comes from the distances between the regions, not from the planes; two planes that cross far from the part never make an edge.
- **Geometry from fits.** Vertices and edges come from the fitted planes, so they are sharper and more accurate than the scan points near the edges, which are often missing or noisy.
- **Invariant.** A rigid motion of the points moves the result with it, since every step uses distances and planes only.
- **Checkable.** The Euler formula and the closed loops show at once whether the model is a valid closed solid.
- **Greedy merge.** Line L5 joins each new vertex to the first kept vertex within $\eta$, so with noise the merged vertices can depend on the order of the faces.

## Variants and improvements

- **Curved faces.** Benkő, Martin and Várady handle faces that are simple analytic surfaces, such as cylinders, cones and spheres, and swept surfaces, and the edges come from [surface-surface intersection](/surface-surface-intersection/) instead of plane intersection.
- **Blends.** In real parts, sharp edges are often rounded. The procedure fits [rolling-ball blends](/rolling-ball-blend/) to the strips between the primary faces and fills the corners with [vertex blends](/vertex-blend/), so the edges are the boundaries of the blends, not plane intersections.
- **Constraints.** Faces that should be parallel, perpendicular or coaxial are fitted together with [constrained fitting](/constrained-primitive-fitting/), so that the model keeps the design intent and the corners are better placed.
- **Repair.** Gaps and small slivers that remain are closed with [B-rep healing](/brep-healing/), or kept with a local tolerance as in [tolerant modeling](/tolerant-modeling/).
- **Candidate selection.** Later methods intersect all candidate planes and choose the faces of the result by optimization, for example PolyFit by Nan and Wonka (2017), and learning methods such as Point2CAD (Liu and others, 2024) reconstruct the topology of curved faces from point clouds. The reference data for such methods are B-rep models, for example of the ABC data set (Koch and others, 2019).

## When to use it

Use it when the part is made of faces of known types, the scan covers all faces and a segmentation is available, for example from [efficient RANSAC](/efficient-ransac-shape-detection/) or [variable-order fitting](/variable-order-surface-fitting/), and the goal is a CAD model that a modeler can edit. For organic shapes without clear faces, a mesh from [surface reconstruction](/surface-reconstruction/), such as [Poisson reconstruction](/poisson-surface-reconstruction/), is the better target.

## Pitfalls

- **$\delta$ too small or too large.** Below the gap across an edge, $s / \sqrt 2$ for samples of spacing $s$, no faces are adjacent and nothing is built; the tests show this. Above the thickness of a thin wall, the two sides of the wall become adjacent.
- **$\eta$ too small.** The corner lies outside the data, at about $s / \sqrt 2$ from the nearest point or farther where the scan misses the edge; with a smaller $\eta$ no corner is kept, as the tests show.
- **Vertices of four or more faces.** At the apex of a square pyramid, the two pairs of opposite faces also come within $\delta$ of each other, and with noise the four planes meet in up to four nearby points, not one. Line L5 merges them only if they lie within $\eta$; otherwise short false edges appear.
- **Nearly parallel neighbors.** Two adjacent faces at a very flat angle meet in a line that moves far when the normals change a little, so a small fit error gives a large edge error.
- **Wrong segments.** One face split into two regions gives two coplanar planes whose line is not defined, and two faces in one region give a bad plane. The method needs a good segmentation.
- **Holes and inner loops.** A face with a hole has a boundary of several cycles, and line L7 then returns no loop; the full procedure needs loops with holes and the Euler formula with rings.

## Implementations

## History

Reverse engineering of CAD models from scans grew in the 1990s, and the survey of Várady, Martin and Cox (1997) set out the pipeline from points to segmentation, surface fitting and B-rep model building. Benkő, Martin and Várady (2001) described a full procedure for conventional engineering objects bounded by simple analytic surfaces, swept surfaces and blends, with the focus on boundary models that are accurate and topologically consistent, ready for CAD and manufacturing. The same group studied constrained fitting and the segmentation of smooth regions in the following years. Later work replaced fixed rules with optimization and learning, as in PolyFit and Point2CAD.

## References
