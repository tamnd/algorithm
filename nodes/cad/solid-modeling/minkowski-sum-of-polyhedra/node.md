---
tag: EBNP81
kind: algorithm
slug: minkowski-sum-of-polyhedra
name: Minkowski sum of polyhedra
aliases:
- polyhedral Minkowski sum
area: cad/solid-modeling
level: advanced
summary: Computes the Minkowski sum of two polyhedra; convex polytopes add face by face through support functions, and general polyhedra go through convex pieces, with up to O(n^3 m^3) output.
solves: [minkowski-sum]
model: word-ram
complexity:
  vars: {n: the number of vertices of P, m: the number of vertices of Q}
  time: {worst: "O(n m (n + m))"}
  space: {extra: "O(n m)"}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 2007
  people: [Efi Fogel, Dan Halperin]
  note: Fogel and Halperin computed exact Minkowski sums of convex polyhedra by overlaying their Gaussian maps on the sphere, with exact arithmetic in CGAL.
prereqs: [minkowski-sum, support-function, convex-polytope]
see_also: [minkowski-sum-convex-polygons, convex-hull-3d, convex-decomposition, nef-polyhedron, solid-offsetting, swept-volume, gjk-algorithm, configuration-space]
sources:
  - paper: doi:10.1016/j.cad.2007.05.017
    title: Efi Fogel and Dan Halperin, Exact and efficient construction of Minkowski sums of convex polyhedra with applications, Computer-Aided Design 39(11), 929 to 940, 2007
    locator: the Gaussian map of a convex polyhedron, the overlay of two Gaussian maps as the Gaussian map of the sum, and the exact implementation
  - paper: doi:10.1007/s00454-009-9159-1
    title: Efi Fogel, Dan Halperin and Christophe Weibel, On the exact maximum complexity of Minkowski sums of polytopes, Discrete and Computational Geometry 42(4), 654 to 669, 2009
    locator: the tight bound on the number of facets of the sum of two convex polytopes in three dimensions (the conference version, SoCG 2007, states it as 4mn - 9m - 9n + 26 for summands with m and n facets)
  - paper: doi:10.1007/s00453-008-9219-6
    title: Peter Hachenberger, Exact Minkowksi sums of polyhedra and exact and efficient decomposition of polyhedra into convex pieces, Algorithmica 55(2), 329 to 345, 2009
    locator: the decomposition of nonconvex polyhedra into O(r^2) convex pieces, the pairwise sums and their union with Nef polyhedra (the word Minkowksi is spelled this way in the printed title)
  - book: isbn:9781107601017
    title: Rolf Schneider, Convex Bodies, The Brunn-Minkowski Theory, second edition, Cambridge University Press, 2014
    locator: Section 1.7 on support functions and their additivity, and Chapter 2 on faces and normal cones of convex bodies
---

The Minkowski sum of two solids $P$ and $Q$ is $P \oplus Q = \{p + q : p \in P, q \in Q\}$: the region that $Q$ covers when its reference point moves over all of $P$. In solid modeling it grows a part by a tool shape, as in [offsetting](/solid-offsetting/) with a ball, gives the region a translating tool sweeps along a segment, and gives the [configuration space](/configuration-space/) obstacles for a robot that translates. The plane version is on the [Minkowski sum](/minkowski-sum/) page, with the merge for [convex polygons](/minkowski-sum-convex-polygons/). In three dimensions the convex case is still easy: the support functions add, so each face of the sum is the sum of a face of $P$ and a face of $Q$ with the same outer normal, and the sum of two convex polytopes has $O(nm)$ faces. The general case goes through a [convex decomposition](/convex-decomposition/) of both solids, the pairwise sums of the pieces and a union of up to quadratically many convex polytopes, and the result can have $\Theta(n^3 m^3)$ faces. This page gives the convex step exactly, with integer arithmetic.

## In plain words

Take a box and a little pyramid. Put a copy of the pyramid at every point of the box. The result is a bigger convex shape.

Look at the result from any side. The part of it that sticks out furthest toward you is the part of the box that sticks out furthest that way, plus the part of the pyramid that sticks out furthest that way. Those parts can be a corner, an edge or a flat face. Two corners give a corner, a corner and a face give a copy of the face, and two edges that are not parallel give a flat four-sided face.

So the flat faces of the result come from three places: the faces of the box, the faces of the pyramid, and pairs of edges, one from each. The method lists all these candidates and keeps the ones that give a flat face.

## The problem

**Input.** Two finite point sets $P$ and $Q$ in $\mathbb{R}^3$ with integer coordinates, each with a three-dimensional convex hull. We write $P$ and $Q$ also for the hulls, the convex polytopes. $P$ has $n$ points, $Q$ has $m$.

**Output.** The facets of $P \oplus Q$: for each facet, its outer normal $u$ as a primitive integer vector and the cycle of its vertices in counterclockwise order seen from outside.

**Notation.** For a direction $u \neq 0$, $h_K(u) = \max_{x \in K} u \cdot x$ is the [support function](/support-function/) and $F(K, u) = \{x \in K : u \cdot x = h_K(u)\}$ is the face of $K$ in direction $u$. For a finite set, $F$ is the set of points that attain the maximum. A face is a *facet* if it spans a plane and an *edge* if it spans a line. The *normal cone* of a face $G$ is the set of $u$ with $F(K, u) \supseteq G$.

The key fact is the additivity of support functions and faces:

$$h_{P \oplus Q}(u) = h_P(u) + h_Q(u), \qquad F(P \oplus Q, u) = F(P, u) \oplus F(Q, u).$$

The first equation is item 4 on the support function page. The second follows: $u \cdot (p + q) = h_P(u) + h_Q(u)$ with $u \cdot p \le h_P(u)$ and $u \cdot q \le h_Q(u)$ holds only if both are equalities. So the faces of the sum are sums of faces of the summands with a common normal, and a facet of the sum with normal $u$ comes from one of three cases: a facet of $P$ plus a face of $Q$, a face of $P$ plus a facet of $Q$, or an edge $e$ of $P$ plus an edge $f$ of $Q$ that are not parallel, with $u$ perpendicular to both, that is $u = \pm\, e \times f$.

## The algorithm

```pseudo id=main
MINKOWSKI-SUM-CONVEX(P, Q)
L1  N ← the outer facet normals of P and of Q
L2  for each edge direction e of P and each edge direction f of Q do
L3      if e × f ≠ 0 then add e × f and −(e × f) to N, as primitive integer vectors
L4  S ← an empty map from normals to facets
L5  for each u in N do
L6      A ← F(P, u); B ← F(Q, u)                     ▷ two support queries
L7      if the points a + b, a ∈ A, b ∈ B, span a plane then
L8          S[u] ← the convex polygon of these points, counterclockwise seen from u
L9  return S
```

Line L1 needs the facets of $P$ and $Q$. A B-rep gives them; for point sets, the code finds them by brute force over triples of points. The edges of line L2 come from the facets: if $u_1$ and $u_2$ are the normals of two adjacent facets, then $F(P, u_1 + u_2)$ is their common edge. Line L3 adds both signs, since the cross product does not tell which side the facet is on; line L7 rejects the wrong sign and every pair whose Gauss arcs do not cross. The vertices of the sum are the vertices of its facets.

Fogel and Halperin do lines L2 to L7 in one pass: the *Gaussian map* of a convex polytope puts each facet normal as a point on the unit sphere, each edge as a great arc between the normals of its two facets, and each vertex as the spherical region of its normal cone. The Gaussian map of $P \oplus Q$ is the overlay of the two maps, so the edge pairs that give facets are exactly the pairs of arcs that cross, and a sweep over the sphere finds them without testing all $E_P E_Q$ pairs.

## Example

Let $T$ be the tetrahedron with corners $(0,0,0), (1,0,0), (0,1,0), (0,0,1)$ and $C$ the unit cube $[0,1]^3$. Line L1 gives the 4 normals of $T$ and the 6 of $C$. The three normals $(-1,0,0)$, $(0,-1,0)$ and $(0,0,-1)$ are shared, so $N$ has 7 vectors so far. $T$ has 6 edge directions and $C$ has 3, which give 15 non-parallel pairs, and line L3 brings $N$ to 13 vectors. Lines L5 to L8 then do this:

| $u$ | $F(T, u)$ | $F(C, u)$ | sum spans | result |
|---|---|---|---|---|
| $(1,1,1)$ | facet $x + y + z = 1$ | vertex $(1,1,1)$ | plane | triangle |
| $(-1,0,0)$, $(0,-1,0)$, $(0,0,-1)$ | facet | facet | plane | pentagon, 5 vertices each |
| $(1,0,0)$, $(0,1,0)$, $(0,0,1)$ | vertex | facet | plane | unit square, 4 vertices each |
| $(1,1,0)$, $(1,0,1)$, $(0,1,1)$ | edge, such as $(1,0,0)(0,1,0)$ | edge, such as $(1,1,0)(1,1,1)$ | plane | parallelogram |
| $(-1,-1,0)$, $(-1,0,-1)$, $(0,-1,-1)$ | edge, such as $(0,0,0)(0,0,1)$ | the parallel edge $(0,0,0)(0,0,1)$ | line | rejected |

The sum has $1 + 3 + 3 + 3 = 10$ facets and 13 vertices, so it has 21 edges, and $13 - 21 + 10 = 2$ as Euler's formula requires. The pentagon on the plane $x = 0$ has the vertices $(0,0,0), (0,2,0), (0,2,1), (0,1,2), (0,0,2)$. In the three rejected rows, an edge of $T$ is parallel to an edge of $C$, and their sum is a longer edge of $P \oplus Q$, not a facet.

Two more sums that the tests check: the tetrahedron $T$ plus its reflection $-T$ gives a cuboctahedron, with 8 triangles, 6 squares and 12 vertices. The cube plus the octahedron with vertices $\pm e_i$ gives 6 squares, 8 triangles and 12 rectangles, 26 facets and 24 vertices.

## Correctness

The face identity above says that $F(P \oplus Q, u) = A \oplus B$ for the sets of line L6, so a candidate $u$ that passes line L7 is the normal of a facet of the sum, and line L8 records that facet. Conversely, let $u$ be the outer normal of a facet of the sum. The facet is $A \oplus B$, whose span is the sum of the spans of $A$ and $B$. If $A$ spans a plane, $u$ is the normal of a facet of $P$, which is in $N$ by line L1; the same holds for $B$. Otherwise each of $A$ and $B$ is a vertex or an edge, and their spans add up to a plane only if both are edges with directions $e$ and $f$ that are not parallel. Then $u$ is perpendicular to $e$ and $f$, so it is a positive multiple of $e \times f$ or of $-(e \times f)$, and line L3 added both. Every edge of $P$ is the intersection of two facets, so the edge directions of line L2 cover all edges. So $S$ is exactly the set of facets of the sum. The full proof is in the proof file.

The tests check that the vertices of the output attain $h_P(w) + h_Q(w)$ for all 124 integer directions $w$ with entries in $\{-2, \ldots, 2\}$ on 500 random pairs, and for all 728 directions with entries in $\{-4, \ldots, 4\}$ on 60 larger pairs. They check that each facet is a supporting plane that touches exactly its listed vertices, in counterclockwise order, that $V - E + F = 2$, and on 80 small pairs that the facets and vertices equal those of the convex hull of all $nm$ vertex sums, found by brute force over triples.

## Complexity

- The set $N$ has at most $F_P + F_Q + 2 E_P E_Q$ vectors, where $F$ and $E$ count facets and edges. By Euler's formula a convex polytope with $n$ vertices has at most $3n - 6$ edges and $2n - 4$ facets, so $|N| = O(nm)$.
- Each candidate needs two support queries in $O(n + m)$ time and a plane hull of $|A| \cdot |B|$ points, so the total time is $O((n + m) \cdot nm)$ in the worst case. The code adds the brute-force facet search on point sets, $O(n^4 + m^4)$; a B-rep input avoids it.
- The output has $O(nm)$ facets, and this is tight: for two prisms over regular $k$-gons, one turned by a right angle, the arcs of the top and bottom edges of each prism cross $\Theta(k^2)$ arcs of the other. Fogel, Halperin and Weibel found the exact maximum number of facets of the sum of two convex polytopes; the conference version of their paper states it as $4mn - 9m - 9n + 26$ for summands with $m$ and $n$ facets, and the tests check this bound on 300 random pairs.
- With the Gaussian map overlay, the time is the time of a map overlay on the sphere, $O((n + m + k) \log (n + m))$ for $k$ crossings by a plane sweep, which is near linear in the output.
- For nonconvex polyhedra the output can have $\Theta(n^3 m^3)$ faces, so no method is better than that in the worst case.

## Properties

- **Exact.** Every quantity is an integer: the normals are cross products of integer vectors, and the faces are found by comparing integer dot products. No tolerance is needed, and degenerate inputs, such as parallel edges or coplanar faces, are handled by line L7 and not by special cases.
- **Output sensitive with the overlay.** The plain version tests $\Theta(E_P E_Q)$ pairs even when few of them cross; the Gaussian map overlay pays only for the crossings.
- **Symmetric.** The output does not depend on the order of $P$ and $Q$.
- **The sum of a polytope and a segment.** If $Q$ is a segment, the sum is the region a translating $P$ sweeps, the extrusion case of the [sweep representation](/sweep-representation/) for a convex profile.

## Variants and improvements

- **Convex hull of vertex sums.** The sum of two convex polytopes is the convex hull of the $nm$ sums of vertices, which a [3D convex hull](/convex-hull-3d/) algorithm computes in $O(nm \log(nm))$ time. It is short to code but does $\Theta(nm)$ work even when the sum has few faces.
- **Gaussian map overlay.** Fogel and Halperin's method, with exact arithmetic in CGAL. They also used the sum $P \oplus (-Q)$ for collision detection and penetration depth.
- **Nonconvex polyhedra by decomposition.** Decompose both polyhedra into convex pieces, add each pair of pieces with the convex method, and take the union of all pairwise sums. Hachenberger made this exact, with a decomposition into $O(r^2)$ pieces for $r$ reflex edges and the union computed with [Nef polyhedra](/nef-polyhedron/); this is the method of CGAL's 3D Minkowski sum. The union is the expensive step.
- **Convolution.** As in the plane, a candidate surface is formed from facet and vertex pairs and from edge and edge pairs whose normals match, and the sum is the part of space where this surface has a positive winding number. It avoids the decomposition, but the arrangement of the candidate surface is hard to compute robustly in three dimensions.
- **Approximation.** Voxel grids and distance fields give approximate sums with a bounded error, used when the inputs are meshes with many faces.
- **Minkowski difference.** For convex $P$ and $Q$, the set $\{x : x + Q \subseteq P\}$ is the polytope cut out by the facet planes of $P$, each moved inward by $h_Q$ of its normal: $x + Q \subseteq P$ exactly when $u \cdot x + h_Q(u) \le h_P(u)$ for every facet normal $u$ of $P$.

## When to use it

Use the convex method whenever both solids are convex, or when one is convex and the other is a union of a few convex pieces: tool shapes in machining, convex hulls of robot links, bounding shapes in collision tests. For questions that need only one direction at a time, such as distance and intersection tests between convex shapes, do not build the sum at all; [GJK](/gjk-algorithm/) uses the support function of $P \oplus (-Q)$ directly. For offsets of a solid by a ball, the sum has spherical and cylindrical faces, and the dedicated offsetting methods are simpler. Use the decomposition method for general polyhedra only when an exact result matters, as in assembly planning, since its output and time can be very large.

## Pitfalls

- **Only one sign of $e \times f$.** The cross product of two edge directions gives the line of the normal, not its side. Test both signs, as line L3 does.
- **Parallel edges.** If $e \times f = 0$, the edges add to a longer edge, not a facet. Skip the pair, or the code divides by zero when it normalizes the vector.
- **Floating-point normals.** With floating-point coordinates, two nearly parallel facets of the sum can come out as two facets with a sliver between them, or a face can appear that does not exist. Use integer or rational coordinates and exact dot products, or merge normals with a tolerance and accept that the result is approximate.
- **Points that are not vertices.** A face found by support queries can contain points of the input that are not vertices, for example the middle of an edge. Take the plane hull of the face, as line L8 does, instead of all points.
- **Nonconvex inputs.** The face rule holds only for convex sets. For a nonconvex solid, the support face in a direction says nothing about the dents, so the convex method gives the convex hull of the sum, not the sum.

## Implementations

## History

Minkowski defined the sum of convex bodies around 1900 in his work on convex bodies and mixed volumes, and the additivity of support functions was part of that theory. In robotics, Lozano-Pérez used sums of convex polygons and polyhedra for configuration space obstacles in the late 1970s and early 1980s, and in solid modeling, Rossignac and Requicha used sums with a ball to define offsets in 1986. Fogel and Halperin gave an exact and fast construction of the sum of convex polyhedra through Gaussian maps in 2007. Fogel, Halperin and Weibel settled the exact maximum number of facets of the sum of two convex polytopes in 2007 and 2009, and Hachenberger gave the first exact implementation for nonconvex polyhedra by decomposition and Nef polyhedra in 2007, published in 2009.

## References
