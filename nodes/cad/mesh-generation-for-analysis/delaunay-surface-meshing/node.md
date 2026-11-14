---
tag: 8F2351
kind: algorithm
slug: delaunay-surface-meshing
name: Delaunay refinement surface meshing
aliases:
- Boissonnat-Oudot surface mesher
area: cad/mesh-generation-for-analysis
level: research
summary: Boissonnat and Oudot's mesher that inserts points of a smooth surface until the restricted Delaunay triangulation is a good, homeomorphic approximation.
solves: [mesh-generation]
model: real-ram
complexity:
  vars: {n: the number of output vertices}
  time: {worst: O(n^3)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2005
  people: [Jean-Daniel Boissonnat, Steve Oudot]
  note: Boissonnat and Oudot turned Chew's 1993 surface mesher into an algorithm with proofs, showing that its output is a loose epsilon-sample whose restricted Delaunay triangulation is homeomorphic and close to the surface.
prereqs: [restricted-delaunay-triangulation, delaunay-refinement, bowyer-watson-algorithm]
see_also: [chew-second-algorithm, protecting-balls, surface-reconstruction, marching-cubes, isosurface-extraction, parametric-surface-meshing, tetrahedral-delaunay-refinement, mesh-sizing-function]
sources:
  - paper: doi:10.1016/j.gmod.2005.01.004
    title: Jean-Daniel Boissonnat and Steve Oudot, Provably good sampling and meshing of surfaces, Graphical Models 67(5), 2005, 405 to 451
    locator: Section 2 (surface Delaunay balls, Definition 2.2 of a loose epsilon-sample, Lemma 2.3), Section 2.3 (the constant epsilon_0, about 0.091), Theorems 4.3, 4.4 and 4.5 (manifold, homeomorphism and isotopy, Hausdorff distance at most 4.5 epsilon^2 times the largest d_M), Theorem 5.1 and Theorem 5.4 (lower and upper bounds on the size), Section 6 (the algorithm), Section 7 (persistent facets, Lemmas 7.1 and 7.2), Section 8 (Lemmas 8.1 to 8.4), Section 9.1 (removing skinny facets for angles below 30 degrees)
  - paper: doi:10.1145/160985.161150
    title: L. Paul Chew, Guaranteed-quality mesh generation for curved surfaces, Proceedings of the 9th Annual Symposium on Computational Geometry, 1993, 274 to 280
    locator: the surface mesher that inserts centers of large surface Delaunay balls (general locator)
  - book: isbn:9781584887300
    title: Siu-Wing Cheng, Tamal K. Dey and Jonathan Richard Shewchuk, Delaunay Mesh Generation, CRC Press, 2013
    locator: Chapter 13 (restricted Delaunay triangulations of surface samples, pages 287 to 316), Chapter 14 (meshing smooth surfaces and volumes, pages 317 to 348)
  - paper: doi:10.1137/060665889
    title: Siu-Wing Cheng, Tamal K. Dey, Edgar A. Ramos and Tathagata Ray, Sampling and meshing a surface with guaranteed topology and geometry, SIAM Journal on Computing 37(4), 2007, 1199 to 1227
    locator: refinement driven by the topological ball property instead of the local feature size (general locator)
  - paper: doi:10.1145/1137856.1137906
    title: Jean-Daniel Boissonnat and Steve Oudot, Provably good sampling and meshing of Lipschitz surfaces, Proceedings of the 22nd Annual Symposium on Computational Geometry, 2006, 337 to 346
    locator: the extension to surfaces that are only Lipschitz (general locator)
  - paper: doi:10.1142/S0218195997000223
    title: Herbert Edelsbrunner and Nimish R. Shah, Triangulating topological spaces, International Journal of Computational Geometry and Applications 7(4), 1997, 365 to 378
    locator: the restricted Delaunay triangulation and the closed ball property (general locator)
  - paper: doi:10.1007/PL00009475
    title: Nina Amenta and Marshall Bern, Surface reconstruction by Voronoi filtering, Discrete and Computational Geometry 22(4), 1999, 481 to 504
    locator: the local feature size and epsilon-samples; Theorem 2 on Voronoi faces that meet the surface for epsilon below 0.1
---

Delaunay refinement surface meshing builds a triangle mesh of a smooth closed surface $S$ by choosing points on $S$ one at a time. It keeps the 3D [Delaunay triangulation](/delaunay-triangulation/) of the points chosen so far and reads off the [restricted Delaunay triangulation](/restricted-delaunay-triangulation/): the triangles whose dual [Voronoi](/voronoi-diagram/) edge meets $S$. Each place where such an edge meets $S$ is the center of an empty ball that touches the three corners of the triangle. If the ball is larger than a user size $\sigma$ at its center, its center is added. Boissonnat and Oudot (2005) proved that the loop stops, and that with $\sigma$ below about $0.091$ times the local feature size, the output is homeomorphic to $S$ and close to it. The surface is used only through an oracle that intersects segments with it.

## In plain words

Scatter a few points on the surface. Build their 3D Delaunay triangulation, then ask, for each triangle, whether the line of points equally far from its three corners crosses the surface between the right limits. Where it does, a ball centered on the surface touches the three corners and contains no other point. A big ball means a big hole in the sample, so put a new point at its center and repeat. When every such ball is smaller than the size you asked for, the triangles you found form the mesh. The proof says that a small enough size gives the right shape. Tests show that much larger sizes still give the right shape, and that too large a size does not.

## The problem

The input is a smooth ($C^2$) closed surface $S \subset \mathbb{R}^3$ and a size function $\sigma : S \to \mathbb{R}$ that is positive and 1-Lipschitz. The surface is known through an *oracle* that, given a segment or a ray, returns the points where it meets $S$. The output is a finite sample $E \subset S$ and its restricted Delaunay triangulation $\mathrm{Del}|_S(E)$.

The *medial axis* of $S$ is the closure of the set of points with two or more nearest points on $S$, and $d_M(x)$ is the distance from $x \in S$ to it, also called the local feature size. Let $V(E)$ be the union of the Voronoi edges of $E$. For a triangle $f$ of the Delaunay triangulation whose dual Voronoi edge meets $S$ at $c$, the ball $B(c, r)$ through the corners of $f$ is a *surface Delaunay ball*. It contains no point of $E$ in its interior. Following Definition 2.2 of the paper, $E$ is a *loose $\varepsilon$-sample* when

1. every $x \in S \cap V(E)$ has a point of $E$ within $\varepsilon\, d_M(x)$, that is, every surface Delaunay ball has radius at most $\varepsilon\, d_M$ at its center, and
2. $\mathrm{Del}|_S(E)$ has a vertex on every connected component of $S$.

An $\varepsilon$-sample in the sense of Amenta and Bern, with every point of $S$ within $\varepsilon\, d_M$ of $E$, is a loose $\varepsilon$-sample when $\varepsilon < 0.1$ (Lemma 2.3).

This page makes three kinds of claim.

- *Proved bounds, cited.* Let $\varepsilon_0 \approx 0.091$ be the smallest positive $\varepsilon$ with $\frac{2\varepsilon}{1 - 8\varepsilon} + \arcsin\frac{\varepsilon}{1 - \varepsilon} \ge \frac{\pi}{4}$ (Section 2.3 of the paper). For a loose $\varepsilon$-sample with $\varepsilon \le \varepsilon_0$: $\mathrm{Del}|_S(E)$ is a 2-manifold without boundary (Theorem 4.3); the nearest point map $\pi$ restricted to it is a homeomorphism onto $S$, and the two are ambient isotopic (Theorem 4.4); the Hausdorff distance between them is at most $4.5\,\varepsilon^2 \sup_S d_M$ (Theorem 4.5); and $|E| \ge 2(1 - g) + \frac{2}{5\pi}\, \mu(S) / \varepsilon^2$, where $g$ is the genus and $\mu(S) = \iint_S d_M^{-2}$ (Theorem 5.1). For the algorithm: it terminates for every positive 1-Lipschitz $\sigma$ (Lemma 8.1); if $\sigma \le \varepsilon\, d_M$ the output is a loose $\varepsilon$-sample (Lemma 8.2); and if $\sigma \le d_M$ the points inserted by the loop number at most $\frac{64}{3\pi} \cdot 4 \iint_S \sigma^{-2} = \frac{256}{3\pi} \iint_S \sigma^{-2} \approx 27.2 \iint_S \sigma^{-2}$, since the proof of Lemma 8.3 shows they are $(\frac12, \sigma)$-sparse and Theorem 5.4 bounds a $(\kappa, \varphi)$-sparse sample by $\frac{64}{3\pi} \frac{1}{\kappa^2} \iint_S \varphi^{-2}$. So the topological guarantee needs $\sigma < 0.091\, d_M$.
- *Proved here.* The oracle used by the implementation answers exactly whether a Voronoi edge meets $S$; the dual Voronoi edge of a triangle is the segment between the circumcenters of its two tetrahedra, or a ray for a hull triangle; recomputing only the triangles of changed tetrahedra keeps $\mathrm{Del}|_S(E)$ correct; the loop stops even though new points are rounded to an integer grid; persistent facets survive. See `proofs/correctness.md`.
- *Measured, no guarantee.* On a sphere of radius $R$ ($d_M = R$) and a torus with tube radius $r$ and $R_{\text{torus}} = 3r$ ($d_M = r$), the output was a closed surface with the right Euler characteristic, every edge in two triangles, for every $\sigma$ tried: from $0.09R$ to $3R$ on the sphere, and from $0.5r$ to $1.5r$ on the torus, $16$ times the proved threshold. On the torus it failed at $\sigma = 2r$ for each of the five seeds tried. The sizes were well inside the proved bounds: at $\sigma = 0.09 R$ on the sphere the run gave $1050$ points, against the lower bound $2 + \frac{2}{5\pi} \cdot 4\pi / 0.0081 \approx 200$ and the upper bound $12 + \frac{256}{3\pi} \cdot 4\pi / 0.0081 \approx 42{,}000$. The proved constants are much worse than the measured ones.

## The algorithm

The mesher keeps the 3D Delaunay triangulation $D$ of $E$, with a ghost tetrahedron on each face of the convex hull, so that every triangle has two neighbors. For a triangle $f$ with neighbors $t_1, t_2$, the dual Voronoi edge is the segment between their circumcenters, or, if $t_2$ is a ghost, the ray from the circumcenter of $t_1$ along the outward normal of $f$. The oracle returns the points of $S$ on it.

```pseudo id=main
DELAUNAY-SURFACE-MESHING(S, σ)
L1  E ← for one or more seed points x on each component of S, three points of S near x that form a persistent facet
L2  D ← the Delaunay triangulation of E, with ghost tetrahedra on the hull faces
L3  for each triangle f of D: C(f) ← the points where the Voronoi edge dual to f meets S, found by the oracle
L4  while some triangle f has c in C(f) whose ball has radius r = |c - a| > σ(c), for a corner a of f:
L5      take the pair (f, c) with the largest r / σ(c)
L6      insert c into E and update D by Bowyer-Watson insertion
L7      recompute C(g) for each triangle g of a removed or new tetrahedron, and forget the triangles that are gone
L8  return E and Del|S(E), the triangles f with C(f) not empty
```

The paper takes the bad balls from a list in any order; picking the worst first is this implementation's choice. Line L1 follows Section 7 of the paper. Around each seed $x$, take a ball $B_x$ of radius below $\min\{\frac16 \mathrm{dist}(x, \text{other seeds}),\ d_M(x),\ \frac16 \sigma(x)\}$ and pick three points of $S \cap B_x$ such that the line through their circumcenter, normal to their plane, meets $S$ inside $B_x$. The resulting facet has a surface Delaunay ball of radius at most $\frac13 \sigma$; Lemma 7.1 shows such a *persistent facet* stays in $\mathrm{Del}|_S(E)$ to the end, which gives Condition 2.

The implementation meshes a sphere and a torus, both zero sets of a polynomial $F$ with integer coefficients. All points have integer coordinates. A circumcenter is $N / W$ with integer $N$ and $W$, so a Voronoi edge is the set of $(A + sB)/W$ for $s$ in $[0, 1]$ or $[0, \infty)$, and $W^d F((A + sB)/W)$ is a polynomial in $s$ with integer coefficients. A Sturm sequence counts its roots in the interval exactly; bisection then locates each root to within $\frac18$ of a unit, and the center is rounded to the grid. Orientation and insphere signs are exact integer computations. Radii and $\sigma$ are compared in floating point; this only decides which balls count as bad.

## Example

A sphere of radius $R = 2^{20}$ with $\sigma = R/2$ and seed 1. Four seeds at the corners of a randomly rotated regular tetrahedron give $12$ starting points. Their restricted Delaunay triangulation has $20$ triangles: the $4$ persistent facets, whose balls have $r / \sigma = 0.082$, and $16$ triangles with bad balls, the worst at $r / \sigma = 2.256$. Each row shows the state before the next insertion.

| insertions | points | triangles of Del\|S(E) | bad balls | worst r / σ |
|---:|---:|---:|---:|---:|
| 0 | 12 | 20 | 16 | 2.256 |
| 4 | 16 | 28 | 24 | 1.793 |
| 10 | 22 | 40 | 27 | 1.233 |
| 22 | 34 | 64 | 11 | 1.051 |
| 28 | 40 | 76 | 1 | 1.000 |
| 29 | 41 | 78 | 0 | none |

At every step the restricted triangulation is a triangulated sphere with $2V - 4$ triangles. The output has $41$ points, $78$ triangles and $117$ edges, each in exactly two triangles, so its Euler characteristic is $2$, and the $4$ persistent facets are still there. Every vertex is within one grid unit of $S$ (on a radius of about a million), and the triangles found from the Delaunay triangulation are exactly those found by testing every triple of points against the definition. Here $\sigma = 0.5\, d_M$, more than five times the proved threshold, so the topology is correct without a guarantee.

The torus with $R = 3 \cdot 2^{18}$ and $r = 2^{18}$ behaves the same at $\sigma = 1.5\, r$: $40$ points, $80$ triangles, Euler characteristic $0$. At $\sigma = 2r$ the loop stops after $20$ points with $30$ triangles, some edges in one, three or four triangles, and Euler characteristic $6$. The surface Delaunay balls are all small enough, yet the output is not a surface: the threshold matters, though the proved one is far too cautious.

## Correctness

Termination (Lemma 8.1): a point inserted as the center of a bad ball $B(c, r)$ is at distance $r > \sigma(c) \ge \sigma_0 = \min_S \sigma > 0$ from every earlier point, because the ball is empty. So the inserted points are $\sigma_0$ apart, and a compact surface has room for only finitely many of them. In the implementation the rounded point is at distance at least $r - \frac{\sqrt3}{2}$, so the same argument works whenever $\sigma_0 > \frac{\sqrt3}{2}$ grid units.

Output quality (Lemma 8.2): when the loop stops, no surface Delaunay ball is bad, so every one has $r \le \sigma(c)$. If $\sigma \le \varepsilon\, d_M$ this is Condition 1 of a loose $\varepsilon$-sample. Condition 2 comes from the persistent facets: if a later point $x$ fell inside a persistent ball $B(c_i, r_i)$ with $r_i \le \frac13 \sigma(c_i)$, then $\sigma(x) > \frac23 \sigma(c_i)$ by the Lipschitz condition, while a corner $v$ of the facet satisfies $|v - x| \le 2 r_i \le \frac23 \sigma(c_i) < \sigma(x)$, so $v$ would lie inside the bad ball centered at $x$, which is empty. With $\varepsilon \le 0.091$, Theorems 4.3 to 4.5 then give a manifold, homeomorphic and isotopic to $S$, within $4.5\,\varepsilon^2 \sup d_M$.

Bookkeeping: inserting a point changes only the tetrahedra of its cavity, and the dual Voronoi edge of a triangle depends only on its two tetrahedra. So only triangles of removed or new tetrahedra need a new oracle call. The proof file gives the details, including why the segment between the two circumcenters is the whole Voronoi edge.

The theorems assume $E \subset S$. The implementation's points are within $\frac{\sqrt3}{2} + \frac18$ grid units of $S$, so the theorems are not formally applied to it; the tests check the topology directly.

## Complexity

For $n$ output vertices, the 3D Delaunay triangulation has $O(n^2)$ tetrahedra in the worst case, so each insertion costs $O(n^2)$ and the loop costs $O(n^3)$ in the worst case, with $O(n^2)$ space. The oracle call per triangle costs a constant number of operations on numbers whose size grows with the coordinates. Samples of smooth surfaces behave much better than the worst case: in the runs above there were only a few tetrahedra per point. The scan for the worst ball adds $O(n)$ per insertion, which a priority queue would reduce. The sphere with $\sigma = 0.09R$ and $1050$ points took about $10$ seconds in Python.

The number of output points is $\Theta(\mu(S) / \varepsilon^2)$ when $\sigma = \varepsilon\, d_M$ with $\varepsilon \le 0.091$ (Lemma 8.4 and Theorem 5.1), so it is optimal up to a constant factor. On the sphere, with $\mu(S) = 4\pi$, the runs gave $41$, $106$, $382$ and $1050$ points for $\varepsilon = 0.5, 0.3, 0.15, 0.09$, which is $0.82$, $0.76$, $0.68$ and $0.68$ times $\mu(S) / \varepsilon^2$.

## Properties

- The output vertices are points of $S$ (in exact arithmetic), so no projection step is needed.
- $\sigma$ can vary over $S$. It must be 1-Lipschitz, and must stay below $0.091\, d_M$ where the guarantee is wanted.
- The algorithm needs only the oracle, not a parametrization, normals or curvature.
- The restricted triangulation contains every persistent facet from the start.
- Triangle shapes are not controlled by the basic loop. Section 9.1 of the paper adds a second pass that also calls a ball bad when its triangle has an angle below $\theta$, and proves termination for $\theta < 30°$.

## Variants and improvements

- Chew's 1993 mesher is the ancestor: it refines surface Delaunay balls by size and shape, without the sampling theory that gives the topological guarantee. The planar version is [Chew's second algorithm](/chew-second-algorithm/).
- Cheng, Dey, Ramos and Ray guarantee the topology without knowing $d_M$, by refining until the restricted Voronoi cells have the topological ball property, which Edelsbrunner and Shah's theorem turns into a homeomorphism.
- Boissonnat and Oudot extended the method to Lipschitz surfaces in 2006, and [protecting balls](/protecting-balls/) extend Delaunay refinement to surfaces with sharp edges and corners.
- Chapter 14 of Cheng, Dey and Shewchuk adds volume meshing: refine the tetrahedra inside $S$ as well, as in [tetrahedral Delaunay refinement](/tetrahedral-delaunay-refinement/).
- The CGAL library's former Surface_mesher package, by Laurent Rineau and Mariette Yvinec, states that it is mainly based on this work; it is deprecated since CGAL 6.0 in favor of the 3D Mesh Generation package.

## When to use it

Use it when the surface is given implicitly, as a level set, a CAD surface with an intersection routine, or anything else that can answer segment queries, and when a topological guarantee matters. For a fast mesh of a level set on a grid, [marching cubes](/marching-cubes/) and other [isosurface extraction](/isosurface-extraction/) methods are simpler but offer no shape or topology guarantee. For a parametric patch, [parametric surface meshing](/parametric-surface-meshing/) works in the parameter plane. For reconstruction from a fixed point cloud with no oracle, see [surface reconstruction](/surface-reconstruction/).

## Pitfalls

- With $\sigma$ too large the loop can stop with a non-manifold output, as the torus at $\sigma = 2r$ shows: every ball is small enough, yet triangles share edges three or four at a time. No check after the fact is built in.
- Without the persistent facets of Section 7, a sample with no restricted triangle on some component has no bad ball there, and the loop never reaches it.
- $d_M$ is rarely known for a real surface. A guessed $\sigma$ gives no guarantee; the variant of Cheng, Dey, Ramos and Ray avoids the guess.
- The intersection of a Voronoi edge with $S$ is a root of a polynomial or of a general function. Missing a root, or seeing a tangency as a crossing, changes $\mathrm{Del}|_S(E)$. Exact root counting avoids this for algebraic surfaces.
- The tetrahedra of $D$ are scaffolding, not a volume mesh: many are flat. A volume mesh needs its own refinement, and a radius-edge bound would not remove its slivers.
- A Voronoi vertex exactly on $S$, a Voronoi edge tangent to $S$, or five cospherical points are degenerate cases that the paper assumes away. The implementation raises an error when such a case would make a tetrahedron flat.

## Implementations

## History

Chew (1993) proposed meshing a curved surface by refining surface Delaunay balls. Edelsbrunner and Shah (1994, 1997) defined the restricted Delaunay triangulation and proved that the closed ball property makes it homeomorphic to the surface, and Amenta and Bern (1999) showed that for an $\varepsilon$-sample with $\varepsilon < 0.1$ every Voronoi face meets the surface in a topological ball or not at all. Boissonnat and Oudot (2005) introduced loose $\varepsilon$-samples, which a mesher can check on its own output, and proved that Chew-style refinement produces them with optimal size. Cheng, Dey, Ramos and Ray (2004, 2007) removed the need to know the local feature size, and the book of Cheng, Dey and Shewchuk (2013) gives the whole theory.

## References
