---
tag: JMSVP1
kind: algorithm
slug: topological-tetrahedral-mesh-improvement
name: Topological tetrahedral mesh improvement
aliases:
- multi-face removal
- aggressive tetrahedral mesh improvement
area: cad/mesh-generation-for-analysis
level: research
summary: Improves a tetrahedral mesh by edge removal, multi-face removal, flips and vertex insertion chosen to raise the worst quality, as Shewchuk and Klingner did.
solves: [mesh-generation]
model: real-ram
complexity:
  vars: {n: the number of tetrahedra}
  time: {flip: O(1), pass: O(n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 2007
  people: [Bryan Matthew Klingner, Jonathan Richard Shewchuk, Barry Joe, Lori A. Freitag, Carl Ollivier-Gooch]
  note: Joe studied local flips for tetrahedral quality in 1995, and Freitag and Ollivier-Gooch combined flips with smoothing in 1997. Klingner and Shewchuk combined edge removal, multi-face removal, smoothing and vertex insertion in 2007.
prereqs: [tetrahedralization, edge-flip, mesh-quality-measures]
see_also: [optimization-based-mesh-smoothing, sliver-exudation, tetrahedral-delaunay-refinement, schonhardt-polyhedron, flip-graph, mesh-untangling, optimal-delaunay-triangulation, constrained-delaunay-tetrahedralization]
sources:
  - paper: doi:10.1007/978-3-540-75103-8_1
    title: Bryan Matthew Klingner and Jonathan Richard Shewchuk, Aggressive tetrahedral mesh improvement, Proceedings of the 16th International Meshing Roundtable, Springer, 2007, 3 to 23
    locator: edge removal, multi-face removal, the smoothing and vertex insertion steps, the hill climbing schedule and the measured dihedral angles (general locator)
  - paper: doi:10.1137/0916075
    title: Barry Joe, Construction of three-dimensional improved-quality triangulations using local transformations, SIAM Journal on Scientific Computing 16(6), 1995, 1292 to 1307
    locator: the local transformations of tetrahedral meshes, including the 2-3 and 3-2 flips, applied to raise a quality measure (general locator)
  - book: isbn:978-1-58488-730-0
    title: Siu-Wing Cheng, Tamal K. Dey and Jonathan R. Shewchuk, Delaunay Mesh Generation, CRC Press, 2012
    locator: chapter 4 (bistellar flips of tetrahedra and their validity conditions)
---

Topological tetrahedral mesh improvement changes which vertices make up the tetrahedra of a mesh, without moving the vertices, to raise the quality of the worst tetrahedra. The basic moves are the 2-3 flip, which replaces two tetrahedra on a shared triangle by three around a new edge, and its inverse, the 3-2 flip. Edge removal generalises the 3-2 flip to an edge with any number of tetrahedra around it, and multi-face removal generalises the 2-3 flip to a stack of triangles. Klingner and Shewchuk combined these moves with smoothing and vertex insertion in a hill climbing scheme that accepts a move only if it raises the worst quality nearby, and got meshes with all dihedral angles far from 0° and 180° on their tests. The validity of each flip and the termination of hill climbing are proved; the quality of the result is only measured.

## In plain words

A tetrahedral mesh fills a solid with small four-cornered pieces. A bad piece is flat, like a coin, and spoils a simulation. Sometimes the corners are in good places, but they are joined the wrong way.

Look at two pieces glued on a common triangle. Their five corners can also be joined as three pieces around the line between the two far corners. That swap is a 2-3 flip, and the reverse is a 3-2 flip. It is allowed only if that line passes through the inside of the shared triangle; otherwise the new pieces would stick out or overlap.

The method tries all such swaps, and keeps a swap only if the worst of the new pieces is better than the worst of the old ones. It stops when no swap helps. Larger swaps, moving corners and adding corners help it get further. A program measures the result.

## The problem

The input is a valid tetrahedral mesh: positively oriented tetrahedra with disjoint interiors that meet face to face. The goal is a mesh of the same region with the same boundary triangles, on the same vertices or on a few more, whose worst tetrahedron is as good as possible under a measure from the [mesh quality measures](/mesh-quality-measures/). This page uses the mean ratio $12(3V)^{2/3}/\sum \ell^2$, which is 1 for the regular tetrahedron and 0 for a flat one. Klingner and Shewchuk also used the smallest sine of the six dihedral angles and a volume-length measure.

The radius-edge ratio, used by [tetrahedral Delaunay refinement](/tetrahedral-delaunay-refinement/), is $\sqrt6/4$ for the regular tetrahedron, but a sliver, a flat tetrahedron whose four vertices lie near a circle, can have a small radius-edge ratio too. Slivers pass a radius-edge bound, which is why improvement works with measures that see them, such as the mean ratio or dihedral angles.

## The algorithm

orient3d is six times the signed volume, computed exactly. $q$ is the quality. Faces and edges are scanned in a fixed order, and the first improving flip is applied.

```pseudo id=main
FLIP-23(abc, d, e)                  ▷ tetrahedra abcd and abce share abc
L1  if orient3d(a,b,d,e), orient3d(b,c,d,e), orient3d(c,a,d,e) do not have one strict sign then fail
L2  return abde, bcde, cade, each ordered so that orient3d > 0

FLIP-32(de, ring abc)               ▷ exactly three tetrahedra contain the interior edge de
L3  if orient3d(a,b,c,d) · orient3d(a,b,c,e) ≥ 0 then fail
L4  return abcd, abce, each ordered so that orient3d > 0

IMPROVE(M)
L5  repeat
L6      for each face abc shared by two tetrahedra abcd and abce of M do
L7          N ← FLIP-23(abc, d, e)
L8          if N ≠ fail and min q(N) > min(q(abcd), q(abce)) then replace them by N; restart at L5
L9      for each interior edge de in exactly three tetrahedra, with ring abc, do
L10         N ← FLIP-32(de, abc)
L11         if N ≠ fail and min q(N) > min q of the three then replace them by N; restart at L5
L12 until no flip was applied in the pass
L13 return M
```

L1 is the exact form of the condition that the segment $de$ crosses the interior of the triangle $abc$. L3 asks that $d$ and $e$ are strictly on opposite sides of the plane $abc$; given that the three tetrahedra around $de$ are valid, this is the same crossing condition seen from the other side. L8 and L11 make the method hill climbing on the worst local quality.

## Example

Take the triangle $a = (0,0,0)$, $b = (4,0,0)$, $c = (2,4,0)$ and the apexes $d = (2,1,1)$ above and $e = (2,1,-1)$ below. The two tetrahedra $abcd$ and $abce$ are flat: each has $6V = 16$ and mean ratio $0.6154$. The values in L1 are $[abde] = -8$, $[bcde] = -12$, $[cade] = -12$, one strict sign, because the segment $de$ meets the plane $z = 0$ at $(2, 1, 0)$, inside $abc$. The flip gives three tetrahedra with $6V = 8, 12, 12$, which add up to 32, the old total $16 + 16$. Their mean ratios are $0.6872$, $0.7076$ and $0.7076$, so the worst rises from $0.6154$ to $0.6872$, and L8 accepts the flip.

A valid flip is not always an improvement. With $c = (0,4,0)$, $d = (1,1,3)$, $e = (1,1,-2)$, the old pair has $6V = 48$ and $32$ and mean ratios $0.8836$ and $0.7775$; the flip is valid, with $6V = 20, 40, 20$ that add up to 80, but the worst new mean ratio is $0.6121$, so hill climbing rejects it. If $e$ moves to $(5,5,-1)$, the segment $de$ misses the triangle, L1 fails, and the flip would make overlapping tetrahedra.

On the cube $[0,3]^3$ cut into 162 tetrahedra by the Kuhn split, with the interior vertices moved randomly by up to $1/2$, hill climbing made 6 flips in one run and raised the worst mean ratio from $0.125$ to $0.188$, and 8 flips in another, from $0.212$ to $0.263$. In a third run it made 4 flips but the worst tetrahedron, which no single flip could reach, stayed at $0.142$. These are measurements.

## Correctness

The full proofs are in the proof file. The key fact is a five-point identity: for any five points, the alternating sum of the signed volumes of the five tetrahedra that leave out one point is zero. Applied to $a, b, c, d, e$, it says that the two old volumes add up to the three new ones, so the flip keeps the volume. Lemma 2 of the proof shows that the three new orientations are $-\frac1s$ times the barycentric coordinates of the crossing point $p$ of $de$ with the plane $abc$, times $[abcd]$. So they have one strict sign exactly when $p$ is inside $abc$, which is the validity condition. The new tetrahedra then have disjoint interiors and the same six boundary triangles as the old pair, so the rest of the mesh still fits. The 3-2 flip is the inverse.

Hill climbing stops: each accepted flip makes the sorted list of qualities lexicographically larger, and a fixed vertex set has only finitely many tetrahedral meshes, so no mesh repeats.

What is proved: every flip keeps a valid mesh of the same region with the same boundary, the worst quality never decreases, and the loop stops. What is not proved: any bound on the angles. In a measured run, a $2 \times 2 \times 2$ cube mesh whose smallest dihedral angle was $34.4°$ was scrambled by random valid flips to a mesh with smallest dihedral angle $2.53°$, and hill climbing with 2-3 and 3-2 flips alone could not raise it at all.

## Complexity

A flip test and a flip cost $O(1)$ with an adjacency structure. A pass over all faces and edges costs $O(n)$ for $n$ tetrahedra. The number of flips has no useful proved bound beyond the finite number of meshes, but in practice each flip is local and the number is a small multiple of the number of bad tetrahedra. Klingner and Shewchuk keep a queue of tetrahedra below a quality threshold and work only around them. Edge removal on an edge with $k$ tetrahedra around it chooses the best triangulation of the ring of $k$ vertices by dynamic programming in $O(k^3)$ time, and $k$ is small, typically below 10. The simple implementation here rescans the mesh after each flip, which costs $O(n)$ per flip. The space is $O(n)$.

## Properties

- **Valid output, proved.** Each flip passes exact orientation tests, so no tetrahedron inverts, and the boundary is kept.
- **Monotone, proved.** The worst quality never decreases.
- **Terminates, proved.** The sorted quality list increases.
- **No quality guarantee.** The result is a local optimum of local moves; its angles are measured.
- **No moved vertices.** Flips change only the connectivity. Smoothing and vertex insertion are separate steps that are combined with them.

## Variants and improvements

- **Edge removal.** An edge with $k$ tetrahedra around it, whose other vertices form a ring of $k$ points, is removed by replacing the $k$ tetrahedra by $2k - 4$: the ring is triangulated, and each triangle is joined to both ends of the edge. The best ring triangulation, which maximises the worst new tetrahedron, is found by dynamic programming over polygon triangulations, as in Klincsek's algorithm. The 3-2 flip is the case $k = 3$.
- **Multi-face removal.** The inverse of edge removal: a stack of triangles that separate two vertices $d$ and $e$ is removed, and the tetrahedra around the new edge $de$ replace those on the triangles. Shewchuk found the best set of triangles to remove by a dynamic program over a tree of candidate faces. The 2-3 flip is the case of one triangle.
- **Smoothing.** Moving vertices by [optimization-based mesh smoothing](/optimization-based-mesh-smoothing/) raises the worst dihedral angle where flips cannot. Klingner and Shewchuk alternate it with the flips.
- **Vertex insertion.** Inserting a new vertex inside a bad region, and then removing the bad tetrahedra around it by flips, escapes local optima.
- **Sliver exudation.** [Sliver exudation](/sliver-exudation/) instead changes the weights of a weighted Delaunay triangulation, with a proved but tiny angle bound.
- **Delaunay flips.** The same flips with the in-sphere test give a 3D Delaunay flip algorithm, but in 3D flips alone cannot always reach the Delaunay triangulation from any start, unlike in the plane.

## When to use it

Use it after a tetrahedral mesh generator, such as Delaunay refinement or an advancing front method, to remove slivers and flat tetrahedra before a finite element solve, especially when large dihedral angles hurt the solver. Combine it with smoothing. When the boundary may not change, apply flips only to interior faces and edges, as here. If a proved bound is needed, use a method with a theorem, but expect weaker angles than the measured ones of aggressive improvement.

## Pitfalls

- **Validity in floats.** A nearly flat configuration can pass a float test and produce an inverted tetrahedron. Use exact orientation tests, as here.
- **Accepting any valid flip.** A valid flip can lower the quality, as in the example. Compare the worst quality of the old and new tetrahedra.
- **Boundary faces.** A flip on a boundary face or edge changes the boundary. Restrict the flips, or check that the boundary triangles stay on the boundary surface.
- **Stopping too early.** 2-3 and 3-2 flips alone reach poor local optima. Use edge removal, multi-face removal, smoothing and vertex insertion together.
- **Wrong measure.** The radius-edge ratio does not see slivers, so improving it does not remove them.

## Implementations

## History

Barry Joe studied local transformations of tetrahedral meshes, including the 2-3 and 3-2 flips, to raise a quality measure in 1995. Freitag and Ollivier-Gooch combined face and edge swapping with optimisation-based smoothing in 1997 and measured which combinations work best. Shewchuk described edge removal and multi-face removal with dynamic programming in a 2002 manuscript, and Klingner and Shewchuk combined them with smoothing and vertex insertion in a hill climbing scheme in 2007; with their best settings, all dihedral angles of their test meshes lay between $31°$ and $149°$, a measured result.

## References
